# task-router.ps1 - Route tasks to appropriate tools (Local LLM, lmarena, Claude)
# Run before starting any task: .\scripts\task-router.ps1

param(
    [Parameter(Position=0)]
    [string]$TaskDescription
)

$LLMUrl = "http://127.0.0.1:8081"

function Test-LLMAvailable {
    try {
        $response = Invoke-WebRequest -Uri "$LLMUrl/health" -TimeoutSec 2 -UseBasicParsing
        return $true
    } catch {
        return $false
    }
}

function Ask-LLM {
    param([string]$Prompt, [int]$MaxTokens = 500)
    
    $body = @{
        model = "local"
        messages = @(@{ role = "user"; content = $Prompt })
        max_tokens = $MaxTokens
        temperature = 0.7
    } | ConvertTo-Json -Depth 3
    
    try {
        $response = Invoke-WebRequest -Uri "$LLMUrl/v1/chat/completions" `
            -Method POST -Body $body -ContentType "application/json" -UseBasicParsing
        $result = $response.Content | ConvertFrom-Json
        return $result.choices[0].message.content
    } catch {
        return $null
    }
}

function Show-Menu {
    Write-Host "`n🔀 TASK ROUTER - What are you trying to do?" -ForegroundColor Cyan
    Write-Host "=" * 50
    Write-Host "1. Generate boilerplate/simple code"
    Write-Host "2. Format/transform text or data"
    Write-Host "3. Architecture/planning decision"
    Write-Host "4. Complex reasoning/multi-step task"
    Write-Host "5. File operations (search, rename, etc.)"
    Write-Host "6. Git/GitHub operations"
    Write-Host "7. API testing"
    Write-Host "8. Check task routing for description"
    Write-Host "Q. Quit"
    Write-Host ""
}

function Route-Task {
    param([string]$Choice)
    
    switch ($Choice) {
        "1" {
            Write-Host "`n✅ USE: Local LLM" -ForegroundColor Green
            Write-Host "Use your local LLM server for simple code generation."
            if (Test-LLMAvailable) {
                Write-Host "`n🟢 Local LLM is ONLINE at $LLMUrl" -ForegroundColor Green
            } else {
                Write-Host "`n🔴 Local LLM is OFFLINE - start it first" -ForegroundColor Red
            }
        }
        "2" {
            Write-Host "`n✅ USE: Local LLM or shell tools" -ForegroundColor Green
            Write-Host "Shell: jq, sed, awk, PowerShell"
            Write-Host "LLM: For text formatting and summarization"
        }
        "3" {
            Write-Host "`n✅ USE: lmarena.ai (multi-model)" -ForegroundColor Yellow
            Write-Host "URL: https://lmarena.ai"
            Write-Host "`nOpen side-by-side mode, compare multiple models"
            Write-Host "Document decision in memory/$(Get-Date -Format 'yyyy-MM-dd').md"
            Start-Process "https://lmarena.ai"
        }
        "4" {
            Write-Host "`n✅ USE: Claude (appropriate for complex tasks)" -ForegroundColor Magenta
            Write-Host "This is the right tool for:"
            Write-Host "  - Multi-file refactoring"
            Write-Host "  - Complex debugging"
            Write-Host "  - Tool orchestration"
            Write-Host "  - Security-sensitive code"
        }
        "5" {
            Write-Host "`n✅ USE: Shell tools" -ForegroundColor Blue
            Write-Host "Search: rg, fd, grep, Get-ChildItem"
            Write-Host "Transform: sed, awk, ForEach-Object"
            Write-Host "Bulk: PowerShell loops"
        }
        "6" {
            Write-Host "`n✅ USE: git / gh CLI" -ForegroundColor Blue
            Write-Host "git status, git diff, git log"
            Write-Host "gh pr list, gh issue create, gh run list"
        }
        "7" {
            Write-Host "`n✅ USE: curl / Invoke-WebRequest" -ForegroundColor Blue
            Write-Host "curl -s http://localhost:8080/api/status | jq"
            Write-Host "Invoke-WebRequest -Uri ... | Select Content"
        }
        "8" {
            $desc = if ($TaskDescription) { $TaskDescription } else {
                Read-Host "Describe the task"
            }
            Route-ByDescription $desc
        }
    }
}

function Route-ByDescription {
    param([string]$Description)
    
    Write-Host "`nAnalyzing task..." -ForegroundColor Gray
    
    $lower = $Description.ToLower()
    
    if ($lower -match "generat|creat|boilerplate|scaffold|template") {
        Write-Host "`n🎯 ROUTED TO: Local LLM" -ForegroundColor Green
        Route-Task "1"
    }
    elseif ($lower -match "format|transform|convert|parse|extract") {
        Write-Host "`n🎯 ROUTED TO: LLM or Shell" -ForegroundColor Green
        Route-Task "2"
    }
    elseif ($lower -match "architect|design|plan|approach|decide|best way") {
        Write-Host "`n🎯 ROUTED TO: lmarena.ai" -ForegroundColor Yellow
        Route-Task "3"
    }
    elseif ($lower -match "search|find|grep|list files") {
        Write-Host "`n🎯 ROUTED TO: Shell tools" -ForegroundColor Blue
        Route-Task "5"
    }
    elseif ($lower -match "git|commit|push|pull|pr|branch") {
        Write-Host "`n🎯 ROUTED TO: git/gh CLI" -ForegroundColor Blue
        Route-Task "6"
    }
    elseif ($lower -match "debug|refactor|complex|integrate|orchestrat") {
        Write-Host "`n🎯 ROUTED TO: Claude" -ForegroundColor Magenta
        Route-Task "4"
    }
    else {
        Write-Host "`n🤔 Unclear routing" -ForegroundColor Gray
        if (Test-LLMAvailable) {
            $routePrompt = @"
Classify this task into ONE category:
- LLM: simple code gen, formatting, boilerplate
- SHELL: file ops, git, search, API calls
- LMARENA: architecture, planning, decisions
- CLAUDE: complex reasoning, multi-step, debugging

Task: $Description

Reply with just the category name (LLM/SHELL/LMARENA/CLAUDE):
"@
            $result = Ask-LLM $routePrompt 20
            Write-Host "Local LLM suggests: $result" -ForegroundColor Cyan
        } else {
            Write-Host "Start with local LLM, escalate to Claude if needed" -ForegroundColor Yellow
        }
    }
}

# Main
if ($TaskDescription) {
    Route-ByDescription $TaskDescription
} else {
    do {
        Show-Menu
        $choice = Read-Host "Select option"
        if ($choice -ne "Q" -and $choice -ne "q") {
            Route-Task $choice
        }
    } while ($choice -ne "Q" -and $choice -ne "q")
}

Write-Host "`n💡 Remember: Cheapest tool first, escalate when needed" -ForegroundColor Gray
