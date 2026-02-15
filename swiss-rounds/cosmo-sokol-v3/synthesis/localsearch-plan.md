# Specialist Plan: localsearch

**Specialist:** localsearch  
**Domain:** File inventory, developer workflows, pre-commit hooks  
**Priority:** #5 (Medium)  
**Dependencies:** All tools working (Phase 3 complete)  
**Estimated Effort:** 4 hours

---

## Mission

Implement developer workflow tooling including pre-commit hooks and symbol verification scripts that catch drift before it reaches CI.

## Deliverables

| File | Priority | Description |
|------|----------|-------------|
| `scripts/pre-commit-drift-check.sh` | P2 | Git pre-commit hook for drift detection |
| `scripts/verify-symbols.sh` | P2 | Post-build symbol verification |
| `scripts/watch-manifest.json` | P3 | File change monitoring triggers |

## Technical Specifications

### pre-commit-drift-check.sh

**Purpose:** Block commits if significant drift detected or API out of sync

**Installation:**
```bash
cp scripts/pre-commit-drift-check.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

**Behavior:**
1. Run drift-report (if available)
2. Run check-api-sync (if available)
3. Block commit if either fails
4. Allow bypass with `--no-verify`

**Implementation:**
```bash
#!/bin/bash
set -e

# Colors (optional, degrade gracefully)
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "🔍 Pre-commit drift check..."

# Check if tools exist
TOOLS_DIR="$(git rev-parse --show-toplevel)/tools"

# API sync check (critical)
if [ -x "$TOOLS_DIR/check-api-sync" ]; then
    echo "  Checking API sync..."
    if ! "$TOOLS_DIR/check-api-sync" > /dev/null 2>&1; then
        echo -e "${RED}❌ API mismatch detected!${NC}"
        echo "   Run './tools/check-api-sync' for details"
        echo "   Bypass with: git commit --no-verify"
        exit 1
    fi
    echo -e "  ${GREEN}✓${NC} API in sync"
else
    echo "  ⚠️ check-api-sync not found, skipping"
fi

# Drift check (warning only, don't block)
if [ -x "$TOOLS_DIR/drift-report" ]; then
    echo "  Checking drift..."
    DRIFT=$("$TOOLS_DIR/drift-report" --json 2>/dev/null | jq -r '.total_drift // 0')
    if [ "$DRIFT" -gt 500 ]; then
        echo -e "  ${RED}⚠️ Significant drift: $DRIFT commits${NC}"
        echo "  Consider syncing before new development"
    elif [ "$DRIFT" -gt 50 ]; then
        echo "  🟡 Moderate drift: $DRIFT commits"
    else
        echo -e "  ${GREEN}✓${NC} Minimal drift: $DRIFT commits"
    fi
fi

echo -e "${GREEN}✓ Pre-commit checks passed${NC}"
exit 0
```

### verify-symbols.sh

**Purpose:** Verify APE binary exports expected symbols

**Usage:**
```bash
./scripts/verify-symbols.sh ./build/cosmo-sokol-demo
```

**Implementation:**
```bash
#!/bin/bash
set -e

BINARY="${1:-./build/cosmo-sokol-demo}"
EXPECTED_SYMBOLS=(
    "sapp_run"
    "sapp_width"
    "sapp_height"
    "sg_setup"
    "sg_shutdown"
    "sg_make_buffer"
    "sg_make_shader"
    "sg_make_pipeline"
)

echo "🔍 Verifying symbols in: $BINARY"

if [ ! -f "$BINARY" ]; then
    echo "❌ Binary not found: $BINARY"
    exit 1
fi

# Extract symbols (handle APE format)
extract_symbols() {
    local bin="$1"
    
    # Try nm first
    if command -v nm &>/dev/null; then
        if nm "$bin" 2>/dev/null | grep -E ' [TtWw] ' | awk '{print $NF}' 2>/dev/null; then
            return 0
        fi
    fi
    
    # Fallback to objdump
    if command -v objdump &>/dev/null; then
        if objdump -t "$bin" 2>/dev/null | awk '/FUNC/ {print $NF}' 2>/dev/null; then
            return 0
        fi
    fi
    
    echo "Warning: Could not extract symbols (nm/objdump not available)"
    return 1
}

SYMBOLS=$(extract_symbols "$BINARY" | sort -u)
MISSING=0

for sym in "${EXPECTED_SYMBOLS[@]}"; do
    if echo "$SYMBOLS" | grep -q "^${sym}$"; then
        echo "  ✓ $sym"
    else
        echo "  ❌ MISSING: $sym"
        MISSING=$((MISSING + 1))
    fi
done

echo ""
if [ $MISSING -eq 0 ]; then
    echo "✓ All expected symbols present"
    exit 0
else
    echo "❌ $MISSING symbols missing"
    exit 1
fi
```

### watch-manifest.json

**Purpose:** Define which files trigger rebuilds/rechecks

**Structure:**
```json
{
  "version": 1,
  "description": "File watch triggers for cosmo-sokol development",
  "triggers": {
    "api-check": {
      "description": "Files that require API sync check when modified",
      "patterns": [
        "deps/sokol/*.h",
        "shims/include/gen-sokol.h"
      ],
      "action": "./tools/check-api-sync"
    },
    "rebuild": {
      "description": "Files that require full rebuild",
      "patterns": [
        "shims/**/*.c",
        "shims/**/*.h",
        "Makefile"
      ],
      "action": "make clean && make"
    },
    "tools-rebuild": {
      "description": "Files that require tool rebuild",
      "patterns": [
        "tools/*.c",
        "tools/Makefile"
      ],
      "action": "make -C tools clean && make -C tools"
    },
    "ci-check": {
      "description": "Workflow files that need validation",
      "patterns": [
        ".github/workflows/*.yml"
      ],
      "action": "python -c \"import yaml; yaml.safe_load(open('$FILE'))\""
    }
  }
}
```

## Success Criteria

- [ ] `pre-commit-drift-check.sh` runs without errors
- [ ] Pre-commit blocks on API mismatch
- [ ] Pre-commit warns on high drift (doesn't block)
- [ ] `verify-symbols.sh` checks APE binary
- [ ] Handles APE format (nm may fail, fallback works)
- [ ] `watch-manifest.json` is valid JSON
- [ ] All scripts work on Linux, Windows (Git Bash), macOS

## File Locations

```
C:\cosmo-sokol\
└── scripts\
    ├── pre-commit-drift-check.sh   # CREATE
    ├── verify-symbols.sh           # CREATE
    └── watch-manifest.json         # CREATE
```

## Dependencies

- **Requires:** C tools built and working (cosmo, seeker)
- **Optional:** jq for JSON parsing (graceful degradation)
- **Provides:** Developer workflow guards

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| nm can't parse APE | Fallback to objdump, then warn |
| jq not installed | Parse with grep/awk fallback |
| Hook slows commits | Fast path if tools missing |
| Windows compatibility | Use Git Bash explicitly |

## Developer Setup

Add to CONTRIBUTING.md:

```markdown
## Setting Up Pre-commit Hooks

To catch API mismatches before they reach CI:

bash
# Install pre-commit hook
cp scripts/pre-commit-drift-check.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# Test the hook
.git/hooks/pre-commit

# Bypass if needed
git commit --no-verify -m "WIP"
```

---

*localsearch Plan Complete*
