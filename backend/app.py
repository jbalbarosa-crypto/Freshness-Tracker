"""Freshness Tracker backend entrypoint.

Usage:
        python app.py

Behavior:
- Windows: binds to the Wi‑Fi adapter IPv4 when available, updating HOST in .env.
- WSL2: binds to 0.0.0.0 and attempts to configure Windows firewall and portproxy
    so phones can reach the API at http://<Windows_WiFi_IP>:<PORT>.

API docs: http://<host>:<port>/docs
"""

import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from database import engine, Base
from api.routers import batches, auth, users, config
from models.batch import Batch
from models.user import User
import platform
from lan_ip import (
    get_lan_ip,
    update_env_host,
    get_windows_wifi_ip,
    update_env_var,
    ensure_portproxy,
    ensure_firewall_port,
    is_wsl as _is_wsl,
    get_wsl_ip,
)

# Load environment variables from .env file
load_dotenv()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    api_title = os.getenv("API_TITLE", "Freshness Tracker API")
    api_version = os.getenv("API_VERSION", "1.0.0")
    cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")

    app = FastAPI(title=api_title, version=api_version)

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(auth.router)
    app.include_router(users.router)
    app.include_router(batches.router)
    app.include_router(config.router)

    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    return app


app = create_app()


if __name__ == "__main__":
    system = platform.system().lower()
    is_wsl = _is_wsl()

    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "True").lower() == "true"
    public_host = None

    host = None
    if system == "windows":
        wifi_ip = get_windows_wifi_ip()
        if wifi_ip:
            host = wifi_ip
            if update_env_host(host):
                print(f"[startup] Using Windows Wi‑Fi IPv4 for HOST: {host}")
            os.environ["HOST"] = host
        else:
            print("[startup] Could not detect Windows Wi‑Fi IPv4; falling back to detection/env")

    if is_wsl:
        public_host = get_windows_wifi_ip()
        if public_host:
            update_env_var("PUBLIC_HOST", public_host)
            os.environ["PUBLIC_HOST"] = public_host
            print(f"[startup] Detected Windows Wi‑Fi IP (PUBLIC_HOST): {public_host}")
        host = host or "0.0.0.0"
        # Try to auto-configure Windows portproxy + firewall so phones can reach the backend
        wsl_ip = get_wsl_ip()
        if public_host and wsl_ip:
            ok_fw, msg_fw = ensure_firewall_port(port)
            print(f"[startup] Firewall: {msg_fw}")
            ok_pp, msg_pp = ensure_portproxy(public_host, port, wsl_ip, port)
            print(f"[startup] PortProxy: {msg_pp}")
            if not ok_pp:
                print("[startup] If prompted with UAC, accept to complete the port forwarding.")

    if host is None:
        detected_ip = get_lan_ip()
        host = detected_ip or os.getenv("HOST", "0.0.0.0")
        if detected_ip:
            if update_env_host(host):
                print(f"[startup] Updated .env HOST={host}")
            os.environ["HOST"] = host
            print(f"[startup] Detected bindable LAN IP: {detected_ip}")
        else:
            print("[startup] Could not detect LAN IP; falling back to HOST env / 0.0.0.0")

    print(f"[startup] Binding backend to http://{host}:{port}")
    if is_wsl and public_host:
        print(f"[startup] From your phone, use: http://{public_host}:{port}")
    print("[startup] If phone can't reach, confirm: ipconfig IPv4 matches above, Firewall allows port, same Wi‑Fi network.")
    uvicorn.run("app:app", host=host, port=port, reload=reload)
