# Monitor OpenClaw Gateway Health
# Run this as a scheduled task every 5 minutes

$gatewayUrl = "http://127.0.0.1:18790/health"
$flagFile = "$env:USERPROFILE\.openclaw\workspace\OPENCLAW_DOWN.flag"

try {
    $response = Invoke-WebRequest -Uri $gatewayUrl -TimeoutSec 5 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        # Gateway healthy - remove flag if exists
        if (Test-Path $flagFile) {
            Remove-Item $flagFile -Force
        }
        Write-Host "OpenClaw gateway is healthy"
        exit 0
    }
} catch {
    # Gateway unreachable - create flag
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "OpenClaw gateway down at $timestamp" | Out-File $flagFile -Encoding UTF8
    Write-Host "WARNING: OpenClaw gateway is DOWN!"
    
    # Log to event
    Write-EventLog -LogName Application -Source "OpenClaw" -EventId 1001 -EntryType Warning -Message "OpenClaw gateway unreachable at $timestamp" -ErrorAction SilentlyContinue
    
    exit 1
}
