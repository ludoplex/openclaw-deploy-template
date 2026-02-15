# Stage Prompts: localsearch

**Specialist:** localsearch  
**Total Stages:** 3

---

## Stage 1: pre-commit-drift-check.sh Implementation

### Prompt

```
You are the localsearch specialist implementing scripts/pre-commit-drift-check.sh for the cosmo-sokol project.

CONTEXT:
- Developers need to catch API mismatches before pushing to CI
- The project has C tools (check-api-sync, drift-report) for validation
- Must work on Linux, Windows (Git Bash), and macOS

TASK:
Create a pre-commit hook script that:
1. Runs check-api-sync if available (blocks on failure)
2. Runs drift-report if available (warns on high drift, doesn't block)
3. Provides clear output with colors (optional, degrades gracefully)
4. Allows bypass with --no-verify

REQUIREMENTS:
- Shebang: #!/bin/bash
- set -e for strict error handling
- Find tools relative to git root
- Color output (RED, GREEN) with NC fallback
- Clear success/failure messages
- Helpful bypass instructions

INSTALLATION:
```bash
cp scripts/pre-commit-drift-check.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

EXPECTED OUTPUT (success):
```
🔍 Pre-commit drift check...
  Checking API sync...
  ✓ API in sync
  Checking drift...
  ✓ Minimal drift: 12 commits
✓ Pre-commit checks passed
```

EXPECTED OUTPUT (failure):
```
🔍 Pre-commit drift check...
  Checking API sync...
❌ API mismatch detected!
   Run './tools/check-api-sync' for details
   Bypass with: git commit --no-verify
```

EXIT CODES:
- 0: All checks passed
- 1: API mismatch (critical, blocks)
- Note: Drift warnings don't block

EDGE CASES:
- Tools not built yet → skip gracefully
- jq not available → skip drift count
- Not in git repo → error early

Provide the complete script.
```

---

## Stage 2: verify-symbols.sh Implementation

### Prompt

```
You are the localsearch specialist implementing scripts/verify-symbols.sh for the cosmo-sokol project.

CONTEXT:
- APE binaries are polyglot (DOS/PE/ELF headers combined)
- Standard tools (nm, objdump) may not parse them correctly
- Need to verify expected symbols are exported after build

TASK:
Create a script that:
1. Extracts symbols from APE binary
2. Checks for expected sokol symbols
3. Reports missing symbols clearly
4. Handles tool failures gracefully

USAGE:
```bash
./scripts/verify-symbols.sh ./build/cosmo-sokol-demo
./scripts/verify-symbols.sh  # Uses default path
```

EXPECTED SYMBOLS:
```bash
EXPECTED_SYMBOLS=(
    # sokol_app
    "sapp_run"
    "sapp_isvalid"
    "sapp_width"
    "sapp_height"
    "sapp_dpi_scale"
    # sokol_gfx
    "sg_setup"
    "sg_shutdown"
    "sg_make_buffer"
    "sg_make_shader"
    "sg_make_pipeline"
    "sg_apply_pipeline"
    "sg_apply_bindings"
    "sg_apply_uniforms"
    "sg_draw"
    "sg_commit"
)
```

SYMBOL EXTRACTION (with fallbacks):
```bash
extract_symbols() {
    local bin="$1"
    
    # Try nm first (works on many systems)
    if command -v nm &>/dev/null; then
        nm "$bin" 2>/dev/null | grep -E ' [TtWw] ' | awk '{print $NF}' && return 0
    fi
    
    # Fallback to objdump
    if command -v objdump &>/dev/null; then
        objdump -t "$bin" 2>/dev/null | awk '/FUNC/ {print $NF}' && return 0
    fi
    
    # Last resort: strings + grep (less reliable)
    if command -v strings &>/dev/null; then
        strings "$bin" | grep -E '^(sapp_|sg_)' && return 0
    fi
    
    return 1
}
```

OUTPUT FORMAT:
```
🔍 Verifying symbols in: ./build/cosmo-sokol-demo

  ✓ sapp_run
  ✓ sapp_isvalid
  ✓ sapp_width
  ✓ sg_setup
  ...
  ❌ MISSING: sg_new_function

✓ All expected symbols present (15/15)
or
❌ 2 symbols missing (13/15)
```

EXIT CODES:
- 0: All symbols found
- 1: Some symbols missing
- 2: Binary not found or cannot extract symbols

Provide the complete script.
```

---

## Stage 3: watch-manifest.json Implementation

### Prompt

```
You are the localsearch specialist implementing scripts/watch-manifest.json for the cosmo-sokol project.

CONTEXT:
- Developers use file watchers for automatic rebuilds
- Different file changes require different actions
- This manifest documents those relationships

TASK:
Create a JSON manifest that:
1. Documents which files trigger which actions
2. Groups related files logically
3. Provides human-readable descriptions
4. Can be consumed by tooling (if desired)

STRUCTURE:
```json
{
  "version": 1,
  "description": "File watch triggers for cosmo-sokol development",
  "triggers": {
    "trigger-name": {
      "description": "Human-readable explanation",
      "patterns": ["glob patterns"],
      "action": "command to run"
    }
  }
}
```

TRIGGER GROUPS:

1. **api-check**: Changes that require API sync verification
   - deps/sokol/*.h
   - shims/include/gen-sokol.h
   - Action: ./tools/check-api-sync

2. **full-rebuild**: Changes requiring complete rebuild
   - shims/**/*.c
   - shims/**/*.h
   - Makefile
   - Action: make clean && make

3. **tools-rebuild**: Changes to C tools
   - tools/*.c
   - tools/Makefile
   - Action: make -C tools clean && make -C tools

4. **ci-validate**: Workflow changes
   - .github/workflows/*.yml
   - Action: yamllint + dry run

5. **docs-check**: Documentation changes
   - *.md
   - docs/**/*.md
   - Action: markdown lint (optional)

6. **hook-update**: Hook script changes
   - scripts/*.sh
   - Action: Copy to .git/hooks + chmod

Provide the complete JSON file with all triggers properly documented.
```

---

## Verification Commands

After all stages:

```bash
cd C:\cosmo-sokol

# Test pre-commit hook
./scripts/pre-commit-drift-check.sh
echo "Exit code: $?"

# Install hook
cp scripts/pre-commit-drift-check.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# Test symbol verification (after build)
./scripts/verify-symbols.sh ./build/cosmo-sokol-demo

# Validate JSON
python -c "import json; json.load(open('scripts/watch-manifest.json'))"
```

---

*localsearch Stage Prompts Complete*
