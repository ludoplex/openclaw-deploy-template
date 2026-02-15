# Triad Phase 1: Redundancy Check — cosmo-sokol-v3 — Round 2

**Triad Role:** Redundancy Checker  
**Date:** 2026-02-09  
**Reports Analyzed:** 8 specialist Round 2 reports  
**Input Context:** Round 1 Triad feedback (Redundancy, Critique, Solution)  
**Goal:** Verify specialists consolidated as instructed; catch new redundancies; flag ignored mature tools

---

## Executive Summary

**Overall Assessment: 85% COMPLIANT** — Specialists largely followed consolidation instructions. Most duplications eliminated. However:

| Category | Status | Details |
|----------|--------|---------|
| Script consolidation | ✅ Complied | 6 scripts → 1 (testcov owns `check-api-sync.py`) |
| Workflow consolidation | ✅ Complied | 4 workflows → 1 (cicd owns `upstream-sync.yml`) |
| Manifest consolidation | ⚠️ Partial | dbeng's `cosmo-sokol.json` is primary, but neteng still references `version-manifest.json` |
| Mature tools ignored | ⚠️ Still present | libabigail, pycparser, Renovate still not adopted |
| Scope creep | ✅ Controlled | No inappropriate scope creep detected |
| New redundancies | ⚠️ Minor | 2 small overlaps identified |

---

## 1. Consolidation Compliance Verification

### 1.1 API Extraction Scripts — ✅ COMPLIED

**Round 1 Problem:** 6 specialists proposed identical scripts:
- cosmo: `extract-sokol-api.py`
- localsearch: `extract-sokol-api.py`
- seeker: `extract-sokol-api.py`
- testcov: `abi_check.py`
- cicd: "API drift detection step"
- neteng: `check-api-drift.py`

**Round 2 Status:**

| Specialist | Action | Verification |
|------------|--------|--------------|
| testcov | ✅ Created unified `check-api-sync.py` | Owner as assigned |
| cosmo | ✅ Deferred to testcov | No duplicate script |
| localsearch | ✅ Deferred to testcov | Only provides pre-validation |
| seeker | ✅ Deferred to testcov | Only provides documentation |
| cicd | ✅ Deferred to testcov | Calls testcov's script in CI |
| neteng | ✅ Deferred to testcov | Removed `check-api-drift.py` proposal |

**Verdict:** ✅ Consolidation successful.

---

### 1.2 Sync Workflows — ✅ COMPLIED

**Round 1 Problem:** 4 specialists proposed sync workflows:
- cicd: `upstream-sync.yml`
- neteng: `sync-upstream.yml`
- seeker: `upstream-check.yml`
- testcov: `sync-check.yml`

**Round 2 Status:**

| Specialist | Action | Verification |
|------------|--------|--------------|
| cicd | ✅ Created unified `upstream-sync.yml` | Owner as assigned |
| neteng | ✅ Retracted `sync-upstream.yml` | Uses cicd's workflow |
| seeker | ✅ Retracted workflow | Only provides documentation |
| testcov | ⚠️ Minor inconsistency | References `sync-check.yml` in Phase 2 but deferred |

**Verdict:** ✅ Consolidation successful (minor cleanup needed in testcov docs).

---

### 1.3 Metadata Manifests — ⚠️ PARTIAL COMPLIANCE

**Round 1 Problem:** 3 specialists proposed different manifests:
- dbeng: `cosmo-sokol.json` (selected)
- localsearch: `version.yaml` (eliminated)
- neteng: `version-manifest.json` (eliminated)

**Round 2 Status:**

| Specialist | Action | Verification |
|------------|--------|--------------|
| dbeng | ✅ `cosmo-sokol.json` v2.0.0 created | Owner as assigned |
| localsearch | ✅ Eliminated `version.yaml` | Provides data to dbeng |
| neteng | ⚠️ Still references `version-manifest.json` | Lines 259, 315 of report |

**Issue Found:**

neteng's Round 2 report still contains:
```yaml
- name: Generate version manifest (dbeng/neteng)
  run: python3 scripts/generate-manifest.py > bin/version-manifest.json
```

And references `generate-manifest.py` as a deliverable.

**Required Fix:** neteng should:
1. Remove `generate-manifest.py` references
2. Use dbeng's `cosmo-sokol.json` instead
3. Or coordinate with dbeng to have their script update the unified manifest

**Verdict:** ⚠️ Partial compliance. neteng needs to align with dbeng's schema.

---

### 1.4 Dependabot Adoption — ✅ COMPLIED

**Round 1 Instruction:** Use Dependabot for submodule tracking instead of custom cron jobs.

**Round 2 Status:**
- cicd: ✅ Created `.github/dependabot.yml`
- All specialists: ✅ No custom cron jobs for detection (only for threshold-based issue creation)

**Verdict:** ✅ Existing tool adopted.

---

## 2. NEW Redundancies Detected in Round 2

### 2.1 Pre-Validation Overlap (Minor)

**localsearch's `validate-source-files.py`:**
```python
REQUIRED_FILES = {
    "deps/sokol/sokol_app.h": {
        "min_size": 100000,
        "must_contain": ["SOKOL_APP_API_DECL", "sapp_run"]
    },
    ...
}
```

**testcov's `check-api-sync.py`:**
- Also implicitly checks file existence when opening headers
- Fails if files don't exist

**Assessment:** Low overlap. localsearch's script is a *pre-flight check* that validates file health before regex runs. testcov's script assumes files exist. Both can coexist, but they MUST run in correct order:

```yaml
# CI order
- name: Pre-validate source files
  run: python scripts/validate-source-files.py  # localsearch

- name: Check API sync
  run: python scripts/check-api-sync.py  # testcov
```

**Verdict:** ⚠️ Minor redundancy, but architecturally sound. Keep both.

---

### 2.2 dlopen Safety Macros Duplication Risk

**cosmo's `cosmo_dl_safe.h`:**
```c
#define COSMO_DL_LOAD_LIB(handle_var, lib_path, lib_name) do { \
    (handle_var) = cosmo_dlopen((lib_path), RTLD_NOW | RTLD_GLOBAL); \
    ...
```

**asm's `cosmo_dlopen_safe.h`:**
```c
#define COSMO_LOAD_LIB(var, name) do { \
    var = cosmo_dlopen(name, RTLD_NOW | RTLD_GLOBAL); \
    ...
```

**Issue:** Both specialists created nearly identical headers for dlopen safety macros.

**Resolution Required:**
- Use cosmo's version (owns shim layer per consolidation)
- asm's proposal should be marked as "superseded by cosmo's implementation"
- OR merge the best features from both into a single header

**Verdict:** ⚠️ NEW redundancy detected. Requires resolution.

---

## 3. Existing Mature Tools STILL Being Ignored

### 3.1 libabigail / abidiff — IGNORED

**What it is:** GNU's ABI compliance checker that compares binary ABIs between library versions. Used by major projects (glibc, systemd, libabigail itself).

**What specialists did instead:** Static assertions for struct sizes (asm).

**Gap:**
- Static assertions verify *compile-time* sizes
- `abidiff` verifies *binary-level* ABI compatibility
- When calling system libraries via dlopen, *binary ABI* matters more

**How libabigail works:**
```bash
# Install
apt install abigail-tools

# Generate ABI from binary
abidw --out-file libX11.abi /usr/lib/x86_64-linux-gnu/libX11.so.6

# Compare ABIs across versions
abidiff old-libX11.abi new-libX11.abi
```

**Recommendation:**
For verifying that cosmo-sokol's shims are compatible with system libraries:
```yaml
- name: Verify OpenGL ABI stability
  run: |
    abidw --out-file current-gl.abi /usr/lib/x86_64-linux-gnu/libGL.so.1
    # Compare against known-good baseline
    abidiff baseline-gl.abi current-gl.abi
```

**Priority:** P2 — Nice to have, but static assertions cover the critical path.

---

### 3.2 pycparser / tree-sitter — IGNORED

**What they are:**
- **pycparser:** Pure Python C parser, generates AST from C code
- **tree-sitter:** Multi-language parser with C bindings, used by GitHub for syntax highlighting

**What specialists did instead:** Regex with whitespace normalization.

**testcov's approach (Round 2):**
```python
# Whitespace normalization fixes multi-line
content = re.sub(r'\s+', ' ', content)
pattern = rf'{macro}\s+(?!typedef)(\w[\w\s\*]+?)\s+(\w+)\s*\(([^)]*)\)\s*;'
```

**Gap:** Still fragile for edge cases:
- Preprocessor macros in function declarations
- Nested parentheses in parameters
- Function pointers as parameters
- Attributes (`__attribute__((unused))`)

**How pycparser works:**
```python
from pycparser import c_parser, c_ast

parser = c_parser.CParser()
ast = parser.parse('''
SOKOL_GFX_API_DECL sg_pipeline sg_make_pipeline(
    const sg_pipeline_desc* desc
);
''')

# Walk AST to extract function declarations reliably
for node in ast.ext:
    if isinstance(node, c_ast.Decl):
        print(f"Function: {node.name}")
```

**Why this matters:**
sokol headers contain complex declarations that regex can misparse:
```c
SOKOL_GFX_API_DECL void sg_apply_uniforms(int ub_slot, 
                                          const sg_range* data 
                                          SOKOL_MAYBE_UNUSED);
```

The `SOKOL_MAYBE_UNUSED` attribute will confuse regex.

**Recommendation:**
```python
# In check-api-sync.py, add proper C parsing as fallback
try:
    from pycparser import parse_file
    # Use robust AST parsing
except ImportError:
    # Fall back to regex for environments without pycparser
```

**Priority:** P2 — Current regex works for now, but add pycparser for robustness.

---

### 3.3 Renovate vs Dependabot — NOT CONSIDERED

**Round 1 mentioned Renovate** as alternative to Dependabot if submodule support is insufficient.

**Round 2 Status:** Only Dependabot was implemented.

**Gap Analysis:**

| Feature | Dependabot | Renovate |
|---------|------------|----------|
| Git submodules | ✅ Basic | ✅ Better (nested support) |
| Dockerfile base images | ❌ | ✅ |
| Custom version files | ❌ | ✅ Regex manager |
| Grouped updates | ❌ | ✅ |
| Self-hosted | ❌ | ✅ |

**For cosmo-sokol specifically:**
- Dependabot's `gitsubmodule` ecosystem works for deps/sokol and deps/cimgui
- BUT deps/cimgui contains *nested* submodule (deps/cimgui/imgui)
- Dependabot may not update the nested submodule

**Recommendation:**
Monitor whether Dependabot updates the nested imgui submodule. If not, consider:
```yaml
# renovate.json
{
  "extends": ["config:recommended"],
  "git-submodules": {
    "enabled": true,
    "recursive": true  # Handles nested submodules
  }
}
```

**Priority:** P3 — Wait and see if Dependabot is sufficient.

---

### 3.4 step-security/harden-runner — NOT ADOPTED

**What it is:** GitHub Action that adds security monitoring to CI runs. Detects:
- Unexpected network calls
- Malicious code execution
- Exfiltration attempts

**Round 1 mentioned it** for action hardening alongside SHA pinning.

**Round 2 Status:** neteng SHA-pinned actions but didn't add harden-runner.

**How it works:**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: step-security/harden-runner@17d0e2bd7d51742c71671bd19fa12bdc9d40a3d6
        with:
          egress-policy: audit  # or 'block'
          
      - uses: actions/checkout@v4
        # ... rest of workflow
```

**Benefits:**
- Catches supply chain attacks in dependencies
- Generates network egress reports
- Can block unauthorized outbound connections

**Recommendation:**
```yaml
# Add as first step in build.yml
- uses: step-security/harden-runner@17d0e2bd7d51742c71671bd19fa12bdc9d40a3d6
  with:
    egress-policy: audit
    allowed-endpoints: >
      api.github.com:443
      github.com:443
      objects.githubusercontent.com:443
```

**Priority:** P2 — Quick win for supply chain security.

---

### 3.5 pin-github-action CLI — NOT USED

**What it is:** CLI tool to automatically pin GitHub Actions to SHAs.

**Round 2 Status:** neteng manually looked up and pinned SHAs.

**How it works:**
```bash
npm install -g pin-github-action

# Automatically update all actions to SHA pins
pin-github-action .github/workflows/build.yml
```

**Benefits:**
- Less manual work
- Can be run in pre-commit hook
- Catches new actions added by contributors

**Recommendation:** Add to contributing guidelines:
```markdown
## Adding GitHub Actions

Before committing workflow changes:
```bash
npx pin-github-action .github/workflows/*.yml
```

This ensures all actions are pinned to commit SHAs.
```

**Priority:** P3 — Nice to have for maintainer productivity.

---

## 4. Scope Creep Assessment

### 4.1 Checking for Deferred Items Returning

**Items explicitly deferred in Round 1:**

| Item | Status in Round 2 | Verdict |
|------|-------------------|---------|
| Vulkan backend | ❌ Not mentioned | ✅ Stayed out of scope |
| Full macOS implementation | ❌ Not mentioned | ✅ Stayed out of scope |
| SBOM generation | ❌ Not mentioned | ✅ Stayed out of scope |
| Visual regression testing | ❌ Not mentioned | ✅ Stayed out of scope |

**Verdict:** ✅ No scope creep from deferred items.

---

### 4.2 New Scope in Round 2

| New Item | Specialist | Assessment |
|----------|------------|------------|
| ARM64 testing | asm | ✅ Valid — addresses Critique §2.4 |
| verify-symbols.sh | localsearch | ✅ Valid — post-build sanity check |
| watch-manifest.json | localsearch | ⚠️ Questionable — adds maintenance burden |
| Windows type cross-validation | asm | ✅ Valid — addresses Windows ABI safety |

**watch-manifest.json Assessment:**

localsearch proposes tracking all files that need monitoring:
```json
{
  "source_files": {
    "sokol_headers": [
      {"path": "deps/sokol/sokol_app.h", "watch_patterns": ["SOKOL_APP_API_DECL"]}
    ]
  }
}
```

**Concern:** This creates a *third* JSON manifest in addition to:
- `cosmo-sokol.json` (dbeng)
- `dependabot.yml` (cicd)

**Recommendation:** Either:
1. Merge into `cosmo-sokol.json` under a `watch` key
2. Or defer entirely — Dependabot already triggers on submodule changes

**Priority:** P3 — Defer or merge into existing manifest.

---

## 5. Residual Cleanup Required

### 5.1 File References to Remove/Update

| File | Issue | Required Fix |
|------|-------|--------------|
| neteng report | References `version-manifest.json` | Use `cosmo-sokol.json` |
| neteng report | References `generate-manifest.py` | Coordinate with dbeng |
| testcov report | References `sync-check.yml` in Phase 2 | Remove reference |
| asm report | Proposes `cosmo_dlopen_safe.h` | Defer to cosmo's `cosmo_dl_safe.h` |

### 5.2 Ownership Clarifications Needed

| Deliverable | Claimed By | Resolution |
|-------------|------------|------------|
| dlopen safety macros | cosmo + asm | **cosmo** is authoritative owner |
| cosmocc version matrix | cicd | Confirmed (asm provides compatibility data) |
| SHA256SUMS | neteng | Confirmed |
| Nested submodule tracking | dbeng | Confirmed (seeker provides data) |

---

## 6. Updated Consolidated Work Item List

After Round 2 redundancy elimination:

### Phase 1: Foundation (Week 1) — No Changes from Round 1

| ID | Task | Owner | Status |
|----|------|-------|--------|
| F1 | Configure Dependabot for submodules | cicd | ✅ Done |
| F2 | Add static assertions | asm | ✅ Done (enhanced) |
| F3 | Create API sync check script | testcov | ✅ Done |
| F4 | Create cosmo-sokol.json | dbeng | ✅ Done (v2.0.0) |
| F5 | Pin GitHub Actions | neteng | ✅ Done |

### Phase 2: CI/CD (Week 2) — Updated

| ID | Task | Owner | Status |
|----|------|-------|--------|
| C1 | Create unified upstream-sync workflow | cicd | ✅ Done |
| C2 | Add headless flag to main.c | testcov | ✅ Done |
| C3 | Add dlopen safety macros | cosmo | ✅ Done |
| C4 | Add platform test matrix | cicd + neteng | ✅ Done |
| C5 | Add SHA256SUMS to releases | neteng | ✅ Done |

### Phase 3: Automation (Week 3) — Updated

| ID | Task | Owner | Status |
|----|------|-------|--------|
| A1 | Enable auto-PR for submodule updates | cicd | Pending (via Dependabot) |
| A2 | Add cosmocc version matrix | cicd | ✅ Done |
| A3 | Create sync documentation | seeker | ✅ Done (SYNC.md) |

---

## 7. Items to Eliminate (Newly Identified)

Based on Round 2 analysis:

| Item | Original Owner | Reason |
|------|----------------|--------|
| `version-manifest.json` | neteng | Use `cosmo-sokol.json` |
| `generate-manifest.py` | neteng | Merge into dbeng's workflow |
| `watch-manifest.json` | localsearch | Merge into `cosmo-sokol.json` or defer |
| `cosmo_dlopen_safe.h` | asm | Use cosmo's `cosmo_dl_safe.h` |
| `sync-check.yml` references | testcov | Cleaned up to cicd's workflow |

---

## 8. Recommendations

### 8.1 For Round 3 or Implementation Phase

1. **Resolve dlopen header ownership:** cosmo and asm must agree on single header
2. **neteng alignment:** Update to use `cosmo-sokol.json` instead of separate manifest
3. **Consider pycparser:** Add as optional dependency for robust C parsing
4. **Add step-security/harden-runner:** Quick supply chain security win
5. **Monitor Dependabot:** Verify nested imgui submodule updates work

### 8.2 Integration Order (Updated)

```
Week 1: ✅ DONE (F1-F5)
├── Dependabot configured
├── Static assertions added
├── check-api-sync.py created
├── cosmo-sokol.json v2.0.0 created
└── GitHub Actions SHA-pinned

Week 2: ✅ DONE (C1-C5)
├── upstream-sync.yml consolidated
├── --headless flag added
├── cosmo_dl_safe.h created
├── Platform matrix (Linux/Windows/macOS)
└── SHA256SUMS in releases

Week 3: IN PROGRESS (A1-A3)
├── Dependabot auto-PRs enabled
├── cosmocc version matrix [3.9.5, 3.9.6]
└── SYNC.md documentation
```

---

## 9. Summary

### Round 2 Compliance Score: 85%

**What went well:**
- Script consolidation (6 → 1) fully achieved
- Workflow consolidation (4 → 1) fully achieved
- Dependabot adopted over custom crons
- No scope creep on deferred items
- All P0 issues from Critique addressed

**What needs work:**
- neteng still has separate manifest (minor)
- dlopen header duplication between cosmo/asm (minor)
- Mature tools still being reinvented (libabigail, pycparser)

**Risk Assessment:**

| Issue | Severity | Action |
|-------|----------|--------|
| Manifest duplication | Low | neteng aligns with dbeng |
| dlopen header duplication | Low | cosmo's version is authoritative |
| No pycparser | Medium | Current regex works; add later |
| No harden-runner | Medium | Quick security win |

---

## 10. Conclusion

The specialists successfully followed Round 1 consolidation instructions. The major redundancies (6 scripts → 1, 4 workflows → 1, 3 manifests → 1) are resolved. 

Two minor new redundancies emerged (dlopen headers, manifest references) but these are easily resolvable by clarifying ownership.

The persistent gap is **mature tooling adoption**. Specialists continue to build custom solutions (regex parsing, static assertions) when battle-tested tools exist (pycparser, libabigail). This is acceptable for the MVP but should be revisited for long-term maintenance robustness.

**Recommendation:** Proceed to implementation. Address the minor cleanup items in parallel. Consider mature tool adoption in a future maintenance cycle.

---

*Triad Round 2 Redundancy Check Complete*  
*Ready for implementation phase*
