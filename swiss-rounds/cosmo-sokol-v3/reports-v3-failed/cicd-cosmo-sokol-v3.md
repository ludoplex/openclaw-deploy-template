# CI/CD Analysis: cosmo-sokol Fork Automation

**Specialist:** cicd  
**Round:** 1  
**Project:** cosmo-sokol-v3  
**Date:** 2026-02-09

## Executive Summary

The ludoplex/cosmo-sokol fork needs automated synchronization with two upstream sources:
1. **bullno1/cosmo-sokol** — The original project this is forked from
2. **floooh/sokol** — The sokol library (git submodule in `deps/sokol`)

Additionally, the cosmopolitan toolchain (cosmocc) version is hardcoded and should track upstream releases.

## Current State Analysis

### Repository Structure
```
ludoplex/cosmo-sokol (fork)
├── origin: github.com/ludoplex/cosmo-sokol
├── upstream: github.com/bullno1/cosmo-sokol
└── deps/sokol (submodule) → github.com/floooh/sokol
```

### Version Gaps Identified

| Component | Current | Latest | Gap |
|-----------|---------|--------|-----|
| bullno1/cosmo-sokol | `5656716` | `5656716` | ✅ Synced (fork ahead by 2 commits) |
| floooh/sokol | `eaa1ca79` | `d48aa2ff` | ⚠️ Behind ~279 commits |
| cosmocc | `3.9.6` | `4.0.2` | ⚠️ Major version behind |

### Current CI/CD
- Single workflow: `.github/workflows/build.yml`
- Builds on push, releases on tags
- Hardcoded cosmocc version `3.9.6`
- No automated sync mechanism

## Proposed Workflows

### 1. Upstream Sync Workflow (`sync-upstream.yml`)

Automatically syncs changes from `bullno1/cosmo-sokol` without losing fork-specific changes.

**Strategy:** Fetch upstream, attempt merge, create PR if conflicts or changes detected.

```yaml
name: Sync Upstream (bullno1/cosmo-sokol)
run-name: "Sync from bullno1/cosmo-sokol"

on:
  schedule:
    - cron: '0 6 * * 1'  # Weekly on Monday 6 AM UTC
  workflow_dispatch:
    inputs:
      force:
        description: 'Force sync even if no changes'
        required: false
        default: 'false'
        type: boolean

permissions:
  contents: write
  pull-requests: write

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout fork
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Configure git
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"

      - name: Add upstream remote
        run: |
          git remote add upstream https://github.com/bullno1/cosmo-sokol.git || true
          git fetch upstream

      - name: Check for upstream changes
        id: check
        run: |
          UPSTREAM_SHA=$(git rev-parse upstream/master)
          MERGE_BASE=$(git merge-base HEAD upstream/master)
          
          if [ "$UPSTREAM_SHA" = "$MERGE_BASE" ]; then
            echo "up-to-date=true" >> $GITHUB_OUTPUT
            echo "No new upstream commits"
          else
            echo "up-to-date=false" >> $GITHUB_OUTPUT
            echo "New upstream commits detected"
            git log --oneline $MERGE_BASE..upstream/master
          fi

      - name: Attempt merge
        id: merge
        if: steps.check.outputs.up-to-date == 'false' || github.event.inputs.force == 'true'
        run: |
          BRANCH="sync/upstream-$(date +%Y%m%d)"
          git checkout -b "$BRANCH"
          
          if git merge upstream/master --no-edit; then
            echo "merge-clean=true" >> $GITHUB_OUTPUT
            echo "branch=$BRANCH" >> $GITHUB_OUTPUT
          else
            echo "merge-clean=false" >> $GITHUB_OUTPUT
            echo "branch=$BRANCH" >> $GITHUB_OUTPUT
            git merge --abort
          fi

      - name: Push branch
        if: steps.merge.outputs.branch != ''
        run: |
          git push origin ${{ steps.merge.outputs.branch }}

      - name: Create Pull Request
        if: steps.merge.outputs.branch != ''
        uses: peter-evans/create-pull-request@v6
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          branch: ${{ steps.merge.outputs.branch }}
          base: main
          title: "⬆️ Sync from bullno1/cosmo-sokol"
          body: |
            ## Upstream Sync
            
            This PR syncs changes from [bullno1/cosmo-sokol](https://github.com/bullno1/cosmo-sokol).
            
            **Merge Status:** ${{ steps.merge.outputs.merge-clean == 'true' && '✅ Clean merge' || '⚠️ Conflicts detected - manual resolution required' }}
            
            ### Changes from upstream
            ```
            $(git log --oneline $(git merge-base HEAD upstream/master)..upstream/master)
            ```
            
            ---
            *Automated by sync-upstream workflow*
          labels: |
            sync
            upstream
```

### 2. Sokol Submodule Update Workflow (`update-sokol.yml`)

Monitors floooh/sokol for new commits and creates PRs to update the submodule.

```yaml
name: Update Sokol Submodule
run-name: "Check for sokol updates"

on:
  schedule:
    - cron: '0 7 * * *'  # Daily at 7 AM UTC
  workflow_dispatch:
    inputs:
      target_ref:
        description: 'Specific sokol commit/tag to update to (leave empty for latest)'
        required: false
        default: ''
        type: string

permissions:
  contents: write
  pull-requests: write

jobs:
  check-update:
    runs-on: ubuntu-latest
    outputs:
      needs-update: ${{ steps.compare.outputs.needs-update }}
      current-sha: ${{ steps.compare.outputs.current-sha }}
      latest-sha: ${{ steps.compare.outputs.latest-sha }}
      commits-behind: ${{ steps.compare.outputs.commits-behind }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: recursive

      - name: Compare versions
        id: compare
        run: |
          cd deps/sokol
          CURRENT=$(git rev-parse HEAD)
          echo "current-sha=$CURRENT" >> $GITHUB_OUTPUT
          
          git fetch origin
          
          if [ -n "${{ github.event.inputs.target_ref }}" ]; then
            TARGET="${{ github.event.inputs.target_ref }}"
          else
            TARGET=$(git rev-parse origin/master)
          fi
          echo "latest-sha=$TARGET" >> $GITHUB_OUTPUT
          
          if [ "$CURRENT" = "$TARGET" ]; then
            echo "needs-update=false" >> $GITHUB_OUTPUT
            echo "commits-behind=0" >> $GITHUB_OUTPUT
          else
            BEHIND=$(git rev-list --count $CURRENT..$TARGET)
            echo "needs-update=true" >> $GITHUB_OUTPUT
            echo "commits-behind=$BEHIND" >> $GITHUB_OUTPUT
          fi

  update:
    needs: check-update
    if: needs.check-update.outputs.needs-update == 'true'
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: recursive
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Configure git
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"

      - name: Update submodule
        id: update
        run: |
          cd deps/sokol
          git fetch origin
          
          TARGET="${{ github.event.inputs.target_ref || 'origin/master' }}"
          git checkout $TARGET
          
          NEW_SHA=$(git rev-parse HEAD)
          SHORT_SHA=$(git rev-parse --short HEAD)
          
          cd ../..
          BRANCH="deps/sokol-${SHORT_SHA}"
          git checkout -b "$BRANCH"
          git add deps/sokol
          git commit -m "deps: update sokol to ${SHORT_SHA}
          
          Updating from ${{ needs.check-update.outputs.current-sha }} to ${NEW_SHA}
          (${{ needs.check-update.outputs.commits-behind }} commits)"
          
          echo "branch=$BRANCH" >> $GITHUB_OUTPUT
          echo "short-sha=$SHORT_SHA" >> $GITHUB_OUTPUT

      - name: Push and create PR
        run: |
          git push origin ${{ steps.update.outputs.branch }}

      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v6
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          branch: ${{ steps.update.outputs.branch }}
          base: main
          title: "⬆️ deps: update sokol to ${{ steps.update.outputs.short-sha }}"
          body: |
            ## Sokol Submodule Update
            
            Updates `deps/sokol` from [floooh/sokol](https://github.com/floooh/sokol).
            
            | | Commit |
            |---|--------|
            | **Previous** | `${{ needs.check-update.outputs.current-sha }}` |
            | **New** | `${{ needs.check-update.outputs.latest-sha }}` |
            | **Commits** | ${{ needs.check-update.outputs.commits-behind }} |
            
            ⚠️ **Review Required:**
            - Check if `gen-sokol` needs updates for new/changed API functions
            - Verify build completes successfully
            - Test on all platforms if possible
            
            ---
            *Automated by update-sokol workflow*
          labels: |
            dependencies
            sokol
```

### 3. Cosmocc Version Check Workflow (`check-cosmocc.yml`)

Monitors cosmopolitan releases and updates the build workflow.

```yaml
name: Check Cosmocc Version
run-name: "Check for cosmocc updates"

on:
  schedule:
    - cron: '0 8 * * 1'  # Weekly on Monday 8 AM UTC
  workflow_dispatch:

permissions:
  contents: write
  pull-requests: write

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Get current version
        id: current
        run: |
          VERSION=$(grep -oP 'version:\s*"\K[^"]+' .github/workflows/build.yml || echo "unknown")
          echo "version=$VERSION" >> $GITHUB_OUTPUT

      - name: Get latest release
        id: latest
        run: |
          LATEST=$(curl -s https://api.github.com/repos/jart/cosmopolitan/releases/latest | jq -r .tag_name)
          echo "version=$LATEST" >> $GITHUB_OUTPUT

      - name: Compare versions
        id: compare
        run: |
          CURRENT="${{ steps.current.outputs.version }}"
          LATEST="${{ steps.latest.outputs.version }}"
          
          if [ "$CURRENT" = "$LATEST" ]; then
            echo "needs-update=false" >> $GITHUB_OUTPUT
          else
            echo "needs-update=true" >> $GITHUB_OUTPUT
          fi

      - name: Update build.yml
        if: steps.compare.outputs.needs-update == 'true'
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          
          LATEST="${{ steps.latest.outputs.version }}"
          CURRENT="${{ steps.current.outputs.version }}"
          
          sed -i "s/version: \"$CURRENT\"/version: \"$LATEST\"/" .github/workflows/build.yml
          
          BRANCH="deps/cosmocc-${LATEST}"
          git checkout -b "$BRANCH"
          git add .github/workflows/build.yml
          git commit -m "ci: update cosmocc to ${LATEST}"
          git push origin "$BRANCH"

      - name: Create Pull Request
        if: steps.compare.outputs.needs-update == 'true'
        uses: peter-evans/create-pull-request@v6
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          branch: deps/cosmocc-${{ steps.latest.outputs.version }}
          base: main
          title: "⬆️ ci: update cosmocc to ${{ steps.latest.outputs.version }}"
          body: |
            ## Cosmocc Update
            
            Updates the cosmopolitan toolchain version in build workflow.
            
            | | Version |
            |---|---------|
            | **Previous** | `${{ steps.current.outputs.version }}` |
            | **New** | `${{ steps.latest.outputs.version }}` |
            
            ### Changelog
            See [cosmopolitan releases](https://github.com/jart/cosmopolitan/releases/tag/${{ steps.latest.outputs.version }})
            
            ⚠️ **Review Required:**
            - Check release notes for breaking changes
            - Verify build completes successfully
            
            ---
            *Automated by check-cosmocc workflow*
          labels: |
            dependencies
            cosmocc

```

### 4. Enhanced Build Workflow (Updated `build.yml`)

Improve the existing build workflow with caching and matrix builds:

```yaml
name: Build
run-name: Build

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]
  workflow_dispatch:

permissions:
  contents: write

env:
  COSMOCC_VERSION: "4.0.2"  # Single source of truth

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          submodules: recursive

      - name: Cache cosmocc
        uses: actions/cache@v4
        with:
          path: ~/.cosmocc
          key: cosmocc-${{ env.COSMOCC_VERSION }}

      - name: Install deps
        uses: awalsh128/cache-apt-pkgs-action@latest
        with:
          packages: libx11-dev libgl-dev libxcursor-dev libxi-dev
          version: "1.0"

      - name: Download cosmopolitan
        uses: bjia56/setup-cosmocc@main
        with:
          version: ${{ env.COSMOCC_VERSION }}

      - name: Build
        run: ./build

      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: cosmo-sokol-build
          path: bin/
          retention-days: 7

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

## Implementation Priority

| Priority | Workflow | Effort | Impact |
|----------|----------|--------|--------|
| 🔴 High | `update-sokol.yml` | Medium | Keeps core dependency fresh |
| 🟡 Medium | `check-cosmocc.yml` | Low | Ensures toolchain stays current |
| 🟡 Medium | `sync-upstream.yml` | Medium | Catches upstream improvements |
| 🟢 Low | Enhanced `build.yml` | Low | Better DX, caching |

## Repository Secrets Required

None required for basic operation. All workflows use `GITHUB_TOKEN` which is automatically provided.

For advanced use:
- `PAT_TOKEN` — If you need to trigger workflows from other workflows

## Recommended Schedule

| Workflow | Frequency | Rationale |
|----------|-----------|-----------|
| Sokol update | Daily | Active development, frequent commits |
| Cosmocc check | Weekly | Infrequent releases |
| Upstream sync | Weekly | Low activity in bullno1/cosmo-sokol |

## Risk Considerations

### Sokol Updates
- **Breaking changes:** Sokol occasionally changes API. The `gen-sokol` script may need updates.
- **Mitigation:** CI build will fail, alerting maintainer to review changes.

### Cosmocc Updates
- **Major version jumps:** 3.x → 4.x may have breaking changes.
- **Mitigation:** Review release notes in PR before merging.

### Upstream Sync
- **Merge conflicts:** Fork-specific changes (macOS support) may conflict.
- **Mitigation:** Workflow detects conflicts and creates PR for manual resolution.

## Files to Create

```
.github/workflows/
├── build.yml          # (update existing)
├── sync-upstream.yml  # NEW
├── update-sokol.yml   # NEW
└── check-cosmocc.yml  # NEW
```

## Next Steps

1. Create the three new workflow files
2. Update `build.yml` with environment variable for cosmocc version
3. Test workflows with `workflow_dispatch` trigger
4. Monitor first automated runs
5. Adjust schedules based on update frequency

## Questions for Triad Discussion

1. **Sync strategy for macOS work:** Should upstream sync preserve the macOS branch separately, or attempt to merge into main?

2. **Sokol update frequency:** Daily seems aggressive. Should we batch updates weekly or use a "stable tag" strategy?

3. **Cosmocc testing:** Should we test with both current and latest cosmocc versions before auto-upgrading?

---

*Report generated by CI/CD specialist for Swiss Rounds v3*
