# Mighty House SOPs - Quick Sync Script
# Usage: .\sync.ps1 "Your commit message"
# Or just: .\sync.ps1  (uses default message with timestamp)

param(
    [string]$Message = ""
)

$ErrorActionPreference = "Continue"

Write-Host "=== Mighty House SOPs - Sync ===" -ForegroundColor Cyan

# Get current branch
$branch = git rev-parse --abbrev-ref HEAD 2>$null
if (-not $branch) {
    Write-Host "Error: Not a git repository. Run SETUP-GIT.bat first." -ForegroundColor Red
    exit 1
}

Write-Host "Branch: $branch" -ForegroundColor Gray

# Pull first
Write-Host "[1/3] Pulling latest changes..." -ForegroundColor Yellow
git pull origin $branch 2>&1 | Write-Host

# Stage changes
Write-Host "[2/3] Staging changes..." -ForegroundColor Yellow
git add -A

# Check if there are changes
$status = git status --porcelain
if (-not $status) {
    Write-Host "No changes to commit." -ForegroundColor Green
    exit 0
}

# Commit
Write-Host "[3/3] Committing and pushing..." -ForegroundColor Yellow
if (-not $Message) {
    $Message = "Update $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
}
git commit -m $Message

# Push
git push origin $branch

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Sync complete!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Push failed. Check your connection or run 'git status' for details." -ForegroundColor Red
}
