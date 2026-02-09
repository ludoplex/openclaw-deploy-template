<# 
.SYNOPSIS
    Swiss Rounds Synthesis workflow manager

.DESCRIPTION
    Manages multi-agent deliberation with cross-examination, retrospectives, 
    and triad validation before PM synthesis.

.PARAMETER Action
    start, status, advance, validate, abort

.PARAMETER Project
    Project name (required for start)

.PARAMETER Specialists
    Comma-separated list of specialist agent IDs (default: analyst,ballistics,cosmo,seeker)

.EXAMPLE
    .\swiss-rounds.ps1 -Action start -Project sop-automation -Specialists "analyst,ballistics,cosmo,ops"
    .\swiss-rounds.ps1 -Action status
    .\swiss-rounds.ps1 -Action validate -Project sop-automation
    .\swiss-rounds.ps1 -Action advance -Project sop-automation
#>

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("start", "status", "advance", "validate", "abort")]
    [string]$Action,
    
    [string]$Project,
    
    [string]$Specialists = "analyst,ballistics,cosmo,seeker"
)

$SwissDir = "$env:USERPROFILE\.openclaw\workspace\swiss-rounds"

function Get-StateFile($proj) {
    return "$SwissDir\$proj\state.json"
}

function Load-State($proj) {
    $file = Get-StateFile $proj
    if (Test-Path $file) {
        return Get-Content $file | ConvertFrom-Json
    }
    return $null
}

function Save-State($state) {
    $dir = "$SwissDir\$($state.project)"
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    $state | ConvertTo-Json -Depth 10 | Set-Content (Get-StateFile $state.project)
}

function Get-ActiveProjects {
    if (-not (Test-Path $SwissDir)) { return @() }
    Get-ChildItem $SwissDir -Directory | Where-Object {
        $state = Load-State $_.Name
        $state -and -not $state.pmComplete
    } | Select-Object -ExpandProperty Name
}

switch ($Action) {
    "start" {
        if (-not $Project) {
            Write-Error "Project name required for start action"
            exit 1
        }
        
        $specList = $Specialists -split ","
        $projectDir = "$SwissDir\$Project"
        
        # Create directories
        @("reports", "triad", "synthesis") | ForEach-Object {
            $path = "$projectDir\$_"
            if (-not (Test-Path $path)) { New-Item -ItemType Directory -Path $path -Force | Out-Null }
        }
        
        # Create initial state
        $state = @{
            project = $Project
            startedAt = (Get-Date).ToUniversalTime().ToString("o")
            specialists = $specList
            currentRound = 1
            rounds = @{
                "1" = @{
                    status = "pending"
                    completed = @()
                    pending = $specList
                    triadComplete = $false
                }
            }
            pmComplete = $false
        }
        
        Save-State $state
        
        Write-Host "✅ Swiss Rounds started for: $Project" -ForegroundColor Green
        Write-Host "   Specialists: $($specList -join ', ')"
        Write-Host "   State: $projectDir\state.json"
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Yellow
        Write-Host "1. Spawn each specialist for Round 1 initial reports"
        Write-Host "2. After all complete, run triad validation"
        Write-Host "3. Use 'swiss-rounds.ps1 -Action advance -Project $Project' to proceed"
    }
    
    "status" {
        $projects = Get-ActiveProjects
        if ($projects.Count -eq 0) {
            Write-Host "No active Swiss Rounds projects" -ForegroundColor Yellow
            exit 0
        }
        
        foreach ($proj in $projects) {
            $state = Load-State $proj
            $round = $state.currentRound
            $roundState = $state.rounds."$round"
            
            Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
            Write-Host "Project: $proj" -ForegroundColor Cyan
            Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
            
            $roundNames = @{1="Initial Reports"; 2="Addendum 1"; 3="Retrospective 1"; 4="Addendum 2"; 5="Final Retrospective"; 6="PM Synthesis"}
            Write-Host "Round: $round/5 - $($roundNames[$round])"
            Write-Host "Status: $($roundState.status)"
            Write-Host "Completed: $($roundState.completed -join ', ')"
            Write-Host "Pending: $($roundState.pending -join ', ')"
            Write-Host "Triad: $(if ($roundState.triadComplete) { '✅' } else { '⏳' })"
            Write-Host ""
        }
    }
    
    "validate" {
        if (-not $Project) {
            Write-Error "Project name required"
            exit 1
        }
        
        $state = Load-State $Project
        if (-not $state) {
            Write-Error "Project not found: $Project"
            exit 1
        }
        
        $projectDir = "$SwissDir\$Project"
        $round = $state.currentRound
        $missing = @()
        
        Write-Host "Validating Round $round artifacts..." -ForegroundColor Yellow
        
        # Check reports
        foreach ($spec in $state.specialists) {
            $report = "$projectDir\reports\$spec-$Project.md"
            if (Test-Path $report) {
                Write-Host "  ✅ $spec report exists" -ForegroundColor Green
                
                # Check for round-specific sections
                $content = Get-Content $report -Raw
                $sections = @{
                    2 = "## Addendum 1"
                    3 = "## Retrospective Part 1"
                    4 = "## Addendum 2 from"
                    5 = "## Final Retrospective"
                }
                
                if ($round -gt 1 -and $sections.ContainsKey($round)) {
                    $section = $sections[$round]
                    if ($content -match [regex]::Escape($section)) {
                        Write-Host "    ✅ $section present" -ForegroundColor Green
                    } else {
                        Write-Host "    ❌ $section MISSING" -ForegroundColor Red
                        $missing += "$section in $spec report"
                    }
                }
            } else {
                Write-Host "  ❌ $spec report MISSING" -ForegroundColor Red
                $missing += "$spec-$Project.md"
            }
        }
        
        # Check triad for previous round
        if ($round -gt 1) {
            $prevRound = $round - 1
            $triadFiles = @("redundancy", "critique", "solution")
            foreach ($f in $triadFiles) {
                $triadFile = "$projectDir\triad\round$prevRound-$f.md"
                if (Test-Path $triadFile) {
                    Write-Host "  ✅ Round $prevRound triad $f" -ForegroundColor Green
                } else {
                    Write-Host "  ❌ Round $prevRound triad $f MISSING" -ForegroundColor Red
                    $missing += "triad/round$prevRound-$f.md"
                }
            }
        }
        
        Write-Host ""
        if ($missing.Count -eq 0) {
            Write-Host "✅ All artifacts valid for Round $round" -ForegroundColor Green
        } else {
            Write-Host "❌ Missing $($missing.Count) artifacts:" -ForegroundColor Red
            $missing | ForEach-Object { Write-Host "   - $_" -ForegroundColor Red }
        }
    }
    
    "advance" {
        if (-not $Project) {
            Write-Error "Project name required"
            exit 1
        }
        
        $state = Load-State $Project
        if (-not $state) {
            Write-Error "Project not found: $Project"
            exit 1
        }
        
        $currentRound = $state.currentRound
        
        # Mark current round complete and triad complete
        $state.rounds."$currentRound".status = "complete"
        $state.rounds."$currentRound".triadComplete = $true
        $state.rounds."$currentRound".completed = $state.specialists
        $state.rounds."$currentRound".pending = @()
        
        # Advance to next round
        $nextRound = $currentRound + 1
        $state.currentRound = $nextRound
        
        if ($nextRound -le 5) {
            $state.rounds."$nextRound" = @{
                status = "pending"
                completed = @()
                pending = $state.specialists
                triadComplete = $false
            }
            Write-Host "✅ Advanced to Round $nextRound" -ForegroundColor Green
        } elseif ($nextRound -eq 6) {
            $state.rounds."6" = @{
                status = "pending"
                completed = @()
                pending = @("project-manager")
                triadComplete = $false
            }
            Write-Host "✅ All rounds complete. Ready for PM Synthesis." -ForegroundColor Green
        } else {
            $state.pmComplete = $true
            Write-Host "✅ Swiss Rounds COMPLETE for $Project" -ForegroundColor Green
        }
        
        Save-State $state
    }
    
    "abort" {
        if (-not $Project) {
            Write-Error "Project name required"
            exit 1
        }
        
        $stateFile = Get-StateFile $Project
        if (Test-Path $stateFile) {
            Remove-Item $stateFile -Force
            Write-Host "❌ Aborted Swiss Rounds for: $Project" -ForegroundColor Yellow
        } else {
            Write-Host "Project not found: $Project" -ForegroundColor Red
        }
    }
}
