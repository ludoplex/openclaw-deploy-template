# OpenClaw Recovery - Paste This Into Claude Code

Peridot (OpenClaw AI assistant) appears to be down. Please help restore the service.

## Steps to recover:

1. First, check if the gateway is actually down:
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:18790/health" -TimeoutSec 5
```

2. If it fails, run the restart script:
```powershell
& "C:\Users\user\.openclaw\workspace\scripts\contingency\restart-openclaw.ps1"
```

3. If that doesn't work, try manual restart in WSL:
```bash
wsl -d Ubuntu
cd /home/user/.openclaw/openclaw-2026.2.2
./openclaw gateway
```

4. Check the logs if still failing:
```bash
wsl cat /tmp/openclaw-gateway.log
```

## Common Issues:

- **Port conflict:** Another process using 18790
  - Fix: `wsl lsof -i :18790` then kill the process
  
- **Node.js issue:** Missing dependencies
  - Fix: `wsl cd /home/user/.openclaw/openclaw-2026.2.2 && npm install`
  
- **Config error:** Bad JSON in openclaw.json
  - Fix: Check `/home/user/.openclaw/openclaw.json` for syntax errors

## After Recovery:

Once the gateway is running, Peridot will automatically reconnect to Telegram and resume operation. Send a message to verify.
