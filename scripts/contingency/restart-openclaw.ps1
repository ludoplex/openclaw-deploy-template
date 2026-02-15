# Restart OpenClaw Gateway
# Can be run from PowerShell or triggered by Claude Code

param(
    [switch]$Force,
    [switch]$Verbose
)

$wslDistro = "Ubuntu"
$openclawPath = "/home/user/.openclaw/openclaw-2026.2.2/openclaw"

Write-Host "=== OpenClaw Gateway Restart ===" -ForegroundColor Cyan

# Step 1: Stop any existing gateway
Write-Host "Stopping existing gateway processes..."
wsl -d $wslDistro -- pkill -f "openclaw gateway" 2>$null
wsl -d $wslDistro -- pkill -f "node.*openclaw" 2>$null
Start-Sleep -Seconds 2

# Step 2: Start new gateway
Write-Host "Starting OpenClaw gateway..."
$startCmd = "cd /home/user/.openclaw/openclaw-2026.2.2 && nohup ./openclaw gateway > /tmp/openclaw-gateway.log 2>&1 &"
wsl -d $wslDistro -- bash -c $startCmd

Start-Sleep -Seconds 5

# Step 3: Verify
Write-Host "Verifying gateway status..."
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:18790/health" -TimeoutSec 10 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "SUCCESS: OpenClaw gateway is running!" -ForegroundColor Green
        
        # Remove down flag if exists
        $flagFile = "$env:USERPROFILE\.openclaw\workspace\OPENCLAW_DOWN.flag"
        if (Test-Path $flagFile) {
            Remove-Item $flagFile -Force
        }
        exit 0
    }
} catch {
    Write-Host "ERROR: Gateway failed to start. Check logs at /tmp/openclaw-gateway.log" -ForegroundColor Red
    Write-Host "Try running manually: wsl openclaw gateway" -ForegroundColor Yellow
    exit 1
}
