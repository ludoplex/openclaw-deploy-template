# install-hooks.ps1 - Install git hooks for workflow enforcement
# Run once per repo: .\scripts\install-hooks.ps1 -RepoPath "path\to\repo"

param(
    [Parameter(Mandatory=$true)]
    [string]$RepoPath
)

$hooksDir = Join-Path $RepoPath ".git\hooks"

if (-not (Test-Path $hooksDir)) {
    Write-Host "❌ Not a git repository: $RepoPath" -ForegroundColor Red
    exit 1
}

# Pre-commit hook content
$preCommitHook = @'
#!/bin/sh
# Workflow enforcement hook - reminds about tool selection

# Count new lines of code
ADDED_LINES=$(git diff --cached --numstat | awk '{sum += $1} END {print sum}')

if [ "$ADDED_LINES" -gt 100 ]; then
    echo ""
    echo "📊 Large commit detected ($ADDED_LINES new lines)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Quick check - was the right tool used?"
    echo ""
    echo "  ✓ Boilerplate → Local Qwen (localhost:8081)"
    echo "  ✓ Architecture → lmarena.ai (multi-model)"
    echo "  ✓ Complex logic → Claude ✓"
    echo ""
    echo "Run 'task-router.ps1' before next task"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
fi

# Check for common boilerplate patterns that should use Qwen
STAGED_FILES=$(git diff --cached --name-only)

for file in $STAGED_FILES; do
    if echo "$file" | grep -qE "\.(py|php|js|ts)$"; then
        # Check if file has boilerplate markers
        if git diff --cached "$file" | grep -qiE "(TODO|FIXME|boilerplate|template|scaffold)"; then
            echo "⚠️  $file may contain boilerplate - consider Qwen for future similar files"
        fi
    fi
done

exit 0
'@

# Post-commit hook - log to memory
$postCommitHook = @'
#!/bin/sh
# Log significant commits to daily memory

COMMIT_MSG=$(git log -1 --pretty=%B)
COMMIT_HASH=$(git log -1 --pretty=%h)
DATE=$(date +%Y-%m-%d)
MEMORY_FILE="$HOME/.openclaw/workspace/memory/$DATE.md"

# Only log if memory file exists and commit is significant
if [ -f "$MEMORY_FILE" ]; then
    CHANGED_FILES=$(git diff-tree --no-commit-id --name-only -r HEAD | wc -l)
    if [ "$CHANGED_FILES" -gt 3 ]; then
        echo "" >> "$MEMORY_FILE"
        echo "### Commit $COMMIT_HASH" >> "$MEMORY_FILE"
        echo "- $COMMIT_MSG" >> "$MEMORY_FILE"
    fi
fi

exit 0
'@

# Write hooks
$preCommitPath = Join-Path $hooksDir "pre-commit"
$postCommitPath = Join-Path $hooksDir "post-commit"

Set-Content -Path $preCommitPath -Value $preCommitHook -NoNewline
Set-Content -Path $postCommitPath -Value $postCommitHook -NoNewline

Write-Host "✅ Installed hooks in $RepoPath" -ForegroundColor Green
Write-Host "   - pre-commit: workflow reminder on large commits"
Write-Host "   - post-commit: log to daily memory"
