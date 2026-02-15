# Stage Prompts: neteng

**Specialist:** neteng  
**Total Stages:** 1 (single comprehensive workflow)

---

## Stage 1: build.yml Implementation

### Prompt

```
You are the neteng specialist implementing .github/workflows/build.yml for the cosmo-sokol project.

CONTEXT:
- cosmo-sokol is a Cosmopolitan libc port of sokol graphics library
- Builds produce APE (Actually Portable Executable) binaries
- Must work on Linux, Windows, and macOS from single source
- C tools in tools/ directory perform validation

TASK:
Create a complete, production-ready GitHub Actions workflow that:
1. Builds C validation tools
2. Validates sources before build
3. Builds with multiple cosmocc versions
4. Runs smoke tests on native runners (all 3 platforms)
5. Creates releases with checksums

WORKFLOW STRUCTURE:
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
  build-tools:
    # Build C tools first (validation infrastructure)
    
  validate:
    needs: build-tools
    # Run check-api-sync and validate-sources
    
  build:
    needs: validate
    strategy:
      matrix:
        cosmocc: ['3.9.5', '3.9.6']
    # Main build matrix
    
  smoke-linux:
    needs: build
    runs-on: ubuntu-latest
    
  smoke-windows:
    needs: build
    runs-on: windows-latest
    
  smoke-macos:
    needs: build
    runs-on: macos-latest
    
  release:
    needs: [smoke-linux, smoke-windows, smoke-macos]
    if: startsWith(github.ref, 'refs/tags/')
```

CRITICAL REQUIREMENTS:

1. **SHA-Pinned Actions** (security):
```yaml
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
  with:
    submodules: recursive

- uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02  # v4.6.0
- uses: actions/download-artifact@95815c38cf2ff2164869cbab79da8d1f422bc89e  # v4.1.9
- uses: softprops/action-gh-release@c95fe1489396fe8a9eb87c0abf8aa5b2ef267fda  # v2.2.1
```

2. **cosmocc Setup**:
```yaml
- name: Setup cosmocc
  run: |
    COSMOCC_VERSION="${{ matrix.cosmocc || '3.9.6' }}"
    mkdir -p $HOME/cosmocc
    curl -sSL "https://cosmo.zip/pub/cosmocc/cosmocc-${COSMOCC_VERSION}.zip" \
      -o /tmp/cosmocc.zip
    unzip -q /tmp/cosmocc.zip -d $HOME/cosmocc
    echo "$HOME/cosmocc/bin" >> $GITHUB_PATH
```

3. **Error Propagation in Tool Build** (P2 fix):
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

4. **Headless Smoke Tests** (critical for CI):
```yaml
- name: Smoke test
  run: |
    chmod +x ./cosmo-sokol-demo
    timeout 30 ./cosmo-sokol-demo --headless --frames 10 || {
      echo "::error::Smoke test failed or timed out"
      exit 1
    }
```

5. **Checksums in Release**:
```yaml
- name: Generate checksums
  run: |
    cd artifacts
    sha256sum * > SHA256SUMS.txt
    sha512sum * > SHA512SUMS.txt
    cat SHA256SUMS.txt
```

6. **Windows Compatibility**:
```yaml
smoke-windows:
  runs-on: windows-latest
  defaults:
    run:
      shell: bash  # Use Git Bash for APE compatibility
```

ARTIFACT NAMES:
- build-tools: tools-${{ github.sha }}
- build: cosmo-sokol-${{ matrix.cosmocc }}-${{ github.sha }}

TIMEOUT:
- build-tools: 5 minutes
- validate: 2 minutes
- build: 15 minutes
- smoke tests: 5 minutes each
- release: 10 minutes

Provide the complete workflow YAML file.
```

---

## Verification Commands

After implementation:

```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('.github/workflows/build.yml'))"

# Dry run with act (local testing)
act --dryrun push

# Check SHA pins are valid
grep -E "uses:.*@[a-f0-9]{40}" .github/workflows/build.yml
```

---

*neteng Stage Prompts Complete*
