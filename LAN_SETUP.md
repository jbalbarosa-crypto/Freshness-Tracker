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
- QR codes now generate URLs like: `http://192.168.141.171:3000/batch/{id}`
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
