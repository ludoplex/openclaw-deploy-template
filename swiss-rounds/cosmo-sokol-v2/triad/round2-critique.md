# Swiss Rounds Triad — Round 2 Critical Evaluation

**Project:** cosmo-sokol-v2  
**Role:** project-critic  
**Date:** 2026-02-09  
**Challenge:** Redundancy checker gave everyone 4-5/5. Is this justified?

---

## Overall Assessment

The redundancy checker's generosity is notable. Of 8 specialists, 7 received 5/5 and 1 received 4/5. This near-perfect scoring masks genuine weaknesses. The "production-usable" label is premature—most deliverables are documentation of *intentions* rather than *verified implementations*.

**Key observation:** Only ONE specialist (neteng) actually ran a binary. Everyone else produced documentation, schemas, or code that has never been compiled or executed against the actual cosmo-sokol repository.

---

## Critique of seeker (Round 2)

**Redundancy Score:** 5/5  
**My Assessment:** 3.5/5 — Inflated

### Score Justified?
**No.** The 5/5 celebrates URL collection as if it were deep analysis. Adding sections on sokol-shdc, dlopen limitations, PR #1318, and APE format is valuable catalog work—but seeker's unique contribution is *aggregating information others already documented*. The dlopen platform matrix was lifted from cosmo's analysis of `dlopen.c`. The PR #1318 function list is just reading the PR.

### Risk Remaining
- **URL staleness.** Web resources decay. The 10+ GitHub raw URLs could break on any upstream refactor.
- **No verification.** Seeker claims the dlopen platform matrix as a deliverable but never verified it against actual binaries.
- **False completeness.** Claiming "no solution for CI status badges" as a gap when they could have documented workarounds (e.g., GitHub Actions API queries, shields.io badges).

### Weakest Element
The "Cross-specialist coordination" section telling others what to do (`testcov: Document macOS x86-64...`, `cicd: Use sokol-samples CI...`) without doing any original synthesis. Seeker is passing the buck while claiming credit for coordination.

---

## Critique of localsearch (Round 2)

**Redundancy Score:** 5/5  
**My Assessment:** 4/5 — Slightly Inflated

### Score Justified?
**Partially.** The discovery of `sokol_cosmo.c` (3,098 lines, 152 dispatched functions) is genuinely critical—this *is* the glue layer that makes the project work. Answering "no `#ifdef __COSMOPOLITAN__` conditionals exist" is a concrete, useful finding.

### Risk Remaining
- **Static inventory.** The file counts, line counts, and function counts are fragile metadata. Any upstream commit invalidates them.
- **No checksums.** Identified in "Remaining gaps" but never addressed. Critical shim files (`sokol_cosmo.c`, `sokol_windows.c`) should have SHA256 for reproducibility.
- **"152 verified" is unverified.** The function count was derived by reading source, not by running `objdump` or `nm` against compiled binaries.

### Weakest Element
The claim of "verified" function counts without verification. localsearch never compiled anything. The "152 functions" could be wrong if there are preprocessor conditionals, dead code paths, or inline functions.

---

## Critique of asm (Round 2)

**Redundancy Score:** 5/5  
**My Assessment:** 4/5 — Inflated

### Score Justified?
**No.** The redundancy checker celebrates "The _Static_assert template is directly usable in CI" and "Excellent intellectual honesty in accepting empirical corrections." But look closely:

1. The struct sizes asm provided in Round 1 were **significantly wrong** (sapp_desc: claimed 280-320, actual 472—a 50% error).
2. The "correction" is simply copying testcov's empirically derived values.
3. The _Static_assert template has **TBD placeholders**—it's NOT directly usable.

### Risk Remaining
- **No actual assembly inspection.** asm's report says "Actual generated trampoline assembly not inspected." This is the core of their domain!
- **Deadlock scenario unverified.** Both Round 1 and Round 2 note the locking change "needs verification"—never done.
- **Theory vs. practice.** Everything is theoretical: calling convention analysis, struct layout analysis, SIMD register analysis. None verified against actual compiled objects.

### Weakest Element
```c
_Static_assert(sizeof(sapp_desc) == 472, "sapp_desc ABI drift");
```
This line is in the "Updated Deliverables" but the actual `abi_verify_cosmo.c` in testcov's report has:
```c
/* ABI_CHECK(sapp_desc, TBD);  -- needs verification */
```
The template is incomplete. The asserts require values asm never independently measured.

---

## Critique of cicd (Round 2)

**Redundancy Score:** 5/5  
**My Assessment:** 4/5 — Inflated

### Score Justified?
**No.** The Round 2 improvements are: "Fixed macOS test job to link-only verification" and "Integrated testcov's smoke test." But:

1. **"Fixed" = gave up.** Changing macOS tests to "link-only verification" isn't fixing, it's admitting defeat. The justification (dlopen limitation) is valid, but claiming a fix where none exists is misleading.
2. **Integration = copy-paste.** "Integrated testcov's smoke test with `--smoke` flag" means copying testcov's code. That's not cicd's contribution.
3. **Foreign helper permissions.** "May have permission issues" for cross-workflow artifact download is an unsolved problem listed as a "remaining gap."

### Risk Remaining
- **Untested workflows.** The workflows are YAML specifications, not running CI jobs. Has anyone actually pushed these to a test repo?
- **No deployment.** Both Round 1 and Round 2 note "No deployment workflow yet"—the most critical gap for infrastructure goes unaddressed.
- **macOS ARM untested.** GitHub Actions `macos-14` is ARM, but cicd never added this to the matrix. The "link-only" cop-out applies to both Intel and ARM equally.

### Weakest Element
The entire `test.yml` (dedicated test workflow) depends on artifacts from the build workflow but uses `workflow_run` triggering which has well-documented race conditions and permission issues. cicd acknowledges this but doesn't solve it.

---

## Critique of cosmo (Round 2)

**Redundancy Score:** 5/5  
**My Assessment:** 4/5 — Slightly Inflated

### Score Justified?
**Partially.** cosmo's expertise is genuine. The foreign helper mechanism explanation, `BLOCK_SIGNALS/BLOCK_CANCELATION` documentation, OpenBSD msyscall explanation, and `__syslib v6` structure documentation are authoritative.

### Risk Remaining
- **No assembly documentation.** "Actual assembly implementation of `foreign_thunk_sysv`/`foreign_thunk_nt` not documented" is listed in "Remaining gaps"—but this IS cosmo's core domain.
- **Deadlock unverified.** "Deadlock scenario that prompted locking change still unverified (requires changelog search)"—a straightforward task left undone across two rounds.
- **Version delta is surface-level.** "No API breakage" claim is based on function signature comparison, not on behavioral testing.

### Weakest Element
The claim that `__dlopen_lock()` change provides thread safety, stated as fact: "The `__dlopen_lock()` change DOES protect concurrent dlsym." But this is inference from reading source, not verified behavior. Concurrent dlopen stress tests were never run.

---

## Critique of dbeng (Round 2)

**Redundancy Score:** 4/5  
**My Assessment:** 4/5 — Actually Justified

### Score Justified?
**Yes.** dbeng is the *only* specialist with an honest self-assessment. "Loses one point because deliverables are schemas only—needs implementation to be usable" is accurate. The schema design is comprehensive, addresses all feedback, and correctly identifies that it's aspirational.

### Risk Remaining
- **Complexity without utility.** Three separate databases (build_metadata.db, test_results.db, artifact_registry.db) with cross-database ATTACH queries is enterprise architecture for a project with 2 releases and 34 stars.
- **Schema drift.** The `abi_fingerprint` table expects struct sizes that asm couldn't provide and testcov marked "TBD."
- **No data.** Empty tables are useless. The seed script is a "stub, not complete implementation."

### Weakest Element
The `extract_versions.py` stub:
```python
if __name__ == '__main__':
    versions = get_submodule_info()
    versions['cosmocc'] = {'version': '3.9.6'}  # From build.yml
    print(json.dumps(versions, indent=2))
```
This hardcodes `3.9.6` instead of actually extracting it. It's a mock, not a tool.

---

## Critique of neteng (Round 2)

**Redundancy Score:** 5/5  
**My Assessment:** 4.5/5 — Closest to Justified

### Score Justified?
**Mostly.** neteng is the ONLY specialist who actually **ran the binary**. The Windows runtime verification ("Execution: ✅ Successful"), SHA256 checksums generated from actual files, and APE format verification with real hex bytes are empirical contributions. This is what "verified" should mean.

### Risk Remaining
- **Manual verification.** Windows test was manual, not automated. CI doesn't run it.
- **No Linux/macOS runtime verification.** Only Windows was tested. The platform matrix still shows "untested" for FreeBSD, NetBSD.
- **CDN/deployment deferred.** "No CDN/mirror distribution setup (acknowledged, lower priority)" and "No deployment workflow" remain gaps after two rounds.

### Weakest Element
The SHA256 checksums are generated but not integrated:
```
| v1.1.0 | cosmo-sokol.zip | 268B00B4798A91AD... |
```
These exist in a markdown table. They're not in the actual release notes, not in a `checksums.txt` file, not verified by CI. Documentation without integration is incomplete.

---

## Critique of testcov (Round 2)

**Redundancy Score:** 5/5  
**My Assessment:** 4/5 — Inflated

### Score Justified?
**No.** The redundancy checker celebrates "The Cosmopolitan-aware smoke test is the critical fix" and "Outstanding response to critical feedback." But:

1. The smoke test **has never been compiled or run**. It's theoretical code.
2. The `abi_verify_cosmo.c` has `/* TBD */` placeholders for the actual struct sizes.
3. "cimgui smoke test not yet created" despite cimgui being half the project.

### Risk Remaining
- **Untested tests.** The smoke_test_cosmo.c code looks correct for Cosmopolitan but has never been:
  - Compiled with cosmocc
  - Linked against sokol_cosmo.c
  - Run on any platform
- **API coverage drift.** The `gen_api_coverage.py` maintains hardcoded function lists (`SOKOL_GFX_FUNCTIONS`, etc.). These will drift from actual headers without auto-generation.
- **No coverage tooling.** "No code coverage tooling (gcov/llvm-cov) integrated" remains a gap.

### Weakest Element
```c
/* ABI_CHECK(sapp_desc, TBD);  -- needs verification */
/* ABI_CHECK(sapp_event, TBD); -- needs verification */
```
The core deliverable—ABI verification—cannot function without the actual values. testcov provides scaffolding, not solutions.

---

## Cross-Cutting Issues

### 1. Documentation ≠ Implementation
Seven of eight specialists produced documentation. Only neteng empirically verified anything. The redundancy checker conflates "well-documented plans" with "usable deliverables."

### 2. Circular Dependencies
- asm needs testcov's struct sizes → testcov needs to compile with cosmocc → cicd needs working tests → tests need verified struct sizes
- This circle was never broken. Everyone references everyone else without independent verification.

### 3. The "Remaining Gaps" Pattern
Every specialist has a "Remaining gaps" section. The redundancy checker treats acknowledged gaps as acceptable ("correctly identified as not addressable"). But repeated acknowledgment across two rounds suggests these gaps are intractable, not merely deferred.

### 4. No Integration Testing
- seeker collected URLs
- localsearch inventoried files  
- asm analyzed ABIs theoretically
- cicd wrote workflow YAML
- cosmo documented internals
- dbeng designed schemas
- neteng verified one Windows run
- testcov wrote test code

**Nobody verified the pieces work together.** Does the smoke test compile with the ABI assertions? Does the CI workflow actually run? Do the schemas capture real build data? Unknown.

---

## Revised Scores

| Specialist | Redundancy Score | Critique Score | Delta |
|------------|------------------|----------------|-------|
| seeker | 5/5 | 3.5/5 | -1.5 |
| localsearch | 5/5 | 4/5 | -1 |
| asm | 5/5 | 4/5 | -1 |
| cicd | 5/5 | 4/5 | -1 |
| cosmo | 5/5 | 4/5 | -1 |
| dbeng | 4/5 | 4/5 | 0 |
| neteng | 5/5 | 4.5/5 | -0.5 |
| testcov | 5/5 | 4/5 | -1 |

**Summary:** The redundancy checker's average was 4.875/5. My critical assessment averages 4.0/5. The reports are *good documentation* but not *production-ready deliverables*. Round 3 should demand: compile something, run something, verify something.

---

## Recommendations for Round 3

1. **Require empirical verification.** No more "TBD" placeholders. Actually run `abi_sizes.c` with cosmocc.
2. **Integration checkpoint.** Have someone (not a specialist) try to use the deliverables together.
3. **Close acknowledged gaps.** "Still unverified" appearing in Round 2 should be unacceptable for Round 3.
4. **Reduce scope.** Three databases for a 34-star project? Focus on what's actually needed.
5. **Deploy something.** Even pushing to a test repo and triggering CI would prove the workflows work.
