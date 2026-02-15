# cosmo-sokol Architecture Manifest

> **Source:** `C:\cosmo-sokol` (ludoplex/cosmo-sokol fork)  
> **Goal:** Keep fork updated with upstream sources (floooh/sokol, jart/cosmopolitan)  
> **Date:** 2026-02-09

---

## Executive Summary

cosmo-sokol wraps the [sokol](https://github.com/floooh/sokol) single-file libraries for Cosmopolitan libc, enabling truly portable fat binaries (Linux + Windows + macOS from one executable). It achieves this through:

1. **Compile-time prefixing** — All sokol functions get platform-specific prefixes (e.g., `sapp_run` → `linux_sapp_run`)
2. **Runtime dispatch** — A shim layer routes calls to the correct platform implementation at runtime
3. **Dynamic library loading** — System libraries (X11, OpenGL, Win32) are dlopen'd rather than linked

---

## 1. gen-sokol Script — Code Generation

**File:** `shims/sokol/gen-sokol` (lines 1-267)

### Purpose
Generates both the platform prefix headers (`sokol_linux.h`, `sokol_windows.h`, `sokol_macos.h`) and the runtime dispatch shim (`sokol_cosmo.c`).

### SOKOL_FUNCTIONS List (lines 7-199)
The script maintains an **explicit list of all exported sokol public functions**. This is the critical touchpoint for upstream updates:

```python
SOKOL_FUNCTIONS = [
    # sokol_app (61 functions)
    "bool sapp_isvalid()",
    "int sapp_width()",
    "void sapp_run(const sapp_desc* desc)",
    # ... etc ...
    
    # sokol_gfx (136 functions)
    "void sg_setup(const sg_desc* desc)",
    "sg_buffer sg_make_buffer(const sg_buffer_desc* desc)",
    # ... etc ...
]
```

**Current count:** ~197 functions total (61 sokol_app + 136 sokol_gfx)

### Platform Configuration (lines 201-206)
```python
PLATFORMS = [
    {"name": "linux", "check": "IsLinux", "enabled": True},
    {"name": "windows", "check": "IsWindows", "enabled": True},
    {"name": "macos", "check": "IsXnu", "enabled": True},
]
```

### Prefix Trick (lines 220-228)
For each platform, generates a header with `#define` macros:
```c
// sokol_linux.h
#define sapp_isvalid linux_sapp_isvalid
#define sapp_width linux_sapp_width
// ...
```

This allows including sokol headers multiple times with different prefixes:
- `sokol_linux.c` includes `sokol_linux.h` before `sokol_app.h` → functions become `linux_*`
- `sokol_windows.c` includes `sokol_windows.h` → functions become `windows_*`

### Signature Parser (lines 246-288)
Regex-based C function signature parser:
```python
pattern = r"(?P<return_type>[...])(?P<name>[...])\\s*\\((?P<args>.*)\\)"
```

Handles pointer types, const qualifiers, and void parameters.

---

## 2. sokol_cosmo.c — Runtime Dispatch

**File:** `shims/sokol/sokol_cosmo.c` (3099 lines, auto-generated)

### Header Comments (lines 1-9)
```c
// Auto-generated: sokol runtime dispatch for Cosmopolitan
// Dispatches sokol calls to the correct platform implementation at runtime.

#include <sokol_app.h>
#include <sokol_gfx.h>
#include <cosmo.h>
#pragma GCC diagnostic ignored "-Wreturn-type"
```

### Dispatch Pattern
For each function, the generator creates:

1. **External declarations** for all platform variants:
```c
extern bool linux_sapp_isvalid(void);
extern bool windows_sapp_isvalid(void);
extern bool macos_sapp_isvalid(void);
```

2. **Dispatch function** using Cosmopolitan runtime checks:
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

### Return Type Handling
- For `void` functions: calls platform function then `return;`
- For non-void: `return` the platform function result

**Note:** `#pragma GCC diagnostic ignored "-Wreturn-type"` suppresses warnings for missing return in unreachable code paths.

---

## 3. Platform Backends

### 3.1 sokol_linux.c (14 lines)

**File:** `shims/sokol/sokol_linux.c`

```c
#define SOKOL_GLCORE
#define SOKOL_IMPL
#define dlopen cosmo_dlopen      // Use Cosmopolitan's dlopen
#define dlsym cosmo_dlsym        // Use Cosmopolitan's dlsym
#define SOKOL_NO_ENTRY
#define sokol_main linux_sokol_main

#ifndef __linux__
#define __linux__
#endif

#include "sokol_linux.h"         // Apply linux_ prefix macros
#include "sokol_app.h"
#include "sokol_gfx.h"
```

**Key insight:** The `#define dlopen cosmo_dlopen` redirects sokol's internal dlopen calls to Cosmopolitan's portable implementation.

### 3.2 sokol_windows.c (297+ lines)

**File:** `shims/sokol/sokol_windows.c`

This file is the most complex because Cosmopolitan's Windows headers are incomplete. It manually defines:

1. **Type definitions** (lines 1-300):
   - `LARGE_INTEGER`, `RECT`, `POINT`, `MSG`
   - `PIXELFORMATDESCRIPTOR`, `MONITORINFO`, `RAWINPUT`
   - `WNDCLASSW`, `BITMAPV5HEADER`, etc.

2. **Win32 constants** (throughout):
   - Window styles: `WS_EX_OVERLAPPEDWINDOW`, `WS_CAPTION`, etc.
   - Messages: `WM_CLOSE`, `WM_KEYDOWN`, `WM_MOUSEMOVE`, etc.
   - Virtual keys: `VK_SHIFT`, `VK_CONTROL`, etc.

3. **Function aliasing** (line ~280):
```c
#define CreateWindowExW CreateWindowEx
#define DefWindowProcW DefWindowProc
#define DispatchMessageW DispatchMessage
// ... etc
```

4. **Sokol configuration**:
```c
#define _WIN32
#define SOKOL_GLCORE
#define SOKOL_NO_ENTRY
#define SOKOL_IMPL
#include "sokol_windows.h"
#include "sokol_app.h"
#include "sokol_gfx.h"
```

### 3.3 sokol_macos.c (778 lines) — STUB

**File:** `shims/sokol/sokol_macos.c`

Currently a **stub implementation** with detailed documentation on the challenge:

```c
/*
 * CHALLENGE:
 * Sokol's macOS backend uses Objective-C extensively. Cosmopolitan's
 * cosmocc cannot directly compile Objective-C code.
 * 
 * FUTURE IMPLEMENTATION OPTIONS:
 * 1. OBJC RUNTIME VIA C: Use objc_msgSend pattern
 * 2. MINIMAL NATIVE HELPER: dlopen'd Objective-C library
 * 3. GLFW/SDL ALTERNATIVE: C-based windowing
 */
```

All functions return stub values and print a warning at runtime:
```c
void macos_sapp_run(const sapp_desc* desc) {
    _macos_not_implemented("sapp_run");
    // ...
    exit(1);
}
```

### 3.4 sokol_shared.c (10 lines)

**File:** `shims/sokol/sokol_shared.c`

Shared code that doesn't need platform dispatch:
```c
#define SOKOL_NO_ENTRY
#define SOKOL_GLCORE
#include "sokol_app.h"
#include "sokol_gfx.h"
#define SOKOL_IMPL
#include "sokol_log.h"
#include "sokol_glue.h"
```

---

## 4. System Shims — dlopen Pattern

### 4.1 gen-x11 (lines 1-132)

**File:** `shims/linux/gen-x11`

Generates X11 shims via dlopen pattern. Function list organized by library:

```python
FUNCTIONS = {
    "X11": [
        "Display *XOpenDisplay(const char *display_name)",
        "int XCloseDisplay(Display *display)",
        # ~55 functions total
    ],
    "Xcursor": [
        "Cursor XcursorImageLoadCursor(Display *dpy, const XcursorImage *image)",
        # 6 functions
    ],
    "Xi": [
        "Status XIQueryVersion(Display* dpy, int* major_version_inout, ...)",
        # 2 functions
    ],
}
```

### 4.2 x11.c Output (lines 1-500+)

**File:** `shims/linux/x11.c` (auto-generated)

Generated pattern for each function:

1. **Static library handle and function pointer:**
```c
static void* libX11 = NULL;
static Display * (*proc_XOpenDisplay)(const char* display_name) = NULL;
```

2. **Loader function:**
```c
static void load_X11_procs(void) {
    libX11 = cosmo_dlopen("libX11.so", RTLD_NOW | RTLD_GLOBAL);
    proc_XOpenDisplay = cosmo_dltramp(cosmo_dlsym(libX11, "XOpenDisplay"));
    assert(proc_XOpenDisplay != NULL && "Could not load XOpenDisplay");
    // ...
}
```

3. **Shim function:**
```c
Display * XOpenDisplay(const char* display_name) {
    if (libX11 == NULL) { load_X11_procs(); }
    return proc_XOpenDisplay(display_name);
}
```

**Key pattern:** `cosmo_dltramp()` creates a trampoline for cross-platform ABI compatibility.

### 4.3 gen-gl (lines 1-95)

**File:** `shims/linux/gen-gl`

Parses Khronos OpenGL XML registry to generate GL shims:

```python
MIN_VERSION = (4, 0)  # GL 4.0 minimum

tree = ET.parse("gl.xml")
# Iterate versions, extract required commands
# Generate proc_glXxx pointers and shim functions
```

### 4.4 gl.c Output (6172 lines)

**File:** `shims/linux/gl.c` (auto-generated)

Same dlopen pattern but with GL registry-derived functions. Includes all GL ≤4.0 functions.

---

## 5. Build Script

**File:** `build` (52 lines)

### Environment Detection (lines 3-8)
```sh
if ! command -v cosmocc > /dev/null; then
    echo "You need to add cosmopolitan toolchain to your path"
    exit 1
fi
COSMO_HOME=$(dirname $(dirname $(which cosmocc)))
```

### Compiler Flags (lines 10-22)
```sh
FLAGS="-I deps/sokol -I deps/cimgui -mcosmo -mtiny -Wall -Werror"
LINUX_FLAGS="${FLAGS} -Ishims/linux"
WIN32_FLAGS="${FLAGS} -Ishims/win32 -I ${COSMO_HOME}/include/libc/nt"
MACOS_FLAGS="${FLAGS}"
```

### Compilation Targets (lines 26-49)

| Target | Flags |
|--------|-------|
| `shims/sokol/sokol_windows.c` | `WIN32_FLAGS` |
| `shims/sokol/sokol_linux.c` | `LINUX_FLAGS` |
| `shims/sokol/sokol_macos.c` | `MACOS_FLAGS` |
| `shims/sokol/sokol_shared.c` | `FLAGS` |
| `shims/sokol/sokol_cosmo.c` | `FLAGS` |
| `deps/cimgui/*.cpp` | `FLAGS` |
| `shims/linux/gl.c` | `LINUX_FLAGS` |
| `shims/linux/x11.c` | `LINUX_FLAGS` |
| `nvapi/nvapi.c` | `WIN32_FLAGS` |
| `win32_tweaks.c` | `WIN32_FLAGS` |
| `main.c` | `FLAGS -Invapi` |

### Parallel Compilation (lines 42-44)
```sh
cat .build/commands | parallel $PARALLEL_FLAGS --max-procs $(nproc)
```

### Linking (lines 46-48)
```sh
objects=$(find .build -name '*.o' -not -path '*.aarch64/*')
cosmoc++ ${FLAGS} -o bin/cosmo-sokol $objects
```

---

## 6. Upstream Update Impact Analysis

### What Changes When Updating floooh/sokol

| Component | Impact | Action Required |
|-----------|--------|-----------------|
| **SOKOL_FUNCTIONS list** | HIGH | Must add/remove/modify function signatures in `gen-sokol` |
| **sokol_app.h API** | HIGH | New functions need dispatch entries |
| **sokol_gfx.h API** | HIGH | New functions need dispatch entries |
| **Internal implementation** | LOW | Automatic via header inclusion |
| **New backends** | MEDIUM | May need new platform files |

### What Changes When Updating jart/cosmopolitan

| Component | Impact | Action Required |
|-----------|--------|-----------------|
| **Win32 API coverage** | MEDIUM | May need fewer manual definitions in `sokol_windows.c` |
| **dlopen behavior** | LOW | Unlikely to break |
| **New platform detection** | LOW | `IsLinux()`, `IsWindows()`, `IsXnu()` stable |

### Automation Opportunities

1. **Parse sokol headers directly** instead of manual SOKOL_FUNCTIONS list
2. **Auto-detect missing Win32 definitions** by compiling with `-Werror=implicit-function-declaration`
3. **CI that compares function counts** between upstream sokol and gen-sokol list

---

## 7. File Reference Index

| File | Lines | Purpose |
|------|-------|---------|
| `shims/sokol/gen-sokol` | 267 | Python generator for dispatch layer |
| `shims/sokol/sokol_cosmo.c` | 3099 | Generated runtime dispatch (auto) |
| `shims/sokol/sokol_linux.h` | 199 | Generated prefix macros (auto) |
| `shims/sokol/sokol_linux.c` | 14 | Linux sokol backend |
| `shims/sokol/sokol_windows.h` | 199 | Generated prefix macros (auto) |
| `shims/sokol/sokol_windows.c` | 297+ | Windows sokol backend + Win32 defs |
| `shims/sokol/sokol_macos.h` | 199 | Generated prefix macros (auto) |
| `shims/sokol/sokol_macos.c` | 778 | macOS stub backend |
| `shims/sokol/sokol_shared.c` | 10 | Shared sokol code |
| `shims/linux/gen-x11` | 132 | Python X11 shim generator |
| `shims/linux/x11.c` | 500+ | Generated X11 shims (auto) |
| `shims/linux/gen-gl` | 95 | Python OpenGL shim generator |
| `shims/linux/gl.c` | 6172 | Generated GL shims (auto) |
| `build` | 52 | Build script |
| `main.c` | 119 | Demo application |

---

## 8. Key Observations for Upstream Sync

1. **SOKOL_FUNCTIONS is the bottleneck** — Any new sokol API function MUST be added here manually
2. **Windows definitions are fragile** — `sokol_windows.c` duplicates many Windows SDK structures
3. **macOS is non-functional** — Requires Objective-C runtime approach to implement
4. **dlopen pattern is robust** — System library shims work well and rarely break
5. **No version pinning exists** — Upstream sokol is a git submodule, not pinned to a release

---

## 9. Recommended Update Strategy

### For sokol upstream updates:

1. `cd deps/sokol && git pull origin master`
2. Diff `sokol_app.h` and `sokol_gfx.h` for new/changed public functions
3. Update `SOKOL_FUNCTIONS` list in `shims/sokol/gen-sokol`
4. Run `python shims/sokol/gen-sokol`
5. Build and test on Linux and Windows
6. Check for new undefined symbols → add to `gen-x11` or `sokol_windows.c`

### For cosmopolitan upstream updates:

1. Update cosmocc toolchain
2. Rebuild — usually "just works"
3. If new Win32 functions available in cosmopolitan, can simplify `sokol_windows.c`

---

*Generated by cosmo subagent for Swiss Rounds Round 1 analysis*
