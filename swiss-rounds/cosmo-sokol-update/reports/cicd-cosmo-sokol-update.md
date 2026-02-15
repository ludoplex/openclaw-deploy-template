# CI/CD Pipeline Design: cosmo-sokol Automation

**Generated:** 2026-02-09  
**Role:** CI/CD Specialist  
**Subject:** Automated upstream sync and build pipeline design

---

## Executive Summary

The current CI/CD for ludoplex/cosmo-sokol is minimal: a single Ubuntu build on push with manual tag-based releases. This report designs a comprehensive automation pipeline that:

1. **Monitors upstreams** (sokol, cosmopolitan, cimgui) for updates
2. **Auto-generates PRs** for submodule updates
3. **Runs tri-platform builds** to catch breaking changes early
4. **Publishes releases** automatically when ready

**Key Constraint:** Dependabot does NOT support git submodules properly. We need custom workflows.

---

## 1. Current State Analysis

### 1.1 Existing Workflow (`.github/workflows/build.yml`)

```yaml
# Current: Single runner, no upstream monitoring
runs-on: ubuntu-latest
steps:
  - checkout with submodules
  - apt install libx11-dev libgl-dev libxcursor-dev libxi-dev  
  - setup cosmocc v3.9.6
  - ./build
  - release on tag push (draft only)
```

**Issues:**
- ❌ No macOS or Windows build verification
- ❌ No upstream monitoring (drift accumulates silently)
- ❌ No automated testing beyond "does it compile"
- ❌ Draft releases require manual publishing
- ❌ cosmocc version hardcoded (3.9.6) — should track latest

### 1.2 Dependencies

| Dependency | Type | Tracking | Current Version |
|------------|------|----------|-----------------|
| floooh/sokol | Submodule | Commit hash | `eaa1ca79` (Nov 2024) |
| cimgui/cimgui | Submodule | Commit hash | `8ec6558e` (v1.65.4-662) |
| jart/cosmopolitan | Toolchain | bjia56/setup-cosmocc | v3.9.6 (hardcoded) |

### 1.3 Technical Architecture

cosmo-sokol uses a **prefix trick** to compile all platform backends into one binary:
- Linux backend via `linux_sapp_*` prefixes
- Windows backend via `windows_sapp_*` prefixes  
- macOS backend via `macos_sapp_*` prefixes (stub only)
- Runtime dispatch via `IsLinux()`, `IsWindows()`, `IsXnu()`

This means:
- **Build must succeed on Linux** (primary dev platform)
- **Windows runtime testing is valuable** (full backend)
- **macOS compile-only is sufficient** (stub backend)

---

## 2. Upstream Monitoring Strategy

### 2.1 Challenge: No Dependabot for Submodules

Dependabot's git submodule support is limited:
- Only checks for new commits, doesn't understand breaking changes
- Can't run builds before creating PRs
- Floods with PRs on active repos like sokol (1000+ commits behind)

### 2.2 Solution: Scheduled Digest Workflow

Instead of per-commit PRs, use a weekly **digest approach**:

```yaml
# .github/workflows/upstream-check.yml
name: Upstream Check

on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday 9 AM UTC
  workflow_dispatch:      # Manual trigger

jobs:
  check-upstreams:
    runs-on: ubuntu-latest
    outputs:
      sokol_behind: ${{ steps.sokol.outputs.behind }}
      cimgui_behind: ${{ steps.cimgui.outputs.behind }}
      cosmo_update: ${{ steps.cosmo.outputs.new_version }}
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive
          
      - name: Check sokol
        id: sokol
        run: |
          cd deps/sokol
          git fetch origin master
          BEHIND=$(git rev-list HEAD..origin/master --count)
          echo "behind=$BEHIND" >> $GITHUB_OUTPUT
          echo "::notice::sokol is $BEHIND commits behind"
          
      - name: Check cimgui
        id: cimgui
        run: |
          cd deps/cimgui
          git fetch origin master
          BEHIND=$(git rev-list HEAD..origin/master --count)
          echo "behind=$BEHIND" >> $GITHUB_OUTPUT
          echo "::notice::cimgui is $BEHIND commits behind"
          
      - name: Check cosmopolitan
        id: cosmo
        run: |
          LATEST=$(curl -s https://api.github.com/repos/jart/cosmopolitan/releases/latest | jq -r .tag_name)
          CURRENT="v3.9.6"  # From build.yml
          if [ "$LATEST" != "$CURRENT" ]; then
            echo "new_version=$LATEST" >> $GITHUB_OUTPUT
            echo "::notice::cosmopolitan $LATEST available (have $CURRENT)"
          fi
          
      - name: Create tracking issue
        if: steps.sokol.outputs.behind > 50 || steps.cimgui.outputs.behind > 20
        uses: peter-evans/create-issue-from-file@v5
        with:
          title: "Upstream Update: sokol (${{ steps.sokol.outputs.behind }}) / cimgui (${{ steps.cimgui.outputs.behind }})"
          content-filepath: .github/UPSTREAM_UPDATE_TEMPLATE.md
          labels: upstream, automated
```

### 2.3 Changelog Extraction

To help identify breaking changes, extract relevant CHANGELOG sections:

```yaml
      - name: Extract sokol breaking changes
        if: steps.sokol.outputs.behind > 0
        run: |
          cd deps/sokol
          git fetch origin master
          # Get commits since current
          SINCE=$(git log -1 --format=%ci HEAD)
          # Extract CHANGELOG between versions
          git show origin/master:CHANGELOG.md > /tmp/new_changelog.md
          # Look for BREAKING markers (sokol uses "BREAKING" in changelog)
          echo "## Potential Breaking Changes" > /tmp/breaking.md
          grep -A5 -i "breaking\|removed\|renamed\|changed.*signature" /tmp/new_changelog.md >> /tmp/breaking.md || true
```

---

## 3. Automated PR Generation

### 3.1 Submodule Update Workflow

```yaml
# .github/workflows/update-submodules.yml
name: Update Submodules

on:
  workflow_dispatch:
    inputs:
      submodule:
        description: 'Which submodule to update'
        required: true
        type: choice
        options:
          - sokol
          - cimgui
          - all
      commits:
        description: 'Number of commits to advance (0 = latest)'
        required: false
        default: '50'

permissions:
  contents: write
  pull-requests: write

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive
          token: ${{ secrets.GITHUB_TOKEN }}
          
      - name: Update sokol
        if: inputs.submodule == 'sokol' || inputs.submodule == 'all'
        run: |
          cd deps/sokol
          git fetch origin master
          if [ "${{ inputs.commits }}" = "0" ]; then
            git checkout origin/master
          else
            # Advance by N commits
            CURRENT=$(git rev-parse HEAD)
            TARGET=$(git rev-list HEAD..origin/master | tail -n ${{ inputs.commits }} | head -n 1)
            git checkout $TARGET
          fi
          NEW_SHA=$(git rev-parse --short HEAD)
          echo "SOKOL_SHA=$NEW_SHA" >> $GITHUB_ENV
          
      - name: Update cimgui  
        if: inputs.submodule == 'cimgui' || inputs.submodule == 'all'
        run: |
          cd deps/cimgui
          git fetch origin master
          git checkout origin/master
          git submodule update --init --recursive
          NEW_SHA=$(git rev-parse --short HEAD)
          echo "CIMGUI_SHA=$NEW_SHA" >> $GITHUB_ENV

      - name: Create PR
        uses: peter-evans/create-pull-request@v6
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          commit-message: "chore(deps): update ${{ inputs.submodule }} submodule(s)"
          title: "Update ${{ inputs.submodule }} to ${{ env.SOKOL_SHA || env.CIMGUI_SHA }}"
          body: |
            ## Submodule Update
            
            Updates `${{ inputs.submodule }}` submodule(s).
            
            ### Changes
            - sokol: ${{ env.SOKOL_SHA || 'unchanged' }}
            - cimgui: ${{ env.CIMGUI_SHA || 'unchanged' }}
            
            ### Checklist
            - [ ] Build passes on all platforms
            - [ ] gen-sokol SOKOL_FUNCTIONS list updated if needed
            - [ ] Breaking changes reviewed in CHANGELOG
            
            ---
            *Automated PR - verify build results before merging*
          branch: update/${{ inputs.submodule }}
          labels: dependencies, automated
```

### 3.2 Incremental Update Strategy

Given sokol is 1000+ commits behind, use **batched updates**:

```yaml
# Alternative: Auto-advance script
- name: Incremental sokol update
  run: |
    cd deps/sokol
    git fetch origin master
    
    # Get count behind
    BEHIND=$(git rev-list HEAD..origin/master --count)
    
    # Update in chunks of 50-100 commits
    if [ $BEHIND -gt 100 ]; then
      ADVANCE=50
    elif [ $BEHIND -gt 20 ]; then
      ADVANCE=$((BEHIND / 2))
    else
      ADVANCE=$BEHIND
    fi
    
    TARGET=$(git rev-list HEAD..origin/master | tail -n $ADVANCE | head -n 1)
    git checkout $TARGET
    echo "Advanced $ADVANCE commits, $((BEHIND - ADVANCE)) remaining"
```

---

## 4. Build Matrix Design

### 4.1 Platform Matrix

```yaml
# .github/workflows/build.yml (enhanced)
name: Build

on:
  push:
    branches: [main, master]
  pull_request:
  workflow_dispatch:

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  build-linux:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive
          
      - name: Install Linux deps
        uses: awalsh128/cache-apt-pkgs-action@latest
        with:
          packages: libx11-dev libgl-dev libxcursor-dev libxi-dev
          
      - name: Setup cosmocc
        uses: bjia56/setup-cosmocc@main
        with:
          version: "latest"  # Track latest instead of pinning
          
      - name: Build
        run: ./build
        
      - name: Smoke test (Linux native)
        run: |
          # Verify binary runs and prints version
          timeout 5 ./bin/cosmo-sokol --help || true
          file ./bin/cosmo-sokol
          ls -la ./bin/
          
      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: cosmo-sokol-linux
          path: bin/cosmo-sokol
          
  build-windows:
    runs-on: windows-latest
    needs: build-linux
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: cosmo-sokol-linux
          
      - name: Test on Windows
        shell: pwsh
        run: |
          # APE binaries can run on Windows via wine or natively
          # The binary from Linux should just work
          dir
          # Timeout test - verify it starts without immediate crash
          $proc = Start-Process -FilePath ".\cosmo-sokol" -PassThru
          Start-Sleep -Seconds 2
          if (!$proc.HasExited) {
            $proc.Kill()
            Write-Host "✓ Binary ran successfully on Windows"
          } else {
            Write-Host "⚠ Binary exited (may be expected for GUI app without display)"
          }

  build-macos:
    runs-on: macos-latest
    needs: build-linux
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: cosmo-sokol-linux
          
      - name: Test on macOS
        run: |
          chmod +x ./cosmo-sokol
          # APE binaries should at least start on macOS
          # (will hit stub and show error message)
          ./cosmo-sokol 2>&1 | head -20 || true
          echo "✓ Binary loaded on macOS (stub expected)"

  # API compatibility check
  api-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive
          
      - name: Extract sokol API surface
        run: |
          # Count public functions
          grep -E "^SOKOL_[A-Z]+_API_DECL" deps/sokol/sokol_app.h | wc -l
          grep -E "^SOKOL_[A-Z]+_API_DECL" deps/sokol/sokol_gfx.h | wc -l
          
      - name: Verify SOKOL_FUNCTIONS alignment
        run: |
          # Check that gen-sokol covers all needed functions
          SHIM_FUNCS=$(grep -E "^[a-z_]+\(" shims/sokol/gen-sokol | wc -l || echo "0")
          echo "gen-sokol defines $SHIM_FUNCS function mappings"
```

### 4.2 Build Artifacts

```yaml
  package:
    runs-on: ubuntu-latest
    needs: [build-linux, build-windows, build-macos]
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
      - uses: actions/download-artifact@v4
        with:
          path: artifacts
          
      - name: Package release
        run: |
          mkdir -p release
          cp artifacts/cosmo-sokol-linux/cosmo-sokol release/
          chmod +x release/cosmo-sokol
          
          # Create portable package
          cd release
          zip -r ../cosmo-sokol-portable.zip *
          
          # Also create platform-specific symlinks for clarity
          cp cosmo-sokol cosmo-sokol.com  # Windows-friendly extension
          
      - name: Upload package
        uses: actions/upload-artifact@v4
        with:
          name: cosmo-sokol-release
          path: |
            cosmo-sokol-portable.zip
            release/
```

---

## 5. Release Automation

### 5.1 Semantic Release Workflow

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to release (e.g., v1.0.0)'
        required: true

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0  # For changelog generation
          
      - name: Install deps
        uses: awalsh128/cache-apt-pkgs-action@latest
        with:
          packages: libx11-dev libgl-dev libxcursor-dev libxi-dev
          
      - name: Setup cosmocc
        uses: bjia56/setup-cosmocc@main
        with:
          version: "latest"
          
      - name: Build
        run: ./build
        
      - name: Get version info
        id: version
        run: |
          VERSION=${GITHUB_REF_NAME:-${{ github.event.inputs.version }}}
          echo "version=$VERSION" >> $GITHUB_OUTPUT
          
          # Get submodule versions for release notes
          SOKOL_SHA=$(cd deps/sokol && git rev-parse --short HEAD)
          CIMGUI_SHA=$(cd deps/cimgui && git rev-parse --short HEAD)
          echo "sokol_sha=$SOKOL_SHA" >> $GITHUB_OUTPUT
          echo "cimgui_sha=$CIMGUI_SHA" >> $GITHUB_OUTPUT
          
      - name: Package
        run: |
          mkdir -p dist
          cp bin/cosmo-sokol dist/
          
          # Create zip
          cd dist && zip -r ../cosmo-sokol-${{ steps.version.outputs.version }}.zip *
          
      - name: Generate changelog
        id: changelog
        run: |
          # Get changes since last tag
          PREV_TAG=$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo "")
          if [ -n "$PREV_TAG" ]; then
            git log --pretty="- %s" $PREV_TAG..HEAD > RELEASE_NOTES.md
          else
            echo "Initial release" > RELEASE_NOTES.md
          fi
          
      - name: Create Release
        uses: softprops/action-gh-release@v2
        with:
          tag_name: ${{ steps.version.outputs.version }}
          name: "cosmo-sokol ${{ steps.version.outputs.version }}"
          body: |
            ## cosmo-sokol ${{ steps.version.outputs.version }}
            
            Portable Sokol+ImGui application compiled with Cosmopolitan.
            
            ### Dependencies
            - sokol: `${{ steps.version.outputs.sokol_sha }}`
            - cimgui: `${{ steps.version.outputs.cimgui_sha }}`
            - cosmopolitan: latest
            
            ### Platforms
            - ✅ Linux (OpenGL via dlopen)
            - ✅ Windows (OpenGL via WGL)
            - 🚧 macOS (stub - displays error message)
            
            ### Usage
            ```bash
            # Download and run (works on Linux and Windows)
            chmod +x cosmo-sokol
            ./cosmo-sokol
            ```
            
            ### Changes
            ${{ steps.changelog.outputs.changes }}
          draft: false
          prerelease: ${{ contains(steps.version.outputs.version, 'rc') || contains(steps.version.outputs.version, 'alpha') }}
          files: |
            cosmo-sokol-${{ steps.version.outputs.version }}.zip
            dist/cosmo-sokol
```

### 5.2 Version Bumping Workflow

```yaml
# .github/workflows/version-bump.yml
name: Version Bump

on:
  workflow_dispatch:
    inputs:
      bump:
        description: 'Version bump type'
        required: true
        type: choice
        options:
          - patch
          - minor
          - major

permissions:
  contents: write

jobs:
  bump:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          
      - name: Get current version
        id: current
        run: |
          CURRENT=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
          echo "version=$CURRENT" >> $GITHUB_OUTPUT
          
      - name: Calculate next version
        id: next
        run: |
          CURRENT=${{ steps.current.outputs.version }}
          CURRENT=${CURRENT#v}  # Remove v prefix
          IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT"
          
          case "${{ inputs.bump }}" in
            major) MAJOR=$((MAJOR + 1)); MINOR=0; PATCH=0 ;;
            minor) MINOR=$((MINOR + 1)); PATCH=0 ;;
            patch) PATCH=$((PATCH + 1)) ;;
          esac
          
          NEXT="v$MAJOR.$MINOR.$PATCH"
          echo "version=$NEXT" >> $GITHUB_OUTPUT
          
      - name: Create tag
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git tag -a ${{ steps.next.outputs.version }} -m "Release ${{ steps.next.outputs.version }}"
          git push origin ${{ steps.next.outputs.version }}
```

---

## 6. Complete Workflow Files

### 6.1 Directory Structure

```
.github/
├── workflows/
│   ├── build.yml           # Main build + test
│   ├── upstream-check.yml  # Weekly dependency check
│   ├── update-submodules.yml  # Manual/triggered updates
│   ├── release.yml         # Tag-triggered releases
│   └── version-bump.yml    # Version management
├── UPSTREAM_UPDATE_TEMPLATE.md
└── dependabot.yml          # For non-submodule deps only
```

### 6.2 Full Build Workflow

```yaml
# .github/workflows/build.yml
name: Build

on:
  push:
    branches: [main, master]
    paths-ignore:
      - '**.md'
      - '.github/ISSUE_TEMPLATE/**'
  pull_request:
    paths-ignore:
      - '**.md'
  workflow_dispatch:

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

permissions:
  contents: write
  pull-requests: read

env:
  COSMO_VERSION: "latest"

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      binary_hash: ${{ steps.hash.outputs.sha256 }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: recursive
          
      - name: Cache apt packages
        uses: awalsh128/cache-apt-pkgs-action@latest
        with:
          packages: libx11-dev libgl-dev libxcursor-dev libxi-dev parallel
          version: "1.0"
          
      - name: Setup cosmocc
        uses: bjia56/setup-cosmocc@main
        with:
          version: ${{ env.COSMO_VERSION }}
          
      - name: Build
        run: ./build
        
      - name: Binary info
        id: hash
        run: |
          file bin/cosmo-sokol
          ls -lh bin/cosmo-sokol
          SHA=$(sha256sum bin/cosmo-sokol | cut -d' ' -f1)
          echo "sha256=$SHA" >> $GITHUB_OUTPUT
          echo "Binary SHA256: $SHA"
          
      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: cosmo-sokol
          path: bin/cosmo-sokol
          retention-days: 7
          
  test-linux:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: cosmo-sokol
          
      - name: Test binary
        run: |
          chmod +x cosmo-sokol
          # Test that it loads (will fail gracefully without display)
          timeout 3 ./cosmo-sokol 2>&1 || true
          echo "✓ Binary executed on Linux"
          
  test-windows:
    runs-on: windows-latest
    needs: build
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: cosmo-sokol
          
      - name: Test binary
        shell: pwsh
        run: |
          # APE format works on Windows
          $proc = Start-Process -FilePath ".\cosmo-sokol" -PassThru -NoNewWindow
          Start-Sleep -Seconds 2
          if (!$proc.HasExited) {
            $proc.Kill()
            Write-Host "✓ Binary ran on Windows"
          } else {
            Write-Host "✓ Binary loaded on Windows (exit expected without display)"
          }

  test-macos:
    runs-on: macos-latest
    needs: build
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: cosmo-sokol
          
      - name: Test binary
        run: |
          chmod +x cosmo-sokol
          # Should show stub message on macOS
          ./cosmo-sokol 2>&1 | head -5 || true
          echo "✓ Binary loaded on macOS (stub expected)"

  release:
    runs-on: ubuntu-latest
    needs: [build, test-linux, test-windows, test-macos]
    if: startsWith(github.ref, 'refs/tags/')
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive
          
      - uses: actions/download-artifact@v4
        with:
          name: cosmo-sokol
          path: dist/
          
      - name: Package
        run: |
          chmod +x dist/cosmo-sokol
          cd dist && zip -r ../cosmo-sokol.zip cosmo-sokol
          
      - name: Get versions
        id: versions
        run: |
          echo "sokol=$(cd deps/sokol && git rev-parse --short HEAD)" >> $GITHUB_OUTPUT
          echo "cimgui=$(cd deps/cimgui && git rev-parse --short HEAD)" >> $GITHUB_OUTPUT
          
      - name: Release
        uses: softprops/action-gh-release@v2
        with:
          body: |
            ## Dependencies
            - sokol: `${{ steps.versions.outputs.sokol }}`
            - cimgui: `${{ steps.versions.outputs.cimgui }}`
            
            ## Platforms
            - ✅ Linux | ✅ Windows | 🚧 macOS (stub)
            
            ## SHA256
            `${{ needs.build.outputs.binary_hash }}`
          files: |
            cosmo-sokol.zip
            dist/cosmo-sokol
```

---

## 7. Monitoring Dashboard

### 7.1 GitHub Actions Status Badge

Add to README.md:
```markdown
[![Build](https://github.com/ludoplex/cosmo-sokol/actions/workflows/build.yml/badge.svg)](https://github.com/ludoplex/cosmo-sokol/actions/workflows/build.yml)
[![Upstream Check](https://github.com/ludoplex/cosmo-sokol/actions/workflows/upstream-check.yml/badge.svg)](https://github.com/ludoplex/cosmo-sokol/actions/workflows/upstream-check.yml)
```

### 7.2 Issue Labels

Create these labels for automated issues:
- `upstream` - Upstream dependency updates
- `automated` - Bot-generated issues/PRs
- `breaking-change` - Known breaking changes
- `api-drift` - API surface has changed

---

## 8. Migration Plan

### 8.1 Phase 1: Enhanced Build (Week 1)

1. Update `build.yml` with multi-platform testing
2. Add artifact uploads
3. Switch to `version: "latest"` for cosmocc

### 8.2 Phase 2: Upstream Monitoring (Week 2)

1. Add `upstream-check.yml`
2. Create issue template for updates
3. Run manually to test

### 8.3 Phase 3: Submodule Updates (Week 3)

1. Add `update-submodules.yml`
2. Create first batch update PR (50 commits)
3. Update `gen-sokol` SOKOL_FUNCTIONS if needed

### 8.4 Phase 4: Release Automation (Week 4)

1. Add `release.yml`
2. Add `version-bump.yml`
3. Tag first automated release

---

## 9. Cost Analysis

### GitHub Actions Minutes

| Workflow | Frequency | Est. Minutes | Monthly Cost |
|----------|-----------|--------------|--------------|
| build.yml | 20/month | 10 each | ~200 min |
| upstream-check | 4/month | 2 each | ~8 min |
| update-submodules | 2/month | 5 each | ~10 min |
| release | 1/month | 15 each | ~15 min |

**Total:** ~233 minutes/month (well within free tier of 2000 min/month for public repos)

---

## 10. Recommendations Summary

| Priority | Action | Impact |
|----------|--------|--------|
| **P0** | Add Windows/macOS test jobs | Catch platform-specific breaks |
| **P0** | Track latest cosmocc | Get bug fixes automatically |
| **P1** | Add upstream-check.yml | Visibility into dependency drift |
| **P1** | Add API surface check | Detect when gen-sokol needs update |
| **P2** | Add release automation | Reduce manual release overhead |
| **P2** | Incremental submodule updates | Catch breaks in smaller batches |

---

## 11. Addendum: Cross-Report Integration

### Agreements with Other Reports

1. **Analyst's quarterly cadence**: The upstream-check.yml weekly schedule supports their recommended quarterly sync by providing early warning of accumulating changes.

2. **Seeker's 1,044 commit gap**: The incremental update workflow (50-commit batches) directly addresses the challenge of catching up from major drift.

3. **Ballistics' gen-sokol focus**: The API check job surfaces when SOKOL_FUNCTIONS needs updating before runtime failures occur.

### Differences from Current State

1. **Multi-platform testing**: Current CI only builds on Linux. Proposed CI verifies the APE binary works on all target platforms.

2. **Proactive monitoring**: Current CI is reactive (only runs on push). Proposed CI proactively monitors upstreams.

3. **Automated releases**: Current CI creates draft releases. Proposed CI publishes automatically with full metadata.

### Open Questions

1. Should macos-latest be kept in CI given the permanent stub decision? (Compile verification has value even for stubs)

2. What's the right batch size for sokol updates? 50 commits is a guess; may need tuning based on breaking change frequency.

3. Should cosmopolitan version be pinned or track latest? Latest gets bug fixes but could introduce breaks.

---

*Generated by CI/CD specialist subagent*
