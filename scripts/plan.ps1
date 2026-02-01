<#
.SYNOPSIS
    Open lmarena.ai for multi-model planning session

.DESCRIPTION
    Opens lmarena.ai in side-by-side mode and optionally copies
    a planning prompt to clipboard.

.PARAMETER Task
    Brief description of the task to plan

.PARAMETER Constraints
    Technical constraints (comma-separated)

.EXAMPLE
    .\plan.ps1 -Task "Design caching layer" -Constraints "Redis, Laravel, 10k rps"
#>

param(
    [string]$Task = "",
    [string]$Constraints = ""
)

$url = "https://lmarena.ai/?side-by-side"

if ($Task) {
    $prompt = @"
Task: $Task
$(if ($Constraints) { "Constraints: $Constraints" })

I need help planning the approach. Please consider:
1. Architecture patterns that fit this use case
2. Potential edge cases and how to handle them
3. Error handling strategy
4. Testing approach
5. Performance considerations

What's the best way to implement this?
"@

    # Copy to clipboard
    $prompt | Set-Clipboard
    Write-Host "📋 Planning prompt copied to clipboard!" -ForegroundColor Green
    Write-Host "`nPrompt:" -ForegroundColor Cyan
    Write-Host $prompt -ForegroundColor White
}

Write-Host "`n🚀 Opening lmarena.ai..." -ForegroundColor Cyan
Start-Process $url

Write-Host @"

Tips:
- Select different models in each pane (GPT 5.2, Claude Opus 4.5, Gemini)
- Paste the prompt (Ctrl+V) and compare responses
- Extract best ideas from each model
- Document decision in memory/$(Get-Date -Format 'yyyy-MM-dd').md

"@ -ForegroundColor Yellow
