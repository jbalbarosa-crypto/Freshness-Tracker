# LAN Access Configuration Summary

## Your Network Configuration
- **LAN IP Address**: 192.168.141.171
- **Frontend URL**: http://192.168.141.171:3000
- **Backend URL**: http://192.168.141.171:8000

## What's Been Configured

### 1. Frontend (.env)
- `REACT_APP_API_URL=http://192.168.141.171:8000` - API calls go to LAN IP
- `REACT_APP_PUBLIC_URL=http://192.168.141.171:3000` - QR codes point to LAN IP

### 2. Backend (.env)
- `HOST=0.0.0.0` - Accepts connections from all network interfaces (including LAN)
- `PORT=8000` - Backend port
- `CORS_ORIGINS=http://localhost:3000,http://192.168.141.171:3000` - Allows both localhost and LAN access

### 3. QR Code Generation
- QR codes dynamically use the backend-detected LAN IP (Windows Wi‑Fi IP when available).
- Example format: `http://<your-lan-ip>:3000/batch/{id}`
- These URLs work when scanned from ANY device on your network (phones, tablets, etc.)

## How to Start the Application

### Start Backend (Terminal 1):
```bash
cd backend
python app.py
```
The backend will be accessible at: http://192.168.141.171:8000

### Start Frontend (Terminal 2):
```bash
cd frontend
npm start
```
The frontend will be accessible at: http://192.168.141.171:3000

## Testing

### From Your Computer:
- Open browser: http://192.168.141.171:3000 or http://localhost:3000

### From Other Devices (Phone/Tablet):
1. Make sure the device is on the SAME WiFi network
2. Open browser: http://192.168.141.171:3000
3. Or scan a QR code from the admin portal

### Scanning QR Codes:
1. Login to admin portal
2. Create a new batch
3. A QR code will be generated
4. Scan with phone camera - it will open: http://192.168.141.171:3000/batch/{id}
5. The batch freshness details will load from: http://192.168.141.171:8000/batches/{id}

## Troubleshooting

### If QR codes still show localhost:
1. Stop the frontend server (Ctrl+C)
2. Clear .env cache: `rm -rf node_modules/.cache`
3. Restart: `npm start`

### If other devices can't connect:
1. Check Windows Firewall - allow ports 3000 and 8000
2. Verify both devices are on the same network
3. Try pinging: `ping 192.168.141.171` from the other device
4. (WSL2 only) If backend runs inside WSL2 and phone can't reach it, set up a Windows portproxy (see section below).

### If your IP changes:
1. Run: `ip addr show` or `ipconfig` (Windows CMD)
2. Update both frontend/.env and backend/.env with new IP
3. Restart both servers

## Windows Firewall Rules (if needed)

Run in PowerShell as Administrator:
```powershell
# Allow Frontend Port
New-NetFirewallRule -DisplayName "Freshness Tracker Frontend" -Direction Inbound -LocalPort 3000 -Protocol TCP -Action Allow

# Allow Backend Port
New-NetFirewallRule -DisplayName "Freshness Tracker Backend" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```

## WSL2 Port Forwarding (Windows PortProxy)

If the backend is started inside WSL2, it listens on a virtual NAT IP (e.g. `172.x.x.x`) that's not directly reachable from other LAN devices. Your phone must hit the Windows host's Wi‑Fi IPv4 (e.g. `192.168.1.25`). To bridge the traffic you can either run the backend with native Windows Python, or create a port forward using `netsh interface portproxy`.

### Option A: Run backend on Windows directly (simplest)
```powershell
cd C:\Users\Drew\Desktop\Freshness-Tracker\backend
python app.py
```
This binds directly to the Wi‑Fi IP so phones can connect without extra steps.

### Option B: Keep backend in WSL2 + PortProxy
1. Start backend in WSL2 (binds `0.0.0.0:8000`).
2. Find Windows Wi‑Fi IPv4:
	```powershell
	ipconfig | findstr /i "Wireless" & ipconfig | findstr /i "IPv4"
	```
	(or just run `ipconfig` and note the "Wireless LAN adapter Wi‑Fi" -> IPv4 Address.)
3. Find WSL instance IPv4 (inside WSL):
	```bash
	hostname -I | awk '{print $1}'
	```
	Example: `172.29.112.113`.
4. Create portproxy (run in elevated Windows PowerShell / CMD):
	```powershell
	netsh interface portproxy add v4tov4 listenaddress=192.168.1.25 listenport=8000 connectaddress=172.29.112.113 connectport=8000
	```
5. (Firewall) Ensure an inbound allow rule for TCP 8000 exists (see above rules).
6. Test from phone: http://192.168.1.25:8000

### Verify PortProxy
```powershell
netsh interface portproxy show all
```
You should see the mapping from `192.168.1.25:8000` -> `172.29.112.113:8000`.

### Remove / Update
If your WSL IP changes (it often does after `wsl --shutdown`):
```powershell
netsh interface portproxy delete v4tov4 listenaddress=192.168.1.25 listenport=8000
netsh interface portproxy add v4tov4 listenaddress=192.168.1.25 listenport=8000 connectaddress=NEW_WSL_IP connectport=8000
```

### Common Issues
- "Connection refused": Backend not running or wrong `connectaddress`.
- "Timed out": Firewall blocking or incorrect Wi‑Fi IP.
- Works on laptop, not on phone: Phone on different network (guest / 5G) or captive portal.
- After reboot it breaks: WSL IP changed; recreate portproxy.

### Quick Checklist
- [ ] Backend running in WSL (`python app.py`) and shows binding.
- [ ] PortProxy rule points to current WSL IP.
- [ ] Firewall inbound rule for port 8000.
- [ ] Phone on same SSID.

Once this is set, the message: `From your phone, use: http://192.168.1.25:8000` will work.
