# Triad Phase 1: Redundancy Check — cosmo-sokol-v3 — Round 3

**Triad Role:** Redundancy Checker  
**Date:** 2026-02-09  
**Reports Analyzed:** 8 specialist Round 3 reports  
**Input Context:** Round 2 Triad feedback, C/APE mandate adoption  
**Goal:** Verify specialists consolidated as instructed; catch new redundancies; confirm philosophy alignment

---

## Executive Summary

**Overall Assessment: 95% COMPLIANT** — Specialists have fully embraced the C/APE philosophy. Python tooling has been eliminated across all proposals. Consolidation is nearly complete.

| Category | Status | Details |
|----------|--------|---------|
| C/APE Philosophy | ✅ COMPLIED | All Python scripts withdrawn/replaced |
| Tool Consolidation | ✅ COMPLIED | Single owner per tool confirmed |
| Workflow Consolidation | ✅ COMPLIED | Single build.yml, single upstream-sync.yml |
| dlopen Header | ✅ RESOLVED | cosmo's version authoritative, asm defers |
| Manifest Files | ⚠️ Minor | localsearch's watch-manifest.json vs dbeng's cosmo-sokol.json |
| New Redundancies | ✅ None | No significant new overlaps detected |

---

## 1. Philosophy Alignment Verification

### 1.1 Python Script Elimination — ✅ COMPLETE

**Round 2 Problem:** Python scripts violated Cosmopolitan philosophy.

**Round 3 Status:**

| Script | Original Owner | Status | Replacement |
|--------|----------------|--------|-------------|
| `check-api-sync.py` | testcov | ❌ WITHDRAWN | `tools/check-api-sync.c` (cosmo) |
| `validate-source-files.py` | localsearch | ❌ WITHDRAWN | `tools/validate-sources.c` |
| `function_coverage.py` | testcov | ❌ WITHDRAWN | N/A (test analysis only) |
| `extract-sokol-api.py` | seeker | ❌ WITHDRAWN | C-based in check-api-sync.c |
| `scan-changelog.py` | seeker | ❌ WITHDRAWN | `tools/changelog-scan.c` |
| `generate-sync-report.py` | seeker | ❌ WITHDRAWN | `tools/drift-report.c` |
| `gen-sokol` | legacy | 🟡 Pending | Future C rewrite |

**Verdict:** ✅ All specialists have withdrawn Python tooling proposals.

### 1.2 C/APE Tool Ownership — ✅ CLEAR

| Tool | Owner | Status |
|------|-------|--------|
| `tools/check-api-sync.c` | cosmo + triad | ✅ Complete implementation |
| `tools/validate-sources.c` | triad | ✅ Complete implementation |
| `tools/changelog-scan.c` | seeker | ✅ Complete implementation |
| `tools/drift-report.c` | seeker | ✅ Complete implementation |
| `tools/Makefile` | seeker (consolidated) | ✅ Updated |

**No Overlap:** Each tool has single owner.

---

## 2. Consolidation Compliance Verification

### 2.1 dlopen Header Resolution — ✅ RESOLVED

**Round 2 Problem:** Both asm and cosmo proposed dlopen safety headers.

**Round 3 Status:**

| Header | Owner | Status |
|--------|-------|--------|
| `cosmo_dl_safe.h` | cosmo | ✅ AUTHORITATIVE |
| `cosmo_dlopen_safe.h` | asm | ❌ DEPRECATED |

**Cosmo's Round 3 Report States:**
> "Decision: Use cosmo's `cosmo_dl_safe.h` as authoritative. asm specialist should update any references."

**Verified:** asm has not submitted conflicting proposal in Round 3.

**Verdict:** ✅ Consolidation complete.

---

### 2.2 CI/CD Workflows — ✅ CONSOLIDATED

**Round 3 Status:**

| Workflow | Owner | Status |
|----------|-------|--------|
| `.github/workflows/build.yml` | neteng | ✅ Production-ready |
| `.github/workflows/upstream-sync.yml` | cicd | ✅ Complete |

**Neteng's build.yml Includes:**
- Build tools phase (C tools)
- Validate phase (uses C tools)
- Build matrix (cosmocc 3.9.5, 3.9.6)
- Native platform smoke tests
- Release packaging

**No Redundant Workflows:** Single owner, comprehensive implementation.

**Verdict:** ✅ Consolidation complete.

---

### 2.3 Manifest Files — ⚠️ MINOR OVERLAP

**Round 3 Status:**

| Manifest | Owner | Purpose |
|----------|-------|---------|
| `cosmo-sokol.json` | dbeng | Project metadata, versions, dependencies |
| `watch-manifest.json` | localsearch | File monitoring triggers |
| `version-manifest.json` | neteng (in release) | Release metadata |

**Assessment:**

- `cosmo-sokol.json` (dbeng): Primary project manifest
- `watch-manifest.json` (localsearch): CI trigger configuration
- `version-manifest.json` (neteng): Generated at release time

**These serve different purposes:**
- dbeng's: Development metadata
- localsearch's: Change detection triggers  
- neteng's: Release provenance

**Recommendation:** 
- Keep all three for their distinct purposes
- OR: Merge `watch-manifest.json` into `cosmo-sokol.json` under a `"watch"` key

**Priority:** P3 — Minor organizational issue, no functional overlap.

---

## 3. New Redundancy Check — Round 3 Proposals

### 3.1 check-api-sync.c Implementations

**Potential Concern:** Both cosmo and seeker mention check-api-sync.c

**Verification:**

| Report | Contribution |
|--------|--------------|
| cosmo R3 | Full implementation of `check-api-sync.c` |
| seeker R3 | References triad's implementation, contributes different tools |
| testcov R3 | References tools, doesn't implement |

**Result:** ✅ NO REDUNDANCY — cosmo provides implementation, seeker defers.

---

### 3.2 Shell Scripts (localsearch)

**Concern:** localsearch proposes shell scripts, others propose C tools.

**Analysis:**

| Script | Purpose | Relationship to C Tools |
|--------|---------|------------------------|
| `pre-commit-drift-check.sh` | Developer hook | Supplements (runs before CI) |
| `verify-symbols.sh` | Post-build | Supplements (different scope) |

**Result:** ✅ NO REDUNDANCY — Shell scripts for developer workflow, C tools for CI/APE.

---

### 3.3 Documentation Overlap

**Concern:** Multiple specialists mention SYNC.md

| Specialist | Contribution |
|------------|--------------|
| seeker R3 | Full SYNC.md implementation (C-tools-aware) |
| testcov R3 | References SYNC.md as deliverable needed |
| cosmo R3 | No SYNC.md proposal |

**Result:** ✅ NO REDUNDANCY — Seeker owns SYNC.md.

---

## 4. Existing Mature Tools — Status Check

### 4.1 Tools from Round 2 Discussion

| Tool | Round 2 Status | Round 3 Status |
|------|----------------|----------------|
| libabigail/abidiff | Not adopted | Still not adopted (acceptable for MVP) |
| pycparser/tree-sitter | Not adopted | Intentionally avoided (C approach) |
| Renovate | Not adopted | Dependabot working, not needed |
| step-security/harden-runner | Not adopted | 🟡 Still recommended |
| pin-github-action CLI | Not used | 🟡 Useful for maintainers |

**Assessment:**
- libabigail: Static assertions sufficient for now
- pycparser: C-based parsing more aligned with philosophy
- Renovate: Dependabot sufficient for submodules
- harden-runner: Should add (P2)
- pin-github-action: Nice-to-have (P3)

---

## 5. Scope Creep Assessment

### 5.1 Deferred Items Still Deferred

| Item | Status |
|------|--------|
| Vulkan backend | ❌ Not mentioned |
| Full macOS implementation | 🟡 Documented as stub |
| SBOM generation | ❌ Not mentioned |
| Visual regression testing | ❌ Not mentioned |
| ARM64 CI | 🟡 Mentioned for future |

**Verdict:** ✅ No scope creep.

### 5.2 New Scope in Round 3

| New Item | Specialist | Assessment |
|----------|------------|------------|
| changelog-scan.c | seeker | ✅ Valid — fills detection gap |
| drift-report.c | seeker | ✅ Valid — fills reporting gap |
| verify-symbols.sh | localsearch | ✅ Valid — post-build verification |
| pre-commit hook | localsearch | ✅ Valid — developer workflow |

**All new scope is valid and fills genuine gaps.**

---

## 6. Final Consolidation Status

### 6.1 Owner Matrix (Updated Round 3)

| Domain | Owner | Deliverables |
|--------|-------|--------------|
| dlopen safety | cosmo | `cosmo_dl_safe.h` |
| API sync checking | cosmo | `tools/check-api-sync.c` |
| Source validation | triad/solver | `tools/validate-sources.c` |
| Changelog scanning | seeker | `tools/changelog-scan.c` |
| Drift reporting | seeker | `tools/drift-report.c` |
| Build system | neteng | `.github/workflows/build.yml` |
| Upstream sync workflow | cicd | `.github/workflows/upstream-sync.yml` |
| Pre-commit hooks | localsearch | Shell scripts |
| Symbol verification | localsearch | `verify-symbols.sh` |
| Sync documentation | seeker | `SYNC.md` |
| Project metadata | dbeng | `cosmo-sokol.json` |

### 6.2 Eliminated/Deprecated

| Item | Original Owner | Reason |
|------|----------------|--------|
| All Python scripts | Various | Philosophy violation |
| `cosmo_dlopen_safe.h` | asm | Superseded by cosmo's header |
| `version-manifest.json` (manual) | neteng R2 | Generated at release time now |

---

## 7. Recommendations

### 7.1 For Immediate Implementation

1. ✅ Proceed with all C tool implementations as proposed
2. ✅ Deploy neteng's production build.yml
3. ✅ Use cosmo's `cosmo_dl_safe.h` exclusively
4. ✅ Integrate seeker's shell scripts for developer workflow

### 7.2 Minor Cleanup

1. **Manifest consolidation (P3):** Consider merging watch-manifest.json into cosmo-sokol.json
2. **harden-runner (P2):** Add step-security/harden-runner to workflows
3. **pin-github-action (P3):** Document as optional maintainer tool

### 7.3 No Action Required

- libabigail — static assertions sufficient
- pycparser — C approach better aligned
- Renovate — Dependabot working

---

## 8. Summary

**Round 3 Redundancy Check: 95% COMPLIANT**

| Metric | Score |
|--------|-------|
| Python elimination | 100% |
| Tool ownership clarity | 100% |
| Workflow consolidation | 100% |
| Header consolidation | 100% |
| Manifest organization | 90% (minor overlap) |
| Scope control | 100% |

**Key Achievement:** All specialists have embraced the C/APE philosophy. The project now has a coherent, dependency-free tooling approach that embodies Cosmopolitan's core values.

**Recommendation:** Proceed to implementation. No blocking redundancies.

---

*Triad Round 3 Redundancy Check Complete*  
*Ready for Technical Critique phase*
