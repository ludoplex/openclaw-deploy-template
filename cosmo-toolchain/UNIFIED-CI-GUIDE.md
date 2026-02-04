# Cosmopolitan Toolchain - Unified CI/CD Guide

This document describes the unified CI/CD approach for the Cosmopolitan toolchain projects.

## Projects

| Project | Purpose | Binary Output |
|---------|---------|---------------|
| tedit-cosmo | Text editor (C) | `tedit.com` |
| e9studio | Binary analysis tool | `e9studio.com` |
| llamafile-llm | Local LLM configuration | N/A (uses pre-built llamafile.exe) |

## CI Architecture

### Common Pattern

All APE-producing projects follow this workflow structure:

```
┌─────────────┐     ┌─────────────┐
│  security   │     │    lint     │
│  (Gitleaks  │     │  (headers,  │
│   + Trivy)  │     │   C checks) │
└──────┬──────┘     └──────┬──────┘
       │                   │
       └────────┬──────────┘
                ▼
        ┌───────────────┐
        │   build-ape   │ (Linux + cosmocc)
        │  (+ caching)  │
        └───────┬───────┘
                │
       ┌────────┴────────┐
       ▼                 ▼
┌─────────────┐   ┌─────────────┐
│ test-macos  │   │ test-macos  │
│   (Intel)   │   │   (ARM64)   │
└──────┬──────┘   └──────┬──────┘
       │                 │
       └────────┬────────┘
                ▼
        ┌───────────────┐
        │   release     │ (on tag/release)
        └───────────────┘
```

### Key Components

#### 1. Security Scanning (First)

```yaml
security:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0  # Required for Gitleaks

    - uses: gitleaks/gitleaks-action@v2
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

    - uses: aquasecurity/trivy-action@0.33.1
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy.sarif'
        severity: 'CRITICAL,HIGH'

    - uses: github/codeql-action/upload-sarif@v3
      with:
        sarif_file: trivy.sarif
```

#### 2. Cosmocc Setup with Caching

```yaml
env:
  COSMOCC_VERSION: "3.9.7"

steps:
  - name: Cache cosmocc toolchain
    uses: actions/cache@v4
    with:
      path: ${{ github.workspace }}/cosmocc
      key: cosmocc-${{ env.COSMOCC_VERSION }}-${{ runner.os }}-v3

  - name: Install cosmocc
    if: steps.cache-cosmocc.outputs.cache-hit != 'true'
    run: |
      mkdir -p $GITHUB_WORKSPACE/cosmocc
      cd $GITHUB_WORKSPACE/cosmocc
      curl -fsSL "https://cosmo.zip/pub/cosmocc/cosmocc.zip" -o cosmocc.zip
      unzip -q cosmocc.zip
      rm cosmocc.zip
```

#### 3. APE Loader for Linux

```yaml
- name: Setup APE loader
  run: |
    if [ -f $GITHUB_WORKSPACE/cosmocc/bin/ape-x86_64.elf ]; then
      sudo cp $GITHUB_WORKSPACE/cosmocc/bin/ape-x86_64.elf /usr/bin/ape
      sudo chmod +x /usr/bin/ape
    fi
    sudo sh -c "echo ':APE:M::MZqFpD::/usr/bin/ape:' >/proc/sys/fs/binfmt_misc/register" 2>/dev/null || true
```

#### 4. ZipOS Resource Embedding

```yaml
- name: Create embedded resources
  run: |
    mkdir -p .cosmo
    echo "My App - APE Binary" > .cosmo/README
    echo "$(git describe --tags 2>/dev/null || echo 'dev')" > .cosmo/VERSION
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > .cosmo/BUILD_TIME
    
    # Include config files, WASM modules, etc.
    cp config.ini .cosmo/ 2>/dev/null || true
    
    zip -r resources.zip .cosmo/
    cat resources.zip >> myapp.com
    chmod +x myapp.com
```

#### 5. Multi-Platform Testing

```yaml
test-macos-intel:
  needs: build-ape
  runs-on: macos-15
  steps:
    - uses: actions/download-artifact@v4
      with:
        name: my-app-ape
    - run: |
        chmod +x myapp.com
        ./myapp.com --help || true

test-macos-arm:
  needs: build-ape
  runs-on: macos-latest
  steps:
    - uses: actions/download-artifact@v4
      with:
        name: my-app-ape
    - run: |
        chmod +x myapp.com
        ./myapp.com --help || true
```

## Security Tools Reference

| Tool | Purpose | When to Use |
|------|---------|-------------|
| **Gitleaks** | Secret detection | Always - catches leaked credentials |
| **Trivy** | Vulnerability scanning | Always - covers files, containers, IaC |
| **CodeQL** | Deep static analysis | For complex C/C++ projects |
| **Bandit** | Python SAST | If Python is involved |
| **Semgrep** | Multi-language SAST | For custom security rules |

## C Code Security Checks

For C projects, include these lint checks:

```yaml
- name: Check for dangerous functions
  run: |
    # CRITICAL: Never use gets()
    if grep -rn "gets\s*(" src/; then
      exit 1
    fi
    
    # WARNING: Review sprintf/strcpy/strcat usage
    for func in sprintf strcpy strcat; do
      grep -rn "${func}\s*(" src/ || true
    done
```

## Triggers

Standard trigger configuration:

```yaml
on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]
  release:
    types: [created]
  workflow_dispatch:
```

For projects with WASM/optional components, add path filters:

```yaml
on:
  push:
    paths:
      - 'src/**'
      - 'Makefile*'
      - '.github/workflows/**'
```

## Reusable Workflows

Centralized reusable workflows are available at:
- `cosmo-toolchain/reusable-workflows/setup-cosmocc.yml`
- `cosmo-toolchain/reusable-workflows/release-ape.yml`

To use (once published to a central repo):

```yaml
jobs:
  build:
    uses: your-org/.github/.github/workflows/setup-cosmocc.yml@main
    with:
      cosmocc-version: "3.9.7"
```

## GitHub Actions Tips for APE

1. **Use ubuntu-latest for primary builds** - cosmocc cross-compiles, so Linux is fine
2. **Cache is essential** - cosmocc download is ~100MB
3. **Test on actual macOS runners** - Intel (macos-15) and ARM (macos-latest)
4. **APE loader is required on Linux** - Won't execute without binfmt_misc registration
5. **ZipOS for embedded resources** - Append ZIP to binary for portable config

## File Structure

After implementing unified CI:

```
project/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml          # Main build + test + release
│   │   └── security.yml    # Dedicated security scanning (optional)
│   └── mlc-config.json     # Markdown link check config (if using)
├── src/
├── Makefile
└── README.md
```
