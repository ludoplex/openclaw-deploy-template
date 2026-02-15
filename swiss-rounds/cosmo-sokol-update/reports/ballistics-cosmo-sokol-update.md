# cosmo-sokol Self-Updating: Technical Requirements Analysis

**Report Type:** Swiss Rounds Round 1 — Initial Technical Analysis  
**Date:** 2026-02-09  
**Author:** ballistics (subagent)

---

## Executive Summary

The ludoplex/cosmo-sokol fork provides a clever mechanism for building Sokol applications as fat binaries using Cosmopolitan Libc. The architecture hinges on a **prefix trick** that allows compiling platform-specific code paths simultaneously, with runtime dispatch. Keeping this synchronized with upstream Sokol and Cosmopolitan requires understanding several fragile integration points.

---

## 1. The Prefix Trick

### How gen-sokol Works

The `gen-sokol` Python script is the **heart of the multi-platform compilation strategy**:

1. **Input:** A manually maintained list of ~170 Sokol public function signatures (SOKOL_FUNCTIONS array)
2. **Output:**
   - `sokol_linux.h` — Contains `#define sapp_foo linux_sapp_foo` for all functions
   - `sokol_windows.h` — Contains `#define sapp_foo windows_sapp_foo` for all functions  
   - `sokol_macos.h` — Contains `#define sapp_foo macos_sapp_foo` for all functions
   - `sokol_cosmo.c` — Runtime dispatch shim that calls the correct platform variant

**Example generated code:**

```c
// sokol_cosmo.c (generated)
extern bool linux_sapp_isvalid(void);
extern bool windows_sapp_isvalid(void);
extern bool macos_sapp_isvalid(void);

bool sapp_isvalid(void) {
    if (IsLinux()) { return linux_sapp_isvalid(); }
    if (IsWindows()) { return windows_sapp_isvalid(); }
    if (IsXnu()) { return macos_sapp_isvalid(); }
}
```

### What Happens When Sokol Changes Functions

| Change Type | Impact | Detection Difficulty |
|-------------|--------|---------------------|
| **New function added** | Linker error: undefined reference | Easy — build fails |
| **Function removed** | Dead code in SOKOL_FUNCTIONS list | Silent — no error |
| **Function renamed** | Linker error | Easy — build fails |
| **Signature changed** | Potential ABI mismatch, runtime crash | **Dangerous** — may compile fine |
| **Return type changed** | May cause subtle bugs | Medium — compiler warnings possible |

### Automation Possibilities

**Option A: Parse Sokol Headers Directly**

```
sokol_app.h contains SOKOL_APP_API_DECL markers:
  SOKOL_APP_API_DECL bool sapp_isvalid(void);
  SOKOL_APP_API_DECL int sapp_width(void);
```

A script could:
1. Extract all `SOKOL_APP_API_DECL` and `SOKOL_GFX_API_DECL` lines
2. Parse function signatures using regex (similar to gen-sokol's existing `parse_c_signature`)
3. Generate the SOKOL_FUNCTIONS list automatically

**Challenges:**
- Complex types like `sg_image_desc` need to be preserved exactly
- Pointer syntax variations (`const char*` vs `char const *`)
- Default argument handling for C++

**Option B: Symbol Extraction from Object Files**

Compile Sokol once with full symbols, then extract the public API:
```bash
nm -g sokol.o | grep ' T ' | awk '{print $3}'
```

**Challenge:** Loses type information needed for shim generation.

**Option C: Hybrid Approach (Recommended)**

1. Parse headers for function signatures
2. Validate against compiled symbols via `nm`
3. Diff against previous SOKOL_FUNCTIONS list
4. Generate human-readable changelog for review

---

## 2. Platform Backend Architecture

### Linux: X11 + OpenGL via dlopen

**Pattern:** Lazy-loading system libraries at runtime

```c
// From gen-x11 generated x11.c
static void* libX11 = NULL;
static int (*proc_XPending)(Display *display) = NULL;

int XPending(Display *display) {
    if (libX11 == NULL) { load_X11_procs(); }
    return proc_XPending(display);
}
```

**Dependencies:**
- `libX11.so` — Core X11 windowing
- `libXcursor.so` — Cursor handling
- `libXi.so` — XInput2 extension
- `libGL.so` — OpenGL

**What's Needed from Cosmopolitan:**
- `cosmo_dlopen()` / `cosmo_dlsym()` / `cosmo_dltramp()` — Dynamic loading
- Basic POSIX compatibility for pthread, signals

**gen-x11 / gen-gl Scripts:**
- Manually maintained function lists extracted from build errors
- Gen-gl uses Khronos GL registry XML for completeness

### Windows: WGL + Win32

**Pattern:** Static import via Cosmopolitan's master.sh

Cosmopolitan's `libc/nt/master.sh` defines Win32 function imports:
```
imp 'CreateWindowExW'  CreateWindowExW  user32  12
imp 'wglCreateContext' wglCreateContext opengl32 1
```

**Dependencies:**
- kernel32.dll, user32.dll, gdi32.dll — Core Win32
- opengl32.dll — WGL/OpenGL

**What's Needed from Cosmopolitan:**
- Function prototypes merged into master.sh
- Windows struct definitions (replicated in `sokol_windows.c` due to conflicts)

**Key Constraint:** New Win32 functions require **upstream changes to Cosmopolitan**.

### macOS: The objc_msgSend Challenge

**Current Status:** Stub implementation (compiles but fails at runtime)

**The Problem:**
- Sokol's macOS backend is Objective-C (NSApplication, NSWindow, NSOpenGLView, Metal)
- cosmocc cannot compile Objective-C
- No way to `#ifdef` around the entire implementation

**Solution Path via Objective-C Runtime:**

```c
#include <objc/objc.h>
#include <objc/message.h>

// Load runtime dynamically
void* libobjc = cosmo_dlopen("/usr/lib/libobjc.dylib", RTLD_NOW);

// Equivalent to: [NSApplication sharedApplication]
id app = ((id(*)(id, SEL))objc_msgSend)(
    objc_getClass("NSApplication"),
    sel_registerName("sharedApplication")
);
```

**What's Needed from Cosmopolitan:**
- Working `cosmo_dlopen` on macOS (present in recent versions)
- Objective-C runtime header shims (`objc/objc.h`, `objc/message.h`)
- System framework paths (`/System/Library/Frameworks/`)

**Estimated Effort:** High — requires rewriting Sokol's entire macOS backend in pure C using objc_msgSend patterns. Hundreds of Objective-C method calls to translate.

---

## 3. Breaking Change Categories

### Category A: Function Signature Changes

**Risk Level:** 🔴 HIGH — may cause silent runtime corruption

**Examples from Sokol CHANGELOG (Dec 2025):**
- `sapp_color_format()` return type changed from `int` to `sapp_pixel_format`
- `sg_query_frame_stats()` renamed to `sg_query_stats()` with different return type
- Backend-specific config items moved into nested structs in `sapp_desc`

**Detection Requirements:**
1. Parse old and new function signatures
2. Compare return types, parameter types, parameter counts
3. Flag ANY change as requiring human review

### Category B: New Required Functions

**Risk Level:** 🟡 MEDIUM — build fails, easy to detect

**Example:** Sokol adds `sapp_get_environment()` (Dec 2025)

**Detection:** 
- Compare symbol lists between versions
- New symbols = new entries needed in SOKOL_FUNCTIONS

### Category C: Removed Functions

**Risk Level:** 🟡 MEDIUM — stale code, potential confusion

**Example:** Sokol removed several `sapp_*_get_*` functions, moving data to `sapp_environment` struct

**Detection:**
- Symbols present in SOKOL_FUNCTIONS but missing from new headers
- Should trigger removal from list + migration guide

### Category D: Struct Layout Changes

**Risk Level:** 🔴 HIGH — ABI breaks, potential memory corruption

**Examples:**
- `sapp_desc` nested struct reorganization
- `sg_desc` backend-specific item restructuring

**Detection Difficulty:** Very hard — requires parsing struct definitions from headers

**Mitigation:** 
- Always compile all platform backends together
- Runtime assertions on struct sizes where possible

### Category E: Preprocessor Define Changes

**Risk Level:** 🟡 MEDIUM — may change behavior silently

**Examples:**
- `SG_MAX_COLOR_ATTACHMENTS` changed from 4 to 8
- `SG_MAX_VIEW_BINDSLOTS` changed from 28 to 32

**Detection:** 
- Extract `#define SG_*` and `#define SAPP_*` from headers
- Diff between versions

---

## 4. Testing Requirements

### Build Verification Matrix

| Platform | Backend | Verification Method |
|----------|---------|---------------------|
| Linux x86_64 | X11 + GL | CI container with X11 headers |
| Linux aarch64 | X11 + GL | QEMU or native ARM runner |
| Windows x64 | WGL + Win32 | GitHub Actions windows-latest |
| macOS x64 | (stub) | Verify compile-only for now |
| macOS aarch64 | (stub) | Verify compile-only for now |

### CI/CD Pipeline Requirements

```yaml
# Minimal verification workflow
jobs:
  build:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    steps:
      - name: Install cosmocc
        run: # Download from jart/cosmopolitan releases
      
      - name: Install Linux deps
        if: matrix.os == 'ubuntu-latest'
        run: sudo apt-get install -y libx11-dev libxcursor-dev libxi-dev
      
      - name: Build
        run: ./build
      
      - name: Verify binary type
        run: file bin/cosmo-sokol  # Should show "APE" or "Actually Portable Executable"
      
      - name: Run smoke test (Linux only)
        if: matrix.os == 'ubuntu-latest'
        run: |
          Xvfb :99 &
          DISPLAY=:99 timeout 5 ./bin/cosmo-sokol || true
```

### Regression Detection

**Automated Checks:**
1. **Symbol count regression** — Track number of exported symbols per version
2. **Binary size delta** — Alert on >10% size changes
3. **Function signature hash** — Hash of all SOKOL_FUNCTIONS, alert on change

**Manual Checks (on upstream update):**
1. Review Sokol CHANGELOG.md for breaking changes
2. Diff gen-sokol's SOKOL_FUNCTIONS against new headers
3. Test one full application flow on each platform

### Upstream Sync Workflow

```
1. Fetch upstream sokol (floooh/sokol)
2. Fetch upstream cosmopolitan (jart/cosmopolitan)
3. Run header-parsing script to detect API changes
4. Generate diff report:
   - New functions
   - Removed functions
   - Changed signatures
   - New struct definitions
5. If changes detected:
   - Update SOKOL_FUNCTIONS list
   - Re-run gen-sokol, gen-x11, gen-gl
   - Build test on all platforms
   - If Windows needs new imports: PR to cosmopolitan
6. Create tagged release with changelog
```

---

## 5. Dependency Version Tracking

### Current State

| Dependency | Source | Version Tracking |
|------------|--------|------------------|
| Sokol | floooh/sokol | Manual pin in deps/ |
| Cosmopolitan | jart/cosmopolitan | Requires cosmocc ≥3.9.5 |
| cimgui | cimgui/cimgui | Manual pin in deps/ |
| Dear ImGui | imgui source via cimgui | Transitive |

### Recommended Tracking

```json
// versions.json (proposed)
{
  "sokol": {
    "repo": "floooh/sokol",
    "commit": "abc123...",
    "date": "2025-12-13",
    "api_hash": "sha256:..."
  },
  "cosmopolitan": {
    "repo": "jart/cosmopolitan",
    "min_version": "3.9.5",
    "tested_version": "3.10.0"
  },
  "cimgui": {
    "repo": "cimgui/cimgui",
    "commit": "def456..."
  }
}
```

---

## 6. Key Constraints Summary

1. **gen-sokol's SOKOL_FUNCTIONS list is manually maintained** — This is the primary sync point with upstream Sokol

2. **Windows requires upstream Cosmopolitan changes** — New Win32 functions must be added to `master.sh`

3. **macOS is effectively non-functional** — Full implementation requires person-months of work

4. **No automated API change detection** — Currently relies on build failures and manual review

5. **Platform shims (gen-x11, gen-gl) use build-error-driven discovery** — Functional but not proactive

6. **Struct layout changes are invisible** — No automated detection for ABI breaks

---

## 7. Recommendations for Self-Updating

### Minimum Viable Automation

1. **Header parser for Sokol API** — Extract function signatures automatically
2. **Version manifest** — Track exact commits of all dependencies  
3. **CI matrix build** — Verify all platform backends compile
4. **Diff reporter** — Generate human-readable change logs on upstream update

### Advanced Automation

1. **ABI validator** — Compare struct sizes/layouts between versions
2. **Auto-PR to Cosmopolitan** — For missing Win32 functions
3. **Symbol coverage checker** — Ensure SOKOL_FUNCTIONS matches actual exports

### Do Not Automate (Human Review Required)

1. **Semantic API changes** — New behavior with same signature
2. **macOS backend implementation** — Too complex for automation
3. **Breaking change migrations** — Require understanding of user impact

---

## Appendix: Files in ludoplex/cosmo-sokol

```
├── build                      # Main build script
├── shims/
│   ├── sokol/
│   │   ├── gen-sokol          # THE KEY SCRIPT - generates prefixes & dispatch
│   │   ├── sokol_linux.h      # Generated: Linux function prefixes
│   │   ├── sokol_windows.h    # Generated: Windows function prefixes
│   │   ├── sokol_macos.h      # Generated: macOS function prefixes
│   │   ├── sokol_cosmo.c      # Generated: Runtime dispatch
│   │   ├── sokol_linux.c      # Linux backend (includes sokol with prefixes)
│   │   ├── sokol_windows.c    # Windows backend (includes Win32 definitions)
│   │   ├── sokol_macos.c      # macOS backend (STUB)
│   │   └── sokol_shared.c     # Shared code (Dear ImGui integration)
│   ├── linux/
│   │   ├── gen-x11            # Generates X11 dlopen stubs
│   │   ├── gen-gl             # Generates OpenGL dlopen stubs
│   │   ├── x11.c              # Generated: X11 stubs
│   │   └── gl.c               # Generated: OpenGL stubs
│   ├── macos/
│   │   └── README.md          # Documentation for future implementation
│   └── win32/
│       └── (headers)
└── deps/
    ├── sokol/                 # Upstream sokol headers
    └── cimgui/                # Dear ImGui C bindings
```

---

*End of Technical Requirements Analysis*

---

## Addendum 1 (Cross-Reading)
**Signed:** ballistics
**Date:** 2026-02-09

After reading reports from: seeker, analyst, cosmo + triad solution

### Agreements

1. **API Delta is Tractable (Seeker + Triad):** Seeker's detailed enumeration of breaking changes (bindings cleanup Nov 2024, sapp_desc restructuring Dec 2025, sg_query_frame_stats rename) confirms my "Category A/B/C/D" classification. The triad's measurement of ~25-40 actual API changes versus 1,000+ commits validates my concern that signature changes are the real risk, not commit volume.

2. **Two-Stage Extraction is Correct (Triad):** The triad's "automation-assisted human review" approach matches my recommendation to NOT fully automate. My proposed hybrid approach (parse headers → validate via nm → diff → human review) aligns with their Stage 1/Stage 2 model.

3. **macOS Permanent Stub (Triad):** Completely agree. My analysis noted the objc_msgSend challenge requires "person-months" of work. The triad's recommendation to stub permanently with clear documentation is the right call. Dead code is acceptable; false hope is not.

4. **ABI Detection Gap (Triad):** The `_Static_assert` on struct sizes is exactly the right mechanism. I identified "struct layout changes are invisible" as a key constraint but didn't propose a solution — the triad filled this gap well.

5. **Strategic Value is Real (Analyst):** The analyst's positioning of cosmo-sokol as filling a unique niche (native GUI + single-file + cross-platform) validates my effort on understanding the architecture. This isn't academic — it matters for air-gapped deployments.

### Disagreements

1. **Quarterly Sync Cadence May Be Too Infrequent (Analyst vs Reality):** Analyst proposes "8-16 hours quarterly" and the triad says "6-9 hours per quarter after caught up." Given Sokol's rate of breaking changes (seeker identified 4 major breaks in 14 months), I'd argue **monthly monitoring with quarterly full-sync** is more realistic. A December breaking change shouldn't wait until March to discover.

2. **gen-gl/gen-x11 Underexplored:** All reports (including mine) treated the Linux shim generators as stable. But cosmo's analysis shows gen-gl parses the 2.8MB Khronos `gl.xml` with `MIN_VERSION = (4, 0)`. If upstream adds GL 4.7+ functions that Sokol starts using, this becomes a blocker. Neither seeker nor analyst flagged OpenGL spec evolution as a risk.

3. **cimgui Dismissal May Be Premature (Triad):** The triad says "stable enough to ignore" but seeker notes cimgui is at `1.91.x` pinned while latest is `1.94.2dock_conv`. That's ~3 minor versions. If sokol_imgui.h expects 1.94 features, compilation fails. I'd prefer explicit verification, not assumption.

### Questions

1. **For Seeker:** You extracted specific commit hashes and dates. Did you verify that `eaa1ca79` (the pinned version) is actually *before* the Nov 7, 2024 bindings cleanup, or did bullno1 intentionally pin *after* it and we're missing migration work?

2. **For Analyst:** Your competitive analysis didn't mention other Cosmopolitan GUI attempts. Has anyone tried cosmo+SDL or cosmo+GLFW? If so, why did those fail where cosmo-sokol succeeded?

3. **For Cosmo:** Your file size summary shows `sokol_macos.c` at 23KB but it's supposedly a stub. What's in those 23KB? Are there partial implementations that might conflict with future real implementations?

4. **For Triad:** The `_Static_assert` approach catches size changes but not field reordering. You note this is "rare in practice" — what's the evidence? Sokol's bindings cleanup moved fields between shader stages — that's reordering, not resizing.

### Synthesis

Reading the other reports modifies my analysis in three key ways:

1. **Effort Estimates Now Grounded:** My report lacked concrete hours. The triad's task breakdown (22-34 hours initial, 6-9 hours quarterly) gives my "Testing Requirements" section real numbers. I should have included: "Regression Detection budget: 2-4 hours per sync."

2. **Detection Mechanisms Refined:** My "Detection Difficulty" assessments (Easy/Medium/Dangerous) were qualitative. The triad's concrete proposals (diff scripts, ABI assertions) turn these into actionable checks. Incorporating their `diff_sokol_api.sh` into my "Upstream Sync Workflow" section would make it executable.

3. **Priority Ordering Clarified:** Analyst's strategic value argument + Triad's macOS decision means Linux+Windows are the real deliverables. My "Build Verification Matrix" should mark macOS as "compile-only verification" rather than implying functional testing is possible.

4. **Missing Piece Identified:** No report addressed **who** does this work. Is it ludoplex? MHI? Community? The maintenance economics are clear but the maintenance *ownership* is not. This affects whether automation investments pay off.

**Overall Assessment:** The four perspectives are largely convergent. Seeker provided facts, Analyst provided context, Cosmo provided code archaeology, and Triad provided solutions. My contribution focused on execution requirements — what breaks, how to test, what to track. Combined, we have a complete picture of a 3-5 day initial effort followed by sustainable quarterly maintenance.
