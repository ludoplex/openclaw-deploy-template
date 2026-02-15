# Swiss Rounds — Round 2 Redundancy Check

**Project:** cosmo-sokol-update  
**Date:** 2026-02-09  
**Checker:** redundant-project-checker subagent

---

## Executive Summary

After cross-reading, specialists are **strongly converging** on core technical findings and recommendations. The Addendum 1 sections show healthy refinement of positions rather than fundamental disagreement. The few remaining disputes are around scope boundaries (cimgui, macOS documentation) and calibration (monitoring cadence) rather than architectural direction.

**Convergence Score:** 🟢 HIGH — Ready for final synthesis

---

## 1. Consensus Emerged (Strong Agreement)

### 1.1 Technical Foundation — Unanimous

| Finding | Seeker | Analyst | Ballistics | Cosmo |
|---------|:------:|:-------:|:----------:|:-----:|
| `gen-sokol` is the critical integration point | ✅ | ✅ | ✅ | ✅ |
| Nov 2024 bindings cleanup is the root blocker | ✅ | ✅ | ✅ | ✅ |
| ~30 function-level changes (not 1,000+ commits) | ✅ | ✅ | ✅ | ✅ |
| Two-stage extraction (automated + human review) | ✅ | ✅ | ✅ | ✅ |
| `_Static_assert` for ABI/struct size detection | ✅ | ✅ | ✅ | ✅ |
| Initial backlog effort: 22-34 hours | ✅ | ✅ revised | ✅ | ✅ |

All four specialists independently identified these same core findings and converged on identical conclusions after cross-reading.

### 1.2 Strategic Direction — Unanimous

| Recommendation | Seeker | Analyst | Ballistics | Cosmo |
|----------------|:------:|:-------:|:----------:|:-----:|
| Stay current vs pin versions | ✅ | ✅ | ✅ | ✅ |
| macOS as permanent stub (not blocked on implementation) | ✅ | ✅ | ✅ | ⚠️ soft |
| Quarterly sync cadence (post-backlog) | ✅ | ✅ | ⚠️ wants monthly monitoring | ✅ |
| Automation-assisted, not full automation | ✅ | ✅ revised | ✅ | ✅ |

### 1.3 Tooling Deliverables — Unanimous

All specialists explicitly endorsed the triad's proposed tooling:
- `scripts/extract_sokol_api.py` — Mechanical API extraction
- `scripts/diff_sokol_api.sh` — API delta measurement
- `sokol_abi_check.h` — Compile-time struct size assertions
- `versions.json` — Dependency version manifest

---

## 2. Disagreements Remaining (Unresolved)

### 2.1 cimgui Verification — LOW PRIORITY DISPUTE

**Position Split:**
- **Triad + Analyst:** "Stable enough to ignore"
- **Seeker:** "Deserves 1-2 hours of verification"
- **Ballistics:** "May be premature to dismiss"
- **Cosmo:** "Should track dependency chain explicitly"

**Nature:** This is a scope boundary dispute, not a technical disagreement. Everyone agrees cimgui is lower risk than sokol. The question is whether the 1.91→1.94 version gap warrants explicit verification.

**Resolution Path:** Include cimgui smoke test in phase 5 (1-2 hours). Low cost insurance.

### 2.2 macOS Documentation — PHILOSOPHICAL DISPUTE

**Position Split:**
- **Triad + Seeker + Analyst + Ballistics:** "Permanent stub with clear documentation"
- **Cosmo:** "Document the implementation path for future contributors; don't completely close the door"

**Nature:** Everyone agrees implementation is not in scope (2-4 person-months). The disagreement is whether the stub documentation should include a "future implementation guide" or simply say "not supported."

**Resolution Path:** Accept Cosmo's framing. The existing `sokol_macos.c` already documents three implementation options (objc_msgSend, native helper, alternative library). Keep this documentation but make runtime error messages unambiguous: "macOS GUI not supported."

### 2.3 Monitoring Cadence — CALIBRATION DISPUTE

**Position Split:**
- **Seeker + Analyst + Cosmo:** "Quarterly full sync"
- **Ballistics:** "Monthly monitoring with quarterly full-sync"

**Nature:** Ballistics argues that a December breaking change shouldn't wait until March to discover. The others implicitly assume changelog watching is continuous but formal work is quarterly.

**Resolution Path:** Accept Ballistics' refinement: monthly changelog review (~30 min), quarterly sync work (6-9 hours). These are compatible positions.

---

## 3. New Questions Raised

Cross-reading surfaced questions that weren't in the original reports:

### 3.1 Win32 Function Coverage (Seeker)
> "Has anyone verified which Win32 functions the latest sokol needs that aren't in Cosmopolitan 4.0.2's `master.sh`?"

**Status:** Unanswered. Could be a hidden blocker.  
**Recommended Action:** Add to task list before Phase 2 API update.

### 3.2 Baseline Struct Sizes for ABI Checks (Seeker)
> "Should we hardcode sizeof() from current build? Generate programmatically? Document platform variance?"

**Status:** Triad proposed mechanism but not implementation details.  
**Recommended Action:** Hardcode from current working build; document expected sizes per platform (x86/ARM).

### 3.3 Compile-time vs Runtime Breakage (Analyst → Seeker)
> "Are the removed `sapp_*_get_*` functions compile-time breakage (linker errors) or runtime (stubs that fail)?"

**Status:** Unanswered. Affects whether update can be incremental.  
**Recommended Action:** Verify before starting Phase 3 code migration.

### 3.4 macOS CI Strategy (Analyst → Ballistics)
> "Should macOS be dropped from CI entirely to avoid false confidence, or kept as compile-gate?"

**Status:** Not explicitly resolved.  
**Recommended Action:** Keep macOS in CI as compile-only verification. Catches header-level breaks without implying runtime functionality.

### 3.5 Vulkan Backend Relevance (Seeker + Cosmo)
> "Should cosmo-sokol track the new experimental Vulkan backend?"

**Status:** Consensus: Not initial scope.  
**Recommended Action:** Track for future; would require new shim work (vulkan loader dlopen).

### 3.6 FreeBSD/NetBSD Dispatch (Cosmo)
> "Cosmopolitan supports IsFreebsd(), IsOpenbsd(), IsNetbsd(). Should gen-sokol generate stubs?"

**Status:** Not addressed by others.  
**Recommended Action:** Out of scope for this update. Document as future enhancement.

### 3.7 Maintenance Ownership (Ballistics)
> "Who does this work? ludoplex? MHI? Community?"

**Status:** Not addressed.  
**Recommended Action:** Surface to main agent/user. This is a planning question, not a technical one.

---

## 4. Convergence Assessment

### 4.1 Are Specialists Converging or Diverging?

**🟢 STRONGLY CONVERGING**

Evidence:
1. **Analyst explicitly revised estimates** from "8-16 hours quarterly" to align with triad's 22-34 hours initial + 6-9 hours ongoing
2. **Analyst explicitly revised macOS recommendation** from "invest in completion" to accept permanent stub
3. **Analyst explicitly revised automation scope** from vague "create sync automation" to specific triad tooling
4. **Seeker synthesized all reports** into a unified task checklist matching triad's phases
5. **Ballistics' "disagreements"** are refinements (monthly monitoring) not contradictions
6. **Cosmo's "disagreements"** are scope additions (document macOS path) not alternatives

### 4.2 Quality of Cross-Reading

All four specialists demonstrated genuine engagement with other reports:
- **Seeker** noted specific line numbers from other reports (e.g., "triad estimates 22-34 hours")
- **Analyst** created a revised effort table explicitly showing "original vs revised"
- **Ballistics** asked targeted questions to specific specialists (e.g., "For Cosmo: Your file size summary shows sokol_macos.c at 23KB...")
- **Cosmo** created synthesis section showing how different reports combine

### 4.3 Gaps Filled by Cross-Reading

| Gap | Original Report | Filled By |
|-----|-----------------|-----------|
| Concrete effort estimates | Analyst (vague) | Triad + others |
| ABI break detection mechanism | Ballistics (identified gap) | Triad |
| macOS strategic decision | All (ambiguous) | Triad |
| Version intelligence details | Analyst (strategic level) | Seeker |
| Task breakdown structure | All (different formats) | Triad + Seeker synthesis |

---

## 5. Final Synthesis: Combined Findings

### 5.1 The Problem (Unanimous)
- cosmo-sokol is 1,032-1,044 commits behind upstream sokol
- The real delta is ~30 function-level API changes, not 1,000 commits
- Root cause: Nov 2024 bindings cleanup breaking change blocked further updates
- The `gen-sokol` script's hardcoded SOKOL_FUNCTIONS list is the critical sync point

### 5.2 The Solution (Unanimous)
1. **Tooling investment** before code changes
2. **Two-stage extraction**: automated parsing + human review
3. **Compile-time ABI checks** via `_Static_assert`
4. **macOS as permanent stub** with clear runtime errors
5. **Stay current** with quarterly sync cadence (+ monthly changelog review)

### 5.3 The Effort (Converged)

| Phase | Hours | Confidence |
|-------|-------|------------|
| 0. Documentation | 2 | High |
| 1. Tooling | 6-8 | High |
| 2. API Update | 4-6 | High |
| 3. Code Migration | 6-10 | Medium (bindings cleanup ripples) |
| 4. Build & Test | 4 | High |
| 5. cimgui Verification | 1-2 | High |
| 6. Review & Merge | 2 | High |
| **Total Initial** | **25-34h** | |
| **Quarterly Ongoing** | **6-9h** | |

### 5.4 Remaining Uncertainty
- Win32 function coverage verification (potential hidden blocker)
- Exact ripple effects of bindings cleanup on demo code
- Maintenance ownership question

---

## 6. Recommendation for Round 3

**Status: Ready for Final Synthesis**

The specialists have converged strongly. Remaining disagreements are:
- Minor scope decisions (cimgui verification, macOS docs detail level)
- Calibration refinements (monthly vs quarterly monitoring)

These don't require another round of debate. The triad's solution stands with minor refinements:
1. Include cimgui smoke test (Phase 5)
2. Keep macOS implementation guide in docs but make runtime errors clear
3. Add monthly changelog review to cadence

**Proceed to final deliverable synthesis.**

---

*Round 2 Redundancy Check Complete*
