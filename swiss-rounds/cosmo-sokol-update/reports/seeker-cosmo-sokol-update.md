# Upstream Intelligence Report: cosmo-sokol-update

**Date:** 2026-02-09
**Researcher:** seeker (subagent)
**Methodology:** Direct GitHub API and raw file fetching

---

## Executive Summary

**bullno1/cosmo-sokol** is currently pinned to Nov 2024 versions of all dependencies and cosmocc v3.9.6. Updating to latest versions requires addressing **significant breaking changes** in sokol (especially the Aug 2025 "resource view update") and cimgui (Dear ImGui 1.92.0 texture handling changes).

---

## 1. floooh/sokol — Latest State & Breaking Changes

### Current Status
- **Repository:** https://github.com/floooh/sokol
- **Latest Activity:** Feb 8, 2026 (iOS/Metal scissor rect fix)
- **Release Pattern:** Rolling releases, no version tags (commit-based)

### Pinned in cosmo-sokol
- **Commit:** `eaa1ca79a4004750e58cb51e0100d27f23e3e1ff`
- **Date:** Nov 23, 2024
- **Description:** "sokol_app.h html5: cleanup canvas lookup handling"

### Major Breaking Changes Since Nov 2024

#### 🚨 CRITICAL: Aug 23, 2025 — "Resource View Update"
**Impact: VERY HIGH — Requires significant code rewrite**

- New object type `sg_view` added — views now "specialize" images/buffers for shader access
- `sg_attachments` object type **REMOVED**
- `sg_bindings` now takes single array of `sg_view` objects
- Storage-image-bindings moved from pass-attachments to regular bindings
- `sg_pass.attachments` changed to transient nested struct
- **sokol-shdc must also be updated** — shader recompilation required

Source: [CHANGELOG.md](https://github.com/floooh/sokol/blob/master/CHANGELOG.md) — "The sokol_gfx.h 'resource view update'"

#### Dec 4, 2025 — Stats API Rename
- `sg_frame_stats` → `sg_stats`
- `sg_query_frame_stats()` → `sg_query_stats()`

#### Dec 5, 2025 — sokol_gfx_imgui.h Breaking Changes
- `sgimgui_init()` → `sgimgui_setup()`
- `sgimgui_discard()` → `sgimgui_shutdown()`
- 'Context arg' removed from public API

#### Sep 15, 2025 — Cubemap API Change
- `sg_image_data.subimage[face][mip]` → `sg_image_data.mip_levels[mip]`
- `sg_cube_face` enum removed
- `sg_image_desc.num_slices` default for cubemaps changed to 6

#### Jun 29, 2025 — Dear ImGui 1.92.0 Backend Update
- Font atlas rendering changes (high-DPI fixes)
- `igImage()` now takes `ImTextureRef` struct instead of `ImTextureID`
- Custom font attachment code needs update

#### Dec 2, 2025 — Vulkan Backend (Experimental)
- New backend added for Linux/Windows
- May affect compilation if not properly conditionally compiled

### Other Notable Changes
- Sep 29, 2025: Flexible resource binding limits
- Sep 1, 2025: Custom mouse cursor support
- Multiple WebGPU backend updates

---

## 2. jart/cosmopolitan — v4.0.2 Analysis

### Current Status
- **Latest Release:** v4.0.2 (Jan 6, 2026)
- **Repository:** https://github.com/jart/cosmopolitan
- **Release Pattern:** Semantic versioning with patch releases

### Pinned in cosmo-sokol CI
- **Version:** 3.9.6 (via `bjia56/setup-cosmocc@main`)
- **Minimum Required:** 3.9.5 (per README)

### v4.0.x Release Notes

#### v4.0.0 (Jan 3, 2026)
Major improvements:
- Fix fork waiter leak in nsync
- Eliminate cyclic locks in runtime
- Make threads faster and more reliable
- Fix fork thread handle leak on Windows
- Improve memory manager and signal handling
- **fork() now 30% faster**
- Windows sleep accuracy improved: 15ms → 15µs

#### v4.0.1 (Jan 4, 2026)
- Add missing lock to fork() on Windows
- Fix pthread_create ordering

#### v4.0.2 (Jan 6, 2026)
- Fix fork() regression on Windows
- Make execve() linger when can't spoof parent
- Fix Windows MODE=tiny breakage

### dlopen Capabilities
**dlopen has been available since at least v3.9.5** — this is how cosmo-sokol loads system libraries dynamically (libX11, libGL, etc.). The approach is documented in the cosmo-sokol README:
- Instead of linking directly to libraries, stub implementations are used
- When called, the stub loads the actual library via `dlopen` and forwards the call via `dlsym`

Source: [cosmo-sokol README](https://github.com/bullno1/cosmo-sokol#how-it-works)

### Platform Support
| Platform | Min Version | Circa |
|----------|-------------|-------|
| Linux | 2.6.18 | 2007 |
| Windows | 8 | 2012 |
| Darwin (macOS) | 23.1.0+ | 2023 |
| OpenBSD | 7.3 | 2023 |
| FreeBSD | 13 | 2020 |
| NetBSD | 9.2 | 2021 |

### Known Issues
- Windows Vista/7 requires [vista branch](https://github.com/jart/cosmopolitan/tree/vista)
- binfmt_misc interpreter may be needed on some Linux distros
- zsh 5.9+ required (older versions have execve() bug)

---

## 3. bullno1/cosmo-sokol — Version Pinning Analysis

### Current Submodule Pins

| Dependency | Commit SHA | Date | Notes |
|------------|-----------|------|-------|
| sokol | `eaa1ca79a4004750e58cb51e0100d27f23e3e1ff` | Nov 23, 2024 | Pre-resource-view-update |
| cimgui | `8ec6558ecc9476c681d5d8c9f69597962045c2e6` | Nov 18, 2024 | docking_inter branch merge |
| cosmocc (CI) | 3.9.6 | Nov 1, 2024 | Not submodule, workflow-pinned |

### Commit History Analysis

#### Recent Activity
1. **Mar 29, 2025** — Merged PR #2: "Updated submodules to most recent sokol shader bindings" (JayBernstein)
2. **Nov 2, 2024** — NVidia threaded optimization handling
3. **Nov 2, 2024** — Console hiding for Windows GUI apps

#### Why Versions Are Pinned

Based on the repository structure and commit history:

1. **Complex Shim Architecture** — cosmo-sokol uses a sophisticated shim layer:
   - `shims/sokol/gen-sokol` generates platform multiplexing code
   - `shims/linux/gen-gl` and `shims/linux/gen-x11` generate dlopen stubs
   - These shims parse sokol headers and generate wrapper code
   - **Any sokol API change requires regenerating shims**

2. **Manual Platform Abstraction** — The project compiles ALL platform code paths simultaneously:
   - Every sokol public function is prefixed with platform name (e.g., `linux_sapp_show_keyboard`)
   - A runtime shim selects the correct implementation
   - **Breaking changes in sokol require updating ALL platform implementations**

3. **Cosmopolitan Header Limitations** — From README:
   - Cosmopolitan's own headers lack many Windows function prototypes
   - All relevant Windows struct definitions are manually replicated in `sokol_windows.c`
   - **New Windows APIs in sokol may require manual cosmopolitan patches**

### What Breaks When Updating

#### If updating sokol to latest:
1. **shims/sokol/gen-sokol** must be updated for new/changed API
2. **sokol_cosmo.c** (65KB) needs regeneration — handles runtime platform selection
3. **Resource view update** requires:
   - Converting `sg_attachments` usage to `sg_view` objects
   - Updating all `sg_bindings` usage
   - Recompiling all shaders with new sokol-shdc
4. **sokol_windows.c** may need new struct definitions

#### If updating cosmopolitan to v4.0.x:
- Lower risk — mostly internal improvements
- May need to verify Windows GUI subsystem detection still works
- Test fork() behavior changes don't affect anything

---

## 4. cimgui/cimgui — Current vs Latest

### Current Status
- **Repository:** https://github.com/cimgui/cimgui
- **Default Branch:** `docking_inter` (tracks Dear ImGui docking branch)
- **Latest Dear ImGui:** 1.92.4

### Pinned in cosmo-sokol
- **Commit:** `8ec6558ecc9476c681d5d8c9f69597962045c2e6`
- **Date:** Nov 18, 2024
- **Tracks:** Dear ImGui ~1.91.x (pre-1.92.0)

### Breaking Changes Since Nov 2024

#### Nov 10, 2025 — Non-POD Struct Handling
- Functions returning/taking non-POD structs now have internal conversion
- C names have `_c` suffix for these cases
- `structs_and_enums.json` now includes `nonPOD_used` key
- **Impact:** May affect C bindings if using affected functions

#### Dear ImGui 1.92.0 Changes (Jun 2025)
- Font texture handling changed
- `igImage()` now takes `ImTextureRef` instead of `ImTextureID`
- Custom font setup code needs update

### Stability Assessment
- cimgui itself is auto-generated from Dear ImGui
- Stable if tracking same Dear ImGui version
- Breaking changes flow from Dear ImGui upstream
- **Recommendation:** Update together with sokol_imgui.h updates

---

## 5. Specific Commits/Changes That Caused Pinning

### Timeline Reconstruction

1. **Nov 2024** — bullno1 created initial cosmo-sokol with working sokol + cimgui
2. **Dec 2024** — JayBernstein submitted PR updating shader bindings
3. **Mar 2025** — PR merged, but only updating shader-related submodule refs
4. **Aug 2025** — sokol's "resource view update" makes updating very difficult
5. **Present** — Repo still on pre-resource-view-update sokol

### Root Cause Analysis

The fundamental issue is **architectural**: cosmo-sokol's multi-platform shim generation approach means:

1. Every sokol API function becomes 2+ functions (linux_, windows_)
2. A master dispatcher must be maintained in sokol_cosmo.c
3. Any API change requires regenerating ~65KB of glue code
4. Breaking changes multiply complexity across all platforms

**The Aug 2025 "resource view update" is the primary blocker** — it's not just a function rename but a fundamental redesign of the resource binding model.

---

## 6. Recommendations for ludoplex/cosmo-sokol

### Short-term (Lower Risk)
1. ✅ Update cosmopolitan from 3.9.6 → 4.0.2 (mostly internal improvements)
2. ⚠️ Test thoroughly on Windows (fork/exec changes)

### Medium-term (Moderate Effort)
1. Update cimgui to latest (requires handling non-POD changes)
2. Update Dear ImGui texture handling code

### Long-term (Significant Effort)
1. **Fork sokol at pre-resource-view commit** and maintain separately
2. **OR** Undertake full resource view migration:
   - Regenerate all shims
   - Update main.c for new binding API
   - Update sokol_cosmo.c generator
   - Recompile all shaders

### Automation Opportunities
- CI could track upstream commits and flag breaking changes
- Shim generators could be enhanced to detect API changes
- A "compatibility layer" could abstract sokol API versions

---

## Sources

1. [floooh/sokol CHANGELOG.md](https://raw.githubusercontent.com/floooh/sokol/master/CHANGELOG.md)
2. [jart/cosmopolitan releases](https://github.com/jart/cosmopolitan/releases)
3. [bullno1/cosmo-sokol GitHub API commits](https://api.github.com/repos/bullno1/cosmo-sokol/commits)
4. [bullno1/cosmo-sokol .gitmodules](https://raw.githubusercontent.com/bullno1/cosmo-sokol/master/.gitmodules)
5. [bullno1/cosmo-sokol build.yml](https://raw.githubusercontent.com/bullno1/cosmo-sokol/master/.github/workflows/build.yml)
6. [cimgui/cimgui README](https://github.com/cimgui/cimgui)
7. [sokol commit eaa1ca79](https://github.com/floooh/sokol/commit/eaa1ca79a4004750e58cb51e0100d27f23e3e1ff) (pinned version)
8. [cimgui commit 8ec6558](https://github.com/cimgui/cimgui/commit/8ec6558ecc9476c681d5d8c9f69597962045c2e6) (pinned version)
