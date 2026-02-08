# Research Protocol Skill 🔬

**Purpose:** Prevent building on imagined APIs. Verify before recommending.

---

## When to Use

Before recommending or implementing ANY:
- External library or package
- API or service integration
- Framework choice
- Tool selection
- Pattern or architecture from a specific project

---

## The Protocol

### Step 1: Find Authoritative Source

```bash
# For GitHub repos
gh api repos/{owner}/{repo} --jq '.description, .stargazers_count, .open_issues_count, .pushed_at'

# List repo structure
gh api repos/{owner}/{repo}/contents/src --jq '.[].name'

# For npm packages, find the repo first
npm view {package} repository.url
```

**Critical:** Use the OFFICIAL repo, not forks. Forks can be abandoned, modified, or contain malicious changes.

### Step 2: Verify Features in Source Code

```bash
# Fetch actual source file
gh api repos/{owner}/{repo}/contents/src/feature.ts -H "Accept: application/vnd.github.raw"

# Search for specific function
gh api -X GET "repos/{owner}/{repo}/code/search?q=functionName" --jq '.items[].path'
```

For each claimed feature:
1. Find the actual function/class that implements it
2. Note the exact file path and line numbers
3. Read enough to understand what it ACTUALLY does
4. Look for: `TODO`, `NotImplementedError`, `throw new Error("not implemented")`

### Step 3: Check Issues and Limitations

```bash
# Search issues for known problems
gh issue list --repo {owner}/{repo} --search "{feature}" --state all

# Check for breaking changes in recent commits
gh api repos/{owner}/{repo}/commits --jq '.[0:5] | .[].commit.message'
```

### Step 4: Assess Maturity

| Metric | Good | Concerning |
|--------|------|------------|
| Last commit | < 3 months | > 1 year |
| Open issues | < 50 or triaged | > 500 untriaged |
| Stars | Context-dependent | N/A |
| Bus factor | Multiple maintainers | Single author, inactive |

---

## Output Template

```markdown
## {Technology Name} - Verification Report

**Source:** {repo URL}
**Verified:** {date}
**Commit:** {sha or "latest as of date"}

### ✅ Verified Features
| Feature | Location | Notes |
|---------|----------|-------|
| {feature} | `src/path/file.ts:42` - `functionName()` | {brief notes} |

### ❌ Does NOT Exist (Common Misconceptions)
| Claimed Feature | Reality |
|-----------------|---------|
| "{thing people assume}" | {what actually exists or doesn't} |

### ⚠️ Known Limitations
- {from issues, source comments, or testing}

### 📊 Maturity Assessment
- **Stars:** X | **Forks:** Y | **Open Issues:** Z
- **Last commit:** {date}
- **Maintenance:** {Active / Sporadic / Abandoned}
- **Bus factor:** {assessment}

### Recommendation
{Use / Use with caution / Avoid / Investigate further}
```

---

## Anti-Patterns to Avoid

### 1. Documentation Trust
> "The docs say it supports X"

Documentation can be:
- Outdated (feature removed)
- Aspirational (feature planned, not implemented)
- Wrong (docs diverged from code)

**Always verify in source.**

### 2. Memory Trust
> "I know this library can do X"

Your training data has a cutoff. Libraries change. APIs get deprecated.

**Always verify current state.**

### 3. Inference
> "If it has A and B, it probably has C"

Software doesn't follow logical implications. Features are added based on maintainer priorities, not completeness.

**Verify explicitly.**

---

## The OpenClaw Incident

**Reference:** `C:\Users\user\openclaw-features-reference.md`

An agent once invented these APIs that don't exist:
- `agent_message()` / `agent_inbox()` — NOT REAL
- `agent:spawn` hook event — NOT REAL
- `tool:post-execute` hook event — NOT REAL
- "Spawn and wait" pattern — IMPOSSIBLE

This happened because assumptions were made instead of reading source.

**Actual OpenClaw hook events (verified):**
- `command` (with actions: `new`, `reset`, `stop`)
- `agent:bootstrap`
- `gateway:startup`

That's it. Three event types. Everything else was hallucinated.

---

## Quick Reference Commands

```bash
# Get repo info
gh api repos/{owner}/{repo} --jq '{desc: .description, stars: .stargazers_count, issues: .open_issues_count, pushed: .pushed_at}'

# List source files
gh api repos/{owner}/{repo}/contents/src --jq '.[].name'

# Read a file
gh api repos/{owner}/{repo}/contents/{path} -H "Accept: application/vnd.github.raw"

# Search code (limited but useful)
gh search code "{query}" --repo {owner}/{repo} --json path,repository

# Recent issues
gh issue list --repo {owner}/{repo} --limit 10 --state all

# Check if feature exists (grep-style)
gh api repos/{owner}/{repo}/contents/src/{file} -H "Accept: application/vnd.github.raw" | grep -i "{feature}"
```

---

**Remember:** The 30 minutes spent verifying saves the 30 hours spent building on a lie.
