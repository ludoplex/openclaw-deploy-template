# Overarching Plan: cosmo-sokol v3 Upstream Sync

**Project:** ludoplex/cosmo-sokol fork ← floooh/sokol upstream synchronization  
**Synthesis Date:** 2026-02-09  
**PM Agent:** project-manager  
**Source Reports:** 8 specialist reports + 9 triad reports (24 total)  
**Status:** READY FOR IMPLEMENTATION

---

## 1. Executive Summary

The cosmo-sokol project (a Cosmopolitan libc fork of sokol) has accumulated **1,032 commits of drift** from upstream floooh/sokol. This synthesis consolidates findings from 8 specialist agents across 3 Swiss Rounds to produce a comprehensive synchronization plan.

### Key Decisions

| Decision | Outcome |
|----------|---------|
| Philosophy | All Python tooling → C/APE binaries (Cosmopolitan philosophy) |
| Primary Risk | Breaking changes since Nov 2024 (`sg_apply_uniforms` signature) |
| Tool Ownership | Single owner per deliverable (no redundancy) |
| Readiness | 92-95% production-ready per final triad assessment |

### Critical Metrics

- **Upstream Commits Behind:** 1,032
- **Breaking Changes Detected:** 1 major (Nov 2024 bindings cleanup)
- **Python Scripts Eliminated:** 6 → 0
- **C/APE Tools Created:** 4
- **Workflow Files Consolidated:** 6 → 2

---

## 2. Project Manifest

### 2.1 Repository Structure

```
C:\cosmo-sokol\                         # ludoplex/cosmo-sokol fork
├── .github/workflows/
│   ├── build.yml                       # REPLACE (neteng)
│   └── upstream-sync.yml               # REPLACE (cicd)
├── deps/
│   └── sokol/                          # Submodule: floooh/sokol (1032 behind)
│       ├── sokol_app.h                 # 61 sapp_* functions
│       ├── sokol_gfx.h                 # ~100 sg_* functions  
│       └── CHANGELOG.md                # Breaking changes source
├── shims/
│   ├── include/
│   │   ├── gen-sokol.h                 # Generated API wrapper
│   │   └── cosmo_dl_safe.h             # CREATE (cosmo)
│   └── linux/
│       └── x11.c                       # UPDATE to use safe macros
├── tools/                              # CREATE directory
│   ├── check-api-sync.c                # CREATE (cosmo)
│   ├── validate-sources.c              # CREATE (triad)
│   ├── changelog-scan.c                # CREATE (seeker)
│   ├── drift-report.c                  # CREATE (seeker)
│   └── Makefile                        # CREATE (seeker)
├── scripts/                            # Developer workflow
│   ├── pre-commit-drift-check.sh       # CREATE (localsearch)
│   └── verify-symbols.sh               # CREATE (localsearch)
├── cosmo-sokol.json                    # CREATE (dbeng)
└── SYNC.md                             # CREATE (seeker)
```

### 2.2 Key Functions Tracked

#### sokol_app.h (61 functions)
```
sapp_run, sapp_isvalid, sapp_width, sapp_height, sapp_widthf, sapp_heightf,
sapp_color_format, sapp_depth_format, sapp_sample_count, sapp_high_dpi,
sapp_dpi_scale, sapp_show_keyboard, sapp_keyboard_shown, sapp_is_fullscreen,
sapp_toggle_fullscreen, sapp_show_mouse, sapp_mouse_shown, sapp_enable_clipboard,
sapp_set_clipboard_string, sapp_get_clipboard_string, sapp_set_window_title,
sapp_set_icon, sapp_get_num_dropped_files, sapp_get_dropped_file_path,
sapp_request_quit, sapp_cancel_quit, sapp_quit, sapp_consume_event,
sapp_frame_count, sapp_frame_duration, sapp_lock_mouse, sapp_mouse_locked,
sapp_d3d11_get_device, sapp_d3d11_get_device_context, sapp_d3d11_get_render_view,
sapp_d3d11_get_depth_stencil_view, sapp_wgpu_get_device, sapp_wgpu_get_render_view,
sapp_wgpu_get_resolve_view, sapp_wgpu_get_depth_stencil_view, sapp_gl_get_framebuffer,
sapp_gl_get_major_version, sapp_gl_get_minor_version, sapp_android_get_native_activity,
sapp_macos_get_window, sapp_ios_get_window, sapp_win32_get_hwnd,
sapp_x11_get_display, sapp_x11_get_window
```

#### sokol_gfx.h (~100 functions) - Key Breaking Change
```c
// BEFORE (pre-Nov 2024):
SOKOL_GFX_API_DECL void sg_apply_uniforms(sg_shader_stage stage, int ub_index, 
                                          const sg_range* data);

// AFTER (Nov 2024+):
SOKOL_GFX_API_DECL void sg_apply_uniforms(int ub_slot, const sg_range* data);
// sg_shader_stage removed from signature!
```

### 2.3 Critical Variables & Macros

```c
// shims/include/cosmo_dl_safe.h
#define COSMO_DL_LOAD_LIB(handle_var, lib_name, required)
#define COSMO_DL_LOAD_SYM(handle, sym_ptr, sym_name, required)
#define COSMO_DL_LOAD_SYM_OPT(handle, sym_ptr, sym_name)
#define COSMO_DL_UNLOAD_LIB(handle_var)

// Platform detection
#define COSMO_DL_HINTS_X11       "libX11.so.6:libX11.so"
#define COSMO_DL_HINTS_GL_LINUX  "libGL.so.1:libGL.so"
#define COSMO_DL_HINTS_GL_MACOS  "/System/Library/Frameworks/OpenGL.framework/OpenGL"
#define COSMO_DL_HINTS_GL_WIN    "opengl32.dll"

// Static assertions (asm)
COSMO_STATIC_ASSERT_SAME_SIZE(sg_buffer, gen_sg_buffer);
COSMO_STATIC_ASSERT_SAME_ALIGNMENT(sg_pipeline, gen_sg_pipeline);
```

### 2.4 Workflow Patterns

```yaml
# .github/workflows/build.yml job sequence
jobs:
  build-tools:      # Build C/APE tools first
    steps: cosmocc, make -C tools
  validate:         # Run C tools for validation
    needs: build-tools
    steps: ./tools/check-api-sync, ./tools/validate-sources
  build:            # Main build matrix
    needs: validate
    matrix: [cosmocc-3.9.5, cosmocc-3.9.6]
  smoke-linux:      # Native runners per platform
    needs: build
  smoke-windows:
    needs: build
  smoke-macos:
    needs: build
  release:
    needs: [smoke-linux, smoke-windows, smoke-macos]
    if: startsWith(github.ref, 'refs/tags/')
```

---

## 3. Phase Plan

### Phase 0: Prerequisites (Immediate)
**Duration:** 0.5 day  
**Dependencies:** None

| Task | Owner | File |
|------|-------|------|
| Create `tools/` directory | PM | - |
| Update submodule reference | PM | `deps/sokol` |
| Backup current state | PM | - |

### Phase 1: Core C Tools (Day 1)
**Duration:** 1 day  
**Dependencies:** Phase 0

| Task | Owner | Files | Priority |
|------|-------|-------|----------|
| Implement check-api-sync.c | cosmo | `tools/check-api-sync.c` | P0 |
| Implement validate-sources.c | cosmo | `tools/validate-sources.c` | P0 |
| Create tools Makefile | seeker | `tools/Makefile` | P0 |
| Verify tool compilation | PM | - | P0 |

### Phase 2: Infrastructure (Day 1-2)
**Duration:** 1.5 days  
**Dependencies:** Phase 1

| Task | Owner | Files | Priority |
|------|-------|-------|----------|
| Create cosmo_dl_safe.h | cosmo | `shims/include/cosmo_dl_safe.h` | P0 |
| Update x11.c with safe macros | cosmo | `shims/linux/x11.c` | P1 |
| Replace build.yml | neteng | `.github/workflows/build.yml` | P0 |
| Update upstream-sync.yml | cicd | `.github/workflows/upstream-sync.yml` | P1 |
| Create cosmo-sokol.json | dbeng | `cosmo-sokol.json` | P2 |

### Phase 3: Seeker Tools (Day 2-3)
**Duration:** 1 day  
**Dependencies:** Phase 1 (Makefile)

| Task | Owner | Files | Priority |
|------|-------|-------|----------|
| Implement changelog-scan.c | seeker | `tools/changelog-scan.c` | P1 |
| Implement drift-report.c | seeker | `tools/drift-report.c` | P1 |
| Create SYNC.md | seeker | `SYNC.md` | P1 |
| Windows popen() fix | seeker | `tools/drift-report.c` | P1 |

### Phase 4: Developer Workflow (Day 3-4)
**Duration:** 1 day  
**Dependencies:** Phase 2, Phase 3

| Task | Owner | Files | Priority |
|------|-------|-------|----------|
| Create pre-commit hook | localsearch | `scripts/pre-commit-drift-check.sh` | P2 |
| Create symbol verifier | localsearch | `scripts/verify-symbols.sh` | P2 |
| Create watch manifest | localsearch | `scripts/watch-manifest.json` | P3 |
| Document in CONTRIBUTING.md | PM | `CONTRIBUTING.md` | P2 |

### Phase 5: Integration Testing (Day 4)
**Duration:** 0.5 day  
**Dependencies:** All previous phases

| Task | Owner | Description |
|------|-------|-------------|
| Local build verification | PM | All tools compile, tests pass |
| Cross-platform verification | neteng | Linux, Windows, macOS |
| CI pipeline verification | cicd | All workflow jobs pass |
| Pre-commit hook testing | localsearch | Drift detection works |

### Phase 6: Sync Execution (Day 5)
**Duration:** 0.5 day  
**Dependencies:** Phase 5

| Task | Owner | Description |
|------|-------|-------------|
| Execute submodule update | PM | `git submodule update` |
| Apply breaking change fixes | cosmo | Update gen-sokol.h signatures |
| Run full validation | PM | All tools pass |
| Create release tag | PM | v3.0.0-sync |

---

## 4. Dependency Graph

```
                    ┌─────────────────────────────────────────────────────┐
                    │                    PHASE 0                           │
                    │              Prerequisites                           │
                    └─────────────────────────────────────────────────────┘
                                           │
                    ┌──────────────────────┴──────────────────────┐
                    ▼                                              ▼
     ┌──────────────────────────┐               ┌──────────────────────────┐
     │        PHASE 1           │               │        PHASE 2           │
     │   Core C Tools (cosmo)   │◀──────────────│   Infrastructure         │
     │  check-api-sync.c        │               │   cosmo_dl_safe.h        │
     │  validate-sources.c      │               │   build.yml (neteng)     │
     │  Makefile (seeker)       │               │   upstream-sync.yml      │
     └──────────────────────────┘               └──────────────────────────┘
                    │                                              │
                    ▼                                              │
     ┌──────────────────────────┐                                  │
     │        PHASE 3           │                                  │
     │   Seeker Tools           │◀─────────────────────────────────┘
     │  changelog-scan.c        │
     │  drift-report.c          │
     │  SYNC.md                 │
     └──────────────────────────┘
                    │
                    ├──────────────────────────────────────────────┐
                    ▼                                              ▼
     ┌──────────────────────────┐               ┌──────────────────────────┐
     │        PHASE 4           │               │        PHASE 5           │
     │   Developer Workflow     │──────────────▶│   Integration Testing    │
     │  pre-commit hooks        │               │   Cross-platform verify  │
     │  verify-symbols.sh       │               │   CI pipeline verify     │
     └──────────────────────────┘               └──────────────────────────┘
                                                           │
                                                           ▼
                                               ┌──────────────────────────┐
                                               │        PHASE 6           │
                                               │   Sync Execution         │
                                               │   Submodule update       │
                                               │   Breaking change fixes  │
                                               │   Release v3.0.0         │
                                               └──────────────────────────┘
```

---

## 5. Success Criteria

### 5.1 Technical Criteria

| Criterion | Metric | Verification |
|-----------|--------|--------------|
| Tools compile | `make -C tools all` exits 0 | CI job |
| API sync verified | `./tools/check-api-sync` exits 0 | CI job |
| Sources valid | `./tools/validate-sources` exits 0 | CI job |
| Cross-platform | Works on Linux, Windows, macOS | Smoke tests |
| No Python required | Zero Python in CI | Workflow audit |
| Submodule current | Drift = 0 commits | drift-report.c |

### 5.2 Philosophy Criteria

| Criterion | Metric |
|-----------|--------|
| APE binaries | All tools compile with cosmocc |
| No external deps | No pip, no npm, no runtime requirements |
| Single source | One canonical implementation per tool |
| Self-contained | Works offline, no network dependencies |

### 5.3 Process Criteria

| Criterion | Metric |
|-----------|--------|
| Pre-commit catches drift | Test with known-bad submodule |
| CI catches breaking changes | Force-trigger with stale API |
| Documentation complete | SYNC.md, CONTRIBUTING.md updated |
| Release artifacts | Checksums, provenance, changelog |

---

## 6. Risk Register

### 6.1 Critical Risks (P0)

| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|------------|-------|
| Breaking API change breaks build | HIGH | CRITICAL | Pre-sync API comparison, staged rollout | cosmo |
| Windows popen() fails | MEDIUM | HIGH | Use chdir() + direct exec | seeker |
| gen-sokol.h signature mismatch | HIGH | CRITICAL | Static assertions, incremental update | asm |

### 6.2 High Risks (P1)

| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|------------|-------|
| Multi-line declarations parse wrong | MEDIUM | MEDIUM | Strip inline comments fix | cosmo |
| Date parsing fails on new format | LOW | MEDIUM | Multi-format parser | seeker |
| CI runner unavailable | LOW | HIGH | Fallback to ubuntu-latest | neteng |

### 6.3 Medium Risks (P2)

| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|------------|-------|
| Empty file passes validation | LOW | LOW | Minimum size check | cosmo |
| Pointer type whitespace mismatch | MEDIUM | LOW | Normalize before compare | cosmo |
| Makefile error not propagated | LOW | LOW | Explicit error check | neteng |

### 6.4 Accepted Risks (Deferred)

| Risk | Rationale |
|------|-----------|
| Full macOS backend incomplete | Major effort, separate project |
| Vulkan backend not supported | Experimental upstream |
| gen-sokol not rewritten in C | Large scope, works as-is |
| ARM64 CI not available | Infrastructure not ready |

---

## 7. Timetable & Milestones

### Week 1 Schedule

| Day | Phase | Milestone | Deliverables |
|-----|-------|-----------|--------------|
| Mon | 0, 1 | Tools foundation | `tools/` directory, check-api-sync.c skeleton |
| Tue | 1, 2 | Core complete | All C tools compile, cosmo_dl_safe.h done |
| Wed | 2, 3 | Infrastructure | build.yml deployed, seeker tools started |
| Thu | 3, 4 | Workflows | All tools complete, pre-commit hooks |
| Fri | 5, 6 | Integration | Testing complete, sync executed |

### Milestone Checkpoints

| Milestone | Date | Verification |
|-----------|------|--------------|
| M1: Tools compile | Day 2 | `make -C tools all` succeeds |
| M2: CI green | Day 3 | All workflow jobs pass |
| M3: Cross-platform | Day 4 | Smoke tests on 3 platforms |
| M4: Sync complete | Day 5 | Submodule at upstream HEAD |
| M5: Release tagged | Day 5 | v3.0.0-sync published |

---

## 8. Budget Estimates

### 8.1 USD Cost Estimate

| Category | Item | Est. Hours | Rate | Cost |
|----------|------|------------|------|------|
| Development | cosmo specialist | 8h | $150/h | $1,200 |
| Development | seeker specialist | 6h | $150/h | $900 |
| Development | neteng specialist | 4h | $150/h | $600 |
| Development | cicd specialist | 3h | $150/h | $450 |
| Development | localsearch specialist | 4h | $150/h | $600 |
| Development | dbeng specialist | 2h | $150/h | $300 |
| PM | Coordination & review | 6h | $150/h | $900 |
| Testing | Integration testing | 4h | $100/h | $400 |
| CI | GitHub Actions minutes | ~500 mins | $0.008/min | $4 |
| **TOTAL** | | **37h** | | **$5,354** |

### 8.2 Token Budget Estimate

| Phase | Activity | Est. Tokens |
|-------|----------|-------------|
| Analysis | Report reading, synthesis | 150,000 |
| Planning | This document, specialist plans | 80,000 |
| Implementation | Code generation, review | 200,000 |
| Testing | Verification, debugging | 50,000 |
| Documentation | SYNC.md, updates | 30,000 |
| **TOTAL** | | **510,000 tokens** |

### 8.3 Time Budget

| Phase | Duration |
|-------|----------|
| Total elapsed | 5 business days |
| Total effort | 37 specialist-hours |
| Critical path | Phase 0 → 1 → 5 → 6 (3.5 days) |

---

## 9. Specialist Assignment Sequence

### 9.1 Assignment Order with Justification

| Order | Specialist | Justification |
|-------|------------|---------------|
| 1 | **cosmo** | Owns core C tools (check-api-sync.c, cosmo_dl_safe.h). Everything depends on these. |
| 2 | **seeker** | Owns Makefile, changelog-scan.c, drift-report.c, SYNC.md. Depends on Phase 1 tools structure. |
| 3 | **neteng** | Owns build.yml. Needs C tools to exist before integrating into CI. |
| 4 | **cicd** | Owns upstream-sync.yml. Builds on neteng's workflow foundation. |
| 5 | **localsearch** | Owns pre-commit hooks, verify-symbols.sh. Needs all tools working first. |
| 6 | **dbeng** | Owns cosmo-sokol.json. Metadata file, low urgency, parallel-safe. |
| 7 | **asm** | Static assertions. Deferred - current checks sufficient for MVP. |
| 8 | **testcov** | Test coverage strategy. Deferred - implementation priority over testing infra. |

### 9.2 Parallel Execution Windows

```
Day 1:  [cosmo: check-api-sync.c, validate-sources.c, cosmo_dl_safe.h]
        [dbeng: cosmo-sokol.json] (parallel, no deps)
        
Day 2:  [seeker: Makefile, changelog-scan.c, drift-report.c]
        [neteng: build.yml] (parallel after cosmo done)
        
Day 3:  [seeker: SYNC.md, Windows fixes]
        [cicd: upstream-sync.yml]
        [localsearch: pre-commit hooks]
        
Day 4:  [localsearch: verify-symbols.sh, watch-manifest.json]
        [Integration testing]
        
Day 5:  [Sync execution, release]
```

---

## 10. Verification Checklist

### Pre-Implementation

- [ ] Backup current repository state
- [ ] Verify GitHub Actions quotas
- [ ] Confirm cosmocc toolchain available (3.9.5, 3.9.6)
- [ ] Review upstream sokol CHANGELOG for surprises

### Post-Phase 1

- [ ] `tools/check-api-sync.c` compiles with cosmocc
- [ ] `tools/validate-sources.c` compiles with cosmocc
- [ ] Both tools exit 0 with current state

### Post-Phase 2

- [ ] `cosmo_dl_safe.h` included without errors
- [ ] `x11.c` uses safe macros
- [ ] `build.yml` syntax valid (act --dryrun)

### Post-Phase 3

- [ ] `changelog-scan.c` parses real CHANGELOG
- [ ] `drift-report.c` shows 1032 commits behind
- [ ] `SYNC.md` documents complete process

### Post-Phase 4

- [ ] Pre-commit hook blocks on drift
- [ ] `verify-symbols.sh` lists expected symbols
- [ ] CONTRIBUTING.md updated

### Post-Phase 5

- [ ] Linux smoke test passes
- [ ] Windows smoke test passes
- [ ] macOS smoke test passes
- [ ] All CI jobs green

### Post-Phase 6

- [ ] Submodule at upstream HEAD
- [ ] Breaking changes resolved
- [ ] Release v3.0.0-sync tagged
- [ ] Checksums published

---

## 11. State Tracking

```json
{
  "synthesis_date": "2026-02-09",
  "pm.complete": false,
  "phases": {
    "0": { "status": "pending", "owner": "PM" },
    "1": { "status": "pending", "owner": "cosmo" },
    "2": { "status": "pending", "owner": "cosmo,neteng" },
    "3": { "status": "pending", "owner": "seeker" },
    "4": { "status": "pending", "owner": "localsearch" },
    "5": { "status": "pending", "owner": "PM,all" },
    "6": { "status": "pending", "owner": "PM" }
  },
  "specialists_assigned": {
    "cosmo": false,
    "seeker": false,
    "neteng": false,
    "cicd": false,
    "localsearch": false,
    "dbeng": false,
    "asm": "deferred",
    "testcov": "deferred"
  },
  "blocking_issues": [],
  "next_action": "Create specialist plans"
}
```

---

*Overarching Plan Complete*  
*Next: Generate individual specialist plans and stage prompts*
