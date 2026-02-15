# Stage Prompts: seeker

**Specialist:** seeker  
**Total Stages:** 4

---

## Stage 1: tools/Makefile Implementation

### Prompt

```
You are the seeker specialist implementing tools/Makefile for the cosmo-sokol project.

CONTEXT:
- All tools must compile with cosmocc (Cosmopolitan C compiler)
- Tools are standalone APE binaries, no shared libraries
- Must work on Linux, Windows, macOS

TASK:
Create tools/Makefile that:
1. Compiles all C tools (check-api-sync, validate-sources, changelog-scan, drift-report)
2. Uses cosmocc as the compiler
3. Includes appropriate optimization and warning flags
4. Provides 'all', 'clean', and individual tool targets

REQUIREMENTS:
- Default target: all
- CC = cosmocc (can be overridden: make CC=gcc)
- CFLAGS = -O2 -Wall -Wextra
- Proper dependencies (recompile on source change)
- Clean removes binaries

EXPECTED USAGE:
```bash
cd tools
make              # Build all tools
make clean        # Remove binaries
make check-api-sync  # Build specific tool
CC=gcc make       # Use different compiler
```

Provide the complete Makefile.
```

---

## Stage 2: changelog-scan.c Implementation

### Prompt

```
You are the seeker specialist implementing tools/changelog-scan.c for the cosmo-sokol project.

CONTEXT:
- sokol's CHANGELOG.md uses markdown format with dated sections
- Breaking changes need to be surfaced before sync
- Date formats vary: "23-Nov-2024", "2024-11-23", "Merge branch (23-Dec-2024)"

TASK:
Implement tools/changelog-scan.c that:
1. Parses sokol CHANGELOG.md
2. Filters entries since a given date
3. Classifies severity (BREAKING, WARN, INFO)
4. Outputs actionable summary

COMMAND LINE:
```
./changelog-scan --since 2024-01-01 deps/sokol/CHANGELOG.md
./changelog-scan --help
```

DATE PARSING (CRITICAL):
Support multiple formats:
- DD-Mon-YYYY: "23-Nov-2024"
- YYYY-MM-DD: "2024-11-23"  
- Embedded in text: "Merge branch 'compute' (23-Dec-2024)"

SEVERITY CLASSIFICATION (CONTEXT-AWARE):
```c
// BREAKING
- Contains "BREAKING:" or "**BREAKING**"
- "API removed", "function removed", "callback removed"
- "signature changed"

// WARN
- "deprecated" (without "internal" or "private")
- "renamed" (public API)

// INFO (not breaking)
- "removed unused", "removed redundant", "cleanup"
- "internal", "private" modifications
```

OUTPUT FORMAT:
```
Scanning deps/sokol/CHANGELOG.md for changes since 2024-01-01...

🔴 BREAKING (1):
  23-Nov-2024: sg_apply_uniforms signature changed (stage parameter removed)

🟡 WARNINGS (3):
  15-Dec-2024: deprecated sapp_keyboard_shown
  ...

🟢 INFO (47):
  (count only, or list with --verbose)

Summary: 1 breaking, 3 warnings, 47 info changes
Exit code: 1 (breaking changes found) | 0 (no breaking)
```

EXIT CODES:
- 0: No breaking changes
- 1: Breaking changes found
- 2: Parse error / file not found

Provide the complete implementation.
```

---

## Stage 3: drift-report.c Implementation

### Prompt

```
You are the seeker specialist implementing tools/drift-report.c for the cosmo-sokol project.

CONTEXT:
- cosmo-sokol has git submodules (deps/sokol, deps/cimgui)
- These drift behind their upstream repositories
- Need to measure and report drift for decision-making

TASK:
Implement tools/drift-report.c that:
1. Identifies submodule current commit
2. Fetches upstream to compare
3. Counts commits behind
4. Reports status and recommendations

COMMAND LINE:
```
./drift-report                    # Check all known submodules
./drift-report --path deps/sokol  # Check specific path
./drift-report --json             # JSON output for CI
```

CRITICAL FIX - WINDOWS COMPATIBILITY:
Do NOT use: `popen("cd path && git ...")`
Instead use chdir() for cross-platform support:
```c
#ifdef _WIN32
#include <direct.h>
#define chdir _chdir
#define getcwd _getcwd
#endif

static int run_git_cmd_in_dir(const char* dir, const char* git_args, 
                               char* output, size_t output_size) {
    char original_cwd[512];
    getcwd(original_cwd, sizeof(original_cwd));
    
    if (chdir(dir) != 0) {
        fprintf(stderr, "Cannot change to directory: %s\n", dir);
        return -1;
    }
    
    // Run git command directly (no shell cd)
    char cmd[512];
    snprintf(cmd, sizeof(cmd), "git %s", git_args);
    FILE* fp = popen(cmd, "r");
    // ... read output ...
    
    chdir(original_cwd);  // Always restore
    return ret;
}
```

GIT COMMANDS NEEDED:
```bash
# Get current commit
git rev-parse HEAD

# Fetch upstream
git fetch origin master

# Count commits behind
git rev-list --count HEAD..origin/master

# Get commit date
git log -1 --format=%ci HEAD
```

OUTPUT FORMAT:
```
Drift Report - cosmo-sokol submodules
=====================================

deps/sokol:
  Current:  abc1234 (2024-03-15)
  Upstream: def5678 (2025-02-09)
  Behind:   1,032 commits
  Status:   ⚠️ SIGNIFICANT DRIFT (>500)

deps/cimgui:
  Current:  111aaaa (2024-06-01)
  Upstream: 222bbbb (2025-01-15)
  Behind:   89 commits
  Status:   🟡 MODERATE DRIFT (50-500)

Total drift: 1,121 commits across 2 submodules

Recommendations:
  1. Review CHANGELOG before syncing deps/sokol
  2. Run './tools/changelog-scan --since <last-sync-date>'
  3. Consider incremental sync if breaking changes found
```

JSON OUTPUT (--json):
```json
{
  "submodules": [
    {
      "path": "deps/sokol",
      "current": "abc1234",
      "upstream": "def5678",
      "behind": 1032,
      "status": "significant"
    }
  ],
  "total_drift": 1121
}
```

EXIT CODES:
- 0: No significant drift (<50 commits each)
- 1: Moderate or significant drift
- 2: Git error / submodule not found

Provide the complete implementation.
```

---

## Stage 4: SYNC.md Documentation

### Prompt

```
You are the seeker specialist creating SYNC.md for the cosmo-sokol project.

CONTEXT:
- Maintainers need clear documentation for syncing with upstream sokol
- The process involves multiple tools and checkpoints
- Documentation should be actionable and complete

TASK:
Create SYNC.md with comprehensive sync documentation.

REQUIRED SECTIONS:

# Synchronizing with Upstream Sokol

## Quick Start
```bash
# One-liner for simple syncs
./tools/drift-report && ./tools/changelog-scan --since $(git log -1 --format=%ci deps/sokol) deps/sokol/CHANGELOG.md && git submodule update --remote deps/sokol && ./tools/check-api-sync
```

## Prerequisites
- cosmocc installed
- git with submodule support
- C tools built (make -C tools)

## Pre-Sync Checklist
- [ ] Check current drift: `./tools/drift-report`
- [ ] Review breaking changes: `./tools/changelog-scan --since <date>`
- [ ] Backup current working state
- [ ] Ensure CI is green on current commit

## Sync Process

### Step 1: Assess Drift
```bash
./tools/drift-report
```
- <50 commits: Minor sync, proceed normally
- 50-500 commits: Moderate sync, review changelog carefully
- >500 commits: Major sync, consider incremental approach

### Step 2: Review Breaking Changes
```bash
./tools/changelog-scan --since <last-sync-date> deps/sokol/CHANGELOG.md
```
Note any BREAKING changes that require code updates.

### Step 3: Update Submodule
```bash
cd deps/sokol
git fetch origin
git checkout <target-commit-or-tag>
cd ../..
git add deps/sokol
```

### Step 4: Fix API Mismatches
```bash
./tools/check-api-sync
```
If mismatches found:
1. Update gen-sokol.h signatures
2. Update any shim code using changed APIs
3. Re-run check-api-sync until clean

### Step 5: Build and Test
```bash
make clean
make
./build/cosmo-sokol-demo  # Smoke test
```

### Step 6: Commit and Tag
```bash
git commit -m "sync: update sokol to <commit>"
git tag v<version>-sync
git push origin main --tags
```

## Rollback Procedure
If sync fails:
```bash
git submodule update --init  # Reset to committed state
```

## Automation (CI)
The upstream-sync.yml workflow runs weekly and creates PRs for review.

## FAQ
Q: What if check-api-sync fails?
A: The gen-sokol.h bindings need updating...

Provide the complete SYNC.md document.
```

---

## Verification Commands

After all stages:

```bash
cd C:\cosmo-sokol

# Build all tools
make -C tools

# Test changelog-scan
./tools/changelog-scan --since 2024-01-01 deps/sokol/CHANGELOG.md

# Test drift-report
./tools/drift-report

# Verify documentation
cat SYNC.md | head -50
```

---

*seeker Stage Prompts Complete*
