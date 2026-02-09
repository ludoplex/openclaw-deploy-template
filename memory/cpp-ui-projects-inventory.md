# C/C++ UI Projects Inventory

**Generated:** 2026-02-09T00:45 MST (Overnight Mission)
**Last Updated By:** testcov subagent

## Summary Table

| Project | UI Library | Current State | Refactor Needed | Priority |
|---------|-----------|---------------|-----------------|----------|
| mhi-procurement | sokol + cimgui | ✅ Correct cosmo-sokol pattern | No | - |
| tedit-cosmo | cimgui (GLFW) | ⚠️ Platform-specific GUI | Yes | HIGH |
| e9studio | None (CLI) | CLI tools only | No GUI planned? | LOW |
| cosmo-disasm | None (library) | Pure library | N/A | - |
| apeswarm | cimgui (WASM) | WASM/browser UI | Different pattern | MEDIUM |
| BallisticsCalculator | None (library) | C library | N/A | - |
| llamafile-llm | Unknown | Directory exists but empty | Investigate | - |

---

## Detailed Project Analysis

### 1. mhi-procurement ✅ **REFERENCE IMPLEMENTATION**

**Path:** `C:\mhi-procurement`
**Repo:** https://github.com/ludoplex/mhi-procurement

**UI Library:** Sokol (sokol_app, sokol_gfx) + cimgui/Dear ImGui

**Architecture:** ✅ **CORRECT cosmo-sokol pattern**
- Uses prefix trick: `linux_sapp_*`, `windows_sapp_*`
- Runtime dispatch via `sokol_cosmo.c` with `IsWindows()`/`IsLinux()`
- All platform backends compiled INTO the APE
- System libs (X11, OpenGL) loaded via dlopen
- Shims directory: `shims/sokol/`, `shims/linux/`, `shims/win32/`
- Generator scripts for X11, GL, and Sokol dispatch

**Build Status:**
- CI: ✅ GitHub Actions (`build.yml`, `sanitizers.yml`, `security.yml`)
- Tests: ✅ Sanitizer tests (ASAN, UBSAN, MSAN, TSAN)
- Local changes: Many files modified (active development)

**Key Files:**
- `shims/sokol/sokol_cosmo.c` - Runtime dispatcher
- `shims/sokol/sokol_linux.c` - Linux platform (prefixed)
- `shims/sokol/sokol_windows.c` - Windows platform (prefixed)
- `shims/linux/x11.c` - X11 dlopen stubs
- `shims/linux/gl.c` - OpenGL dlopen stubs
- `nvapi/nvapi.c` - NVIDIA threaded optimization fix

**Refactor Needed:** No - this IS the reference implementation

---

### 2. tedit-cosmo ⚠️ **NEEDS REFACTOR**

**Path:** `C:\tedit-cosmo`
**Repo:** https://github.com/ludoplex/tedit-cosmo

**UI Library:** cimgui (C bindings for Dear ImGui) + GLFW + OpenGL

**Architecture:** ❌ **Platform-specific GUI mode**
- CLI mode works with cosmocc (APE)
- GUI mode uses GLFW/OpenGL directly (native only)
- No cosmo-sokol integration
- GUI backend: `src/platform/cimgui_backend.c` uses GLFW directly

**Build Status:**
- CI: ✅ GitHub Actions (`ci.yml`) - builds CLI APE
- Tests: ✅ Unity test framework (`tests/test_buffer.c`, `tests/test_history.c`)
- CLI: Builds and runs as APE
- GUI: Only works with native toolchain

**Current Makefile Targets:**
```makefile
cli:  # CLI-only APE with cosmocc ✅ Works
gui:  # GUI with native toolchain (GLFW/GL) - NOT portable
```

**Refactor Needed:** YES - HIGH PRIORITY
- Replace GLFW with Sokol (sokol_app)
- Implement cosmo-sokol pattern from mhi-procurement
- Add shims directory structure
- Generate platform dispatch code
- Update CI to build GUI APE

**Work Estimate:** 2-4 days
- Copy shims structure from mhi-procurement
- Adapt cimgui_backend.c to use sokol_app instead of GLFW
- Add CI workflow for GUI APE build/test

---

### 3. e9studio (CLI Only)

**Path:** `C:\e9studio`
**Repo:** https://github.com/ludoplex/e9studio

**UI Library:** None (CLI tools)

**Architecture:** 
- e9patch and e9tool are CLI utilities
- Binary rewriting/patching tools
- Has IDE plugin support (CLion bridge, Notepad++ plugin)
- WASM host support for e9patch.wasm

**Build Status:**
- CI: ✅ GitHub Actions (`build-e9studio.yml`)
- Tests: ✅ Vendor library tests, self-test
- Builds as APE with cosmocc
- Tested on Linux, macOS Intel, macOS ARM

**GUI Plans:** 
- `src/e9patch/ide/` suggests IDE integration focus
- `contrib/ide-plugins/notepadpp-e9patch/` - Notepad++ plugin
- No standalone GUI planned (designed for IDE integration)

**Refactor Needed:** No (CLI by design)
- Future possibility: GUI wrapper using cosmo-sokol
- Would show disassembly, patch status, etc.

**Priority:** LOW - works well as CLI

---

### 4. cosmo-disasm (Library Only)

**Path:** `C:\cosmo-disasm`
**Repo:** https://github.com/ludoplex/cosmo-disasm

**UI Library:** None (pure library)

**Architecture:**
- Static library (`libcosmo_disasm.a`)
- x86 and ARM64 disassembly support
- Designed for integration into other projects
- tedit-cosmo has optional integration (`DISASM=1`)

**Build Status:**
- CI: ❌ No GitHub Actions workflows found
- Tests: ✅ `test/test_disasm.c`
- Builds with cosmocc

**Refactor Needed:** N/A (library, not application)

---

### 5. apeswarm (WASM UI)

**Path:** `C:\apeswarm`
**Repo:** https://github.com/ludoplex/apeswarm

**UI Library:** cimgui compiled to WASM (Emscripten)

**Architecture:** Different paradigm
- Server: Native Cosmopolitan APE (WebSocket server)
- Client: WASM module rendered in browser
- Uses cimgui but compiled to `app.wasm`
- Framebuffer blitted to HTML canvas

**Build Status:**
- CI: ✅ GitHub Actions (`ci.yml`, `pr-check.yml`, `release.yml`, `security.yml`)
- Tests: ✅ Unity tests in `tests/c/`

**Key Files:**
- `client/wasm-ui-cimgui/src/ui_main.c` - WASM UI entry point
- `server/src/main.c` - APE server

**Refactor Needed:** Different pattern (WASM-based)
- Not using native GUI - uses browser rendering
- Could add native GUI client using cosmo-sokol
- **Priority:** MEDIUM - if native client desired

---

### 6. BallisticsCalculator (Library Only)

**Path:** `C:\BallisticsCalculator`
**Repo:** Not a GitHub repo (local only?)

**UI Library:** None (C library)

**Architecture:**
- Pure C ballistics calculation library
- SQLite database support
- Objective-C wrapper for iOS
- Test framework included

**Build Status:**
- Uses native gcc (not cosmocc)
- Comprehensive test suite (valgrind, coverage)

**Refactor Needed:** N/A (library, not application)
- Could wrap with cosmo-sokol GUI for visualization
- Would be a new project rather than refactor

---

### 7. llamafile-llm (Unknown/Empty)

**Path:** `C:\llamafile-llm`
**Status:** Directory exists but appears to have no C/C++ source files

**Investigation Needed:**
- May be placeholder for future llamafile integration
- Check if this should use llamafile's DSO pattern for GPU
- Different from cosmo-sokol (compute vs GUI)

---

## Reference Implementation

**bullno1/cosmo-sokol:** `C:\cosmo-sokol-ref`

**Key Concepts:**
1. **Prefix trick** - Compile each platform with symbol prefix
2. **Runtime dispatch** - `sokol_cosmo.c` routes to correct platform
3. **dlopen for system libs** - X11, OpenGL from host system
4. **Single APE binary** - All backends compiled in, no DSOs

**Generator Scripts:**
- `gen-sokol` - Generates prefix defines and cosmo dispatch
- `gen-x11` - Generates X11 dlopen stubs
- `gen-gl` - Generates OpenGL dlopen stubs

**CI Status:** ✅ Passing (`build.yml`)

---

## Skill Reference

**Location:** `C:\Users\user\.openclaw\workspace\skills\sokol-cosmo\SKILL.md`

Key takeaways:
- cosmo-sokol ≠ raw sokol
- llamafile pattern (DSO extraction) ≠ cosmo-sokol pattern
- All GUI code goes IN the APE, not in separate DLLs
- System graphics libs (X11, GL) are dlopen'd from host

---

## Recommended Actions

### Immediate (High Priority)
1. **tedit-cosmo GUI refactor**
   - Copy `shims/` structure from mhi-procurement
   - Replace GLFW with sokol_app
   - Integrate with existing cimgui code
   - Add CI workflow for GUI APE

### Future (Medium Priority)
2. **apeswarm native client option**
   - Alternative to WASM browser client
   - Use cosmo-sokol for native rendering

### Low Priority / Optional
3. **e9studio GUI wrapper**
   - Standalone GUI for binary patching
   - Use cosmo-sokol pattern

4. **BallisticsCalculator visualization tool**
   - New project: ballistics visualizer
   - Trajectory plotting with sokol_gfx

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     APE Binary (e.g., app.com)                  │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │ linux_sapp_*│  │windows_sapp_│  │ macos_sapp_*│  Platform   │
│  │ (prefixed)  │  │ (prefixed)  │  │ (prefixed)  │  Backends   │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘              │
│         │                │                │                     │
│         └────────┬───────┴────────┬───────┘                     │
│                  │                │                             │
│           ┌──────▼──────┐  ┌──────▼──────┐                      │
│           │sokol_cosmo.c│  │  App Code   │                      │
│           │ (dispatch)  │  │ (cimgui UI) │                      │
│           └──────┬──────┘  └─────────────┘                      │
│                  │                                              │
│                  ▼                                              │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ IsWindows()? → windows_sapp_run()                          │ │
│  │ IsLinux()?   → linux_sapp_run()   → dlopen(libX11, libGL)  │ │
│  │ IsXnu()?     → macos_sapp_run()                            │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## Other C/C++ Projects Checked (No UI)

| Directory | Type | Notes |
|-----------|------|-------|
| `C:\dev\` | Various | Development area, check for projects |
| `C:\d\` | Unknown | Single-letter dir, likely temp |
| `C:\scripts\` | Scripts | Not C/C++ |
| `C:\ecosystem\` | Unknown | Check contents |
| `C:\masm64-*` | Assembly | MASM projects, not C |
| `C:\GUNDOM\` | Unknown | Game? Check for UI |

---

## Notes for Vincent

1. **mhi-procurement is the gold standard** - use it as template for other projects
2. **tedit-cosmo is top refactor priority** - text editor needs portable GUI
3. **cosmo-disasm integration** - tedit-cosmo already supports it optionally
4. **apeswarm uses different paradigm** - WASM/browser, valid for its use case
5. **e9studio works great as CLI** - IDE integration preferred over standalone GUI
