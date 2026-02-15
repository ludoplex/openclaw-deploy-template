# Test Strategy Report: cosmo-sokol Auto-Update

**Project:** ludoplex/cosmo-sokol  
**Upstream Sources:** floooh/sokol, jart/cosmopolitan  
**Date:** 2026-02-09  
**Round:** Swiss Rounds R1 — Initial Report

---

## 1. Current Test Status

### Existing Tests: **None**

The cosmo-sokol repository contains **zero automated tests**. The only validation mechanism is:

- **CI Build Check:** `.github/workflows/build.yml` compiles the project on ubuntu-latest
- **Manual Testing:** Running `bin/cosmo-sokol` and observing the ImGui demo window

The `deps/cimgui/test/main.c` contains a useful pattern (headless ImGui test with struct size verification), but it's not integrated into cosmo-sokol's build.

---

## 2. Risk Areas for Upstream Breakage

### 2.1 Sokol API Changes (High Risk)
The shim generation in `gen-sokol` hardcodes **183 function signatures** for sokol_app and sokol_gfx. If upstream sokol:
- Adds new functions → missing from shim
- Removes functions → dead code, but harmless
- Changes signatures → compile failure or runtime crash
- Changes struct layouts → ABI mismatch, memory corruption

### 2.2 Cosmopolitan API Changes (Medium Risk)
Uses:
- `IsLinux()`, `IsWindows()`, `IsXnu()` — platform detection
- `cosmo_dlopen()`, `cosmo_dlsym()`, `cosmo_dltramp()` — dynamic loading
- NT function prototypes from cosmopolitan headers

### 2.3 X11/OpenGL Header Drift (Low Risk)
Linux shims `gen-x11` and `gen-gl` depend on:
- Khronos gl.xml for OpenGL
- X11 function signatures

### 2.4 Struct ABI Compatibility (High Risk)
Critical structs that MUST match between upstream and shims:
- `sapp_desc`, `sapp_event`, `sapp_icon_desc`
- `sg_desc`, `sg_buffer_desc`, `sg_image_desc`, `sg_shader_desc`, `sg_pipeline_desc`
- All `*_info` query return types

---

## 3. Minimum Viable Test Suite

### Level 0: Build Verification (Must Have)

```yaml
# Already exists in .github/workflows/build.yml
- Compile all sources without errors
- Link successfully
- Produce bin/cosmo-sokol binary
```

**Recommendation:** Add `-Werror` to catch warnings (already present in build script).

---

### Level 1: Smoke Tests (Must Have)

**Purpose:** Verify the binary runs and exits cleanly.

#### 1a. Linux Smoke Test (Xvfb)
```bash
#!/bin/bash
# tests/smoke-linux.sh
set -e

# Start virtual X server
Xvfb :99 -screen 0 1024x768x24 &
export DISPLAY=:99
sleep 1

# Run with timeout, expect clean exit
timeout 5 ./bin/cosmo-sokol --smoke || true

# Check for crash (exit code 139 = SIGSEGV, 134 = SIGABRT)
EXIT_CODE=$?
if [ $EXIT_CODE -eq 139 ] || [ $EXIT_CODE -eq 134 ]; then
    echo "FAILED: Crashed with signal"
    exit 1
fi
echo "PASSED: Smoke test"
```

**Requires:** `--smoke` mode that runs a few frames then exits:
```c
// Add to main.c
static int smoke_frame_count = 0;
static bool smoke_mode = false;

void frame(void) {
    // existing code...
    if (smoke_mode && ++smoke_frame_count >= 10) {
        sapp_request_quit();
    }
}

int main(int argc, char* argv[]) {
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--smoke") == 0) smoke_mode = true;
    }
    // ...
}
```

#### 1b. Windows Smoke Test
```powershell
# tests/smoke-windows.ps1
$proc = Start-Process -FilePath ".\bin\cosmo-sokol.com" -ArgumentList "--smoke" -PassThru -Wait -NoNewWindow
if ($proc.ExitCode -ne 0) {
    Write-Error "FAILED: Exit code $($proc.ExitCode)"
    exit 1
}
```

#### 1c. macOS Smoke Test
```bash
# Currently just checks stub message appears
./bin/cosmo-sokol.com 2>&1 | grep -q "macOS not yet implemented"
```

---

### Level 2: Symbol/API Coverage Verification (Should Have)

**Purpose:** Ensure all 183 functions in gen-sokol SOKOL_FUNCTIONS exist and link.

```c
// tests/api_coverage_test.c
#include <sokol_app.h>
#include <sokol_gfx.h>
#include <stdio.h>

// Generate function pointer checks for all APIs
#define CHECK_FUNC(fn) do { \
    void* p = (void*)&fn; \
    if (!p) { printf("MISSING: " #fn "\n"); failures++; } \
} while(0)

int main(void) {
    int failures = 0;
    
    // sokol_app functions
    CHECK_FUNC(sapp_isvalid);
    CHECK_FUNC(sapp_width);
    CHECK_FUNC(sapp_height);
    CHECK_FUNC(sapp_run);
    // ... all 183 functions
    
    printf("API coverage: %d failures\n", failures);
    return failures > 0 ? 1 : 0;
}
```

**Automated Generation:**
```python
# tests/gen_api_coverage.py
# Reads SOKOL_FUNCTIONS from gen-sokol and outputs test file
```

---

### Level 3: ABI Verification (Should Have)

**Purpose:** Catch struct layout changes between upstream and cosmo builds.

```c
// tests/abi_verify.c
#include <sokol_app.h>
#include <sokol_gfx.h>
#include <assert.h>
#include <stdio.h>

// Expected sizes from upstream (update when syncing)
#define EXPECTED_SAPP_DESC_SIZE 456
#define EXPECTED_SG_DESC_SIZE 232
#define EXPECTED_SG_BUFFER_DESC_SIZE 48
// ...

#define CHECK_SIZE(type, expected) do { \
    size_t actual = sizeof(type); \
    if (actual != expected) { \
        printf("ABI MISMATCH: sizeof(" #type ") = %zu, expected %zu\n", \
               actual, expected); \
        failures++; \
    } \
} while(0)

int main(void) {
    int failures = 0;
    
    CHECK_SIZE(sapp_desc, EXPECTED_SAPP_DESC_SIZE);
    CHECK_SIZE(sapp_event, EXPECTED_SAPP_EVENT_SIZE);
    CHECK_SIZE(sg_desc, EXPECTED_SG_DESC_SIZE);
    CHECK_SIZE(sg_buffer_desc, EXPECTED_SG_BUFFER_DESC_SIZE);
    CHECK_SIZE(sg_image_desc, EXPECTED_SG_IMAGE_DESC_SIZE);
    CHECK_SIZE(sg_shader_desc, EXPECTED_SG_SHADER_DESC_SIZE);
    CHECK_SIZE(sg_pipeline_desc, EXPECTED_SG_PIPELINE_DESC_SIZE);
    // ... all critical structs
    
    if (failures == 0) {
        printf("ABI verification PASSED\n");
    }
    return failures > 0 ? 1 : 0;
}
```

**Auto-extraction:** Run on reference platform to capture expected sizes:
```bash
# scripts/extract_struct_sizes.sh
gcc -DSOKOL_GLCORE -include sokol_app.h -include sokol_gfx.h - <<'EOF'
#include <stdio.h>
int main() {
    printf("#define EXPECTED_SAPP_DESC_SIZE %zu\n", sizeof(sapp_desc));
    // ...
}
EOF
```

---

### Level 4: Shim Generation Regression (Should Have)

**Purpose:** Detect when gen-sokol output changes unexpectedly.

```bash
# tests/shim_regression.sh
# Regenerate shims and diff against committed versions

cd shims/sokol
python3 gen-sokol > /tmp/sokol_cosmo.c.new

if ! diff -q sokol_cosmo.c /tmp/sokol_cosmo.c.new; then
    echo "REGRESSION: sokol_cosmo.c differs from generated"
    diff sokol_cosmo.c /tmp/sokol_cosmo.c.new
    exit 1
fi
```

---

### Level 5: Symbol Count Tracking (Nice to Have)

**Purpose:** Detect unexpected additions/removals of exported symbols.

```bash
# tests/symbol_audit.sh
nm bin/cosmo-sokol | grep -E '^[0-9a-f]+ [Tt] (sapp_|sg_)' | wc -l > /tmp/symbol_count

EXPECTED=183  # Update when intentionally changing
ACTUAL=$(cat /tmp/symbol_count)

if [ "$ACTUAL" -ne "$EXPECTED" ]; then
    echo "Symbol count changed: expected $EXPECTED, got $ACTUAL"
    nm bin/cosmo-sokol | grep -E '^[0-9a-f]+ [Tt] (sapp_|sg_)' | sort > /tmp/symbols.txt
    # Diff against baseline
fi
```

---

## 4. Platform-Specific Test Matrix

| Test | Linux | Windows | macOS |
|------|-------|---------|-------|
| Build compiles | ✅ CI | ❌ Not in CI | ❌ Not in CI |
| Smoke test | ✅ Xvfb | ⚠️ Needs headless | ⚠️ Stub only |
| API coverage | ✅ | ✅ | ❌ N/A (stub) |
| ABI verify | ✅ | ✅ | ❌ N/A |
| GL dlopen works | ✅ Xvfb | N/A (WGL) | ❌ N/A |

### CI Platform Recommendations

```yaml
# Enhanced .github/workflows/build.yml
jobs:
  build-linux:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { submodules: recursive }
      - run: sudo apt-get install -y xvfb libx11-dev libgl-dev libxcursor-dev libxi-dev
      - uses: bjia56/setup-cosmocc@main
      - run: ./build
      - run: ./tests/smoke-linux.sh
      - run: ./tests/api_coverage_test
      - run: ./tests/abi_verify
      
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
        with: { submodules: recursive }
      - uses: bjia56/setup-cosmocc@main
      # Windows cross-compile from Linux runner
      - run: ./build
      # Note: Actual Windows testing requires self-hosted runner or wine
```

---

## 5. Recommended Test Implementation Priority

### Phase 1: Immediate (Block Auto-Update Without)
1. **Smoke test mode** — Add `--smoke` flag to main.c
2. **Linux Xvfb smoke** — Verify binary runs
3. **API coverage test** — Auto-generate from gen-sokol

### Phase 2: Before First Auto-Update
4. **ABI verification** — Capture baseline struct sizes
5. **Shim regeneration check** — Ensure gen-sokol is deterministic

### Phase 3: Ongoing
6. **Symbol count tracking** — Baseline and monitor
7. **Windows CI** — Cross-compile validation
8. **Performance baseline** — Frame time checks (optional)

---

## 6. Test Infrastructure Files to Create

```
cosmo-sokol/
├── tests/
│   ├── smoke-linux.sh
│   ├── smoke-windows.ps1
│   ├── api_coverage_test.c
│   ├── abi_verify.c
│   ├── shim_regression.sh
│   ├── symbol_audit.sh
│   └── gen_api_coverage.py
├── scripts/
│   └── extract_struct_sizes.sh
└── .github/workflows/
    └── build.yml  # Enhanced with test steps
```

---

## 7. Upstream Monitoring Strategy

### Sokol Changes to Watch
```bash
# Monitor sokol changelog for:
# - Function signature changes in sokol_app.h and sokol_gfx.h
# - New functions (need adding to gen-sokol SOKOL_FUNCTIONS)
# - Struct layout changes
# - Deprecation/removal notices

# Auto-detect new functions:
grep -E '^SOKOL_APP_API_DECL|^SOKOL_GFX_API_DECL' deps/sokol/sokol_*.h | \
    grep -oE '[a-z_]+\(' | tr -d '(' | sort -u > /tmp/upstream_funcs.txt
```

### Cosmopolitan Changes to Watch
- `IsLinux()`, `IsWindows()`, `IsXnu()` API stability
- `cosmo_dlopen` behavior changes
- NT function availability in headers

---

## 8. Summary: Minimum Viable Test Suite

| Test | Effort | Value | Auto-Generate? |
|------|--------|-------|----------------|
| Build succeeds | Exists | High | ✅ |
| Smoke test (Xvfb) | 2h | Critical | Partial |
| API coverage | 4h | High | ✅ From gen-sokol |
| ABI verify | 4h | High | ✅ Baseline script |
| Shim regression | 1h | Medium | ✅ |
| Symbol audit | 2h | Low | ✅ |

**Total estimated effort:** 13 hours to implement Phase 1 + Phase 2.

**Key insight:** The gen-sokol SOKOL_FUNCTIONS list is the source of truth. Tests should be auto-generated from it to stay in sync.
