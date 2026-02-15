# Project Index: cosmo-sokol v3 Upstream Sync

**Generated:** 2026-02-09
**Method:** Incremental indexing from specialist reports
**Purpose:** Quick-reference index of key terms, concepts, file locations, and line numbers

---

## Index by Report

### 1. asm-cosmo-sokol-v3.md (ASM Specialist)
**Domain:** AMD64/AArch64 Assembly, ABI, Calling Conventions

#### Key Terms
- `cosmo_dltramp` — Trampoline wrapper for cross-ABI function calls
- `cosmo_dlopen` — Cosmopolitan's dlopen wrapper
- `cosmo_dlsym` — Symbol lookup function
- HFA (Homogeneous Floating-Point Aggregate) — ARM64 calling convention for float structs
- Hidden pointer return — Struct return mechanism for large structs

#### Critical File Locations
| File | Lines | Content |
|------|-------|---------|
| `deps/sokol/sokol_gfx.h` | 1648-1653 | Handle type definitions (sg_buffer, sg_image, etc.) |
| `deps/sokol/sokol_gfx.h` | 1662-1665 | sg_range struct definition (16 bytes) |
| `deps/sokol/sokol_gfx.h` | 1702 | sg_color struct (4 floats) |
| `shims/sokol/sokol_windows.c` | 1-105 | Win32 type redefinitions |
| `shims/sokol/sokol_windows.c` | 14-24 | LARGE_INTEGER definition |
| `shims/sokol/sokol_windows.c` | 26-31 | RECT definition |
| `shims/sokol/sokol_windows.c` | 33-36 | POINT definition |
| `shims/sokol/sokol_windows.c` | 38-46 | MSG definition |
| `shims/sokol/sokol_windows.c` | 72-95 | PIXELFORMATDESCRIPTOR |
| `shims/linux/x11.c` | 81-146 | cosmo_dltramp pattern usage |
| `shims/linux/x11.c` | 87 | Load-before-use pattern |
| `shims/linux/x11.c` | 89 | assert()-based error handling (PROBLEM) |

#### Key Concepts
1. **Handle Types ABI-Safe** — All 4-byte single-member structs, register-passed
2. **sg_range 16-byte boundary** — Different handling between SysV (2 regs) vs MS x64 (hidden ptr)
3. **sg_color ARM64 HFA** — Passed in SIMD registers V0-V3 on ARM64
4. **cosmo_dltramp pattern** — save regs → convert ABI → call → convert return → restore

#### Struct Sizes (Verified)
| Struct | Size | Alignment | Notes |
|--------|------|-----------|-------|
| sg_buffer | 4 bytes | 4 bytes | uint32_t id |
| sg_image | 4 bytes | 4 bytes | uint32_t id |
| sg_sampler | 4 bytes | 4 bytes | uint32_t id |
| sg_shader | 4 bytes | 4 bytes | uint32_t id |
| sg_pipeline | 4 bytes | 4 bytes | uint32_t id |
| sg_attachments | 4 bytes | 4 bytes | uint32_t id |
| sg_range | 16 bytes | 8 bytes | ptr + size |
| sg_color | 16 bytes | 4 bytes | 4 floats |
| LARGE_INTEGER | 8 bytes | 8 bytes | Win32 |
| RECT | 16 bytes | 4 bytes | Win32 |
| POINT | 8 bytes | 4 bytes | Win32 |
| MSG | 48 bytes | 8 bytes | Win32 |

#### Identified Issues
| Issue | Severity | Location | Description |
|-------|----------|----------|-------------|
| assert() in production | MEDIUM | x11.c:89 | assert removed in NDEBUG builds |
| Unversioned .so names | MEDIUM | x11.c | libX11.so instead of libX11.so.6 |
| ARM64 HFA untested | MEDIUM | - | sg_color SIMD register passing |

#### Proposed Deliverables
| File | Description |
|------|-------------|
| `shims/include/sokol_abi_check.h` | Static assertions for struct layouts |
| `test/abi_smoke_test.c` | ABI verification test program |

#### Register Mapping Reference
| Arg # | AMD64 SysV | AMD64 MS x64 | ARM64 AAPCS |
|-------|------------|--------------|-------------|
| 1 (int/ptr) | RDI | RCX | X0 |
| 2 (int/ptr) | RSI | RDX | X1 |
| 3 (int/ptr) | RDX | R8 | X2 |
| 4 (int/ptr) | RCX | R9 | X3 |
| 5+ | R8, R9, stack | stack | X4-X7, stack |
| Float 1 | XMM0 | XMM0 | V0 |
| Float 2 | XMM1 | XMM1 | V1 |

---

### 2. cicd-cosmo-sokol-v3.md (CI/CD Specialist)
**Domain:** GitHub Actions, automated testing, release automation

#### Key Terms
- `bjia56/setup-cosmocc` — GitHub Action for Cosmopolitan toolchain
- Dependabot — Automated dependency updates
- `cosmo-sokol.json` — Project metadata manifest (proposed)
- APE binary — Actually Portable Executable format
- Xvfb — X Virtual Framebuffer for headless testing

#### Critical File Locations
| File | Lines | Content |
|------|-------|---------|
| `.github/workflows/build.yml` | 1-38 | Current minimal build workflow |
| `build` | 1-48 | Shell build script (parallel compilation) |
| `scripts/compile` | 1-20 | Per-file compilation script |
| `shims/sokol/gen-sokol` | 1-229 | Generator for platform-specific stubs |
| `shims/sokol/gen-sokol` | 7-180 | SOKOL_FUNCTIONS list (manual maintenance) |

#### Key Metrics
| Metric | Value | Source |
|--------|-------|--------|
| Commits behind upstream | **1,032** | Verified via git rev-list |
| cosmocc CI version | 3.9.6 | build.yml |
| cosmocc minimum version | 3.9.5 | README |
| Platform support | Linux (full), Windows (full), macOS (stub) | - |

#### CI/CD Gaps Identified
| Gap | Severity | Description |
|-----|----------|-------------|
| No upstream sync automation | CRITICAL | sokol 1,032 commits behind |
| No testing infrastructure | HIGH | Zero unit/integration tests |
| No cross-platform validation | HIGH | Build only on ubuntu-latest |
| No API/ABI compatibility checks | HIGH | gen-sokol drift undetected |
| Hardcoded cosmocc version | MEDIUM | May miss updates |
| No security scanning | MEDIUM | No CodeQL/SAST |

#### Proposed Workflows
| Workflow | Purpose | Priority |
|----------|---------|----------|
| `upstream-sync.yml` | Weekly drift detection + issue creation | P0 |
| `static-analysis.yml` | ABI assertions, API drift, dltramp lint | P0 |
| `build-matrix.yml` | Multi-version cosmocc matrix | P1 |
| `platform-validate.yml` | Linux/Windows/macOS smoke tests | P1 |
| `release-metadata.yml` | Generate cosmo-sokol.json on release | P2 |

#### Exit Code Semantics (C Tools)
| Tool | Exit 0 | Exit 1 |
|------|--------|--------|
| `drift-report` | All submodules <500 behind | Any ≥500 behind |
| `changelog-scan` | No breaking changes | Breaking changes found |
| `check-api-sync` | API in sync | API drift detected |

#### Bugs Fixed in Round 3
| Bug | Location | Fix |
|-----|----------|-----|
| String comparison `behind > 0` | upstream-sync.yml | Use `fromJSON()` |
| Duplicate issue creation | upstream-sync.yml | Add deduplication check |
| No git fetch error handling | upstream-sync.yml | Graceful degradation |

#### Five-Tier CI Architecture
```
Tier 1: Upstream Monitoring (weekly cron)
Tier 2: Static Analysis (ABI, API, dltramp)
Tier 3: Build Matrix (cosmocc versions)
Tier 4: Platform Validation (Linux/Windows/macOS)
Tier 5: Release & Metadata (cosmo-sokol.json)
```

---

### 3. cosmo-cosmo-sokol-v3.md (Cosmo Specialist)
**Domain:** Cosmopolitan libc internals (dlopen, APE format, cross-platform shims)

#### Key Terms
- `cosmo_dlopen()` — Load dynamic library at runtime
- `cosmo_dlsym()` — Retrieve symbol from library
- `cosmo_dltramp()` — Create ABI-safe trampoline wrapper (REQUIRED)
- `cosmo_dlerror()` — Get last error message
- `IsLinux()`, `IsWindows()`, `IsXnu()` — Platform detection macros
- APE — Actually Portable Executable format
- Lazy loading — Libraries loaded on first function call

#### Critical File Locations
| File | Lines | Content |
|------|-------|---------|
| `shims/linux/x11.c` | 77-80 | cosmo_dltramp pattern usage |
| `shims/linux/x11.c` | 489 total | X11 dlopen shims (47 functions) |
| `shims/linux/gl.c` | 6172 total | OpenGL dlopen shims (600+ functions) |
| `shims/sokol/sokol_cosmo.c` | 9-22 | Runtime dispatch pattern |
| `shims/sokol/sokol_cosmo.c` | 3099 total | **HIGH SENSITIVITY** dispatch layer |
| `shims/sokol/gen-sokol` | 7-177 | SOKOL_FUNCTIONS manual list |
| `shims/sokol/gen-sokol` | 230 total | **HIGH SENSITIVITY** generator |
| `shims/sokol/sokol_macos.c` | 753 total | macOS stub (needs implementation) |
| `build` | 16 | NT import headers path |
| `build` | 65 total | Build script with cosmo flags |

#### Platform Detection Pattern (sokol_cosmo.c)
```c
if (IsLinux()) { return linux_sapp_isvalid(); }
if (IsWindows()) { return windows_sapp_isvalid(); }
if (IsXnu()) { return macos_sapp_isvalid(); }
```

#### Libraries Loaded at Runtime
| Library | File | Functions |
|---------|------|-----------|
| libX11.so | x11.c:77 | 47 functions |
| libXcursor.so | x11.c:149 | 6 functions |
| libXi.so | x11.c:169 | 2 functions |
| libGL.so | gl.c | 600+ functions |

#### Proposed Deliverables
| File | Priority | Description |
|------|----------|-------------|
| `shims/include/cosmo_dl_safe.h` | P0 | Safe dlopen macros with error handling |
| `scripts/extract-sokol-api.py` | P1 | API extractor for gen-sokol sync |
| `shims/macos/objc_bridge.c` | P2 | Objective-C runtime bridge for macOS |
| `tools/check-api-sync.c` | P1 | C/APE API drift detector |

#### Breaking API Changes Detected (sokol upstream)
| Change | Type | Impact |
|--------|------|--------|
| `sapp_color_format()` return `int` → `sapp_pixel_format` | Breaking | gen-sokol update |
| `sapp_depth_format()` return `int` → `sapp_pixel_format` | Breaking | gen-sokol update |
| New: `sapp_bind_mouse_cursor_image()` | Addition | gen-sokol addition |
| New: `sapp_unbind_mouse_cursor_image()` | Addition | gen-sokol addition |
| Metal/D3D11 accessor functions removed | Breaking | May affect Windows |

#### macOS Implementation Challenges
1. Objective-C runtime requires separate trampolines:
   - `objc_msgSend` (normal)
   - `objc_msgSend_stret` (struct returns)
   - `objc_msgSend_fpret` (float returns)
2. ARM64 macOS uses unified `objc_msgSend` (simpler)
3. Block callbacks require additional handling

#### cosmocc Version Matrix
| cosmocc | sokol | Status |
|---------|-------|--------|
| 3.9.5 | eaa1ca7 | ✅ Minimum required |
| 3.9.6 | eaa1ca7 | ✅ CI-pinned |
| 3.10.x | TBD | ⚠️ Untested |

---

### 4. seeker-cosmo-sokol-v3.md (Seeker Specialist)
**Domain:** Advanced search, source discovery, upstream tracking

#### Key Findings
| Metric | Value |
|--------|-------|
| Submodule commit | `eaa1ca79a4004750e58cb51e0100d27f23e3e1ff` |
| Submodule date | 2024-11-23 |
| Upstream HEAD | `d48aa2ff673af2d6b981032dd43766ab15689163` |
| **Commits behind** | **1,032** |
| **Time drift** | ~14.5 months |

#### Critical Breaking Changes (Must Address)
| Date | PR | Change | Impact |
|------|-----|--------|--------|
| 2024-11-07 | PR#1111 | `sg_apply_uniforms()` signature changed, `sg_bindings` struct changed | **CRITICAL** |
| 2025-01+ | PR#1200+ | Compute shader support (`sg_dispatch()`) | gen-sokol update |
| 2025-01+ | PR#1350 | Experimental Vulkan backend | Platform impact |
| 2025-02+ | PR#1287 | Resource views (`sg_view`) | API additions |

#### sg_apply_uniforms Breaking Change
```c
// BEFORE (current in fork):
void sg_apply_uniforms(sg_shader_stage stage, int ub_slot, const sg_range* data);

// AFTER (upstream):
void sg_apply_uniforms(int ub_slot, const sg_range* data);  // No shader stage!
```

#### sg_bindings Breaking Change
```c
// BEFORE: Separate fs/vs image arrays
struct { sg_image images[...]; } fs, vs;

// AFTER: Unified arrays
sg_image images[SG_MAX_IMAGE_BINDSLOTS];
sg_sampler samplers[SG_MAX_SAMPLER_BINDSLOTS];
sg_buffer storage_buffers[SG_MAX_STORAGEBUFFER_BINDSLOTS];  // NEW
```

#### Missing Functions in gen-sokol
| Function | PR | Purpose |
|----------|-----|---------|
| `sg_dispatch()` | PR#1200 | Compute shaders |
| `sg_draw_ex()` | PR#1339 | Extended draw |
| `sg_make_view()` | PR#1287 | Resource views |
| `sg_destroy_view()` | PR#1287 | Resource views |
| `sapp_get_swapchain()` | PR#1350 | Renamed API |

#### gen-sokol Function Count
| Category | Count |
|----------|-------|
| `sapp_*` functions | 52 |
| `sg_*` functions | 141 |
| **Total** | 193 |

#### Repository Structure
| Path | Type | Status |
|------|------|--------|
| `C:\cosmo-sokol` | Primary fork | ✅ |
| `C:\cosmo-sokol\deps\sokol` | Submodule (floooh/sokol) | 1,032 behind |
| `C:\cosmo-sokol\deps\cimgui` | Submodule (cimgui/cimgui) | Needs check |

#### Proposed Tools (C/APE)
| Tool | Purpose | Lines |
|------|---------|-------|
| `tools/changelog-scan.c` | Parse sokol CHANGELOG for breaking changes | ~400 |
| `tools/drift-report.c` | Git submodule drift detection | ~300 |
| `tools/check-api-sync.c` | Verify gen-sokol matches sokol headers | ~350 |

---

### 5. neteng-cosmo-sokol-v3.md (Network Engineering Specialist)
**Domain:** Deployment, distribution, binary verification, platform testing

#### Build Infrastructure
| File | Lines | Purpose |
|------|-------|---------|
| `build` | 57 | POSIX shell build script |
| `.github/workflows/build.yml` | 34 | CI workflow |
| `.gitmodules` | - | Submodule configuration |

#### Build Script Key Lines
| Line | Feature |
|------|---------|
| 3-7 | cosmocc detection |
| 9 | COSMO_HOME derivation |
| 11-19 | Platform-specific flags |
| 24-33 | Platform compilation |
| 47-49 | Parallel build |
| 52-53 | Final link |

#### Build Outputs
```
bin/
├── cosmo-sokol              # APE polyglot binary
├── cosmo-sokol.aarch64.elf  # ARM64 ELF (if built)
└── cosmo-sokol.com.dbg      # Debug symbols (if built)
```

#### Platform Status
| Platform | Backend | Status |
|----------|---------|--------|
| Linux | OpenGL via dlopen | ✅ Full |
| Windows | WGL + D3D11 | ✅ Full |
| macOS | Metal | 🚧 Stub only |

#### Distribution Gaps
| Component | Current | Required |
|-----------|---------|----------|
| SHA256 checksums | ❌ None | SHA256SUMS file |
| Platform smoke tests | ❌ None | Cross-platform validation |
| Provenance | ❌ None | SLSA-compliant artifacts |

---

### 6. Triad Reports Summary (Critique/Solution/Redundancy)
**Domain:** Quality assurance across all specialist reports

#### Philosophy Decision
> All Python tooling → C/APE binaries (Cosmopolitan philosophy)

#### Final Status
| Area | Status |
|------|--------|
| Philosophy | ✅ All Python eliminated, C/APE tooling |
| Consolidation | ✅ Single owner per deliverable |
| CI/CD | ✅ Production-ready workflows |
| Remaining | 6 P1/P2 fixes |

#### P0 Fixes Applied
| Issue | Fix |
|-------|-----|
| String comparison bug | Use `fromJSON()` |
| Duplicate issue creation | Deduplication check |
| Git fetch error handling | Graceful degradation |

#### P1 Fixes Specified
| Issue | File | Fix |
|-------|------|-----|
| Windows popen() | drift-report.c | Use chdir() instead of shell cd |
| Multi-line comments | check-api-sync.c | Strip inline comments |
| Date parsing | changelog-scan.c | Multi-format parser |

#### Deliverable Ownership
| Deliverable | Owner |
|-------------|-------|
| check-api-sync.c | cosmo |
| validate-sources.c | cosmo |
| cosmo_dl_safe.h | cosmo |
| Makefile | seeker |
| changelog-scan.c | seeker |
| drift-report.c | seeker |
| build.yml | neteng |
| upstream-sync.yml | cicd |
| cosmo-sokol.json | dbeng |

---

## Quick Reference Summary

### Critical Metrics
| Metric | Value |
|--------|-------|
| Commits behind upstream | **1,032** |
| Breaking API changes | 1 major (Nov 2024 bindings) |
| Time drift | ~14.5 months |
| Platform support | Linux ✅, Windows ✅, macOS 🚧 |
| gen-sokol function count | 193 (52 sapp_* + 141 sg_*) |

### Key Files (High Sensitivity)
| File | Sensitivity | Reason |
|------|-------------|--------|
| `shims/sokol/gen-sokol` | **HIGH** | Manual function list |
| `shims/sokol/sokol_cosmo.c` | **HIGH** | Generated dispatch layer |
| `shims/include/cosmo_dl_safe.h` | HIGH | Error handling macros |
| `deps/sokol/sokol_gfx.h` | CRITICAL | ABI definitions |

### Breaking Change: sg_apply_uniforms
```c
// OLD: void sg_apply_uniforms(sg_shader_stage stage, int ub_slot, const sg_range* data);
// NEW: void sg_apply_uniforms(int ub_slot, const sg_range* data);
```

### Phase Plan Summary
| Phase | Duration | Focus |
|-------|----------|-------|
| 0 | 0.5 day | Prerequisites, backup |
| 1 | 1 day | Core C tools |
| 2 | 1.5 days | Infrastructure (cosmo_dl_safe.h, build.yml) |
| 3 | 1 day | Seeker tools (changelog-scan, drift-report) |
| 4 | 1 day | Developer workflow (pre-commit hooks) |
| 5 | 0.5 day | Integration testing |
| 6 | 0.5 day | Sync execution, release v3.0.0 |

---

*Index complete. Generated from 25 specialist reports.*
*Ready for overarching plan synthesis.*
