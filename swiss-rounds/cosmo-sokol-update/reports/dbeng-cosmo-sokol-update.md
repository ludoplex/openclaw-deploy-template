# cosmo-sokol Version Tracking System Design

**Agent:** dbeng  
**Date:** 2026-02-09  
**Task:** Dependency & Version Management for ludoplex/cosmo-sokol

---

## 1. Current State Analysis

### How Versions Are Currently Tracked

| Dependency | Tracking Method | Location |
|------------|----------------|----------|
| **sokol** | Git submodule | `deps/sokol` → floooh/sokol |
| **cimgui** | Git submodule | `deps/cimgui` → cimgui/cimgui |
| **cosmopolitan** | External toolchain (PATH) | User-managed, ≥v3.9.5 required |

**Problems with current approach:**
- No explicit version pinning beyond submodule commit SHAs
- Cosmopolitan version requirement buried in README, not machine-readable
- No tracking of known-working version combinations
- No record of API changes handled in shims
- No rollback mechanism beyond git history archaeology

---

## 2. Version Schema Design

### Proposed: `versions.json`

```json
{
  "$schema": "./versions.schema.json",
  "schemaVersion": "1.0.0",
  "lastUpdated": "2026-02-09T19:54:00Z",
  "current": {
    "sokol": {
      "commit": "d48aa2ff673af2d6b981032dd43766ab15689163",
      "date": "2026-02-08",
      "upstream": "floooh/sokol"
    },
    "cimgui": {
      "commit": "c56d1668b1ffd156609805c62a562bceec65d61a",
      "date": "2026-02-09",
      "upstream": "cimgui/cimgui",
      "imgui_version": "1.91.x"
    },
    "cosmopolitan": {
      "minVersion": "3.9.5",
      "testedVersion": "4.0.2",
      "upstream": "jart/cosmopolitan"
    }
  },
  "shimStatus": {
    "sokol_app": {
      "functions_shimmed": 87,
      "last_audit": "2026-02-01"
    },
    "sokol_gfx": {
      "functions_shimmed": 142,
      "last_audit": "2026-02-01"
    }
  }
}
```

### What to Track

| Field | Purpose | Update Trigger |
|-------|---------|----------------|
| `sokol.commit` | Exact upstream commit | Submodule update |
| `sokol.date` | Human-readable age | Derived from commit |
| `cimgui.commit` | cimgui binding version | Submodule update |
| `cimgui.imgui_version` | Underlying Dear ImGui | Read from cimgui's embedded imgui |
| `cosmopolitan.minVersion` | Minimum required | Breaking changes upstream |
| `cosmopolitan.testedVersion` | CI-verified version | After successful CI build |
| `shimStatus.*` | Shim layer health | After gen-sokol runs |

---

## 3. Compatibility Matrix

### Proposed: `compatibility.json`

```json
{
  "knownGood": [
    {
      "id": "2026-02-baseline",
      "sokol": "d48aa2ff673af2d6b981032dd43766ab15689163",
      "cimgui": "c56d1668b1ffd156609805c62a562bceec65d61a",
      "cosmopolitan": ">=4.0.2",
      "platforms": {
        "linux": "full",
        "windows": "full",
        "macos": "stub"
      },
      "ciPassed": true,
      "notes": "Current stable baseline"
    }
  ],
  "knownBad": [
    {
      "sokol": "abc123...",
      "cosmopolitan": "<3.9.5",
      "reason": "Missing Win32 functions in cosmo libc",
      "issue": "https://github.com/ludoplex/cosmo-sokol/issues/X"
    }
  ],
  "breakingChanges": {
    "sokol": {
      "2024-11-04": {
        "change": "sg_pass renamed fields",
        "shimImpact": "sokol_cosmo.c updated",
        "minCommit": "xxx"
      }
    },
    "cosmopolitan": {
      "3.9.5": {
        "change": "Added required Win32 functions",
        "shimImpact": "Windows backend enabled"
      }
    }
  }
}
```

### Compatibility Decision Matrix

```
┌─────────────────────────────────────────────────────────────────┐
│                    sokol HEAD                                    │
├─────────────┬───────────┬───────────────────────────────────────┤
│ cosmo ≥4.0  │ ✅ SAFE   │ Automatic update possible             │
├─────────────┼───────────┼───────────────────────────────────────┤
│ cosmo 3.9.x │ ⚠️  CHECK │ May need Win32 function additions     │
├─────────────┼───────────┼───────────────────────────────────────┤
│ cosmo <3.9  │ ❌ FAIL   │ Missing essential Win32 support       │
└─────────────┴───────────┴───────────────────────────────────────┘
```

---

## 4. Migration Tracking

### API Change Tracking: `migrations.json`

```json
{
  "migrations": [
    {
      "id": "2026-01-sokol-vulkan-labels",
      "upstream": "floooh/sokol#1422",
      "date": "2026-01-24",
      "type": "new_feature",
      "affectsShim": false,
      "description": "VK_EXT_debug_utils for object labels",
      "action": "none_required",
      "handled": true
    },
    {
      "id": "2026-01-sokol-dual-blend",
      "upstream": "floooh/sokol#1426",
      "date": "2026-01-26",
      "type": "new_api",
      "affectsShim": true,
      "shimFile": "shims/sokol/gen-sokol",
      "newFunctions": ["sg_query_features"],
      "action": "regenerate_shims",
      "handled": true
    }
  ],
  "pendingReview": []
}
```

### Automated Detection Script

```bash
#!/bin/bash
# scripts/check-upstream-changes.sh

SOKOL_CURRENT=$(git -C deps/sokol rev-parse HEAD)
SOKOL_LATEST=$(git ls-remote https://github.com/floooh/sokol HEAD | cut -f1)

if [ "$SOKOL_CURRENT" != "$SOKOL_LATEST" ]; then
    echo "sokol: $SOKOL_CURRENT → $SOKOL_LATEST"
    git -C deps/sokol log --oneline $SOKOL_CURRENT..$SOKOL_LATEST
    
    # Check for API changes in headers
    git -C deps/sokol diff $SOKOL_CURRENT..$SOKOL_LATEST -- \
        sokol_app.h sokol_gfx.h | grep -E '^[\+\-].*\bSAPP_|SG_' 
fi
```

---

## 5. Rollback Strategy

### Git Tag Convention

```
cosmo-sokol-v{MAJOR}.{MINOR}.{PATCH}
  │
  └── Example: cosmo-sokol-v1.2.0
      ├── sokol@{commit}
      ├── cimgui@{commit}  
      └── tested with cosmopolitan v4.0.2
```

### Rollback Procedure

```bash
#!/bin/bash
# scripts/rollback.sh <tag-or-id>

TARGET=${1:-$(jq -r '.knownGood[0].id' compatibility.json)}

# 1. Find the known-good configuration
CONFIG=$(jq -r ".knownGood[] | select(.id==\"$TARGET\")" compatibility.json)

SOKOL_COMMIT=$(echo $CONFIG | jq -r '.sokol')
CIMGUI_COMMIT=$(echo $CONFIG | jq -r '.cimgui')

# 2. Reset submodules
git -C deps/sokol checkout $SOKOL_COMMIT
git -C deps/cimgui checkout $CIMGUI_COMMIT

# 3. Regenerate shims
./shims/sokol/gen-sokol

# 4. Verify build
./build && echo "Rollback successful to $TARGET"
```

### Snapshot Before Update

```bash
# scripts/snapshot-versions.sh
DATE=$(date +%Y-%m-%d)
SNAPSHOT_ID="${DATE}-pre-update"

jq --arg id "$SNAPSHOT_ID" \
   --arg sokol "$(git -C deps/sokol rev-parse HEAD)" \
   --arg cimgui "$(git -C deps/cimgui rev-parse HEAD)" \
   '.knownGood += [{
     "id": $id,
     "sokol": $sokol,
     "cimgui": $cimgui,
     "cosmopolitan": ">=4.0.2",
     "ciPassed": true,
     "notes": "Snapshot before update"
   }]' compatibility.json > tmp.json && mv tmp.json compatibility.json
```

---

## 6. Implementation Recommendation

### File Structure

```
cosmo-sokol/
├── versions.json           # Current pinned versions
├── compatibility.json      # Known-good/bad combinations
├── migrations.json         # API change tracking
├── scripts/
│   ├── check-upstream.sh   # Detect new upstream commits
│   ├── update-deps.sh      # Coordinated update workflow
│   ├── rollback.sh         # Revert to known-good
│   └── snapshot.sh         # Save current state
└── .github/workflows/
    └── update-check.yml    # Weekly upstream check
```

### GitHub Actions Integration

```yaml
# .github/workflows/update-check.yml
name: Check Upstream Updates

on:
  schedule:
    - cron: '0 6 * * 1'  # Weekly Monday 6 AM UTC
  workflow_dispatch:

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: true
      
      - name: Check for updates
        run: ./scripts/check-upstream.sh > upstream-status.txt
      
      - name: Create issue if updates available
        if: ${{ hashFiles('upstream-status.txt') != '' }}
        uses: peter-evans/create-issue-from-file@v4
        with:
          title: 'Upstream updates available'
          content-filepath: ./upstream-status.txt
          labels: dependencies, automated
```

---

## 7. Summary

| Component | Solution |
|-----------|----------|
| **Version tracking** | `versions.json` with commit SHAs + dates |
| **Compatibility** | `compatibility.json` with known-good/bad sets |
| **Migration tracking** | `migrations.json` + automated diff analysis |
| **Rollback** | Git tags + `rollback.sh` script |
| **Automation** | Weekly GitHub Actions check + issue creation |

### Key Benefits

1. **Machine-readable** — CI can validate versions
2. **Auditable** — Clear history of what works
3. **Recoverable** — One command rollback
4. **Proactive** — Automated upstream monitoring

### Next Steps (for other agents)

- [ ] Implement `check-upstream.sh` script
- [ ] Create GitHub Actions workflow for automated checks
- [ ] Define shim function list for `gen-sokol` audit
- [ ] Test rollback procedure on existing repo
