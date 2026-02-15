# Test Coverage Report: cosmo-sokol-v3
**Specialist:** testcov  
**Round:** 1  
**Date:** 2026-02-09  
**Goal:** Keep ludoplex/cosmo-sokol fork updated with upstream without manual version pinning

---

## Executive Summary

The ludoplex/cosmo-sokol fork currently has **zero test coverage**. The CI pipeline only builds—no verification that the binary works. Upstream sokol (floooh/sokol) has comprehensive tests that are not being leveraged. This report outlines a testing strategy to:

1. Detect upstream API drift (ABI verification)
2. Verify builds work on all platforms (smoke tests)
3. Enable confident automatic updates

---

## Current State Analysis

### Repository Structure
```
ludoplex/cosmo-sokol (fork)
├── upstream: bullno1/cosmo-sokol
├── deps/sokol → floooh/sokol (submodule)
├── deps/cimgui → cimgui/cimgui (submodule)
└── shims/ (platform dispatch layer)
```

### Fork Divergence from bullno1/cosmo-sokol
- **+2,231 lines** of additions (macOS stub support)
- Key files: `sokol_macos.c` (1015 lines), `sokol_cosmo.c` (840 lines)
- Tri-platform dispatch: Linux ✅, Windows ✅, macOS 🚧 (stub)

### Current CI (`build.yml`)
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - Build only (no tests)
      - Release packaging (tags only)
```

**Problems:**
- No test step
- No multi-platform testing (only ubuntu-latest)
- No verification builds actually run
- No detection of upstream API changes

---

## ABI Verification Requirements

### gen-sokol Function Registry

The `shims/sokol/gen-sokol` script tracks **193 public sokol functions** that need platform dispatch:

| Module | Functions | Notes |
|--------|-----------|-------|
| sokol_app (`sapp_*`) | 61 | Window/input management |
| sokol_gfx (`sg_*`) | 132 | Graphics API |

**Verification needed:** When sokol upstream adds/removes/changes function signatures, `gen-sokol` MUST be updated or builds break silently.

### ABI Drift Detection Script

```python
#!/usr/bin/env python
"""abi_check.py - Detect sokol API drift"""
import re
import sys

def extract_api_decls(header_path, prefix):
    """Extract SOKOL_*_API_DECL function signatures"""
    pattern = rf'^SOKOL_{prefix.upper()}_API_DECL\s+(.+);'
    funcs = []
    with open(header_path) as f:
        for line in f:
            if match := re.match(pattern, line):
                funcs.append(match.group(1).strip())
    return set(funcs)

def extract_gen_sokol_funcs(gen_script_path):
    """Extract function signatures from gen-sokol SOKOL_FUNCTIONS"""
    funcs = []
    with open(gen_script_path) as f:
        content = f.read()
        # Extract strings from SOKOL_FUNCTIONS list
        for match in re.finditer(r'"([^"]+)"', content):
            sig = match.group(1)
            if 'sapp_' in sig or 'sg_' in sig:
                funcs.append(sig)
    return set(funcs)

def normalize_sig(sig):
    """Normalize signature for comparison"""
    # Remove parameter names, normalize whitespace
    return re.sub(r'\s+', ' ', sig.strip())

if __name__ == '__main__':
    # Compare upstream headers with gen-sokol
    # Report: new functions, removed functions, signature changes
    pass
```

### Recommended CI Check

```yaml
- name: Verify ABI sync
  run: |
    python scripts/abi_check.py \
      --sokol-app deps/sokol/sokol_app.h \
      --sokol-gfx deps/sokol/sokol_gfx.h \
      --gen-sokol shims/sokol/gen-sokol
```

---

## Smoke Test Strategy

### Level 1: Build Verification (Current)
✅ Already implemented in CI

### Level 2: Binary Execution Test (MISSING)
Verify the built binary at least starts:

```bash
# On Linux
timeout 5 ./bin/cosmo-sokol --headless 2>&1 || true

# Check for crash vs clean exit
if [ $? -eq 139 ]; then
  echo "SEGFAULT - build broken"
  exit 1
fi
```

**Requirement:** Add `--headless` flag to main.c for CI testing without display.

### Level 3: Function Coverage Smoke Tests

Create minimal test harness that exercises key paths:

```c
// test/smoke_test.c
#include <sokol_app.h>
#include <sokol_gfx.h>

// Verify function dispatch works
void smoke_test(void) {
    // These should NOT crash even without display
    (void)sapp_isvalid();  // Expected: false
    
    #ifdef HEADLESS_TEST
    // Init with dummy backend
    sg_setup(&(sg_desc){
        .environment.defaults.color_format = SG_PIXELFORMAT_RGBA8,
    });
    assert(sg_isvalid());
    sg_shutdown();
    #endif
}
```

---

## Platform Testing Matrix

### Current Support Status

| Platform | Backend | Status | Test Coverage |
|----------|---------|--------|---------------|
| Linux | OpenGL (dlopen libGL.so) | ✅ Full | ❌ None |
| Windows | OpenGL (WGL) | ✅ Full | ❌ None |
| macOS | Stub | 🚧 Compiles only | ❌ None |

### Recommended CI Matrix

```yaml
jobs:
  build-test:
    strategy:
      matrix:
        include:
          - os: ubuntu-latest
            test: true
            name: "Linux"
          - os: windows-latest
            test: true
            name: "Windows"
          - os: macos-latest
            test: false  # Stub only compiles
            name: "macOS (compile-only)"
```

### Platform-Specific Smoke Tests

**Linux:**
```bash
# Virtual framebuffer for headless GL
xvfb-run -a ./bin/cosmo-sokol --smoke-test
```

**Windows:**
```powershell
# Use software renderer
$env:LIBGL_ALWAYS_SOFTWARE = "1"
.\bin\cosmo-sokol.exe --smoke-test
```

**macOS:**
```bash
# Verify stub error message, no crash
./bin/cosmo-sokol 2>&1 | grep -q "macOS not yet supported"
```

---

## Upstream Sync Automation

### Problem: Manual Version Pinning

Currently, updating sokol requires:
1. `git submodule update --remote`
2. Manual review of changes
3. Update gen-sokol if API changed
4. Rebuild and test

### Solution: Automated Sync Workflow

```yaml
# .github/workflows/sync-upstream.yml
name: Sync Upstream
on:
  schedule:
    - cron: '0 6 * * 1'  # Weekly Monday 6 AM
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive
          
      - name: Update sokol submodule
        run: |
          cd deps/sokol
          git fetch origin
          git checkout $(git describe --tags --abbrev=0 origin/master)
          
      - name: Check for API drift
        run: python scripts/abi_check.py
        
      - name: Build test
        run: ./build
        
      - name: Create PR if changes
        uses: peter-evans/create-pull-request@v5
        with:
          title: "chore: update sokol to $(git -C deps/sokol describe)"
          body: |
            Automated sokol submodule update.
            
            **Changes:** [View diff](https://github.com/floooh/sokol/compare/$OLD..$NEW)
            **ABI Check:** ✅ Passed
```

### Bullno1 Upstream Sync

```yaml
- name: Check bullno1 upstream
  run: |
    git fetch upstream
    BEHIND=$(git rev-list HEAD..upstream/master --count)
    if [ "$BEHIND" -gt 0 ]; then
      echo "::warning::$BEHIND commits behind bullno1/cosmo-sokol"
    fi
```

---

## Test File Recommendations

### Directory Structure
```
cosmo-sokol/
├── test/
│   ├── smoke_test.c       # Basic execution test
│   ├── abi_check.py       # API drift detection
│   ├── run_tests.sh       # Test runner
│   └── headless/
│       ├── test_sapp.c    # sokol_app function coverage
│       └── test_sg.c      # sokol_gfx function coverage
├── scripts/
│   └── abi_check.py       # (or here if preferred)
└── .github/workflows/
    ├── build.yml          # Existing (enhance with tests)
    └── sync-upstream.yml  # New: automated sync
```

### Test Coverage Targets

| Component | Current | Target (Phase 1) | Target (Phase 2) |
|-----------|---------|------------------|------------------|
| Build verification | ✅ | ✅ | ✅ |
| Binary execution | ❌ | ✅ | ✅ |
| ABI drift detection | ❌ | ✅ | ✅ |
| Platform matrix | ❌ | ✅ Linux/Win | ✅ All 3 |
| Function smoke tests | ❌ | ❌ | ✅ |
| Upstream sync | ❌ | ✅ | ✅ Automated PRs |

---

## Leveraging Upstream Tests

### Sokol's Test Suite (deps/sokol/tests/)

```
deps/sokol/tests/
├── functional/
│   ├── sokol_gfx_test.c    # 2948 lines, comprehensive
│   ├── sokol_app_test.c    # App lifecycle tests
│   └── utest.h             # Test framework
└── compile/
    └── CMakeLists.txt      # Compile-only verification
```

**Opportunity:** Adapt sokol's test framework for cosmo builds:

1. `sokol_gfx_test.c` uses `force_dummy_backend.h` for headless testing
2. Could be compiled with cosmocc using platform dispatch
3. Would verify all 132 sg_* functions work correctly

### Integration Steps

```bash
# Compile sokol tests with cosmocc
compile deps/sokol/tests/functional/sokol_gfx_test.c \
  -DSOKOL_DUMMY_BACKEND \
  ${FLAGS}
```

---

## Action Items for CI/CD Specialist

1. **Immediate (P0):**
   - Add ABI check script to CI
   - Add binary execution smoke test
   
2. **Short-term (P1):**
   - Implement platform matrix testing
   - Add `--headless` / `--smoke-test` flags to main.c
   
3. **Medium-term (P2):**
   - Implement automated upstream sync workflow
   - Port sokol_gfx_test.c to cosmo build

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Upstream API break | Medium | High | ABI check script |
| Platform-specific regression | Medium | High | Matrix testing |
| macOS stub breaks | Low | Low | Compile-only verification |
| Submodule desync | High | Medium | Automated sync PRs |

---

## Conclusion

The cosmo-sokol fork lacks test coverage, relying entirely on "it compiles" as verification. To enable automatic upstream updates:

1. **Add ABI verification** to detect API drift immediately
2. **Add smoke tests** to catch runtime failures
3. **Enable multi-platform CI** to catch platform-specific issues
4. **Automate upstream sync** with PR workflow

Estimated effort: 2-3 days for P0+P1, 1 week for full implementation.

---

*Report generated by testcov specialist for Swiss Rounds v3*
