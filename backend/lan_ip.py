"""Network and environment utilities for LAN access on Windows/WSL.

This module focuses on discovering a phone-accessible IPv4 and automating
Windows networking setup when running the backend inside WSL2.

Main capabilities:
- get_windows_wifi_ip(): Find the Windows Wi‑Fi adapter IPv4 (prefers 192.168.0/1.x).
- get_lan_ip(): Cross‑platform best‑effort LAN IPv4 (prefers 192.168.0/1.x).
- is_wsl(), get_wsl_ip(): Detect WSL and get the current WSL instance IPv4.
- ensure_portproxy(): Configure Windows portproxy to forward Wi‑Fi_IP:port → WSL_IP:port.
- ensure_firewall_port(): Ensure a Windows firewall inbound rule for a TCP port.
- update_env_var(), update_env_host(): Update backend/.env values.

Notes:
- "Real LAN" is treated as 192.168.0.x or 192.168.1.x to simplify mobile access.
- Portproxy/firewall helpers attempt elevation via PowerShell when needed.
"""

import os
import re
import subprocess
import socket
import platform
from pathlib import Path
from typing import Optional, Tuple

try:
    import psutil  # type: ignore
except ImportError:
    psutil = None

REAL_LAN_PATTERN = re.compile(r"^192\.168\.(0|1)\.[0-9]+$")
WIFI_SECTION_PATTERN = re.compile(r"Wireless LAN adapter.*Wi[- ]?Fi", re.IGNORECASE)
IP_LINE_PATTERN = re.compile(r"IPv4 Address[ .:]*([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)")

IPCONFIG_WSL_PATH = Path("/mnt/c/Windows/System32/ipconfig.exe")
NETSH_WSL_PATH = Path("/mnt/c/Windows/System32/netsh.exe")
POWERSHELL_WSL_PATH = Path("/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe")

def _is_real_lan_ip(ip: str) -> bool:
    """Return True if IPv4 is within 192.168.0.x or 192.168.1.x."""
    return bool(REAL_LAN_PATTERN.match(ip))


def _run_ipconfig() -> str:
    """Run Windows ipconfig (from WSL or native) and return stdout, else empty string."""
    cmd: list[str]
    if IPCONFIG_WSL_PATH.exists():
        cmd = [str(IPCONFIG_WSL_PATH)]
    else:
        cmd = ["ipconfig"]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        return result.stdout
    except Exception:
        return ""

def get_windows_wifi_ip() -> Optional[str]:
    """Find the Windows Wi‑Fi adapter IPv4 (prefers 192.168.0/1.x)."""
    output = _run_ipconfig()
    if not output:
        return None

    wifi_ip: Optional[str] = None
    any_real_lan: Optional[str] = None
    in_wifi = False

    for raw in output.splitlines():
        line = raw.strip()
        if WIFI_SECTION_PATTERN.search(raw):
            in_wifi = True
            continue
        if in_wifi:
            m = IP_LINE_PATTERN.search(raw)
            if m:
                ip = m.group(1)
                if _is_real_lan_ip(ip):
                    wifi_ip = ip
            if line == "":
                in_wifi = False
        m2 = IP_LINE_PATTERN.search(raw)
        if m2:
            ip2 = m2.group(1)
            if _is_real_lan_ip(ip2) and any_real_lan is None:
                any_real_lan = ip2

    return wifi_ip or any_real_lan

def get_lan_ip() -> Optional[str]:
    """Best‑effort LAN IPv4 detection with preference for 192.168.0/1.x."""
    system = platform.system().lower()
    if system == "windows":
        return get_windows_wifi_ip()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            if _is_real_lan_ip(ip):
                return ip
    except Exception:
        pass

    if psutil:
        try:
            for iface, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if getattr(addr, "family", None) == socket.AF_INET:
                        ip = addr.address
                        if _is_real_lan_ip(ip):
                            return ip
        except Exception:
            pass

    return None

def is_wsl() -> bool:
    """Return True when running inside a WSL environment."""
    try:
        return platform.system().lower() == "linux" and "microsoft" in platform.release().lower()
    except Exception:
        return False


def get_wsl_ip() -> Optional[str]:
    """Return the primary IPv4 of the WSL instance (typically 172.x.x.x)."""
    try:
        result = subprocess.run(["hostname", "-I"], capture_output=True, text=True, timeout=3)
        if result.stdout:
            parts = [p for p in result.stdout.strip().split() if re.match(r"^\d+\.\d+\.\d+\.\d+$", p)]
            if parts:
                return parts[0]
    except Exception:
        pass
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return None

def _netsh_available() -> bool:
    return NETSH_WSL_PATH.exists() or platform.system().lower() == "windows"


def _run_win(cmd: list[str], timeout: int = 8) -> Tuple[int, str, str]:
    """Run a Windows command from WSL or Windows. Returns (code, stdout, stderr)."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)


def ensure_portproxy(listen_ip: str, listen_port: int, connect_ip: str, connect_port: int) -> Tuple[bool, str]:
    """Ensure Windows portproxy forwards listen_ip:listen_port → connect_ip:connect_port.

    Attempts to delete conflicting mappings, add the rule, and elevate via PowerShell
    if necessary. Returns (ok, message).
    """
    if not _netsh_available():
        return False, "netsh not available"

    netsh = str(NETSH_WSL_PATH) if NETSH_WSL_PATH.exists() else "netsh"

    code, out, _ = _run_win([netsh, "interface", "portproxy", "show", "all"])
    if code == 0 and f"{listen_ip}:{listen_port}" in out and f"{connect_ip}:{connect_port}" in out:
        return True, "portproxy already configured"

    _run_win([netsh, "interface", "portproxy", "delete", "v4tov4",
              f"listenaddress={listen_ip}", f"listenport={listen_port}"])

    add_cmd = [netsh, "interface", "portproxy", "add", "v4tov4",
               f"listenaddress={listen_ip}", f"listenport={listen_port}",
               f"connectaddress={connect_ip}", f"connectport={connect_port}"]
    code, _, err = _run_win(add_cmd)
    if code == 0:
        return True, "portproxy configured"

    if POWERSHELL_WSL_PATH.exists():
        ps = str(POWERSHELL_WSL_PATH)
    else:
        ps = "powershell"
    arg_list = "interface portproxy add v4tov4 " \
               f"listenaddress={listen_ip} listenport={listen_port} " \
               f"connectaddress={connect_ip} connectport={connect_port}"
    elevate_cmd = [ps, "-NoProfile", "-Command",
                   f"Start-Process netsh -ArgumentList '{arg_list}' -Verb RunAs"]
    code2, _, err2 = _run_win(elevate_cmd, timeout=15)
    code3, out3, _ = _run_win([netsh, "interface", "portproxy", "show", "all"])
    if code3 == 0 and f"{listen_ip}:{listen_port}" in out3 and f"{connect_ip}:{connect_port}" in out3:
        return True, "portproxy configured (elevated)"
    return False, f"failed to configure portproxy: {err or err2}"


def ensure_firewall_port(port: int, name: str = "Freshness Tracker Backend") -> Tuple[bool, str]:
    """Ensure a Windows firewall inbound allow rule exists for the given TCP port."""
    if not _netsh_available():
        return False, "netsh not available"

    netsh = str(NETSH_WSL_PATH) if NETSH_WSL_PATH.exists() else "netsh"

    code, out, _ = _run_win([netsh, "advfirewall", "firewall", "show", "rule", f"name={name}"])
    if code == 0 and str(port) in out:
        return True, "firewall rule exists"

    add_cmd = [netsh, "advfirewall", "firewall", "add", "rule",
               f"name={name}", "dir=in", "action=allow", "protocol=TCP",
               f"localport={port}", "profile=any"]
    code, _, err = _run_win(add_cmd)
    if code == 0:
        return True, "firewall rule added"

    if POWERSHELL_WSL_PATH.exists():
        ps = str(POWERSHELL_WSL_PATH)
    else:
        ps = "powershell"
    arg_list = f"advfirewall firewall add rule name=\"{name}\" dir=in action=allow protocol=TCP localport={port} profile=any"
    elevate_cmd = [ps, "-NoProfile", "-Command",
                   f"Start-Process netsh -ArgumentList '{arg_list}' -Verb RunAs"]
    _run_win(elevate_cmd, timeout=15)
    code2, out2, _ = _run_win([netsh, "advfirewall", "firewall", "show", "rule", f"name={name}"])
    if code2 == 0 and str(port) in out2:
        return True, "firewall rule added (elevated)"
    return False, f"failed to add firewall rule: {err}"


# -------------------------
# .env helpers
# -------------------------

def _resolve_env_path(env_path: Optional[Path] = None) -> Path:
    """Resolve the .env path (defaults to backend/.env)."""
    if env_path is not None:
        return env_path
    return Path(__file__).parent / ".env"


def update_env_var(name: str, value: str, env_path: Optional[Path] = None) -> bool:
    """Create/update NAME=VALUE in .env. Returns True if file was written."""
    path = _resolve_env_path(env_path)
    lines: list[str] = []
    changed = False

    if path.exists():
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except Exception:
            lines = []

    out: list[str] = []
    found = False
    for line in lines:
        if line.strip().startswith("#") or "=" not in line:
            out.append(line)
            continue
        key, _, old_val = line.partition("=")
        if key.strip() == name:
            found = True
            if old_val != value:
                out.append(f"{name}={value}")
                changed = True
            else:
                out.append(line)
        else:
            out.append(line)

    if not found:
        out.append(f"{name}={value}")
        changed = True

    if changed or not path.exists():
        try:
            path.write_text("\n".join(out) + "\n", encoding="utf-8")
            return True
        except Exception:
            return False
    return False


def update_env_host(host: str, env_path: Optional[Path] = None) -> bool:
    """Update HOST in .env to the provided host."""
    return update_env_var("HOST", host, env_path)


__all__ = [
    "get_windows_wifi_ip",
    "get_lan_ip",
    "update_env_var",
    "update_env_host",
    "is_wsl",
    "get_wsl_ip",
    "ensure_portproxy",
    "ensure_firewall_port",
]
