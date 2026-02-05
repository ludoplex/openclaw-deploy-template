# backup.ps1 - Backup workspace to local and cloud storage
# Usage: .\scripts\backup.ps1

$timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
$src = "$env:USERPROFILE\.openclaw\workspace"
$localBackup = "$env:USERPROFILE\Backups"
$backupName = "openclaw-backup-$timestamp"

Write-Output "Starting backup: $backupName"

# Create local backup dir
New-Item -ItemType Directory -Path $localBackup -Force | Out-Null

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

# Cleanup old backups (keep last 10)
Get-ChildItem "$localBackup\openclaw-backup-*.zip" | Sort-Object CreationTime -Descending | Select-Object -Skip 10 | Remove-Item -Force

Write-Output "Backup complete!"
