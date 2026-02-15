# Stage Prompts: dbeng

**Specialist:** dbeng  
**Total Stages:** 1

---

## Stage 1: cosmo-sokol.json Implementation

### Prompt

```
You are the dbeng specialist implementing cosmo-sokol.json for the cosmo-sokol project.

CONTEXT:
- cosmo-sokol is a Cosmopolitan libc port of floooh/sokol
- The project has multiple submodules, build tools, and CI workflows
- Need a central manifest for project metadata

TASK:
Create cosmo-sokol.json as the authoritative project manifest containing:
1. Project metadata (name, description, license, repo)
2. Upstream tracking info (sokol, cimgui submodules)
3. Build configuration (cosmocc versions, platforms)
4. Tooling inventory (C tools, workflows)
5. Sync configuration (thresholds, schedule)

SCHEMA:
```json
{
  "version": "manifest schema version",
  "project": {
    "name": "project name",
    "description": "project description",
    "repository": "GitHub URL",
    "license": "license type",
    "maintainers": ["list of maintainers"]
  },
  "upstream": {
    "sokol": {
      "repository": "upstream URL",
      "branch": "tracking branch",
      "last_sync": "YYYY-MM-DD",
      "last_sync_commit": "full SHA"
    }
  },
  "build": {
    "cosmocc_versions": ["tested versions"],
    "minimum_cosmocc": "minimum required",
    "platforms": ["supported platforms"]
  },
  "tooling": {
    "tools": ["list of C tools"],
    "workflows": ["list of workflow files"]
  },
  "sync": {
    "status": "current|drift|significant-drift",
    "drift_threshold_moderate": 50,
    "drift_threshold_significant": 500,
    "auto_sync_enabled": true,
    "sync_schedule": "cron expression or description"
  },
  "api": {
    "sokol_app_functions": 61,
    "sokol_gfx_functions": 103,
    "gen_sokol_functions": 164
  }
}
```

CURRENT STATE TO CAPTURE:
- sokol submodule: 1,032 commits behind (last sync ~2024-03-15)
- cimgui submodule: moderate drift
- Tested cosmocc: 3.9.5, 3.9.6
- Platforms: Linux x86_64, Windows x86_64, macOS x86_64/arm64

USAGE EXAMPLES:

By drift-report.c:
```c
// Parse manifest for last sync commit
const char* last_sync = json_get(manifest, "upstream.sokol.last_sync_commit");
```

By CI workflows:
```yaml
- name: Get cosmocc version
  run: |
    VERSION=$(jq -r '.build.minimum_cosmocc' cosmo-sokol.json)
    echo "Using cosmocc $VERSION"
```

By documentation:
```bash
# Generate platform support table
jq -r '.build.platforms[]' cosmo-sokol.json
```

REQUIREMENTS:
- Valid JSON (parseable by jq, Python json, etc.)
- Human-readable (properly formatted, commented if needed)
- Machine-consumable (consistent structure)
- Accurate current state

Provide the complete JSON file.
```

---

## Verification Commands

After implementation:

```bash
cd C:\cosmo-sokol

# Validate JSON syntax
python -c "import json; json.load(open('cosmo-sokol.json'))"

# Pretty print
jq . cosmo-sokol.json

# Query examples
jq '.upstream.sokol.last_sync' cosmo-sokol.json
jq '.build.cosmocc_versions[]' cosmo-sokol.json
jq '.sync.drift_threshold_significant' cosmo-sokol.json
```

---

*dbeng Stage Prompts Complete*
