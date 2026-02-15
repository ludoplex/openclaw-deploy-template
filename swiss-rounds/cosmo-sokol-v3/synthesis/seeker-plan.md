# Specialist Plan: seeker

**Specialist:** seeker  
**Domain:** Upstream tracking, changelog analysis, drift reporting  
**Priority:** #2 (High)  
**Dependencies:** Phase 1 tools structure (after cosmo)  
**Estimated Effort:** 6 hours

---

## Mission

Implement the upstream tracking and drift detection tools that enable proactive sync management. Also own the tools Makefile and SYNC.md documentation.

## Deliverables

| File | Priority | Description |
|------|----------|-------------|
| `tools/Makefile` | P0 | Build system for all C tools |
| `tools/changelog-scan.c` | P1 | Parse CHANGELOG.md for breaking changes |
| `tools/drift-report.c` | P1 | Report submodule drift against upstream |
| `SYNC.md` | P1 | Documentation for sync process |

## Technical Specifications

### tools/Makefile

**Purpose:** Build all C/APE tools with cosmocc

```makefile
CC = cosmocc
CFLAGS = -O2 -Wall -Wextra

TOOLS = check-api-sync validate-sources changelog-scan drift-report

all: $(TOOLS)

check-api-sync: check-api-sync.c
	$(CC) $(CFLAGS) -o $@ $<

validate-sources: validate-sources.c
	$(CC) $(CFLAGS) -o $@ $<

changelog-scan: changelog-scan.c
	$(CC) $(CFLAGS) -o $@ $<

drift-report: drift-report.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TOOLS) *.o

.PHONY: all clean
```

### changelog-scan.c

**Purpose:** Parse sokol CHANGELOG.md and identify breaking changes since a given date

**Command Line:**
```
./changelog-scan --since 2024-01-01 deps/sokol/CHANGELOG.md
```

**Key Functions:**
```c
// Date parsing (robust - handle multiple formats)
static bool parse_date(const char* line, char* date_out, size_t size);
static time_t parse_any_date(const char* date_str);  // DD-Mon-YYYY and YYYY-MM-DD

// Severity classification (context-aware)
static Severity classify_severity(const char* line);
// - "BREAKING:" → SEV_BREAKING
// - "removed API" → SEV_BREAKING
// - "removed unused" → SEV_INFO (not breaking)

// Entry extraction
static int scan_changelog(const char* content, time_t since_date, Entry* entries);
```

**Output Format:**
```
Scanning deps/sokol/CHANGELOG.md for changes since 2024-01-01...

🔴 BREAKING (1):
  23-Nov-2024: sg_apply_uniforms signature changed (stage parameter removed)

🟡 WARNINGS (3):
  15-Dec-2024: deprecated sapp_keyboard_shown (use sapp_is_keyboard_shown)
  02-Jan-2025: renamed internal buffer handling
  ...

🟢 INFO (47):
  Various minor changes...

Summary: 1 breaking, 3 warnings, 47 info changes since 2024-01-01
```

**Critical Fixes:**
1. Multi-format date parsing (DD-Mon-YYYY and YYYY-MM-DD)
2. Context-aware BREAKING detection (ignore "removed unused")
3. Handle headers with text before date

### drift-report.c

**Purpose:** Report commit drift between submodule and upstream

**Command Line:**
```
./drift-report [--path deps/sokol] [--ref master]
```

**Key Functions:**
```c
// Platform-aware command execution (critical fix for Windows)
static int run_git_cmd_in_dir(const char* dir, const char* git_args, 
                               char* output, size_t output_size);

// Use chdir() instead of "cd && git" for Windows compatibility
static int git_fetch_in_dir(const char* dir, const char* ref);
static int git_rev_list_count(const char* dir, const char* range);

// Submodule discovery (optional enhancement)
static int discover_submodules(Submodule* out, int max);
```

**Output Format:**
```
Drift Report - cosmo-sokol submodules
=====================================

deps/sokol:
  Current:  abc1234 (2024-03-15)
  Upstream: def5678 (2025-02-09)
  Behind:   1,032 commits
  Status:   ⚠️ SIGNIFICANT DRIFT

deps/cimgui:
  Current:  111aaaa (2024-06-01)
  Upstream: 222bbbb (2025-01-15)
  Behind:   89 commits
  Status:   ⚠️ MODERATE DRIFT

Recommendations:
1. Review CHANGELOG for breaking changes before sync
2. Run check-api-sync after updating submodule
3. Consider incremental sync if drift > 500 commits
```

**Critical Fix - Windows Compatibility:**
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
    
    if (chdir(dir) != 0) return -1;
    
    char cmd[512];
    snprintf(cmd, sizeof(cmd), "git %s", git_args);
    
    int ret = run_cmd(cmd, output, output_size);
    
    chdir(original_cwd);
    return ret;
}
```

### SYNC.md

**Purpose:** Document the complete sync process for maintainers

**Structure:**
```markdown
# Synchronizing with Upstream Sokol

## Quick Start
## Prerequisites
## Pre-Sync Checklist
## Sync Process
### Step 1: Assess Drift
### Step 2: Review Breaking Changes
### Step 3: Update Submodule
### Step 4: Fix API Mismatches
### Step 5: Build and Test
### Step 6: Commit and Tag
## Rollback Procedure
## Automation (CI)
## FAQ
```

## Success Criteria

- [ ] `make -C tools all` builds all 4 tools
- [ ] `changelog-scan --since 2024-01-01` parses real CHANGELOG
- [ ] `drift-report` shows 1,032 commits behind
- [ ] `drift-report` works on Windows (Git Bash and cmd)
- [ ] SYNC.md covers complete process
- [ ] All tools produce clear, actionable output

## File Locations

```
C:\cosmo-sokol\
├── tools\
│   ├── Makefile              # CREATE
│   ├── changelog-scan.c      # CREATE
│   └── drift-report.c        # CREATE
└── SYNC.md                   # CREATE
```

## Dependencies

- **Requires:** cosmo tools structure (check-api-sync.c exists)
- **Requires:** Git installed and accessible
- **Provides to:** neteng (Makefile for CI), localsearch (drift-report for hooks)

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Date format not recognized | Multi-format parser with fallback |
| Windows popen() fails | Use chdir() + direct exec |
| Git not in PATH | Check for git before running, helpful error |
| Submodule paths change | Support --path argument, read .gitmodules |

---

*seeker Plan Complete*
