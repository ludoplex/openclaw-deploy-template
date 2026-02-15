# Specialist Plan: dbeng

**Specialist:** dbeng  
**Domain:** Database/metadata engineering, version tracking  
**Priority:** #6 (Low - Parallel Safe)  
**Dependencies:** None (can run in parallel with Phase 1)  
**Estimated Effort:** 2 hours

---

## Mission

Implement the project metadata manifest that tracks versions, dependencies, and sync state for cosmo-sokol.

## Deliverables

| File | Priority | Description |
|------|----------|-------------|
| `cosmo-sokol.json` | P2 | Project metadata manifest |

## Technical Specifications

### cosmo-sokol.json

**Purpose:** Machine-readable project metadata for tooling and CI

**Schema:**
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "cosmo-sokol project manifest",
  "version": "1.0.0",
  "project": {
    "name": "string",
    "description": "string",
    "repository": "string",
    "license": "string"
  },
  "upstream": {
    "sokol": {
      "repository": "string",
      "branch": "string",
      "last_sync": "ISO date",
      "last_sync_commit": "string (SHA)"
    }
  },
  "build": {
    "cosmocc_versions": ["string array"],
    "minimum_cosmocc": "string",
    "platforms": ["string array"]
  },
  "tooling": {
    "tools": ["string array"],
    "workflows": ["string array"]
  },
  "sync": {
    "status": "current | drift | significant-drift",
    "drift_threshold_moderate": "number",
    "drift_threshold_significant": "number",
    "auto_sync_enabled": "boolean"
  }
}
```

**Example Implementation:**
```json
{
  "version": "1.0.0",
  "project": {
    "name": "cosmo-sokol",
    "description": "Cosmopolitan libc port of sokol graphics library",
    "repository": "https://github.com/ludoplex/cosmo-sokol",
    "license": "MIT",
    "maintainers": ["ludoplex"]
  },
  "upstream": {
    "sokol": {
      "repository": "https://github.com/floooh/sokol",
      "branch": "master",
      "last_sync": "2024-03-15",
      "last_sync_commit": "abc1234def5678"
    },
    "cimgui": {
      "repository": "https://github.com/cimgui/cimgui",
      "branch": "master",
      "last_sync": "2024-06-01",
      "last_sync_commit": "111aaaa222bbbb"
    }
  },
  "build": {
    "cosmocc_versions": ["3.9.5", "3.9.6"],
    "minimum_cosmocc": "3.9.5",
    "platforms": ["linux-x86_64", "windows-x86_64", "macos-x86_64", "macos-arm64"]
  },
  "tooling": {
    "tools": [
      "tools/check-api-sync",
      "tools/validate-sources",
      "tools/changelog-scan",
      "tools/drift-report"
    ],
    "workflows": [
      ".github/workflows/build.yml",
      ".github/workflows/upstream-sync.yml"
    ]
  },
  "sync": {
    "status": "drift",
    "drift_threshold_moderate": 50,
    "drift_threshold_significant": 500,
    "auto_sync_enabled": true,
    "sync_schedule": "weekly"
  },
  "api": {
    "sokol_app_functions": 61,
    "sokol_gfx_functions": 103,
    "gen_sokol_functions": 164
  }
}
```

### Usage in Tools

**drift-report.c:**
```c
// Read last sync info from manifest
static void read_manifest_sync_info(const char* path, SyncInfo* info) {
    // Parse cosmo-sokol.json
    // Extract upstream.sokol.last_sync_commit
    // Compare with current submodule HEAD
}
```

**CI workflows:**
```yaml
- name: Read manifest
  id: manifest
  run: |
    echo "cosmocc=$(jq -r '.build.minimum_cosmocc' cosmo-sokol.json)" >> $GITHUB_OUTPUT
```

### Maintenance

The manifest should be updated:
1. After each sync (update last_sync, last_sync_commit)
2. When adding new tools/workflows
3. When changing build requirements

**Automation (optional):**
```bash
# Update sync date in manifest
jq '.upstream.sokol.last_sync = "'"$(date +%Y-%m-%d)"'"' \
   cosmo-sokol.json > tmp.json && mv tmp.json cosmo-sokol.json
```

## Success Criteria

- [ ] `cosmo-sokol.json` is valid JSON
- [ ] Schema is well-documented
- [ ] Contains accurate current state
- [ ] Parseable by jq in CI
- [ ] Useful for tooling integration

## File Location

```
C:\cosmo-sokol\
└── cosmo-sokol.json    # CREATE (project root)
```

## Dependencies

- **Requires:** Nothing (independent deliverable)
- **Provides:** Metadata for tools, CI, documentation

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Manual updates forgotten | CI job to validate/update |
| Schema unclear | Document in README |
| JSON parse errors | Validate in pre-commit |

## Integration Points

1. **drift-report.c:** Read last_sync info
2. **CI workflows:** Read build config
3. **Documentation:** Generate from manifest
4. **Pre-commit hooks:** Validate JSON syntax

---

*dbeng Plan Complete*
