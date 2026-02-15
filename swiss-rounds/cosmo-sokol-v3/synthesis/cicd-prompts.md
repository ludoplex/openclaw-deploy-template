# Stage Prompts: cicd

**Specialist:** cicd  
**Total Stages:** 1

---

## Stage 1: upstream-sync.yml Implementation

### Prompt

```
You are the cicd specialist implementing .github/workflows/upstream-sync.yml for the cosmo-sokol project.

CONTEXT:
- cosmo-sokol tracks the floooh/sokol upstream via git submodule
- The submodule can drift significantly (currently 1,032 commits behind)
- Maintainers need automated detection and PR creation for syncs
- Breaking changes require human review before merge

TASK:
Create an automated upstream sync workflow that:
1. Runs weekly (Monday 6 AM UTC) and on manual trigger
2. Checks drift against upstream sokol master
3. Scans CHANGELOG for breaking changes
4. Creates a PR if drift exceeds threshold (50 commits)
5. Marks PR as draft if breaking changes detected

CRITICAL FIXES:

1. **Numeric Comparison** (not string!):
```yaml
# WRONG:
if: needs.check-drift.outputs.drift_count > '50'

# CORRECT:
if: ${{ fromJSON(needs.check-drift.outputs.drift_count) > 50 }}
```

2. **Deduplication** (prevent multiple PRs):
```yaml
- name: Check for existing sync PR
  id: existing
  run: |
    EXISTING=$(gh pr list --state open --head "sync/" --json number -q 'length')
    echo "count=$EXISTING" >> $GITHUB_OUTPUT
  env:
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

- name: Create sync PR
  if: steps.existing.outputs.count == '0'
  # ...
```

WORKFLOW STRUCTURE:
```yaml
name: Upstream Sync Check

on:
  schedule:
    - cron: '0 6 * * 1'  # Weekly Monday 6 AM UTC
  workflow_dispatch:
    inputs:
      force_check:
        description: 'Force check regardless of drift'
        type: boolean
        default: false

jobs:
  check-drift:
    runs-on: ubuntu-latest
    outputs:
      drift_count: ${{ steps.drift.outputs.count }}
      drift_status: ${{ steps.drift.outputs.status }}
      has_breaking: ${{ steps.changelog.outputs.breaking }}
      last_sync: ${{ steps.drift.outputs.last_sync }}
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
        with:
          submodules: recursive
          fetch-depth: 0
      
      - name: Build tools
        run: make -C tools changelog-scan || echo "Tool not yet available"
      
      - name: Check drift
        id: drift
        run: |
          cd deps/sokol
          git fetch origin master
          
          BEHIND=$(git rev-list --count HEAD..origin/master)
          LAST_SYNC=$(git log -1 --format=%Y-%m-%d HEAD)
          CURRENT=$(git rev-parse --short HEAD)
          UPSTREAM=$(git rev-parse --short origin/master)
          
          echo "count=$BEHIND" >> $GITHUB_OUTPUT
          echo "last_sync=$LAST_SYNC" >> $GITHUB_OUTPUT
          echo "current=$CURRENT" >> $GITHUB_OUTPUT
          echo "upstream=$UPSTREAM" >> $GITHUB_OUTPUT
          
          if [ "$BEHIND" -gt 500 ]; then
            echo "status=significant" >> $GITHUB_OUTPUT
          elif [ "$BEHIND" -gt 50 ]; then
            echo "status=moderate" >> $GITHUB_OUTPUT
          else
            echo "status=minimal" >> $GITHUB_OUTPUT
          fi
          
          echo "📊 Drift: $BEHIND commits behind ($CURRENT → $UPSTREAM)"
      
      - name: Scan changelog
        id: changelog
        run: |
          if [ -f tools/changelog-scan ]; then
            ./tools/changelog-scan --since "${{ steps.drift.outputs.last_sync }}" \
              deps/sokol/CHANGELOG.md > changes.txt 2>&1 || true
          else
            # Fallback grep for BREAKING
            grep -i "breaking" deps/sokol/CHANGELOG.md > changes.txt 2>&1 || true
          fi
          
          if grep -qi "breaking" changes.txt; then
            echo "breaking=true" >> $GITHUB_OUTPUT
            echo "⚠️ Breaking changes detected!"
          else
            echo "breaking=false" >> $GITHUB_OUTPUT
            echo "✅ No breaking changes detected"
          fi
          
          cat changes.txt

  create-pr:
    needs: check-drift
    if: ${{ fromJSON(needs.check-drift.outputs.drift_count) > 50 || github.event.inputs.force_check == 'true' }}
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
        with:
          submodules: recursive
          fetch-depth: 0
      
      - name: Check for existing sync PR
        id: existing
        run: |
          EXISTING=$(gh pr list --state open --head "sync/" --json number -q 'length')
          echo "count=$EXISTING" >> $GITHUB_OUTPUT
          
          if [ "$EXISTING" -gt 0 ]; then
            echo "⚠️ Existing sync PR found, skipping creation"
          fi
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Update submodule
        if: steps.existing.outputs.count == '0'
        run: |
          cd deps/sokol
          git checkout origin/master
          cd ../..
          git add deps/sokol
      
      - name: Create sync PR
        if: steps.existing.outputs.count == '0'
        uses: peter-evans/create-pull-request@5e914681df9dc83aa4e4905692ca88beb2f9e91f
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          branch: sync/sokol-${{ github.run_number }}
          title: "sync: update sokol (${{ needs.check-drift.outputs.drift_count }} commits)"
          body: |
            ## 🔄 Automated Sync PR
            
            | Metric | Value |
            |--------|-------|
            | Commits behind | **${{ needs.check-drift.outputs.drift_count }}** |
            | Status | ${{ needs.check-drift.outputs.drift_status == 'significant' && '🔴 Significant' || '🟡 Moderate' }} |
            | Breaking changes | ${{ needs.check-drift.outputs.has_breaking == 'true' && '⚠️ YES' || '✅ None' }} |
            | Last sync | ${{ needs.check-drift.outputs.last_sync }} |
            
            ### Pre-merge checklist
            
            - [ ] Review CHANGELOG for breaking changes
            - [ ] Run `./tools/check-api-sync` locally
            - [ ] Update gen-sokol.h if API changed
            - [ ] Run full build and smoke tests
            - [ ] Update SYNC.md with notes
            
            ### Commands
            
            ```bash
            # Checkout this PR
            gh pr checkout ${{ github.run_number }}
            
            # Check API sync
            ./tools/check-api-sync
            
            # Review changes
            ./tools/changelog-scan --since ${{ needs.check-drift.outputs.last_sync }} deps/sokol/CHANGELOG.md
            ```
            
            ---
            *Created by upstream-sync workflow*
          labels: |
            sync
            automated
          draft: ${{ needs.check-drift.outputs.has_breaking == 'true' }}
```

SHA-PINNED ACTIONS:
- actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 (v4.2.2)
- peter-evans/create-pull-request@5e914681df9dc83aa4e4905692ca88beb2f9e91f (v7.0.5)

Provide the complete workflow YAML file.
```

---

## Verification Commands

After implementation:

```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('.github/workflows/upstream-sync.yml'))"

# Test manually via workflow_dispatch
gh workflow run upstream-sync.yml --field force_check=true

# Check workflow runs
gh run list --workflow=upstream-sync.yml
```

---

*cicd Stage Prompts Complete*
