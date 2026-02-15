# Solver Validation: Finding the Path Forward

**Prepared by:** Solver (final synthesis subagent)  
**Date:** 2026-02-09  
**Status:** Decision framework and creative alternatives

---

## Executive Summary

The validation chain revealed a **3-5x gap** between PM estimates and reality. But "don't do it" isn't a satisfying answer. This synthesis explores creative paths forward that capture value without the full $15-25k migration.

| What We Know | PM Said | Reality |
|--------------|---------|---------|
| Breaking changes | 1 | 5-6 (incl. architecture rewrite) |
| Timeline | 5 days | 15-25 days for full sync |
| Budget | $5,354 | $10,000-$25,000 for full sync |
| ROI | Not calculated | Negative to marginal |

**The core tension:** The sync *as scoped* isn't worth it. But valuable work might still exist inside this project.

---

## 1. Synthesis of All Findings

### What Seeker Found (Ground Truth)
- **5 major breaking changes** in 2025 alone (PM only counted 1)
- **August 2025 Resource View Update** = fundamental API redesign, not a signature change
- `sg_attachments` removed entirely, `sg_view` added, `sg_bindings` restructured
- Realistic effort: **50-80 hours** (PM: 37 hours)
- Realistic timeline: **10-15 business days** (PM: 5 days)

### What Critic Found (Gap Analysis)
- PM synthesis **dropped seeker's warnings** entirely
- Resource View not mentioned anywhere in PM plan
- Tools designed for "detecting drift" but problem requires "migration tooling"
- Shader recompilation requirement not addressed
- macOS backend (stub only) gets more broken after sync
- gen-sokol.py → C rewrite unscoped but required for philosophy compliance

### What Analyst Found (Economic Reality)
- **Unknown user base** — possibly just ludoplex internal use
- **No documented problem** with current version
- **Negative to marginal ROI** on full sync
- Options ranked: Fork/Defer > Partial Sync > Full Sync
- Key question unanswered: *Why does this need to happen?*

### The Meta-Problem
The PM created a detailed plan for executing a sync that nobody validated should happen. Three validators all found scope/cost issues, but the fundamental question — **"What value does this create?"** — remains unanswered.

---

## 2. Creative Alternatives

The analyst presented four options (Full/Partial/Fork/Defer). Here are alternatives that might thread the needle:

### Alternative A: "Cherry-Pick Sync"
**Concept:** Don't sync commits sequentially. Cherry-pick specific valuable changes.

| Aspect | Details |
|--------|---------|
| Scope | Identify 10-20 high-value commits (bug fixes, specific features) |
| Avoids | Resource View migration, bulk breaking changes |
| Cost | ~$2,000-4,000 |
| Timeline | 3-5 days |
| Risk | MEDIUM — conflicts possible but manageable |

**How it works:**
1. Audit sokol CHANGELOG for bug fixes that affect cosmo-sokol's use case
2. Cherry-pick those commits in isolation
3. Resolve conflicts case-by-case
4. Skip architecture changes entirely

**When this makes sense:**
- You're hitting specific bugs that upstream fixed
- You want specific features (not "everything")
- You don't need the new Resource View architecture

### Alternative B: "Shim the Old API"
**Concept:** Let upstream evolve. Build a compatibility layer that translates old API → new API.

| Aspect | Details |
|--------|---------|
| Scope | Create `sokol_compat.h` that wraps new API in old interface |
| Avoids | Rewriting all calling code |
| Cost | ~$3,000-5,000 |
| Timeline | 5-8 days |
| Risk | MEDIUM — maintenance burden, performance overhead |

**How it works:**
1. Sync to upstream HEAD
2. Create `sokol_compat.h` with:
   - `sg_attachments` emulation using `sg_view`
   - Old `sg_bindings` → new `sg_bindings` translation
   - Old `sg_apply_uniforms(stage, slot, data)` → new signature shim
3. Existing cosmo-sokol code uses compat layer
4. New code can use native API

**When this makes sense:**
- You want current upstream for security/bug fixes
- You can't afford to rewrite all downstream code
- Performance overhead is acceptable (extra indirection)

### Alternative C: "Minimum Viable Tooling"
**Concept:** The sync isn't worth it, but the *tooling* has independent value.

| Aspect | Details |
|--------|---------|
| Scope | Build `drift-report.c` and `changelog-scan.c` only |
| Avoids | Actual sync execution |
| Cost | ~$1,000-1,500 |
| Timeline | 2-3 days |
| Outcome | Know exactly what you'd be getting into |

**How it works:**
1. Build just the analysis tools
2. Run them to generate detailed sync requirements
3. Archive the report for future reference
4. Defer actual sync decision with full information

**When this makes sense:**
- You're not ready to commit to sync
- You want to understand the problem before solving it
- You might revisit in 6-12 months

### Alternative D: "Upstream Contribution Path"
**Concept:** Instead of pulling upstream changes, push cosmo-specific value upstream.

| Aspect | Details |
|--------|---------|
| Scope | Identify cosmo-sokol innovations worth upstreaming |
| Avoids | Ongoing fork maintenance burden |
| Cost | ~$2,000-4,000 |
| Timeline | 4-6 weeks (upstream review process) |
| Outcome | Reduces future sync burden |

**How it works:**
1. Audit cosmo-sokol for improvements over upstream
2. Clean them up for contribution
3. Submit PRs to floooh/sokol
4. If accepted, future syncs are simpler

**When this makes sense:**
- cosmo-sokol has valuable innovations
- Reducing maintenance burden is priority
- You have time for upstream review cycles

### Alternative E: "Staged Partial + Evaluation"
**Concept:** Do Option B (partial sync to pre-Aug-2025), then evaluate full migration with real data.

| Aspect | Details |
|--------|---------|
| Phase 1 | Partial sync to July 2025 (avoid Resource View) |
| Phase 1 Cost | $5,000-8,000 |
| Phase 1 Time | 8-12 days |
| Phase 2 | Evaluate if Resource View migration is worth it |
| Phase 2 Cost | $0 (decision point) or $8,000-15,000 (if proceeding) |

**How it works:**
1. Sync to the commit *before* Aug 23, 2025 Resource View Update
2. Get 9 months of bug fixes and improvements
3. Run in production for 1-2 months
4. Evaluate: Did this help? Is more needed?
5. Only then decide on full migration

**When this makes sense:**
- You want progress without betting $15-25k
- You need data to justify larger investment
- "Wait and see" with some forward motion

---

## 3. What Would Make Full Sync Worth It?

The analyst is right that current data doesn't justify $15-25k. Here's what would change that calculus:

### Scenario 1: Active External Users
**If** cosmo-sokol has 10+ active external users depending on it:
- Community obligation matters
- Maintenance burden is shared
- Sync has multiplied value

**How to verify:** Check GitHub issues, stars, forks. Survey users.

### Scenario 2: Critical Bug in Current Version
**If** there's a known bug causing real problems that upstream fixed:
- Sync becomes "bug fix" not "maintenance"
- ROI becomes concrete (cost of bug × likelihood × impact)

**How to verify:** Review ludoplex's issue tracker. Ask what's broken.

### Scenario 3: Required Upstream Feature
**If** a specific upstream feature is needed for planned development:
- Sync becomes enabling infrastructure
- Delay costs are real

**How to verify:** What's the cosmo-sokol roadmap? What features are blocked?

### Scenario 4: Security Vulnerability
**If** there's an unpatched vulnerability in pre-Nov-2024 sokol:
- Sync becomes mandatory
- Timeline becomes "ASAP"

**How to verify:** CVE search, security advisories, upstream commits for security fixes.

### Scenario 5: Strategic Commitment
**If** ludoplex plans 5+ years of active cosmo-sokol development:
- Upfront investment amortizes over many years
- Staying current has compounding value

**How to verify:** What's the 5-year vision for cosmo-sokol?

---

## 4. Decision Framework

### If You Have 10 Minutes
Ask these three questions:
1. **Is current cosmo-sokol causing problems?** (No → Defer)
2. **Do you need specific upstream features?** (No → Fork)
3. **Are there external users?** (No → Fork or minimal tooling)

### If You Have 2 Hours
1. Count active external users/dependents
2. List specific bugs or missing features causing pain
3. Define the 3-year vision for cosmo-sokol
4. Calculate: What else could $15k fund?

### Decision Matrix

| Situation | Recommended Path | Investment |
|-----------|------------------|------------|
| Works fine, no external users | **Fork permanently** | $500 |
| Works fine, some external users | **Defer 6-12 months** | $0 now |
| Specific bug causing pain | **Cherry-pick that fix** | $500-2,000 |
| Need features pre-Aug 2025 | **Partial sync (Alternative E)** | $5,000-8,000 |
| Long-term strategic asset | **Staged migration (E → full)** | $12,000-20,000 |
| Security vulnerability | **Emergency sync** | Whatever it costs |

---

## 5. If Proceeding: Revised Plan

If after answering the above questions, sync is justified, here's the adjusted plan:

### Option: Partial Sync (Recommended if sync needed)

**Target:** Sync to commit immediately before Aug 23, 2025 Resource View Update

**Scope:**
- 4 breaking changes (not 5) — avoid Resource View
- No architecture migration
- Gets ~9 months of improvements

**Revised Estimates:**

| Category | Original PM | Adjusted |
|----------|-------------|----------|
| Timeline | 5 days | **10-12 business days** |
| Effort | 37 hours | **60-80 hours** |
| Budget | $5,354 | **$8,000-$12,000** |

**Revised Phase Plan:**

| Phase | Duration | Focus |
|-------|----------|-------|
| 0 | 1 day | Analysis: Identify exact sync target commit |
| 1 | 2 days | Tooling: Build analysis tools (drift-report, changelog-scan) |
| 2 | 3 days | Sync prep: Identify all changes needed, create migration plan |
| 3 | 3 days | Execution: Submodule update, fix breaking changes |
| 4 | 2 days | Testing: Cross-platform verification, regression testing |
| 5 | 1 day | Release: Tag, document, announce |

**New Risk Mitigations:**

| Risk | Mitigation |
|------|------------|
| Breaking changes cascade | Incremental commit-by-commit sync with tests |
| macOS gets more broken | Accept and document; defer to separate project |
| gen-sokol.py updates needed | Keep Python for now; C rewrite is separate project |
| Shader recompilation | Audit shader usage before sync; may be N/A for cosmo-sokol |

### Option: Full Sync (Only if strategically justified)

**Only if:** Clear strategic commitment, multiple users, specific feature need.

**Revised Estimates:**

| Category | Original PM | Adjusted |
|----------|-------------|----------|
| Timeline | 5 days | **20-30 business days** |
| Effort | 37 hours | **120-160 hours** |
| Budget | $5,354 | **$18,000-$24,000** |

**Added Phases:**
- Resource View migration: 5-7 days, $6,000-$9,000
- Shader pipeline audit/update: 2-3 days, $2,000-$3,000
- Extended testing for new architecture: 3-4 days, $3,000-$4,500

---

## 6. If Not Proceeding: What to Do Instead

### Immediate Actions (< $500)
1. **Document the decision** — Why we're not syncing, what would change that
2. **Archive this analysis** — Don't repeat this work later
3. **Update README** — Note that fork is stable but not tracking upstream

### Low-Investment Wins (~$1,000-2,000)
1. **Build drift-report.c** — Always know how far behind you are
2. **Create sync runbook** — Document exact steps for future sync
3. **Audit for security issues** — Targeted review of upstream security commits

### Set Review Trigger
Create a reminder to re-evaluate in 6-12 months, or when:
- Upstream releases "stable" Vulkan backend
- Resource View API matures
- External user base grows
- Specific feature becomes needed

---

## 7. Final Recommendation

### Primary Path: Alternative E — Staged Partial Sync

**Why this path:**
1. **Captures 80% of value** (9 months of bug fixes) for **40% of cost**
2. **Avoids biggest risk** (Resource View architecture migration)
3. **Creates option value** — Can still do full sync later with better data
4. **Limits downside** — If partial sync causes problems, abort before larger investment

**Recommended Budget:** $8,000-$10,000  
**Recommended Timeline:** 12 business days  
**Recommended Target:** Last commit before Aug 23, 2025 Resource View Update

### Alternative: If No Clear Business Need → Fork Permanently

If answering the questions in Section 3-4 reveals:
- No external users
- Current version works fine
- No specific feature blocked

Then **fork permanently**, document the decision, and move on. Spend the $15,000 elsewhere.

---

## 8. Summary

| Question | Answer |
|----------|--------|
| Should we do the PM's plan as-is? | **No.** Underestimates by 3-5x. |
| Should we abandon the project? | **Not necessarily.** Creative alternatives exist. |
| What's the minimum viable path? | **Cherry-pick or partial sync** — $2,000-8,000 |
| What would make full sync worth it? | External users, critical bugs, strategic commitment |
| What's the recommended path? | **Staged partial sync** (Alternative E) OR **permanent fork** |

### The One Question That Matters
> **Is anyone besides ludoplex actually using cosmo-sokol, and is the current version causing them problems?**

The answer to this question determines everything. If yes, invest appropriately. If no, fork and move on.

---

## Appendix: Quick Reference Decision Tree

```
START: Is cosmo-sokol causing problems today?
│
├── YES: What specifically?
│   ├── Bug in current version
│   │   └── Cherry-pick that fix ($500-2,000) → DONE
│   ├── Missing specific feature (pre-Aug 2025)
│   │   └── Partial sync ($5,000-8,000) → DONE
│   ├── Missing Resource View or Vulkan
│   │   └── Is this worth $18,000+?
│   │       ├── YES: Full sync (accept costs)
│   │       └── NO: Wait for upstream to stabilize
│   └── Security vulnerability
│       └── Emergency targeted sync (whatever it costs)
│
└── NO: Is there strategic value in staying current?
    ├── YES (external users, long-term plans)
    │   └── Partial sync now, evaluate full sync later
    └── NO
        └── Fork permanently ($500) → DONE
```

---

*Solver validation complete.*

**Bottom Line:** The PM plan isn't viable, but the project isn't dead. There's a $5,000-10,000 middle path that captures most of the value without the $15,000-25,000 architecture migration. Answer the key questions first, then proceed with the appropriate-sized investment.
