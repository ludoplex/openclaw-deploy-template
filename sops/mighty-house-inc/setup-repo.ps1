# Mighty House SOPs - Repository Setup Script
# Run this script to initialize git and push to GitHub

$ErrorActionPreference = "Stop"
$repoPath = $PSScriptRoot
$repoName = "mighty-house-sops"
$backupPath = "$env:USERPROFILE\Backups\$repoName-backup"

Write-Host "=== Mighty House SOPs - Repository Setup ===" -ForegroundColor Cyan
Write-Host ""

# Step 1: Initialize Git if not already
Write-Host "[1/5] Initializing Git repository..." -ForegroundColor Yellow
Set-Location $repoPath

if (-not (Test-Path ".git")) {
    git init
    Write-Host "  Git initialized." -ForegroundColor Green
} else {
    Write-Host "  Git already initialized." -ForegroundColor Green
}

# Step 2: Create .gitignore if needed
if (-not (Test-Path ".gitignore")) {
    @"
# OS files
.DS_Store
Thumbs.db
desktop.ini

# Editor files
*.swp
*.swo
*~
.vscode/
.idea/

# Temp files
*.tmp
*.bak
*.log

# Local config (if any)
.env
.env.local
"@ | Out-File -FilePath ".gitignore" -Encoding utf8
    Write-Host "  Created .gitignore" -ForegroundColor Green
}

# Step 3: Stage and commit all files
Write-Host "[2/5] Staging and committing files..." -ForegroundColor Yellow
git add -A
$commitMessage = "Initial commit: Mighty House Inc. SOPs and Marketing Materials"
git commit -m $commitMessage 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "  Committed successfully." -ForegroundColor Green
} else {
    Write-Host "  No new changes to commit or already committed." -ForegroundColor Yellow
}

# Step 4: Create local backup
Write-Host "[3/5] Creating local backup..." -ForegroundColor Yellow
$backupDir = "$env:USERPROFILE\Backups"
if (-not (Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
}

$timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
$backupZip = "$backupDir\$repoName-$timestamp.zip"

# Create zip backup
Compress-Archive -Path "$repoPath\*" -DestinationPath $backupZip -Force
Write-Host "  Local backup created: $backupZip" -ForegroundColor Green

# Step 5: Create GitHub repository and push
Write-Host "[4/5] Creating GitHub repository..." -ForegroundColor Yellow

# Check gh auth
$authStatus = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ERROR: GitHub CLI not authenticated. Run 'gh auth login' first." -ForegroundColor Red
    exit 1
}

# Create repo (private by default)
$repoCreateResult = gh repo create $repoName --private --source=. --remote=origin --push 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  GitHub repository created and pushed!" -ForegroundColor Green
} else {
    # Repo might already exist, try to add remote and push
    Write-Host "  Repo may exist, attempting to connect..." -ForegroundColor Yellow

    # Get GitHub username
    $ghUser = gh api user --jq '.login' 2>$null

    # Check if remote exists
    $remotes = git remote
    if ($remotes -notcontains "origin") {
        git remote add origin "https://github.com/$ghUser/$repoName.git"
    }

    # Push
    git branch -M main
    git push -u origin main --force

    if ($LASTEXITCODE -eq 0) {
        Write-Host "  Pushed to existing repository!" -ForegroundColor Green
    } else {
        Write-Host "  Push failed. You may need to create the repo manually on GitHub." -ForegroundColor Red
    }
}

# Step 5: Show clone instructions
Write-Host ""
Write-Host "[5/5] Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "=== To clone on other devices ===" -ForegroundColor Cyan
$ghUser = gh api user --jq '.login' 2>$null
if ($ghUser) {
    Write-Host "  git clone https://github.com/$ghUser/$repoName.git" -ForegroundColor White
    Write-Host ""
    Write-Host "  Or with SSH:" -ForegroundColor Gray
    Write-Host "  git clone git@github.com:$ghUser/$repoName.git" -ForegroundColor White
}
Write-Host ""
Write-Host "=== Local backup location ===" -ForegroundColor Cyan
Write-Host "  $backupZip" -ForegroundColor White
Write-Host ""
Write-Host "=== Quick commands ===" -ForegroundColor Cyan
Write-Host "  Pull updates:  git pull origin main" -ForegroundColor White
Write-Host "  Push changes:  git add -A && git commit -m 'Update' && git push" -ForegroundColor White
Write-Host ""
