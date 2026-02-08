<#
.SYNOPSIS
    Export LLM chat sessions from Arena.ai, Perplexity, ChatGPT
    
.DESCRIPTION
    Since direct CDP is auth-blocked, this script:
    1. Uses clipboard-based extraction
    2. Guides user through manual export where needed
    3. Saves to structured files
#>

$OutputDir = "$PSScriptRoot\..\llm-exports"
$Timestamp = Get-Date -Format "yyyy-MM-dd_HHmm"

# Create output directory
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

Write-Host @"

===================================
  LLM Session Exporter
===================================

Since browser automation is limited by auth, here are your options:

1. ARENA.AI / LMARENA.AI:
   - Go to https://arena.ai or https://lmarena.ai
   - Open Settings/Profile
   - Look for "Export" or "Download Data" option
   - If none exists, manually copy conversations

2. PERPLEXITY.AI:
   - Go to https://perplexity.ai/library
   - Each thread has a "..." menu with "Copy" option
   - Or use browser extension to bulk export

3. CHATGPT:
   - Go to https://chat.openai.com
   - Settings > Data controls > Export data
   - They'll email you a download link

4. MANUAL CLIPBOARD METHOD:
   - Open each conversation
   - Ctrl+A, Ctrl+C (select all, copy)
   - Run: Get-Clipboard | Out-File "$OutputDir\session-name.txt"

===================================
"@

# Check for any API keys that might enable direct export
$EnvKeys = @(
    "OPENAI_API_KEY",
    "PERPLEXITY_API_KEY",
    "ANTHROPIC_API_KEY"
)

Write-Host "`nChecking for API keys that might enable direct export..."
foreach ($key in $EnvKeys) {
    $val = [Environment]::GetEnvironmentVariable($key)
    if ($val) {
        Write-Host "  Found: $key" -ForegroundColor Green
    }
}

Write-Host "`nOutput directory: $OutputDir"
Write-Host "Timestamp: $Timestamp"

# Create a manifest file to track exports
$Manifest = @{
    timestamp = $Timestamp
    exports = @()
}

$ManifestPath = "$OutputDir\manifest_$Timestamp.json"
$Manifest | ConvertTo-Json | Out-File $ManifestPath

Write-Host "`nManifest created: $ManifestPath"
Write-Host "`nRun the following to save clipboard content:"
Write-Host "  Get-Clipboard | Out-File `"$OutputDir\session-NAME.txt`"" -ForegroundColor Cyan
