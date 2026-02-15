# Setup Windows Scheduled Task for OpenClaw Monitoring
# Run this once as Administrator to enable automatic health checks

$taskName = "OpenClaw Health Monitor"
$taskPath = "\OpenClaw\"

# Check if running as admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "WARNING: Run this script as Administrator for full functionality" -ForegroundColor Yellow
}

# Create the scheduled task
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File `"$env:USERPROFILE\.openclaw\workspace\scripts\contingency\monitor-openclaw.ps1`""
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration (New-TimeSpan -Days 9999)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# Register the task
try {
    Register-ScheduledTask -TaskName $taskName -TaskPath $taskPath -Action $action -Trigger $trigger -Settings $settings -Description "Monitors OpenClaw gateway health every 5 minutes" -Force
    Write-Host "SUCCESS: Scheduled task created!" -ForegroundColor Green
    Write-Host "Task: $taskPath$taskName"
    Write-Host "Interval: Every 5 minutes"
} catch {
    Write-Host "ERROR: Failed to create scheduled task: $_" -ForegroundColor Red
    Write-Host "You can manually add the task in Task Scheduler" -ForegroundColor Yellow
}

# Also register the Application event source if not exists
try {
    New-EventLog -LogName Application -Source "OpenClaw" -ErrorAction SilentlyContinue
    Write-Host "Event log source 'OpenClaw' registered" -ForegroundColor Green
} catch {
    # Already exists, ignore
}

Write-Host "`n=== Setup Complete ===" -ForegroundColor Cyan
Write-Host "Monitor script: $env:USERPROFILE\.openclaw\workspace\scripts\contingency\monitor-openclaw.ps1"
Write-Host "Restart script: $env:USERPROFILE\.openclaw\workspace\scripts\contingency\restart-openclaw.ps1"
Write-Host "Recovery prompt: $env:USERPROFILE\.openclaw\workspace\scripts\contingency\recovery-prompt.md"
