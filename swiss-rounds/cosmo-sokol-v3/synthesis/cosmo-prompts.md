# Stage Prompts: cosmo

**Specialist:** cosmo  
**Total Stages:** 4

---

## Stage 1: check-api-sync.c Implementation

### Prompt

```
You are the cosmo specialist implementing tools/check-api-sync.c for the cosmo-sokol project.

CONTEXT:
- cosmo-sokol is a Cosmopolitan libc fork of floooh/sokol
- The sokol submodule is 1,032 commits behind upstream
- Philosophy: Pure C/APE binaries, no Python, no external dependencies

TASK:
Implement tools/check-api-sync.c that:
1. Reads deps/sokol/sokol_app.h, deps/sokol/sokol_gfx.h, shims/include/gen-sokol.h
2. Extracts function declarations from SOKOL_APP_API_DECL and SOKOL_GFX_API_DECL
3. Extracts gen_sapp_* and gen_sg_* function declarations from gen-sokol.h
4. Compares signatures (function name, return type, parameter types)
5. Reports mismatches and exits with code 1 if any found

CRITICAL FIXES TO INCLUDE:
1. strip_inline_comments_from_sig() - Handle multi-line declarations with embedded comments
2. Minimum file size check - Empty/corrupted files should fail (sokol_app.h should be >100KB)
3. normalize_pointer_spaces() - "const void*" and "const void *" are equivalent

OUTPUT FORMAT:
✅ API in sync
   sokol_app: 61 functions
   sokol_gfx: 103 functions
   gen-sokol: 164 functions

Or on mismatch:
❌ API MISMATCH DETECTED
   MISSING: sapp_new_function (in header, not in gen-sokol)
   CHANGED: sg_apply_uniforms
     Header: void sg_apply_uniforms(int ub_slot, const sg_range* data)
     Gen:    void sg_apply_uniforms(sg_shader_stage stage, int ub_index, const sg_range* data)

EXIT CODES:
- 0: Sync OK
- 1: Mismatch detected
- 2: File error

COMPILE WITH:
cosmocc -o check-api-sync check-api-sync.c

Provide the complete implementation.
```

---

## Stage 2: validate-sources.c Implementation

### Prompt

```
You are the cosmo specialist implementing tools/validate-sources.c for the cosmo-sokol project.

CONTEXT:
- This tool runs before the main build to catch missing/corrupted files early
- Must work as APE binary on Linux, Windows, macOS
- No external dependencies

TASK:
Implement tools/validate-sources.c that:
1. Checks existence of required source files
2. Validates minimum file sizes (guards against empty/corrupted)
3. Verifies expected content markers (e.g., sokol headers contain version macro)
4. Reports issues clearly and exits non-zero on failure

REQUIRED FILES TO CHECK:
```c
{"shims/include/gen-sokol.h", 5000, "gen_sapp_"},
{"deps/sokol/sokol_app.h", 100000, "SOKOL_APP_API_DECL"},
{"deps/sokol/sokol_gfx.h", 200000, "SOKOL_GFX_API_DECL"},
{"deps/sokol/sokol_glue.h", 5000, "SOKOL_GLUE_API_DECL"},
```

OUTPUT FORMAT:
✅ All source files valid
   shims/include/gen-sokol.h: 45,230 bytes, marker found
   deps/sokol/sokol_app.h: 156,789 bytes, marker found
   deps/sokol/sokol_gfx.h: 312,456 bytes, marker found
   deps/sokol/sokol_glue.h: 8,901 bytes, marker found

Or on error:
❌ VALIDATION FAILED
   deps/sokol/sokol_app.h: File missing or size 0 (expected >100KB)
   Hint: Run 'git submodule update --init --recursive'

EXIT CODES:
- 0: All valid
- 1: Validation failed
- 2: Internal error

Provide the complete implementation.
```

---

## Stage 3: cosmo_dl_safe.h Implementation

### Prompt

```
You are the cosmo specialist implementing shims/include/cosmo_dl_safe.h for the cosmo-sokol project.

CONTEXT:
- Cosmopolitan's dlopen() requires platform-aware library hints
- cosmo_dltramp() must wrap function pointers for cross-platform calls
- This header standardizes safe dlopen patterns across the codebase

TASK:
Implement shims/include/cosmo_dl_safe.h with:

1. Platform detection helpers (IsLinux, IsWindows, IsMacOS wrappers)
2. Library hint resolution by platform
3. Safe loading macros with error handling

REQUIRED MACROS:
```c
// Load library with platform hints
COSMO_DL_LOAD_LIB(handle_var, lib_name, required)
// required=true: exit(1) on failure
// required=false: set handle to NULL on failure

// Load symbol with dltramp wrapping
COSMO_DL_LOAD_SYM(handle, sym_ptr, sym_name, required)

// Load optional symbol (no error on missing)
COSMO_DL_LOAD_SYM_OPT(handle, sym_ptr, sym_name)

// Cleanup
COSMO_DL_UNLOAD_LIB(handle_var)
```

PLATFORM HINTS TABLE:
| Library | Linux | macOS | Windows |
|---------|-------|-------|---------|
| X11 | libX11.so.6:libX11.so | - | - |
| GL | libGL.so.1:libGL.so | OpenGL.framework/OpenGL | opengl32.dll |
| Xlib funcs | libX11.so.6 | - | - |
| Xi | libXi.so.6:libXi.so | - | - |
| Xcursor | libXcursor.so.1 | - | - |

INCLUDE GUARD:
#ifndef COSMO_DL_SAFE_H
#define COSMO_DL_SAFE_H

DEPENDENCIES:
#include <cosmo.h>       // IsLinux(), etc.
#include <dlfcn.h>       // dlopen, dlsym, dlclose
#include <stdio.h>       // fprintf
#include <stdlib.h>      // exit
#include <string.h>      // strcmp

Provide the complete header implementation.
```

---

## Stage 4: x11.c Update

### Prompt

```
You are the cosmo specialist updating shims/linux/x11.c to use the new cosmo_dl_safe.h macros.

CONTEXT:
- x11.c currently uses raw dlopen/dlsym calls
- These need to be replaced with safe macros for consistency and error handling
- The cosmo_dl_safe.h header is now available

TASK:
Update shims/linux/x11.c to:
1. Include cosmo_dl_safe.h
2. Replace dlopen() calls with COSMO_DL_LOAD_LIB()
3. Replace dlsym() calls with COSMO_DL_LOAD_SYM() or COSMO_DL_LOAD_SYM_OPT()
4. Ensure all function pointers are wrapped with dltramp via the macros

EXAMPLE TRANSFORMATION:
```c
// BEFORE:
void* x11_lib = dlopen("libX11.so.6", RTLD_NOW);
if (!x11_lib) x11_lib = dlopen("libX11.so", RTLD_NOW);
if (!x11_lib) { fprintf(stderr, "Failed to load X11\n"); return; }

XOpenDisplay_fn = dlsym(x11_lib, "XOpenDisplay");
XCloseDisplay_fn = dlsym(x11_lib, "XCloseDisplay");

// AFTER:
#include "cosmo_dl_safe.h"

void* x11_lib = NULL;
COSMO_DL_LOAD_LIB(x11_lib, "X11", true);  // Required, exit on failure

COSMO_DL_LOAD_SYM(x11_lib, XOpenDisplay_fn, "XOpenDisplay", true);
COSMO_DL_LOAD_SYM(x11_lib, XCloseDisplay_fn, "XCloseDisplay", true);
```

REVIEW CHECKLIST:
- [ ] All dlopen() replaced with COSMO_DL_LOAD_LIB
- [ ] All dlsym() replaced with COSMO_DL_LOAD_SYM or COSMO_DL_LOAD_SYM_OPT
- [ ] No raw cosmo_dltramp() calls (handled by macros)
- [ ] Error handling consistent

Provide the updated x11.c implementation (or a diff if the file is large).
```

---

## Verification Commands

After all stages:

```bash
cd C:\cosmo-sokol

# Build tools
cd tools
cosmocc -o check-api-sync check-api-sync.c
cosmocc -o validate-sources validate-sources.c

# Test tools
./check-api-sync
echo "Exit code: $?"

./validate-sources
echo "Exit code: $?"

# Verify x11.c compiles
cd ../shims/linux
cosmocc -c x11.c -I../include
```

---

*cosmo Stage Prompts Complete*
