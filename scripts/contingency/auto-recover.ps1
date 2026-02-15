# Auto-Recovery: Prompt Claude Code to restart OpenClaw
# Uses SAFE clicks (avoids Cancel/Close buttons)

param(
    [switch]$DryRun,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

Write-Host "=== OpenClaw Auto-Recovery ===" -ForegroundColor Cyan

# Step 1: Check if recovery is needed
if (-not $Force) {
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:18790/health" -TimeoutSec 3 -UseBasicParsing
        Write-Host "OpenClaw gateway is HEALTHY - no recovery needed" -ForegroundColor Green
        exit 0
    } catch {
        Write-Host "OpenClaw is DOWN - initiating recovery" -ForegroundColor Yellow
    }
}

# Step 2: Safe-click Claude Code input (left-biased, avoid Cancel)
Write-Host "`nStep 1: Focusing Claude Code input area (LEFT side - safe)..."
$scriptPath = "$env:USERPROFILE\.openclaw\workspace\scripts\contingency\safe-click.ps1"

if ($DryRun) {
    & $scriptPath -WindowTitle "Claude" -Clicks 1 -SpreadPx 5 -DryRun
} else {
    & $scriptPath -WindowTitle "Claude" -Clicks 1 -SpreadPx 5
}

Start-Sleep -Seconds 1

# Step 3: Type recovery command (short, no risky characters)
Write-Host "`nStep 2: Typing recovery command..."

$recoveryMessage = "OpenClaw is down. Run this: wsl /home/user/.openclaw/openclaw-2026.2.2/openclaw gateway"

Add-Type -AssemblyName System.Windows.Forms

if (-not $DryRun) {
    # Type slowly and safely
    foreach ($char in $recoveryMessage.ToCharArray()) {
        $escaped = $char
        if ($char -match '[\+\^\%\~\(\)\{\}\[\]]') {
            $escaped = "{$char}"
        }
        [System.Windows.Forms.SendKeys]::SendWait($escaped)
        Start-Sleep -Milliseconds 20
    }
    
    Write-Host "Message typed" -ForegroundColor Green
    
    # Don't auto-press Enter - let Claude Code user decide
    Write-Host "`nRecovery message ready. Press Enter in Claude Code to send." -ForegroundColor Yellow
} else {
    Write-Host "[DRY RUN] Would type: $recoveryMessage" -ForegroundColor Gray
}

Write-Host "`n=== Recovery initiated ===" -ForegroundColor Cyan
