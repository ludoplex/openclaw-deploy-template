# PR Review Fix Cycle

> Handle feedback from Copilot/Sourcery AI reviews

## When to Use
- PR has review comments from bots or humans
- Need to iterate on code quality issues

## Steps

### 1. Check Reviews
```powershell
# Quick status
gh pr view <PR#> --repo <owner/repo> --json state,reviews,comments

# Get review details
gh api repos/<owner/repo>/pulls/<PR#>/reviews --jq ".[] | {user: .user.login, state: .state}"

# Get inline comments (the actual issues)
gh api repos/<owner/repo>/pulls/<PR#>/comments --jq ".[] | {file: .path, line: .line, body: .body[:200]}"
```

### 2. Categorize Issues
Priority order:
1. **Security** — CSRF, injection, auth bypass → Fix immediately
2. **Bugs** — Will cause runtime errors → Fix
3. **Performance** — Memory leaks, N+1 queries → Fix if easy
4. **Style** — Formatting, naming → Fix if quick
5. **Suggestions** — Nice-to-have → Defer or ignore

### 3. Fix Issues
```bash
# Make sure on feature branch
git checkout feature/branch-name

# Make fixes
# ... edit files ...

# Commit with descriptive message
git commit -am "fix: address review feedback

- Security: add state validation
- Bug: fix URL construction
- ..."
```

### 4. Push & Verify
```bash
git push origin feature/branch-name

# Check PR updated
gh pr view <PR#> --repo <owner/repo> --web
```

### 5. Respond to Reviews
If reviewers need response:
```bash
gh pr comment <PR#> --body "Fixed issues in commit abc123:
- ✅ State validation added
- ✅ URL bug fixed
- ⏸️ Memory optimization deferred to follow-up"
```

## Checklist
- [ ] All security issues addressed
- [ ] All bug issues addressed  
- [ ] Commit message explains fixes
- [ ] Pushed to feature branch
- [ ] PR shows new commit

## Tips
- Don't argue with bots — just fix or explain why not
- Group related fixes in single commit
- If issue is invalid, comment explaining why
- Re-request review if needed: `gh pr edit <PR#> --add-reviewer <user>`
