# Specialist Plan: neteng

**Specialist:** neteng  
**Domain:** CI/CD deployment, build workflows, platform testing  
**Priority:** #3 (High)  
**Dependencies:** Phase 1 (C tools exist)  
**Estimated Effort:** 4 hours

---

## Mission

Implement the production-ready GitHub Actions workflow that builds, validates, and releases cosmo-sokol across all platforms.

## Deliverables

| File | Priority | Description |
|------|----------|-------------|
| `.github/workflows/build.yml` | P0 | Complete build/test/release workflow |

## Technical Specifications

### build.yml Architecture

```yaml
name: Build cosmo-sokol

on:
  push:
    branches: [main, develop]
    tags: ['v*']
  pull_request:
    branches: [main]
  workflow_dispatch:

jobs:
  # Phase 1: Build C tools (APE binaries)
  build-tools:
    runs-on: ubuntu-latest
    steps:
      - checkout
      - setup cosmocc
      - make -C tools all
      - upload tools artifact

  # Phase 2: Validate sources
  validate:
    needs: build-tools
    runs-on: ubuntu-latest
    steps:
      - checkout with submodules
      - download tools
      - ./tools/validate-sources
      - ./tools/check-api-sync

  # Phase 3: Build matrix
  build:
    needs: validate
    strategy:
      matrix:
        cosmocc: ['3.9.5', '3.9.6']
    runs-on: ubuntu-latest
    steps:
      - build with specified cosmocc version
      - upload build artifacts

  # Phase 4: Platform smoke tests (native runners)
  smoke-linux:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - download artifacts
      - run headless smoke test

  smoke-windows:
    needs: build
    runs-on: windows-latest
    steps:
      - download artifacts
      - run smoke test (--headless critical!)

  smoke-macos:
    needs: build
    runs-on: macos-latest
    steps:
      - download artifacts
      - run smoke test

  # Phase 5: Release (tag-triggered)
  release:
    needs: [smoke-linux, smoke-windows, smoke-macos]
    if: startsWith(github.ref, 'refs/tags/')
    runs-on: ubuntu-latest
    steps:
      - create checksums
      - create GitHub release
      - upload assets
```

### Critical Implementation Details

#### cosmocc Setup
```yaml
- name: Setup cosmocc
  run: |
    mkdir -p $HOME/cosmocc
    curl -sSL https://cosmo.zip/pub/cosmocc/cosmocc-${{ matrix.cosmocc || '3.9.6' }}.zip \
      | tar -xzf - -C $HOME/cosmocc
    echo "$HOME/cosmocc/bin" >> $GITHUB_PATH
```

#### C Tools Build with Error Propagation (P2 Fix)
```yaml
- name: Build C tools
  run: |
    if [ -d tools ] && [ -f tools/Makefile ]; then
      cd tools
      if ! make all; then
        echo "::error::C tool build failed"
        exit 1
      fi
      echo "✓ C tools built successfully"
    else
      echo "::notice::tools/ directory not yet created - skipping"
    fi
```

#### Headless Flag (Critical for CI)
```yaml
- name: Smoke test (Linux)
  run: |
    chmod +x ./cosmo-sokol-demo
    ./cosmo-sokol-demo --headless --frames 10 || exit 1
```

#### SHA-Pinned Actions
```yaml
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
- uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02  # v4.6.0
- uses: actions/download-artifact@95815c38cf2ff2164869cbab79da8d1f422bc89e  # v4.1.9
```

#### Checksums and Release
```yaml
- name: Generate checksums
  run: |
    cd artifacts
    sha256sum * > SHA256SUMS.txt
    sha512sum * > SHA512SUMS.txt

- name: Create Release
  uses: softprops/action-gh-release@c95fe1489396fe8a9eb87c0abf8aa5b2ef267fda  # v2.2.1
  with:
    files: |
      artifacts/*
      artifacts/SHA256SUMS.txt
    generate_release_notes: true
```

## Success Criteria

- [ ] `build.yml` passes YAML linting
- [ ] build-tools job completes successfully
- [ ] validate job runs C tools and passes
- [ ] build matrix produces artifacts for both cosmocc versions
- [ ] smoke tests pass on all 3 platforms
- [ ] Release job creates proper GitHub release with checksums
- [ ] All action versions are SHA-pinned

## File Location

```
C:\cosmo-sokol\
└── .github\
    └── workflows\
        └── build.yml    # REPLACE
```

## Dependencies

- **Requires:** C tools in tools/ directory (cosmo deliverable)
- **Requires:** Makefile exists (seeker deliverable)
- **Provides to:** All platforms get tested binaries

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| CI runner unavailable | Fallback: ubuntu-latest always available |
| cosmocc download fails | Cache cosmocc, retry logic |
| Smoke test hangs | --headless flag, timeout |
| Make error silent | Explicit error check and exit |

## Platform-Specific Notes

### Linux (ubuntu-latest)
- Primary build platform
- X11 libraries may need installation for linking

### Windows (windows-latest)
- APE binaries work in Git Bash
- --headless critical (no display)
- Use bash shell explicitly

### macOS (macos-latest)
- OpenGL deprecated warnings expected
- Metal not yet supported (future)
- --headless critical

---

*neteng Plan Complete*
