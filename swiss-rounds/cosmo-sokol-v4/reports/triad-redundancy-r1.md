# Triad Redundancy Check — cosmo-sokol-v4 Round 1

**Phase:** Triad Phase 1 — Redundancy Check  
**Generated:** 2026-02-09T19:20:00-07:00  
**Project Philosophy:** Cosmopolitan C-only, APE binaries, NO interpreters

---

## Executive Summary

After analyzing all 8 specialist reports, I've identified **4 critical philosophy violations**, **6 overlapping proposals**, and **11 existing mature tools** that could replace proposed custom solutions. The project is largely well-scoped, but there are several areas where existing Cosmopolitan ecosystem tools should be leveraged instead of building from scratch.

---

## 🚨 CRITICAL: Philosophy Violations

### 1. Python Generator Script — MUST REPLACE

**Location:** `shims/sokol/gen-sokol` (Python script)  
**Flagged by:** neteng, localsearch, cicd  
**Problem:** Uses Python interpreter to generate C code

**EXISTING TOOL — Use Instead:**
- **[m4](https://www.gnu.org/software/m4/)** — Macro processor, pure C, easily compiled with cosmocc
- **sed/awk** — Already in Cosmopolitan as `sed.com` and `awk.com`
- **Custom C codegen** — Write a simple C program that reads sokol headers and generates dispatch code

**How m4 works:** M4 is a text macro processor that reads input, processes macro definitions, and outputs expanded text. It's the classic Unix tool for code generation. Define macros for each sokol function pattern, feed it a list of function signatures, output the C dispatch layer.

```bash
# Example: Build m4 as APE binary
cosmocc -o m4.com m4/*.c
./m4.com sokol_dispatch.m4 > sokol_cosmo.c
```

**Recommendation:** Write a 200-line C tool that parses `sokol_app.h` function declarations and generates `sokol_cosmo.c`. This is a one-time cost that removes Python forever.

---

### 2. No Testing Framework — Don't Use Python-based Ones

**Flagged by:** testcov, cicd  
**Problem:** Multiple reports suggest testing but don't specify tools. Risk of importing pytest/unittest.

**EXISTING TOOL — Use Instead:**
- **[µnit](https://github.com/nemequ/munit)** — Single-header C testing framework, compiles with cosmocc
- **[greatest](https://github.com/silentbicycle/greatest)** — Another single-header C test framework
- **Cosmopolitan's own test suite** — Uses simple `assert()` + `printf()` patterns

**How µnit works:** Drop the header into your project, write test functions with `MUNIT_TEST()` macro, register them in a test suite, link and run. No interpreters, no build system dependencies — just C.

```c
// tests/smoke_test.c
#include "munit.h"

static MunitResult test_sapp_isvalid(const MunitParameter params[], void* data) {
    munit_assert_false(sapp_isvalid()); // Before setup
    return MUNIT_OK;
}
```

---

### 3. CI/CD Changelog Generation — Avoid Shell-to-Python Patterns

**Location:** cicd report recommends changelog generation  
**Problem:** Easy to slip in Python/Node for markdown processing

**EXISTING TOOL — Use Instead:**
- **git log --format** — Pure Git, no interpreter
- **[chag](https://github.com/mtdowling/chag)** — Shell-based changelog tool
- **Custom C tool** — 50 lines of C to format git log output

**How it works:** Git's `--format` option is Turing-complete for changelog needs:
```bash
git log --pretty=format:"- %s (%h)" v1.0..HEAD > CHANGELOG.md
```

---

### 4. Upstream Sync — Avoid GitHub Actions Scripting Creep

**Flagged by:** cicd, seeker  
**Problem:** Proposed sync workflow uses shell scripting that could grow into Python

**EXISTING TOOL — Use Instead:**
- **git submodule update** — Already handles deps/sokol sync
- **[git-subrepo](https://github.com/ingydotnet/git-subrepo)** — Pure Git alternative
- **Simple Makefile target** — Pure POSIX shell in Makefile

---

## 🔄 Overlapping Proposals Across Specialists

### Overlap 1: Function Manifest Generation (6 specialists)

**Who proposed it:** asm, cicd, cosmo, dbeng, localsearch, testcov, seeker, neteng  
**Observation:** Every specialist independently generated function manifests

**Consolidation:** These should have been done ONCE with a shared C tool that:
1. Parses C headers for function signatures
2. Outputs JSON/Markdown manifest
3. Can be run in CI to verify no drift

**EXISTING TOOL:** **[ctags](https://github.com/universal-ctags/ctags)** — Compiles with cosmocc, outputs function index. Alternatively, use Cosmopolitan's built-in tools.

---

### Overlap 2: Platform Support Matrix (5 specialists)

**Who repeated it:** asm, cicd, dbeng, neteng, testcov  
**Observation:** Each report recreates the same Windows ✅ / Linux ✅ / macOS ⚠️ table

**Consolidation:** Single `PLATFORM_STATUS.md` file in repo root, updated by CI.

---

### Overlap 3: macOS Implementation Discussion (4 specialists)

**Who discussed it:** asm, cicd, cosmo, neteng  
**Observation:** All mention "needs Objective-C runtime" but none propose solution

**EXISTING APPROACH — Already Documented:**
Cosmopolitan supports calling Objective-C via `objc_msgSend()` from C. This is documented in:
- jart/cosmopolitan issue #123 (macOS runtime)
- The pattern is: `dlopen("libobjc.dylib")` + `objc_msgSend` trampolines

This is the ONLY viable path. No new tools needed — just implementation work.

---

### Overlap 4: Build Verification (3 specialists)

**Who proposed it:** cicd, testcov, neteng  
**Observation:** Each proposes slightly different smoke tests

**Consolidation:** Single `tests/smoke.c`:
```c
int main(void) {
    #ifdef __COSMOPOLITAN__
    printf("✓ APE binary\n");
    #endif
    return 0;
}
```

---

### Overlap 5: Dynamic Library Loading Documentation (3 specialists)

**Who covered it:** asm, cosmo, localsearch  
**Observation:** Each explains `cosmo_dlopen`/`cosmo_dltramp` independently

**Consolidation:** Already documented in Cosmopolitan. Reference, don't re-document.

---

### Overlap 6: sokol API Coverage Lists (All 8 specialists)

**Observation:** Every report lists the same ~116 sokol_app + sokol_gfx functions

**Problem:** Massive redundancy across 250KB of reports  
**Solution:** Single `API_COVERAGE.md` maintained automatically from sokol headers

---

## ✅ Existing Mature Tools to Prescribe

### For Code Generation (Replace Python gen-sokol)

| Tool | GitHub | How It Works | Compiles with cosmocc |
|------|--------|--------------|----------------------|
| **m4** | GNU project | Text macro processor — define templates, feed data, output code | ✅ Yes |
| **re2c** | [re2c/re2c](https://github.com/skvadrik/re2c) | Lexer generator — outputs C code from regex specs | ✅ Yes |
| **ragel** | [adrian-thurston/ragel](https://github.com/adrian-thurston/ragel) | State machine compiler — outputs C | ✅ Yes |

**Recommendation:** M4 is simplest. Pattern:
```m4
define(`DISPATCH_FUNC', `
$2 $1($3) {
    if (IsLinux()) { return linux_$1($4); }
    if (IsWindows()) { return windows_$1($4); }
    if (IsXnu()) { return macos_$1($4); }
}')
DISPATCH_FUNC(sapp_isvalid, bool, void, )
DISPATCH_FUNC(sapp_width, int, void, )
```

---

### For Testing

| Tool | GitHub | How It Works | Compiles with cosmocc |
|------|--------|--------------|----------------------|
| **µnit** | [nemequ/munit](https://github.com/nemequ/munit) | Single-header test framework — `MUNIT_TEST()` macros, assertions, suites | ✅ Yes |
| **greatest** | [silentbicycle/greatest](https://github.com/silentbicycle/greatest) | Single-header — even simpler than munit | ✅ Yes |
| **snow** | [mortie/snow](https://github.com/mortie/snow) | BDD-style single-header tests | ✅ Yes |

**Recommendation:** greatest.h is 1 file, zero config:
```c
#include "greatest.h"
TEST smoke_test() { ASSERT(1); PASS(); }
SUITE(all) { RUN_TEST(smoke_test); }
GREATEST_MAIN_DEFS();
int main(int argc, char **argv) {
    GREATEST_MAIN_BEGIN();
    RUN_SUITE(all);
    GREATEST_MAIN_END();
}
```

---

### For Documentation Generation

| Tool | GitHub | How It Works | Compiles with cosmocc |
|------|--------|--------------|----------------------|
| **cmark** | [commonmark/cmark](https://github.com/commonmark/cmark) | C Markdown parser/renderer | ✅ Yes |
| **lowdown** | [kristapsdz/lowdown](https://github.com/kristapsdz/lowdown) | Markdown→HTML/man/LaTeX in C | ✅ Yes |

---

### For Function Indexing / Static Analysis

| Tool | GitHub | How It Works | Compiles with cosmocc |
|------|--------|--------------|----------------------|
| **ctags** | [universal-ctags/ctags](https://github.com/universal-ctags/ctags) | Parses C/C++/etc, outputs function index | ✅ Yes |
| **cscope** | [cscope.sourceforge.io](http://cscope.sourceforge.io/) | Symbol database for C | ✅ Yes |

**How ctags works:** Run `ctags -R .` → generates `tags` file with every function, struct, macro. Parse this file (it's plain text) for API manifests.

---

### For CI/CD Tooling

| Tool | How It Works | Notes |
|------|--------------|-------|
| **GNU Make** | Already cross-platform, pure POSIX | Don't add CMake/Meson |
| **busybox** | Cosmopolitan includes busybox APE | `sh`, `grep`, `sed`, `awk` as single binary |

---

## 🎯 Scope Creep Warnings

### 1. macOS Full Implementation — OUT OF SCOPE for v1

**Who mentioned it:** All specialists discuss macOS  
**Reality check:** macOS support requires:
- Objective-C runtime calls via `objc_msgSend`
- Cocoa/AppKit window creation
- Metal or OpenGL via CAMetalLayer

**Recommendation:** Keep stubs for v1. macOS is v2 scope. Don't let it delay shipping.

---

### 2. Audio Backend — OUT OF SCOPE

**Seeker report mentions:** `sokol_audio.h`  
**Reality:** cosmo-sokol currently only implements sokol_app + sokol_gfx

**Recommendation:** Do NOT add audio until gfx is stable. Audio brings CoreAudio/WASAPI/ALSA complexity.

---

### 3. WebGPU Backend — OUT OF SCOPE

**Several reports mention:** `sapp_wgpu_*` functions  
**Reality:** WebGPU requires Dawn/wgpu-native runtime

**Recommendation:** Stub these forever on desktop. WGPU is for WASM builds only.

---

### 4. D3D11 Backend — QUESTIONABLE SCOPE

**Windows reports mention:** Direct3D11 support  
**Reality:** OpenGL works fine on Windows. D3D11 adds complexity for marginal benefit.

**Recommendation:** OpenGL-only for v1. D3D11 is v2 if users demand it.

---

## 📋 Action Items for Next Round

### MUST DO (Philosophy Compliance)

1. ⬜ **Replace `gen-sokol` Python script** with C/m4 code generator
2. ⬜ **Add `tests/` directory** with pure C smoke tests using greatest.h
3. ⬜ **Document in CONTRIBUTING.md**: NO Python, NO Node, NO interpreters

### SHOULD DO (Deduplication)

4. ⬜ Create single `API_COVERAGE.md` generated by ctags
5. ⬜ Create single `PLATFORM_STATUS.md` 
6. ⬜ Remove duplicate function manifests from specialist reports

### COULD DO (Nice to Have)

7. ⬜ Add `make check` target that runs smoke tests
8. ⬜ Add pre-commit hook that verifies no *.py or *.js files added
9. ⬜ Document macOS path forward (objc_msgSend pattern)

---

## Summary

| Category | Count | Severity |
|----------|-------|----------|
| Philosophy Violations | 4 | 🔴 CRITICAL |
| Overlapping Proposals | 6 | 🟡 MEDIUM |
| Existing Tools Available | 11 | 🟢 INFO |
| Scope Creep Risks | 4 | 🟡 MEDIUM |

The project is fundamentally sound. The main risk is the Python generator script — this MUST be replaced before v1 release to maintain Cosmopolitan philosophy integrity. All other issues are deduplication or documentation cleanup.

---

*Generated by Redundancy Checker for Swiss Rounds v4 — Triad Phase 1*
