# DBEng Report: cosmo-sokol-v3 — Round 1

**Domain:** Data structures and schemas (version tracking, compatibility matrices, build metadata)  
**Agent:** dbeng  
**Date:** 2026-02-09  
**Goal:** Keep ludoplex/cosmo-sokol fork updated with upstream (floooh/sokol, bullno1/cosmo-sokol) without manual version pinning

---

## Executive Summary

The ludoplex/cosmo-sokol fork is **1,032 commits behind** floooh/sokol upstream. A major breaking change occurred in November 2024 ("bindings cleanup update") requiring significant migration. I propose structured schemas for automated version tracking, compatibility assessment, and build metadata to enable automated upstream synchronization.

---

## 1. Current State Analysis

### 1.1 Repository Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                    UPSTREAM HIERARCHY                        │
├─────────────────────────────────────────────────────────────┤
│  floooh/sokol (master)                                      │
│      │ d48aa2f - "Merge pull request #1438"                 │
│      │                                                       │
│      │ ▲ 1,032 commits                                      │
│      │                                                       │
│  ludoplex/cosmo-sokol/deps/sokol (submodule)               │
│      │ eaa1ca7 - "Merge pull request #1159"                 │
│      │                                                       │
│  bullno1/cosmo-sokol (upstream remote)                     │
│      │ 5656716 - "Merge pull request #2"                    │
│      │                                                       │
│      │ ▲ 2 commits                                          │
│      │                                                       │
│  ludoplex/cosmo-sokol (origin)                             │
│      └ 028aafa - "Update README with macOS support..."      │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Current Pinned Versions

| Dependency | Current Commit | Describe Tag | Status |
|------------|----------------|--------------|--------|
| sokol | `eaa1ca79a4004750e58cb51e0100d27f23e3e1ff` | `gles2-951-geaa1ca7` | **1032 behind** |
| cimgui | `8ec6558ecc9476c681d5d8c9f69597962045c2e6` | `v1.65.4-662-g8ec6558` | TBD |

### 1.3 Critical Breaking Changes Detected

**November 7, 2024 — "Bindings Cleanup Update"**
- `sg_apply_uniforms()` shader stage parameter removed
- `sg_bindings` struct interior reorganized (no longer per-shader-stage)
- New reflection information in `sg_shader_desc`
- Requires sokol-shdc migration for `layout(binding=N)` annotations

---

## 2. Proposed Version Tracking Schema

### 2.1 `version-manifest.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "schemaVersion": { "const": "1.0.0" },
    "project": {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "repo": { "type": "string" },
        "branch": { "type": "string" }
      }
    },
    "upstreams": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "repo": { "type": "string" },
          "remote": { "type": "string" },
          "branch": { "type": "string" },
          "lastSync": { "type": "string", "format": "date-time" },
          "lastSyncCommit": { "type": "string" },
          "commitsAhead": { "type": "integer" },
          "commitsBehind": { "type": "integer" }
        }
      }
    },
    "submodules": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "path": { "type": "string" },
          "url": { "type": "string" },
          "pinnedCommit": { "type": "string" },
          "pinnedTag": { "type": "string" },
          "upstreamHead": { "type": "string" },
          "commitsBehind": { "type": "integer" },
          "breakingChanges": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "commit": { "type": "string" },
                "date": { "type": "string", "format": "date" },
                "description": { "type": "string" },
                "migrationGuide": { "type": "string" }
              }
            }
          }
        }
      }
    },
    "lastUpdated": { "type": "string", "format": "date-time" }
  }
}
```

### 2.2 Example Manifest for cosmo-sokol

```json
{
  "schemaVersion": "1.0.0",
  "project": {
    "name": "cosmo-sokol",
    "repo": "ludoplex/cosmo-sokol",
    "branch": "master"
  },
  "upstreams": [
    {
      "name": "bullno1-cosmo-sokol",
      "repo": "bullno1/cosmo-sokol",
      "remote": "upstream",
      "branch": "master",
      "lastSync": "2026-02-09T00:00:00Z",
      "lastSyncCommit": "5656716",
      "commitsAhead": 2,
      "commitsBehind": 0
    }
  ],
  "submodules": [
    {
      "name": "sokol",
      "path": "deps/sokol",
      "url": "https://github.com/floooh/sokol.git",
      "pinnedCommit": "eaa1ca79a4004750e58cb51e0100d27f23e3e1ff",
      "pinnedTag": "gles2-951-geaa1ca7",
      "upstreamHead": "d48aa2f",
      "commitsBehind": 1032,
      "breakingChanges": [
        {
          "commit": "1111xxx",
          "date": "2024-11-07",
          "description": "Bindings cleanup update - sg_bindings struct reorganized",
          "migrationGuide": "https://floooh.github.io/2024/11/04/sokol-fall-2024-update.html"
        }
      ]
    },
    {
      "name": "cimgui",
      "path": "deps/cimgui",
      "url": "https://github.com/cimgui/cimgui.git",
      "pinnedCommit": "8ec6558ecc9476c681d5d8c9f69597962045c2e6",
      "pinnedTag": "v1.65.4-662-g8ec6558",
      "upstreamHead": null,
      "commitsBehind": null,
      "breakingChanges": []
    }
  ],
  "lastUpdated": "2026-02-09T18:08:00Z"
}
```

---

## 3. Compatibility Matrix Schema

### 3.1 `compatibility-matrix.json`

Track which versions of sokol work with which cosmo-sokol shim versions:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "schemaVersion": { "const": "1.0.0" },
    "matrix": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "shimVersion": { "type": "string" },
          "shimCommit": { "type": "string" },
          "sokolRange": {
            "type": "object",
            "properties": {
              "minCommit": { "type": "string" },
              "maxCommit": { "type": "string" },
              "minDate": { "type": "string", "format": "date" },
              "maxDate": { "type": "string", "format": "date" }
            }
          },
          "cimguiRange": {
            "type": "object",
            "properties": {
              "minVersion": { "type": "string" },
              "maxVersion": { "type": "string" }
            }
          },
          "platforms": {
            "type": "object",
            "properties": {
              "windows": { "enum": ["full", "partial", "none"] },
              "linux": { "enum": ["full", "partial", "none"] },
              "macos": { "enum": ["full", "partial", "none"] }
            }
          },
          "cosmoVersion": { "type": "string" },
          "verified": { "type": "boolean" },
          "notes": { "type": "string" }
        }
      }
    }
  }
}
```

### 3.2 Current Compatibility Assessment

| Shim Component | Sokol API Used | Breaking Change Impact |
|----------------|----------------|----------------------|
| `sokol_windows.c` | `sg_setup`, `sg_commit`, etc. | Medium - bindings struct |
| `sokol_linux.c` | X11+GL integration | Medium - bindings struct |
| `sokol_macos.c` | Stub only | None |
| `sokol_shared.c` | Core state machine | High - may use `sg_apply_uniforms` |
| `sokol_cosmo.c` | Platform dispatch | Low - routing only |

---

## 4. Build Metadata Schema

### 4.1 `build-metadata.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "schemaVersion": { "const": "1.0.0" },
    "build": {
      "type": "object",
      "properties": {
        "timestamp": { "type": "string", "format": "date-time" },
        "commitHash": { "type": "string" },
        "branch": { "type": "string" },
        "dirty": { "type": "boolean" }
      }
    },
    "dependencies": {
      "type": "object",
      "properties": {
        "sokol": {
          "type": "object",
          "properties": {
            "commit": { "type": "string" },
            "describeTag": { "type": "string" }
          }
        },
        "cimgui": {
          "type": "object",
          "properties": {
            "commit": { "type": "string" },
            "describeTag": { "type": "string" }
          }
        }
      }
    },
    "toolchain": {
      "type": "object",
      "properties": {
        "cosmocc": { "type": "string" },
        "parallel": { "type": "string" }
      }
    },
    "platforms": {
      "type": "array",
      "items": {
        "enum": ["windows", "linux", "macos"]
      }
    },
    "artifacts": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "path": { "type": "string" },
          "sha256": { "type": "string" },
          "size": { "type": "integer" }
        }
      }
    }
  }
}
```

---

## 5. Automated Update Tracking System

### 5.1 Proposed Database Schema (SQLite)

```sql
-- Repositories being tracked
CREATE TABLE repositories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    url TEXT NOT NULL,
    type TEXT CHECK(type IN ('fork', 'upstream', 'submodule')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Commits observed
CREATE TABLE commits (
    id INTEGER PRIMARY KEY,
    repo_id INTEGER REFERENCES repositories(id),
    hash TEXT NOT NULL,
    short_hash TEXT NOT NULL,
    author TEXT,
    date TIMESTAMP,
    message TEXT,
    is_breaking BOOLEAN DEFAULT FALSE,
    breaking_category TEXT,
    UNIQUE(repo_id, hash)
);

-- Sync events
CREATE TABLE sync_events (
    id INTEGER PRIMARY KEY,
    source_repo_id INTEGER REFERENCES repositories(id),
    target_repo_id INTEGER REFERENCES repositories(id),
    from_commit TEXT,
    to_commit TEXT,
    commits_synced INTEGER,
    status TEXT CHECK(status IN ('pending', 'in_progress', 'success', 'failed', 'blocked')),
    blocked_by_breaking_change BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Breaking changes requiring migration
CREATE TABLE breaking_changes (
    id INTEGER PRIMARY KEY,
    commit_id INTEGER REFERENCES commits(id),
    title TEXT NOT NULL,
    description TEXT,
    migration_guide_url TEXT,
    severity TEXT CHECK(severity IN ('minor', 'moderate', 'major')),
    auto_migratable BOOLEAN DEFAULT FALSE,
    migration_script TEXT
);

-- Compatibility test results
CREATE TABLE compatibility_tests (
    id INTEGER PRIMARY KEY,
    sokol_commit TEXT NOT NULL,
    shim_commit TEXT NOT NULL,
    platform TEXT NOT NULL,
    test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    build_success BOOLEAN,
    tests_passed INTEGER,
    tests_failed INTEGER,
    notes TEXT
);

-- Version pins
CREATE TABLE version_pins (
    id INTEGER PRIMARY KEY,
    submodule_path TEXT NOT NULL,
    pinned_commit TEXT NOT NULL,
    pinned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    pinned_by TEXT,
    reason TEXT,
    UNIQUE(submodule_path, pinned_commit)
);
```

### 5.2 Version Check Script Data Flow

```
┌───────────────────────────────────────────────────────────────┐
│                    VERSION CHECK FLOW                          │
├───────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Fetch upstream refs                                        │
│     ┌─────────────┐                                            │
│     │ git fetch   │ floooh/sokol                               │
│     │ origin      │ bullno1/cosmo-sokol                        │
│     └─────────────┘                                            │
│            │                                                    │
│            ▼                                                    │
│  2. Compare commits                                            │
│     ┌─────────────────────────────────────────────┐           │
│     │ git rev-list HEAD..origin/master --count    │           │
│     │ git log --oneline HEAD..origin/master       │           │
│     └─────────────────────────────────────────────┘           │
│            │                                                    │
│            ▼                                                    │
│  3. Parse CHANGELOG.md for breaking changes                    │
│     ┌─────────────────────────────────────────────┐           │
│     │ grep -E "(breaking|BREAKING|removed|renamed)"│           │
│     │ between current and HEAD                     │           │
│     └─────────────────────────────────────────────┘           │
│            │                                                    │
│            ▼                                                    │
│  4. Update version-manifest.json                               │
│     ┌─────────────────────────────────────────────┐           │
│     │ {                                            │           │
│     │   "commitsBehind": 1032,                    │           │
│     │   "breakingChanges": [...]                  │           │
│     │ }                                            │           │
│     └─────────────────────────────────────────────┘           │
│            │                                                    │
│            ▼                                                    │
│  5. Emit notification if threshold exceeded                    │
│     ┌─────────────────────────────────────────────┐           │
│     │ if commitsBehind > 100 OR hasBreaking:      │           │
│     │   notify("Update available")                │           │
│     └─────────────────────────────────────────────┘           │
│                                                                 │
└───────────────────────────────────────────────────────────────┘
```

---

## 6. Recommendations

### 6.1 Immediate Actions

1. **Create `version-manifest.json`** in repository root with current state
2. **Add CHANGELOG parsing** to detect breaking changes between versions
3. **Document the November 2024 breaking change** with migration requirements

### 6.2 Automation Pipeline

1. **Weekly cron job** to update version-manifest.json
2. **GitHub Action** that checks upstream on PR and comments with version delta
3. **Pre-update compatibility script** that:
   - Identifies breaking changes in range
   - Maps breaking changes to affected shim files
   - Generates migration checklist

### 6.3 Migration Strategy for Current Gap

Given the 1032-commit gap with breaking changes, recommend:

1. **Incremental sync** — identify safe waypoints before/after breaking changes
2. **Two-phase migration**:
   - Phase 1: Update to commit before Nov 7, 2024 bindings change
   - Phase 2: Apply bindings migration, then update to HEAD

### 6.4 Shim Impact Analysis

Files requiring update for bindings change:

| File | Likely Changes |
|------|---------------|
| `shims/sokol/sokol_shared.c` | `sg_apply_uniforms` signature |
| `main.c` | `sg_bindings` struct usage |
| Any shader bindings | `layout(binding=N)` annotations |

---

## 7. Artifacts to Create

| Artifact | Purpose | Priority |
|----------|---------|----------|
| `version-manifest.json` | Track current vs upstream versions | High |
| `compatibility-matrix.json` | Document tested version combos | Medium |
| `scripts/check-upstream.sh` | Automated version delta check | High |
| `MIGRATION.md` | Document known breaking changes | High |
| `.github/workflows/version-check.yml` | CI integration | Medium |

---

## 8. Coordination Points

**For cosmo agent:** Shim layer modifications for API changes  
**For cicd agent:** GitHub Actions workflow for version checking  
**For asm agent:** Low-level platform shim compatibility  
**For testcov agent:** Compatibility test matrix execution

---

*Report generated by dbeng specialist — Round 1*
