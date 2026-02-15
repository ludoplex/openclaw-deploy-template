# Local File Discovery Report: cosmo-sokol-v3

**Agent:** localsearch  
**Round:** 1  
**Date:** 2026-02-09 18:08 MST  
**Goal:** Keep ludoplex/cosmo-sokol fork updated with upstream (floooh/sokol, bullno1/cosmo-sokol) without manual version pinning

---

## 1. Repository Architecture

### 1.1 Fork Relationships

```
floooh/sokol (upstream sokol headers)
    ↓ submodule
ludoplex/cosmo-sokol ← fork of ← bullno1/cosmo-sokol
    ↓ submodule
cimgui/cimgui (upstream imgui C bindings)
```

### 1.2 Git Remotes (C:\Users\user\cosmo-sokol)

| Remote | URL |
|--------|-----|
| origin | https://github.com/ludoplex/cosmo-sokol.git |
| upstream | https://github.com/bullno1/cosmo-sokol |

### 1.3 Submodule Pinned Commits

| Submodule | Commit SHA | Version Tag |
|-----------|------------|-------------|
| deps/sokol | `eaa1ca79a4004750e58cb51e0100d27f23e3e1ff` | gles2-951-geaa1ca7 |
| deps/cimgui | `8ec6558ecc9476c681d5d8c9f69597962045c2e6` | v1.65.4-662-g8ec6558 |

### 1.4 .gitmodules Content

```ini
[submodule "deps/sokol"]
    path = deps/sokol
    url = https://github.com/floooh/sokol.git

[submodule "deps/cimgui"]
    path = deps/cimgui
    url = https://github.com/cimgui/cimgui.git
```

---

## 2. File Inventory

### 2.1 Core Project Files (C:\Users\user\cosmo-sokol)

| File | Size | Purpose |
|------|------|---------|
| `main.c` | 3,991 bytes | cimgui demo entry point |
| `win32_tweaks.c` | 498 bytes | Windows console hide |
| `win32_tweaks.h` | 96 bytes | Header for above |
| `build` | ~2 KB | Main build script (shell) |
| `README.md` | 5,215 bytes | Documentation |
| `.github/workflows/build.yml` | 1,060 bytes | CI/CD workflow |

### 2.2 Generator Scripts (shims/sokol/)

| Script | Lines | Purpose |
|--------|-------|---------|
| `gen-sokol` | 347 lines | **CRITICAL:** Generates sokol_cosmo.c and platform headers |
| `gen-x11` | 180 lines | Generates X11 shim from undefined symbols |
| `gen-gl` | 94 lines | Generates OpenGL shim from gl.xml spec |

### 2.3 Platform Backend Files

| File | Size | Status |
|------|------|--------|
| `shims/sokol/sokol_cosmo.c` | 95,462 bytes | Runtime dispatch (189 functions) |
| `shims/sokol/sokol_linux.c` | 283 bytes | Linux backend include |
| `shims/sokol/sokol_linux.h` | 11,023 bytes | Linux function prefixes |
| `shims/sokol/sokol_windows.c` | 11,571 bytes | Windows backend |
| `shims/sokol/sokol_windows.h` | 11,411 bytes | Windows function prefixes |
| `shims/sokol/sokol_macos.c` | 22,481 bytes | **STUB** macOS backend |
| `shims/sokol/sokol_macos.h` | 11,023 bytes | macOS function prefixes |
| `shims/sokol/sokol_shared.c` | 209 bytes | Shared config |

### 2.4 Linux Shim Files

| File | Size | Purpose |
|------|------|---------|
| `shims/linux/gl.c` | 253,903 bytes | OpenGL function shims (auto-generated) |
| `shims/linux/x11.c` | 28,935 bytes | X11 function shims (auto-generated) |

### 2.5 Windows Extras

| File | Size | Purpose |
|------|------|---------|
| `nvapi/nvapi.c` | 5,624 bytes | NVIDIA threaded optimization disable |
| `nvapi/nvapi.h` | 148 bytes | Header |
| `nvapi/nvapi_decl.h` | 9,216 bytes | NVIDIA API declarations |
| `shims/win32/shellapi.h` | 0 bytes | Empty shim |
| `shims/win32/windowsx.h` | 0 bytes | Empty shim |

---

## 3. Function Dispatch Analysis

### 3.1 sokol_cosmo.c Dispatched Functions

**Total Functions:** 189

#### By API Module:
- **sokol_app (sapp_*)**: 64 functions
- **sokol_gfx (sg_*)**: 125 functions

#### Key Function Categories:

| Category | Count | Examples |
|----------|-------|----------|
| Window/Display | 20 | `sapp_width`, `sapp_height`, `sapp_dpi_scale` |
| Input | 12 | `sapp_mouse_shown`, `sapp_keyboard_shown` |
| Graphics Pipeline | 25 | `sg_make_pipeline`, `sg_apply_bindings` |
| Resources | 30 | `sg_make_buffer`, `sg_make_image`, `sg_make_shader` |
| Backend Queries | 35 | `sg_d3d11_*`, `sg_mtl_*`, `sg_wgpu_*`, `sg_gl_*` |
| Other | 67 | Misc lifecycle, state, debugging |

### 3.2 Runtime Dispatch Pattern

```c
// Example from sokol_cosmo.c
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

Uses Cosmopolitan's `IsLinux()`, `IsWindows()`, `IsXnu()` macros for platform detection.

---

## 4. Generator Script Analysis

### 4.1 gen-sokol Architecture

**Purpose:** Generate runtime dispatch code from function list

**Input:** Hardcoded `SOKOL_FUNCTIONS` list (189 entries)

**Output:**
1. `sokol_cosmo.c` - Runtime dispatch implementation
2. `sokol_linux.h` - `#define sapp_* linux_sapp_*` prefixes
3. `sokol_windows.h` - `#define sapp_* windows_sapp_*` prefixes
4. `sokol_macos.h` - `#define sapp_* macos_sapp_*` prefixes

**Critical Data Structure:**
```python
SOKOL_FUNCTIONS = [
    "bool sapp_isvalid()",
    "int sapp_width()",
    # ... 187 more ...
    "sg_gl_attachments_info sg_gl_query_attachments_info(sg_attachments atts)",
]
```

### 4.2 Auto-Update Blockers

**Current Problem:** The `SOKOL_FUNCTIONS` list is **manually maintained**.

When upstream floooh/sokol adds new API functions:
1. Developer must notice the change
2. Manually add new function signatures to `gen-sokol`
3. Re-run `gen-sokol` to regenerate dispatch code

**Solution for Auto-Updates:**

Extract functions from sokol headers using pattern:
```
SOKOL_APP_API_DECL <return_type> <function_name>(<params>);
SOKOL_GFX_API_DECL <return_type> <function_name>(<params>);
```

### 4.3 gen-x11 and gen-gl Patterns

**gen-x11:** Uses undefined reference extraction:
```bash
./build 2>&1 | grep -i 'undefined reference' | awk -F'`|'"'" '{print $2}' | sort -u
```

**gen-gl:** Parses OpenGL XML spec:
```python
tree = ET.parse("gl.xml")
for feature in root.findall('./feature[@api="gl"]'):
    # Extract commands for GL 4.0+
```

---

## 5. Upstream Diff Analysis

### 5.1 ludoplex/cosmo-sokol vs bullno1/cosmo-sokol

```diff
README.md                   |   64 ++-
build                       |   12 +
shims/macos/README.md       |   74 +++  (NEW)
shims/sokol/gen-sokol       |   45 +-
shims/sokol/sokol_cosmo.c   |  840 +++  (expanded for macOS)
shims/sokol/sokol_linux.h   |    2 +
shims/sokol/sokol_macos.c   | 1015 +++  (NEW - stub)
shims/sokol/sokol_macos.h   |  196 +++     (NEW)
shims/sokol/sokol_windows.h |    2 +
───────────────────────────────────────────
9 files changed, 2,231 insertions(+), 19 deletions(-)
```

**Key Additions in ludoplex fork:**
1. macOS stub implementation
2. 3-platform dispatch in gen-sokol
3. Enhanced documentation

### 5.2 Upstream sokol Gap

| Repository | Latest Commit | cosmo-sokol Pinned |
|------------|---------------|-------------------|
| floooh/sokol | `d48aa2f` (iOS fix) | `eaa1ca79` |
| bullno1/cosmo-sokol | `5656716` | N/A (is upstream) |

---

## 6. Sokol Headers in deps/sokol

### 6.1 Core Headers

| Header | Size | Lines (approx) |
|--------|------|----------------|
| `sokol_app.h` | 495,005 bytes | ~11,500 |
| `sokol_gfx.h` | 906,784 bytes | ~19,000 |
| `sokol_audio.h` | 107,199 bytes | ~2,500 |
| `sokol_fetch.h` | 120,383 bytes | ~2,700 |
| `sokol_glue.h` | 5,786 bytes | ~130 |
| `sokol_log.h` | 12,528 bytes | ~300 |
| `sokol_time.h` | 11,373 bytes | ~280 |
| `sokol_args.h` | 27,565 bytes | ~720 |

### 6.2 Utility Headers (deps/sokol/util/)

| Header | Size | Purpose |
|--------|------|---------|
| `sokol_imgui.h` | 190,393 bytes | ImGui integration |
| `sokol_gl.h` | 230,629 bytes | Immediate mode GL |
| `sokol_debugtext.h` | 267,453 bytes | Debug text rendering |
| `sokol_shape.h` | 57,516 bytes | Shape generation |
| `sokol_spine.h` | 320,254 bytes | Spine animation |
| `sokol_gfx_imgui.h` | 199,199 bytes | GFX debug UI |
| `sokol_fontstash.h` | 136,728 bytes | Font rendering |
| `sokol_nuklear.h` | 166,637 bytes | Nuklear UI |
| `sokol_color.h` | 58,698 bytes | Color utilities |
| `sokol_memtrack.h` | 5,286 bytes | Memory tracking |

---

## 7. cimgui Submodule

### 7.1 Key Files

| File | Size | Purpose |
|------|------|---------|
| `cimgui.h` | 224,433 bytes | C bindings header |
| `imgui/imgui.h` | 376,674 bytes | Core ImGui C++ header |
| `imgui/imgui_internal.h` | 271,906 bytes | Internal API |

---

## 8. Recommendations for Auto-Update System

### 8.1 Required Changes for Upstream Sync

1. **Auto-extract SOKOL_FUNCTIONS:**
   ```python
   # Parse sokol_app.h and sokol_gfx.h for:
   # SOKOL_APP_API_DECL <signature>;
   # SOKOL_GFX_API_DECL <signature>;
   import re
   pattern = r'SOKOL_(?:APP|GFX)_API_DECL\s+(.+?);'
   ```

2. **Create version manifest file:**
   ```yaml
   # version.yaml
   sokol:
     commit: eaa1ca79a4004750e58cb51e0100d27f23e3e1ff
     tag: gles2-951
   cimgui:
     commit: 8ec6558ecc9476c681d5d8c9f69597962045c2e6
     tag: v1.65.4-662
   ```

3. **CI workflow additions:**
   - Weekly check for upstream changes
   - Auto-regenerate dispatch code
   - Run build verification
   - Create PR if changes detected

### 8.2 Key Files to Monitor

| Upstream Repo | Files to Watch |
|---------------|----------------|
| floooh/sokol | `sokol_app.h`, `sokol_gfx.h` API changes |
| bullno1/cosmo-sokol | All shims/* changes |
| cimgui/cimgui | `cimgui.h` API changes |

### 8.3 Auto-Update Pipeline

```
┌────────────────────────────────────────────────────────┐
│ 1. Fetch upstream/sokol latest                         │
│ 2. Extract SOKOL_*_API_DECL from sokol_app.h/gfx.h    │
│ 3. Compare with current SOKOL_FUNCTIONS list           │
│ 4. If new functions: update gen-sokol, regenerate      │
│ 5. Update submodule commit                             │
│ 6. Build test                                          │
│ 7. Create PR if successful                             │
└────────────────────────────────────────────────────────┘
```

---

## 9. Statistics Summary

| Metric | Value |
|--------|-------|
| Total dispatched functions | 189 |
| sokol_app functions | 64 |
| sokol_gfx functions | 125 |
| Platform backends | 3 (Linux, Windows, macOS-stub) |
| Generator scripts | 3 (gen-sokol, gen-x11, gen-gl) |
| Fork additions vs upstream | +2,231 lines |
| Submodule commits pinned | 2 |
| CI workflows | 1 |

---

## 10. Files Critical for Version Pinning

| File | Current State | Auto-Update Need |
|------|---------------|------------------|
| `.gitmodules` | URLs only, no version | Add branch/tag tracking |
| `shims/sokol/gen-sokol` | Manual function list | Auto-extract from headers |
| `deps/sokol` (submodule) | Pinned to eaa1ca79 | Needs update to latest |
| `deps/cimgui` (submodule) | Pinned to 8ec6558e | Needs update to latest |

---

*Report generated by localsearch agent for Swiss Rounds v3*
