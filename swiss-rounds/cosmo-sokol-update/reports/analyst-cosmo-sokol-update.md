# Strategic Analysis: cosmo-sokol Fork Maintenance

**Date:** 2026-02-09  
**Analyst:** Swiss Rounds Subagent  
**Subject:** ludoplex/cosmo-sokol ecosystem dynamics and strategic value

---

## Executive Summary

The cosmo-sokol project represents a unique intersection of two powerful ecosystems: **Sokol** (minimal C graphics headers) and **Cosmopolitan** (build-once-run-anywhere C library). This combination enables portable native GUI applications as single executables—a capability with significant strategic value for air-gapped environments, simplified deployment, and cross-platform tooling.

**Key Finding:** This project fills a genuine niche with no direct alternatives. Staying current with upstream is recommended despite maintenance costs, as both upstreams are actively developed with frequent breaking changes.

---

## 1. Market Position Analysis

### 1.1 Sokol Users

**Primary Audience:**
- **Indie game developers** - Released games on Steam include *Solar Storm* (Odin+Sokol) and *Spanking Runners*
- **Emulator/retro computing** - Tiny 8-bit emulators, MEG-4 virtual fantasy console, buxn (uxn implementation)
- **Tool developers** - Dear ImGui integration makes it popular for internal/debug tools
- **Educational projects** - LearnOpenGL ports, Pacman clone examples
- **Cross-platform libraries** - Official bindings for Zig, Odin, Nim, Rust, D, Jai, C3

**Sokol Philosophy:**
> "WebAssembly is a 'first-class citizen', one important motivation for the Sokol headers is to provide a collection of cross-platform APIs with a minimal footprint on the web platform while still being useful."

This WASM-first philosophy means Sokol aggressively minimizes dependencies and binary size—exactly what Cosmopolitan needs.

### 1.2 Cosmopolitan Users

**Primary Audience:**
- **CLI tool developers** - Portable bash, emacs, vim, git, etc.
- **Single-binary app distributors** - Redbean web server, llama.cpp
- **DevOps/SRE** - Air-gapped deployments, no-install tools
- **Embedded/constrained environments** - BIOS bootable applications

**Cosmopolitan Philosophy:**
> "Makes C/C++ a build-once run-anywhere language, like Java, except it doesn't need an interpreter or virtual machine."

Supported platforms: Linux + Mac + Windows + FreeBSD + OpenBSD + NetBSD + BIOS boot

### 1.3 The Intersection: Portable Native GUI Apps

**cosmo-sokol uniquely enables:**
- Native-performance GUI apps as single executables
- Cross-platform distribution without installers
- Air-gapped deployment (no network, no package managers)
- Debugging with `--strace` and `--ftrace` flags built-in

**Current Platform Support:**

| Platform | Status | Graphics Backend |
|----------|--------|------------------|
| Linux | ✅ Full | OpenGL via dlopen(libGL.so) |
| Windows | ✅ Full | OpenGL via WGL |
| macOS | 🚧 Stub | Planned: objc_msgSend to Metal/OpenGL |

---

## 2. Competitive Landscape

### 2.1 Sokol Alternatives

| Library | Stars | Philosophy | Why Not for cosmo-sokol? |
|---------|-------|------------|--------------------------|
| **SDL** | ~38k | Kitchen sink multimedia | Too large, complex dependencies, harder cosmo integration |
| **GLFW** | ~14k | Window/input only | No graphics abstraction layer |
| **raylib** | ~25k | High-level, educational | More opinionated, less suitable as low-level substrate |
| **BGFX** | ~15k | Bring-your-own-engine | C++ core, heavier than Sokol |

**Why Sokol wins for Cosmopolitan:**
- Pure C, single-header design
- No external dependencies
- Explicit runtime platform detection is possible
- Minimal binary footprint (critical for APE format)
- floooh's responsive maintenance

### 2.2 Cosmopolitan Alternatives for Portability

| Approach | Platforms | Limitations |
|----------|-----------|-------------|
| **Static musl** | Linux only | Single platform per binary |
| **Go** | Many | Runtime overhead, larger binaries (~2MB+ hello world) |
| **Rust** | Many | Complex toolchain, not C ecosystem |
| **AppImage** | Linux only | Not Windows/macOS |
| **Electron** | All | Enormous size (~100MB+), requires runtime |

**Why Cosmopolitan wins:**
- Smallest binaries (12-16KB hello world vs 100KB+ Go)
- Native performance (no VM/interpreter)
- True single file (no unpacking needed)
- Built-in debugging (--strace, --ftrace)
- BIOS bootable (useful for recovery tools)

### 2.3 Why cosmo-sokol Specifically?

**There is no alternative that provides all of:**
1. Native GUI with hardware-accelerated graphics
2. Single-file distribution
3. Cross-platform (Linux + Windows + macOS pending)
4. Minimal size overhead
5. C-based (integrates with existing codebases)

The closest alternatives would require:
- Shipping separate binaries per platform, OR
- Accepting massive size overhead (Electron), OR
- Limiting to CLI-only (pure Cosmopolitan)

---

## 3. Maintenance Economics

### 3.1 Upstream Activity Analysis

#### floooh/sokol

**Activity Level:** ⚡ Very High

| Metric | Value |
|--------|-------|
| Commits (Jan 2026) | ~25+ |
| Last commit | Feb 8, 2026 |
| Release model | Rolling (no tags) |
| Breaking changes | Regular, well-documented |

**Recent Major Changes (from CHANGELOG):**
- Feb 2026: iOS Metal fixes, Vulkan Windows support
- Jan 2026: Dual-source blending, Vulkan object labels
- Dec 2025: WebGPU cleanup, sokol_gfx_imgui API break
- Dec 2025: **Experimental Vulkan backend** added

**floooh's Breaking Change Policy:**
- Changes are documented in CHANGELOG.md immediately
- Usually provides migration guidance
- Tends to rename functions rather than silently change behavior
- No formal deprecation period (rolling release model)

#### jart/cosmopolitan

**Activity Level:** ⚡ Very High

| Metric | Value |
|--------|-------|
| Latest release | v4.0.2 (Jan 6, 2026) |
| Release cadence | Every 2-3 months |
| Breaking changes | Version bumps (3.x → 4.x) |

**Recent v4.0 Highlights:**
- Windows fork() fixes
- 30% faster fork()
- Windows sleep accuracy: 15ms → 15µs
- PID spoofing across execve() on Windows

**Cosmopolitan Stability:**
- More traditional semver (v4.0.2)
- Major versions can have breaking changes
- Better for pinning than Sokol

#### bullno1 (upstream cosmo-sokol)

**Activity Level:** 🔄 Moderate

| Metric | Value |
|--------|-------|
| cosmo-sokol stars | 34 |
| cosmo-sokol forks | 5 |
| Other relevant projects | buxn (Sokol-based uxn), ugc (GC library) |
| Location | Singapore |
| Sponsors | rui314, jart (shows ecosystem commitment) |

**Maintenance Pattern:**
- Responds to issues (contributed Windows support to Cosmopolitan upstream)
- Not daily/weekly commits but keeps project functional
- Project serves as proof-of-concept more than production library

### 3.2 Cost of Staying Current vs Pinning

| Strategy | Pros | Cons |
|----------|------|------|
| **Stay Current** | Access to bug fixes, new features (Vulkan!), security patches | Ongoing integration work, potential breaking changes |
| **Pin Versions** | Stability, predictability | Miss WebGPU improvements, security issues, eventual bitrot |
| **Lazy Sync** | Best of both - update quarterly | May accumulate breaking changes |

**Recommendation: Stay Current with Quarterly Sync Cadence**

Rationale:
1. Sokol has no releases to pin to anyway (rolling release)
2. Both upstreams are actively fixing bugs
3. Breaking changes are manageable if caught early
4. New features (Vulkan, WebGPU improvements) have strategic value

**Estimated Maintenance Effort:**
- Monthly: ~2-4 hours (monitor changelogs, smoke test)
- Quarterly: ~8-16 hours (sync, fix breaks, test all platforms)
- Major breaks: ~1-2 days (rare, maybe 1-2x per year)

---

## 4. Strategic Value for MHI/DSAIC

### 4.1 Portable Desktop Apps

**Applicable Projects:**
- **MHI Procurement** - Internal tooling that runs on any analyst workstation
- **tedit-cosmo** - Portable text editor with GUI
- **Field deployment tools** - Single binary, no installation, works offline

**Value Proposition:**
```
Traditional Deployment:
  - Build for Windows x64
  - Build for Linux x64  
  - Build for macOS x64
  - Build for macOS ARM
  - Maintain 4 CI pipelines
  - Distribute 4 binaries
  - Handle missing dependencies per platform

cosmo-sokol Deployment:
  - Build once
  - Distribute one file
  - Works everywhere
```

### 4.2 Single-Binary Deployment Advantage

**Operational Benefits:**
1. **Zero-install deployment** - Copy file, run file
2. **No dependency conflicts** - Self-contained
3. **Version management** - The binary IS the version
4. **Rollback** - Just use the old binary file
5. **Auditing** - Hash the binary, done

**Developer Benefits:**
1. **Simpler CI/CD** - One build target
2. **Easier testing** - Same binary everywhere
3. **Reduced support burden** - "Did you install the dependencies?" is eliminated

### 4.3 Air-Gapped Environment Support

**Critical for:**
- SCIFs (Sensitive Compartmented Information Facilities)
- Isolated lab environments
- Field deployment without network access
- Systems without package managers

**cosmo-sokol Enables:**
- GUI applications without network installation
- Self-contained debugging (--strace, --ftrace)
- No external library dependencies at runtime
- ZIP file embedding for assets

### 4.4 Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| bullno1 abandons project | Medium | Medium | Fork exists (ludoplex), shim approach is documented |
| Sokol major breaking change | High | Low | Changes well-documented, integration is mechanical |
| Cosmopolitan major breaking change | Low | Medium | Semver, can pin if needed |
| macOS support never completed | Medium | Variable | macOS may not be required for all use cases |
| Windows-specific bugs | Medium | Medium | bullno1 actively fixes, cosmo community responsive |

---

## 5. Technical Deep Dive: How cosmo-sokol Works

### 5.1 Runtime Platform Dispatch

The key innovation: Sokol uses compile-time `#ifdef` for platform code. Cosmopolitan wants to compile ALL platform code and dispatch at runtime.

**Solution: gen-sokol preprocessor trick**

```c
// Instead of compile-time:
#ifdef _WIN32
void sapp_show_keyboard() { /* Windows impl */ }
#else
void sapp_show_keyboard() { /* Linux impl */ }
#endif

// cosmo-sokol creates:
#define sapp_show_keyboard windows_sapp_show_keyboard
// (include sokol for Windows)
#undef sapp_show_keyboard
#define sapp_show_keyboard linux_sapp_show_keyboard  
// (include sokol for Linux)

// Then runtime dispatch:
void sapp_show_keyboard() {
    if (IsWindows()) return windows_sapp_show_keyboard();
    if (IsLinux()) return linux_sapp_show_keyboard();
    if (IsXnu()) return macos_sapp_show_keyboard();
}
```

### 5.2 Dynamic Library Loading

**Linux:** dlopen() for libGL.so, libX11.so at runtime
**Windows:** WGL direct integration (required upstream cosmopolitan changes)
**macOS (planned):** objc_msgSend() to call Objective-C runtime from C

### 5.3 Fork Divergence (ludoplex vs bullno1)

**ludoplex additions:**
- Tri-platform shim generation (Linux + Windows + macOS)
- sokol_macos.h / sokol_macos.c stubs
- IsXnu() dispatch in sokol_cosmo.c
- macOS documentation in shims/macos/

**Sync Strategy:**
1. Monitor bullno1 for Linux/Windows fixes
2. Maintain macOS additions in ludoplex fork
3. Consider upstreaming macOS work once functional

---

## 6. Recommendations

### 6.1 Immediate Actions

1. **Set up upstream monitoring** - Watch floooh/sokol and jart/cosmopolitan for releases/major commits
2. **Document current versions** - Pin commit hashes used in last working build
3. **Create sync automation** - Script to diff upstream changes and highlight breaking items

### 6.2 Quarterly Maintenance Cadence

| Month | Activity |
|-------|----------|
| Q1 Start | Sync with upstreams, full test cycle |
| Mid-Q | Monitor changelogs, patch critical fixes only |
| Q End | Evaluate new features, document known issues |

### 6.3 Strategic Investments

1. **Complete macOS support** - Significant effort but enables full tri-platform story
2. **Build cosmo-sokol-imgui starter kit** - Reduce friction for new projects
3. **Document air-gapped deployment patterns** - Capture institutional knowledge

---

## 7. Conclusion

**cosmo-sokol fills a genuine niche** that has no alternatives. The combination of:
- Native GUI performance
- Single-file distribution
- True cross-platform support
- Minimal binary size

...makes it strategically valuable for MHI/DSAIC's portable tooling needs.

**The maintenance burden is manageable** given:
- Well-documented upstream changes
- Active upstream maintainers
- Mechanical integration work (not design changes)
- Quarterly sync cadence is sufficient

**Recommendation: Invest in keeping current** rather than pinning. The benefits of ongoing bug fixes, security patches, and new features (especially Vulkan/WebGPU) outweigh the integration costs.

---

*Generated by Swiss Rounds strategic analysis subagent*

---

## Addendum 1 (Cross-Reading)
**Signed:** analyst
**Date:** 2026-02-09

After reading reports from: seeker, ballistics, cosmo + triad solution

### Agreements

1. **Gap magnitude confirmed**: Seeker's precise count (1,044 commits) and Cosmo's (1,032 commits) validate my assessment that this is a substantial but manageable backlog. The actual API delta (~25-40 function changes per triad) vindicates my claim that "breaking changes are manageable if caught early."

2. **gen-sokol is the critical integration point**: All three specialists independently identified `gen-sokol` and its `SOKOL_FUNCTIONS` list as the primary maintenance burden. Ballistics' analysis of the "prefix trick" architecture confirms my technical deep-dive was accurate.

3. **Quarterly cadence is correct**: The triad's grounded estimates (6-9 hours post-backlog) closely match my "8-16 hours quarterly" recommendation. This convergence strengthens the strategic recommendation to stay current.

4. **Strategic value assessment validated**: Seeker's ecosystem research (kosmos, buxn, MEG-4) and Cosmo's detailed API analysis confirm there are real users of this pattern. The air-gapped deployment value I highlighted is reinforced by the platform detection mechanisms documented by all specialists.

5. **Sokol's rolling release model is the core challenge**: All reports identify the lack of tagged releases as complicating version tracking. Cosmopolitan's semver approach (v4.0.2) is indeed more tractable for pinning.

### Disagreements

1. **My maintenance estimates were slightly optimistic**: I quoted "8-16 hours quarterly" as steady-state, but the triad's grounded task breakdown shows **22-34 hours for the initial backlog**. My strategic analysis undersold the one-time cost of catching up from 14 months of drift. I should have distinguished "initial sync" from "ongoing maintenance" more clearly.

2. **macOS framing**: I described macOS as "🚧 Stub, Planned" with recommendations to "Complete macOS support" as a strategic investment. The triad's verdict is more decisive: **stub permanently with clear documentation**. On reflection, the triad is correct — my recommendation to invest in macOS completion was aspirational without grounding in effort estimates (2-4 person-months per ballistics).

3. **Automation scope**: My recommendation to "Create sync automation - Script to diff upstream changes" was vague. The triad's framing is better: **automation-assisted human review, not full automation**. The two-stage extraction approach (mechanical extraction + human curation) is more realistic than my implied "automate it away."

### Questions

1. **For Seeker**: You documented that several `sapp_*_get_*` functions were removed in favor of `sapp_get_environment`/`sapp_get_swapchain`. Are these removals compile-time breakage (linker errors) or runtime (stubs that fail)? This affects whether the update can be incremental.

2. **For Ballistics**: Your CI/CD matrix includes `macos-latest` for "compile-only" verification. Given the permanent stub decision, should macOS be dropped from CI entirely to avoid false confidence, or kept as compile-gate to catch header-level breaks?

3. **For Cosmo**: You identified 180 functions in the current `SOKOL_FUNCTIONS` list but upstream has ~185 public functions. Is the delta from intentional omissions (e.g., backend-specific functions not needed) or drift? This affects whether automation can safely add new functions.

4. **For Triad**: The `_Static_assert` mechanism catches struct size changes but not field reordering. For `sapp_desc` and `sg_desc` which are passed across the shim boundary, is field-level offset verification worth the maintenance burden, or is size-only sufficient in practice?

### Synthesis

The cross-reading has refined my strategic analysis in three ways:

**1. Effort Model Update**

| Phase | Original Estimate | Revised Estimate |
|-------|-------------------|------------------|
| Initial backlog | (not separated) | 22-34 hours (triad) |
| Quarterly steady-state | 8-16 hours | 6-9 hours (triad) |
| Major breaks | 1-2 days | 1-2 days (confirmed) |

My "quarterly" estimate was accidentally averaging the backlog case. The actual ongoing cost is lower than I stated.

**2. macOS Strategy Revision**

My original recommendation: "Complete macOS support - Significant effort but enables full tri-platform story"

Revised recommendation: **Do not invest in macOS implementation.** The triad's analysis is correct — 2-4 person-months of effort for a platform that may not be required. The stub-with-clear-error approach preserves architecture without committing resources. If macOS becomes critical, the integration point exists.

**3. Automation Strategy Clarification**

Original: Vague "create sync automation"

Revised: Adopt the triad's specific tooling recommendations:
- `scripts/extract_sokol_api.py` — Mechanical API extraction
- `scripts/diff_sokol_api.sh` — API delta measurement  
- `sokol_abi_check.h` — Compile-time struct size assertions

This is concrete and actionable, replacing my hand-wavy recommendation.

**4. Risk Matrix Refinement**

Ballistics identified a risk I missed: **ABI breaks from struct layout changes**. My risk table covered abandonment, breaking changes, and Windows bugs, but not silent corruption from struct changes. The `_Static_assert` mitigation addresses this gap.

**5. Strategic Positioning Strengthened**

Reading the detailed technical reports actually strengthens my core thesis: cosmo-sokol fills a genuine niche with no alternatives. The fact that the integration is this mechanical (prefix trick + function list + runtime dispatch) rather than requiring deep platform expertise means maintenance is tractable. The challenge is **bookkeeping, not engineering** — which is exactly the kind of problem that benefits from the tooling the triad recommends.

**Bottom Line**: My strategic recommendation stands — invest in staying current rather than pinning — but with more precise effort estimates and concrete tooling requirements from the specialist reports.
