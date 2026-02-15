# PM Synthesis Validation Report

**Prepared by:** Seeker (subagent)  
**Date:** 2026-02-09  
**Status:** Independent verification of PM estimates

---

## Executive Summary

| Claim | PM Estimate | Validation | Status |
|-------|-------------|------------|--------|
| 37 hours effort | 4 C tools + 2 CI + hooks + docs | **OPTIMISTIC** | ⚠️ |
| $5,354 budget | Claude API + CI | **PLAUSIBLE BUT UNCERTAIN** | ⚠️ |
| 1,032 commits behind | Since Nov 2024 | **CANNOT VERIFY EXACT COUNT** | ❓ |
| 5 business days critical path | Implementation timeline | **HIGHLY OPTIMISTIC** | ⚠️ |

---

## 1. Effort Estimate: 37 Hours

### Claimed Scope
- 4 C tools (~400 lines each = ~1,600 LOC total)
- 2 CI workflows
- Pre-commit hooks
- Documentation

### Industry Benchmarks

**Source:** QSM Function Point Languages Table v5.0  
**URL:** https://www.qsm.com/resources/function-point-languages-table

| Language | Avg SLOC/FP | Median | Range |
|----------|-------------|--------|-------|
| C | 97 | 99 | 39-333 |
| C++ | 50 | 53 | 25-80 |

**Industry productivity rates** (from software estimation literature):
- Experienced developer: 20-50 LOC/hour for new C code (including testing)
- AI-assisted: Potentially 2-3x higher, but requires review/refinement
- Complex integration work: Lower end of range

### Analysis

For 1,600 lines of C code at 25-50 LOC/hour:
- **Low estimate:** 1,600 / 50 = 32 hours (just coding)
- **High estimate:** 1,600 / 25 = 64 hours (just coding)

**Missing from 37-hour estimate:**
- Testing and debugging (typically 25-50% of development time)
- Integration complexity with sokol upstream changes
- CI workflow development and debugging
- Documentation (typically 10-20% of development time)
- Pre-commit hook testing across platforms

### Verdict: ⚠️ OPTIMISTIC

37 hours is at the **aggressive end** for the coding alone, and likely **underestimates** the integration, testing, and debugging time. A more realistic estimate would be **50-80 hours** for a complete, tested solution.

---

## 2. Budget Estimate: $5,354

### Claude API Pricing (Current)

**Source:** https://claude.com/pricing (formerly anthropic.com/pricing)

| Model | Input | Output | Cache Write | Cache Read |
|-------|-------|--------|-------------|------------|
| Opus 4.6 | $5/MTok | $25/MTok | $6.25/MTok | $0.50/MTok |
| Sonnet 4.5 | $3/MTok | $15/MTok | $3.75/MTok | $0.30/MTok |
| Haiku 4.5 | $1/MTok | $5/MTok | $1.25/MTok | $0.10/MTok |

### Cost Estimation

Assuming heavy Opus/Sonnet usage for code generation and review:

**Per implementation session (rough estimate):**
- Context loading: ~50K tokens input per session
- Output generation: ~20K tokens per session
- At 10-20 major sessions: 500K-1M input, 200K-400K output

**Using Sonnet 4.5:**
- Input: 1M tokens × $3/MTok = $3.00
- Output: 400K tokens × $15/MTok = $6.00
- **Subtotal:** ~$9 per heavy session

**For full project (10-20 sessions):** $90-$180

**Using Opus 4.6 (more expensive):**
- Could be $300-$600 for equivalent work

### CI Compute Costs

**Source:** https://docs.github.com/en/billing/concepts/product-billing/github-actions

| Runner Type | Rate |
|-------------|------|
| Linux 2-core | $0.006/min |
| Windows 2-core | $0.010/min |
| macOS 3-core | $0.062/min |

**For a typical CI setup (cross-platform builds):**
- 5-10 min per build across 3 platforms
- ~50-100 builds during development
- Cost: ~$50-$200

### Analysis

The $5,354 budget seems **significantly inflated** for a 37-hour project:
- Claude API costs: ~$200-$600 (heavy usage)
- CI costs: ~$50-$200
- **Realistic total:** $300-$800

The $5,354 figure might include:
- Human developer time (37 hrs × $100-$150/hr = $3,700-$5,550)
- Contingency buffer

### Verdict: ⚠️ PLAUSIBLE BUT UNCLEAR BREAKDOWN

If budget includes human labor, it's reasonable. If it's meant to represent API/infrastructure costs alone, it's **significantly overestimated**.

---

## 3. Commits Behind: 1,032

### Sokol Repository Activity

**Source:** https://github.com/floooh/sokol

- **Repository:** floooh/sokol (9,579 stars as of Feb 2026)
- **Active maintainer:** Andre Weissflog (@floooh)
- **Commit frequency:** Very active (multiple commits per week)

### Changelog Analysis (Nov 2024 - Feb 2026)

**Source:** https://raw.githubusercontent.com/floooh/sokol/master/CHANGELOG.md

**Major Breaking Changes Since Late 2024:**

1. **23-Aug-2025: Resource View Update** (BREAKING)
   - `sg_attachments` object type removed
   - New `sg_view` object type added
   - `sg_bindings` struct completely restructured
   - Requires shader recompilation

2. **02-Dec-2025: Experimental Vulkan Backend** (BREAKING)
   - Major additions to sokol_app.h and sokol_gfx.h
   - Platform-specific config changes

3. **04-Dec-2025: Stats API Changes** (BREAKING)
   - `sg_frame_stats` → `sg_stats` rename
   - Function signature changes

4. **05-Dec-2025: sokol_gfx_imgui.h API Changes** (BREAKING)
   - `sgimgui_init()` → `sgimgui_setup()`
   - Context arg removed

5. **15-Sep-2025: Image Data Structure Changes** (BREAKING)
   - `sg_image_data.subimage[face][mip]` → `sg_image_data.mip_levels[mip]`

### Commit Count Verification

**API Query Result:** https://api.github.com/repos/floooh/sokol/compare/master~200...master

The 200-commit span covers Jan 18, 2025 to Feb 8, 2026 (about 13 months ago to present = ~3 weeks of commits).

**Rough extrapolation:**
- 200 commits per month (high activity periods)
- Nov 2024 to Feb 2026 = ~15 months
- **Estimated range:** 300-600 commits

### Verdict: ❓ CANNOT VERIFY EXACT COUNT

The **1,032 commits** figure seems **high but not implausible** given sokol's activity level. However, I could not verify the exact count with the tools available. The changelog shows **at least 5 major breaking changes** that would require significant adaptation work.

**Note:** If "1,032 commits behind" refers to a specific fork divergence, this would need to be verified against the actual cosmo-sokol fork's last sync point.

---

## 4. Critical Path: 5 Business Days

### Timeline Analysis

**Claimed 5-day breakdown would require:**
- Day 1-2: Tool implementation (~16 hours)
- Day 3: CI workflows (~8 hours)
- Day 4: Testing & integration (~8 hours)
- Day 5: Documentation & polish (~5 hours)

### Reality Check

**Significant upstream breaking changes identified:**

1. **Resource View Update (Aug 2025)**
   - This alone requires adapting all rendering code
   - New shader compilation workflow
   - API surface completely changed for bindings

2. **Multiple sg_* function signature changes**
   - Scattered throughout 2025 changelogs
   - Each requires code audit and update

**For a fork that's been divergent since Nov 2024:**
- Identifying all breaking changes: 1-2 days
- Adapting to resource view update: 2-3 days
- Testing across platforms: 1-2 days
- Documentation updates: 1 day

### Verdict: ⚠️ HIGHLY OPTIMISTIC

5 business days is **extremely aggressive** given the scope of upstream breaking changes. A more realistic estimate:

| Scenario | Timeline |
|----------|----------|
| Optimistic (experienced dev, focused effort) | 8-10 business days |
| Realistic (standard development) | 10-15 business days |
| Conservative (thorough testing) | 15-20 business days |

---

## 5. Key Risk: sg_apply_uniforms Change

### What Changed

The PM synthesis mentions an `sg_apply_uniforms` API change as significant.

**From the changelog (Aug 2025 Resource View Update):**
- The entire uniform/binding model was restructured
- `sg_bindings` now uses unified `sg_view` array instead of separate arrays
- This is part of the broader "resource view" architectural change

### Impact Assessment

This isn't just a function rename—it's a **fundamental API redesign** that affects:
- How shaders declare bindings
- How bindings are set at runtime
- The entire resource management model

### Mitigation

Tools to automate this change would need to:
1. Parse existing code for old binding patterns
2. Identify shader bindslot collisions
3. Generate new code using `sg_view` objects
4. Update all `sg_apply_bindings()` call sites

---

## 6. External Resources Consulted

| Resource | URL | Relevance |
|----------|-----|-----------|
| Sokol GitHub | https://github.com/floooh/sokol | Primary source |
| Sokol CHANGELOG | https://raw.githubusercontent.com/floooh/sokol/master/CHANGELOG.md | Breaking changes |
| Resource View Blog Post | https://floooh.github.io/2025/08/17/sokol-gfx-view-update.html | Major breaking change details |
| Claude API Pricing | https://claude.com/pricing | Cost validation |
| GitHub Actions Billing | https://docs.github.com/en/billing/concepts/product-billing/github-actions | CI cost validation |
| QSM Function Points | https://www.qsm.com/resources/function-point-languages-table | LOC estimation benchmarks |

---

## 7. Recommendations

### Immediate Actions

1. **Verify exact fork divergence point** - Check cosmo-sokol fork's last upstream sync commit hash
2. **Audit breaking changes** - Create comprehensive list against actual codebase
3. **Revise timeline** - Adjust to 10-15 business days minimum
4. **Clarify budget** - Separate labor costs from API/infrastructure costs

### Risk Mitigation

1. **Incremental sync strategy** - Consider syncing to intermediate commits rather than HEAD
2. **Automated testing** - Invest in test infrastructure before changes
3. **Rollback plan** - Maintain ability to revert if sync causes regressions

---

## Conclusion

The PM synthesis estimates are **optimistic across the board**:

- **37 hours** likely underestimates by 30-50%
- **$5,354** needs breakdown clarity (labor vs. infrastructure)
- **1,032 commits** unverified but breaking change scope is significant
- **5 business days** should be **10-15 business days** minimum

The major risk factor is the **August 2025 resource view update**, which represents a fundamental API redesign requiring substantial adaptation effort beyond simple find-and-replace migrations.
