# Round 1 Solution Synthesis: cosmo-sokol-update

**Generated:** 2026-02-09  
**Synthesizer:** Solution synthesis subagent  
**Inputs:** 8 specialist reports + redundancy analysis + devil's advocate critique

---

## Executive Summary

The critic's challenges fundamentally reframe this analysis. The real question isn't "how do we automate upstream sync" but **"should ludoplex/cosmo-sokol exist at all, and if so, what's the minimum intervention needed?"**

**Bottom Line:** Before doing ANY work, **contact bullno1**. If bullno1 has plans or the project is abandoned, that changes everything. If we proceed, **the minimum viable path is 4-6 hours of work, not 40-60.**

---

## 1. Addressing the Critic's Challenges

### Challenge 1: Should We Automate at All?

**Answer: NO, not initially.**

The critic is right. The manual SOKOL_FUNCTIONS list has worked for 14 months. The actual delta is ~25-40 function changes, not 1,044 commits. The specialist reports over-engineered a solution for a problem that doesn't yet exist.

**Decision:**
- ❌ Do NOT build automation infrastructure now
- ✅ Document the manual process clearly
- ✅ Create a simple `UPGRADE.md` checklist
- ⏸️ Revisit automation IF manual updates become frequent (>2x/year)

**Rationale:** Automation ROI requires:
- Setup cost: ~20 hours (scripts, CI, testing)
- Per-update cost (manual): ~4-6 hours
- Per-update cost (automated): ~1-2 hours
- Break-even: ~5-6 updates

At quarterly cadence, that's 1.5 years to ROI. At annual cadence, it's 4+ years. Manual wins.

---

### Challenge 2: Is "Ask bullno1" the Right First Step?

**Answer: YES, absolutely. This should have been the FIRST thing.**

**Why this matters:**
1. bullno1 might be planning an update already
2. bullno1 might have decided to freeze (stable snapshot strategy)
3. bullno1 might be open to collaboration or accepting PRs
4. The project might be abandoned (different strategy entirely)

**Action Item #1 (5 minutes):**
```markdown
Open issue on bullno1/cosmo-sokol:

Title: "Plans for upstream sync? (sokol is 14 months behind)"

Body:
Hi! I maintain a fork at ludoplex/cosmo-sokol and I'm evaluating whether to:
1. Sync upstream (including the Aug 2025 resource view update)
2. Stay on current versions (stable snapshot approach)
3. Something else

Before duplicating effort, wanted to check:
- Do you have plans to update?
- Would you accept PRs for upstream sync?
- Any blockers or known issues with the resource view update?

Thanks for creating this awesome project!
```

**DO THIS FIRST. Everything else is contingent on the answer.**

---

### Challenge 3: What's the TRUE Minimum Viable Path?

**Scenario A: bullno1 is active and planning update**
→ Wait and/or offer to help with their update. **Effort: 0 hours.**

**Scenario B: bullno1 accepts PRs, wants collaboration**
→ Submit PRs to bullno1/cosmo-sokol instead of maintaining separate fork. **Effort: Same work, better outcome.**

**Scenario C: bullno1 is inactive/abandoned, or wants to stay frozen**
→ We maintain ludoplex/cosmo-sokol. Continue to analysis below.

---

### For Scenario C: The TRUE Minimum Viable Path

**Question:** Do we even need to update sokol?

| Factor | Update | Don't Update |
|--------|--------|--------------|
| Code works today | ✅ | ✅ |
| New sokol features needed | ❓ Unknown | N/A |
| Security fixes | ⚠️ Possible | Risk accepted |
| Community confusion | Reduced | "Why is this old?" |
| Maintenance burden | Higher | Near zero |

**Decision Framework:**

```
IF no active user demand for new sokol features
  AND no known security issues in pinned version
  AND demo app works correctly
THEN: Stable Snapshot Strategy — don't update, document version

ELSE IF specific feature/fix needed
THEN: Targeted Update — update to specific commit with that fix

ELSE IF staying current is strategically valuable
THEN: Full Upstream Sync — do the work
```

**For ludoplex/cosmo-sokol specifically:**
- Is there user demand? → Unknown. Check issues, ask.
- Security issues? → Not identified in reports.
- Demo works? → Presumably yes.

**Recommendation:** Default to **Stable Snapshot** unless there's a reason not to.

---

### The Actual Minimum Viable Path (If Update IS Needed)

**Phase 0: Prerequisite (30 minutes)**
1. ✅ Open issue on bullno1/cosmo-sokol — wait for response
2. ✅ Check ludoplex/cosmo-sokol issues — is anyone asking for updates?

**Phase 1: Cosmopolitan Toolchain Update (1-2 hours)**
- Low risk, high value
- Update CI from cosmocc 3.9.6 → 4.0.2
- `version: "latest"` in GitHub Actions
- Build, verify nothing breaks

**Phase 2: Decide on Sokol Strategy (1 hour of thinking)**

| Option | Effort | Outcome |
|--------|--------|---------|
| **A: Stay frozen** | 2 hours | Document "this is sokol circa Nov 2024", update README |
| **B: Pre-resource-view update** | 8-12 hours | Get bug fixes through Aug 2025, avoid breaking change |
| **C: Full resource view migration** | 30-50 hours | Match latest upstream, major rework |

**Recommended: Option A or B.** Option C only if there's a specific user demand.

**Phase 3: If Option B (pre-resource-view update)**

1. Find the commit just before Aug 23, 2025 resource view update
2. Update sokol submodule to that commit
3. Diff SOKOL_FUNCTIONS against new headers (grep, not automation)
4. Manually update gen-sokol (~20-30 functions, 2-3 hours)
5. Regenerate shims
6. Build and test
7. Commit with clear changelog

**Total for Option B: ~8-12 hours**

---

### Challenge 4: When Does Automation ROI Make Sense?

**Automation makes sense when:**
1. Updates are frequent (quarterly or more)
2. Updates are large (100+ function changes)
3. Multiple people need to do updates
4. The manual process is error-prone

**Automation does NOT make sense when:**
1. Updates are rare (annual or less)
2. Updates are small (~20-40 changes)
3. One person owns the project
4. The manual process is straightforward

**For cosmo-sokol:**
- Update frequency: Unknown, historically ~0/year
- Update size: ~25-40 function changes per major version
- Maintainers: 1 (ludoplex)
- Manual complexity: Medium (documented process)

**Verdict: Automation NOT justified at this time.**

**Revisit automation if:**
- We do 3+ updates in one year
- sokol starts releasing breaking changes monthly
- Multiple contributors need to sync independently

---

### Challenge 5: "Stable Snapshot" vs "Track Upstream" Decision Framework

```
┌─────────────────────────────────────────────────────────────────┐
│           DECISION: How to Position This Fork                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Q1: Is there ACTIVE USER DEMAND for new upstream features?     │
│      │                                                          │
│      ├─► YES ──► Q2: Is the required feature in a recent       │
│      │              upstream commit?                            │
│      │              │                                           │
│      │              ├─► YES ──► TRACK UPSTREAM (selective)      │
│      │              │           Update to commit with feature   │
│      │              │                                           │
│      │              └─► NO ───► STABLE SNAPSHOT                 │
│      │                          Feature not available anyway    │
│      │                                                          │
│      └─► NO ───► Q3: Are there SECURITY CONCERNS in             │
│                      pinned versions?                           │
│                      │                                          │
│                      ├─► YES ──► TARGETED UPDATE                │
│                      │           Cherry-pick security fixes     │
│                      │                                          │
│                      └─► NO ───► STABLE SNAPSHOT                │
│                                  "It works, don't touch it"     │
│                                                                 │
│  Q4: Is TRACKING UPSTREAM strategically valuable?               │
│      (ecosystem alignment, contributor attraction, etc.)        │
│      │                                                          │
│      ├─► YES ──► Consider TRACK UPSTREAM with scheduled cadence │
│      │           (quarterly, semi-annually)                     │
│      │                                                          │
│      └─► NO ───► STABLE SNAPSHOT remains optimal                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**For ludoplex/cosmo-sokol today:**
- Q1: Unknown → Check issues, ask users
- Q3: No security concerns identified
- Q4: Probably no (fork serves specific use case)

**Default recommendation: STABLE SNAPSHOT**

---

## 2. Synthesized Recommendations

### Immediate Actions (This Week)

| # | Action | Time | Outcome |
|---|--------|------|---------|
| 1 | Open issue on bullno1/cosmo-sokol | 5 min | Understand upstream plans |
| 2 | Check ludoplex issues for user demand | 10 min | Know if updates are wanted |
| 3 | Update README with version info | 30 min | Set expectations clearly |

**That's it for now.** Wait for bullno1 response before proceeding.

### If bullno1 Is Inactive AND Updates Are Desired

| # | Action | Time | Priority |
|---|--------|------|----------|
| 4 | Update cosmocc to 4.0.2 | 1-2 hrs | P1 - Low risk |
| 5 | Decide: Freeze vs Pre-Aug-2025 vs Full | 1 hr | P1 - Required |
| 6 | Execute chosen strategy | Varies | P1 |
| 7 | Create UPGRADE.md checklist | 1 hr | P2 - For future |

### What NOT To Do (Avoid Premature Optimization)

| ❌ Don't Do | Why |
|------------|-----|
| Build automated API extraction scripts | Manual is fine for rare updates |
| Create comprehensive CI test matrix | Overkill for a demo app |
| Implement versions.json schema | Not needed unless multiple contributors |
| Add struct size assertions everywhere | Do it when ABI breaks, not before |
| Set up weekly upstream monitoring | Only monitor when actively planning update |

---

## 3. Revised Effort Estimates

### If We Do Nothing (Stable Snapshot)
- Total effort: **2 hours**
- Update README, close issue, done

### If We Update to Pre-Resource-View
- Cosmo toolchain update: 2 hours
- Sokol update (pre-Aug-2025): 8-10 hours
- Testing and validation: 2-4 hours
- Documentation: 1 hour
- **Total: 13-17 hours**

### If We Do Full Resource View Migration
- All of the above: 15 hours
- Resource view API migration: 15-25 hours
- Shader recompilation: 2-4 hours
- Extended testing: 4-8 hours
- **Total: 36-52 hours**

### If We Build Full Automation
- All manual work: 15-50 hours
- Automation scripts: 10-15 hours
- CI infrastructure: 8-12 hours
- Test suite: 10-15 hours
- **Total: 43-92 hours** (before seeing any automation benefit)

---

## 4. Risk Analysis (Revised)

### Risk: Over-Engineering
**Likelihood: HIGH** (specialist reports show this tendency)  
**Mitigation:** Start with minimum viable, add only when needed

### Risk: Under-Engineering
**Likelihood: LOW** (manual process is well-understood)  
**Mitigation:** Document manual process for future reference

### Risk: Wasted Effort
**Likelihood: MEDIUM** (if bullno1 updates while we work)  
**Mitigation:** Ask bullno1 FIRST

### Risk: Project Abandonment
**Likelihood: LOW** (demo app works, has users)  
**Mitigation:** Stable snapshot strategy means minimal ongoing commitment

---

## 5. macOS Support Decision

**All reports agree: macOS should remain a stub.**

| Factor | Analysis |
|--------|----------|
| Implementation effort | 2-4 person-months |
| User demand | Unknown, likely low |
| Technical complexity | High (objc_msgSend rewrite) |
| Alternative | Users can use native Mac tools |

**Decision:** Document macOS as "not supported, contributions welcome." No investment.

---

## 6. Final Decision Matrix

| Strategy | When to Choose | Effort | Risk |
|----------|----------------|--------|------|
| **Do Nothing** | bullno1 is active | 0 hrs | None |
| **Stable Snapshot** | No user demand, code works | 2 hrs | Low |
| **Pre-Aug-2025 Update** | Want bug fixes, avoid breakage | 15 hrs | Medium |
| **Full Upstream Sync** | Specific feature needed post-Aug-2025 | 40+ hrs | High |
| **Automate First** | Never. Automation comes after proven need | 50+ hrs | Very High |

---

## 7. Concrete Next Steps

### Step 1: Contact bullno1 (Today)
```bash
# Go to https://github.com/bullno1/cosmo-sokol/issues
# Open issue with template from section above
```

### Step 2: Wait for Response (1-2 weeks)
- If response: Adjust strategy accordingly
- If no response after 2 weeks: Assume inactive, proceed with own strategy

### Step 3: Check User Demand
- Search ludoplex/cosmo-sokol issues for update requests
- If no issues repo, consider if anyone actually uses this fork

### Step 4: Execute Minimum Viable Strategy
Based on findings from steps 1-3, choose ONE:
- A: Do nothing (bullno1 handling it)
- B: Stable snapshot (update docs only)
- C: Pre-Aug-2025 update (selective sync)
- D: Full sync (only if specifically needed)

---

## 8. Conclusion

The specialist reports provided excellent technical analysis but answered the wrong question. The critic correctly identified that we jumped to "how do we automate" without asking "should we do anything at all."

**Key Insights:**
1. The code works. That's not nothing.
2. 14 months of stability is a feature, not a bug.
3. Manual processes are fine when updates are rare.
4. Automation is a solution looking for a problem.
5. Always ask the upstream maintainer first.

**Recommended Path Forward:**
1. Ask bullno1 (5 minutes)
2. Check for user demand (10 minutes)
3. Probably: Stable snapshot + clear documentation (2 hours)
4. Defer everything else until there's a proven need

**Total Recommended Investment: 2-3 hours, not 40-60.**

The specialist reports are valuable documentation for IF we need to do a full update later. Archive them for reference. But don't act on them until there's a reason to.

---

## Appendix A: UPGRADE.md (If Needed Later)

```markdown
# Upgrading cosmo-sokol Dependencies

## Prerequisites
- Understand the gen-sokol prefix trick architecture
- Have a working build of current version
- Set aside 8-16 hours for a full sync

## Step 1: Update cosmopolitan toolchain
1. Change `version:` in `.github/workflows/build.yml` to latest
2. Build locally, verify no issues
3. Commit: "chore: update cosmocc to vX.Y.Z"

## Step 2: Update sokol submodule
1. `cd deps/sokol && git fetch origin`
2. Check CHANGELOG.md for breaking changes since current commit
3. Choose target commit (recommend: before major breaking changes)
4. `git checkout <target-commit>`
5. `cd ../.. && git add deps/sokol`

## Step 3: Update gen-sokol SOKOL_FUNCTIONS
1. Extract new functions: `grep 'SOKOL_APP_API_DECL' deps/sokol/sokol_app.h`
2. Compare against SOKOL_FUNCTIONS list in shims/sokol/gen-sokol
3. Add new functions, remove deleted functions
4. Run: `python shims/sokol/gen-sokol`

## Step 4: Build and Test
1. `./build`
2. Fix any compilation errors (usually missing Win32 definitions)
3. Run binary on Linux and Windows
4. Verify demo window appears and is interactive

## Step 5: Commit and Document
1. Commit with changelog of what changed
2. Update README.md with new version info
3. Tag release if appropriate
```

---

## Appendix B: When to Revisit This Analysis

Revisit this solution and consider the specialist recommendations if:

- [ ] bullno1 responds with "not maintaining, please fork"
- [ ] 3+ users request upstream sync
- [ ] A security vulnerability is discovered in pinned versions
- [ ] A specific sokol feature is needed that's only in recent commits
- [ ] MHI/DSAIC has a production use case requiring latest features

Until any of these conditions are met, the stable snapshot strategy is optimal.

---

*Solution synthesis complete. The answer to "how do we maintain this" turned out to be "we probably don't need to."*
