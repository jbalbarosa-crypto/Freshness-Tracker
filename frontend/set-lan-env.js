const os = require('os');
const fs = require('fs');
const path = require('path');


function getWifiIP() {
  const interfaces = os.networkInterfaces();
  for (const name of Object.keys(interfaces)) {
    // Look for Wi-Fi or Wireless LAN adapter
    if (/wi[-]?fi|wireless/i.test(name)) {
      for (const iface of interfaces[name]) {
        if (iface.family === 'IPv4' && !iface.internal) {
          return iface.address;
        }
      }
    }
  }
  // Fallback: first non-internal IPv4
  for (const name of Object.keys(interfaces)) {
    for (const iface of interfaces[name]) {
      if (iface.family === 'IPv4' && !iface.internal) {
        return iface.address;
      }
    }
  }
  return null;
}

const ip = getWifiIP();
if (!ip) {
  console.error('No Wi-Fi/Wireless LAN IPv4 address found. Please check your network connection.');
  process.exit(1);
}

const envPath = path.join(__dirname, '.env');
let envContent = fs.readFileSync(envPath, 'utf8');

// Replace REACT_APP_API_URL and REACT_APP_PUBLIC_URL
envContent = envContent.replace(/REACT_APP_API_URL=.*/g, `REACT_APP_API_URL=http://${ip}:8000`);
envContent = envContent.replace(/REACT_APP_PUBLIC_URL=.*/g, `REACT_APP_PUBLIC_URL=http://${ip}:3000`);

fs.writeFileSync(envPath, envContent, 'utf8');
console.log(`Set REACT_APP_API_URL and REACT_APP_PUBLIC_URL to http://${ip}`);
