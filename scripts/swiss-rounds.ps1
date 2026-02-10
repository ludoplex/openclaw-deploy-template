<# 
.SYNOPSIS
    Swiss Rounds Synthesis workflow manager

.DESCRIPTION
    Manages multi-agent deliberation with cross-examination, retrospectives, 
    and triad validation before PM synthesis.

.PARAMETER Action
    start, status, advance, validate, abort, add-source, verify-sources

.PARAMETER Project
    Project name (required for most actions)

.PARAMETER Specialists
    Comma-separated list of specialist agent IDs

.PARAMETER SourceName
    Name for source (e.g., "upstream", "fork")

.PARAMETER SourcePath
    Path to source directory

.PARAMETER SourceRepo
    Repository URL (optional)

.PARAMETER SourceType
    Type of source: "source" or "binary" (default: source)

.EXAMPLE
    .\swiss-rounds.ps1 -Action start -Project my-project -Specialists "seeker,asm,cosmo"
    .\swiss-rounds.ps1 -Action add-source -Project my-project -SourceName upstream -SourcePath C:\repos\upstream
    .\swiss-rounds.ps1 -Action verify-sources -Project my-project
    .\swiss-rounds.ps1 -Action status
    .\swiss-rounds.ps1 -Action validate -Project my-project
    .\swiss-rounds.ps1 -Action advance -Project my-project
#>

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("start", "start-revision", "status", "advance", "validate", "abort", "add-source", "verify-sources")]
    [string]$Action,
    
    [string]$Project,
    
    [string]$Specialists = "seeker,localsearch,asm,cosmo,dbeng,neteng,cicd,testcov",
    
    [string]$SourceName,
    [string]$SourcePath,
    [string]$SourceRepo,
    [ValidateSet("source", "binary")]
    [string]$SourceType = "source",
    
    [string]$PriorPlanPath,
    [string]$RevisionScope,
    [string]$TriggeredBy = "user"
)

$SwissDir = "$env:USERPROFILE\.openclaw\workspace\swiss-rounds"

function Get-StateFile($proj) {
    return "$SwissDir\$proj\state.json"
}

function Load-State($proj) {
    $file = Get-StateFile $proj
    if (Test-Path $file) {
        $json = Get-Content $file -Raw | ConvertFrom-Json
        # Convert PSObject to hashtable for easier manipulation
        return $json
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
        $state -and $state.phase -ne "complete"
    } | Select-Object -ExpandProperty Name
}

function Get-PhaseAction($state) {
    # Setup phase
    if ($state.phase -eq "setup") {
        if ($state.sources.Count -eq 0) {
            return @{ action = "setup_needed"; reason = "No sources defined. Add sources first." }
        }
        $unverified = $state.sources | Where-Object { -not $_.verified }
        if ($unverified.Count -gt 0) {
            return @{ action = "setup_needed"; reason = "Sources not verified: $($unverified.name -join ', ')" }
        }
        if (-not $state.userVerified) {
            return @{ action = "setup_needed"; reason = "User has not verified sources. Run verify-sources." }
        }
        return @{ action = "spawn_specialists"; reason = "Setup complete. Begin Round 1." }
    }

    # Rounds phase
    if ($state.phase -eq "rounds") {
        $round = $state.rounds["$($state.currentRound)"]
        if (-not $round) {
            return @{ action = "spawn_specialists"; reason = "Initialize Round $($state.currentRound)" }
        }
        
        if (-not $round.specialistsComplete) {
            if ($round.pending.Count -gt 0) {
                return @{ action = "wait"; reason = "Waiting for specialists: $($round.pending -join ', ')" }
            }
            return @{ action = "spawn_specialists"; reason = "Spawn specialists for Round $($state.currentRound)" }
        }
        
        if (-not $round.triadComplete) {
            return @{ action = "spawn_triad"; reason = "Specialists complete. Spawn triad." }
        }
        
        if ($state.currentRound -lt $state.totalRounds) {
            return @{ action = "spawn_specialists"; reason = "Round $($state.currentRound) complete. Advance to Round $($state.currentRound + 1)" }
        } else {
            return @{ action = "spawn_pm"; reason = "All rounds complete. Spawn PM." }
        }
    }

    # PM phase
    if ($state.phase -eq "pm") {
        if ($state.pm.complete) {
            return @{ action = "done"; reason = "PM synthesis complete." }
        }
        if (-not $state.pm.started) {
            return @{ action = "spawn_pm"; reason = "Spawn PM to begin synthesis." }
        }
        return @{ action = "wait"; reason = "PM synthesis in progress." }
    }

    # Complete phase
    if ($state.phase -eq "complete") {
        return @{ action = "done"; reason = "Swiss Rounds complete." }
    }

    return @{ action = "wait"; reason = "Unknown state" }
}

switch ($Action) {
    "start" {
        if (-not $Project) {
            Write-Error "Project name required for start action"
            exit 1
        }
        
        $specList = @($Specialists -split ",")
        $projectDir = "$SwissDir\$Project"
        
        # Create directories
        @("reports", "triad", "synthesis") | ForEach-Object {
            $path = "$projectDir\$_"
            if (-not (Test-Path $path)) { New-Item -ItemType Directory -Path $path -Force | Out-Null }
        }
        
        # Create initial state with new schema
        $state = @{
            project = $Project
            mode = "new"
            phase = "setup"
            sources = @()
            userVerified = $false
            specialists = $specList
            currentRound = 1
            totalRounds = 5
            rounds = @{}
            pm = @{
                started = $false
                overarchingPlanComplete = $false
                sequence = @()
                specialistPlans = @{}
                complete = $false
            }
            revision = @{
                priorPlanPath = $null
                scope = $null
                triggeredBy = $null
            }
            startedAt = (Get-Date).ToUniversalTime().ToString("o")
        }
        
        Save-State $state
        
        Write-Host "✅ Swiss Rounds started for: $Project" -ForegroundColor Green
        Write-Host "   Phase: setup" -ForegroundColor Yellow
        Write-Host "   Specialists: $($specList -join ', ')"
        Write-Host "   State: $projectDir\state.json"
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Yellow
        Write-Host "1. Add sources: .\swiss-rounds.ps1 -Action add-source -Project $Project -SourceName upstream -SourcePath C:\path\to\repo"
        Write-Host "2. Verify sources: .\swiss-rounds.ps1 -Action verify-sources -Project $Project"
        Write-Host "3. Then spawn specialists for Round 1"
    }
    
    "start-revision" {
        if (-not $Project) {
            Write-Error "Project name required for start-revision action"
            exit 1
        }
        if (-not $PriorPlanPath) {
            Write-Error "PriorPlanPath required for revision mode"
            exit 1
        }
        if (-not $RevisionScope) {
            Write-Error "RevisionScope required for revision mode"
            exit 1
        }
        
        $specList = @($Specialists -split ",")
        $projectDir = "$SwissDir\$Project"
        
        # Create directories
        @("reports", "triad", "synthesis") | ForEach-Object {
            $path = "$projectDir\$_"
            if (-not (Test-Path $path)) { New-Item -ItemType Directory -Path $path -Force | Out-Null }
        }
        
        # Create revision state
        $state = @{
            project = $Project
            mode = "revision"
            phase = "setup"
            sources = @()
            userVerified = $false
            specialists = $specList
            currentRound = 1
            totalRounds = 5
            rounds = @{}
            pm = @{
                started = $false
                overarchingPlanComplete = $false
                sequence = @()
                specialistPlans = @{}
                complete = $false
            }
            revision = @{
                priorPlanPath = $PriorPlanPath
                scope = $RevisionScope
                triggeredBy = $TriggeredBy
            }
            startedAt = (Get-Date).ToUniversalTime().ToString("o")
        }
        
        Save-State $state
        
        Write-Host "✅ Swiss Rounds REVISION started for: $Project" -ForegroundColor Green
        Write-Host "   Mode: revision" -ForegroundColor Yellow
        Write-Host "   Prior Plan: $PriorPlanPath"
        Write-Host "   Scope: $RevisionScope"
        Write-Host "   Triggered By: $TriggeredBy"
        Write-Host "   Specialists: $($specList -join ', ')"
        Write-Host "   State: $projectDir\state.json"
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Yellow
        Write-Host "1. Add/verify sources (same as new project)"
        Write-Host "2. Spawn specialists - they will receive prior plan + revision scope as context"
        Write-Host "3. Full Swiss Rounds process runs on the revision itself"
    }
    
    "add-source" {
        if (-not $Project -or -not $SourceName -or -not $SourcePath) {
            Write-Error "Project, SourceName, and SourcePath required"
            exit 1
        }
        
        $state = Load-State $Project
        if (-not $state) {
            Write-Error "Project not found: $Project"
            exit 1
        }
        
        # Check path exists
        if (-not (Test-Path $SourcePath)) {
            Write-Error "Source path does not exist: $SourcePath"
            exit 1
        }
        
        $newSource = @{
            name = $SourceName
            repo = if ($SourceRepo) { $SourceRepo } else { $null }
            path = (Resolve-Path $SourcePath).Path
            type = $SourceType
            verified = $false
        }
        
        $state.sources += $newSource
        Save-State $state
        
        Write-Host "✅ Added source: $SourceName" -ForegroundColor Green
        Write-Host "   Path: $SourcePath"
        Write-Host "   Type: $SourceType"
        Write-Host "   Verified: false (run verify-sources to mark verified)"
    }
    
    "verify-sources" {
        if (-not $Project) {
            Write-Error "Project name required"
            exit 1
        }
        
        $state = Load-State $Project
        if (-not $state) {
            Write-Error "Project not found: $Project"
            exit 1
        }
        
        if ($state.sources.Count -eq 0) {
            Write-Host "❌ No sources defined. Add sources first." -ForegroundColor Red
            exit 1
        }
        
        Write-Host "Sources for $Project :" -ForegroundColor Cyan
        foreach ($src in $state.sources) {
            $exists = Test-Path $src.path
            $status = if ($exists) { "✅" } else { "❌ NOT FOUND" }
            Write-Host "  $status $($src.name): $($src.path) [$($src.type)]"
            
            if ($exists) {
                # Mark as verified
                $src.verified = $true
            }
        }
        
        $state.userVerified = $true
        $state.phase = "rounds"
        
        # Initialize Round 1
        $state.rounds["1"] = @{
            specialistsComplete = $false
            triadComplete = $false
            completed = @()
            pending = @($state.specialists)
        }
        
        Save-State $state
        
        Write-Host ""
        Write-Host "✅ Sources verified. Phase advanced to: rounds" -ForegroundColor Green
        Write-Host "   Ready to spawn specialists for Round 1" -ForegroundColor Yellow
    }
    
    "status" {
        $projects = Get-ActiveProjects
        if ($projects.Count -eq 0) {
            Write-Host "No active Swiss Rounds projects" -ForegroundColor Yellow
            exit 0
        }
        
        foreach ($proj in $projects) {
            $state = Load-State $proj
            $phaseAction = Get-PhaseAction $state
            
            Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
            Write-Host "Project: $proj" -ForegroundColor Cyan
            Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
            
            Write-Host "Phase: $($state.phase)"
            Write-Host "Mode: $($state.mode)"
            Write-Host "Round: $($state.currentRound)/$($state.totalRounds)"
            
            Write-Host ""
            Write-Host "Sources:" -ForegroundColor Yellow
            foreach ($src in $state.sources) {
                $v = if ($src.verified) { "✅" } else { "⏳" }
                Write-Host "  $v $($src.name): $($src.path) [$($src.type)]"
            }
            Write-Host "User Verified: $(if ($state.userVerified) { '✅' } else { '❌' })"
            
            if ($state.phase -eq "rounds") {
                $round = $state.rounds["$($state.currentRound)"]
                if ($round) {
                    Write-Host ""
                    Write-Host "Round $($state.currentRound) State:" -ForegroundColor Yellow
                    Write-Host "  Specialists Complete: $(if ($round.specialistsComplete) { '✅' } else { '⏳' })"
                    Write-Host "  Triad Complete: $(if ($round.triadComplete) { '✅' } else { '⏳' })"
                    Write-Host "  Completed: $($round.completed -join ', ')"
                    Write-Host "  Pending: $($round.pending -join ', ')"
                }
            }
            
            if ($state.phase -eq "pm") {
                Write-Host ""
                Write-Host "PM State:" -ForegroundColor Yellow
                Write-Host "  Started: $(if ($state.pm.started) { '✅' } else { '⏳' })"
                Write-Host "  Overarching Plan: $(if ($state.pm.overarchingPlanComplete) { '✅' } else { '⏳' })"
                Write-Host "  Sequence: $($state.pm.sequence -join ' -> ')"
                Write-Host "  Complete: $(if ($state.pm.complete) { '✅' } else { '⏳' })"
            }
            
            Write-Host ""
            Write-Host "Next Action: $($phaseAction.action)" -ForegroundColor Green
            Write-Host "Reason: $($phaseAction.reason)"
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
        
        if ($state.phase -eq "setup") {
            Write-Host "❌ Cannot advance: still in setup phase. Add and verify sources first." -ForegroundColor Red
            exit 1
        }
        
        if ($state.phase -eq "rounds") {
            # Mark current round complete
            $state.rounds["$currentRound"].specialistsComplete = $true
            $state.rounds["$currentRound"].triadComplete = $true
            $state.rounds["$currentRound"].completed = @($state.specialists)
            $state.rounds["$currentRound"].pending = @()
            
            # Advance to next round
            $nextRound = $currentRound + 1
            $state.currentRound = $nextRound
            
            if ($nextRound -le $state.totalRounds) {
                $state.rounds["$nextRound"] = @{
                    specialistsComplete = $false
                    triadComplete = $false
                    completed = @()
                    pending = @($state.specialists)
                }
                Write-Host "✅ Advanced to Round $nextRound" -ForegroundColor Green
            } else {
                $state.phase = "pm"
                Write-Host "✅ All rounds complete. Phase: pm" -ForegroundColor Green
                Write-Host "   Ready to spawn project-manager" -ForegroundColor Yellow
            }
        } elseif ($state.phase -eq "pm") {
            $state.pm.complete = $true
            $state.phase = "complete"
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
