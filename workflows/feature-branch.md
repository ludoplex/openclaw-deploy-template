# Feature Branch Workflow

> Develop features with PR-based review cycle

## When to Use
- Adding new functionality
- Want Copilot/Sourcery review before merge
- Collaborating or tracking changes

## Steps

### 1. Create Branch
```bash
# From main/master
git checkout main
git pull origin main
git checkout -b feature/descriptive-name
```

Naming conventions:
- `feature/add-discord-provider`
- `fix/oauth-state-validation`
- `refactor/extract-upload-concern`

### 2. Develop
Follow 3-phase workflow:
1. **Plan** — `.\scripts\plan.ps1` or lmarena.ai
2. **Setup** — Templates, Qwen for boilerplate
3. **Execute** — Shell tools, minimal tokens

Commit often:
```bash
git add -A
git commit -m "feat: implement core functionality"
git commit -m "feat: add tests"
git commit -m "docs: update README"
```

### 3. Push & Create PR
```bash
git push -u origin feature/descriptive-name

# Create PR via CLI
gh pr create \
  --title "feat: Add descriptive title" \
  --body "## Summary
What this PR does...

## Changes
- Change 1
- Change 2

## Testing
How to test..." \
  --base main
```

### 4. Review Cycle
```bash
# Check for reviews (add to HEARTBEAT.md)
gh api repos/<owner/repo>/pulls/<PR#>/comments

# Fix issues, push updates
git commit -am "fix: address review feedback"
git push
```

### 5. Merge
Once approved:
```bash
# Squash merge (clean history)
gh pr merge <PR#> --squash --delete-branch

# Or merge commit (preserve history)
gh pr merge <PR#> --merge --delete-branch
```

### 6. Cleanup
```bash
git checkout main
git pull origin main
git branch -d feature/descriptive-name
```

## Checklist
- [ ] Branch created from latest main
- [ ] Commits are logical units
- [ ] PR has clear description
- [ ] Tests pass (if applicable)
- [ ] Review feedback addressed
- [ ] Merged and branch deleted

## Templates

### PR Body Template
```markdown
## Summary
Brief description of changes.

## Changes
- Added X
- Fixed Y
- Updated Z

## Testing
- [ ] Manual testing done
- [ ] Unit tests added/updated

## Screenshots
(if UI changes)
```
