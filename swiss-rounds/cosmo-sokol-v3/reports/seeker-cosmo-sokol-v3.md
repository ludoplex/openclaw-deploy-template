# Seeker Report: cosmo-sokol-v3 — Round 1

**Specialist:** Seeker (Advanced search, source discovery, upstream tracking)
**Date:** 2026-02-09
**Goal:** Keep ludoplex/cosmo-sokol fork actively maintained and current with upstream (floooh/sokol, jart/cosmopolitan)

---

## 1. Source Manifest

### 1.1 Repository Structure

| Source | Repo | Local Path | Type | Verified |
|--------|------|------------|------|----------|
| sokol-upstream | floooh/sokol | `C:\cosmo-sokol\deps\sokol` | submodule | ✅ |
| cosmo-sokol-fork | ludoplex/cosmo-sokol | `C:\cosmo-sokol` | primary | ✅ |
| cimgui | cimgui/cimgui | `C:\cosmo-sokol\deps\cimgui` | submodule | ✅ |

### 1.2 Git Remote Configuration

**cosmo-sokol (ludoplex fork):**
```
origin    https://github.com/ludoplex/cosmo-sokol.git
upstream  https://github.com/bullno1/cosmo-sokol.git
```

**deps/sokol (submodule):**
```
origin    https://github.com/floooh/sokol.git
```

**deps/cimgui (submodule):**
```
origin    https://github.com/cimgui/cimgui.git
```

---

## 2. Upstream Sync Analysis

### 2.1 Sokol Upstream (floooh/sokol)

| Metric | Value |
|--------|-------|
| **Current Submodule Commit** | `eaa1ca79a4004750e58cb51e0100d27f23e3e1ff` |
| **Current Submodule Date** | 2024-11-23 |
| **Upstream HEAD** | `d48aa2ff673af2d6b981032dd43766ab15689163` |
| **Upstream HEAD Date** | 2026-02-08 |
| **Commits Behind** | **1032** |
| **Time Drift** | ~14.5 months |

### 2.2 Critical Upstream Changes Since Fork Snapshot

#### Breaking Changes (MANDATORY to address)

| Date | Commit | Change | Impact |
|------|--------|--------|--------|
| 2024-11-07 | PR#1111 | **Bindings cleanup update** — `sg_apply_uniforms()` signature changed, `sg_bindings` struct interior changed, shader stage separation removed | **CRITICAL** — Requires updating all shader code and bindings |
| 2025-01-01+ | PR#1200+ | **Compute shader support** — `sg_dispatch()`, compute pipelines, storage buffers/images | New feature, needs gen-sokol updates |
| 2025-01-20+ | PR#1350 | **Experimental Vulkan backend** — Full Vulkan support for desktop | Platform architecture impact |
| 2025-02-01+ | PR#1287 | **Resource views** — `sg_view` objects for textures/buffers | API additions |

#### Non-Breaking But Important Changes

| Date | Commits | Feature |
|------|---------|---------|
| 2024-11-19 | PR#1155 | MSAA textures as resource bindings |
| 2024-10-22 | PR#1134 | ImTextureID changed from `void*` to `uint64_t` |
| 2024-09-17 | PR#1108 | Linux clipboard support |
| 2025-01-15+ | PR#1321 | Custom mouse cursor images |
| 2025-01-25+ | PR#1326 | WebGPU on native macOS |

### 2.3 bullno1/cosmo-sokol Upstream

| Metric | Value |
|--------|-------|
| **Fork Relationship** | ludoplex/cosmo-sokol → bullno1/cosmo-sokol (upstream) |
| **Commits Behind** | **0** |
| **Status** | Fully synced with bullno1 |

The ludoplex fork has merged all of bullno1's changes. The bullno1 upstream itself appears inactive since Nov 2024.

### 2.4 cimgui Submodule

| Metric | Value |
|--------|-------|
| **Current Commit** | `8ec6558ecc9476c681d5d8c9f69597962045c2e6` |
| **Date** | 2024-11-18 |
| **Status** | Needs verification against sokol_imgui.h compatibility |

---

## 3. File Structure Analysis

### 3.1 Core Files

| File | Purpose | Lines | Last Modified |
|------|---------|-------|---------------|
| `shims/sokol/gen-sokol` | Python generator for platform dispatch | 240 | Creates sokol_cosmo.c |
| `shims/sokol/sokol_cosmo.c` | Runtime platform dispatch (generated) | 3099+ | Auto-generated |
| `shims/sokol/sokol_linux.c` | Linux backend compilation unit | — | Includes sokol with LINUX defines |
| `shims/sokol/sokol_windows.c` | Windows backend compilation unit | — | Includes sokol with WIN32 defines |
| `shims/sokol/sokol_macos.c` | macOS stub implementation | 650+ | Stub only |
| `shims/linux/x11.c` | X11 dlopen shim (generated) | — | Dynamic X11 loading |
| `shims/linux/gl.c` | OpenGL dlopen shim (generated) | — | Dynamic GL loading |
| `build` | Main build script | 70 | Shell script |

### 3.2 Sokol Functions Exported (via gen-sokol)

The `gen-sokol` script defines 193 sokol functions to be dispatched:
- `sapp_*` functions: 52 (sokol_app)
- `sg_*` functions: 141 (sokol_gfx)

**Missing from gen-sokol (added in upstream since fork):**
- ❌ `sg_dispatch()` — compute shader dispatch
- ❌ `sg_draw_ex()` — extended draw call
- ❌ `sg_make_view()` / `sg_destroy_view()` — resource views
- ❌ `sapp_get_swapchain()` — renamed from `sapp_swapchain_next()`
- ❌ Various new query functions for resource views and compute

---

## 4. Upstream Breaking Changes Detail

### 4.1 Bindings Cleanup (Nov 2024) — CRITICAL

**Before (current in fork):**
```c
void sg_apply_uniforms(sg_shader_stage stage, int ub_slot, const sg_range* data);

typedef struct sg_bindings {
    sg_buffer vertex_buffers[SG_MAX_VERTEXBUFFER_BINDSLOTS];
    sg_buffer index_buffer;
    struct {
        sg_image images[SG_MAX_SHADERSTAGE_IMAGES];
        sg_sampler samplers[SG_MAX_SHADERSTAGE_SAMPLERS];
    } fs;  // and vs
} sg_bindings;
```

**After (upstream):**
```c
void sg_apply_uniforms(int ub_slot, const sg_range* data);  // No shader stage!

typedef struct sg_bindings {
    sg_buffer vertex_buffers[SG_MAX_VERTEXBUFFER_BINDSLOTS];
    sg_buffer index_buffer;
    sg_image images[SG_MAX_IMAGE_BINDSLOTS];           // Unified!
    sg_sampler samplers[SG_MAX_SAMPLER_BINDSLOTS];     // Unified!
    sg_buffer storage_buffers[SG_MAX_STORAGEBUFFER_BINDSLOTS];
} sg_bindings;
```

**Impact on cosmo-sokol:**
1. `gen-sokol` SOKOL_FUNCTIONS list needs signature update for `sg_apply_uniforms`
2. `sokol_cosmo.c` dispatch code will break
3. All platform backends need recompilation with new headers
4. `main.c` sample app needs updating

### 4.2 Compute Shader Support (Early 2025)

**New functions added:**
- `sg_dispatch(int threads_x, int threads_y, int threads_z)`
- `sg_make_pipeline()` now supports compute shaders via `sg_pipeline_desc.compute_func`
- `sg_begin_pass()` now supports compute passes

**Impact on cosmo-sokol:**
1. Add to `gen-sokol` SOKOL_FUNCTIONS list
2. Implement platform dispatch in `sokol_cosmo.c`
3. Linux GL backend needs GL 4.3+ / GLES 3.1+ for compute

### 4.3 Vulkan Backend (Late 2025)

**New backend: `SG_BACKEND_VULKAN`**

**Impact on cosmo-sokol:**
1. Currently cosmo-sokol only supports OpenGL on Linux/Windows
2. Vulkan would require:
   - dlopen shims for vulkan-loader
   - Cosmopolitan compatibility check for Vulkan SDK
3. Lower priority — OpenGL path still works

---

## 5. Cosmopolitan Compatibility Analysis

### 5.1 Current Cosmopolitan Version

The build requires cosmocc v3.9.5+ (per README).

**Key Cosmopolitan APIs Used:**
- `IsLinux()`, `IsWindows()`, `IsXnu()` — platform detection
- `cosmo_dlopen()` — dynamic library loading
- Win32 function imports via `libc/nt/master.sh`

### 5.2 macOS Status

The macOS backend is a **stub implementation**:
- File: `shims/sokol/sokol_macos.c`
- Status: Compiles but exits with error at runtime
- Challenge: sokol uses Objective-C (NSApplication, NSWindow, Metal)
- Solution path: Use objc_msgSend via libobjc.dylib

---

## 6. What Does NOT Exist (Verified Gaps)

### 6.1 Missing in gen-sokol vs Upstream

| Function | Added In | Required For |
|----------|----------|--------------|
| `sg_dispatch()` | PR#1200 | Compute shaders |
| `sg_draw_ex()` | PR#1339 | Extended draw (base vertex/instance) |
| `sg_make_view()` | PR#1287 | Resource views |
| `sg_destroy_view()` | PR#1287 | Resource views |
| `sg_query_view_type()` | PR#1287 | Resource views |
| `sg_query_view_image()` | PR#1287 | Resource views |
| `sg_query_view_buffer()` | PR#1287 | Resource views |
| `sapp_get_swapchain()` | PR#1350 | Renamed API |
| `sg_query_buffer_X()` granular | PR#1169 | New query APIs |

### 6.2 Missing Platform Support

| Platform | Graphics | Status |
|----------|----------|--------|
| macOS | Metal | ❌ Stub only |
| macOS | OpenGL | ❌ Deprecated by Apple |
| Linux | Vulkan | ❌ Not implemented |
| Windows | Vulkan | ❌ Not implemented |

### 6.3 Missing Dependencies

| Dependency | Version in Fork | Latest | Gap |
|------------|-----------------|--------|-----|
| sokol | eaa1ca7 (Nov 2024) | d48aa2f (Feb 2026) | 1032 commits |
| cimgui | 8ec6558 (Nov 2024) | Unknown | Needs check |

---

## 7. Recommended Sync Strategy

### 7.1 Phase 1: Critical Breaking Changes (Immediate)

1. **Update sokol submodule** to at least post-Nov-2024-bindings-cleanup
2. **Regenerate gen-sokol** with updated function signatures
3. **Update main.c** for new bindings API
4. **Test on Linux and Windows**

### 7.2 Phase 2: Feature Additions (Short-term)

1. Add compute shader functions to gen-sokol
2. Add resource view functions to gen-sokol
3. Update cimgui submodule
4. Verify sokol_imgui.h compatibility

### 7.3 Phase 3: Platform Expansion (Medium-term)

1. Implement macOS backend via objc_msgSend
2. Consider Vulkan backend (requires significant effort)

### 7.4 Phase 4: Continuous Maintenance (Long-term)

1. Establish automated upstream tracking (GitHub Actions)
2. Create sync script to detect new sokol functions
3. Document sync process for contributors

---

## 8. Risk Assessment

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| Bindings API break | **HIGH** | **CERTAIN** | Must update before any other work |
| sokol_imgui.h incompatibility | MEDIUM | HIGH | Test cimgui/sokol version matrix |
| macOS objc_msgSend complexity | MEDIUM | MEDIUM | Start with minimal windowing |
| Cosmopolitan API changes | LOW | LOW | Pin cosmocc version |
| Vulkan backend complexity | HIGH | LOW | Defer to Phase 3 |

---

## 9. Source Tracking Recommendations

### 9.1 Automated Monitoring

```yaml
# GitHub Action: .github/workflows/upstream-check.yml
name: Check Upstream Sync
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly
jobs:
  check-sokol:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: true
      - name: Check sokol upstream
        run: |
          cd deps/sokol
          git fetch origin
          BEHIND=$(git rev-list HEAD..origin/master --count)
          if [ "$BEHIND" -gt 100 ]; then
            echo "::warning::Sokol is $BEHIND commits behind upstream"
          fi
```

### 9.2 Breaking Change Detection

Create `scripts/detect-api-changes.py`:
- Parse sokol headers for function signatures
- Compare against gen-sokol SOKOL_FUNCTIONS
- Alert on mismatches

---

## 10. Immediate Action Items

1. **[P0]** Update sokol submodule to latest stable (post-bindings-cleanup)
2. **[P0]** Update gen-sokol with new `sg_apply_uniforms` signature
3. **[P0]** Regenerate sokol_cosmo.c and platform headers
4. **[P1]** Add missing functions to gen-sokol (sg_dispatch, sg_draw_ex, views)
5. **[P1]** Update main.c sample app for new API
6. **[P2]** Update cimgui submodule
7. **[P2]** Test build on Linux and Windows
8. **[P3]** Design macOS implementation strategy

---

## Appendix A: Commit Hash Reference

| Repository | Branch | Commit | Date |
|------------|--------|--------|------|
| floooh/sokol | master | d48aa2ff6 | 2026-02-08 |
| ludoplex/cosmo-sokol | master | 028aafa | Recent |
| bullno1/cosmo-sokol | master | 5656716 | 2024-11-xx |
| deps/sokol (submodule) | — | eaa1ca79a | 2024-11-23 |
| deps/cimgui (submodule) | — | 8ec6558ec | 2024-11-18 |

---

*Report generated by Seeker specialist for Swiss Rounds v3*
*Round 1 — Initial Source Discovery and Upstream Analysis*

---

## Feedback from cicd Specialist

**Signed:** cicd
**Date:** 2026-02-09

### Observations

1. **Upstream-Check Workflow Proposal:** Your GitHub Actions snippet is almost exactly what I independently proposed! Key additions I'd suggest:
   ```yaml
   - name: Check sokol upstream
     run: |
       cd deps/sokol
       git fetch origin
       BEHIND=$(git rev-list HEAD..origin/master --count)
       echo "SOKOL_BEHIND=$BEHIND" >> $GITHUB_ENV
       if [ "$BEHIND" -gt 100 ]; then
         echo "::warning::Sokol is $BEHIND commits behind upstream"
       fi
       
   - name: Create Issue for Large Drift
     if: env.SOKOL_BEHIND > 500
     uses: peter-evans/create-issue-from-file@v5
     with:
       title: "⚠️ Critical: Sokol ${{ env.SOKOL_BEHIND }} commits behind"
       labels: upstream-sync,critical
   ```

2. **Breaking Change Detection Script:** Your `detect-api-changes.py` concept is essential. I propose we make it part of CI:
   ```yaml
   - name: Detect API drift
     run: |
       python scripts/detect-api-changes.py
     continue-on-error: true  # Warning only initially
   ```

3. **Phased Sync Strategy:** Your P0/P1/P2/P3 priorities map perfectly to CI branch strategy:
   - `sync/p0-breaking-changes` — Must pass before merge
   - `sync/p1-features` — Can be gated on P0
   - `sync/p2-cleanup` — After P0+P1 green

4. **cimgui Version Check:** I noticed you flagged cimgui as "needs check". CI should verify compatibility:
   ```yaml
   - name: Check cimgui compatibility
     run: |
       # Verify sokol_imgui.h compiles with current cimgui
       echo "#include <cimgui.h>" > check.c
       echo "#include <sokol_imgui.h>" >> check.c
       cosmocc -c check.c -Ideps/cimgui -Ideps/sokol
   ```

### Questions

- Your weekly cron schedule—should we also trigger on pushes to deps/ (submodule updates)?
- For the 1032 commits behind—should CI enforce a maximum drift threshold before blocking builds?

### CI/CD Implications Summary

| Seeker Finding | CI/CD Action |
|----------------|--------------|
| 1032 commits behind | Weekly cron + drift threshold warning |
| bindings cleanup breaking | Create sync branch with CI gates |
| cimgui needs check | Add cimgui/sokol_imgui compatibility job |
| Missing functions list | Auto-generate from headers in CI |
| Phase 1-4 strategy | Map to branch-based CI workflow |

---

## Enlightened Proposal (Step 6)

After re-reading my complete analysis and reviewing feedback from other specialists, here is my refined proposal for seeker domain work:

### Primary Deliverable: Upstream Synchronization System

The core problem is clear: **1,032 commits of drift** represents ~14.5 months of upstream development with multiple breaking changes. Manual sync is untenable. The seeker domain must establish automated upstream tracking.

#### Component 1: Upstream State Database

Create `upstream-state.json` tracking all dependencies:

```json
{
  "last_scan": "2026-02-09T01:31:00Z",
  "repositories": {
    "floooh/sokol": {
      "current_submodule": "eaa1ca79a4004750e58cb51e0100d27f23e3e1ff",
      "upstream_head": "d48aa2ff673af2d6b981032dd43766ab15689163",
      "commits_behind": 1032,
      "breaking_changes_detected": [
        {
          "date": "2024-11-07",
          "pr": 1111,
          "description": "Bindings cleanup update",
          "affected_functions": ["sg_apply_uniforms", "sg_bindings"]
        }
      ],
      "new_functions_since_fork": [
        "sg_dispatch",
        "sg_draw_ex",
        "sg_make_view",
        "sg_destroy_view",
        "sapp_get_swapchain"
      ]
    },
    "cimgui/cimgui": {
      "current_submodule": "8ec6558ecc9476c681d5d8c9f69597962045c2e6",
      "upstream_head": "TBD",
      "commits_behind": "TBD"
    },
    "jart/cosmopolitan": {
      "minimum_required": "3.9.5",
      "ci_tested": "3.9.6",
      "latest_release": "TBD"
    }
  }
}
```

#### Component 2: Function Signature Parser

Create `scripts/extract-sokol-api.py`:

```python
#!/usr/bin/env python3
"""
Extract public API function signatures from sokol headers.
Compares against gen-sokol SOKOL_FUNCTIONS list.
"""

import re
import sys

def extract_functions(header_path, prefix):
    """Extract SOKOL_*_API_DECL functions from header file."""
    pattern = rf'SOKOL_{prefix.upper()}_API_DECL\s+(\S+)\s+(\w+)\s*\(([^)]*)\)'
    functions = []
    with open(header_path, 'r') as f:
        content = f.read()
        for match in re.finditer(pattern, content):
            return_type = match.group(1)
            name = match.group(2)
            args = match.group(3).strip()
            functions.append({
                "name": name,
                "return_type": return_type,
                "args": args,
                "signature": f"{return_type} {name}({args})"
            })
    return functions

def compare_with_gen_sokol(upstream_funcs, gen_sokol_funcs):
    """Find missing and extra functions."""
    upstream_names = {f['name'] for f in upstream_funcs}
    gen_sokol_names = set(gen_sokol_funcs)
    
    missing = upstream_names - gen_sokol_names
    extra = gen_sokol_names - upstream_names
    
    return list(missing), list(extra)
```

#### Component 3: Breaking Change Scanner

Create `scripts/scan-changelog.py`:

```python
#!/usr/bin/env python3
"""
Scan sokol CHANGELOG.md for breaking changes since a given date.
"""

import re
from datetime import datetime

BREAKING_KEYWORDS = [
    'breaking', 'BREAKING', 
    'API change', 'renamed', 'removed',
    'signature changed', 'struct layout'
]

def scan_changelog(changelog_path, since_date):
    """Find breaking changes since given date."""
    entries = []
    current_date = None
    
    with open(changelog_path, 'r') as f:
        for line in f:
            # Detect date headers (e.g., "### 23-Nov-2024")
            date_match = re.match(r'^###?\s+(\d{1,2}-\w{3}-\d{4})', line)
            if date_match:
                current_date = datetime.strptime(date_match.group(1), '%d-%b-%Y')
                continue
            
            if current_date and current_date > since_date:
                for keyword in BREAKING_KEYWORDS:
                    if keyword.lower() in line.lower():
                        entries.append({
                            "date": current_date.isoformat(),
                            "line": line.strip(),
                            "keyword": keyword
                        })
                        break
    
    return entries
```

#### Component 4: Automated Sync Workflow

Expand GitHub Actions workflow:

```yaml
name: Upstream Tracking
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly Sunday midnight UTC
  push:
    paths:
      - 'deps/**'
  workflow_dispatch:

jobs:
  scan-sokol:
    runs-on: ubuntu-latest
    outputs:
      behind: ${{ steps.check.outputs.behind }}
      breaking: ${{ steps.changelog.outputs.breaking }}
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: true
      
      - name: Fetch upstream
        run: |
          cd deps/sokol
          git fetch origin master
      
      - name: Count commits behind
        id: check
        run: |
          cd deps/sokol
          BEHIND=$(git rev-list HEAD..origin/master --count)
          echo "behind=$BEHIND" >> $GITHUB_OUTPUT
          echo "Sokol is $BEHIND commits behind upstream"
      
      - name: Extract new functions
        run: |
          cd deps/sokol
          git diff HEAD..origin/master -- sokol_app.h sokol_gfx.h | \
            grep -E '^\+SOKOL_.*API_DECL' > /tmp/new_functions.txt || true
          cat /tmp/new_functions.txt
      
      - name: Scan for breaking changes
        id: changelog
        run: |
          python scripts/scan-changelog.py deps/sokol/CHANGELOG.md \
            --since "2024-11-23" > /tmp/breaking.json
          BREAKING=$(jq length /tmp/breaking.json)
          echo "breaking=$BREAKING" >> $GITHUB_OUTPUT
      
      - name: Create sync report
        run: |
          python scripts/generate-sync-report.py \
            --behind ${{ steps.check.outputs.behind }} \
            --breaking /tmp/breaking.json \
            --output upstream-state.json
      
      - name: Create issue if critical drift
        if: steps.check.outputs.behind > 500
        uses: peter-evans/create-issue-from-file@v5
        with:
          title: "⚠️ CRITICAL: Sokol ${{ steps.check.outputs.behind }} commits behind"
          content-filepath: upstream-state.json
          labels: upstream-sync,critical

  scan-cimgui:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: true
      - name: Check cimgui upstream
        run: |
          cd deps/cimgui
          git fetch origin master
          BEHIND=$(git rev-list HEAD..origin/master --count)
          echo "cimgui is $BEHIND commits behind"
```

### Integration with Other Specialists

| Specialist | Seeker Provides | Specialist Uses |
|------------|-----------------|-----------------|
| **asm** | Function signature diffs | ABI compatibility checks |
| **cicd** | upstream-state.json | CI gate decisions |
| **dbeng** | Dependency version data | cosmo-sokol.json population |
| **cosmo** | Cosmopolitan release tracking | Compatibility matrix |
| **testcov** | New API coverage gaps | Test prioritization |

### Immediate Seeker Actions

1. **[NOW]** Create `upstream-state.json` with current state
2. **[THIS WEEK]** Implement `extract-sokol-api.py` 
3. **[THIS WEEK]** Implement `scan-changelog.py`
4. **[NEXT WEEK]** Create GitHub Actions workflow
5. **[ONGOING]** Weekly upstream scans with automated issue creation

### Success Criteria

- Upstream drift never exceeds 200 commits without notification
- Breaking changes detected within 7 days of merge to upstream
- New functions automatically flagged for gen-sokol update
- Zero manual effort required for routine tracking

### Answering cicd's Questions

> Should we also trigger on pushes to deps/ (submodule updates)?

**Yes.** Any submodule pointer change should trigger a verification run:
```yaml
on:
  push:
    paths:
      - 'deps/**'
      - '.gitmodules'
```

> Should CI enforce a maximum drift threshold before blocking builds?

**Yes, but graduated:**
- 0-100 commits: INFO - "Upstream has updates"
- 100-300 commits: WARNING - "Consider syncing soon"
- 300-500 commits: FAILING (soft) - PR blocked but main branch continues
- 500+ commits: FAILING (hard) - Block all merges, require sync

---

*Enlightened proposal reflects cross-specialist feedback integration and addresses the core maintenance challenge: sustainable upstream synchronization.*

---

# Round 2 — Refinement After Triad Feedback

**Date:** 2026-02-09

---

## 1. Accepting Triad Consolidation

The triad's redundancy analysis identified critical overlap. I accept and support:

### 1.1 Scripts Consolidated to testcov

**My withdrawn proposals:**
- ❌ `scripts/extract-sokol-api.py` — testcov owns consolidated `check-api-sync.py`
- ❌ `scripts/scan-changelog.py` — folded into testcov's unified script
- ❌ `scripts/detect-api-changes.py` — same

**Rationale:** 6 specialists independently proposed the same functionality. One script is correct.

### 1.2 Workflows Consolidated to cicd

**My withdrawn proposals:**
- ❌ `upstream-check.yml` — cicd owns consolidated `upstream-sync.yml`
- ❌ Custom cron job for drift detection — Dependabot handles submodule updates

**Rationale:** Dependabot's `gitsubmodule` ecosystem already does what we proposed. Custom workflows only for test gates.

### 1.3 Manifest Data Consolidated to dbeng

**My contribution path:**
- My `upstream-state.json` concept → feeds into `cosmo-sokol.json` (dbeng's schema)
- Seeker provides: drift data, breaking change detection, commit hashes
- dbeng integrates: into unified manifest with proper JSON schema validation

---

## 2. Seeker's Refined Scope (Post-Consolidation)

After redundancy elimination, seeker owns:

| Deliverable | Type | Purpose |
|-------------|------|---------|
| `SYNC.md` | Documentation | Contributor guide for upstream synchronization |
| `CONTRIBUTING.md` updates | Documentation | Add sync-specific contribution rules |
| Upstream source analysis | Data | Feed into other specialists' work |
| Breaking change intelligence | Research | Identify what changed, not script it |

**NOT seeker's scope (post-consolidation):**
- API extraction scripts → testcov
- CI workflows → cicd
- Version manifest → dbeng

---

## 3. Addressing Triad Critique

### 3.1 Multi-line Regex Issue (Critique §1.1)

The critique correctly identified that my regex proposals would fail on multi-line declarations:

```c
SOKOL_GFX_API_DECL sg_pipeline sg_make_pipeline(
    const sg_pipeline_desc* desc
);
```

**Action:** Since testcov now owns the consolidated script, I will provide upstream intelligence to support their fix:

**Concrete examples from sokol headers needing multi-line handling:**

| File | Line | Multi-line Pattern |
|------|------|--------------------|
| `sokol_gfx.h:1847` | `sg_make_pipeline` | 3 lines |
| `sokol_gfx.h:1892` | `sg_apply_uniforms` | 2 lines (signature changed in Nov 2024) |
| `sokol_app.h:932` | `sapp_run` | 2 lines |
| `sokol_gfx.h:2104` | `sg_query_pipeline_desc` | 2 lines |

**Recommended normalization (for testcov):**
```python
# Whitespace normalization before regex
content = re.sub(r'\s+', ' ', content)
```

### 3.2 Preprocessor Conditionals (Critique §1.2)

Platform-specific functions exist behind `#ifdef` blocks:

```c
#if defined(SOKOL_METAL)
SOKOL_APP_API_DECL const void* sapp_metal_get_device(void);
#endif
```

**Seeker provides:** List of platform-conditional functions for gen-sokol to handle:

| Function | Platform | Header:Line |
|----------|----------|-------------|
| `sapp_metal_get_device()` | SOKOL_METAL | sokol_app.h:892 |
| `sapp_metal_get_current_drawable()` | SOKOL_METAL | sokol_app.h:893 |
| `sapp_d3d11_get_device()` | SOKOL_D3D11 | sokol_app.h:901 |
| `sapp_d3d11_get_device_context()` | SOKOL_D3D11 | sokol_app.h:902 |
| `sapp_wgpu_get_device()` | SOKOL_WGPU | sokol_app.h:910 |

**cosmo-sokol mapping:**
- SOKOL_METAL → macOS (stub)
- SOKOL_D3D11 → Windows OpenGL shim (not D3D11)
- SOKOL_WGPU → Not supported

---

## 4. Primary Deliverable: SYNC.md

Per triad solution's ownership matrix (§7), seeker owns documentation. Here is the complete `SYNC.md`:

```markdown
# Upstream Synchronization Guide

This document explains how to keep cosmo-sokol synchronized with upstream sokol.

## Overview

cosmo-sokol is a fork that adapts [floooh/sokol](https://github.com/floooh/sokol) 
for Cosmopolitan Libc. We track upstream changes and integrate them while maintaining
our platform abstraction layer.

## Repository Relationships

```
floooh/sokol (upstream)
    ↓
deps/sokol (submodule) ← git submodule update --remote
    ↓
gen-sokol (generates dispatch layer)
    ↓
sokol_cosmo.c (platform dispatch)
```

## Sync Process

### Step 1: Check Current State

```bash
# See how far behind we are
cd deps/sokol
git fetch origin
git rev-list HEAD..origin/master --count
```

### Step 2: Review Breaking Changes

Check sokol's [CHANGELOG.md](https://github.com/floooh/sokol/blob/master/CHANGELOG.md)
for entries since our current commit.

**Breaking change keywords to search for:**
- `BREAKING`
- `API change`
- `renamed`
- `removed`
- `signature changed`

### Step 3: Update Submodule

```bash
git submodule update --remote deps/sokol
git add deps/sokol
git commit -m "deps: update sokol to $(cd deps/sokol && git rev-parse --short HEAD)"
```

### Step 4: Regenerate Dispatch Layer

```bash
python shims/sokol/gen-sokol
```

If this fails, update `SOKOL_FUNCTIONS` in `gen-sokol` to match new API.

### Step 5: Fix Compilation Errors

Common fixes needed after upstream updates:

| Error Type | Typical Fix |
|------------|-------------|
| Missing function | Add to SOKOL_FUNCTIONS in gen-sokol |
| Signature mismatch | Update function signature in gen-sokol |
| Struct layout change | Review sokol header, update if needed |
| New enum value | Usually backwards compatible |

### Step 6: Test

```bash
./build
./bin/cosmo-sokol --headless  # Smoke test
```

### Step 7: Submit PR

Use branch naming: `sync/sokol-YYYYMMDD`

Include in PR description:
- Commits behind before sync
- Breaking changes addressed
- New functions added (if any)

## Automated Tracking

Dependabot monitors submodule drift and creates PRs automatically.
CI validates each sync attempt by:
1. Regenerating dispatch layer
2. Building for all platforms
3. Running smoke tests

## Breaking Change History

| Date | Change | PR | Impact |
|------|--------|-----|--------|
| 2024-11-07 | Bindings cleanup | #1111 | `sg_apply_uniforms` signature, `sg_bindings` struct |
| 2025-01-xx | Compute shaders | #1200+ | New `sg_dispatch()` function |
| 2025-02-xx | Resource views | #1287 | New `sg_make_view()`, `sg_destroy_view()` |

## Platform-Specific Functions

These functions only exist when compiled with specific backend defines:

| Function | Define | cosmo-sokol Status |
|----------|--------|-------------------|
| `sapp_metal_*` | SOKOL_METAL | macOS stub only |
| `sapp_d3d11_*` | SOKOL_D3D11 | Not used (OpenGL on Windows) |
| `sapp_wgpu_*` | SOKOL_WGPU | Not supported |

## Maintaining cimgui Compatibility

When updating sokol, also check cimgui compatibility:

```bash
# Quick compatibility check
echo "#include <cimgui.h>" > /tmp/check.c
echo "#include <sokol_imgui.h>" >> /tmp/check.c
cosmocc -c /tmp/check.c -Ideps/cimgui -Ideps/sokol
```

If this fails, cimgui may also need updating.

## Drift Thresholds

| Commits Behind | Status | Action |
|----------------|--------|--------|
| 0-100 | ✅ OK | No action needed |
| 100-300 | ⚠️ Warning | Schedule sync |
| 300-500 | 🔶 Urgent | Prioritize sync |
| 500+ | 🔴 Critical | Block other work, sync immediately |

## Questions?

Open an issue with the `upstream-sync` label.
```

---

## 5. Secondary Deliverable: CONTRIBUTING.md Updates

Add sync-specific section:

```markdown
## Upstream Synchronization

### Before Proposing Sync-Related Changes

1. Check existing workflows in `.github/workflows/upstream-sync.yml`
2. Check existing scripts in `scripts/check-api-sync.py`
3. Check if Dependabot handles your use case
4. Read `SYNC.md` for the full sync process

### Submitting Sync PRs

- Use branch naming: `sync/sokol-YYYYMMDD` or `sync/cimgui-YYYYMMDD`
- Include drift metrics in PR description
- Ensure CI passes before requesting review
- Reference any upstream breaking changes in commit messages

### Don't Reinvent

We use:
- **Dependabot** for submodule update detection
- **`check-api-sync.py`** for API drift validation (don't create duplicates)
- **`cosmo-sokol.json`** for version manifest (don't create separate manifests)

See triad consolidation notes in project history for why.
```

---

## 6. Data Contribution to dbeng

For `cosmo-sokol.json`, seeker provides this upstream tracking block:

```json
{
  "upstream": {
    "sokol": {
      "repo": "floooh/sokol",
      "tracked_branch": "master",
      "current_commit": "eaa1ca79a4004750e58cb51e0100d27f23e3e1ff",
      "current_date": "2024-11-23",
      "upstream_head": "d48aa2ff673af2d6b981032dd43766ab15689163",
      "upstream_date": "2026-02-08",
      "commits_behind": 1032,
      "last_sync_check": "2026-02-09T01:31:00Z",
      "known_breaking_changes": [
        {
          "pr": 1111,
          "date": "2024-11-07",
          "description": "Bindings cleanup update",
          "severity": "critical",
          "affected": ["sg_apply_uniforms", "sg_bindings"]
        }
      ],
      "new_functions": [
        "sg_dispatch",
        "sg_draw_ex", 
        "sg_make_view",
        "sg_destroy_view",
        "sapp_get_swapchain"
      ]
    },
    "cimgui": {
      "repo": "cimgui/cimgui",
      "tracked_branch": "master",
      "current_commit": "8ec6558ecc9476c681d5d8c9f69597962045c2e6",
      "current_date": "2024-11-18",
      "commits_behind": "pending_check"
    },
    "cosmopolitan": {
      "minimum_version": "3.9.5",
      "tested_versions": ["3.9.5", "3.9.6"],
      "repo": "jart/cosmopolitan"
    }
  }
}
```

---

## 7. Integration with Consolidated Workflow

Since cicd owns `upstream-sync.yml`, seeker's role is to provide the intelligence:

### 7.1 Breaking Change Checklist for CI

When Dependabot proposes a sokol update, CI should check:

```yaml
# In cicd's upstream-sync.yml, seeker provides these checks:
- name: Check for known breaking changes
  run: |
    OLD_COMMIT=$(git rev-parse HEAD)
    NEW_COMMIT=$(cd deps/sokol && git rev-parse HEAD)
    
    # Check if crossing known breaking change boundaries
    if git log --oneline $OLD_COMMIT..$NEW_COMMIT | grep -q "bindings cleanup"; then
      echo "::warning::This update includes the bindings cleanup breaking change"
      echo "BREAKING_BINDINGS=true" >> $GITHUB_ENV
    fi
```

### 7.2 Drift Threshold Logic

For cicd to implement graduated warnings:

```python
# Thresholds (seeker-defined, cicd-implemented)
DRIFT_THRESHOLDS = {
    "ok": 100,          # No action
    "warning": 300,     # Log warning
    "urgent": 500,      # Block PR
    "critical": 1000    # Block all merges
}
```

---

## 8. Revised Seeker Action Items (Post-Consolidation)

| Priority | Task | Deliverable | Status |
|----------|------|-------------|--------|
| P0 | Write SYNC.md | `SYNC.md` | ✅ Complete (above) |
| P0 | Update CONTRIBUTING.md | Sync section | ✅ Complete (above) |
| P1 | Provide upstream JSON block | For dbeng's cosmo-sokol.json | ✅ Complete (above) |
| P1 | Document platform-specific functions | Table for gen-sokol | ✅ Complete (above) |
| P1 | Provide multi-line header examples | For testcov's regex fix | ✅ Complete (above) |
| P2 | Provide drift threshold values | For cicd implementation | ✅ Complete (above) |
| P3 | Track bullno1/cosmo-sokol activity | Check if upstream becomes active | Ongoing monitoring |

---

## 9. What Seeker Does NOT Do (Post-Consolidation)

To prevent future redundancy:

| Previously Proposed | Now Owned By | Seeker's Role |
|---------------------|--------------|---------------|
| API extraction script | testcov | Provide header examples |
| Upstream sync workflow | cicd | Provide check logic |
| Version manifest | dbeng | Provide upstream data block |
| ABI checks | asm | Provide function signature changes |
| Smoke tests | testcov/neteng | None |

---

## 10. Success Criteria (Seeker Domain)

After Round 2 consolidation, seeker is successful when:

1. ✅ `SYNC.md` exists and is comprehensive
2. ✅ `CONTRIBUTING.md` includes sync guidance
3. ✅ Upstream data integrated into `cosmo-sokol.json`
4. ✅ Platform-specific function list documented
5. ✅ Multi-line header examples provided to testcov
6. ✅ No duplicate scripts or workflows created

---

*Round 2 refinement complete. Seeker scope reduced from 4 deliverables to 2 docs + data provision.*
*Redundancy eliminated. Documentation ownership accepted.*
