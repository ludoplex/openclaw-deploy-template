# Local File Discovery Report: cosmo-sokol-v3

**Agent:** localsearch  
**Round:** 1  
**Date:** 2026-02-09 18:31 MST  
**Goal:** Keep ludoplex/cosmo-sokol fork actively maintained and current with upstream (floooh/sokol, jart/cosmopolitan)

---

## 1. Repository Architecture

### 1.1 Source Locations (from state.json)

| Source | Repo | Local Path | Type |
|--------|------|------------|------|
| sokol-upstream | floooh/sokol | C:\cosmo-sokol\deps\sokol | source (submodule) |
| cosmo-sokol-fork | ludoplex/cosmo-sokol | C:\cosmo-sokol | source |

### 1.2 Git Configuration

**Current Commit:** `028aafa` — "Update README with macOS support documentation and platform table"

**Remotes:**
| Remote | URL |
|--------|-----|
| origin | https://github.com/ludoplex/cosmo-sokol.git |
| upstream | https://github.com/bullno1/cosmo-sokol.git |

### 1.3 Submodule Status

| Submodule | Path | Commit SHA | Version Tag |
|-----------|------|------------|-------------|
| sokol | deps/sokol | `eaa1ca79a4004750e58cb51e0100d27f23e3e1ff` | gles2-951-geaa1ca7 |
| cimgui | deps/cimgui | `8ec6558ecc9476c681d5d8c9f69597962045c2e6` | v1.65.4-662-g8ec6558 |

### 1.4 .gitmodules

```ini
[submodule "deps/sokol"]
    path = deps/sokol
    url = https://github.com/floooh/sokol.git

[submodule "deps/cimgui"]
    path = deps/cimgui
    url = https://github.com/cimgui/cimgui.git
```

---

## 2. Complete File Inventory

### 2.1 Root Project Files

| File | Size (bytes) | Purpose |
|------|--------------|---------|
| `main.c` | 3,991 | cimgui demo entry point with tri-platform dispatch |
| `build` | 1,844 | Main shell build script using cosmocc |
| `win32_tweaks.c` | 498 | Windows console hide implementation |
| `win32_tweaks.h` | 96 | Header for win32_tweaks |
| `README.md` | 5,321 | Documentation with platform table |
| `LICENSE` | 1,235 | License file |
| `.gitmodules` | 183 | Submodule definitions |
| `.gitignore` | 15 | Git ignore rules |
| `.clangd` | 141 | Clangd configuration |

**Total Root Files:** 9

### 2.2 Shims Directory Structure

#### shims/sokol/ (Platform Dispatch Layer)

| File | Size (bytes) | Purpose | Generated? |
|------|--------------|---------|------------|
| `gen-sokol` | 15,768 | Python generator for dispatch code | Source |
| `sokol_cosmo.c` | 95,462 | Runtime dispatch (189 functions × 3 platforms) | ✅ Generated |
| `sokol_linux.h` | 11,023 | `#define sapp_* linux_sapp_*` prefixes | ✅ Generated |
| `sokol_linux.c` | 283 | Linux backend include wrapper | Source |
| `sokol_windows.h` | 11,411 | `#define sapp_* windows_sapp_*` prefixes | ✅ Generated |
| `sokol_windows.c` | 11,571 | Windows backend with Win32 type definitions | Source |
| `sokol_macos.h` | 11,023 | `#define sapp_* macos_sapp_*` prefixes | ✅ Generated |
| `sokol_macos.c` | 23,496 | macOS stub implementation (all 189 functions) | Source |
| `sokol_shared.c` | 209 | Shared sokol_log and sokol_glue includes | Source |

#### shims/linux/ (X11 & OpenGL Shims)

| File | Size (bytes) | Purpose | Generated? |
|------|--------------|---------|------------|
| `gen-x11` | 10,208 | Python generator for X11 dlopen shims | Source |
| `gen-gl` | 3,442 | Python generator for OpenGL shims from gl.xml | Source |
| `parse-x11` | 105 | Helper script for X11 parsing | Source |
| `x11.c` | 28,935 | X11 function shims (59 functions) | ✅ Generated |
| `gl.c` | 253,903 | OpenGL function shims | ✅ Generated |
| `gl.xml` | 2,804,602 | OpenGL registry specification | Source |
| `GL/` | (symlink) | OpenGL headers directory | - |
| `KHR/` | (symlink) | Khronos headers directory | - |
| `X11/` | (symlink) | X11 headers directory | - |

#### shims/macos/

| File | Size (bytes) | Purpose |
|------|--------------|---------|
| `README.md` | 2,305 | macOS implementation documentation |

#### shims/win32/ (Empty Shim Headers)

| File | Size (bytes) | Purpose |
|------|--------------|---------|
| `shellapi.h` | 0 | Empty shim for missing header |
| `windowsx.h` | 0 | Empty shim for missing header |

### 2.3 nvapi/ (NVIDIA Windows Optimization)

| File | Size (bytes) | Purpose |
|------|--------------|---------|
| `nvapi.c` | 5,624 | NVIDIA threaded optimization disable |
| `nvapi.h` | 148 | Header |
| `nvapi_decl.h` | 9,216 | NVIDIA API declarations |

### 2.4 deps/sokol/ (Upstream Sokol Headers)

| Header | Purpose |
|--------|---------|
| `sokol_app.h` | Application/window abstraction |
| `sokol_gfx.h` | Graphics API abstraction |
| `sokol_audio.h` | Audio playback |
| `sokol_fetch.h` | Async file fetching |
| `sokol_glue.h` | sokol_app + sokol_gfx integration |
| `sokol_log.h` | Logging |
| `sokol_time.h` | Timing utilities |
| `sokol_args.h` | Argument parsing |

### 2.5 deps/sokol/util/ (Utility Headers)

| Header | Purpose |
|--------|---------|
| `sokol_imgui.h` | ImGui integration |
| `sokol_gl.h` | Immediate mode OpenGL API |
| `sokol_debugtext.h` | Debug text rendering |
| `sokol_shape.h` | Shape generation |
| `sokol_spine.h` | Spine animation |
| `sokol_gfx_imgui.h` | GFX debugging UI |
| `sokol_fontstash.h` | Font rendering |
| `sokol_nuklear.h` | Nuklear UI integration |
| `sokol_color.h` | Color utilities |
| `sokol_memtrack.h` | Memory tracking |
| `gen_sokol_color.py` | Color header generator |

### 2.6 CI/CD

| File | Path | Purpose |
|------|------|---------|
| `build.yml` | `.github/workflows/` | GitHub Actions CI workflow |

---

## 3. Function Manifest

### 3.1 Dispatched sokol_app Functions (64 total)

Extracted from `gen-sokol` SOKOL_FUNCTIONS list:

| Function | Signature | Line in gen-sokol |
|----------|-----------|-------------------|
| `sapp_isvalid` | `bool sapp_isvalid()` | 10 |
| `sapp_width` | `int sapp_width()` | 11 |
| `sapp_widthf` | `float sapp_widthf()` | 12 |
| `sapp_height` | `int sapp_height()` | 13 |
| `sapp_heightf` | `float sapp_heightf()` | 14 |
| `sapp_color_format` | `int sapp_color_format()` | 15 |
| `sapp_depth_format` | `int sapp_depth_format()` | 16 |
| `sapp_sample_count` | `int sapp_sample_count()` | 17 |
| `sapp_high_dpi` | `bool sapp_high_dpi()` | 18 |
| `sapp_dpi_scale` | `float sapp_dpi_scale()` | 19 |
| `sapp_show_keyboard` | `void sapp_show_keyboard(bool show)` | 20 |
| `sapp_keyboard_shown` | `bool sapp_keyboard_shown()` | 21 |
| `sapp_is_fullscreen` | `bool sapp_is_fullscreen()` | 22 |
| `sapp_toggle_fullscreen` | `void sapp_toggle_fullscreen()` | 23 |
| `sapp_show_mouse` | `void sapp_show_mouse(bool show)` | 24 |
| `sapp_mouse_shown` | `bool sapp_mouse_shown()` | 25 |
| `sapp_lock_mouse` | `void sapp_lock_mouse(bool lock)` | 26 |
| `sapp_mouse_locked` | `bool sapp_mouse_locked()` | 27 |
| `sapp_set_mouse_cursor` | `void sapp_set_mouse_cursor(sapp_mouse_cursor cursor)` | 28 |
| `sapp_get_mouse_cursor` | `sapp_mouse_cursor sapp_get_mouse_cursor()` | 29 |
| `sapp_userdata` | `void* sapp_userdata()` | 30 |
| `sapp_query_desc` | `sapp_desc sapp_query_desc()` | 31 |
| `sapp_request_quit` | `void sapp_request_quit()` | 32 |
| `sapp_cancel_quit` | `void sapp_cancel_quit()` | 33 |
| `sapp_quit` | `void sapp_quit()` | 34 |
| `sapp_consume_event` | `void sapp_consume_event()` | 35 |
| `sapp_frame_count` | `uint64_t sapp_frame_count()` | 36 |
| `sapp_frame_duration` | `double sapp_frame_duration()` | 37 |
| `sapp_set_clipboard_string` | `void sapp_set_clipboard_string(const char* str)` | 38 |
| `sapp_get_clipboard_string` | `const char* sapp_get_clipboard_string()` | 39 |
| `sapp_set_window_title` | `void sapp_set_window_title(const char* str)` | 40 |
| `sapp_set_icon` | `void sapp_set_icon(const sapp_icon_desc* icon_desc)` | 41 |
| `sapp_get_num_dropped_files` | `int sapp_get_num_dropped_files()` | 42 |
| `sapp_get_dropped_file_path` | `const char* sapp_get_dropped_file_path(int index)` | 43 |
| `sapp_run` | `void sapp_run(const sapp_desc* desc)` | 44 |
| `sapp_egl_get_display` | `const void* sapp_egl_get_display()` | 45 |
| `sapp_egl_get_context` | `const void* sapp_egl_get_context()` | 46 |
| `sapp_html5_ask_leave_site` | `void sapp_html5_ask_leave_site(bool ask)` | 47 |
| `sapp_html5_get_dropped_file_size` | `uint32_t sapp_html5_get_dropped_file_size(int index)` | 48 |
| `sapp_html5_fetch_dropped_file` | `void sapp_html5_fetch_dropped_file(const sapp_html5_fetch_request* request)` | 49 |
| `sapp_metal_get_device` | `const void* sapp_metal_get_device()` | 50 |
| `sapp_metal_get_current_drawable` | `const void* sapp_metal_get_current_drawable()` | 51 |
| `sapp_metal_get_depth_stencil_texture` | `const void* sapp_metal_get_depth_stencil_texture()` | 52 |
| `sapp_metal_get_msaa_color_texture` | `const void* sapp_metal_get_msaa_color_texture()` | 53 |
| `sapp_macos_get_window` | `const void* sapp_macos_get_window()` | 54 |
| `sapp_ios_get_window` | `const void* sapp_ios_get_window()` | 55 |
| `sapp_d3d11_get_device` | `const void* sapp_d3d11_get_device()` | 56 |
| `sapp_d3d11_get_device_context` | `const void* sapp_d3d11_get_device_context()` | 57 |
| `sapp_d3d11_get_swap_chain` | `const void* sapp_d3d11_get_swap_chain()` | 58 |
| `sapp_d3d11_get_render_view` | `const void* sapp_d3d11_get_render_view()` | 59 |
| `sapp_d3d11_get_resolve_view` | `const void* sapp_d3d11_get_resolve_view()` | 60 |
| `sapp_d3d11_get_depth_stencil_view` | `const void* sapp_d3d11_get_depth_stencil_view()` | 61 |
| `sapp_win32_get_hwnd` | `const void* sapp_win32_get_hwnd()` | 62 |
| `sapp_wgpu_get_device` | `const void* sapp_wgpu_get_device()` | 63 |
| `sapp_wgpu_get_render_view` | `const void* sapp_wgpu_get_render_view()` | 64 |
| `sapp_wgpu_get_resolve_view` | `const void* sapp_wgpu_get_resolve_view()` | 65 |
| `sapp_wgpu_get_depth_stencil_view` | `const void* sapp_wgpu_get_depth_stencil_view()` | 66 |
| `sapp_gl_get_framebuffer` | `uint32_t sapp_gl_get_framebuffer()` | 67 |
| `sapp_gl_get_major_version` | `int sapp_gl_get_major_version()` | 68 |
| `sapp_gl_get_minor_version` | `int sapp_gl_get_minor_version()` | 69 |
| `sapp_android_get_native_activity` | `const void* sapp_android_get_native_activity()` | 70 |

### 3.2 Dispatched sokol_gfx Functions (125 total)

Key categories from `gen-sokol`:

**Setup/Shutdown:**
- `sg_setup`, `sg_shutdown`, `sg_isvalid`, `sg_reset_state_cache`

**Resource Creation:**
- `sg_make_buffer`, `sg_make_image`, `sg_make_sampler`, `sg_make_shader`, `sg_make_pipeline`, `sg_make_attachments`

**Resource Destruction:**
- `sg_destroy_buffer`, `sg_destroy_image`, `sg_destroy_sampler`, `sg_destroy_shader`, `sg_destroy_pipeline`, `sg_destroy_attachments`

**Resource Updates:**
- `sg_update_buffer`, `sg_update_image`, `sg_append_buffer`, `sg_query_buffer_overflow`, `sg_query_buffer_will_overflow`

**Render Pass:**
- `sg_begin_pass`, `sg_apply_viewport`, `sg_apply_viewportf`, `sg_apply_scissor_rect`, `sg_apply_scissor_rectf`
- `sg_apply_pipeline`, `sg_apply_bindings`, `sg_apply_uniforms`, `sg_draw`, `sg_end_pass`, `sg_commit`

**Query Functions:**
- `sg_query_desc`, `sg_query_backend`, `sg_query_features`, `sg_query_limits`, `sg_query_pixelformat`
- `sg_query_*_state`, `sg_query_*_info`, `sg_query_*_desc`, `sg_query_*_defaults`

**Allocation/Init (Deferred):**
- `sg_alloc_*`, `sg_dealloc_*`, `sg_init_*`, `sg_uninit_*`, `sg_fail_*`

**Frame Stats:**
- `sg_enable_frame_stats`, `sg_disable_frame_stats`, `sg_frame_stats_enabled`, `sg_query_frame_stats`

**Backend-Specific:**
- `sg_d3d11_*` (8 functions)
- `sg_mtl_*` (7 functions)
- `sg_wgpu_*` (10 functions)
- `sg_gl_*` (5 functions)

### 3.3 X11 Shim Functions (59 total)

From `shims/linux/gen-x11`:

**Core X11 (53 functions):**
- `XOpenDisplay`, `XCloseDisplay`, `XFlush`, `XNextEvent`, `XPending`
- `XInitThreads`, `XFilterEvent`, `XSync`, `XrmInitialize`
- `XChangeProperty`, `XSendEvent`, `XFree`, `XSetErrorHandler`
- `XConvertSelection`, `XLookupString`, `XGetEventData`, `XFreeEventData`
- `XGetWindowProperty`, `XMapWindow`, `XUnmapWindow`, `XRaiseWindow`
- `XGetWindowAttributes`, `XAllocSizeHints`, `XCheckTypedWindowEvent`
- `XCreateColormap`, `XCreateFontCursor`, `XCreateWindow`
- `XWarpPointer`, `XDefineCursor`, `XDestroyWindow`
- `XFreeColormap`, `XFreeCursor`, `XGetKeyboardMapping`
- `XGetSelectionOwner`, `XGrabPointer`, `XInternAtom`, `XInternAtoms`
- `XSetSelectionOwner`, `XSetWMNormalHints`, `XSetWMProtocols`
- `XUndefineCursor`, `XUngrabPointer`, `Xutf8SetWMProperties`
- `XkbSetDetectableAutoRepeat`, `XkbFreeKeyboard`, `XkbFreeNames`
- `XResourceManagerString`, `XrmDestroyDatabase`, `XrmGetResource`
- `XkbGetMap`, `XkbGetNames`, `XrmGetStringDatabase`, `XQueryExtension`

**Xcursor (6 functions):**
- `XcursorGetDefaultSize`, `XcursorGetTheme`, `XcursorImageCreate`
- `XcursorImageDestroy`, `XcursorImageLoadCursor`, `XcursorLibraryLoadImage`

**XInput2 (2 functions):**
- `XIQueryVersion`, `XISelectEvents`

### 3.4 OpenGL Shim Functions

Generated from `gl.xml` for OpenGL 4.0+. Full list in `shims/linux/gl.c` (253 KB).

---

## 4. Platform Configurations

### 4.1 gen-sokol Platform Definitions

```python
PLATFORMS = [
    {"name": "linux", "check": "IsLinux", "enabled": True},
    {"name": "windows", "check": "IsWindows", "enabled": True},
    {"name": "macos", "check": "IsXnu", "enabled": True},
]
```

### 4.2 Runtime Dispatch Pattern

From `sokol_cosmo.c`:

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

### 4.3 Platform Backend Status

| Platform | Backend File | Size | Status | Graphics |
|----------|--------------|------|--------|----------|
| Linux | `sokol_linux.c` | 283 B | ✅ Full | OpenGL via dlopen |
| Windows | `sokol_windows.c` | 11,571 B | ✅ Full | OpenGL via WGL |
| macOS | `sokol_macos.c` | 23,496 B | 🚧 Stub | Planned: objc_msgSend |

---

## 5. Key Data Structures

### 5.1 main.c Application State

```c
typedef struct {
    uint64_t last_time;
    bool show_test_window;
    bool show_another_window;
    sg_pass_action pass_action;
} state_t;
```

**File:** `main.c:17-22`

### 5.2 Windows Type Definitions (sokol_windows.c)

**Critical Win32 structures defined inline:**

| Structure | Lines | Purpose |
|-----------|-------|---------|
| `LARGE_INTEGER` | 17-28 | 64-bit integer union |
| `RECT` | 30-35 | Rectangle coordinates |
| `POINT` | 37-40 | Point coordinates |
| `MSG` | 42-50 | Message struct |
| `PIXELFORMATDESCRIPTOR` | 76-99 | Pixel format |
| `MONITORINFO` | 103-108 | Monitor info |
| `RAWINPUTDEVICE` | 117-122 | Raw input device |
| `TRACKMOUSEEVENT` | 169-174 | Mouse tracking |
| `RAWMOUSE/RAWKEYBOARD/RAWINPUT` | 183-219 | Raw input data |
| `WNDCLASSW` | 224-235 | Window class |
| `BITMAPV5HEADER` | 268-293 | Bitmap header |
| `ICONINFO` | 307-312 | Icon info |

### 5.3 NVAPI Structures

From `nvapi/nvapi_decl.h`:
- `NVDRS_PROFILE`
- `NVDRS_APPLICATION`
- `NVDRS_SETTING`
- `NvDRSSessionHandle`
- `NvDRSProfileHandle`

---

## 6. Build System Analysis

### 6.1 Build Script Flags

From `build` script:

```bash
FLAGS="-I deps/sokol \
    -I deps/cimgui \
    -mcosmo \
    -mtiny \
    -Wall \
    -Werror"

LINUX_FLAGS="${FLAGS} -Ishims/linux"
WIN32_FLAGS="${FLAGS} -Ishims/win32 -I ${COSMO_HOME}/include/libc/nt"
MACOS_FLAGS="${FLAGS}"
```

### 6.2 Compilation Units

| Category | Files | Purpose |
|----------|-------|---------|
| Platform Backends | `sokol_linux.c`, `sokol_windows.c`, `sokol_macos.c` | Platform sokol |
| Dispatch | `sokol_shared.c`, `sokol_cosmo.c` | Runtime dispatch |
| ImGui | 6 cpp files in deps/cimgui | Dear ImGui |
| System Shims | `gl.c`, `x11.c` | Linux dlopen shims |
| Windows | `nvapi.c`, `win32_tweaks.c` | NVIDIA + console |
| Application | `main.c` | Entry point |

### 6.3 CI/CD Workflow

From `.github/workflows/build.yml`:
- Builds on push to any branch
- Uses cosmopolitan toolchain
- Single cross-platform binary output

---

## 7. Upstream Sync Analysis

### 7.1 What Needs Tracking

| Upstream | Key Files to Monitor | Current Pinned |
|----------|---------------------|----------------|
| floooh/sokol | `sokol_app.h`, `sokol_gfx.h` API declarations | eaa1ca79 |
| bullno1/cosmo-sokol | All shims/* changes | N/A (is upstream) |
| cimgui/cimgui | `cimgui.h` API changes | 8ec6558e |
| jart/cosmopolitan | `cosmo.h`, `windowsesque.h` | Not tracked as submodule |

### 7.2 Auto-Detection Pattern for API Changes

From sokol headers:
```
SOKOL_APP_API_DECL <return_type> <function_name>(<params>);
SOKOL_GFX_API_DECL <return_type> <function_name>(<params>);
```

**Extraction regex:**
```python
pattern = r'SOKOL_(?:APP|GFX)_API_DECL\s+(.+?);'
```

### 7.3 gen-sokol Limitation

**Current:** `SOKOL_FUNCTIONS` list is **manually maintained** (189 entries hardcoded)

**Impact:** When upstream adds new API functions:
1. Build won't fail (no undefined references)
2. New functions won't be dispatched
3. Calling new functions from user code → link error

**Solution Required:** Auto-extract function signatures from headers before regenerating dispatch code.

---

## 8. Statistics Summary

| Metric | Value |
|--------|-------|
| Total project files | 423 |
| Root source files | 9 |
| Shim files | 21 |
| Dispatched sokol functions | 189 |
| sokol_app functions | 64 |
| sokol_gfx functions | 125 |
| X11 shim functions | 59 |
| Platform backends | 3 |
| Generator scripts | 3 |
| Submodules | 2 |
| CI workflows | 1 |

---

## 9. Files Critical for Upstream Sync

| File | Role | Auto-Update Need |
|------|------|------------------|
| `.gitmodules` | Submodule URLs | Add version tracking |
| `shims/sokol/gen-sokol` | Manual function list | Auto-extract from headers |
| `deps/sokol` (submodule) | Pinned commit | Regular updates |
| `deps/cimgui` (submodule) | Pinned commit | Regular updates |
| `shims/linux/gen-x11` | Manual function list | Keep in sync with build errors |
| `shims/linux/gen-gl` | Uses gl.xml | Update gl.xml periodically |

---

## 10. Domain-Specific Recommendations

### 10.1 For Automated Updates

1. **Create API extraction script:**
   - Parse `deps/sokol/sokol_app.h` and `deps/sokol/sokol_gfx.h`
   - Extract all `SOKOL_*_API_DECL` lines
   - Compare with current `SOKOL_FUNCTIONS` list
   - Output diff for human review or auto-update

2. **Version manifest file:**
   ```yaml
   # version.yaml
   sokol:
     commit: eaa1ca79a4004750e58cb51e0100d27f23e3e1ff
     version: gles2-951
     last_checked: 2026-02-09
   cimgui:
     commit: 8ec6558ecc9476c681d5d8c9f69597962045c2e6
     version: v1.65.4-662
     last_checked: 2026-02-09
   ```

3. **CI additions:**
   - Weekly upstream check job
   - API diff generation
   - Automated PR creation for updates

### 10.2 For macOS Implementation

The stub in `sokol_macos.c` documents the path forward:

1. **objc_msgSend pattern:**
   ```c
   void* libobjc = cosmo_dlopen("/usr/lib/libobjc.dylib", RTLD_NOW);
   id app = objc_msgSend(objc_getClass("NSApplication"), 
                         sel_registerName("sharedApplication"));
   ```

2. **Key Cocoa classes needed:**
   - `NSApplication`, `NSWindow`, `NSOpenGLView`
   - `NSAutoreleasePool`, `NSEvent`

3. **Alternative: GLFW via C bindings** (if objc_msgSend proves impractical)

---

## 11. Cross-Agent Feedback

*No other specialist reports available in Round 1. Awaiting peer reports for cross-reading.*

---

## 12. Enlightened Proposal: Local File Discovery Work Items

After comprehensive enumeration of the repository structure, functions, and data types, I propose the following concrete work items for maintaining upstream sync:

### 12.1 Create `scripts/extract-sokol-api.py`

**Purpose:** Automatically extract function signatures from upstream sokol headers

**Input:** `deps/sokol/sokol_app.h`, `deps/sokol/sokol_gfx.h`

**Output:** JSON file with all public API functions

**Implementation:**
```python
#!/usr/bin/env python3
import re
import json

def extract_api(header_path, api_prefix):
    """Extract SOKOL_*_API_DECL functions from header."""
    pattern = rf'{api_prefix}_API_DECL\s+(.+?);'
    with open(header_path) as f:
        content = f.read()
    return re.findall(pattern, content, re.MULTILINE)

if __name__ == "__main__":
    sapp_funcs = extract_api("deps/sokol/sokol_app.h", "SOKOL_APP")
    sg_funcs = extract_api("deps/sokol/sokol_gfx.h", "SOKOL_GFX")
    
    manifest = {
        "sokol_app": sapp_funcs,
        "sokol_gfx": sg_funcs,
        "total": len(sapp_funcs) + len(sg_funcs)
    }
    
    with open("scripts/sokol-api-manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
```

**File location:** `scripts/extract-sokol-api.py`

### 12.2 Create `scripts/check-upstream.py`

**Purpose:** Compare current SOKOL_FUNCTIONS against extracted API, report drift

**Implementation notes:**
- Parse `gen-sokol` SOKOL_FUNCTIONS list
- Compare with output of extract-sokol-api.py
- Report: added functions, removed functions, signature changes
- Exit non-zero if drift detected (for CI integration)

**File location:** `scripts/check-upstream.py`

### 12.3 Create `version.yaml` Manifest

**Purpose:** Track pinned versions for all dependencies

```yaml
# version.yaml - Dependency version tracking
dependencies:
  sokol:
    repo: floooh/sokol
    commit: eaa1ca79a4004750e58cb51e0100d27f23e3e1ff
    tag: gles2-951-geaa1ca7
    api_count: 189
    last_synced: 2026-02-09
    
  cimgui:
    repo: cimgui/cimgui
    commit: 8ec6558ecc9476c681d5d8c9f69597962045c2e6
    tag: v1.65.4-662-g8ec6558
    last_synced: 2026-02-09
    
  cosmopolitan:
    note: "Not a submodule - installed via cosmocc"
    min_version: "3.9.5"

upstream:
  bullno1/cosmo-sokol:
    last_merged: null
    fork_divergence: "+2231 lines (macOS support)"
```

**File location:** `version.yaml` (project root)

### 12.4 Modify `gen-sokol` for Auto-Extraction Mode

**Current state:** Hardcoded SOKOL_FUNCTIONS list (lines 8-197)

**Proposed change:** Add `--extract` flag that reads from sokol headers:

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--extract', action='store_true', 
                    help='Extract functions from sokol headers instead of hardcoded list')
args = parser.parse_args()

if args.extract:
    SOKOL_FUNCTIONS = extract_from_headers()
else:
    SOKOL_FUNCTIONS = [...]  # existing hardcoded list
```

This allows:
- `./gen-sokol` — use existing list (safe, known-good)
- `./gen-sokol --extract` — regenerate from headers (for updates)

### 12.5 Create File Watcher Index

**Purpose:** Catalog all files that need monitoring for upstream changes

**Format:** `scripts/watch-manifest.json`

```json
{
  "critical_paths": [
    {
      "path": "deps/sokol/sokol_app.h",
      "watch": ["SOKOL_APP_API_DECL"],
      "triggers": ["gen-sokol regeneration"]
    },
    {
      "path": "deps/sokol/sokol_gfx.h", 
      "watch": ["SOKOL_GFX_API_DECL"],
      "triggers": ["gen-sokol regeneration"]
    },
    {
      "path": "deps/cimgui/cimgui.h",
      "watch": ["CIMGUI_API"],
      "triggers": ["build verification"]
    }
  ],
  "generated_files": [
    "shims/sokol/sokol_cosmo.c",
    "shims/sokol/sokol_linux.h",
    "shims/sokol/sokol_windows.h",
    "shims/sokol/sokol_macos.h",
    "shims/linux/x11.c",
    "shims/linux/gl.c"
  ]
}
```

### 12.6 Priority Order

| Priority | Item | Effort | Impact |
|----------|------|--------|--------|
| 1 | `extract-sokol-api.py` | Low | High — enables automation |
| 2 | `version.yaml` | Low | Medium — tracking visibility |
| 3 | `check-upstream.py` | Medium | High — drift detection |
| 4 | `gen-sokol --extract` | Medium | High — auto-regeneration |
| 5 | `watch-manifest.json` | Low | Medium — documentation |

---

*Report generated by localsearch agent — Local File Discovery for Swiss Rounds v3*

---

# Round 2 — Refined Proposal

**Date:** 2026-02-09 18:48 MST  
**Status:** Acknowledging triad feedback, refining contribution

---

## R2.1 Triad Feedback Analysis

### What the Triad Determined

| My Proposal | Triad Decision | New Owner |
|-------------|----------------|-----------|
| `scripts/extract-sokol-api.py` | Duplicate (1 of 6 identical) | testcov |
| `version.yaml` | Use `cosmo-sokol.json` instead | dbeng |
| `scripts/check-upstream.py` | Consolidated into unified workflow | cicd |
| `gen-sokol --extract` modification | Part of API sync work | testcov |
| `scripts/watch-manifest.json` | Not claimed | **localsearch** (retained) |

**Solution Document §8 Assessment:** *"localsearch: (merged into testcov/dbeng — no unique deliverables)"*

### Accepting the Critique

The triad correctly identified that my primary proposals duplicated work from other specialists. Specifically:

1. **6 agents proposed the same API extraction script** — My version was one of many. testcov's is most complete.
2. **3 agents proposed version manifests** — dbeng's JSON schema is superior to my YAML.
3. **4 agents proposed sync workflows** — cicd owns the consolidated version.

My Round 1 contribution was **valuable as reference material** (comprehensive file inventory, function manifest, structure documentation) but my proposed *work items* overlapped with better-positioned specialists.

---

## R2.2 Refined Contribution: File Integrity & Discovery Support

After reviewing the consolidated solution, I identify **two unique capabilities** localsearch can provide:

### R2.2.1 Pre-Generation File Validation

**Problem Identified by Critique §1.1-1.5:** Regex extraction can fail silently if source files are missing, corrupted, or formatted unexpectedly.

**Localsearch Contribution:** Create a pre-check script that validates file existence and format before any generator runs:

```python
#!/usr/bin/env python3
"""scripts/validate-source-files.py - Pre-generation validation"""

import sys
from pathlib import Path

REQUIRED_FILES = {
    "deps/sokol/sokol_app.h": {
        "min_size": 100000,  # sokol_app.h is ~120KB
        "must_contain": ["SOKOL_APP_API_DECL", "sapp_run"]
    },
    "deps/sokol/sokol_gfx.h": {
        "min_size": 200000,  # sokol_gfx.h is ~280KB
        "must_contain": ["SOKOL_GFX_API_DECL", "sg_setup"]
    },
    "shims/sokol/gen-sokol": {
        "min_size": 10000,
        "must_contain": ["SOKOL_FUNCTIONS", "PLATFORMS"]
    }
}

def validate():
    errors = []
    for path, checks in REQUIRED_FILES.items():
        p = Path(path)
        if not p.exists():
            errors.append(f"MISSING: {path}")
            continue
        
        size = p.stat().st_size
        if size < checks["min_size"]:
            errors.append(f"TOO SMALL: {path} ({size} < {checks['min_size']})")
        
        content = p.read_text(errors='ignore')
        for marker in checks["must_contain"]:
            if marker not in content:
                errors.append(f"MISSING MARKER '{marker}' in {path}")
    
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1
    
    print("All source files validated")
    return 0

if __name__ == "__main__":
    sys.exit(validate())
```

**Integration Point:** CI runs this BEFORE testcov's `check-api-sync.py`.

---

### R2.2.2 Watch Manifest for Change Detection

**Unique Proposal Retained from Round 1:** `scripts/watch-manifest.json`

This file catalogs ALL files that matter for upstream sync, enabling:
- Pre-commit hooks to check if generators need re-running
- CI to skip unnecessary work if unrelated files changed
- Documentation for maintainers

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "cosmo-sokol Watch Manifest",
  "description": "Files to monitor for upstream sync",
  
  "source_files": {
    "sokol_headers": [
      {"path": "deps/sokol/sokol_app.h", "watch_patterns": ["SOKOL_APP_API_DECL"]},
      {"path": "deps/sokol/sokol_gfx.h", "watch_patterns": ["SOKOL_GFX_API_DECL"]},
      {"path": "deps/sokol/sokol_audio.h", "watch_patterns": ["SOKOL_AUDIO_API_DECL"]},
      {"path": "deps/sokol/sokol_fetch.h", "watch_patterns": ["SOKOL_FETCH_API_DECL"]}
    ],
    "cimgui_headers": [
      {"path": "deps/cimgui/cimgui.h", "watch_patterns": ["CIMGUI_API"]}
    ]
  },
  
  "generator_scripts": [
    {"path": "shims/sokol/gen-sokol", "outputs": ["sokol_cosmo.c", "sokol_*.h"]},
    {"path": "shims/linux/gen-x11", "outputs": ["x11.c"]},
    {"path": "shims/linux/gen-gl", "outputs": ["gl.c"]}
  ],
  
  "generated_files": [
    {"path": "shims/sokol/sokol_cosmo.c", "generator": "gen-sokol"},
    {"path": "shims/sokol/sokol_linux.h", "generator": "gen-sokol"},
    {"path": "shims/sokol/sokol_windows.h", "generator": "gen-sokol"},
    {"path": "shims/sokol/sokol_macos.h", "generator": "gen-sokol"},
    {"path": "shims/linux/x11.c", "generator": "gen-x11"},
    {"path": "shims/linux/gl.c", "generator": "gen-gl"}
  ],
  
  "triggers": {
    "submodule_update": ["source_files", "generator_scripts"],
    "generator_modified": ["generated_files"],
    "header_api_change": ["generated_files"]
  }
}
```

---

### R2.2.3 Binary Symbol Verification (New Proposal)

**Unique Capability:** localsearch can extract and verify symbols from compiled binaries.

**Use Case:** After build, verify that all dispatched functions actually exist in the binary:

```bash
#!/bin/bash
# scripts/verify-symbols.sh - Post-build symbol verification

BINARY="${1:-bin/cosmo-sokol}"

if [ ! -f "$BINARY" ]; then
    echo "ERROR: Binary not found: $BINARY"
    exit 1
fi

# Extract expected symbols from sokol_cosmo.c
EXPECTED=$(grep -oP '(?<=^bool |^void |^int |^float |^uint32_t |^uint64_t |^double |^const void\* |^sapp_\w+ |^sg_\w+ )\w+(?=\()' shims/sokol/sokol_cosmo.c | sort -u)

# Extract actual symbols from binary
ACTUAL=$(nm "$BINARY" 2>/dev/null | grep ' T ' | awk '{print $3}' | sort -u)

# Check for missing symbols
MISSING=0
for sym in $EXPECTED; do
    if ! echo "$ACTUAL" | grep -q "^${sym}$"; then
        echo "MISSING SYMBOL: $sym"
        MISSING=$((MISSING + 1))
    fi
done

if [ $MISSING -gt 0 ]; then
    echo "ERROR: $MISSING expected symbols not found in binary"
    exit 1
fi

echo "All $(echo "$EXPECTED" | wc -l) expected symbols found in binary"
exit 0
```

**Integration Point:** CI runs this AFTER successful build, before smoke test.

---

## R2.3 Revised Ownership Matrix

After triad consolidation, localsearch's role changes from "proposer" to "supporter":

| Deliverable | Primary Owner | localsearch Role |
|-------------|---------------|------------------|
| API sync script | testcov | Reference: File locations |
| cosmo-sokol.json | dbeng | Reference: File inventory |
| Upstream workflow | cicd | **Contributor:** validate-source-files.py |
| Watch manifest | **localsearch** | Primary owner |
| Symbol verification | **localsearch** | Primary owner |
| Pre-generation checks | **localsearch** | Primary owner |

---

## R2.4 Integration with Triad Solution

Mapping my refined proposals to the Triad's Minimum Viable Path:

| Triad MVP Item | localsearch Contribution |
|----------------|-------------------------|
| 1. Add `--headless` to main.c | None (testcov) |
| 2. Add dlopen error handling | None (cosmo) |
| 3. Fix regex (whitespace normalize) | **Pre-validation**: Ensure headers exist before regex runs |
| 4. Consolidate sync workflows | **Watch manifest**: Define which files trigger sync |
| 5. Explicit bash shell in Windows CI | None (neteng) |
| 6. Remove Wine, use Windows runners | None (neteng) |
| 7. Pin Python to 3.11 | None (cicd) |

---

## R2.5 Updated Priority Order

| Priority | Item | Effort | Impact | Unique to localsearch? |
|----------|------|--------|--------|------------------------|
| 1 | `validate-source-files.py` | 30min | Medium — prevents silent failures | ✅ Yes |
| 2 | `watch-manifest.json` | 1hr | Medium — enables smart CI triggers | ✅ Yes |
| 3 | `verify-symbols.sh` | 30min | Low — post-build sanity check | ✅ Yes |

**Total unique effort:** ~2 hours
**Total value added:** Prevents several failure modes identified in Critique §1, §4

---

## R2.6 Acceptance of Consolidation

I accept the triad's assessment that my core proposals overlapped with other specialists. The value of Round 1 was the **comprehensive file inventory** and **function manifest**, which serve as reference material for:

- testcov's API extraction script
- dbeng's metadata schema
- asm's ABI verification
- cicd's workflow configuration

For Round 2 and beyond, my contribution shifts to:

1. **Validation and verification** — ensuring files exist and are valid before other scripts run
2. **Symbol verification** — post-build checks using local file analysis tools
3. **Reference documentation** — maintaining the file/function inventory

This is appropriate for the localsearch domain: **local file system search and validation**, not API parsing or CI orchestration.

---

## R2.7 Checklist for Round 3

- [ ] Create `scripts/validate-source-files.py` 
- [ ] Create `scripts/watch-manifest.json`
- [ ] Create `scripts/verify-symbols.sh`
- [ ] Verify integration points with testcov, cicd
- [ ] Update file inventory if repository structure changes

---

*Round 2 refinement complete — localsearch agent*
*Accepting triad consolidation, focusing on unique validation capabilities*
