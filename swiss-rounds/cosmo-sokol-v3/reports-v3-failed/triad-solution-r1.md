# Triad Phase 3: Solutions — cosmo-sokol-v3

**Analyst:** Solutions Synthesizer  
**Date:** 2026-02-09  
**Round:** 1 (Post-Critique)  
**Purpose:** Bridge theory and practice with minimum viable solutions

---

## Executive Summary

The critic is right: **we've been solving the wrong problem.**

8 specialists proposed 40+ hours of automation infrastructure to avoid 10 minutes of monthly manual work. Meanwhile, the actual problem—a 1,032-commit gap with breaking changes—remains unaddressed.

**This document proposes a radically simpler path:**

| Phase | Effort | Outcome |
|-------|--------|---------|
| Phase 0: Validate Need | 30 min | Decide if we even need to act |
| Phase 1: One-Time Migration | 2-4 hours | Close the commit gap |
| Phase 2: Minimal Monitoring | 1 hour | Get notified when upstream changes |
| Phase 3: Automation (Maybe) | TBD | Only if Phase 2 proves insufficient |

**The ONE thing that unblocks everything:** Migrate to current upstream first. Nothing else matters until that's done.

---

## 1. Answering the Hard Questions

### 1.1 "What if we do nothing?"

**Current State:**
- Fork is 11 months / 1,032 commits behind
- Build works on Linux ✅ Windows ✅
- macOS is a stub (compiles, doesn't run)
- No known user complaints about missing features

**Honest Assessment:**
The fork works fine for its current users. Upstream sokol improvements (performance, bug fixes, new backends) are not reaching them, but they haven't complained.

**"Do Nothing" Risk:**
- Security fixes in upstream go unpatched
- New upstream features unavailable
- Gap widens, future migration becomes harder
- Technical debt compounds

**"Do Nothing" is viable IF:**
- No security vulnerabilities exist in old sokol
- No users need features from the last 11 months
- You're willing to let the fork die eventually

**Recommendation:** "Do Nothing" is a legitimate choice, but a conscious one. If you proceed, at least do the one-time migration to reset the clock.

---

### 1.2 "Who maintains this?"

This is the killer question. Every specialist proposed infrastructure they won't maintain.

**Reality Check:**
- ludoplex/cosmo-sokol is a hobby project
- Original author (bullno1) appears inactive
- Current maintainer bandwidth is unknown

**The Maintenance Matrix:**

| Approach | Initial Work | Ongoing Maintenance |
|----------|--------------|---------------------|
| Manual quarterly sync | 0 hours | 2-4 hours/year |
| GitHub notification + manual | 1 hour | 2-4 hours/year + reading notifications |
| Basic automation (weekly PR) | 4 hours | 2-4 hours/year + CI debugging |
| Full automation (8 specialists proposed) | 40+ hours | 10-20 hours/year |

**Brutal Truth:** If you don't have someone who will actively maintain the fork, don't build infrastructure that requires active maintenance.

**Recommendation:** Start with manual quarterly sync. Graduate to automation only when manual becomes a proven pain point.

---

### 1.3 "What's the minimum viable solution?"

**The 80/20 Rule Applied:**

| Need | 80% Solution | 20% Effort |
|------|--------------|------------|
| Know when upstream changes | GitHub Watch + email | 1 click |
| Track version information | `VERSIONS.json` (3 fields) | 10 minutes |
| Catch breaking changes | Build in CI on PR | Already exists |
| Detect API drift | Build failure tells you | 0 additional work |
| Migrate the gap | One afternoon of manual work | 2-4 hours |

**What you DON'T need:**
- API extraction scripts (build errors tell you)
- SBOM generation (no compliance requirement)
- SQLite database (a JSON file works)
- GPG signing (no threat model)
- 3 separate workflows (1 is fine)
- Daily sync checks (quarterly matters)

---

### 1.4 "What about bullno1/cosmo-sokol?"

**Facts:**
- Last commit: March 2025 (11 months ago)
- Total commits: ~15
- Contains: cosmocc integration, basic structure
- Doesn't have: ludoplex's macOS additions

**Recommendation:** **Drop it.** 

The relationship is now:
```
floooh/sokol (active) → bullno1/cosmo-sokol (dormant) → ludoplex/cosmo-sokol (active fork)
```

You're maintaining a fork of a dormant fork. Skip the middleman. Track floooh/sokol directly for the actual graphics library updates.

**Keep bullno1 as origin history**, but don't waste cycles syncing with a dead repo.

---

## 2. The Minimum Viable Path

### Phase 0: Validate Need (30 minutes)

Before doing anything, answer these questions:

**1. Are there security vulnerabilities in the current sokol?**
- Check sokol's CHANGELOG for security fixes since your commit
- If yes: urgent migration needed
- If no: lower priority

**2. Are users asking for features in newer sokol?**
- Check issues, discussions
- If yes: document which features
- If no: less urgent

**3. Can you commit to maintaining this fork long-term?**
- If yes: proceed
- If no: consider archiving with a note pointing to bullno1 or floooh/sokol

**Deliverable:** A go/no-go decision documented in one paragraph.

---

### Phase 1: One-Time Migration (2-4 hours)

This is **the actual work**. Everything else is procrastination.

#### Step 1: Understand the Gap

```bash
cd deps/sokol
git log --oneline HEAD..origin/master | wc -l  # ~1,032 commits
git log --oneline --since="2024-11-01" --until="2024-11-30" origin/master  # Find breaking change
```

#### Step 2: Identify Breaking Changes

From seeker and dbeng reports, the key break is:
- **Nov 7, 2024:** `sg_bindings` restructure (images → textures, commit 92c3...)

```c
// OLD (pre-Nov 2024)
sg_bindings bindings = {
    .vertex_buffers[0] = vbuf,
    .images[0] = img
};

// NEW (post-Nov 2024)  
sg_bindings bindings = {
    .vertex_buffers[0] = vbuf,
    .textures[0] = img  // <-- renamed
};
```

#### Step 3: Migration Strategy

**Option A: Two-Phase (Safer)**
1. Update to commit before Nov 2024 breaking change
2. Test, merge, release
3. Update to HEAD with breaking change migration
4. Test, merge, release

**Option B: Direct to HEAD (Faster)**
1. Update to HEAD
2. Fix all breaking changes in one PR
3. Test, merge, release

**Recommendation:** Option B. The breaking change is well-documented and affects 2-3 files. Just do it.

#### Step 4: Execute

```bash
# Create migration branch
git checkout -b migrate-sokol-2024

# Update submodule
cd deps/sokol
git fetch origin
git checkout <latest-stable-tag-or-HEAD>
cd ../..
git add deps/sokol

# Fix breaking changes in gen-sokol and examples
# (Guided by build errors)

# Build and test
make clean && make

# Update VERSIONS.json (create if needed)
{
  "sokol": { "ref": "<commit-hash>", "date": "2026-02-09" },
  "cosmocc": "3.9.6"
}

# Commit and PR
git add .
git commit -m "Update sokol to <version> with breaking change migration"
```

**Deliverable:** PR updating sokol submodule to current upstream, with all breaking changes resolved.

---

### Phase 2: Minimal Monitoring (1 hour setup)

Once migrated, you need to know when upstream changes. But you don't need custom automation.

#### Option A: GitHub Watch (5 minutes)

1. Go to https://github.com/floooh/sokol
2. Click "Watch" → "Custom" → check "Releases"
3. You'll get emails when new releases happen

**Pros:** Zero maintenance, GitHub does the work
**Cons:** No automatic PR creation

#### Option B: Dependabot (15 minutes)

Create `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: "gitsubmodule"
    directory: "/"
    schedule:
      interval: "monthly"
```

**Pros:** Automatic PR creation for submodule updates
**Cons:** No breaking change detection (but CI will catch that)

#### Option C: Simple Cron Job (1 hour)

If you really want custom notification:

```yaml
# .github/workflows/check-upstream.yml
name: Check Upstream
on:
  schedule:
    - cron: '0 0 1 * *'  # Monthly
  workflow_dispatch:

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: true
      
      - name: Check for upstream updates
        run: |
          cd deps/sokol
          git fetch origin
          LOCAL=$(git rev-parse HEAD)
          REMOTE=$(git rev-parse origin/master)
          if [ "$LOCAL" != "$REMOTE" ]; then
            echo "::warning::Upstream sokol has $(git rev-list HEAD..origin/master --count) new commits"
          fi
```

**This is 20 lines of YAML.** Not 3 workflows with Python scripts.

**Recommendation:** Start with Dependabot (Option B). It's 6 lines of YAML and GitHub maintains it.

---

### Phase 3: Automation (Only If Needed)

**Do NOT proceed to this phase unless:**
1. Phase 1 migration is complete
2. Phase 2 monitoring has run for 3+ months
3. You've experienced actual pain from manual merging
4. You have committed maintainer time for infrastructure

**If all true, then consider:**
- Auto-PR creation (cicd's `sync-upstream.yml`)
- API diff checking (neteng's consolidated script)
- Build matrix expansion (Windows, Linux)

**But remember:** You still have to review and merge the PRs. Automation saves maybe 5 minutes per sync. The question is whether 5 minutes/month is worth 4+ hours of setup and ongoing maintenance.

---

## 3. Addressing Specific Critic Concerns

### 3.1 "The cure may be worse than the disease"

**Solution:** Don't build the cure. Do the migration manually. Monitor with Dependabot. Revisit automation in 6 months.

---

### 3.2 "Who reviews the auto-generated PRs?"

**Solution:** The maintainer, same as today. But since syncs are monthly or quarterly, this is maybe 4-12 PRs/year. That's not a burden.

---

### 3.3 "Weekly polling for quarterly events"

**Solution:** Monthly, not weekly. Or just use Dependabot which handles this intelligently.

---

### 3.4 "API extraction regex untested"

**Solution:** Skip API extraction entirely. The build will fail if APIs change. That's your detection mechanism. YAGNI.

---

### 3.5 "No rollback plan"

**Solution:** Git is your rollback plan.

```bash
# If new sokol breaks things
git revert <merge-commit>
# or
cd deps/sokol && git checkout <known-good-commit>
```

---

### 3.6 "cimgui ignored"

**Solution:** Same approach as sokol. One submodule at a time. After sokol migration succeeds, apply same pattern to cimgui.

---

### 3.7 "macOS is scope creep"

**Solution:** Agree. macOS is a separate project. The sokol sync should work with macOS as a stub. Don't conflate the two.

---

## 4. Consolidated Deliverables (Minimal Set)

### Must Have

| Item | Owner | Effort | When |
|------|-------|--------|------|
| Migrate sokol to current upstream | Maintainer | 2-4 hours | Now |
| Fix `sg_bindings` breaking change | Maintainer | 30 min | During migration |
| Create `VERSIONS.json` (simple) | Maintainer | 10 min | During migration |
| Enable Dependabot for submodules | Maintainer | 5 min | After migration |

### Nice to Have

| Item | Owner | Effort | When |
|------|-------|--------|------|
| `_Static_assert` for struct sizes (asm) | Maintainer | 30 min | After migration |
| `--headless` flag for testing (testcov) | Maintainer | 1 hour | When adding tests |

### Defer Until Proven Needed

| Item | Why Defer |
|------|-----------|
| Custom Python scripts | Build errors are sufficient |
| Multi-workflow CI | One workflow is fine |
| SBOM/GPG signing | No compliance requirement |
| SQLite version DB | JSON file works |
| API extraction automation | YAGNI |

### Explicitly Out of Scope

| Item | Reason |
|------|--------|
| macOS objc_msgSend completion | Separate project |
| Vulkan backend | New feature, not sync |
| Metal support | New feature, not sync |
| bullno1 sync | Dormant repo |

---

## 5. The ONE Thing That Unblocks Everything

**Migrate the submodule to current upstream.**

Everything else is premature optimization until this is done:
- Can't automate syncing until you know how to migrate
- Can't test automation until you have a working build on current sokol
- Can't measure automation value until you've done manual sync

**The action is clear:**

```bash
git checkout -b migrate-sokol-2024
cd deps/sokol && git fetch origin && git checkout origin/master
cd ../.. && make
# Fix what breaks
# Commit
# PR
# Merge
```

**Estimated time:** One focused afternoon.

**After that:** Evaluate if you need any automation at all.

---

## 6. Decision Matrix for Maintainer

| If you have... | Do this |
|----------------|---------|
| 0 hours | Do nothing. The fork works. |
| 2-4 hours | Phase 1: Migrate sokol to current. Stop there. |
| 4-5 hours | Phase 1 + Phase 2: Migrate and set up Dependabot. |
| 10+ hours | Phase 1-3: Full automation. But question if this is the best use of time. |

---

## 7. Summary

### What the Specialists Got Right
- The commit gap is real
- Breaking changes exist and are documented
- API drift detection matters
- CI integration is the right place for checks

### What the Specialists Over-Complicated
- 6 versions of API extraction (need 0-1)
- 3 workflow files (need 1)
- SQLite, SBOM, GPG (need none)
- Weekly polling (monthly or Dependabot is fine)

### The Path Forward
1. **Now:** Decide if this fork is worth maintaining
2. **This week:** If yes, migrate to current upstream (2-4 hours)
3. **After migration:** Enable Dependabot (5 minutes)
4. **In 3 months:** Evaluate if more automation is needed
5. **Only then:** Consider custom scripts/workflows

### The Honest Truth

This is a hobby fork of a dormant fork of an active graphics library. The right amount of infrastructure is "minimal." The specialists proposed enterprise-grade solutions for a solo-maintainer project.

**Do the migration. Enable Dependabot. See if that's enough.**

It probably is.

---

*Solutions Synthesis — Swiss Rounds v3 Round 1*
*"Simplicity is the ultimate sophistication." — Leonardo da Vinci*
