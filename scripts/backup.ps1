# backup.ps1 - Backup workspace to local and OneDrive
# Usage: .\scripts\backup.ps1

$timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
$src = "C:\Users\user\.openclaw\workspace"
$localBackup = "C:\Users\user\Backups"
$oneDriveBackup = "C:\Users\user\OneDrive\Backups"
$backupName = "sop-dashboard-$timestamp"

# Create temp directory (exclude large files)
$temp = "$env:TEMP\$backupName"
New-Item -ItemType Directory -Path $temp -Force | Out-Null

# Copy files (exclude bin, models, __pycache__, .git)
Get-ChildItem $src -Exclude "bin","models","__pycache__",".git" | Copy-Item -Destination $temp -Recurse -Force

# Create zip
$zipPath = "$localBackup\$backupName.zip"
Compress-Archive -Path $temp -DestinationPath $zipPath -Force

# Cleanup temp
Remove-Item $temp -Recurse -Force

# Copy to OneDrive
if (Test-Path $oneDriveBackup) {
    Copy-Item $zipPath $oneDriveBackup -Force
    Write-Output "Backup saved to OneDrive: $backupName.zip"
} else {
    Write-Output "OneDrive backup folder not found, local only"
}

# Show result
$size = "{0:N2} MB" -f ((Get-Item $zipPath).Length / 1MB)
Write-Output "Local backup: $zipPath ($size)"

# Cleanup old backups (keep last 10)
Get-ChildItem "$localBackup\sop-dashboard-*.zip" | Sort-Object CreationTime -Descending | Select-Object -Skip 10 | Remove-Item -Force
