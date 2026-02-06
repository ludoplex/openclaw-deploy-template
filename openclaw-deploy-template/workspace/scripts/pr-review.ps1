<#
.SYNOPSIS
    Fetch and display PR review comments from GitHub

.PARAMETER Repo
    Repository in owner/name format

.PARAMETER PR
    Pull request number

.EXAMPLE
    .\pr-review.ps1 -Repo "ludoplex/mixpost-malone" -PR 1
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$Repo,
    
    [Parameter(Mandatory=$true)]
    [int]$PR
)

Write-Host "`n📋 PR #$PR Review Status" -ForegroundColor Cyan
Write-Host "Repository: $Repo`n" -ForegroundColor Gray

# Get PR info
$prInfo = gh pr view $PR --repo $Repo --json title,state,mergeable,reviewDecision 2>$null | ConvertFrom-Json

if ($prInfo) {
    Write-Host "Title: $($prInfo.title)" -ForegroundColor White
    Write-Host "State: $($prInfo.state)" -ForegroundColor $(if ($prInfo.state -eq "OPEN") { "Green" } else { "Yellow" })
    Write-Host "Mergeable: $($prInfo.mergeable)" -ForegroundColor $(if ($prInfo.mergeable -eq "MERGEABLE") { "Green" } else { "Red" })
    Write-Host "Decision: $($prInfo.reviewDecision)" -ForegroundColor $(if ($prInfo.reviewDecision -eq "APPROVED") { "Green" } else { "Yellow" })
}

Write-Host "`n--- Reviews ---" -ForegroundColor Cyan

# Get reviews
$reviews = gh api "repos/$Repo/pulls/$PR/reviews" 2>$null | ConvertFrom-Json

if ($reviews -and $reviews.Count -gt 0) {
    foreach ($review in $reviews) {
        $color = switch ($review.state) {
            "APPROVED" { "Green" }
            "CHANGES_REQUESTED" { "Red" }
            "COMMENTED" { "Yellow" }
            default { "Gray" }
        }
        Write-Host "`n[$($review.state)] $($review.user.login)" -ForegroundColor $color
        if ($review.body) {
            Write-Host $review.body -ForegroundColor White
        }
    }
} else {
    Write-Host "No reviews yet" -ForegroundColor Gray
}

Write-Host "`n--- Review Comments ---" -ForegroundColor Cyan

# Get review comments (inline code comments)
$comments = gh api "repos/$Repo/pulls/$PR/comments" 2>$null | ConvertFrom-Json

if ($comments -and $comments.Count -gt 0) {
    foreach ($comment in $comments) {
        Write-Host "`n📝 $($comment.user.login) on $($comment.path):$($comment.line)" -ForegroundColor Yellow
        Write-Host $comment.body -ForegroundColor White
    }
} else {
    Write-Host "No inline comments" -ForegroundColor Gray
}

Write-Host "`n--- Issue Comments ---" -ForegroundColor Cyan

# Get issue comments (general PR comments)
$issueComments = gh api "repos/$Repo/issues/$PR/comments" 2>$null | ConvertFrom-Json

if ($issueComments -and $issueComments.Count -gt 0) {
    foreach ($comment in $issueComments) {
        # Skip bot status messages
        if ($comment.body -match "^<!--") { continue }
        
        Write-Host "`n💬 $($comment.user.login):" -ForegroundColor Yellow
        # Truncate long comments
        $body = $comment.body
        if ($body.Length -gt 500) {
            $body = $body.Substring(0, 500) + "..."
        }
        Write-Host $body -ForegroundColor White
    }
} else {
    Write-Host "No comments" -ForegroundColor Gray
}

Write-Host "`n" -NoNewline
