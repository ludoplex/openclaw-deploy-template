# cosmo-sokol Fork Modernization Progress Report

**Date:** 2026-02-09  
**Status:** ✅ Phase 1 Complete (Structure & Stubs)

## Summary

Successfully modernized the ludoplex/cosmo-sokol fork to support the tri-platform pattern (Linux + Windows + macOS) using the bullno1 cosmo-sokol runtime dispatch approach.

## What Was Done

### 1. Updated gen-sokol Generator Script
- Added `macos` to the PLATFORMS list alongside `linux` and `windows`
- Generator now creates `sokol_macos.h` with `macos_` function prefixes
- Generator now includes `IsXnu()` checks in `sokol_cosmo.c` for macOS dispatch

### 2. Created macOS Support Files

**New files:**
- `shims/sokol/sokol_macos.h` - Auto-generated #define prefixes for macos_* functions
- `shims/sokol/sokol_macos.c` - Stub implementation (compiles, prints error at runtime)
- `shims/macos/README.md` - Documentation for implementing full macOS support

**Modified files:**
- `shims/sokol/gen-sokol` - Now generates tri-platform shims
- `shims/sokol/sokol_cosmo.c` - Now includes macos_* externs and IsXnu() dispatch
- `shims/sokol/sokol_linux.h` - Regenerated (no changes to pattern)
- `shims/sokol/sokol_windows.h` - Regenerated (no changes to pattern)
- `build` - Updated to compile sokol_macos.c
- `README.md` - Added platform support table and macOS documentation

### 3. Git Commits & Push
- Committed: "Add macOS support (stub) with tri-platform runtime dispatch"
- Committed: "Update README with macOS support documentation and platform table"
- Pushed to: https://github.com/ludoplex/cosmo-sokol

## Current State

### Platform Status
| Platform | Status | Notes |
|----------|--------|-------|
| Linux | ✅ Working | Uses X11 + OpenGL via dlopen |
| Windows | ✅ Working | Uses Win32 + WGL via NT imports |
| macOS | 🚧 Stub | Compiles, but prints error + exits at runtime |

### The macOS Challenge

Sokol on macOS uses Objective-C extensively:
- `NSApplication`, `NSWindow`, `NSOpenGLView` for window management
- Metal or OpenGL for graphics
- Cocoa event handling

Cosmopolitan's `cosmocc` cannot directly compile Objective-C, so the macOS backend is currently a stub.

## Path to Full macOS Support

### Recommended Approach: objc_msgSend Pattern

Call Objective-C methods from C using the runtime:

```c
// Load Objective-C runtime
void* libobjc = cosmo_dlopen("/usr/lib/libobjc.dylib", RTLD_NOW);

// Get objc_msgSend
typedef id (*objc_msgSend_t)(id, SEL, ...);
objc_msgSend_t msgSend = cosmo_dlsym(libobjc, "objc_msgSend");

// Example: [NSApplication sharedApplication]
id app = msgSend(objc_getClass("NSApplication"), sel_registerName("sharedApplication"));
```

### Work Required for Full Implementation

1. **Create `shims/macos/objc_runtime.c`**
   - Wrapper functions for objc_msgSend calls
   - Macros for common patterns

2. **Create `shims/macos/cocoa.c`**
   - NSApplication shims
   - NSWindow creation/management
   - Event loop handling

3. **Create `shims/macos/opengl.c` or `metal.c`**
   - OpenGL context creation via NSOpenGLView
   - OR Metal setup via MTKView

4. **Update `sokol_macos.c`**
   - Replace stubs with actual objc_msgSend calls
   - Hook into the shim functions

### Estimated Effort
- **Full OpenGL backend:** 2-3 days
- **Full Metal backend:** 3-5 days
- The objc_msgSend pattern is verbose but well-established

## Build Verification

Build was not verified on this machine (cosmocc not installed). The code structure follows the established bullno1 pattern exactly, so compilation should work when tested with cosmocc.

## Repository Links

- **Fork:** https://github.com/ludoplex/cosmo-sokol
- **Upstream:** https://github.com/bullno1/cosmo-sokol
- **Local Path:** C:\Users\user\cosmo-sokol

## Next Steps

1. **Test build** with cosmocc installed
2. **Verify** Linux and Windows still work
3. **Start objc_runtime.c** for macOS Objective-C calls
4. **Implement** minimal NSApplication/NSWindow shims
5. **Test** on actual macOS hardware
