# Swiss Rounds Triad — Round 1 Redundancy Review

**Project:** cosmo-sokol-v2  
**Reviewer:** redundant-project-checker  
**Date:** 2026-02-09  

---

## Feedback for seeker

### What's Missing from Web Resource Collection

1. **sokol-shdc (Shader Compiler)**
   - Missing: `https://github.com/floooh/sokol-tools` with details on sokol-shdc binary releases
   - The shader compilation toolchain is critical for anyone extending cosmo-sokol's shaders
   - Should have checked for prebuilt binaries at `https://github.com/floooh/sokol-tools-bin`

2. **Cosmopolitan dlopen Limitations**
   - You found the dlopen directory but didn't find the explicit documentation about macOS x86-64 being unsupported
   - Missing: The README or documentation explaining `cosmo_dlopen` naming differences
   - This is crucial context the cosmo specialist covered but you could have surfaced from web sources

3. **APE Format Documentation**
   - Listed `https://justine.lol/ape.html` but didn't extract key technical details
   - Missing: The actual polyglot header format (`MZqFpD`) that neteng covered
   - Users need to understand why the binary works everywhere

4. **cimgui Generator Process**
   - You linked the generator directory but didn't explain HOW to regenerate bindings after upstream ImGui updates
   - Missing: Dependencies for cimgui generation (luajit, etc.)

5. **Cosmopolitan NT Function Additions**
   - PR #1318 mentioned but no detail on WHAT NT functions were added for sokol compatibility
   - This is directly relevant to Windows support

### Links That Should Have Been Found

- `https://github.com/floooh/sokol-tools-bin` — Prebuilt shader compiler binaries
- `https://github.com/jart/cosmopolitan/blob/master/libc/dce.h` — Platform detection header (exact location)
- `https://github.com/jart/cosmopolitan/blob/master/libc/nt/master.sh` — Windows import generator
- `https://discord.gg/FwAVVu7eJ4` — Listed but should confirm this is the correct Cosmopolitan community link
- Any blog posts by floooh about sokol architecture decisions

### Specific Gaps in Deliverable

- No version comparison between sokol commits (what changed between bullno1's pinned commit and upstream HEAD)
- No link to sokol's own sample code that demonstrates D3D11/GL/Metal backends
- Missing cimgui's own documentation about C++ to C wrapper generation

---

## Feedback for localsearch

### What Local Files Were Missed

1. **nvapi/ Directory**
   - The build script references `nvapi/nvapi.c` with `${WIN32_FLAGS}` and `compile nvapi/nvapi.c`
   - You didn't explore or document this NVIDIA API integration at all
   - This is Windows-specific GPU optimization code

2. **win32_tweaks.c**
   - Referenced in build script: `compile win32_tweaks.c ${WIN32_FLAGS}`
   - Not documented — what Windows-specific tweaks does this contain?

3. **main.c**
   - The actual application entry point is mentioned but not excerpted
   - Should have shown the `sokol_main()` implementation and how it ties everything together

4. **sokol_shared.c and sokol_cosmo.c**
   - Build script shows: `compile shims/sokol/sokol_shared.c` and `compile shims/sokol/sokol_cosmo.c`
   - You documented sokol_linux.c, sokol_windows.c, sokol_macos.c but NOT these shared files
   - sokol_cosmo.c is the CRITICAL dispatch layer the asm specialist analyzed

5. **Header Files in shims/**
   - `sokol_linux.h`, `sokol_windows.h`, `sokol_macos.h` — only .c files were documented
   - Headers would show the interface contract

6. **.gitmodules**
   - Shows exact submodule URLs and branch tracking

### What Code Snippets Should Have Been Included

- The runtime dispatch pattern from `sokol_cosmo.c` (if/else chain with IsLinux(), IsWindows(), IsXnu())
- The `cosmo_dltramp` wrapper usage in gl.c and x11.c
- Window creation code from sokol_windows.c or sokol_macos.c
- Any shader-related code or glue

### Specific Gaps in Deliverable

- Function counts for each platform backend (812 lines for macOS but what does it do?)
- No analysis of what platform-specific APIs each backend uses
- Missing the `scripts/compile` helper that parallel execution uses
- No mention of the `bin/` output directory structure

---

## Feedback for asm

### What's Missing from ABI Analysis

1. **Actual Size Verification**
   - You estimated struct sizes ("~280-320 bytes") but testcov specialist has ACTUAL sizes:
     - `sapp_desc`: 472 bytes (not 280-320)
     - `sg_desc`: 208 bytes (not 120-150)
     - `sg_bindings`: 328 bytes (not 440)
   - You should have compiled and run sizeof() checks

2. **ARM64 Analysis**
   - Report focuses entirely on x86_64
   - Cosmopolitan now supports ARM64 (SUPPORT_VECTOR includes ARM subset)
   - What's the calling convention for ARM64? (AAPCS64)
   - macOS Silicon uses ARM64 — this is production-relevant

3. **SIMD/Vector Register Usage**
   - Sokol uses SIMD for graphics math
   - How do xmm0-xmm7 (Linux) vs xmm0-xmm3 (Windows) affect passing sg_color or matrix types?

4. **Struct Packing Pragmas**
   - Did you check for `#pragma pack` directives in sokol headers?
   - Some graphics APIs require specific packing

5. **Varargs Functions**
   - Any sokol logging or debug functions use printf-style varargs?
   - Varargs have different ABI handling

### Missing Platform-Specific Details

- FreeBSD/OpenBSD calling conventions (same as Linux System V, but confirm)
- NetBSD specifics
- What happens when macos x86-64 dlopen fails silently?

### Specific Gaps in Deliverable

- No verification of `#pragma GCC diagnostic ignored "-Wreturn-type"` correctness
- Missing: What's the actual `IsLinux()` implementation? (cosmo specialist covered it)
- Should have cross-referenced with testcov's `_Static_assert` approach

---

## Feedback for cosmo

### What's Missing from Cosmopolitan Analysis

1. **Gen-X11 and Gen-GL Scripts**
   - You covered `cosmo_dlopen`/`cosmo_dlsym` but not the GENERATED stubs
   - localsearch found gen-x11 (180 lines) and gen-gl (94 lines) — these generate the dlopen shims
   - How are X11 functions stubbed? What's the FUNCTIONS dict?

2. **binfmt_misc Registration**
   - neteng mentioned APE binfmt handlers: `:APE:M::MZqFpD::`
   - You didn't cover how Linux recognizes APE binaries

3. **foreign_thunk_sysv / foreign_thunk_nt**
   - You mentioned `cosmo_dltramp` calls these but didn't detail the actual thunk generation
   - Where is the trampoline code? Is it generated at runtime?

4. **__syslib Structure**
   - Mentioned for macOS Silicon but didn't show the full interface
   - What version introduced dlopen support? (v6, 2023-11-03)

5. **BLOCK_SIGNALS / BLOCK_CANCELATION Macros**
   - These appear in cosmo_dlopen but you didn't explain them
   - Thread safety mechanism — how do they work?

### Missing Version-Specific Details

- What's in v4.0.0 that's a "Major release"?
- Any breaking changes between 3.9.5 (minimum) and 3.9.6 (pinned)?
- v4.0.2 includes "Fork fixes, Windows improvements" — specifics?

### Specific Gaps in Deliverable

- No discussion of the "foreign helper executable" compilation process (what's in ~/.cosmo/dlopen-helper?)
- Missing: How does Cosmopolitan handle threading across platforms?
- Should have covered `SupportsX()` compile-time macros vs runtime `IsX()` checks

---

## Feedback for neteng

### What's Missing from Infrastructure Analysis

1. **Actual Binary Testing Results**
   - You listed platforms but marked most as "Not tested"
   - No evidence of actually running the binary anywhere
   - At minimum, could have documented Windows execution (your analysis mentions Windows manual testing)

2. **SHA256 Checksums**
   - You identified this as a HIGH priority gap but didn't GENERATE them
   - Should have: `sha256sum cosmo-sokol.zip` output from releases

3. **APE Loader Distribution**
   - You mentioned ape-x86_64.elf and ape.exe but not how they're distributed with the binary
   - Are they embedded? External? First-run extracted?

4. **Gatekeeper Bypass Details**
   - Mentioned `xattr -d com.apple.quarantine` but what about notarization?
   - Apple's requirements for running unsigned code are more complex

5. **Wine Testing**
   - Listed as an option but no actual test results
   - Would be valuable for Linux CI testing Windows execution

### Missing Distribution Details

- No size breakdown (what's taking 4MB? Is it mostly cosmo runtime?)
- No analysis of stripping debug symbols
- No comparison with native sokol builds (how much overhead does Cosmopolitan add?)

### Specific Gaps in Deliverable

- Security analysis is incomplete (SBOM mentioned but not created)
- No CDN or mirror recommendations for high-availability distribution
- Missing: How to verify the downloaded binary matches what CI built

---

## Feedback for cicd

### What's Missing from CI/CD Analysis

1. **Test Execution**
   - Your build-matrix.yml downloads artifacts and checks headers but doesn't RUN the binary
   - The smoke_test that testcov designed should be integrated
   - Windows test just checks it's a PE, doesn't verify rendering

2. **macOS Testing is Hollow**
   - Your test-macos job runs `timeout 5 "$binary" --help` which will fail for GUI apps
   - testcov explains why macOS is stub-only — your workflow doesn't acknowledge this

3. **Cosmocc Version Update Automation**
   - check-upstream.yml checks for new versions but doesn't help UPDATE
   - Should have a workflow to bump cosmocc version and test

4. **Linux X11 Dependencies**
   - Your workflows install libx11-dev etc. but these are BUILD deps
   - For runtime testing, need actual X11 server (Xvfb) — not included

5. **Submodule PR Doesn't Test**
   - update-submodule.yml creates a PR but that PR won't trigger build-matrix.yml (branches filter)
   - Need to trigger CI on the new branch

### Missing Workflow Features

- No caching of cosmocc toolchain (downloads every time)
- No parallel compilation verification (GNU parallel is used locally)
- No artifact retention policy documentation
- No dependabot or renovate configuration for action versions

### Specific Gaps in Deliverable

- The workflows reference `softprops/action-gh-release@v2` without pinning SHA
- No secrets documentation (what's needed for releases?)
- Missing: How to manually trigger release for a specific tag

---

## Feedback for testcov

### What's Missing from Test Coverage Analysis

1. **Integration with CI**
   - You designed tests but didn't show the GitHub Actions integration
   - cicd specialist's workflows don't include your smoke_test
   - Missing: `.github/workflows/test.yml` that uses your scripts

2. **Actual Struct Sizes Verification**
   - Your abi_verify.c has sizes but marked as "estimates"
   - Should have compiled and run abi_sizes.c to get ACTUAL values
   - asm specialist estimated wrong sizes — you could have corrected them

3. **API Coverage Completeness**
   - gen_api_coverage.py has ~40 gfx functions and ~30 app functions
   - localsearch found 200+ API functions declared
   - Your coverage is only ~35% of the API

4. **cimgui Testing**
   - Sokol tests are designed but ImGui is half the project
   - No ImGui-specific smoke test (create window, render text, etc.)

5. **Platform Backend Verification**
   - smoke_test.c uses `SOKOL_D3D11`, `SOKOL_GLCORE`, `SOKOL_METAL`
   - But cosmo-sokol uses a UNIFIED binary — your test doesn't reflect runtime backend selection

### Missing Test Types

- No memory leak detection (Valgrind, ASan)
- No fuzzing targets for input handling
- No performance benchmarks
- No multi-monitor/high-DPI tests

### Specific Gaps in Deliverable

- headless_test_linux.sh uses `sudo apt-get` — not suitable for all Linux distros
- Windows WARP approach is speculative ("if available")
- No actual test run output showing pass/fail

---

## Cross-Report Redundancies

### Duplicated Work

1. **Platform Detection** — Both asm and cosmo analyze `IsLinux()`/`IsWindows()`. Cosmo's is more complete.

2. **Struct Sizes** — asm estimates, testcov provides assertions. Neither verified empirically.

3. **APE Format** — neteng and seeker both mention it, neteng goes deeper.

4. **cosmocc Version** — neteng, cicd, and cosmo all mention 3.9.6 pinning. cicd covers update automation.

5. **dlopen/dltramp** — asm mentions calling convention, cosmo covers implementation, localsearch found usage. Could have been consolidated.

### Information That Should Have Been Shared

- localsearch's function counts should inform testcov's API coverage
- asm's struct estimates should be verified by testcov's _Static_assert
- cosmo's platform support matrix should inform neteng's verification matrix
- seeker's upstream change info should inform cicd's update detection

---

## Summary

| Specialist | Completeness | Key Gaps |
|------------|--------------|----------|
| seeker | 70% | Missing shader tools, deeper cosmopolitan docs |
| localsearch | 75% | Missing nvapi/, win32_tweaks.c, sokol_cosmo.c |
| asm | 65% | Wrong size estimates, no ARM64, no actual verification |
| cosmo | 80% | Missing stub generation, version specifics |
| neteng | 70% | No actual testing, no checksums generated |
| cicd | 75% | Tests don't run, macOS handling incorrect |
| testcov | 60% | Low API coverage, no CI integration, no actual runs |

