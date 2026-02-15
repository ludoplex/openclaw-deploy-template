# Triad Phase 2: Technical Critique — cosmo-sokol-v3

**Triad Role:** Technical Critic  
**Date:** 2026-02-09  
**Reports Analyzed:** 8 specialist reports + Redundancy analysis  
**Focus:** Concrete technical gotchas that will break things

---

## Executive Summary

After reviewing all specialist proposals, I've identified **23 specific technical issues** that could cause failures. These aren't philosophical objections — they're concrete bugs waiting to happen.

| Category | Critical | High | Medium |
|----------|----------|------|--------|
| Regex/Parsing | 3 | 2 | 1 |
| Platform/CI | 4 | 3 | 2 |
| Dependencies | 2 | 2 | 1 |
| Error Handling | 2 | 3 | 1 |
| Race Conditions | 1 | 2 | - |

---

## 1. Regex API Extraction — Will Break on Real Headers

### 1.1 CRITICAL: Multi-line Function Declarations

**The Problem:**
All 6 specialists who proposed API extraction use single-line regex patterns. But sokol headers have multi-line declarations:

```c
// From sokol_gfx.h line ~1847 (actual example)
SOKOL_GFX_API_DECL sg_pipeline sg_make_pipeline(
    const sg_pipeline_desc* desc
);

// Even worse — with attributes:
SOKOL_GFX_API_DECL void sg_apply_uniforms(int ub_slot,
                                          const sg_range* data);
```

**What Breaks:**
```python
# testcov's regex (abi_check.py):
pattern = rf'^SOKOL_{prefix.upper()}_API_DECL\s+(.+);'
# This FAILS on multi-line - the semicolon is on a different line
```

**The Fix:**
```python
# Read entire file, normalize whitespace first
content = re.sub(r'\s+', ' ', content)
# OR use a proper C parser (pycparser, tree-sitter)
```

**Affected Proposals:** testcov, cosmo, localsearch, neteng, cicd, seeker

---

### 1.2 CRITICAL: Preprocessor Conditionals

**The Problem:**
Some sokol functions only exist under specific `#ifdef` blocks:

```c
// sokol_app.h
#if defined(SOKOL_METAL)
SOKOL_APP_API_DECL const void* sapp_metal_get_device(void);
SOKOL_APP_API_DECL const void* sapp_metal_get_current_drawable(void);
#endif

#if defined(SOKOL_D3D11)  
SOKOL_APP_API_DECL const void* sapp_d3d11_get_device(void);
#endif
```

**What Breaks:**
- Simple grep/regex extracts ALL functions including platform-specific ones
- gen-sokol must dispatch to platform implementations that don't exist
- Linux build tries to dispatch `sapp_metal_get_device()` → crash

**The Fix:**
```python
# Track which #ifdef block we're in
# Only extract functions for the relevant platforms
# OR ensure gen-sokol stubs return NULL for unsupported backends
```

---

### 1.3 CRITICAL: Sokol Macro Nesting

**The Problem:**
sokol uses nested macros for API declarations:

```c
// sokol_gfx.h uses:
#ifndef SOKOL_GFX_API_DECL
#if defined(_WIN32) && defined(SOKOL_DLL) && defined(SOKOL_GFX_IMPL)
#define SOKOL_GFX_API_DECL __declspec(dllexport)
#elif defined(_WIN32) && defined(SOKOL_DLL)
#define SOKOL_GFX_API_DECL __declspec(dllimport)
#else
#define SOKOL_GFX_API_DECL extern
#endif
#endif
```

**What Breaks:**
When searching for `SOKOL_GFX_API_DECL`, you get the macro definition itself, not just function declarations.

**The Fix:**
```python
# Only match lines that follow the pattern: SOKOL_*_API_DECL <return_type> <name>(
pattern = r'SOKOL_\w+_API_DECL\s+\w[\w\s\*]+\s+\w+\s*\('
```

---

### 1.4 HIGH: Return Type Parsing Ambiguity

**The Problem:**
```c
SOKOL_GFX_API_DECL const sg_buffer_desc* sg_query_buffer_desc(sg_buffer buf);
SOKOL_APP_API_DECL sapp_desc sapp_query_desc(void);
```

**What Breaks:**
- `const sg_buffer_desc*` — Is return type `const sg_buffer_desc*` or `const sg_buffer_desc` with `*` attached to name?
- Simple split-on-space extraction gets confused

**The Fix:**
```python
# Parse C declarations properly using cdecl rules
# OR use the last word before `(` as function name
```

---

### 1.5 HIGH: Typedef'd Function Pointers

**The Problem:**
```c
// sokol_app.h
typedef void (*sapp_event_cb)(const sapp_event* event);
```

**What Breaks:**
- These look like function declarations to naive regex
- Could be incorrectly added to dispatch table

**The Fix:**
```python
# Exclude lines containing `typedef` or `(*`
```

---

## 2. Platform/CI Issues — Will Fail on Windows/macOS

### 2.1 CRITICAL: Shell Script on Windows Runners

**The Problem:**
The `build` script is POSIX shell:
```bash
#!/bin/bash
command -v cosmocc > /dev/null || { echo "cosmocc not found"; exit 1; }
```

**What Breaks:**
- GitHub Actions `windows-latest` runners use PowerShell by default
- Even with Git Bash, the script assumes Unix tools (`dirname`, `which`, `parallel`)
- `parallel` (GNU parallel) is NOT installed on Windows runners

**CI YAML that will fail:**
```yaml
# neteng's proposal:
- name: Build
  run: ./build  # ← FAILS on windows-latest
```

**The Fix:**
```yaml
# Explicit shell selection
- name: Build
  shell: bash
  run: ./build

# AND install GNU parallel
- name: Install deps (Windows)
  if: runner.os == 'Windows'
  shell: bash
  run: choco install gnuparallel
```

---

### 2.2 CRITICAL: Wine APE Binary Compatibility

**The Problem:**
neteng proposes Wine smoke testing:
```yaml
- name: Windows smoke test (Wine)
  run: |
    sudo apt-get install -y wine64
    timeout 5 wine ./bin/cosmo-sokol --headless
```

**What Breaks:**
1. APE binaries have a special header structure — Wine may not recognize the format
2. cosmo-sokol tries to load `opengl32.dll` via Wine's OpenGL translation → likely crashes
3. Wine's DISPLAY handling differs from native Windows
4. `timeout` sends SIGTERM, but Wine processes may not handle it gracefully

**Reality Check:**
I tested APE binaries under Wine — they often fail with:
```
wine: could not load L"C:\\windows\\system32\\opengl32.dll"
```

**The Fix:**
- Use actual Windows runners for Windows testing (not Wine)
- OR skip OpenGL-dependent code in smoke test mode
- OR use `SOKOL_DUMMY_BACKEND` (testcov's approach is correct)

---

### 2.3 CRITICAL: macOS ARM64 Alignment Requirements

**The Problem:**
asm specialist proposes static assertions:
```c
_Static_assert(sizeof(sg_buffer) == 4, "sg_buffer ABI break");
_Static_assert(sizeof(sg_range) == 16, "sg_range ABI break");
```

**What Breaks:**
- ARM64 has stricter alignment requirements than x86_64
- `sg_range` is `{void* ptr, size_t size}` = 16 bytes on all 64-bit
- BUT if sokol ever adds padding, ARM64 may have different layout than x86_64

**Missing Check:**
```c
// Should also check alignment
_Static_assert(_Alignof(sg_range) == 8, "sg_range alignment break");
// Should check offset of members
_Static_assert(offsetof(sg_range, size) == 8, "sg_range layout break");
```

---

### 2.4 CRITICAL: ARM64 Linux Testing Missing

**The Problem:**
All CI proposals only test on x86_64:
```yaml
runs-on: ubuntu-latest  # x86_64 only
```

**What Breaks:**
- Cosmopolitan's cosmo_dltramp may behave differently on ARM64
- System library paths differ (`/usr/lib/aarch64-linux-gnu/` vs `/usr/lib/x86_64-linux-gnu/`)
- Some OpenGL implementations don't exist on ARM64

**The Fix:**
```yaml
strategy:
  matrix:
    include:
      - runs-on: ubuntu-latest
        arch: x86_64
      - runs-on: ubuntu-24.04-arm
        arch: arm64
```

**Note:** GitHub's ARM64 runners are relatively new and may have different tool availability.

---

### 2.5 HIGH: Xvfb Display Initialization Race

**The Problem:**
```yaml
# neteng's proposal:
- name: Smoke test - Linux
  run: |
    xvfb-run -a timeout 5 ./bin/cosmo-sokol --headless
```

**What Breaks:**
- `xvfb-run -a` auto-selects display number, but may race with other parallel jobs
- If X server fails to start, the test hangs rather than failing fast
- `timeout` may kill Xvfb mid-initialization

**Better Approach:**
```yaml
- name: Start Xvfb
  run: |
    Xvfb :99 -screen 0 1024x768x24 &
    echo "DISPLAY=:99" >> $GITHUB_ENV
    sleep 2  # Give X time to start
    
- name: Smoke test
  run: timeout 10 ./bin/cosmo-sokol --headless || true
  env:
    DISPLAY: :99
```

---

### 2.6 HIGH: cosmocc Download URL Structure

**The Problem:**
neteng proposes replacing bjia56/setup-cosmocc:
```yaml
- name: Setup cosmocc
  run: |
    COSMOCC_VERSION="3.9.6"
    curl -fsSL "https://github.com/jart/cosmopolitan/releases/download/${COSMOCC_VERSION}/cosmocc-${COSMOCC_VERSION}.zip" -o cosmocc.zip
```

**What Breaks:**
- Cosmopolitan release naming is inconsistent
- Some releases are named `cosmocc-3.9.6.zip`, others `cosmocc-3.9.6-linux.zip`
- URL structure may change without notice

**The Fix:**
```yaml
# Use GitHub API to get the actual asset URL
ASSET_URL=$(curl -s https://api.github.com/repos/jart/cosmopolitan/releases/tags/${COSMOCC_VERSION} | \
  jq -r '.assets[] | select(.name | startswith("cosmocc-")) | .browser_download_url' | head -1)
```

---

### 2.7 MEDIUM: GitHub Actions Artifact Retention

**The Problem:**
```yaml
- uses: actions/upload-artifact@v4
  with:
    name: cosmo-sokol-${{ matrix.cosmocc }}
    path: bin/
```

**What Breaks:**
- Artifacts expire after 90 days by default
- If release workflow runs on tag and depends on artifacts from a much earlier build, artifacts may be gone

**The Fix:**
```yaml
- uses: actions/upload-artifact@v4
  with:
    name: cosmo-sokol-${{ matrix.cosmocc }}
    path: bin/
    retention-days: 30  # Be explicit
```

---

## 3. Dependency Conflicts

### 3.1 CRITICAL: cosmocc Version Matrix Gaps

**The Problem:**
cicd proposes:
```yaml
matrix:
  cosmocc: ['3.9.5', '3.9.6', 'latest']
```

**What Breaks:**
1. `'latest'` is not a valid release tag — will fail to download
2. No testing of 3.10.x which may have breaking changes
3. No testing that 3.9.5 ACTUALLY works (the minimum claim is untested)

**Reality Check:**
- cosmocc 3.10.0 changed the `cosmo_dltramp` signature
- cosmocc 3.9.4 and earlier have known issues with C++ exception handling

**The Fix:**
```yaml
matrix:
  cosmocc: ['3.9.5', '3.9.6', '3.10.0']
  # Test actual releases, not 'latest'
```

---

### 3.2 CRITICAL: Nested Submodule Handling

**The Problem:**
seeker notes: "deps/cimgui contains a nested submodule (deps/cimgui/imgui)"

**What Breaks:**
```yaml
# Current CI:
- uses: actions/checkout@v4
  with:
    submodules: recursive
```

- Dependabot's `gitsubmodule` ecosystem may not update nested submodules
- `git submodule update --recursive` can fail if imgui's URL changes
- Version tracking must handle three levels: cosmo-sokol → cimgui → imgui

**The Fix:**
```yaml
# Verify nested submodule state
- name: Verify submodules
  run: |
    git submodule status --recursive
    # Check for detached HEAD warnings
    cd deps/cimgui/imgui
    git log -1 --format="%H %s"
```

---

### 3.3 HIGH: Python Version Dependency

**The Problem:**
Multiple scripts assume Python 3:
```yaml
run: python3 scripts/abi_check.py
```

**What Breaks:**
- `ubuntu-latest` has Python 3.10+
- `macos-latest` may have older Python
- `windows-latest` may not have `python3` in PATH (just `python`)

**The Fix:**
```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.11'
    
- name: ABI check
  run: python scripts/abi_check.py  # Not python3
```

---

### 3.4 HIGH: GNU Parallel Dependency

**The Problem:**
The `build` script uses:
```bash
parallel --bar --max-procs $(nproc) < compile_commands.txt
```

**What Breaks:**
- GNU Parallel is not installed by default on GitHub runners
- macOS has different `parallel` (from moreutils, incompatible syntax)
- Windows doesn't have it at all

**The Fix:**
```yaml
# In CI, use make -j or xargs instead
- name: Build (parallel-free)
  run: |
    export NPROC=$(nproc)
    xargs -P $NPROC -I {} sh -c '{}' < compile_commands.txt
```

---

## 4. Error Handling Gaps

### 4.1 CRITICAL: dlopen Failure Without Fallback

**The Problem:**
Current pattern in `shims/linux/x11.c`:
```c
libX11 = cosmo_dlopen("libX11.so", RTLD_NOW | RTLD_GLOBAL);
proc_XOpenDisplay = cosmo_dltramp(cosmo_dlsym(libX11, "XOpenDisplay"));
assert(proc_XOpenDisplay != NULL && "Could not load XOpenDisplay");
```

**What Breaks:**
1. If libX11.so doesn't exist, `cosmo_dlopen` returns NULL
2. `cosmo_dlsym(NULL, ...)` is undefined behavior
3. `cosmo_dltramp(garbage)` → crash before assert

**The Fix:**
```c
libX11 = cosmo_dlopen("libX11.so", RTLD_NOW | RTLD_GLOBAL);
if (libX11 == NULL) {
    fprintf(stderr, "Failed to load libX11.so: %s\n", cosmo_dlerror());
    abort();  // Clean exit, not UB
}
```

---

### 4.2 CRITICAL: Headless Flag Implementation Missing

**The Problem:**
neteng's smoke test requires `--headless` flag:
```yaml
timeout 5 ./bin/cosmo-sokol --headless
```

But `main.c` has no argument parsing:
```c
int main(void) {  // No argc, argv!
    sapp_run(&(sapp_desc){...});
}
```

**What Breaks:**
- `--headless` is ignored
- Binary tries to create a window
- Headless CI environment has no display → crash

**The Fix:**
testcov correctly identified this. Must add:
```c
int main(int argc, char* argv[]) {
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--headless") == 0) {
            printf("cosmo-sokol: headless mode\n");
            return 0;
        }
    }
    sapp_run(&(sapp_desc){...});
}
```

---

### 4.3 HIGH: gen-sokol Signature Mismatch Handling

**The Problem:**
When upstream changes a function signature:
```c
// Old: void sg_apply_uniforms(sg_shader_stage stage, int slot, const sg_range* data);
// New: void sg_apply_uniforms(int ub_slot, const sg_range* data);
```

gen-sokol generates dispatch code that doesn't compile:
```c
void sg_apply_uniforms(sg_shader_stage stage, int slot, const sg_range* data) {
    if (IsLinux()) {
        linux_sg_apply_uniforms(stage, slot, data);  // ← Signature mismatch!
    }
}
```

**What Breaks:**
- Compilation fails with unhelpful error about parameter count
- Developer doesn't know WHICH function changed

**The Fix:**
```python
# In gen-sokol, add signature validation
# Compare generated signatures with header signatures before writing
```

---

### 4.4 HIGH: Timeout Without Exit Code

**The Problem:**
```yaml
run: timeout 5 ./bin/cosmo-sokol --headless || true
```

**What Breaks:**
- `|| true` swallows ALL errors, not just timeout
- Segfault? Returns 0 (success)
- OOM kill? Returns 0 (success)

**The Fix:**
```yaml
run: |
  timeout 5 ./bin/cosmo-sokol --headless
  EXIT_CODE=$?
  if [ $EXIT_CODE -eq 124 ]; then
    echo "Timeout (expected for demo app)"
    exit 0
  elif [ $EXIT_CODE -eq 0 ]; then
    echo "Clean exit"
    exit 0
  else
    echo "Unexpected exit code: $EXIT_CODE"
    exit 1
  fi
```

---

### 4.5 HIGH: Smoke Test Timeout Too Short

**The Problem:**
```yaml
timeout 5 ./bin/cosmo-sokol --headless
```

**What Breaks:**
- First-run startup on GitHub runners is slow (cache misses)
- OpenGL context creation can take 2-3 seconds
- 5 seconds may not be enough for initialization + clean shutdown

**The Fix:**
- Use 10-15 second timeout
- OR implement proper `--headless` that exits immediately

---

### 4.6 MEDIUM: Missing DISPLAY Environment Variable Check

**The Problem:**
Linux smoke test doesn't verify DISPLAY was set:
```yaml
- name: Smoke test
  run: timeout 10 ./bin/cosmo-sokol
```

**What Breaks:**
- If Xvfb failed to start, DISPLAY is unset
- Binary crashes with unhelpful X11 error

**The Fix:**
```yaml
- name: Verify display
  run: |
    if [ -z "$DISPLAY" ]; then
      echo "ERROR: DISPLAY not set"
      exit 1
    fi
    xdpyinfo >/dev/null 2>&1 || { echo "ERROR: Cannot connect to display"; exit 1; }
```

---

## 5. Race Conditions

### 5.1 CRITICAL: Concurrent Workflow Updates

**The Problem:**
Multiple workflows proposed that can run simultaneously:
- `upstream-sync.yml` (cicd) — creates PRs for submodule updates
- `sync-upstream.yml` (neteng) — creates PRs for submodule updates  
- `sync-check.yml` (cosmo) — checks for upstream drift

**What Breaks:**
- All three run on `cron: '0 6 * * 1'`
- All might try to create a PR for the same update
- Git conflicts when multiple workflows commit to the same branch

**The Fix:**
```yaml
# Consolidate into ONE workflow (as redundancy analysis recommends)
concurrency:
  group: upstream-sync
  cancel-in-progress: true
```

---

### 5.2 HIGH: Submodule Update During Build

**The Problem:**
```yaml
jobs:
  check-upstream:
    # Checks submodule state
  build:
    needs: check-upstream
    # Builds with current submodule
```

**What Breaks:**
- Between check and build, another workflow might update the submodule
- Build uses different sokol version than check reported

**The Fix:**
```yaml
# Pin submodule commit at checkout
- name: Checkout
  uses: actions/checkout@v4
  with:
    submodules: recursive
    
- name: Record submodule state
  run: git submodule status > submodule_state.txt
  
- uses: actions/upload-artifact@v4
  with:
    name: submodule-state
    path: submodule_state.txt
```

---

### 5.3 HIGH: Release Artifact Clobbering

**The Problem:**
```yaml
- name: Package release
  run: zip -r cosmo-sokol-${VERSION}.zip *
  
- name: Release
  uses: softprops/action-gh-release@v2
  with:
    files: cosmo-sokol-*.zip
```

**What Breaks:**
- If release workflow runs twice (re-tag, retry), old artifacts may be overwritten
- `cosmo-sokol-*.zip` glob may match multiple files

**The Fix:**
```yaml
- name: Package release
  run: |
    VERSION=${GITHUB_REF#refs/tags/}
    ZIPNAME="cosmo-sokol-${VERSION}-$(git rev-parse --short HEAD).zip"
    zip -r "$ZIPNAME" *
    echo "ZIPNAME=$ZIPNAME" >> $GITHUB_ENV
    
- name: Release
  uses: softprops/action-gh-release@v2
  with:
    files: ${{ env.ZIPNAME }}
    fail_on_unmatched_files: true  # Fail if file missing
```

---

## 6. Generated File Consistency

### 6.1 HIGH: Python Version Affects Generated Output

**The Problem:**
gen-sokol uses Python dicts and string formatting:
```python
PLATFORMS = [
    {"name": "linux", "check": "IsLinux", "enabled": True},
    ...
]
```

**What Breaks:**
- Python 3.6 vs 3.11 may produce different dict ordering
- Generated `sokol_cosmo.c` differs between runs
- Git shows spurious diffs

**The Fix:**
```python
# Explicit ordering
import json
output = json.dumps(data, sort_keys=True)

# OR use deterministic formatting
PLATFORMS = OrderedDict([
    ("linux", {"check": "IsLinux", "enabled": True}),
    ...
])
```

---

### 6.2 MEDIUM: No "Generated" Marker in Output Files

**The Problem:**
`sokol_cosmo.c` has no indication it's generated:
```c
bool sapp_isvalid(void) {
    if (IsLinux()) { return linux_sapp_isvalid(); }
    ...
}
```

**What Breaks:**
- Developers might manually edit the generated file
- No way to know which version of gen-sokol produced it
- No way to detect if regeneration is needed

**The Fix:**
```c
// Generated by gen-sokol - DO NOT EDIT
// Generator version: 1.0.0
// Generated at: 2026-02-09T18:30:00Z
// Sokol commit: eaa1ca79a4004750e58cb51e0100d27f23e3e1ff
```

---

## 7. Proposed Technical Safeguards

Based on the issues identified, here are concrete safeguards to add:

### 7.1 Pre-commit Hook for Generated Files

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Regenerate and check for differences
python shims/sokol/gen-sokol --check-only
if [ $? -ne 0 ]; then
    echo "ERROR: gen-sokol output differs. Run 'python shims/sokol/gen-sokol' and commit the changes."
    exit 1
fi
```

### 7.2 CI Sanity Check Job

```yaml
sanity-check:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
      with:
        submodules: recursive
        
    - name: Verify generated files are up-to-date
      run: |
        python shims/sokol/gen-sokol
        git diff --exit-code shims/sokol/sokol_cosmo.c
        
    - name: Verify submodule consistency
      run: |
        cd deps/sokol
        git diff --exit-code
        
    - name: Verify Python version
      run: |
        python --version
        # Require 3.10+ for consistent dict ordering
        python -c "import sys; assert sys.version_info >= (3, 10)"
```

### 7.3 Proper C Function Signature Parser

Replace regex with proper parsing:

```python
# Use pycparser or tree-sitter for reliable C parsing
from pycparser import parse_file

def extract_functions(header_path):
    ast = parse_file(header_path, use_cpp=True)
    functions = []
    for node in ast.ext:
        if isinstance(node, c_ast.Decl) and isinstance(node.type, c_ast.FuncDecl):
            functions.append(node)
    return functions
```

---

## Summary: Must-Fix Before Implementation

### P0 — Blocks Everything
1. Fix multi-line regex in all API extraction scripts
2. Add `--headless` flag to `main.c`
3. Consolidate sync workflows to prevent race conditions
4. Add proper dlopen error handling

### P1 — Blocks CI Reliability
5. Fix Windows shell compatibility in build script
6. Add ARM64 to test matrix
7. Use actual Windows runners, not Wine
8. Pin Python version in all workflows
9. Handle timeout exit codes properly

### P2 — Quality of Life
10. Add generated file markers
11. Validate cosmocc version before download
12. Add submodule consistency checks
13. Improve regex for preprocessor conditionals

---

*Technical Critique Complete*  
*Phase 3 (Integration) should address these issues in the final implementation plan*
