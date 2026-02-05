# should-use-claude.ps1 - Quick check: is this task Claude-worthy?
# Usage: .\scripts\should-use-claude.ps1 "generate a Python dataclass for user"

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Task
)

$LLMUrl = "http://127.0.0.1:8081/v1/chat/completions"

$prompt = @"
You are a task router. Classify this task:

Task: $Task

Rules:
- LLM: Simple code gen, formatting, JSON, boilerplate, single-file changes
- SHELL: File search, git commands, API calls (curl), bulk file ops
- LMARENA: Architecture decisions, design choices, planning (needs human review)
- CLAUDE: Multi-file refactoring, complex debugging, tool orchestration, security code

Reply with EXACTLY one word: LLM, SHELL, LMARENA, or CLAUDE
"@

$body = @{
    model = "local"
    messages = @(@{ role = "user"; content = $prompt })
    max_tokens = 10
    temperature = 0
} | ConvertTo-Json -Depth 3

try {
    $response = Invoke-WebRequest -Uri $LLMUrl -Method POST -Body $body `
        -ContentType "application/json" -UseBasicParsing -TimeoutSec 10
    $result = ($response.Content | ConvertFrom-Json).choices[0].message.content.Trim().ToUpper()
    
    $colors = @{
        "LLM" = "Green"
        "SHELL" = "Blue"
        "LMARENA" = "Yellow"
        "CLAUDE" = "Magenta"
    }
    
    $instructions = @{
        "LLM" = "Use local LLM for this task"
        "SHELL" = "Use shell tools (rg, git, curl, jq)"
        "LMARENA" = "Open https://lmarena.ai for multi-model comparison"
        "CLAUDE" = "[OK] This task is appropriate for Claude"
    }
    
    $color = $colors[$result]
    if (-not $color) { $color = "Gray"; $result = "UNKNOWN" }
    
    Write-Host "`n→ $result" -ForegroundColor $color
    Write-Host $instructions[$result] -ForegroundColor Gray
    
    return $result
    
} catch {
    Write-Host "[!] Local LLM offline - defaulting to checklist:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Is it simple code/format/JSON? -> LOCAL LLM"
    Write-Host "Is it file/git/API ops?        -> SHELL"
    Write-Host "Is it a design decision?       -> LMARENA"
    Write-Host "Is it complex/multi-step?      -> CLAUDE [OK]"
    return "UNKNOWN"
}
