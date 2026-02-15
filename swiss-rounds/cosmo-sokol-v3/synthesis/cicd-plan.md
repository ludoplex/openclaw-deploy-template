# Specialist Plan: cicd

**Specialist:** cicd  
**Domain:** CI/CD automation, upstream sync workflows  
**Priority:** #4 (Medium-High)  
**Dependencies:** neteng build.yml foundation  
**Estimated Effort:** 3 hours

---

## Mission

Implement the automated upstream sync workflow that detects new sokol releases and creates pull requests for review.

## Deliverables

| File | Priority | Description |
|------|----------|-------------|
| `.github/workflows/upstream-sync.yml` | P1 | Automated sync detection and PR creation |

## Technical Specifications

### upstream-sync.yml Architecture

```yaml
name: Upstream Sync Check

on:
  schedule:
    - cron: '0 6 * * 1'  # Weekly on Monday at 6 AM UTC
  workflow_dispatch:
    inputs:
      force_check:
        description: 'Force check even if no drift'
        type: boolean
        default: false

jobs:
  check-drift:
    runs-on: ubuntu-latest
    outputs:
      drift_count: ${{ steps.drift.outputs.count }}
      has_breaking: ${{ steps.changelog.outputs.breaking }}
    steps:
      - checkout with submodules
      - build drift-report tool
      - run drift check
      - run changelog scan

  create-pr:
    needs: check-drift
    if: needs.check-drift.outputs.drift_count > 50
    runs-on: ubuntu-latest
    steps:
      - checkout
      - update submodule
      - create PR with drift info
```

### Key Implementation Details

#### Numeric Comparison Fix (Critical)
```yaml
# WRONG: String comparison
if: needs.check-drift.outputs.drift_count > '50'

# CORRECT: Numeric comparison
if: ${{ fromJSON(needs.check-drift.outputs.drift_count) > 50 }}
```

#### Drift Detection Step
```yaml
- name: Check drift
  id: drift
  run: |
    cd deps/sokol
    git fetch origin master
    BEHIND=$(git rev-list --count HEAD..origin/master)
    echo "count=$BEHIND" >> $GITHUB_OUTPUT
    
    if [ "$BEHIND" -gt 500 ]; then
      echo "status=significant" >> $GITHUB_OUTPUT
    elif [ "$BEHIND" -gt 50 ]; then
      echo "status=moderate" >> $GITHUB_OUTPUT
    else
      echo "status=minimal" >> $GITHUB_OUTPUT
    fi
```

#### Changelog Scan Integration
```yaml
- name: Check for breaking changes
  id: changelog
  run: |
    # Get last sync date from submodule commit
    LAST_SYNC=$(git log -1 --format=%ci deps/sokol)
    
    # Run changelog scan
    ./tools/changelog-scan --since "$LAST_SYNC" deps/sokol/CHANGELOG.md > changes.txt 2>&1 || true
    
    if grep -q "BREAKING" changes.txt; then
      echo "breaking=true" >> $GITHUB_OUTPUT
    else
      echo "breaking=false" >> $GITHUB_OUTPUT
    fi
    
    cat changes.txt
```

#### PR Creation with Context
```yaml
- name: Create sync PR
  uses: peter-evans/create-pull-request@5e914681df9dc83aa4e4905692ca88beb2f9e91f  # v7.0.5
  with:
    token: ${{ secrets.GITHUB_TOKEN }}
    branch: sync/sokol-${{ github.run_number }}
    title: "sync: update sokol submodule (${{ needs.check-drift.outputs.drift_count }} commits)"
    body: |
      ## Automated Sync PR
      
      **Drift detected:** ${{ needs.check-drift.outputs.drift_count }} commits behind upstream
      
      **Status:** ${{ needs.check-drift.outputs.drift_count > 500 && '🔴 Significant' || '🟡 Moderate' }}
      
      **Breaking changes:** ${{ needs.check-drift.outputs.has_breaking == 'true' && '⚠️ YES - Review required' || '✅ None detected' }}
      
      ### Pre-merge checklist
      - [ ] Review breaking changes in CHANGELOG
      - [ ] Update gen-sokol.h if needed
      - [ ] Run full test suite locally
      - [ ] Update SYNC.md with sync notes
      
      ---
      *This PR was automatically created by the upstream-sync workflow.*
    labels: |
      sync
      automated
    draft: ${{ needs.check-drift.outputs.has_breaking == 'true' }}
```

## Success Criteria

- [ ] Workflow runs on schedule (weekly Monday)
- [ ] Manual trigger works via workflow_dispatch
- [ ] Drift count is correctly calculated
- [ ] Numeric comparison works (>50 threshold)
- [ ] Breaking changes are detected from changelog
- [ ] PR is created with correct title and body
- [ ] PR is marked as draft if breaking changes found
- [ ] No duplicate PRs are created

## File Location

```
C:\cosmo-sokol\
└── .github\
    └── workflows\
        └── upstream-sync.yml    # REPLACE
```

## Dependencies

- **Requires:** drift-report and changelog-scan tools (seeker)
- **Requires:** Build workflow structure (neteng)
- **Provides:** Automated sync notifications and PRs

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| String comparison bug | Use fromJSON() for numeric |
| Too many PRs | Check for existing sync/ branch |
| Changelog parse fails | Wrap in `|| true`, check output |
| Token permissions | Document GITHUB_TOKEN needs |

## Deduplication Logic

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
  # ... create PR
```

---

*cicd Plan Complete*
