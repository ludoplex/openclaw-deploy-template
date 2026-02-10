# backup-debug.ps1 - Diagnose backup failure
$ErrorActionPreference = "Stop"

$timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
$src = "C:\Users\user\.openclaw\workspace"
$localBackup = "C:\Users\user\Backups"
$backupName = "sop-dashboard-$timestamp"
$temp = "$env:TEMP\$backupName"

Write-Output "=== BACKUP DEBUG ==="
Write-Output "Timestamp: $timestamp"
Write-Output "Source: $src"
Write-Output "Temp: $temp"
Write-Output "Dest: $localBackup"

try {
    Write-Output "`n[1] Creating temp directory..."
    New-Item -ItemType Directory -Path $temp -Force | Out-Null
    Write-Output "OK: $temp"
    
    Write-Output "`n[2] Getting files to copy..."
    $items = Get-ChildItem $src -Exclude "bin","models","__pycache__",".git","node_modules"
    Write-Output "Found $($items.Count) items"
    
    Write-Output "`n[3] Copying files..."
    foreach ($item in $items) {
        Write-Output "  -> $($item.Name)"
        Copy-Item $item.FullName -Destination $temp -Recurse -Force
    }
    Write-Output "Copy complete"
    
    Write-Output "`n[4] Creating zip..."
    $zipPath = "$localBackup\$backupName.zip"
    Compress-Archive -Path "$temp\*" -DestinationPath $zipPath -Force
    $size = "{0:N2} MB" -f ((Get-Item $zipPath).Length / 1MB)
    Write-Output "OK: $zipPath ($size)"
    
    Write-Output "`n[5] Cleanup temp..."
    Remove-Item $temp -Recurse -Force
    Write-Output "OK"
    
    Write-Output "`n=== BACKUP SUCCESS ==="
} catch {
    Write-Output "`n!!! ERROR !!!"
    Write-Output $_.Exception.Message
    Write-Output $_.ScriptStackTrace
    exit 1
}
