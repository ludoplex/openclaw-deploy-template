# MHI Procurement Architecture Refactoring Plan

**Created:** 2026-02-09 00:45 MST  
**Status:** Analysis Complete - Cleanup Required  
**Author:** CICD Agent (overnight autonomous mission)

## Executive Summary

**GOOD NEWS:** The correct cosmo-sokol pattern is ALREADY IMPLEMENTED in mhi-procurement!

The project has migrated to the correct architecture, but deprecated code remains. This is a **cleanup task**, not a full refactor.

---

## Current Architecture Analysis

### Directory Structure

```
C:\mhi-procurement\
├── helpers/                    # ❌ DEPRECATED - Old DSO pattern
│   ├── DEPRECATED.md          # Already marked deprecated!
│   ├── gui_linux.c            # Standalone Linux helper DSO
│   ├── gui_windows.c          # Standalone Windows helper DSO
│   ├── gui_macos.m            # Standalone macOS helper DSO
│   └── *.obj                  # Build artifacts
│
├── shims/                      # ✅ CORRECT - cosmo-sokol pattern
│   ├── sokol/
│   │   ├── sokol_linux.c      # Linux Sokol with linux_ prefix
│   │   ├── sokol_linux.h      # #define sapp_run linux_sapp_run
│   │   ├── sokol_windows.c    # Windows Sokol with windows_ prefix
│   │   ├── sokol_windows.h    # #define sapp_run windows_sapp_run
│   │   ├── sokol_cosmo.c      # Runtime dispatcher (IsWindows()/IsLinux())
│   │   ├── sokol_shared.c     # sokol_log, sokol_glue (platform-agnostic)
│   │   ├── sokol_imgui_impl.c # ImGui integration
│   │   └── gen-sokol          # Generator script
│   ├── linux/
│   │   ├── x11.c              # X11 dlopen stubs
│   │   ├── gl.c               # OpenGL dlopen stubs
│   │   ├── gen-x11, gen-gl    # Generator scripts
│   │   ├── X11/               # Header shims
│   │   ├── GL/                # Header shims
│   │   └── KHR/               # Header shims
│   └── win32/
│       ├── shellapi.h         # Win32 header shims
│       └── windowsx.h
│
├── src/
│   ├── gui_main.c             # ✅ Uses sapp_run() → dispatched at runtime
│   ├── gui_interface.h        # ⚠️ OLD DSO interface - may be unused
│   ├── ui/gui.c               # Application GUI code
│   └── ui/sokol_imgui_impl.c  # ImGui impl
│
├── artifacts/                  # ❌ Contains old DSO artifacts
│   ├── helper-linux/libgui.so
│   ├── helper-windows/libgui.dll
│   └── helper-macos/libgui.dylib
│
├── scripts/
│   └── build-cosmo-gui.sh     # ✅ Correct build script
│
└── Makefile                    # ⚠️ Has both patterns!
```

---

## Architecture Diagrams

### Current State (WRONG - helpers/ pattern still exists)

```
┌────────────────────────────────────────────────────────────────────┐
│                    CURRENT STATE (Dual Patterns)                   │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Pattern 1 (CORRECT - Active):                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  mhi-procurement-gui.com (APE)                              │  │
│  │  ├── gui_main.c → sapp_run() → sokol_cosmo.c dispatcher    │  │
│  │  ├── sokol_linux.o (linux_sapp_run, linux_sg_setup, ...)   │  │
│  │  ├── sokol_windows.o (windows_sapp_run, windows_sg_*, ...) │  │
│  │  ├── x11.o, gl.o (dlopen stubs for system libs)            │  │
│  │  └── CImGui/ImGui linked in                                 │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                    │
│  Pattern 2 (DEPRECATED - Should be deleted):                       │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  APE binary + separate DSOs                                 │  │
│  │  ├── mhi-procurement.com (loads DSO via cosmo_dlopen)      │  │
│  │  ├── libgui.so (built from helpers/gui_linux.c)            │  │
│  │  ├── libgui.dll (built from helpers/gui_windows.c)         │  │
│  │  └── libgui.dylib (built from helpers/gui_macos.m)         │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### Target State (After Cleanup)

```
┌────────────────────────────────────────────────────────────────────┐
│                      TARGET STATE (Clean)                          │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Single APE Binary (cosmo-sokol pattern):                          │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  mhi-procurement-gui.com                                    │  │
│  │  ┌─────────────────────────────────────────────────────────┐│  │
│  │  │                    Application Layer                    ││  │
│  │  │  gui_main.c → gui.c → database.c                       ││  │
│  │  ├─────────────────────────────────────────────────────────┤│  │
│  │  │                    Sokol Dispatcher                     ││  │
│  │  │  sokol_cosmo.c: sapp_run() → {linux,windows}_sapp_run()││  │
│  │  ├───────────────────────┬─────────────────────────────────┤│  │
│  │  │   sokol_linux.o       │    sokol_windows.o              ││  │
│  │  │   - linux_sapp_*      │    - windows_sapp_*             ││  │
│  │  │   - linux_sg_*        │    - windows_sg_*               ││  │
│  │  │   - OpenGL backend    │    - D3D11 or OpenGL backend    ││  │
│  │  ├───────────────────────┴─────────────────────────────────┤│  │
│  │  │                    dlopen Stubs                          ││  │
│  │  │  x11.c, gl.c → Load libX11.so, libGL.so from HOST       ││  │
│  │  └─────────────────────────────────────────────────────────┘│  │
│  │                                                              │  │
│  │  Dependencies: NONE (single file, runs everywhere)          │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                    │
│  Runtime on Linux:                                                 │
│    IsLinux() → linux_sapp_run() → x11.c → dlopen("libX11.so")    │
│                                                                    │
│  Runtime on Windows:                                               │
│    IsWindows() → windows_sapp_run() → Win32 API (NT imports)     │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Migration Guide

### Phase 1: Delete Deprecated Files

| Action | Path | Reason |
|--------|------|--------|
| DELETE | `helpers/gui_linux.c` | Old DSO helper |
| DELETE | `helpers/gui_windows.c` | Old DSO helper |
| DELETE | `helpers/gui_macos.m` | Old DSO helper |
| DELETE | `helpers/DEPRECATED.md` | No longer needed |
| DELETE | `helpers/*.obj` | Build artifacts |
| DELETE | `helpers/` directory | Empty after above |

```bash
# Commands
rm -rf helpers/
```

### Phase 2: Clean Artifact Directory

| Action | Path | Reason |
|--------|------|--------|
| DELETE | `artifacts/helper-linux/libgui.so` | Old DSO |
| DELETE | `artifacts/helper-windows/libgui.dll` | Old DSO |
| DELETE | `artifacts/helper-macos/libgui.dylib` | Old DSO |
| DELETE | `artifacts/helper-linux/` | Empty directory |
| DELETE | `artifacts/helper-windows/` | Empty directory |
| DELETE | `artifacts/helper-macos/` | Empty directory |

```bash
# Commands
rm -rf artifacts/helper-*/
```

### Phase 3: Evaluate gui_interface.h

**Current file:** `src/gui_interface.h`

This file defines the DSO interface for the OLD helper pattern:
- `mhi_gui_init()`, `mhi_gui_run()`, `mhi_gui_shutdown()`
- `mhi_gui_callbacks_t` callback struct for database access
- `MHI_GUI_EXPORT` macros

**Action needed:**
- Check if any code still uses this interface
- If not referenced, DELETE
- If referenced, refactor to remove DSO indirection

```bash
# Check references
grep -r "gui_interface.h" src/
grep -r "mhi_gui_init" src/
grep -r "mhi_gui_callbacks" src/
```

### Phase 4: Clean Makefile

**Remove these targets:**

```makefile
# DELETE: gui-linux, gui-windows, gui-macos targets
gui-linux: ...
gui-windows: ...
gui-macos: ...

# DELETE: embed-helpers, dist-single, verify-single
embed-helpers: ...
dist-single: ...
verify-single: ...
list-embedded: ...
test-embedded: ...

# DELETE: GUI_LINUX, GUI_WINDOWS, GUI_MACOS variables
GUI_LINUX      := $(DIST_DIR)/libmhi_gui.so
GUI_WINDOWS    := $(DIST_DIR)/mhi_gui.dll
GUI_MACOS      := $(DIST_DIR)/libmhi_gui.dylib

# DELETE: HELPERS_DIR variable
HELPERS_DIR    := helpers
```

**Keep these (correct pattern):**

```makefile
# KEEP: cosmo-gui target (the correct build)
cosmo-gui: $(APE_GUI_BINARY)

# KEEP: All GUI_OBJS and their compilation rules
GUI_OBJS := \
    $(GUI_BUILD_DIR)/sokol_windows.o \
    $(GUI_BUILD_DIR)/sokol_linux.o \
    ...
```

### Phase 5: Update CI/CD Workflow

The current `.github/workflows/build.yml` is already correct:
- Uses `ape-gui` job with `scripts/build-cosmo-gui.sh`
- Does NOT build helper DSOs

**Optional cleanup:**
- Remove any references to `helper-*` artifacts in other workflows
- Check `security.yml` and `sanitizers.yml` for deprecated references

### Phase 6: Update Documentation

Update these files:
- `README.md` - Remove references to DLLs/helpers
- `docs/ARCHITECTURE.md` - Confirm single-APE pattern is documented
- `AGENT_DISCOURSE.md` - Remove DLL discussion if present

---

## Files Summary

### Files to DELETE

```
helpers/gui_linux.c
helpers/gui_windows.c
helpers/gui_macos.m
helpers/DEPRECATED.md
helpers/*.obj (any build artifacts)
helpers/ (directory)

artifacts/helper-linux/libgui.so
artifacts/helper-windows/libgui.dll
artifacts/helper-macos/libgui.dylib
artifacts/helper-linux/
artifacts/helper-windows/
artifacts/helper-macos/

src/gui_interface.h (if unused)
```

### Files to MODIFY

```
Makefile
  - Remove: gui-linux, gui-windows, gui-macos targets
  - Remove: embed-helpers, dist-single targets
  - Remove: HELPERS_DIR, GUI_LINUX, GUI_WINDOWS, GUI_MACOS variables
  - Keep: cosmo-gui target and all shims/ compilation rules

README.md
  - Update to reflect single-binary architecture

docs/ARCHITECTURE.md (if exists)
  - Ensure it documents the correct pattern
```

### Files to KEEP (Already Correct)

```
shims/sokol/sokol_linux.c
shims/sokol/sokol_linux.h
shims/sokol/sokol_windows.c
shims/sokol/sokol_windows.h
shims/sokol/sokol_cosmo.c
shims/sokol/sokol_shared.c
shims/sokol/gen-sokol
shims/linux/x11.c
shims/linux/gl.c
shims/linux/gen-x11
shims/linux/gen-gl
shims/linux/X11/
shims/linux/GL/
shims/win32/

src/gui_main.c
src/ui/gui.c
src/ui/sokol_imgui_impl.c

scripts/build-cosmo-gui.sh
.github/workflows/build.yml
nvapi/nvapi.c (NVIDIA fix for Windows)
```

---

## CI/CD Workflow Changes

Current workflow (`.github/workflows/build.yml`) is CORRECT:

```yaml
ape-gui:
  name: APE Binary (GUI)
  runs-on: ubuntu-latest
  steps:
    # ... setup ...
    - name: Build GUI APE (cosmo-sokol pattern)
      run: |
        chmod +x scripts/build-cosmo-gui.sh
        bash scripts/build-cosmo-gui.sh
```

**No changes needed to CI/CD.** The deprecated helper builds were never added to CI.

---

## Verification Checklist

After cleanup, verify:

- [ ] `make cosmo-gui` still builds successfully
- [ ] `scripts/build-cosmo-gui.sh` still works
- [ ] No references to `helpers/` remain in codebase
- [ ] No references to `libgui.so`, `libgui.dll`, `libgui.dylib` remain
- [ ] No references to `gui_interface.h` remain (if deleted)
- [ ] No references to `mhi_gui_init`, `mhi_gui_run`, `mhi_gui_callbacks` remain
- [ ] CI build still passes
- [ ] Binary runs on both Windows and Linux

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Breaking build | Low | High | Test `make cosmo-gui` after each deletion |
| Orphaned references | Low | Medium | Use grep to find all references first |
| Needed interface deleted | Low | Medium | Check if gui_interface.h is referenced |

---

## Notes

1. **The migration was already done** - someone (likely Vincent or prior CI work) already implemented the cosmo-sokol pattern in `shims/`. The old `helpers/` code was marked deprecated but not removed.

2. **The DEPRECATED.md file confirms intent** - The project owner already knew these files should be removed.

3. **CI is already correct** - The GitHub Actions workflow only builds the single APE, not the helpers.

4. **macOS is not yet supported** - The cosmo-sokol pattern in mhi-procurement only has Linux and Windows shims. macOS would need Metal shims similar to the reference implementation.

---

## Comparison with Reference Implementation

| Component | cosmo-sokol-ref | mhi-procurement | Match? |
|-----------|-----------------|-----------------|--------|
| sokol_linux.c | ✅ | ✅ | ✓ |
| sokol_windows.c | ✅ | ✅ | ✓ |
| sokol_cosmo.c | ✅ | ✅ | ✓ (identical) |
| sokol_shared.c | ✅ | ✅ | ✓ |
| x11.c stubs | ✅ | ✅ | ✓ |
| gl.c stubs | ✅ | ✅ | ✓ |
| gen-sokol script | ✅ | ✅ | ✓ |
| Separate DSOs | ❌ (none) | ❌ (deprecated) | ✓ |
| nvapi (NVIDIA fix) | ✅ | ✅ | ✓ |
| win32_tweaks | ✅ | ✅ | ✓ |

The implementations match. Cleanup is the only remaining task.

---

## Conclusion

**mhi-procurement has already migrated to the correct cosmo-sokol pattern.**

The remaining work is cleanup:
1. Delete deprecated `helpers/` directory
2. Clean up `artifacts/` of old DSOs
3. Remove deprecated Makefile targets
4. Optionally remove `src/gui_interface.h` if unused

Estimated effort: **30 minutes** of careful file deletion and Makefile editing.

---

*End of refactoring plan.*
