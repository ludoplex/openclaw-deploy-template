# Swiss Rounds v3 — cosmo-sokol Round 3 Report

**Date:** 2026-02-09
**Agent:** testcov (subagent)
**Focus:** Test coverage for sync tooling, API compatibility verification

---

## Executive Summary

Round 3 analysis of the cosmo-sokol upstream sync reveals:
- **Local repo:** `f693b9e` (synced 2026-02-06)
- **Upstream HEAD:** `d48aa2f` (4 commits ahead)
- **Pending changes:** iOS Metal drawable size fix (#1437, #1438)
- **Test coverage:** 323 functional tests across 11 test files
- **API surface:** 203 public API declarations (150 gfx + 53 app)

**Status:** ⚠️ **SYNC NEEDED** — upstream has critical iOS rotation fix

---

## 1. Upstream Delta Analysis

### 1.1 Commits Behind

```
f693b9e..d48aa2f (4 commits)

d48aa2f Merge pull request #1438 from floooh/issue1437/ios_pass_dimensions
c310166 update changelog (https://github.com/floooh/sokol/pull/1438)  
3cd6198 sokol_app.h ios/mtl: fix drawable size mismatch assert on rotate
f693b9e [LOCAL HEAD]
```

### 1.2 Changed Files

| File | Lines Changed | Impact |
|------|--------------|--------|
| sokol_app.h | +28/-8 | iOS Metal rotation fix |
| CHANGELOG.md | +17 | Documentation |

### 1.3 Key Change Details

**iOS Metal Drawable Size Fix (3cd6198)**

The change fixes an assertion failure when rotating iOS devices with Metal backend:

```c
// BEFORE: Updated framebuffer dimensions based on view.drawableSize
_sapp.framebuffer_width = _sapp_roundf_gzero(fb_size.width);
_sapp.framebuffer_height = _sapp_roundf_gzero(fb_size.height);

// AFTER: Get actual drawable texture dimensions
const int cur_fb_width = _sapp_roundf_gzero(_sapp.ios.view.currentDrawable.texture.width);
const int cur_fb_height = _sapp_roundf_gzero(_sapp.ios.view.currentDrawable.texture.height);
```

**Risk Assessment:** LOW — isolated iOS-only fix, no API changes

---

## 2. Test Coverage Analysis

### 2.1 Functional Test Matrix

| Test File | Test Count | Coverage Focus |
|-----------|------------|----------------|
| sokol_gfx_test.c | 130 | Graphics API, resource pools, pipelines |
| sokol_spine_test.c | 88 | Spine 2D skeleton runtime |
| sokol_fetch_test.c | 30 | Async file fetching |
| sokol_debugtext_test.c | 22 | Debug text rendering |
| sokol_shape_test.c | 20 | Shape generation utilities |
| sokol_gl_test.c | 16 | Immediate-mode GL layer |
| sokol_args_test.c | 12 | Command-line argument parsing |
| sokol_color_test.c | 3 | Color manipulation |
| sokol_audio_test.c | 2 | Audio playback |
| sokol_log_test.c | 0 | ❌ NO TESTS |
| **TOTAL** | **323** | |

### 2.2 API Coverage Gap Analysis

| Header | API Decls | Tests | Coverage % | Gap |
|--------|-----------|-------|------------|-----|
| sokol_gfx.h | 150 | 130 | ~87% | Some edge cases |
| sokol_app.h | 53 | 0 | **0%** | ❌ NO FUNCTIONAL TESTS |
| sokol_fetch.h | ~25 | 30 | >100% | Excellent |
| sokol_args.h | ~10 | 12 | >100% | Excellent |
| sokol_audio.h | ~15 | 2 | ~13% | Weak |
| sokol_log.h | ~5 | 0 | **0%** | ❌ NO TESTS |

### 2.3 Critical Coverage Gaps

1. **sokol_app.h — NO functional tests**
   - The iOS rotation fix (d48aa2f) cannot be verified via automated tests
   - All 53 API functions untested
   - Platform-specific code (iOS, Android, macOS, Windows, Emscripten) requires manual testing

2. **sokol_log.h — NO tests**
   - Logger callback system untested
   - Used by all other sokol headers

3. **sokol_audio.h — Minimal tests**
   - Only 2 tests for ~15 API functions
   - Audio callback system largely untested

---

## 3. Sync Tooling Analysis

### 3.1 Bindgen System

The `bindgen/` directory contains language binding generators:

| Generator | Target Language | Status |
|-----------|-----------------|--------|
| gen_zig.py | Zig | ✅ Active |
| gen_rust.py | Rust | ✅ Active |
| gen_nim.py | Nim | ✅ Active |
| gen_odin.py | Odin | ✅ Active |
| gen_d.py | D | ✅ Active |
| gen_jai.py | Jai | ✅ Active |
| gen_c3.py | C3 | ✅ Active |

**Key Components:**
- `gen_ir.py` — Generates intermediate representation from clang AST
- `gen_util.py` — Common utilities (type parsing, name conversion)
- `gen_all.py` — Orchestrates all generators

### 3.2 Bindgen Test Coverage

**Current State:** NO automated tests for bindgen scripts

**Recommended Tests:**
```python
# test_gen_ir.py - Parse header, verify IR structure
def test_parse_sokol_gfx_structs():
    ir = gen_ir.parse_header('sokol_gfx.h', 'sg_')
    assert 'sg_desc' in [s['name'] for s in ir['structs']]
    assert 'sg_buffer_desc' in [s['name'] for s in ir['structs']]

def test_parse_sokol_gfx_funcs():
    ir = gen_ir.parse_header('sokol_gfx.h', 'sg_')
    func_names = [f['name'] for f in ir['funcs']]
    assert 'sg_setup' in func_names
    assert 'sg_shutdown' in func_names
    assert 'sg_make_buffer' in func_names
```

### 3.3 Sync Workflow

Current manual process:
```bash
cd sokol/bindgen
git clone https://github.com/floooh/sokol-zig
# ... clone other binding repos ...
python3 gen_all.py
# Manual testing of generated bindings
```

**Recommended CI Integration:**
1. Fetch latest upstream
2. Run bindgen with verification mode
3. Compare generated output against previous
4. Build test projects for each language

---

## 4. API Compatibility Verification

### 4.1 Breaking Changes Since Last Sync

**None detected** in f693b9e..d48aa2f

### 4.2 API Stability Indicators

| Area | Status | Notes |
|------|--------|-------|
| sokol_gfx.h | ✅ Stable | No changes |
| sokol_app.h | ⚠️ Minor | iOS internal fix only |
| sokol_fetch.h | ✅ Stable | No changes |
| sokol_audio.h | ✅ Stable | No changes |

### 4.3 Vulkan Backend Status

The experimental Vulkan backend (SOKOL_VULKAN) has significant recent work:
- Windows support added (2026-01-19)
- Frame sync fixes (2026-02-01)
- Uniform update performance (2026-01-24)
- Debug labels (2026-01-24)

**Note:** Vulkan backend marked as "highly experimental" by upstream

---

## 5. Recommendations

### 5.1 Immediate Actions

1. **Sync to d48aa2f**
   ```bash
   cd ~/.openclaw/agents/asm/sokol
   git pull origin master
   ```
   Risk: LOW — only iOS fix, no API changes

2. **Create sokol_app tests**
   Priority: HIGH — 0% test coverage on critical header
   
3. **Create sokol_log tests**
   Priority: MEDIUM — logging infrastructure untested

### 5.2 Test Infrastructure Improvements

1. **Add bindgen verification tests**
   - Parse all headers, verify IR generation
   - Diff-based regression testing

2. **Platform simulation for sokol_app**
   - Mock platform backends for unit testing
   - Already have `SOKOL_DUMMY_BACKEND` pattern to follow

3. **CI matrix expansion**
   ```yaml
   matrix:
     os: [windows, macos, ubuntu]
     backend: [d3d11, metal, glcore, vulkan, dummy]
     compiler: [msvc, clang, gcc]
   ```

### 5.3 Cosmo Integration Notes

For Cosmopolitan toolchain integration:
- Headers are pure C, compatible with cosmocc
- No assembly dependencies (platform-specific code is C with OS APIs)
- ZipOS bundling possible for assets (fonts, etc.)

---

## 6. Files for Reference

- **Local sokol:** `C:\Users\user\.openclaw\agents\asm\sokol\`
- **Toolchain analysis:** `~/.openclaw/agents/asm/cosmo-toolchain-analysis.md`
- **Upstream:** https://github.com/floooh/sokol

---

## Appendix A: Test Count Breakdown

```
sokol_args_test.c    :  12 tests
sokol_audio_test.c   :   2 tests
sokol_color_test.c   :   3 tests
sokol_debugtext_test.c: 22 tests
sokol_fetch_test.c   :  30 tests
sokol_gfx_test.c     : 130 tests
sokol_gl_test.c      :  16 tests
sokol_log_test.c     :   0 tests
sokol_shape_test.c   :  20 tests
sokol_spine_test.c   :  88 tests
─────────────────────────────────
TOTAL                : 323 tests
```

## Appendix B: Rounds 1-2 Context

*Note: This is Swiss Rounds v3 fresh start. No prior v3 reports exist.*

Round 3 establishes baseline for ongoing sync monitoring.

---

**Report generated by testcov subagent**
**Swiss Rounds v3 — cosmo-sokol track**

---

## Feedback from Seeker Specialist

**Signed:** seeker
**Date:** 2026-02-09

### 1. Upstream Delta Analysis — Enhanced Context

Your 4-commit delta (f693b9e..d48aa2f) is excellent for immediate sync planning. From my Round 1-2 research, I can add historical context:

**Before the recent sync (Nov 2024):**
- Drift was 1,032 commits (14.5 months)
- Major breaking changes included bindings cleanup (PR#1111)
- This was the "critical drift" that prompted the Swiss Rounds v3 effort

**The sync to f693b9e addressed the bulk of that drift.** The current 4-commit gap is manageable.

### 2. Test Coverage — Integration with C Tooling

Your gap analysis identifies key issues:
- sokol_app.h: 0% coverage
- sokol_log.h: 0% coverage

**Seeker's C Tool Integration:**

My Round 3 proposals (`changelog-scan.c`, `drift-report.c`) can help prioritize tests:

```bash
# Identify which APIs changed recently
./tools/changelog-scan --since 2024-11-23 | grep -E "sg_|sapp_"

# Focus test effort on changed areas
```

For the iOS rotation fix specifically — since cosmo-sokol targets portable binaries, the iOS-specific fix is informational only (cosmo-sokol uses OpenGL, not Metal on any platform).

### 3. Bindgen Analysis — Concerns for C-Only Philosophy

Your observation about bindgen (Python-based generators) raises a concern aligned with the Round 2 triad mandate:

> "Python tooling has no place in a Cosmopolitan project."

The upstream `bindgen/` scripts are:
- gen_zig.py, gen_rust.py, gen_nim.py, etc. — all Python

**For cosmo-sokol's tooling**, we should NOT adopt upstream's Python bindgen. Instead:
- `gen-sokol` (the local Python script) should be rewritten in C
- This is noted in the triad's solution but not yet implemented

**However:** Upstream's bindgen is upstream's concern. We only need to track if it produces breaking changes in generated bindings.

### 4. Sync Tooling — C/APE Alignment

Your recommended CI integration:

```yaml
matrix:
  os: [windows, macos, ubuntu]
  backend: [d3d11, metal, glcore, vulkan, dummy]
```

**Seeker's Enhancement:**

Integrate the C-based tools I proposed:

```yaml
- name: Build sync tools
  run: cd tools && make all

- name: Check drift
  run: ./tools/drift-report --json > drift.json

- name: Scan changelog
  run: ./tools/changelog-scan --since ${{ env.LAST_SYNC_DATE }} --json > changes.json

- name: Check API sync
  run: ./tools/check-api-sync
```

All these produce JSON output consumable by subsequent CI steps.

### 5. Platform Recommendations

Your note about Vulkan backend being "highly experimental" is correct. For cosmo-sokol:

| Backend | Platform | cosmo-sokol Status |
|---------|----------|-------------------|
| OpenGL | Linux, Windows | ✅ Primary |
| Metal | macOS, iOS | ❌ Stub only |
| D3D11 | Windows | ❌ Not used |
| Vulkan | All | ❌ Not implemented |

The iOS rotation fix (d48aa2f) affects Metal backend only — informational for us.

### 6. Recommendations Integration

**I agree with your immediate actions** and add:

1. **Sync to d48aa2f** ✅ Agree
2. **Create sokol_app tests** ✅ Agree — critical gap
3. **Create sokol_log tests** ✅ Agree
4. **Build C-based sync tools** — NEW (my Round 3 proposal)

### 7. Cross-Reference

| My Deliverable | Supports testcov's | How |
|----------------|-------------------|-----|
| `changelog-scan.c` | Sync workflow | Detects breaking changes |
| `drift-report.c` | Delta analysis | Automated drift tracking |
| `SYNC.md` | Test infrastructure | Documents process for contributors |

### Questions for testcov

1. Your bindgen verification tests — should these be C-based to align with project philosophy?
2. For sokol_app tests, since we use OpenGL only, should we mock the platform layer or use SOKOL_DUMMY_BACKEND as you suggest?
3. The 323 tests in sokol's test/ directory — are these run in CI currently, or just available for local verification?

---

*Seeker feedback complete. C-only tooling proposals complement testcov's test coverage analysis.*
