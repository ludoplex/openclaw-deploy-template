# sync-to-cloud.ps1 - Package local resources for cloud deployment
# Run from local machine to create deployment archive

$ErrorActionPreference = "Stop"

$WORKSPACE = "C:\Users\user\.openclaw\workspace"
$ARCHIVE_DIR = "C:\Users\user\.openclaw\deployment-package"
$TIMESTAMP = Get-Date -Format "yyyy-MM-dd-HHmm"

Write-Host "=== OpenClaw Cloud Deployment Packager ===" -ForegroundColor Cyan
Write-Host "Timestamp: $TIMESTAMP"

# Create archive directory
New-Item -ItemType Directory -Path $ARCHIVE_DIR -Force | Out-Null

# 1. Git push workspace
Write-Host "`n[1/5] Pushing workspace to git..." -ForegroundColor Yellow
Set-Location $WORKSPACE
git add -A
git commit -m "Pre-deployment sync $TIMESTAMP" -ErrorAction SilentlyContinue
git push origin master

# 2. Package Zoho API system (without tokens)
Write-Host "`n[2/5] Packaging Zoho API system..." -ForegroundColor Yellow
$zohoSrc = "C:\zoho-console-api-module-system"
$zohoDst = "$ARCHIVE_DIR\zoho-console-api-module-system"
if (Test-Path $zohoSrc) {
    Copy-Item -Path $zohoSrc -Destination $zohoDst -Recurse -Force
    # Remove sensitive files
    Remove-Item "$zohoDst\config\accounts.json" -ErrorAction SilentlyContinue
    Write-Host "  Copied (tokens excluded)"
}

# 3. Package rclone config template (tokens excluded)
Write-Host "`n[3/5] Creating rclone config template..." -ForegroundColor Yellow
$rcloneConf = "$env:APPDATA\rclone\rclone.conf"
if (Test-Path $rcloneConf) {
    $rcloneTemplate = @"
# rclone.conf template
# Replace TOKEN_PLACEHOLDER with actual token from secure vault

[onedrive]
type = onedrive
token = TOKEN_PLACEHOLDER
drive_id = 5582FE89C6C194BE
drive_type = personal
"@
    Set-Content -Path "$ARCHIVE_DIR\rclone.conf.template" -Value $rcloneTemplate
    Write-Host "  Template created (tokens excluded)"
}

# 4. Package agent workspaces
Write-Host "`n[4/5] Packaging agent workspaces..." -ForegroundColor Yellow
$agentsSrc = "C:\Users\user\.openclaw\agents"
$agentsDst = "$ARCHIVE_DIR\agents"
if (Test-Path $agentsSrc) {
    Copy-Item -Path $agentsSrc -Destination $agentsDst -Recurse -Force
    Write-Host "  Copied agent workspaces"
}

# 5. Create manifest
Write-Host "`n[5/5] Creating deployment manifest..." -ForegroundColor Yellow
$manifest = @{
    created = $TIMESTAMP
    source_machine = $env:COMPUTERNAME
    contents = @(
        "workspace (git repo)",
        "zoho-console-api-module-system",
        "rclone.conf.template",
        "agents"
    )
    secrets_needed = @(
        "zoho-console-api-module-system/config/accounts.json",
        "rclone.conf (with tokens)",
        "~/.openclaw/config.yaml"
    )
    git_repo = "https://github.com/ludoplex/openclaw-workspace"
}
$manifest | ConvertTo-Json -Depth 5 | Set-Content "$ARCHIVE_DIR\manifest.json"

# Create archive
Write-Host "`nCreating ZIP archive..." -ForegroundColor Yellow
$zipPath = "C:\Users\user\.openclaw\deployment-$TIMESTAMP.zip"
Compress-Archive -Path "$ARCHIVE_DIR\*" -DestinationPath $zipPath -Force

Write-Host "`n=== DONE ===" -ForegroundColor Green
Write-Host "Archive: $zipPath"
Write-Host "Size: $([math]::Round((Get-Item $zipPath).Length / 1MB, 2)) MB"
Write-Host "`nNext steps:"
Write-Host "1. Upload archive to cloud VM"
Write-Host "2. Extract and run setup"
Write-Host "3. Restore secrets from 1Password/Bitwarden"
