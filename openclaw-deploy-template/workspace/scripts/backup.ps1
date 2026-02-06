# backup.ps1 - Backup workspace to local, OneDrive, and Google Drive
# Usage: .\scripts\backup.ps1

$timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
$src = "C:\Users\user\.openclaw\workspace"
$localBackup = "C:\Users\user\Backups"
$oneDriveBackup = "C:\Users\user\OneDrive\Backups"
$googleDriveBackup = "G:\My Drive\Backups\OpenClaw"
$backupName = "sop-dashboard-$timestamp"

Write-Output "Starting backup: $backupName"

# Create temp directory (exclude large files)
$temp = "$env:TEMP\$backupName"
New-Item -ItemType Directory -Path $temp -Force | Out-Null

# Copy files (exclude bin, models, __pycache__, .git, node_modules)
Get-ChildItem $src -Exclude "bin","models","__pycache__",".git","node_modules" | Copy-Item -Destination $temp -Recurse -Force

# Create zip
$zipPath = "$localBackup\$backupName.zip"
Compress-Archive -Path $temp -DestinationPath $zipPath -Force

# Cleanup temp
Remove-Item $temp -Recurse -Force

$size = "{0:N2} MB" -f ((Get-Item $zipPath).Length / 1MB)
Write-Output "Local backup: $zipPath ($size)"

# Copy to OneDrive
if (Test-Path $oneDriveBackup) {
    Copy-Item $zipPath $oneDriveBackup -Force
    Write-Output "Copied to OneDrive"
}

# Copy to Google Drive
if (Test-Path $googleDriveBackup) {
    Copy-Item $zipPath $googleDriveBackup -Force
    Write-Output "Copied to Google Drive"
}

# Cleanup old backups (keep last 10 in each location)
Get-ChildItem "$localBackup\sop-dashboard-*.zip" | Sort-Object CreationTime -Descending | Select-Object -Skip 10 | Remove-Item -Force
if (Test-Path $oneDriveBackup) {
    Get-ChildItem "$oneDriveBackup\sop-dashboard-*.zip" -ErrorAction SilentlyContinue | Sort-Object CreationTime -Descending | Select-Object -Skip 10 | Remove-Item -Force
}
if (Test-Path $googleDriveBackup) {
    Get-ChildItem "$googleDriveBackup\sop-dashboard-*.zip" -ErrorAction SilentlyContinue | Sort-Object CreationTime -Descending | Select-Object -Skip 10 | Remove-Item -Force
}

Write-Output "Backup complete!"
