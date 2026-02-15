# Swiss Rounds Triad — Round 1 Individual Critiques

**Project:** cosmo-sokol-v2  
**Critic:** project-critic subagent  
**Date:** 2026-02-09  

---

## Critique of seeker

### Lane Violation?
**N** — Stayed in lane. Web resource collection is their assigned scope.

### Usability Score: 2/5
The deliverable is a **link dump**, not an actionable resource. Links are organized by source (GitHub repos, releases) but lack:
- Extraction of key technical details from linked pages
- Version comparison data
- Direct answers to "what do I need to know?"

A developer hitting this document still has to click every link and read. The seeker was supposed to *gather* intelligence, not just hyperlinks.

### Unsubstantiated Claims
- **"Active development"** — Listed for sokol commits page without stating commit frequency or recency metrics
- **"Minimum cosmocc version: v3.9.5"** — Stated as fact under bullno1 Build Requirements but no link to where this requirement is documented
- **PR #1318 adds "NT function additions for sokol"** — Claims without explaining WHAT functions were added

### Errors Found
1. **Missing sokol-tools-bin** — The shader compiler prebuilt binaries are critical for anyone extending shaders. This is a significant gap.
2. **Missing actual version delta** — Claims there are breaking changes (lists closed PRs) but doesn't explain what broke or what the project currently pins vs upstream HEAD
3. **Rate limited during fetch** — Listed dlopen.c but admitted they couldn't actually read it. This should have been flagged as INCOMPLETE, not presented as a deliverable.
4. **cimgui generator** — Links the directory but doesn't explain the actual regeneration process or dependencies (luajit)
5. **Discord link unverified** — Lists discord.gg/FwAVVu7eJ4 as "Redbean Discord server" — is this even the right community for cosmo-sokol questions?

### Verdict
Seeker delivered a bibliography, not research. Needs to extract and synthesize, not just link.

---

## Critique of localsearch

### Lane Violation?
**N** — Stayed in lane (local file analysis).

### Usability Score: 3/5
The file inventory with line counts and first-10-lines excerpts is genuinely useful. The API function enumeration from sokol headers is thorough (200+ functions listed). However:
- Missing critical files that ARE in the build script
- No analysis of what the code DOES, just what files exist

### Unsubstantiated Claims
- **Line counts** — States "sokol_macos.c: 812 lines" without showing how this was verified (md5sum? wc -l output?)
- **"~200 API Functions Declared"** — Approximate count from manual listing, not a verified programmatic count

### Errors Found
1. **Missing nvapi/ directory** — Build script explicitly compiles `nvapi/nvapi.c`. localsearch missed it entirely. NVIDIA API integration is Windows-specific and architecturally important.

2. **Missing win32_tweaks.c** — Build script: `compile win32_tweaks.c ${WIN32_FLAGS}`. Not documented at all.

3. **Missing sokol_cosmo.c** — Build script: `compile shims/sokol/sokol_cosmo.c ${FLAGS}`. This is THE critical dispatch layer that asm specialist later analyzed. localsearch should have found it FIRST.

4. **Missing sokol_shared.c** — Build script: `compile shims/sokol/sokol_shared.c ${FLAGS}`. Another gap.

5. **Header files not documented** — Listed .c files but not corresponding .h files (sokol_linux.h, sokol_windows.h, sokol_macos.h) which define the interfaces.

6. **No .gitmodules content** — Would show exact submodule tracking branches.

7. **Submodule commits listed but not verified** — States `deps/sokol = eaa1ca79...` without showing the git submodule command output.

### Verdict
localsearch found 75% of the codebase but missed files that are LITERALLY IN THE BUILD SCRIPT. This is unacceptable—the build script is the roadmap to what matters.

---

## Critique of asm

### Lane Violation?
**N** — Stayed in lane (ABI/calling convention analysis).

### Usability Score: 2/5
Theoretical analysis only. The calling convention tables are textbook-correct but:
- Size estimates are **WRONG**
- No actual compilation to verify claims
- No ARM64 analysis despite Cosmopolitan supporting it

### Unsubstantiated Claims
1. **Struct size estimates** — All of them:
   - `sapp_desc`: claimed "~280-320 bytes" → **Actual: 472 bytes** (per testcov)
   - `sg_desc`: claimed "~120-150 bytes" → **Actual: 208 bytes** (per testcov)
   - `sg_bindings`: claimed "~440 bytes" → **Actual: 328 bytes** (per testcov)
   
   These aren't small errors. asm was off by 50-100+ bytes on critical structs. This invalidates any ABI analysis that depends on these numbers.

2. **"cosmo_dltramp wraps each pointer"** — Claims Windows uses trampolines but doesn't show actual assembly or disassembly proving this.

3. **"Generated Assembly (conceptual x86_64)"** — The word "conceptual" means they made it up. This isn't analysis, it's speculation.

4. **sg_commit_listener "potential ABI mismatch point"** — Flags a risk but doesn't verify whether cosmo-sokol even uses this function or if the mismatch actually occurs.

### Errors Found
1. **No ARM64 analysis** — ARM64 is production-relevant (macOS Silicon). Completely absent.

2. **No SIMD register analysis** — Graphics code uses SIMD extensively. xmm0-xmm7 vs xmm0-xmm3 difference between Linux/Windows could affect sg_color or matrix types. Not analyzed.

3. **Wrong struct sizes propagated** — If someone used this report for FFI binding development, their code would crash due to buffer size mismatches.

4. **#pragma pack not checked** — Claims "Alignment-Sensitive Fields" but didn't verify sokol headers for packing pragmas.

5. **Missing return-type warning analysis** — Notes `#pragma GCC diagnostic ignored "-Wreturn-type"` but doesn't analyze whether this is correct or hiding bugs.

### Verdict
asm delivered theoretical textbook knowledge dressed up as codebase analysis. The struct size errors alone make this report dangerous if used for real development. Should have compiled and run `sizeof()` checks.

---

## Critique of cosmo

### Lane Violation?
**N** — Stayed in lane (Cosmopolitan internals).

### Usability Score: 3/5
Solid documentation of cosmo_dlopen/dlsym internals with platform support matrix. The code excerpts from dlopen.c are useful. However:
- Doesn't explain how the project USES these APIs
- Missing critical context for stub generation

### Unsubstantiated Claims
1. **"Windows: Uses `LoadLibrary()`/`GetProcAddress()` directly"** — Claimed but the actual code path through dlopen_nt() isn't shown.

2. **"Foreign helper executable trick"** — Mentions `~/.cosmo/dlopen-helper` but doesn't show what this helper looks like or how it's compiled.

3. **"~600+ Win32 functions wrapped"** — Approximate count without verification.

4. **"No API breakage" between versions** — Claims v3.9.5 → v4.0.2 has no breaking changes but doesn't show a diff or methodical comparison.

### Errors Found
1. **Missing gen-x11 and gen-gl stub analysis** — localsearch found these scripts (180 and 94 lines respectively). cosmo specialist should have explained how X11/GL functions get stubbed through cosmo_dltramp. This is the bridge between Cosmopolitan and the actual cosmo-sokol shims.

2. **Missing binfmt_misc registration** — neteng mentioned `:APE:M::MZqFpD::` but cosmo specialist didn't cover how Linux recognizes APE binaries at the kernel level.

3. **Missing foreign_thunk_sysv / foreign_thunk_nt details** — Mentioned that cosmo_dltramp calls these but didn't show the actual thunk generation mechanism.

4. **No version delta details** — Claims no breaking changes but doesn't explain:
   - What's in v4.0.0 "Major release"?
   - Why is 3.9.5 minimum required?
   - What did 3.9.6 (pinned) add?

5. **BLOCK_SIGNALS / BLOCK_CANCELATION unexplained** — Copied from code but didn't explain the thread safety mechanism.

### Verdict
cosmo delivered good reference documentation but failed to connect Cosmopolitan internals to cosmo-sokol's actual usage. The stub generation gap is significant.

---

## Critique of neteng

### Lane Violation?
**N** — Stayed in lane (deployment infrastructure).

### Usability Score: 2/5
Mostly theoretical. The platform verification matrix is marked "Not tested" for 6 out of 8 platforms. This is an infrastructure report that documents no actual infrastructure testing.

### Unsubstantiated Claims
1. **"theoretically runs on Windows, Linux, macOS, and BSDs without modification"** — The word "theoretically" appears because NO TESTING WAS DONE.

2. **"APE binaries target these platforms without recompilation"** — Claimed but only Linux build was verified in CI per their own report.

3. **"~4MB binary"** — Size listed but no breakdown of what contributes to that size.

4. **Release download counts** — "v1.1.0: 28 downloads, v1.0.0: 6 downloads" — where did these numbers come from? No URL to GitHub API or screenshot.

### Errors Found
1. **No checksums generated** — Report identifies this as "HIGH priority gap" but then... doesn't generate them. The fix is one command: `sha256sum cosmo-sokol.zip`. Why not just do it?

2. **No actual binary testing** — Claimed Windows "Manual" testing but no evidence (screenshot, log output, test script).

3. **APE loader distribution unclear** — Mentions ape-x86_64.elf and ape.exe but doesn't clarify if they're embedded in the APE binary or need separate distribution.

4. **Gatekeeper bypass incomplete** — Mentions `xattr -d com.apple.quarantine` but macOS requirements are more complex (notarization, Gatekeeper CLI bypass on Sequoia, etc.).

5. **Wine testing mentioned but not done** — "Listed as an option but no actual test results."

6. **Missing size regression tracking** — Identifies as gap but proposes no solution.

### Verdict
neteng wrote a specification for what SHOULD be verified without actually verifying any of it. This is a test plan, not test results.

---

## Critique of cicd

### Lane Violation?
**N** — Stayed in lane (CI/CD workflows).

### Usability Score: 4/5
**The most usable deliverable.** Provides actual YAML workflow files that can be committed and used immediately. However, the workflows themselves have flaws.

### Unsubstantiated Claims
1. **"Test APE execution"** — The Windows test just checks for PE headers, doesn't actually RUN the binary and verify output.

2. **"Multi-platform"** — The build happens only on Ubuntu; Windows and macOS jobs just download and inspect artifacts.

3. **Workflows "test" binaries** — No actual rendering or functionality test. Just file existence and header checks.

### Errors Found
1. **macOS test is hollow** — `timeout 5 "$binary" --help` will fail for GUI apps without a display. testcov explicitly says macOS needs display for Metal. cicd's macOS job will always fail or skip actual testing.

2. **Windows test doesn't verify D3D11** — Just checks it's a PE file. Could be corrupt and still pass.

3. **No Xvfb for Linux** — Linux test could use Xvfb (as testcov documents) but doesn't. CI just builds, never renders.

4. **update-submodule.yml branch won't trigger build-matrix.yml** — The new `update-{submodule}-{sha}` branch won't match `branches: [main, master]` filter. The PR won't be tested.

5. **No cosmocc caching** — Downloads toolchain every run. Wasteful.

6. **Floating action versions** — Uses `@latest` for apt-cache and `v2` without SHA pinning. Security risk.

7. **No secrets documentation** — What secrets are needed for release creation? GITHUB_TOKEN only, or others?

8. **No artifact retention policy** — 7-day retention hardcoded but no rationale.

### Verdict
cicd delivered working YAML files (good!) but the tests are cosmetic, not functional. The macOS strategy directly contradicts testcov's analysis.

---

## Critique of testcov

### Lane Violation?
**N** — Stayed in lane (test coverage).

### Usability Score: 3/5
Provides actual C code and Python scripts. The smoke_test.c and abi_verify.c are directly usable. However:
- No CI integration shown
- API coverage is incomplete
- Tests weren't actually RUN

### Unsubstantiated Claims
1. **ABI sizes "derived from sokol headers"** — But then marked as estimates in comments. The 472/208/328 byte sizes contradict asm's estimates. Which is right? Neither verified empirically IN THE REPORT.

2. **"~40 gfx functions and ~30 app functions"** — But localsearch found 200+ API functions. That's ~35% coverage. Not mentioned.

3. **"Compile with: cc -c abi_verify.c"** — But was this actually done? No output shown.

### Errors Found
1. **No integration with CI workflows** — cicd's workflows don't reference smoke_test.c. These test assets exist in isolation.

2. **ABI sizes not verified empirically** — Comments say "MUST match for FFI bindings to work" but no evidence abi_sizes.c was compiled and run to get actual values.

3. **Low API coverage** — gen_api_coverage.py covers ~70 functions. localsearch found ~200. Missing 65% of the API surface.

4. **No cimgui testing** — Half the project is ImGui. No ImGui smoke test.

5. **Platform backend mismatch** — smoke_test.c uses `SOKOL_D3D11`/`SOKOL_GLCORE`/`SOKOL_METAL` compile-time switches. But cosmo-sokol is a UNIFIED binary with RUNTIME selection. The test model doesn't match the actual architecture.

6. **headless_test_linux.sh uses sudo apt-get** — Won't work on non-Debian systems. No Alpine/Arch/Fedora support.

7. **Windows WARP speculative** — "if available" without verifying CI runners have WARP.

8. **No actual test output** — No pass/fail logs from running the tests.

### Verdict
testcov designed tests but didn't execute them. The struct sizes are the most useful part but conflict with asm's estimates. Someone needs to actually compile abi_sizes.c and report the output.

---

## Critique of dbeng

### Lane Violation?
**PARTIAL Y** — Scope creep into speculative territory. 

The task was presumably "database/data engineering" analysis. dbeng produced JSON schemas for version tracking, compatibility matrices, and migrations. This is useful design work BUT:
- No actual data was created
- Schemas aren't validated against real cosmo-sokol data
- This is FORWARD-LOOKING design, not analysis of what exists

### Usability Score: 2/5
JSON schemas are well-structured but:
- Completely hypothetical examples (fake commit SHAs, fake dates)
- No tooling to populate or validate the schemas
- No integration with existing version tracking (submodules, build.yml pinning)

### Unsubstantiated Claims
1. **All example data is fabricated** — `a1b2c3d4e5f6789012345678901234567890abcd` is not a real commit. The "hypothetical update" section is fiction.

2. **"Current production baseline"** — Labels a fake combination as production without verifying what cosmo-sokol actually uses.

### Errors Found
1. **Schemas not validated** — No JSON Schema validator run, no CI integration to enforce schema compliance.

2. **Example commit SHAs don't match reality** — localsearch found actual commits: `eaa1ca79...` for sokol, `8ec6558e...` for cimgui. dbeng used fake SHAs.

3. **No existing data extraction** — Could have populated versions.json with REAL current data from the repo. Didn't.

4. **Migration tracking theoretical** — The gen_sokol_impact schema is detailed but there's no process defined to detect these changes automatically.

5. **Overkill for current needs** — cosmo-sokol has 2 releases and 3 submodules. A simple VERSIONS.md would suffice. The elaborate schema is over-engineering.

### Verdict
dbeng delivered architecture astronautics. Beautifully designed schemas for a problem the project doesn't have yet. Would be valuable IF populated with real data and IF there was tooling to maintain it. As delivered, it's documentation for a system that doesn't exist.

---

## Summary Table

| Specialist | Lane Violation | Usability | Key Failure |
|------------|---------------|-----------|-------------|
| seeker | N | 2/5 | Links without extraction |
| localsearch | N | 3/5 | Missed files in build script |
| asm | N | 2/5 | **Wrong struct sizes** |
| cosmo | N | 3/5 | Missing stub generation |
| neteng | N | 2/5 | No actual testing done |
| cicd | N | 4/5 | Hollow tests, macOS broken |
| testcov | N | 3/5 | Tests not executed |
| dbeng | Partial | 2/5 | All hypothetical |

### Cross-Cutting Issues

1. **asm vs testcov struct sizes conflict** — Someone is wrong. Neither verified empirically.
2. **cicd ignores testcov** — Workflows don't integrate the test code.
3. **localsearch missed files that asm analyzed** — sokol_cosmo.c wasn't in localsearch report but asm analyzed its dispatch pattern.
4. **No specialist actually RAN the binary** — Build verification only, no runtime verification.
5. **macOS is a mess** — testcov says stub-only, cicd tries to run --help, cosmo says x86-64 dlopen unsupported. No consensus.
