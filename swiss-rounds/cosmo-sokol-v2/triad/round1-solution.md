# Swiss Rounds Triad — Round 1 Remediation Plans

**Project:** cosmo-sokol-v2  
**Date:** 2026-02-09  
**Purpose:** Specific action items for each specialist to address Round 1 gaps

---

## Remediation for seeker

1. **Find and document sokol-shdc (shader compiler)**
   - Fetch `https://github.com/floooh/sokol-tools` — explain what sokol-shdc does
   - Fetch `https://github.com/floooh/sokol-tools-bin` — document prebuilt binary locations for Windows/Linux/macOS
   - Extract version info and explain how to regenerate shaders after upstream changes

2. **Extract Cosmopolitan dlopen limitations documentation**
   - Re-fetch `https://github.com/jart/cosmopolitan/blob/master/libc/dlopen/dlopen.c` (was rate-limited)
   - Document the explicit text: "dlopen() isn't supported on x86-64 MacOS"
   - Explain `cosmo_dlopen` naming vs standard `dlopen` and why this matters

3. **Document cimgui regeneration process**
   - Fetch `https://github.com/cimgui/cimgui/tree/docking_inter/generator`
   - List dependencies (luajit requirement)
   - Provide step-by-step: how to regenerate bindings after Dear ImGui version bumps

4. **Get version delta between sokol commits**
   - Compare `eaa1ca79...` (current submodule) vs upstream HEAD
   - List actual breaking changes (not just "PRs closed")
   - Identify specific API changes that might affect cosmo-sokol

5. **Verify and explain PR #1318 NT additions**
   - Fetch `https://github.com/jart/cosmopolitan/pull/1318`
   - List exactly WHICH Windows NT functions were added for sokol compatibility
   - Explain why these were needed (D3D11? Window creation?)

6. **Extract APE format technical details from justine.lol/ape.html**
   - Document the `MZqFpD` magic sequence
   - Explain the polyglot nature (valid as PE, ELF, shell script)
   - neteng already has this — seeker should deduplicate or provide web source context

---

## Remediation for localsearch

1. **Document nvapi/ directory**
   - Path: `C:\cosmo-sokol\nvapi\nvapi.c`
   - Run: `wc -l nvapi/nvapi.c` and `head -50 nvapi/nvapi.c`
   - Explain: What NVIDIA API features does this provide? (GPU preference? Optimus support?)

2. **Document win32_tweaks.c**
   - Path: `C:\cosmo-sokol\win32_tweaks.c`
   - Run: `wc -l win32_tweaks.c` and `cat win32_tweaks.c`
   - Explain: What Windows-specific adjustments does this file make?

3. **Document sokol_cosmo.c (THE critical dispatch layer)**
   - Path: `C:\cosmo-sokol\shims\sokol\sokol_cosmo.c`
   - Show the `IsLinux()` / `IsWindows()` / `IsXnu()` dispatch pattern
   - List which functions are dispatched (cross-reference with asm's analysis)
   - This is the most important file that was missed

4. **Document sokol_shared.c**
   - Path: `C:\cosmo-sokol\shims\sokol\sokol_shared.c`
   - Run: `wc -l shims/sokol/sokol_shared.c` and `head -50 shims/sokol/sokol_shared.c`
   - Explain: What code is shared across all platform backends?

5. **Document header files**
   - List and excerpt: `sokol_linux.h`, `sokol_windows.h`, `sokol_macos.h`
   - Show the interface contract that each platform backend must implement

6. **Extract .gitmodules content**
   - Run: `cat .gitmodules`
   - Show branch tracking for each submodule

7. **Document main.c entry point**
   - Path: `C:\cosmo-sokol\main.c`
   - Show the `sokol_main()` implementation
   - Explain how it ties sokol_app + sokol_gfx + cimgui together

8. **Document scripts/compile helper**
   - Path: `C:\cosmo-sokol\scripts\compile`
   - Explain the parallel compilation mechanism

---

## Remediation for asm

1. **VERIFY STRUCT SIZES EMPIRICALLY**
   - Compile and run testcov's `abi_sizes.c` on Linux (via CI or local machine)
   - Report ACTUAL sizes:
     - `sapp_desc`: Claimed ~280-320, testcov says 472 — which is correct?
     - `sg_desc`: Claimed ~120-150, testcov says 208 — which is correct?
     - `sg_bindings`: Claimed ~440, testcov says 328 — which is correct?
   - Update report with verified sizes

2. **Add ARM64 (AAPCS64) calling convention analysis**
   - Document ARM64 calling conventions (x0-x7 for arguments)
   - Explain how macOS Silicon executes the APE binary
   - Note: Cosmopolitan `SUPPORT_VECTOR` for ARM64 is `(_HOSTLINUX | _HOSTXNU | _HOSTFREEBSD)` — document implications

3. **Analyze SIMD register usage**
   - How do xmm0-xmm7 (Linux) vs xmm0-xmm3 (Windows) affect:
     - `sg_color` (4 floats)
     - Matrix types (if any)
     - HMM (handmade math) integration
   - Does sokol use SIMD intrinsics? Check headers for `__m128` usage

4. **Verify #pragma pack directives**
   - Search sokol headers for `#pragma pack` directives
   - Report: Are any structs explicitly packed?
   - Analyze alignment requirements for D3D11/Metal/GL interop

5. **Verify `#pragma GCC diagnostic ignored "-Wreturn-type"` correctness**
   - Identify WHERE in sokol_cosmo.c this pragma is used
   - Analyze: What happens if unsupported platform is detected at runtime?
   - Is this a bug or intentional undefined behavior?

6. **Cross-reference with cosmo specialist's IsLinux() implementation**
   - cosmo documented `__hostos` bitmask mechanism
   - asm should verify: How does the runtime dispatch affect register state?
   - Are there any caller-saved register clobbers in the dispatch chain?

---

## Remediation for cosmo

1. **Analyze gen-x11 and gen-gl stub generation**
   - Path: `C:\cosmo-sokol\shims\linux\gen-x11` (180 lines)
   - Path: `C:\cosmo-sokol\shims\linux\gen-gl` (94 lines)
   - Document: How is the `FUNCTIONS` dict structured?
   - Explain: How do X11/GL functions get wrapped with `cosmo_dltramp`?
   - Show sample output (generated x11.c and gl.c shim code)

2. **Document binfmt_misc registration for APE**
   - Explain: `:APE:M::MZqFpD::{APE_PATH}:`
   - How does Linux kernel recognize APE binaries?
   - Where is this registered? (bjia56/setup-cosmocc does it in CI)

3. **Document foreign_thunk_sysv / foreign_thunk_nt implementation**
   - Location: Find in Cosmopolitan source
   - Explain: How is the trampoline code generated?
   - Is it static? Generated at runtime? JIT?

4. **Document __syslib structure completely**
   - Path: `libc/runtime/syslib.internal.h`
   - Show ALL v6 fields (dlopen/dlsym/dlclose/dlerror)
   - Explain: How does APE loader on macOS populate this?

5. **Explain BLOCK_SIGNALS / BLOCK_CANCELATION macros**
   - Location: Find definition in Cosmopolitan
   - Explain: Thread safety mechanism
   - Why are these needed around dlopen calls?

6. **Provide version delta details**
   - v3.9.5 → v3.9.6: What changed? (pinned version)
   - v3.9.6 → v4.0.0: What's in "Major release"?
   - v4.0.0 → v4.0.2: "Fork fixes, Windows improvements" — specifics?

7. **Document foreign helper executable**
   - Path: `~/.cosmo/dlopen-helper`
   - Explain: How is this compiled? When? By whom?
   - Is it architecture-specific? What if it doesn't exist?

---

## Remediation for neteng

1. **GENERATE SHA256 CHECKSUMS**
   - Download `https://github.com/bullno1/cosmo-sokol/releases/download/v1.1.0/cosmo-sokol.zip`
   - Run: `sha256sum cosmo-sokol.zip`
   - Provide the actual hash value
   - Recommend adding this to release notes

2. **ACTUALLY TEST the binary on at least one platform**
   - On Windows (if available): Run `cosmo-sokol.exe`, take screenshot, document behavior
   - On Linux: Run via WSL2 or actual Linux, document startup behavior
   - Report: Window title, initial render, any errors

3. **Document APE loader distribution**
   - Are `ape-x86_64.elf` and `ape.exe` embedded in the APE binary?
   - Or distributed separately?
   - What happens on first run without binfmt_misc?

4. **Complete Gatekeeper bypass documentation**
   - Beyond `xattr -d com.apple.quarantine`:
     - Document `spctl --add` option
     - Explain macOS Sequoia changes
     - Note that notarization is NOT possible for APE binaries (not code-signed)

5. **Test Wine execution**
   - Run: `wine ./cosmo-sokol` on Linux
   - Document: Does it work? Any errors?
   - If Wine fails, document why (D3D11 requirement?)

6. **Provide size breakdown**
   - Use `objdump` or similar to analyze binary sections
   - Report: How much is Cosmopolitan runtime? Sokol? ImGui? Code vs data?

7. **Document where release download counts came from**
   - Show: GitHub API query or screenshot showing "28 downloads" for v1.1.0
   - Currently unsubstantiated claim

---

## Remediation for cicd

1. **Integrate testcov's smoke_test into CI**
   - Add `smoke_test.c` compilation to build job
   - Add Xvfb setup for Linux runtime testing:
     ```yaml
     - name: Install Xvfb
       run: sudo apt-get install -y xvfb
     - name: Run smoke test
       run: xvfb-run -a ./bin/smoke_test --smoke
     ```

2. **Fix macOS test job**
   - Current: `timeout 5 "$binary" --help` — will fail for GUI apps
   - Fix: Acknowledge macOS is compile-only/link-only per testcov's analysis
   - Remove runtime test, replace with:
     ```yaml
     - name: Verify macOS linkage
       run: |
         file "$binary"
         # Link-only verification, no runtime test
     ```

3. **Add cosmocc caching**
   ```yaml
   - name: Cache cosmocc
     uses: actions/cache@v4
     with:
       path: ~/.cosmocc
       key: cosmocc-${{ matrix.cosmocc-version }}
   ```

4. **Fix submodule PR trigger**
   - Current: `update-{submodule}-{sha}` branch won't match `branches: [main, master]`
   - Fix: Add `pull_request` trigger to build-matrix.yml or use `workflow_run`

5. **Pin action versions with SHA**
   - Current: `softprops/action-gh-release@v2` — floating
   - Fix: `softprops/action-gh-release@de2c0eb89ae2a093876385947365aca7b0e5f844` (v2.0.9)
   - Same for other actions

6. **Add Windows runtime test (with WARP)**
   - Check if GitHub Actions runners have D3D WARP available
   - If yes, add actual execution test:
     ```powershell
     $env:D3D_FORCE_WARP = "1"
     .\cosmo-sokol.exe --smoke
     ```

7. **Document required secrets**
   - Add comment or README section explaining:
     - `GITHUB_TOKEN` — auto-provided, sufficient for releases
     - Any additional secrets needed?

8. **Add artifact retention policy rationale**
   - Current: 7 days hardcoded
   - Document: Why 7 days? Sufficient for debugging? Storage cost tradeoff?

---

## Remediation for testcov

1. **ACTUALLY RUN abi_sizes.c and report output**
   - Compile: `cosmocc abi_sizes.c -I deps/sokol -o abi_sizes`
   - Run: `./abi_sizes`
   - Paste the output into the report
   - Resolve conflict with asm's estimates

2. **Integrate tests with CI**
   - Create `.github/workflows/test.yml` that:
     - Compiles abi_verify.c (link-only)
     - Runs smoke_test on Linux with Xvfb
     - Skips runtime on macOS (document why)
   - Provide the actual YAML, not just concepts

3. **Expand API coverage to match localsearch's 200+ functions**
   - Current: ~70 functions (~35% coverage)
   - Update gen_api_coverage.py with remaining functions from:
     - sokol_audio.h (11 functions)
     - sokol_fetch.h (13 functions)
     - sokol_args.h (11 functions)
     - sokol_time.h (10 functions)
     - Backend-specific functions (sg_d3d11_*, sg_metal_*, sg_gl_*)

4. **Add cimgui smoke test**
   - Create `imgui_smoke_test.c`:
     - Initialize ImGui context
     - Create a window with `igBegin()`
     - Render text with `igText()`
     - Cleanup
   - This tests the other half of cosmo-sokol

5. **Fix platform backend test model**
   - Current: `SOKOL_D3D11` / `SOKOL_GLCORE` / `SOKOL_METAL` compile-time switches
   - Problem: cosmo-sokol is UNIFIED binary with RUNTIME selection
   - Fix: Test should not define backend, should rely on sokol_cosmo.c dispatch
   - Update smoke_test.c to not require compile-time backend selection

6. **Add cross-distro support to headless_test_linux.sh**
   - Current: Uses `sudo apt-get` — Debian/Ubuntu only
   - Add: Package manager detection for Fedora (`dnf`), Arch (`pacman`), Alpine (`apk`)

7. **Verify Windows WARP availability**
   - Test on GitHub Actions windows-latest
   - Document: Is WARP available? How to force it?

8. **Provide actual test run output**
   - Run smoke_test locally or in CI
   - Paste: Pass/fail output, timing, any warnings

---

## Remediation for dbeng

1. **Populate schemas with REAL data**
   - Current: Fake commit SHAs (`a1b2c3d4e5f6...`)
   - Fix: Use actual submodule commits:
     - deps/sokol: `eaa1ca79a4004750e58cb51e0100d27f23e3e1ff`
     - deps/cimgui: `8ec6558ecc9476c681d5d8c9f69597962045c2e6`
   - Use actual cosmocc version: `3.9.6`

2. **Create tooling to populate/validate schemas**
   - Write `extract_versions.py`:
     - Reads `.gitmodules` and `git submodule status`
     - Reads build.yml for cosmocc version
     - Outputs `versions.json`
   - Write JSON Schema validator integration

3. **Simplify to match project needs**
   - Current: Elaborate migration tracking, impact analysis schemas
   - Reality: 2 releases, 3 submodules
   - Recommendation: Start with simple `VERSIONS.md`:
     ```markdown
     ## Current Versions
     - cosmocc: 3.9.6
     - sokol: eaa1ca79
     - cimgui: 8ec6558e
     ```
   - Scale up IF needed, not before

4. **Integrate with CI**
   - Add step to generate `versions.json` on each build
   - Validate against schema
   - Fail build if schema validation fails

---

## Cross-Cutting Actions

1. **Resolve asm vs testcov struct size conflict**
   - SOMEONE must compile `abi_sizes.c` and report actual values
   - Current claims:
     - asm: `sapp_desc` = 280-320 bytes
     - testcov: `sapp_desc` = 472 bytes
   - Only one can be right. Verify empirically.

2. **Actually RUN the binary**
   - No specialist ran `cosmo-sokol` and documented behavior
   - neteng should do basic execution test
   - cicd should integrate runtime test in CI

3. **Consolidate platform support documentation**
   - Current state: cosmo says x86-64 macOS dlopen unsupported, cicd tries to run --help, testcov says stub-only
   - Need single authoritative matrix:
     | Platform | Build | Runtime | dlopen | Notes |
     |----------|-------|---------|--------|-------|
     | Linux x86_64 | ✅ | ✅ | ✅ | Full support |
     | Windows x86_64 | ✅ | ✅ | ✅ | D3D11 backend |
     | macOS ARM64 | ✅ | ✅ | ✅ | Metal via syslib |
     | macOS x86_64 | ✅ | ❌ | ❌ | dlopen explicitly disabled |
     | OpenBSD | ✅ | ❌ | ❌ | msyscall issues |

---

*End of Remediation Plans*
