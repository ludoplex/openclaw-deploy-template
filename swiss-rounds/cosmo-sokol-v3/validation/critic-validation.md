# Critic Validation Report: cosmo-sokol v3 Upstream Sync

**Prepared by:** Critic (subagent)  
**Date:** 2026-02-09  
**Status:** Critical review of seeker validation & PM synthesis

---

## Executive Summary

| Finding | Severity | Impact |
|---------|----------|--------|
| PM missed 5 breaking changes seeker found in 2025 | **CRITICAL** | Timeline/effort underestimated 3-4x |
| Resource View Update (Aug 2025) not in PM plan | **CRITICAL** | Architectural rewrite required |
| 5-day timeline ignores seeker's 10-15 day recommendation | **HIGH** | Project will overrun |
| Budget math is correct but effort estimate is wrong | **HIGH** | Budget should be ~$8,000-$12,000 |
| Tool scope assumes simple API drift, not API redesign | **MEDIUM** | Tools will need significant rework |

**Bottom line:** The PM synthesis contradicts seeker's findings on timeline, effort, and scope. The PM stuck with optimistic estimates despite seeker flagging them as "highly optimistic."

---

## 1. Critical Gap: Missing Breaking Changes

### What Seeker Found (seeker-validation.md, Section 3)
Seeker identified **5 major breaking changes** from the CHANGELOG:

| Date | Change | Seeker Section |
|------|--------|----------------|
| 23-Aug-2025 | Resource View Update — `sg_attachments` removed, `sg_view` added, `sg_bindings` restructured | Section 3: "Changelog Analysis" |
| 02-Dec-2025 | Experimental Vulkan Backend | Section 3: "Changelog Analysis" |
| 04-Dec-2025 | `sg_frame_stats` → `sg_stats` rename | Section 3: "Changelog Analysis" |
| 05-Dec-2025 | `sgimgui_init()` → `sgimgui_setup()` | Section 3: "Changelog Analysis" |
| 15-Sep-2025 | `sg_image_data.subimage[face][mip]` → `sg_image_data.mip_levels[mip]` | Section 3: "Changelog Analysis" |

### What PM Synthesized (overarching-plan.md, Section 1)
PM claims only **1 breaking change**:

> "Breaking Changes Detected: 1 major (Nov 2024 bindings cleanup)"

**Location:** overarching-plan.md, line ~22 (Key Decisions table)

### The Gap
The PM synthesis **dropped 4-5 breaking changes** that seeker explicitly documented. The Aug 2025 resource view update alone is described by seeker as:

> "This isn't just a function rename—it's a **fundamental API redesign**" — seeker-validation.md, Section 5

### Impact
Every tool in the PM plan assumes simple signature matching (detect drift, generate shims). But if `sg_bindings` was completely restructured and `sg_attachments` was removed entirely, the tools need to:
1. Understand the old API
2. Map to the new API
3. Generate migration code

This is **migration tooling**, not **sync tooling**.

---

## 2. Resource View Update: The Elephant in the Room

### What Seeker Documented (seeker-validation.md, Section 3 & 5)
The August 2025 "Resource View Update" requires:
- All rendering code to be adapted
- New shader compilation workflow
- Understanding of unified `sg_view` array instead of separate arrays

### What's Missing from PM Plan
Searching overarching-plan.md for "resource view": **0 results**  
Searching project-index.md for "resource view": **0 results**

The term appears nowhere in the PM synthesis despite seeker calling it out as the "major risk factor."

### Specific Issue with Phase 6 (overarching-plan.md, Section 3)
PM Phase 6 "Sync Execution" says:

> "Apply breaking change fixes | cosmo | Update gen-sokol.h signatures"

This assumes signature updates. But the resource view change:
- Removed `sg_attachments` (a type)
- Added `sg_view` (a new type)
- Restructured `sg_bindings` (a struct)

You can't "update signatures" for a removed type. This requires:
1. Deciding whether to shim the old API
2. OR updating all downstream code to use the new API
3. Testing all rendering paths

**PM estimate:** 0.5 day for Phase 6  
**Realistic estimate:** 2-3 days minimum for resource view migration alone

---

## 3. Timeline: PM Ignored Seeker's Warning

### Seeker's Explicit Recommendation (seeker-validation.md, Section 4)

> "5 business days is **extremely aggressive** given the scope of upstream breaking changes."

Seeker provided a table:

| Scenario | Timeline |
|----------|----------|
| Optimistic | 8-10 business days |
| Realistic | 10-15 business days |
| Conservative | 15-20 business days |

### PM's Response (overarching-plan.md, Section 7)
PM stuck with **5 business days**. No justification for rejecting seeker's assessment.

**Location:** overarching-plan.md, Section 7 "Timetable & Milestones"

### Why This Matters
If the project runs 10-15 days instead of 5:
- Budget doubles or triples
- Specialist availability needs rescheduling
- Dependencies on downstream projects slip

---

## 4. Budget Analysis: Math is Right, Input is Wrong

### PM's Budget (overarching-plan.md, Section 8.1)
```
37 hours × $150/hr = $5,550
+ $4 CI = ~$5,354
```

The math works. But the input (37 hours) is wrong.

### Seeker's Effort Estimate (seeker-validation.md, Section 1)

> "37 hours is at the **aggressive end** for the coding alone, and likely **underestimates** the integration, testing, and debugging time. A more realistic estimate would be **50-80 hours**."

### Corrected Budget
| Scenario | Hours | @ $150/hr | + CI |
|----------|-------|-----------|------|
| PM (optimistic) | 37h | $5,550 | $5,554 |
| Seeker low | 50h | $7,500 | $7,504 |
| Seeker high | 80h | $12,000 | $12,004 |
| With resource view work | 100h+ | $15,000+ | $15,004+ |

**Recommendation:** Budget should be **$10,000-$15,000** to account for:
- Seeker's 50-80 hour range
- Resource view migration not scoped
- Cross-platform testing on new APIs

---

## 5. Tool Scope Mismatch

### PM's Tool Design (overarching-plan.md, Section 2.1)
Four C tools planned:
1. `check-api-sync.c` — "Verify gen-sokol matches sokol headers"
2. `validate-sources.c` — Source validation
3. `changelog-scan.c` — Parse CHANGELOG for breaking changes
4. `drift-report.c` — Git submodule drift detection

### The Problem
These tools assume the problem is **detecting drift**. But if the API was fundamentally redesigned (resource views), you need tools that:
1. Parse the OLD API
2. Parse the NEW API
3. Generate transformation code
4. Validate the migration

`check-api-sync.c` as specced (project-index.md, seeker report section) is ~350 lines that "verify gen-sokol matches sokol headers."

But after the resource view update, `sg_bindings` has completely different fields. There's no "matching" — the types are structurally incompatible.

### Missing Tool
No tool is planned for:
- Detecting which call sites use `sg_attachments` (removed type)
- Generating `sg_view` equivalents
- Updating `sg_bindings` field access patterns

---

## 6. Project Index Contradicts Seeker Validation

### Dates Don't Align
**project-index.md, Section 4 (Seeker report summary):**
> "2024-11-07 | PR#1111 | sg_apply_uniforms() signature changed"

**seeker-validation.md, Section 3:**
> "23-Aug-2025: Resource View Update (BREAKING)"

These are **different breaking changes**. The Nov 2024 change is `sg_apply_uniforms`. The Aug 2025 change is the resource view restructure.

The project index only captured the Nov 2024 change. It missed the 2025 changes entirely.

### Missing Functions in Project Index (project-index.md, Section 4)
The index lists 5 missing functions:
- `sg_dispatch()`, `sg_draw_ex()`, `sg_make_view()`, `sg_destroy_view()`, `sapp_get_swapchain()`

But `sg_make_view()` and `sg_destroy_view()` are part of the resource view update. If these are missing, the fork can't use the new resource model at all — it's not just "missing functions," it's "missing an entire subsystem."

---

## 7. Hidden Dependencies

### 1. Shader Recompilation (seeker-validation.md, Section 3)
Seeker notes the resource view update "requires shader recompilation."

**Impact:** Not just C code changes. Any shaders using the old binding model need regeneration. Is there a shader pipeline? Who owns it? Not addressed.

### 2. gen-sokol Generator (project-index.md, Section 3)
`gen-sokol` is a 229-line Python script that generates `sokol_cosmo.c`.

**Problem:** PM plan says "All Python tooling → C/APE binaries." But the plan only allocates:
- `check-api-sync.c` for validation
- No replacement for `gen-sokol` itself

If `gen-sokol` must be rewritten in C, that's ~400-600 lines of C (parsing headers, generating code). Not scoped.

### 3. macOS Backend (project-index.md, Section 5)
Status: "🚧 Stub only"

If the sync happens, macOS will be even more broken (new APIs, no implementation). Is this acceptable? Not discussed in risk register.

---

## 8. Risk Register Gaps (overarching-plan.md, Section 6)

### Missing P0 Risk
The risk register lists "Breaking API change breaks build" as P0 with mitigation "Pre-sync API comparison, staged rollout."

But the resource view update isn't a "breaking API change" — it's an **architecture change**. Pre-sync comparison won't help. You need a migration strategy.

### Understated: gen-sokol.h Mismatch
Listed as "HIGH" probability but "CRITICAL" impact with mitigation "Static assertions, incremental update."

Static assertions catch size/alignment issues. They don't catch:
- Removed types (`sg_attachments`)
- Renamed fields in `sg_bindings`
- New types (`sg_view`)

---

## 9. Specific Line Reference Issues

| File | Section/Line | Issue |
|------|--------------|-------|
| overarching-plan.md | Section 1, "Breaking Changes Detected: 1" | Should be 5-6 per seeker |
| overarching-plan.md | Section 2.2, "Key Breaking Change" | Only shows `sg_apply_uniforms`, missing resource view |
| overarching-plan.md | Section 3, Phase 6 "0.5 day" | Should be 2-3 days minimum |
| overarching-plan.md | Section 7, "5 business days" | Should be 10-15 per seeker |
| overarching-plan.md | Section 8.1, "37h" | Should be 50-80h per seeker |
| project-index.md | Section 4, breaking changes table | Missing Aug/Sep/Dec 2025 changes |
| project-index.md | "Critical Metrics" box | "1 major breaking change" should be 5+ |

---

## 10. Recommendations

### Immediate Actions
1. **Update PM plan** to include all 5 breaking changes from seeker validation
2. **Add resource view migration phase** between Phase 3 and Phase 4 (~2-3 days)
3. **Revise timeline** to 12-15 business days
4. **Revise budget** to $10,000-$12,000

### Scope Decisions Required
1. **Resource view strategy:** Shim the old API or migrate to new API?
2. **gen-sokol rewrite:** Is Python acceptable or must it be C?
3. **macOS policy:** Accept increased breakage or defer sync?
4. **Shader pipeline:** Who handles shader recompilation?

### Tool Additions
1. Add migration tool for `sg_attachments` → `sg_view`
2. Add `sg_bindings` field migration detector
3. Extend `changelog-scan.c` to parse 2025 entries (not just 2024)

---

## Summary Table

| Area | PM Estimate | Seeker Finding | Gap | Critic Assessment |
|------|-------------|----------------|-----|-------------------|
| Breaking changes | 1 | 5-6 | **4-5 missed** | PM synthesis dropped seeker's findings |
| Timeline | 5 days | 10-15 days | **2-3x** | PM ignored explicit warning |
| Effort | 37 hours | 50-80 hours | **35-115%** | Resource view adds more |
| Budget | $5,354 | $7,500-$12,000 | **40-120%** | Should be ~$10k-$15k |
| Resource view | Not mentioned | "Fundamental API redesign" | **Unscoped** | Major risk |

---

**Verdict:** The PM synthesis is not ready for implementation. It cherry-picked the optimistic numbers from specialist reports while ignoring seeker's explicit warnings about scope, timeline, and the resource view update. The plan needs revision before specialist assignment begins.

---

*Critic validation complete. Returning to main agent.*
