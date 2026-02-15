# Cosmo-Sokol v3 Analysis: Cosmopolitan Libc Specialist Report

**Domain:** Cosmopolitan libc internals (dlopen, APE format, cross-platform shims)
**Goal:** Keep ludoplex/cosmo-sokol fork updated with upstream without manual version pinning
**Date:** 2026-02-09
**Round:** 1

---

## 1. Executive Summary

The cosmo-sokol project is an elegant example of Cosmopolitan's "compile once, run anywhere" philosophy applied to graphics programming. It wraps the sokol library (a cross-platform 3D graphics library) with runtime dispatch shims that select the appropriate platform implementation at runtime using `IsLinux()`, `IsWindows()`, and `IsXnu()` checks.

**Key Finding:** Automated upstream sync is achievable but requires careful handling of two distinct sync vectors:
1. **floooh/sokol** → deps/sokol submodule (API changes affect shim generation)
2. **bullno1/cosmo-sokol** → ludoplex/cosmo-sokol fork structure (shim pattern changes)

---

## 2. Architecture Analysis

### 2.1 Runtime Platform Dispatch

The core innovation is the runtime dispatch pattern in `sokol_cosmo.c`:

```c
bool sapp_isvalid(void) {
    if (IsLinux()) {
        return linux_sapp_isvalid();
    }
    if (IsWindows()) {
        return windows_sapp_isvalid();
    }
    if (IsXnu()) {
        return macos_sapp_isvalid();
    }
}
```

Each platform implementation is compiled with function name prefixes (`linux_`, `windows_`, `macos_`) via generated header files (`sokol_linux.h`, etc.).

### 2.2 Cosmopolitan dlopen Shim Layer

The Linux implementation (`shims/linux/x11.c`, `shims/linux/gl.c`) uses **cosmo_dlopen** and **cosmo_dlsym** rather than standard POSIX dlopen:

```c
// From x11.c
static void load_X11_procs(void) {
    libX11 = cosmo_dlopen("libX11.so", RTLD_NOW | RTLD_GLOBAL);
    proc_XOpenDisplay = cosmo_dltramp(cosmo_dlsym(libX11, "XOpenDisplay"));
    ...
}
```

**Critical Cosmopolitan APIs used:**
- `cosmo_dlopen()` - Load dynamic library (works across Linux/macOS)
- `cosmo_dlsym()` - Get symbol address
- `cosmo_dltramp()` - Create trampoline for cross-ABI calls
- `IsLinux()`, `IsWindows()`, `IsXnu()` - Runtime platform detection

### 2.3 Current Fork Relationship

```
floooh/sokol (upstream lib)
    ↓ [submodule: deps/sokol]
bullno1/cosmo-sokol (original cosmopolitan wrapper)
    ↓ [forked]
ludoplex/cosmo-sokol (adds macOS stub support)
```

---

## 3. API Stability Analysis

### 3.1 Cosmopolitan API Dependencies

| API | Stability | Notes |
|-----|-----------|-------|
| `cosmo_dlopen` | Stable | Core API since v2.x |
| `cosmo_dlsym` | Stable | Core API |
| `cosmo_dltramp` | Stable | Required for calling foreign ABIs |
| `IsLinux/IsWindows/IsXnu` | Stable | Fundamental detection macros |
| `libc/nt/master.sh` pattern | Semi-stable | Windows API imports require upstream changes |

### 3.2 Sokol API Drift Vectors

The `gen-sokol` script maintains a **hardcoded list** of sokol functions (`SOKOL_FUNCTIONS`):

```python
SOKOL_FUNCTIONS = [
    "bool sapp_isvalid()",
    "int sapp_width()",
    ...
    # ~180 functions total
]
```

**Risk:** New sokol functions added upstream require manual addition to this list.

---

## 4. Automated Update Strategy

### 4.1 Submodule Update Workflow

For sokol submodule updates:

```bash
# In deps/sokol
git fetch origin
git checkout <new-tag-or-commit>

# Regenerate shims
cd shims/sokol
./gen-sokol  # Updates sokol_cosmo.c and platform headers

# Test build
cd ../..
./build
```

### 4.2 Upstream Fork Sync Workflow

```bash
# Fetch upstream bullno1 changes
git fetch upstream
git merge upstream/master

# Resolve conflicts in:
#   - shims/sokol/gen-sokol (if function list changed)
#   - shims/sokol/sokol_cosmo.c (regenerate after merge)
#   - Any new platform shims they add
```

### 4.3 Automation Recommendations

**Proposed CI/CD Pipeline:**

```yaml
# .github/workflows/sync-upstream.yml
name: Sync Upstream
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly
  workflow_dispatch:

jobs:
  check-upstream:
    steps:
      - name: Check sokol for updates
        run: |
          cd deps/sokol
          git fetch origin
          CURRENT=$(git rev-parse HEAD)
          LATEST=$(git rev-parse origin/master)
          if [ "$CURRENT" != "$LATEST" ]; then
            echo "SOKOL_UPDATE=true" >> $GITHUB_ENV
          fi
      
      - name: Extract new sokol API
        if: env.SOKOL_UPDATE == 'true'
        run: |
          # Parse sokol_app.h and sokol_gfx.h for new SOKOL_API_DECL functions
          # Compare against SOKOL_FUNCTIONS list in gen-sokol
          # Generate PR if new functions detected
          
      - name: Check bullno1 upstream
        run: |
          git fetch upstream
          # Check for new commits, patterns, or shim changes
```

---

## 5. macOS Stub Completion Path

### 5.1 Current State

The macOS backend is a **stub** that compiles but doesn't render. It needs Objective-C runtime calls via pure C.

### 5.2 Cosmopolitan-Compatible Implementation

The approach outlined in `shims/macos/README.md` is correct. Here's a refined pattern:

```c
// shims/macos/objc_runtime.c
#include <dlfcn.h>

typedef void* id;
typedef void* SEL;
typedef void* Class;

static void* libobjc = NULL;
static id (*msgSend)(id, SEL, ...) = NULL;
static Class (*getClass)(const char*) = NULL;
static SEL (*registerName)(const char*) = NULL;

void cosmo_objc_init(void) {
    libobjc = cosmo_dlopen("/usr/lib/libobjc.dylib", RTLD_NOW);
    msgSend = cosmo_dltramp(cosmo_dlsym(libobjc, "objc_msgSend"));
    getClass = cosmo_dltramp(cosmo_dlsym(libobjc, "objc_getClass"));
    registerName = cosmo_dltramp(cosmo_dlsym(libobjc, "sel_registerName"));
}

// Usage:
// id pool = msgSend(getClass("NSAutoreleasePool"), registerName("new"));
```

**Key insight:** Unlike X11/OpenGL shims, Objective-C calls need careful handling of:
1. Variable argument passing through `objc_msgSend`
2. Return type variations (`objc_msgSend_stret`, `objc_msgSend_fpret`)
3. Block handling (if needed for callbacks)

---

## 6. Windows API Considerations

### 6.1 NT Import Pattern

Windows APIs are imported via Cosmopolitan's `libc/nt/master.sh`:

```
GetClientRect,kernel32,3
SetWindowTextA,user32,2
```

**Current status:** The cosmo-sokol project relies on updates merged into Cosmopolitan upstream for any new Win32 APIs needed by sokol.

### 6.2 NVAPI Integration

The `nvapi/` directory contains NVIDIA API shims for GPU detection. This is fork-specific and independent of upstream sync.

---

## 7. Version Pinning Elimination Strategy

### 7.1 Current Pinning Points

| What | Where | How to Automate |
|------|-------|-----------------|
| sokol version | `.gitmodules` + submodule commit | CI check + PR generation |
| cosmopolitan version | `build.yml` (`version: "3.9.6"`) | Dependabot or renovate |
| SOKOL_FUNCTIONS list | `gen-sokol` | API extractor script |
| cimgui version | `.gitmodules` + submodule | CI check + PR generation |

### 7.2 API Function Extractor

Create a script to extract public API from sokol headers:

```python
# scripts/extract-sokol-api.py
import re

def extract_api(header_path):
    with open(header_path) as f:
        content = f.read()
    
    # Match SOKOL_API_DECL function declarations
    pattern = r'SOKOL_API_DECL\s+([\w\s\*]+)\s+(\w+)\s*\(([^)]*)\)'
    matches = re.findall(pattern, content)
    
    return [f"{ret.strip()} {name}({args})" 
            for ret, name, args in matches]

# Compare with SOKOL_FUNCTIONS in gen-sokol
# Generate update if delta detected
```

---

## 8. Cosmopolitan-Specific Risks

### 8.1 ABI Changes

Cosmopolitan occasionally changes its ABI for NT or platform shims. Watch for:
- Changes to `cosmo_dltramp` behavior
- New platform detection macros
- NT import changes in `master.sh`

### 8.2 APE Format Evolution

The APE (Actually Portable Executable) format evolves. While this rarely affects source code, it can affect:
- Binary compatibility across platforms
- Debug symbol handling
- Strip/objcopy behavior

### 8.3 Version Matrix

Track compatibility:

| cosmocc version | sokol tag | cimgui tag | Status |
|-----------------|-----------|------------|--------|
| 3.9.6 | eaa1ca7 | master | ✅ Current |
| 3.10.x | TBD | TBD | ⚠️ Test needed |

---

## 9. Recommendations

### 9.1 Immediate Actions

1. **Create API extractor script** to auto-detect new sokol functions
2. **Add GitHub Action** to check for upstream updates weekly
3. **Document cosmopolitan version compatibility** in README

### 9.2 Medium-Term

1. **Implement macOS backend** using objc_msgSend pattern
2. **Create regression test suite** that builds on each platform
3. **Establish fork contribution guidelines** for upstream PRs

### 9.3 Long-Term

1. **Consider proposing sokol-cosmo to floooh** as an official backend option
2. **Monitor Cosmopolitan dlopen evolution** for API improvements
3. **Explore Metal support path** for macOS (vs OpenGL via objc)

---

## 10. Files of Interest

| File | Purpose | Update Sensitivity |
|------|---------|-------------------|
| `shims/sokol/gen-sokol` | Generates dispatch code | **HIGH** - must track sokol API |
| `shims/linux/gen-x11` | Generates X11 shims | Medium - X11 API stable |
| `shims/linux/gen-gl` | Generates OpenGL shims | Medium - OpenGL stable |
| `shims/sokol/sokol_cosmo.c` | Runtime dispatch | **AUTO** - regenerated |
| `.gitmodules` | Submodule pins | **HIGH** - tracks versions |
| `build` | Build script | Low - stable |

---

## Appendix A: Cosmopolitan API Quick Reference

```c
// Platform detection
bool IsLinux(void);
bool IsWindows(void);
bool IsXnu(void);        // macOS
bool IsBsd(void);
bool IsOpenbsd(void);
bool IsFreebsd(void);

// Dynamic loading
void* cosmo_dlopen(const char* path, int mode);
void* cosmo_dlsym(void* handle, const char* symbol);
void* cosmo_dltramp(void* fn);  // Create ABI-safe trampoline
int cosmo_dlclose(void* handle);
char* cosmo_dlerror(void);

// Memory
void* _mapshared(size_t size);
void* _mapanon(size_t size);
```

---

*Report generated by Cosmo specialist (cosmo-sokol-v3 Round 1)*
