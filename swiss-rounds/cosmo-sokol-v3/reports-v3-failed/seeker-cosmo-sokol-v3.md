# Seeker Report: cosmo-sokol-v3 — Round 1
**Date:** 2026-02-09
**Domain:** Web resource discovery (documentation, issues, PRs, release notes)
**Goal:** Keep ludoplex/cosmo-sokol fork updated with upstream (floooh/sokol, bullno1/cosmo-sokol) without manual version pinning.

---

## Executive Summary

The cosmo-sokol project is a clever integration of the **sokol** minimal C headers library with **Cosmopolitan Libc** to create truly portable executables that run natively on Linux, Windows, and (work-in-progress) macOS. The challenge is maintaining three layers of dependencies:

1. **floooh/sokol** (very active upstream) — The source graphics/app library
2. **bullno1/cosmo-sokol** (upstream fork) — The Cosmopolitan integration layer
3. **ludoplex/cosmo-sokol** (our fork) — Adds macOS support structure

**Key Finding:** Sokol is under active development with frequent breaking changes and new features. An automated sync strategy is essential for long-term maintainability.

---

## Repository Analysis

### 1. floooh/sokol (Primary Upstream)

**URL:** https://github.com/floooh/sokol

**Project Description:**
- Simple STB-style cross-platform libraries for C and C++
- Core headers: `sokol_gfx.h`, `sokol_app.h`, `sokol_time.h`, `sokol_audio.h`, `sokol_fetch.h`, `sokol_args.h`, `sokol_log.h`
- Utility headers: `sokol_imgui.h`, `sokol_nuklear.h`, `sokol_gl.h`, `sokol_fontstash.h`, `sokol_debugtext.h`, etc.
- Supports: GL/GLES3/WebGL2 + Metal + D3D11 + WebGPU + **experimental Vulkan**

**Release Strategy:**
- No formal releases or tags — uses rolling releases via master branch
- All changes documented in `CHANGELOG.md`
- Very active: multiple commits per week

**Recent Changelog Highlights (2026):**

| Date | Change | Impact on cosmo-sokol |
|------|--------|----------------------|
| 08-Feb-2026 | iOS/Metal drawable size mismatch fix | Low (iOS-specific) |
| 03-Feb-2026 | Vulkan backend fixes (Windows) | Medium (potential future target) |
| 01-Feb-2026 | Vulkan frame-sync validation fixes | Medium |
| 26-Jan-2026 | **Dual-source-blending support added** | **High** — new feature flag |
| 24-Jan-2026 | Vulkan debug labels, Intel performance fix | Low-Medium |
| 19-Jan-2026 | GL backend: per-MRT color write masks on GLES3.2 | Low |
| 18-Jan-2026 | GL fix for DEPTH_ATTACHMENT switching | **Medium** — potential bug fix needed |
| 13-Dec-2025 | WebGPU backend cleanup | Low |
| 05-Dec-2025 | **sokol_gfx_imgui.h API breaking change** | **High** — if using debug UI |
| 02-Dec-2025 | **Experimental Vulkan backend added** | High (future consideration) |
| 15-Sep-2025 | **sg_image_data struct breaking change** | **Critical** — affects image loading |
| 29-Sep-2025 | **Flexible resource binding limits update** | **High** — new constants/limits |

**Breaking Changes to Watch:**
1. `sg_image_data.subimage[face][mip]` → `sg_image_data.mip_levels[mip]` (Sept 2025)
2. `sgimgui_init()` → `sgimgui_setup()`, `sgimgui_discard()` → `sgimgui_shutdown()` (Dec 2025)
3. `sg_query_frame_stats()` → `sg_query_stats()` (Dec 2025)
4. New binding slot constants (Sept 2025)

**Open Issues/PRs of Interest:**
- #1439: Create order-independent-transparency sample (dual-source-blending)
- #1432: Vulkan VK_EXT_swapchain_maintenance1 integration (WIP)

---

### 2. bullno1/cosmo-sokol (Intermediate Upstream)

**URL:** https://github.com/bullno1/cosmo-sokol

**Project Description:**
- Sample sokol+dearimgui application compiled with Cosmopolitan toolchain
- Provides the integration layer between sokol and cosmocc
- Requires cosmocc v3.9.5+

**Key Architecture Decisions:**
1. **Linux Platform Shim:** Uses dlopen to dynamically load libGL, libX11, etc.
2. **Windows Platform Shim:** Relies on Cosmopolitan's nt/master.sh for Win32 imports
3. **Multi-platform Runtime Dispatch:** Prefixes sokol functions with platform names (`linux_sapp_*`, `windows_sapp_*`)
4. **Generator Scripts:**
   - `gen-x11` — Generates X11 stub forwarding
   - `gen-gl` — Generates OpenGL stub forwarding
   - `gen-sokol` — Generates multi-platform dispatch shim

**Commit History (Recent):**
| Date | SHA | Message |
|------|-----|---------|
| 2025-03-29 | 5656716 | Merge PR#2: Updated submodules to most recent sokol shader bindings |
| 2024-12-01 | b684362 | Updated submodules to most recent sokol shader bindings |
| 2024-11-02 | 5396971 | Remove notice about NVidia setting (now auto-handled) |
| 2024-11-02 | 228d76e | Use NvAPI_DRS_FindApplicationByName to find the profile |
| 2024-11-02 | 750a553 | Hide console in Windows if not launched from CLI |

**Last Sync:** March 2025 (sokol submodule update)
**Gap from floooh/sokol:** ~11 months behind (significant changes missed)

---

### 3. ludoplex/cosmo-sokol (Our Fork)

**URL:** https://github.com/ludoplex/cosmo-sokol

**Fork Additions:**
- macOS support structure (stub implementation)
- Tri-platform runtime dispatch (Linux, Windows, macOS)
- `sokol_macos.h` and `sokol_macos.c` (stubs)
- `shims/macos/` directory with documentation
- Updated `sokol_cosmo.c` with `IsXnu()` dispatch
- Updated build script to compile macOS backend

**Commit History:**
| Date | SHA | Message |
|------|-----|---------|
| 2026-02-09 | 028aafa | Update README with macOS support documentation |
| 2026-02-09 | 5c2416e | Add macOS support (stub) with tri-platform runtime dispatch |
| 2025-03-29 | 5656716 | (inherited) Updated submodules merge |

**Platform Support Status:**
| Platform | Status | Graphics Backend |
|----------|--------|------------------|
| Linux | ✅ Full | OpenGL via dlopen(libGL.so) |
| Windows | ✅ Full | OpenGL via WGL |
| macOS | 🚧 Stub | Planned: Metal or OpenGL via objc_msgSend |

**macOS Challenge:**
- Sokol uses Objective-C extensively (NSApplication, NSWindow, Metal, etc.)
- cosmocc cannot compile Objective-C directly
- Solution: Use Objective-C runtime from C via `objc_msgSend`

---

### 4. jart/cosmopolitan (Toolchain)

**URL:** https://github.com/jart/cosmopolitan

**Minimum Version Required:** v3.9.5+

**Key Capability:** "build-once run-anywhere" C library producing polyglot executables that run natively on:
- Linux (kernel 2.6.18+)
- Windows 8+
- macOS 23.1.0+ (Darwin)
- FreeBSD 13+, OpenBSD 7.3+, NetBSD 9.2+
- BIOS (bare metal)

**macOS Note:** Darwin minimum version 23.1.0+ (Sonoma, October 2023)

---

## Upstream Sync Strategy Recommendations

### Option 1: Git Submodules with Automated Updates

**Current Approach:** Both cosmo-sokol repos use git submodules for `deps/sokol`

**Automation Strategy:**
```yaml
# GitHub Actions workflow concept
name: Sync Upstream Sokol
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly
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
          git fetch origin master
          git checkout origin/master
          cd ../..
          
      - name: Build test
        run: ./build
        
      - name: Create PR if changes
        uses: peter-evans/create-pull-request@v5
        with:
          title: "chore: sync sokol upstream"
          body: "Automated upstream sync from floooh/sokol"
```

**Pros:**
- Simple to implement
- Preserves history
- Easy rollback

**Cons:**
- Manual conflict resolution if shim files need updates
- No automatic detection of breaking API changes

---

### Option 2: Two-Layer Sync (Recommended)

1. **Layer 1:** Sync `ludoplex/cosmo-sokol` with `bullno1/cosmo-sokol`
   - Captures any Cosmopolitan-specific fixes
   - Less frequent (bullno1 moves slowly)

2. **Layer 2:** Direct sokol submodule sync
   - Update `deps/sokol` submodule independently
   - Test build after update
   - Flag breaking changes

**Workflow:**
```
floooh/sokol (weekly check)
       ↓
deps/sokol submodule update
       ↓
bullno1/cosmo-sokol (monthly check)
       ↓
Merge new shim fixes if any
       ↓
ludoplex/cosmo-sokol
```

---

### Option 3: CHANGELOG Monitoring + Semantic Versioning

Since sokol doesn't use semantic versioning, implement monitoring:

1. **Parse CHANGELOG.md** for breaking changes (keywords: "breaking", "renamed", "removed")
2. **Categorize updates:** Critical / High / Medium / Low
3. **Auto-update for Low/Medium**, manual review for High/Critical
4. **Tag stable points** in ludoplex fork for reproducibility

---

## Key Files to Monitor

| Repository | File | Why |
|------------|------|-----|
| floooh/sokol | `CHANGELOG.md` | Breaking changes, new features |
| floooh/sokol | `sokol_app.h` | Platform support changes |
| floooh/sokol | `sokol_gfx.h` | API changes, backend updates |
| bullno1/cosmo-sokol | `shims/sokol/gen-sokol` | Dispatch generator changes |
| bullno1/cosmo-sokol | `shims/linux/gen-x11` | Linux shim updates |
| bullno1/cosmo-sokol | `build` | Build script changes |
| jart/cosmopolitan | `libc/nt/master.sh` | Win32 function imports |

---

## Immediate Action Items

### Critical (Before Next Round)
1. **Sync deps/sokol** to latest floooh/sokol (currently ~11 months behind)
2. **Review breaking changes** especially `sg_image_data` struct change
3. **Verify build** after sync on Linux and Windows

### High Priority
4. **Set up automated CHANGELOG parsing** to detect breaking changes
5. **Create sync automation workflow** (GitHub Actions)
6. **Document version compatibility matrix** between sokol/cosmopolitan/cosmo-sokol

### Medium Priority
7. **Evaluate Vulkan backend** feasibility for Cosmopolitan
8. **Monitor bullno1 for new shim improvements**
9. **Complete macOS objc_msgSend implementation** for full tri-platform support

---

## API Compatibility Concerns

### Sokol Functions Used in cosmo-sokol

The `gen-sokol` script generates dispatch for approximately 100+ public functions. Key categories:

**App Functions (sokol_app.h):**
- `sapp_isvalid`, `sapp_width`, `sapp_height`
- `sapp_show_keyboard`, `sapp_keyboard_shown`
- `sapp_mouse_cursor`, `sapp_request_quit`
- etc.

**Graphics Functions (sokol_gfx.h):**
- `sg_setup`, `sg_shutdown`
- `sg_make_buffer`, `sg_make_image`, `sg_make_shader`
- `sg_begin_pass`, `sg_end_pass`, `sg_commit`
- etc.

**Recent Additions to Track:**
- `sg_draw_ex()` — new in Oct 2025
- `sg_query_stats()` — replaces `sg_query_frame_stats()` Dec 2025
- Dual-source-blend factors — new in Jan 2026

---

## References & Links

- **Sokol CHANGELOG:** https://github.com/floooh/sokol/blob/master/CHANGELOG.md
- **Sokol Blog (floooh):** https://floooh.github.io/
- **Cosmopolitan Downloads:** https://cosmo.zip/pub/cosmocc/
- **Cosmopolitan Discord:** https://discord.gg/FwAVVu7eJ4
- **GitHub Fork Sync Docs:** https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork

---

## Summary for Other Specialists

| Specialist | Key Info |
|------------|----------|
| **localsearch** | Check `deps/sokol` submodule version, compare with upstream HEAD |
| **asm** | Sokol has platform-specific assembly, mostly in sokol_app.h |
| **cosmo** | Watch for cosmopolitan min version bumps, dlopen patterns |
| **dbeng** | Not applicable |
| **neteng** | sokol_fetch.h for HTTP streaming may need testing |
| **cicd** | Need build matrix: Linux x86_64, Windows x86_64, (macOS stub) |
| **testcov** | sokol has no formal test suite; relies on samples compiling |

---

*Report generated by Seeker subagent — Swiss Rounds v3 Round 1*
