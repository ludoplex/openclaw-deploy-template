# Distribution & Deployment Report: cosmo-sokol Fork

**Date:** 2026-02-09  
**Agent:** neteng  
**Focus:** Build outputs, platform verification, release packaging, cosmocc toolchain, cross-platform testing

---

## Executive Summary

The ludoplex/cosmo-sokol fork produces **Actually Portable Executables (APE)** — single fat binaries that run natively on Linux, Windows, and (with stub support) macOS. Distribution is straightforward but the current CI/CD pipeline has opportunities for automation improvements, particularly around cosmocc versioning and cross-platform verification.

---

## 1. Build Outputs

### What Gets Produced

| Artifact | Location | Description |
|----------|----------|-------------|
| `bin/cosmo-sokol` | Local build | APE binary (~fat executable) |
| `bin/cosmo-sokol.zip` | CI release | Packaged release artifact |

### APE Binary Characteristics

- **Format:** Polyglot PE+ELF+MachO+ZIP+SH
- **Single file:** Runs on Linux, Windows, macOS without recompilation
- **Self-contained:** No external runtime dependencies
- **Embeddable assets:** Can include ZIP-embedded resources

### Build Process

```bash
# Local build
./build  # Produces bin/cosmo-sokol

# CI build (GitHub Actions)
# Uses parallel compilation via GNU parallel
# Produces both raw binary and .zip package
```

---

## 2. Cosmocc Toolchain

### Installation Methods

#### Method 1: Direct Download (Manual)
```bash
mkdir -p cosmocc && cd cosmocc
wget https://cosmo.zip/pub/cosmocc/cosmocc.zip
unzip cosmocc.zip
export PATH="$PATH:$(pwd)/bin"
```

#### Method 2: GitHub Actions (CI)
```yaml
- uses: bjia56/setup-cosmocc@main
  with:
    version: "3.9.6"  # Currently pinned
```

### Version Requirements

| Requirement | Version | Notes |
|-------------|---------|-------|
| Minimum | 3.9.5 | Required for cosmo-sokol features |
| Current CI | 3.9.6 | Pinned in workflow |
| Latest | 4.0.2 | Available at cosmo.zip |

### ⚠️ Issue: Manual Version Pinning

The current workflow **manually pins** cosmocc version `3.9.6`:
```yaml
- uses: bjia56/setup-cosmocc@main
  with:
    version: "3.9.6"
```

**Recommendation:** Implement auto-update strategy:
1. Use `version: "latest"` for development builds
2. Pin specific version only for release tags
3. Add CI job to test against latest cosmocc periodically

---

## 3. Platform Verification

### Current Platform Support Matrix

| Platform | Status | Graphics Backend | Verification |
|----------|--------|------------------|--------------|
| Linux | ✅ Full | OpenGL via dlopen(libGL.so) | CI tested |
| Windows | ✅ Full | OpenGL via WGL | Manual only |
| macOS | 🚧 Stub | Planned: Metal/OpenGL | Not functional |

### Linux Verification

**Native execution:**
```bash
./bin/cosmo-sokol
```

**APE Loader setup (recommended):**
```bash
sudo wget -O /usr/bin/ape https://cosmo.zip/pub/cosmos/bin/ape-$(uname -m).elf
sudo chmod +x /usr/bin/ape
sudo sh -c "echo ':APE:M::MZqFpD::/usr/bin/ape:' >/proc/sys/fs/binfmt_misc/register"
```

**Troubleshooting:**
- If "run-detectors: unable to find an interpreter" → Install APE Loader
- If WINE intercepts → Register APE with binfmt_misc

### Windows Verification

**Native execution:**
```cmd
bin\cosmo-sokol.exe
```

Or rename to `.com`:
```cmd
bin\cosmo-sokol.com
```

**Notes:**
- Windows 8+ required (Cosmopolitan support vector)
- No MSVC/MinGW dependencies
- Self-extracting if needed

### macOS Verification (Currently Non-Functional)

**Current status:** Stub implementation — compiles but shows error at runtime.

**Challenge:** Sokol's macOS backend uses Objective-C (NSApplication, NSWindow, etc.)

**Solution path documented in fork:**
```c
// Future: Use objc_msgSend from C
void* libobjc = cosmo_dlopen("/usr/lib/libobjc.dylib", RTLD_NOW);
id app = objc_msgSend(objc_getClass("NSApplication"), 
                      sel_registerName("sharedApplication"));
```

**macOS Requirements:**
- Darwin 23.1.0+ (macOS Sonoma 14.1+)
- Cosmopolitan support is relatively recent

---

## 4. Release Packaging

### Current CI Pipeline

```yaml
# .github/workflows/build.yml
- name: Package binaries
  if: startsWith(github.ref, 'refs/tags/')
  run: |
    cd bin
    zip -r cosmo-sokol.zip *

- name: Release
  uses: softprops/action-gh-release@v2
  if: startsWith(github.ref, 'refs/tags/')
  with:
    draft: true
    files: |
      bin/cosmo-sokol.zip
```

### Release Status

**Current:** No releases published yet (fork is new)

### Recommended Release Structure

```
cosmo-sokol-v1.0.0/
├── cosmo-sokol          # APE binary (runs everywhere)
├── cosmo-sokol.dbg      # Debug symbols (optional)
├── README.md            # Quick start guide
├── CHANGELOG.md         # Version history
└── checksums.sha256     # Integrity verification
```

### Release Improvements

1. **Add checksums:**
   ```yaml
   - name: Generate checksums
     run: |
       cd bin
       sha256sum cosmo-sokol > checksums.sha256
   ```

2. **Add version info to binary:**
   ```c
   // Embed version from git tag
   const char* VERSION = GIT_TAG;
   ```

3. **Auto-publish releases (not draft):**
   ```yaml
   draft: false
   prerelease: ${{ contains(github.ref, 'alpha') || contains(github.ref, 'beta') }}
   ```

---

## 5. Cross-Platform Testing Strategies

### Strategy 1: GitHub Actions Matrix (Recommended)

```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: cosmo-sokol-binary
      - name: Test execution
        run: |
          chmod +x cosmo-sokol 2>/dev/null || true
          ./cosmo-sokol --version || echo "Platform: ${{ matrix.os }}"
```

### Strategy 2: QEMU for Architecture Testing

```yaml
- name: Test ARM64 via QEMU
  uses: uraimo/run-on-arch-action@v2
  with:
    arch: aarch64
    distro: ubuntu22.04
    run: |
      ./cosmo-sokol --version
```

### Strategy 3: Docker for Linux Variant Testing

```yaml
services:
  alpine:
    image: alpine:latest
  debian:
    image: debian:bookworm
  fedora:
    image: fedora:latest
    
steps:
  - name: Test on Alpine
    run: docker run -v $PWD:/app alpine /app/bin/cosmo-sokol --version
```

### Strategy 4: Windows Specific

```yaml
- name: Windows test
  if: runner.os == 'Windows'
  shell: cmd
  run: |
    ren bin\cosmo-sokol bin\cosmo-sokol.exe
    bin\cosmo-sokol.exe --version
```

### Verification Checklist

| Test | Linux | Windows | macOS |
|------|-------|---------|-------|
| Binary executes | ✅ CI | 🔲 Add | 🚧 Stub |
| Window opens | Manual | Manual | N/A |
| Graphics renders | Manual | Manual | N/A |
| Graceful exit | Manual | Manual | N/A |

---

## 6. Deployment Automation Recommendations

### Auto-Update Cosmocc Version

```yaml
# .github/workflows/update-cosmocc.yml
name: Check Cosmocc Updates

on:
  schedule:
    - cron: '0 0 * * 1'  # Weekly

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - name: Get latest cosmocc version
        run: |
          LATEST=$(curl -s https://cosmo.zip/pub/cosmocc/ | grep -oP 'cosmocc-\K[0-9.]+(?=\.zip)' | sort -V | tail -1)
          echo "LATEST_VERSION=$LATEST" >> $GITHUB_ENV
      
      - name: Update workflow if needed
        uses: peter-evans/create-pull-request@v5
        with:
          title: "chore: bump cosmocc to ${{ env.LATEST_VERSION }}"
          body: "Auto-generated PR to update cosmocc version"
```

### Binary Size Tracking

```yaml
- name: Track binary size
  run: |
    SIZE=$(stat -f%z bin/cosmo-sokol 2>/dev/null || stat -c%s bin/cosmo-sokol)
    echo "Binary size: $SIZE bytes"
    # Could push to metrics service
```

---

## 7. Known Issues & Mitigations

### Issue: macOS Not Functional

**Current:** Stub implementation only  
**Blocker:** Cosmopolitan cannot compile Objective-C  
**Mitigation:** Low-priority until objc_msgSend approach is implemented

### Issue: Manual OpenGL Header Management

**Current:** Linux headers symlinked into shims/linux  
**Risk:** Header drift from system  
**Mitigation:** Document required dev packages in CI

### Issue: WSL Interop Conflicts

**Current:** WSL tries to run APE as Windows binary  
**Fix:** Users must disable WSLInterop:
```bash
sudo sh -c "echo -1 >/proc/sys/fs/binfmt_misc/WSLInterop"
```

---

## 8. Summary: Ensuring Fork Works Everywhere

### Immediate Actions

1. ✅ **Keep current CI** — Linux build/test working
2. 🔲 **Add Windows test job** — Verify .exe execution
3. 🔲 **Add checksums to releases** — Integrity verification
4. 🔲 **Document APE loader setup** — In release README

### Medium-Term Actions

1. 🔲 **Auto-update cosmocc** — Weekly version check PR
2. 🔲 **Multi-OS test matrix** — GitHub Actions
3. 🔲 **Binary size tracking** — Catch bloat regressions

### Long-Term Actions

1. 🚧 **macOS implementation** — objc_msgSend approach
2. 🔲 **ARM64 testing** — QEMU or native runners
3. 🔲 **FreeBSD/OpenBSD testing** — Cosmopolitan supports these

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `.github/workflows/build.yml` | CI/CD pipeline |
| `build` | Build script |
| `shims/sokol/sokol_cosmo.c` | Runtime platform dispatch |
| `shims/linux/` | Linux-specific shims |
| `shims/macos/README.md` | macOS implementation docs |

---

*Report generated for Swiss Rounds evaluation of ludoplex/cosmo-sokol fork maintenance strategy.*
