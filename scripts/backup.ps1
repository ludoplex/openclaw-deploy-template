# backup.ps1 - Backup workspace to local, OneDrive, and Google Drive
# Usage: .\scripts\backup.ps1
# Uses 7zip for reliable compression of large directories

$ErrorActionPreference = "Stop"
$timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
$src = "C:\Users\user\.openclaw\workspace"
$localBackup = "C:\Users\user\Backups"
$oneDriveBackup = "C:\Users\user\OneDrive\Backups"
$googleDriveBackup = "G:\My Drive\Backups\OpenClaw"
$backupName = "sop-dashboard-$timestamp"
$sevenZip = "C:\Program Files\7-Zip\7z.exe"

Write-Output "Starting backup: $backupName"

# Create zip directly with 7zip (excludes large dirs)
$zipPath = "$localBackup\$backupName.zip"
$excludes = "-xr!bin", "-xr!models", "-xr!__pycache__", "-xr!.git", "-xr!node_modules"

& $sevenZip a -tzip $zipPath "$src\*" $excludes -mx=5 | Out-Null

if ($LASTEXITCODE -ne 0) {
    Write-Error "7zip failed with exit code $LASTEXITCODE"
    exit 1
}

$size = "{0:N2} MB" -f ((Get-Item $zipPath).Length / 1MB)
Write-Output "Local backup: $zipPath ($size)"

# Copy to OneDrive
if (Test-Path $oneDriveBackup) {
    Copy-Item $zipPath $oneDriveBackup -Force
    Write-Output "Copied to OneDrive"
}

# Copy to Google Drive (non-fatal - GDrive sync can be flaky)
if (Test-Path $googleDriveBackup) {
    try {
        Copy-Item $zipPath $googleDriveBackup -Force -ErrorAction Stop
        Write-Output "Copied to Google Drive"
    } catch {
        Write-Output "WARNING: Google Drive copy failed (sync issue?) - skipping"
    }
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
