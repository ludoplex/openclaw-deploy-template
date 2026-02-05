# setup.ps1 — OpenClaw Deploy Template Setup (Windows)
# Usage: .\setup.ps1
#
# Reads .env file and substitutes ${VAR} placeholders in openclaw.json
# with actual values. Also sets up the directory structure.

param(
    [string]$EnvFile = ".env",
    [string]$OpenClawHome = "$env:USERPROFILE\.openclaw"
)

$ErrorActionPreference = "Stop"

Write-Host "`n🦞 OpenClaw Deploy Template Setup" -ForegroundColor Cyan
Write-Host "=" * 50

# --- Check prerequisites ---
Write-Host "`n📋 Checking prerequisites..." -ForegroundColor Yellow

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Node.js not found. Install from https://nodejs.org (v20+)" -ForegroundColor Red
    exit 1
}
Write-Host "  ✅ Node.js $(node --version)"

$npmGlobalList = npm list -g --depth=0 2>&1
if ($npmGlobalList -notmatch "openclaw") {
    Write-Host "  ⚠️  OpenClaw not found globally. Install with: npm install -g openclaw" -ForegroundColor Yellow
} else {
    Write-Host "  ✅ OpenClaw installed"
}

# --- Load .env ---
Write-Host "`n📄 Loading environment from $EnvFile..." -ForegroundColor Yellow

if (-not (Test-Path $EnvFile)) {
    Write-Host "❌ $EnvFile not found. Copy .env.example to .env and fill in your values." -ForegroundColor Red
    exit 1
}

$envVars = @{}
Get-Content $EnvFile | ForEach-Object {
    $line = $_.Trim()
    if ($line -and -not $line.StartsWith("#")) {
        $parts = $line -split "=", 2
        if ($parts.Count -eq 2) {
            $envVars[$parts[0].Trim()] = $parts[1].Trim()
        }
    }
}

# Set OPENCLAW_HOME
if ($envVars.ContainsKey("OPENCLAW_HOME")) {
    $OpenClawHome = $envVars["OPENCLAW_HOME"]
}
$envVars["OPENCLAW_HOME"] = $OpenClawHome

Write-Host "  Loaded $($envVars.Count) variables"
Write-Host "  OpenClaw Home: $OpenClawHome"

# --- Validate required vars ---
$required = @("ANTHROPIC_API_KEY", "GATEWAY_TOKEN", "TELEGRAM_BOT_TOKEN", "TELEGRAM_ALLOWED_USER_ID")
$missing = @()
foreach ($key in $required) {
    if (-not $envVars.ContainsKey($key) -or $envVars[$key] -match "^\.\.\.|^your-|^123") {
        $missing += $key
    }
}

if ($missing.Count -gt 0) {
    Write-Host "`n⚠️  Missing or placeholder values for:" -ForegroundColor Yellow
    foreach ($m in $missing) {
        Write-Host "    - $m" -ForegroundColor Yellow
    }
    $continue = Read-Host "Continue anyway? (y/N)"
    if ($continue -ne "y") { exit 1 }
}

# --- Create directory structure ---
Write-Host "`n📁 Creating directory structure at $OpenClawHome..." -ForegroundColor Yellow

$dirs = @(
    "$OpenClawHome\workspace\patterns",
    "$OpenClawHome\workspace\scripts",
    "$OpenClawHome\workspace\hooks\workflow-enforcer",
    "$OpenClawHome\workspace\memory"
)

$agents = @('ops','webdev','cosmo','social','course','pearsonvue','ggleap','asm',
            'metaquest','neteng','roblox','cicd','testcov','seeker','sitecraft',
            'skillsmith','ballistics','climbibm','analyst')

foreach ($a in $agents) {
    $dirs += "$OpenClawHome\agents\$a\memory"
    $dirs += "$OpenClawHome\agents\$a\sessions"
}

foreach ($d in $dirs) {
    New-Item -ItemType Directory -Path $d -Force | Out-Null
}

# --- Copy and substitute openclaw.json ---
Write-Host "`n⚙️  Generating openclaw.json..." -ForegroundColor Yellow

$config = Get-Content "openclaw.json" -Raw

# Replace all ${VAR} patterns
foreach ($key in $envVars.Keys) {
    $config = $config -replace [regex]::Escape("`${$key}"), $envVars[$key]
}

# Fix path separators for Windows
$config = $config -replace '/', '\'

Set-Content "$OpenClawHome\openclaw.json" -Value $config -Encoding UTF8
Write-Host "  ✅ Written to $OpenClawHome\openclaw.json"

# --- Copy workspace files ---
Write-Host "`n📝 Copying workspace files..." -ForegroundColor Yellow

$workspaceFiles = @(
    "workspace\AGENTS.md",
    "workspace\SOUL.md",
    "workspace\USER.md",
    "workspace\IDENTITY.md",
    "workspace\HEARTBEAT.md",
    "workspace\BOOTSTRAP.md",
    "workspace\MEMORY.md",
    "workspace\WORKFLOW.md",
    "workspace\TOOLS.md",
    "workspace\patterns\RECURSIVE_REASONING.md",
    "workspace\scripts\backup.ps1",
    "workspace\scripts\task-router.ps1",
    "workspace\scripts\should-use-claude.ps1",
    "workspace\hooks\workflow-enforcer\handler.js",
    "workspace\hooks\workflow-enforcer\handler.ts",
    "workspace\hooks\workflow-enforcer\HOOK.md"
)

foreach ($f in $workspaceFiles) {
    $src = $f
    $dst = "$OpenClawHome\$f"
    if (Test-Path $src) {
        $dstDir = Split-Path $dst -Parent
        New-Item -ItemType Directory -Path $dstDir -Force | Out-Null
        Copy-Item $src $dst -Force
    }
}
Write-Host "  ✅ Workspace files copied"

# --- Copy agent files ---
Write-Host "`n🤖 Copying agent workspaces..." -ForegroundColor Yellow

Get-ChildItem "agents" -Directory | ForEach-Object {
    $agentDir = $_.FullName
    $agentName = $_.Name
    $targetDir = "$OpenClawHome\agents\$agentName"
    
    # Copy .md files (not in memory/ or sessions/)
    Get-ChildItem $agentDir -Filter "*.md" | ForEach-Object {
        Copy-Item $_.FullName "$targetDir\$($_.Name)" -Force
    }
    
    # Copy skills recursively
    $skillsDir = "$agentDir\skills"
    if (Test-Path $skillsDir) {
        Copy-Item $skillsDir "$targetDir\skills" -Recurse -Force
    }
    
    # Copy references and templates (skillsmith)
    foreach ($sub in @("references", "templates")) {
        $subDir = "$agentDir\$sub"
        if (Test-Path $subDir) {
            Copy-Item $subDir "$targetDir\$sub" -Recurse -Force
        }
    }
}
Write-Host "  ✅ Agent workspaces copied"

# --- Set ANTHROPIC_API_KEY env var ---
Write-Host "`n🔑 Setting ANTHROPIC_API_KEY environment variable..." -ForegroundColor Yellow
if ($envVars.ContainsKey("ANTHROPIC_API_KEY")) {
    [System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", $envVars["ANTHROPIC_API_KEY"], "User")
    Write-Host "  ✅ Set for current user"
}

# --- Done ---
Write-Host "`n✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Set ANTHROPIC_API_KEY: `$env:ANTHROPIC_API_KEY = 'sk-ant-...'" 
Write-Host "  2. Start the gateway: openclaw gateway start"
Write-Host "  3. Send a message to your Telegram bot"
Write-Host ""
Write-Host "For cloud deployment, see deploy/ directory." -ForegroundColor Gray
