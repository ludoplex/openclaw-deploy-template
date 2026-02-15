# Triad Phase 1: Redundancy Check — cosmo-sokol-v3

**Triad Role:** Redundancy Checker  
**Date:** 2026-02-09  
**Reports Analyzed:** 8 specialist reports  
**Goal:** Keep ludoplex/cosmo-sokol fork actively maintained and current with upstream

---

## Executive Summary

**Critical Finding:** Significant duplication across specialist proposals. 6 specialists proposed the same API extraction script independently. 4 proposed the same upstream sync workflow. 3 proposed different metadata manifest files.

| Issue Type | Count | Impact |
|------------|-------|--------|
| Duplicate scripts proposed | 6 (same script) | Wasted effort if all built |
| Duplicate workflows proposed | 4 (same workflow) | CI confusion, maintenance burden |
| Duplicate manifests proposed | 3 (different formats) | Inconsistent version tracking |
| Existing tools ignored | 2 major | Reinventing wheels |
| Scope creep items | 4 items | Distracts from goal |

---

## 1. EXISTING SOLUTIONS — Mature Tech Already Available

### 1.1 Dependabot for Submodule Tracking

**What specialists proposed:**
- **cicd:** Custom weekly cron job to check upstream drift
- **seeker:** Custom `upstream-check.yml` workflow
- **neteng:** Custom `sync-upstream.yml` workflow

**What already exists:**
```yaml
# .github/dependabot.yml - THIS ALREADY EXISTS AND WORKS
version: 2
updates:
  - package-ecosystem: "gitsubmodule"
    directory: "/"
    schedule:
      interval: "weekly"
```

**Reality:** GitHub Dependabot natively supports git submodule updates. The proposed custom cron jobs reinvent this wheel.

**Recommendation:** Use Dependabot for automatic submodule update PRs. Only add custom workflow for *blocking* on tests, not for detection.

---

### 1.2 Renovate for More Flexible Updates

**What specialists proposed:** Multiple custom scripts for version tracking and update detection.

**What already exists:** Renovate Bot supports:
- Git submodules
- Dockerfile base images
- GitHub Actions versions
- Arbitrary regex patterns for custom version files

**Recommendation:** If Dependabot's submodule support is insufficient, use Renovate. Don't build custom.

---

### 1.3 ABI Compliance Checker (libabigail)

**What specialists proposed:**
- **asm:** Static assertions for struct sizes
- **testcov:** `abi_check.py` to compare function signatures
- **cosmo:** `extract-sokol-api.py` for API extraction

**What already exists:**
- **abidiff** (libabigail) - Compares ABI between library versions
- **abi-compliance-checker** - More comprehensive ABI/API checking
- **c-ares** patterns - Used by many C projects

**Nuance:** For comparing a *hand-maintained function list* against headers, a simple script is appropriate. But for actual ABI verification (struct layouts, calling conventions), use libabigail.

**Recommendation:** 
- Keep ONE simple script for function list sync (consolidate the 6 proposals)
- Add `_Static_assert` for struct sizes (asm's proposal is correct)
- Don't reinvent ABI checking for the complex cases

---

### 1.4 GitHub Actions Pinning Tools

**What specialists proposed:**
- **neteng:** Manual SHA pinning of all actions
- **cicd:** Partial SHA pinning

**What already exists:**
- **step-security/harden-runner** - Automatic action hardening
- **pin-github-action** CLI tool - Automates SHA pinning
- **Dependabot** - Can update pinned SHAs automatically

**Recommendation:** Use `pin-github-action` or Renovate's `github-actions` manager. Don't manually maintain SHA pins.

---

## 2. REINVENTING WHEELS — Custom Scripts for Solved Problems

### 2.1 Six Specialists, One Script

**The duplication:**

| Specialist | Proposed Script | Purpose |
|------------|-----------------|---------|
| cosmo | `scripts/extract-sokol-api.py` | Extract API from headers |
| localsearch | `scripts/extract-sokol-api.py` | Extract API from headers |
| seeker | `scripts/extract-sokol-api.py` | Extract API from headers |
| testcov | `scripts/abi_check.py` | Compare API to gen-sokol |
| cicd | "API drift detection step" | Same comparison |
| neteng | `scripts/check-api-drift.py` | Same comparison |

**Problem:** 6 specialists independently proposed the same functionality. If each built their version, we'd have 6 scripts doing the same thing.

**Solution:** ONE script: `scripts/check-api-sync.py`
```
Extracts SOKOL_*_API_DECL from headers
Compares to SOKOL_FUNCTIONS in gen-sokol
Outputs delta
Returns exit code for CI
```

**Assignee:** testcov (most complete implementation)

---

### 2.2 Four Workflows, Same Purpose

**The duplication:**

| Specialist | Workflow Name | Purpose |
|------------|---------------|---------|
| cicd | `upstream-sync.yml` | Weekly upstream check |
| neteng | `sync-upstream.yml` | Weekly upstream check |
| seeker | `upstream-check.yml` | Weekly upstream check |
| testcov | `sync-check.yml` | Weekly upstream check |

**Problem:** 4 different workflow files doing the same thing with slightly different implementation details.

**Solution:** ONE workflow: `.github/workflows/upstream-sync.yml`

**Consolidate features from all:**
- Weekly cron + workflow_dispatch (all proposed)
- Check sokol submodule drift (all proposed)
- Check cimgui submodule drift (seeker)
- Check cosmocc version (cicd/cosmo)
- Create issue if drift > threshold (cicd/seeker)
- Run ABI check before PR (asm/testcov)

**Assignee:** cicd (most comprehensive)

---

### 2.3 Three Manifests, Same Data

**The duplication:**

| Specialist | File | Format |
|------------|------|--------|
| dbeng | `cosmo-sokol.json` | JSON with schema |
| localsearch | `version.yaml` | YAML |
| neteng | `version-manifest.json` | JSON |

**Problem:** 3 different files tracking the same information (component versions, platform status, dependencies).

**Solution:** ONE file: `cosmo-sokol.json` (dbeng's proposal)

**Rationale:**
- JSON is more portable (no YAML parser needed)
- dbeng's schema is most complete
- Can validate with JSON Schema in CI

**Migrate:**
- localsearch's `version.yaml` fields → merge into `cosmo-sokol.json`
- neteng's `version-manifest.json` → use dbeng's schema
- Generate during release, commit to repo

**Assignee:** dbeng

---

## 3. OVERLAPPING PROPOSALS — Consolidation Required

### 3.1 ABI/Static Assertions

**Proposals:**
- **asm:** `_Static_assert(sizeof(sg_buffer) == 4, ...)`
- **cicd:** Add to CI as pre-build gate
- **testcov:** Python script for signature comparison
- **cosmo:** Recommends same static assertions

**Consolidation:**
1. **asm** owns: Static assertions in C code (ABI stability)
2. **testcov** owns: Python script for API signature comparison
3. **cicd** owns: CI integration of both checks

**No overlap after consolidation.**

---

### 3.2 Platform Smoke Tests

**Proposals:**
- **testcov:** `test/smoke_test.c` with SOKOL_DUMMY_BACKEND
- **neteng:** Linux Xvfb smoke test, Wine Windows test
- **cicd:** Platform validation jobs

**Consolidation:**
1. **testcov** owns: Creating the smoke test binary
2. **neteng** owns: Platform-specific execution wrappers
3. **cicd** owns: Matrix job configuration

**Dependency:** testcov must add `--headless` flag before neteng can run platform tests.

---

### 3.3 macOS Implementation Strategy

**Proposals:**
- **cosmo:** `objc_bridge.c/h` for Objective-C runtime
- **asm:** objc_msgSend ABI analysis

**Consolidation:** Both are complementary, not overlapping.
- **cosmo** owns: Implementation
- **asm** owns: ABI verification

**Note:** Full macOS implementation may be scope creep (see Section 4).

---

### 3.4 Release Artifact Generation

**Proposals:**
- **neteng:** SHA256SUMS, version-manifest.json, SBOM
- **dbeng:** cosmo-sokol.json with CI provenance
- **cicd:** Auto-tag releases

**Consolidation:**
1. **dbeng** owns: cosmo-sokol.json schema and generation
2. **neteng** owns: SHA256SUMS, binary packaging
3. **cicd** owns: Release workflow that calls both

---

## 4. SCOPE CREEP — Beyond the Goal

The goal is: **"Keep ludoplex/cosmo-sokol fork actively maintained and current with upstream"**

### 4.1 Vulkan Backend — OUT OF SCOPE

**Who proposed:** seeker (Phase 3), asm (mentioned)

**Why it's scope creep:** 
- Adding a new backend is *new development*, not maintenance
- Upstream has experimental Vulkan; fork can inherit when ready
- Requires significant effort (dlopen shims for vulkan-loader)

**Recommendation:** Remove from proposals. Track upstream's Vulkan stabilization instead.

---

### 4.2 Full macOS Implementation — OUT OF SCOPE (for now)

**Who proposed:** cosmo, asm

**Why it's scope creep:**
- Current stub works (builds, fails gracefully at runtime)
- Full implementation requires objc_msgSend, Metal/OpenGL
- Upstream doesn't require macOS for the fork to be "maintained"

**Recommendation:** 
- Keep macOS stub functional
- Mark as separate epic, not part of sync maintenance
- Only pursue if explicitly requested by stakeholders

---

### 4.3 SBOM Generation — OUT OF SCOPE

**Who proposed:** neteng (Priority P2)

**Why it's scope creep:**
- Not required for maintenance goal
- Nice for compliance but adds complexity
- Can be added later if needed

**Recommendation:** Remove from initial scope. Add if compliance requirements emerge.

---

### 4.4 Visual Regression Testing — OUT OF SCOPE

**Who proposed:** testcov (correctly marked P3/optional)

**Why it's scope creep:**
- Requires GPU, screenshots, comparison infrastructure
- Overkill for maintaining API compatibility

**Recommendation:** testcov correctly deprioritized this. Keep out of scope.

---

## 5. Consolidated Work Item List

After eliminating redundancy and scope creep:

### Phase 1: Foundation (Week 1)

| ID | Task | Owner | Deliverable |
|----|------|-------|-------------|
| F1 | Configure Dependabot for submodules | cicd | `.github/dependabot.yml` |
| F2 | Add static assertions | asm | In `sokol_cosmo.c` |
| F3 | Create API sync check script | testcov | `scripts/check-api-sync.py` |
| F4 | Create cosmo-sokol.json | dbeng | `cosmo-sokol.json` + schema |
| F5 | Pin GitHub Actions | neteng | Updated `build.yml` |

### Phase 2: CI/CD (Week 2)

| ID | Task | Owner | Deliverable |
|----|------|-------|-------------|
| C1 | Create unified upstream-sync workflow | cicd | `.github/workflows/upstream-sync.yml` |
| C2 | Add headless flag to main.c | testcov | Modified `main.c` |
| C3 | Add smoke test | testcov | `test/smoke_test.c` |
| C4 | Add platform test matrix | cicd + neteng | Updated CI jobs |
| C5 | Add SHA256SUMS to releases | neteng | Release job modification |

### Phase 3: Automation (Week 3)

| ID | Task | Owner | Deliverable |
|----|------|-------|-------------|
| A1 | Enable auto-PR for submodule updates | cicd | Dependabot + test gates |
| A2 | Add cosmocc version matrix | cicd | Matrix in build.yml |
| A3 | Create sync documentation | seeker | `SYNC.md` |

---

## 6. Eliminated Items

These items should be **removed** from specialist proposals:

| Item | Original Owner | Reason |
|------|----------------|--------|
| Custom upstream detection cron | all | Use Dependabot |
| version.yaml | localsearch | Use cosmo-sokol.json |
| version-manifest.json | neteng | Use cosmo-sokol.json |
| Multiple API extraction scripts | 6 specialists | One script (testcov) |
| Multiple sync workflows | 4 specialists | One workflow (cicd) |
| Vulkan backend | seeker, asm | Scope creep |
| Full macOS implementation | cosmo | Scope creep (separate epic) |
| SBOM generation | neteng | Scope creep |
| Visual regression testing | testcov | Scope creep |

---

## 7. Cross-Cutting Recommendations

### 7.1 Use Existing Tools First

Before writing custom scripts, check:
1. Does Dependabot/Renovate do this?
2. Does a GitHub Action exist?
3. Does an established open-source tool exist?

### 7.2 Single Source of Truth

- **One** metadata file: `cosmo-sokol.json`
- **One** upstream sync workflow
- **One** API checking script
- **One** version tracking mechanism (submodule commits + manifest)

### 7.3 Defense Against Future Redundancy

Add to `CONTRIBUTING.md`:
```markdown
Before proposing new CI/tooling:
1. Check existing workflows in `.github/workflows/`
2. Check existing scripts in `scripts/`
3. Check if Dependabot/Renovate can do it
4. Discuss in issue before implementing
```

---

## Summary

**Redundancy eliminated:** 15+ duplicate items consolidated to 5 core deliverables
**Scope creep removed:** 4 items deferred or eliminated
**Existing tools adopted:** Dependabot, Renovate, step-security/harden-runner

The 8 specialists identified real problems. The issue is they solved the same problems independently. With consolidation, the actual work is ~40% of what was proposed.

---

*Triad Redundancy Check Complete*  
*Phase 2 (Feasibility) and Phase 3 (Integration) should validate this consolidation*
