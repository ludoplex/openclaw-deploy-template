# Triad Phase 1: Redundancy Check — cosmo-sokol-v3

**Analyst:** Redundancy Checker  
**Date:** 2026-02-09  
**Round:** 1 (Post-Specialist Analysis)  
**Goal:** Keep ludoplex/cosmo-sokol fork updated with upstream without manual version pinning

---

## Executive Summary

After reviewing all 8 specialist reports, I found **significant overlap** in proposed solutions, **2 direct conflicts**, and **notable scope creep**. The redundancy is actually a good sign—it shows consensus on the core problems—but consolidation is needed to avoid wasted effort.

| Finding | Count | Severity |
|---------|-------|----------|
| Overlapping Proposals | 6 major areas | High |
| Direct Conflicts | 2 | Medium |
| Existing Solutions Ignored | 3 | Low |
| Scope Creep Items | 5 | Medium |

---

## 1. Overlapping Proposals (Consolidation Needed)

### 1.1 API Drift Detection Scripts — 6 SPECIALISTS PROPOSING THE SAME THING

**The Problem:** How to detect when upstream sokol adds/removes/changes API functions that require `gen-sokol` updates.

| Specialist | Proposal | Implementation Level |
|------------|----------|---------------------|
| **seeker** | "CHANGELOG parsing for breaking changes" | Concept |
| **localsearch** | Regex pattern `SOKOL_(?:APP\|GFX)_API_DECL` | Partial code |
| **asm** | "Parse sokol headers for SOKOL_GFX_API_DECL functions" | Concept |
| **cosmo** | `scripts/extract-sokol-api.py` with same regex | Full code |
| **neteng** | `scripts/check-sokol-api.py` | Full implementation |
| **testcov** | `abi_check.py` | Full implementation |

**Verdict:** Three full implementations exist (cosmo, neteng, testcov). **Merge into ONE script.**

**Recommended Owner:** neteng's implementation is most complete but should incorporate testcov's normalization logic.

---

### 1.2 GitHub Actions Sync Workflow — 6 SPECIALISTS PROPOSING WORKFLOWS

| Specialist | Workflow | Trigger | Creates PR? |
|------------|----------|---------|-------------|
| **seeker** | Concept workflow | Weekly (`0 0 * * 0`) | Yes |
| **cosmo** | "Proposed CI/CD Pipeline" | Weekly | Detection only |
| **dbeng** | Flow diagram | N/A | N/A |
| **neteng** | `sync-upstream.yml` | Weekly (`0 0 * * 0`) | Yes |
| **cicd** | `sync-upstream.yml` + `update-sokol.yml` + `check-cosmocc.yml` | Mixed | Yes |
| **testcov** | `sync-upstream.yml` | Weekly (`0 6 * * 1`) | Yes |

**Verdict:** cicd provides the most comprehensive separation of concerns (3 distinct workflows). **Use cicd's structure** but incorporate neteng's security hardening.

**Recommended Owner:** cicd (with neteng security review)

---

### 1.3 Version Manifest Files — 3 SPECIALISTS PROPOSING

| Specialist | Filename | Format | Complexity |
|------------|----------|--------|------------|
| **localsearch** | `version.yaml` | YAML | Simple |
| **dbeng** | `version-manifest.json` | JSON + JSON Schema | Complex |
| **neteng** | `VERSIONS.json` | JSON | Medium |

**Verdict:** dbeng's schema is over-engineered for this project's scale. **Use neteng's simpler `VERSIONS.json`** with localsearch's simplicity.

**Recommended Owner:** neteng

---

### 1.4 Smoke Tests / Headless Testing — 2 SPECIALISTS

| Specialist | Proposal |
|------------|----------|
| **neteng** | Xvfb + `timeout 5 ./bin/cosmo-sokol --headless` |
| **testcov** | Add `--headless` flag to main.c + test runner |

**Verdict:** Aligned but incomplete without each other. **testcov owns main.c changes, neteng owns CI integration.**

---

### 1.5 Breaking Changes Documentation — 2 SPECIALISTS

| Specialist | Identified Change |
|------------|------------------|
| **seeker** | Nov 2024: `sg_apply_uniforms` change, `sg_bindings` restructure |
| **dbeng** | Nov 7, 2024: "Bindings Cleanup Update" |

**Verdict:** Same breaking change identified independently. **Good validation.** Merge into single `MIGRATION.md`.

---

### 1.6 Struct Size Assertions — 1 SPECIALIST (asm)

**asm** uniquely proposes:
```c
_Static_assert(sizeof(sg_buffer) == 4, "sg_buffer size mismatch");
_Static_assert(sizeof(sg_range) == 16, "sg_range size mismatch");
```

**Verdict:** Valuable unique contribution. **Keep in final plan.**

---

## 2. Direct Conflicts

### 2.1 Sync Frequency: Daily vs Weekly

| Specialist | Sokol Sync Frequency | Rationale |
|------------|---------------------|-----------|
| **cicd** | Daily (`0 7 * * *`) | "Active development, frequent commits" |
| **neteng** | Weekly (`0 0 * * 0`) | Less aggressive |
| **testcov** | Weekly (`0 6 * * 1`) | Standard cadence |
| **seeker** | Weekly | Implicit |

**Conflict:** cicd recommends daily; others recommend weekly.

**Resolution:** **Weekly is sufficient.** Sokol's breaking changes are rare (1-2 per quarter). Daily creates noise. The Nov 2024 breaking change was 11 months ago, and the fork is still functional. cicd's "Daily seems aggressive" self-note in their own report suggests even they're uncertain.

**Winner:** Weekly sync (neteng/testcov position)

---

### 2.2 GitHub Action Pinning: SHA vs Version Tags

| Specialist | Approach | Example |
|------------|----------|---------|
| **cicd** | Version tags | `uses: actions/checkout@v4` |
| **neteng** | SHA hashes | `uses: actions/checkout@8ade135a41bc03ea155e62e844d188df1ea18608` |

**Conflict:** Security vs. maintainability trade-off.

**Resolution:** **Use SHA pins for third-party actions, version tags for GitHub official actions.**

```yaml
# Official actions - version tags OK
uses: actions/checkout@v4
uses: actions/upload-artifact@v4

# Third-party - SHA required
uses: peter-evans/create-pull-request@c5a7806660adcd6...
uses: bjia56/setup-cosmocc@e506d091f30f39b...
```

**Winner:** Compromise (both approaches valid for different action types)

---

## 3. Existing Solutions Being Ignored

### 3.1 Upstream Remote Already Configured

**localsearch** discovered:
```
Remote: upstream → https://github.com/bullno1/cosmo-sokol
```

**Implication:** The fork already has basic sync infrastructure. Specialists didn't need to explain "how to add upstream remote" — it exists.

---

### 3.2 gen-sokol Already Has Function List

The `SOKOL_FUNCTIONS` list in `gen-sokol` already exists with 189 functions. The proposal is to *automate* populating this list, not create it from scratch.

---

### 3.3 Build Workflow Already Exists

`.github/workflows/build.yml` exists. Enhancements should modify it, not replace it entirely.

---

## 4. Scope Creep Analysis

### 4.1 macOS objc_msgSend Implementation 🔴 OUT OF SCOPE

| Specialist | Proposal |
|------------|----------|
| **seeker** | "Complete macOS objc_msgSend implementation" |
| **cosmo** | Detailed objc_msgSend patterns for Cocoa |
| **asm** | macOS Cocoa struct packing (`NSPoint`, `NSRect`) |

**Why it's scope creep:** The goal is "keep fork updated with upstream" — not "implement new features." macOS is currently a stub that compiles but doesn't run. Completing it is a separate project.

**Verdict:** Move to separate epic/milestone. Do not block sync automation on this.

---

### 4.2 SBOM and GPG Signing 🟡 NICE-TO-HAVE

**neteng** proposes:
- CycloneDX SBOM generation
- GPG signing of releases

**Why it's scope creep:** Compliance features beyond basic sync automation.

**Verdict:** Phase 2 enhancement. Not required for initial sync automation.

---

### 4.3 SQLite Database for Version Tracking 🔴 OVER-ENGINEERED

**dbeng** proposes full relational schema:
```sql
CREATE TABLE repositories (...);
CREATE TABLE commits (...);
CREATE TABLE sync_events (...);
CREATE TABLE breaking_changes (...);
```

**Why it's scope creep:** This is a 2-person fork, not a large project. A single JSON file suffices.

**Verdict:** Reject. Use flat file (`VERSIONS.json`) instead.

---

### 4.4 Vulkan Backend Evaluation 🔴 OUT OF SCOPE

**seeker:** "Evaluate Vulkan backend feasibility for Cosmopolitan"

**Why it's scope creep:** New backend development, not sync automation.

**Verdict:** Separate future initiative.

---

### 4.5 Metal Support Path 🔴 OUT OF SCOPE

**cosmo:** "Explore Metal support path for macOS"

**Why it's scope creep:** Same as macOS objc_msgSend — new feature development.

**Verdict:** Separate future initiative.

---

## 5. Recommended Consolidation

### Phase 1: Core Sync Automation (Keep)

| Deliverable | Owner | Source |
|-------------|-------|--------|
| `scripts/check-sokol-api.py` | neteng+testcov (merge) | neteng's structure + testcov's normalization |
| `.github/workflows/update-sokol.yml` | cicd | cicd's implementation |
| `.github/workflows/sync-upstream.yml` | cicd | cicd's implementation |
| `.github/workflows/check-cosmocc.yml` | cicd | cicd's implementation |
| `VERSIONS.json` | neteng | neteng's schema |
| `SHA256SUMS` generation | neteng | neteng's proposal |
| Struct size assertions | asm | asm's proposal |

### Phase 2: Verification (Keep)

| Deliverable | Owner | Source |
|-------------|-------|--------|
| `--headless` flag in main.c | testcov | testcov's proposal |
| Xvfb smoke test in CI | neteng | neteng's proposal |
| Platform test matrix | cicd | cicd's proposal |

### Phase 3: Nice-to-Have (Defer)

| Deliverable | Priority | Notes |
|-------------|----------|-------|
| SBOM generation | Low | Compliance, not core |
| GPG signing | Low | Security hardening |
| Full platform matrix (macOS) | Medium | Blocked on stub completion |

### Rejected / Out of Scope

| Proposal | Specialist | Reason |
|----------|------------|--------|
| SQLite version database | dbeng | Over-engineered |
| macOS objc_msgSend completion | seeker/cosmo/asm | Separate feature project |
| Vulkan backend evaluation | seeker | Separate initiative |
| Metal support exploration | cosmo | Separate initiative |

---

## 6. Questions for Round 2 Discussion

1. **API Script Merge:** Who leads the merge of neteng + testcov API scripts?

2. **Weekly vs Daily:** cicd proposed daily for sokol. Confirm weekly is acceptable?

3. **Action Pinning Policy:** Confirm the hybrid approach (SHA for third-party, version for official)?

4. **macOS Scope:** Confirm macOS completion is OUT OF SCOPE for this initiative?

5. **Breaking Change Handling:** The Nov 2024 breaking change requires migration. Should we:
   - a) Update to pre-breaking-change commit first, then separately migrate?
   - b) Jump straight to latest and handle migration in one PR?

---

## 7. Specialist Feedback Quality

| Specialist | Unique Value | Overlap Level | Scope Discipline |
|------------|--------------|---------------|------------------|
| **seeker** | Breaking change documentation | Medium | ⚠️ macOS creep |
| **localsearch** | File inventory, existing state | Low | ✅ Focused |
| **asm** | ABI safety assertions | Low (unique) | ✅ Focused |
| **cosmo** | Cosmopolitan API expertise | High | ⚠️ macOS creep |
| **dbeng** | Version tracking schemas | Medium | ⚠️ Over-engineered |
| **neteng** | Full implementations, security | High | ✅ Focused |
| **cicd** | Workflow structure | High | ✅ Focused |
| **testcov** | Test gap analysis | Medium | ✅ Focused |

---

## Summary

**Good news:** Strong consensus on core approach (API detection, weekly sync, PR automation).

**Action needed:** Consolidate 6 overlapping API scripts into 1, adopt cicd's workflow structure with neteng's security practices, reject SQLite and macOS scope creep.

**Primary risk:** The 1,032-commit gap with a breaking change in the middle. Recommend two-phase update: first to pre-Nov-2024, then to latest.

---

*Report generated by Triad Redundancy Checker — Swiss Rounds v3 Round 1*
