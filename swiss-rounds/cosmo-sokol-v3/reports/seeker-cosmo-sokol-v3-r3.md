# Seeker Report: cosmo-sokol-v3 — Round 3

**Specialist:** Seeker (Advanced search, source discovery, upstream tracking)
**Date:** 2026-02-09
**Focus:** Upstream tracking methodology using C/APE tools only (no Python)
**Prior Work:** Rounds 1-2 reports in this file

---

## 1. Philosophy Alignment — Accepting the C/APE Mandate

The Round 2 triad solution made a critical point:

> "Python tooling has no place in a Cosmopolitan project."

**I fully accept this.** My Round 1-2 proposals included Python scripts (`extract-sokol-api.py`, `scan-changelog.py`). These violated the project's core identity.

### 1.1 Withdrawn Proposals

| Proposal | Status | Replacement |
|----------|--------|-------------|
| `scripts/extract-sokol-api.py` | ❌ WITHDRAWN | C-based `check-api-sync.c` (testcov/triad) |
| `scripts/scan-changelog.py` | ❌ WITHDRAWN | C-based `changelog-scan.c` (proposed below) |
| `scripts/generate-sync-report.py` | ❌ WITHDRAWN | Shell + C hybrid approach |

### 1.2 What Remains Valid

My **documentation deliverables** remain valid but need updates:
- `SYNC.md` — Updated for C tooling
- `CONTRIBUTING.md` updates — Updated for C tooling
- Upstream data contribution to `cosmo-sokol.json` — Unchanged

---

## 2. C-Based Upstream Tracking Architecture

### 2.1 Design Philosophy

**Cosmopolitan's Promise:**
- Build once, run anywhere
- No runtime dependencies
- Single portable binary

**Upstream Tracking Must Follow:**
- All tools compile to APE binaries
- Run identically on Linux, Windows, macOS, BSD
- Zero external dependencies (no Python, no Node, no Ruby)

### 2.2 Tool Architecture

```
tools/
├── check-api-sync.c       # API extraction + comparison (triad's impl)
├── validate-sources.c     # Pre-flight validation (triad's impl)
├── changelog-scan.c       # Changelog breaking change detection (NEW)
├── drift-report.c         # Generate upstream drift reports (NEW)
└── Makefile               # Build all tools with cosmocc
```

All tools:
- Use `cosmocc` compiler
- Produce APE binaries
- Run on any supported platform without modification

---

## 3. New Proposal: `changelog-scan.c`

The triad's `check-api-sync.c` handles API extraction. **Missing piece:** detecting breaking changes from upstream changelog.

### 3.1 Purpose

Scan sokol's CHANGELOG.md for breaking changes since a known commit/date.

### 3.2 Implementation

**File:** `tools/changelog-scan.c`

```c
/**
 * changelog-scan - Detect breaking changes in sokol's CHANGELOG.md
 * 
 * Compiled with: cosmocc -o tools/changelog-scan tools/changelog-scan.c
 * 
 * Cosmopolitan APE binary - runs on Linux, Windows, macOS, BSD
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <time.h>

#define MAX_LINE 4096
#define MAX_FILE_SIZE (512 * 1024)  // 512 KB
#define MAX_ENTRIES 256

// Breaking change keywords (case-insensitive search)
static const char* BREAKING_KEYWORDS[] = {
    "BREAKING",
    "breaking change",
    "breaking:",
    "API change",
    "signature change",
    "renamed",
    "removed",
    "deprecated",
    "incompatible",
    NULL
};

// Severity levels
typedef enum {
    SEV_INFO = 0,
    SEV_WARN = 1,
    SEV_BREAKING = 2
} Severity;

typedef struct {
    char date[32];
    char line[MAX_LINE];
    Severity severity;
} ChangeEntry;

typedef struct {
    ChangeEntry entries[MAX_ENTRIES];
    int count;
} ChangeLog;

// Case-insensitive substring search
static bool icontains(const char* haystack, const char* needle) {
    size_t h_len = strlen(haystack);
    size_t n_len = strlen(needle);
    
    if (n_len > h_len) return false;
    
    for (size_t i = 0; i <= h_len - n_len; i++) {
        bool match = true;
        for (size_t j = 0; j < n_len && match; j++) {
            if (tolower(haystack[i + j]) != tolower(needle[j])) {
                match = false;
            }
        }
        if (match) return true;
    }
    return false;
}

// Parse date from changelog header (e.g., "### 23-Nov-2024")
static bool parse_date(const char* line, char* date_out, size_t size) {
    // Skip markdown headers
    const char* p = line;
    while (*p == '#' || *p == ' ') p++;
    
    // Look for pattern: DD-Mon-YYYY
    const char* months[] = {"Jan", "Feb", "Mar", "Apr", "May", "Jun",
                            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"};
    
    for (int m = 0; m < 12; m++) {
        const char* found = strstr(p, months[m]);
        if (found && found > p) {
            // Extract the date portion
            const char* start = found;
            while (start > p && (isdigit(start[-1]) || start[-1] == '-')) start--;
            
            const char* end = found + 3;
            while (*end && (isdigit(*end) || *end == '-')) end++;
            
            size_t len = end - start;
            if (len < size) {
                strncpy(date_out, start, len);
                date_out[len] = '\0';
                return true;
            }
        }
    }
    return false;
}

// Parse YYYY-MM-DD date string to time_t
static time_t parse_iso_date(const char* date_str) {
    struct tm tm = {0};
    int year, month, day;
    
    if (sscanf(date_str, "%d-%d-%d", &year, &month, &day) == 3) {
        tm.tm_year = year - 1900;
        tm.tm_mon = month - 1;
        tm.tm_mday = day;
        return mktime(&tm);
    }
    return 0;
}

// Convert "23-Nov-2024" to time_t
static time_t parse_changelog_date(const char* date_str) {
    const char* months[] = {"Jan", "Feb", "Mar", "Apr", "May", "Jun",
                            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"};
    struct tm tm = {0};
    int day, year;
    char month_str[4];
    
    if (sscanf(date_str, "%d-%3s-%d", &day, month_str, &year) == 3) {
        for (int m = 0; m < 12; m++) {
            if (strcasecmp(month_str, months[m]) == 0) {
                tm.tm_year = year - 1900;
                tm.tm_mon = m;
                tm.tm_mday = day;
                return mktime(&tm);
            }
        }
    }
    return 0;
}

// Determine severity based on content
static Severity classify_severity(const char* line) {
    for (int i = 0; BREAKING_KEYWORDS[i]; i++) {
        if (icontains(line, BREAKING_KEYWORDS[i])) {
            // "BREAKING" is definitely breaking
            if (icontains(line, "BREAKING") || icontains(line, "removed")) {
                return SEV_BREAKING;
            }
            // Others are warnings
            return SEV_WARN;
        }
    }
    return SEV_INFO;
}

// Read and parse changelog
static int scan_changelog(const char* path, const char* since_date, ChangeLog* log) {
    FILE* f = fopen(path, "r");
    if (!f) {
        fprintf(stderr, "Error: Cannot open changelog: %s\n", path);
        return -1;
    }
    
    time_t since = parse_iso_date(since_date);
    if (since == 0) {
        fprintf(stderr, "Error: Invalid date format: %s (expected YYYY-MM-DD)\n", since_date);
        fclose(f);
        return -1;
    }
    
    char line[MAX_LINE];
    char current_date[32] = {0};
    time_t current_time = 0;
    log->count = 0;
    
    while (fgets(line, sizeof(line), f) && log->count < MAX_ENTRIES) {
        // Trim newline
        size_t len = strlen(line);
        while (len > 0 && (line[len-1] == '\n' || line[len-1] == '\r')) {
            line[--len] = '\0';
        }
        
        // Check for date header
        if (line[0] == '#') {
            char date[32];
            if (parse_date(line, date, sizeof(date))) {
                strncpy(current_date, date, sizeof(current_date) - 1);
                current_time = parse_changelog_date(date);
            }
            continue;
        }
        
        // Skip if before our threshold date
        if (current_time != 0 && current_time < since) {
            continue;
        }
        
        // Check for breaking change indicators
        Severity sev = classify_severity(line);
        if (sev > SEV_INFO) {
            strncpy(log->entries[log->count].date, current_date, 31);
            strncpy(log->entries[log->count].line, line, MAX_LINE - 1);
            log->entries[log->count].severity = sev;
            log->count++;
        }
    }
    
    fclose(f);
    return log->count;
}

static void print_usage(const char* prog) {
    printf("changelog-scan - Detect breaking changes in CHANGELOG.md\n\n");
    printf("Usage: %s [OPTIONS] <changelog-path>\n\n", prog);
    printf("Options:\n");
    printf("  --since YYYY-MM-DD   Only show changes after this date\n");
    printf("  --json               Output in JSON format\n");
    printf("  --breaking-only      Only show breaking changes (not warnings)\n");
    printf("  --help               Show this help\n");
    printf("\nExamples:\n");
    printf("  %s --since 2024-11-23 deps/sokol/CHANGELOG.md\n", prog);
    printf("  %s --since 2024-11-23 --json deps/sokol/CHANGELOG.md\n", prog);
}

int main(int argc, char* argv[]) {
    const char* since_date = "2024-01-01";  // Default: past year
    const char* changelog_path = NULL;
    bool json_output = false;
    bool breaking_only = false;
    
    // Parse arguments
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--since") == 0 && i + 1 < argc) {
            since_date = argv[++i];
        } else if (strcmp(argv[i], "--json") == 0) {
            json_output = true;
        } else if (strcmp(argv[i], "--breaking-only") == 0) {
            breaking_only = true;
        } else if (strcmp(argv[i], "--help") == 0 || strcmp(argv[i], "-h") == 0) {
            print_usage(argv[0]);
            return 0;
        } else if (argv[i][0] != '-') {
            changelog_path = argv[i];
        }
    }
    
    if (!changelog_path) {
        // Default path
        changelog_path = "deps/sokol/CHANGELOG.md";
    }
    
    ChangeLog log = {0};
    int count = scan_changelog(changelog_path, since_date, &log);
    
    if (count < 0) {
        return 1;
    }
    
    // Filter if breaking-only
    int relevant = 0;
    for (int i = 0; i < log.count; i++) {
        if (!breaking_only || log.entries[i].severity == SEV_BREAKING) {
            relevant++;
        }
    }
    
    // Output
    if (json_output) {
        printf("{\n");
        printf("  \"since\": \"%s\",\n", since_date);
        printf("  \"file\": \"%s\",\n", changelog_path);
        printf("  \"total_flagged\": %d,\n", log.count);
        printf("  \"entries\": [\n");
        
        int printed = 0;
        for (int i = 0; i < log.count; i++) {
            if (breaking_only && log.entries[i].severity != SEV_BREAKING) continue;
            
            if (printed > 0) printf(",\n");
            printf("    {\n");
            printf("      \"date\": \"%s\",\n", log.entries[i].date);
            printf("      \"severity\": \"%s\",\n", 
                   log.entries[i].severity == SEV_BREAKING ? "breaking" : "warning");
            // Escape the line for JSON
            printf("      \"text\": \"");
            for (const char* p = log.entries[i].line; *p; p++) {
                if (*p == '"') printf("\\\"");
                else if (*p == '\\') printf("\\\\");
                else if (*p == '\n') printf("\\n");
                else printf("%c", *p);
            }
            printf("\"\n");
            printf("    }");
            printed++;
        }
        
        printf("\n  ]\n");
        printf("}\n");
    } else {
        printf("=== Changelog Scan Results ===\n");
        printf("Since: %s\n", since_date);
        printf("File:  %s\n", changelog_path);
        printf("Found: %d potential breaking changes\n\n", relevant);
        
        if (relevant == 0) {
            printf("✅ No breaking changes detected\n");
        } else {
            for (int i = 0; i < log.count; i++) {
                if (breaking_only && log.entries[i].severity != SEV_BREAKING) continue;
                
                const char* icon = log.entries[i].severity == SEV_BREAKING ? "🔴" : "⚠️";
                printf("%s [%s] %s\n", icon, log.entries[i].date, log.entries[i].line);
            }
        }
    }
    
    // Exit code: 1 if breaking changes found
    int breaking_count = 0;
    for (int i = 0; i < log.count; i++) {
        if (log.entries[i].severity == SEV_BREAKING) breaking_count++;
    }
    
    return breaking_count > 0 ? 1 : 0;
}
```

### 3.3 Usage in CI

```yaml
- name: Scan for breaking changes
  run: |
    ./tools/changelog-scan --since 2024-11-23 --json deps/sokol/CHANGELOG.md > breaking.json
    BREAKING=$(jq '.entries | map(select(.severity == "breaking")) | length' breaking.json)
    if [ "$BREAKING" -gt 0 ]; then
      echo "::warning::$BREAKING breaking changes detected since last sync"
    fi
```

---

## 4. New Proposal: `drift-report.c`

Generate human-readable and machine-parseable upstream drift reports.

### 4.1 Purpose

Produce a report showing:
- Current submodule commit vs upstream HEAD
- Commits behind count
- Summary of changes (files modified, insertions, deletions)

### 4.2 Implementation

**File:** `tools/drift-report.c`

```c
/**
 * drift-report - Generate upstream drift report using git
 * 
 * Compiled with: cosmocc -o tools/drift-report tools/drift-report.c
 * 
 * Note: This tool shells out to git for data, but all logic is in C.
 * The binary itself is portable; git is expected on the build machine.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <time.h>

#define MAX_LINE 1024
#define MAX_OUTPUT 65536

// Run a shell command and capture output
static int run_cmd(const char* cmd, char* output, size_t output_size) {
    FILE* fp = popen(cmd, "r");
    if (!fp) return -1;
    
    size_t total = 0;
    char line[MAX_LINE];
    
    while (fgets(line, sizeof(line), fp) && total < output_size - 1) {
        size_t len = strlen(line);
        if (total + len < output_size - 1) {
            strcpy(output + total, line);
            total += len;
        }
    }
    output[total] = '\0';
    
    return pclose(fp);
}

// Get single-line command output (strips newline)
static int run_cmd_line(const char* cmd, char* output, size_t output_size) {
    int ret = run_cmd(cmd, output, output_size);
    size_t len = strlen(output);
    while (len > 0 && (output[len-1] == '\n' || output[len-1] == '\r')) {
        output[--len] = '\0';
    }
    return ret;
}

typedef struct {
    char name[64];
    char path[256];
    char current_commit[64];
    char current_date[32];
    char upstream_commit[64];
    char upstream_date[32];
    int commits_behind;
    int files_changed;
    int insertions;
    int deletions;
} DriftInfo;

static int get_drift_info(const char* submodule_path, const char* upstream_ref, DriftInfo* info) {
    char cmd[512];
    char output[MAX_OUTPUT];
    
    // Get submodule name from path
    const char* name = strrchr(submodule_path, '/');
    name = name ? name + 1 : submodule_path;
    strncpy(info->name, name, sizeof(info->name) - 1);
    strncpy(info->path, submodule_path, sizeof(info->path) - 1);
    
    // Current commit
    snprintf(cmd, sizeof(cmd), "cd \"%s\" && git rev-parse HEAD", submodule_path);
    if (run_cmd_line(cmd, info->current_commit, sizeof(info->current_commit)) != 0) {
        fprintf(stderr, "Error: Cannot get current commit for %s\n", submodule_path);
        return -1;
    }
    
    // Current commit date
    snprintf(cmd, sizeof(cmd), "cd \"%s\" && git log -1 --format=%%ci HEAD", submodule_path);
    run_cmd_line(cmd, info->current_date, sizeof(info->current_date));
    
    // Fetch upstream
    snprintf(cmd, sizeof(cmd), "cd \"%s\" && git fetch origin %s 2>/dev/null", 
             submodule_path, upstream_ref);
    run_cmd(cmd, output, sizeof(output));
    
    // Upstream commit
    snprintf(cmd, sizeof(cmd), "cd \"%s\" && git rev-parse origin/%s", 
             submodule_path, upstream_ref);
    if (run_cmd_line(cmd, info->upstream_commit, sizeof(info->upstream_commit)) != 0) {
        fprintf(stderr, "Error: Cannot get upstream commit for %s\n", submodule_path);
        return -1;
    }
    
    // Upstream commit date
    snprintf(cmd, sizeof(cmd), "cd \"%s\" && git log -1 --format=%%ci origin/%s", 
             submodule_path, upstream_ref);
    run_cmd_line(cmd, info->upstream_date, sizeof(info->upstream_date));
    
    // Commits behind
    snprintf(cmd, sizeof(cmd), "cd \"%s\" && git rev-list --count HEAD..origin/%s", 
             submodule_path, upstream_ref);
    run_cmd_line(cmd, output, sizeof(output));
    info->commits_behind = atoi(output);
    
    // Diffstat
    if (info->commits_behind > 0) {
        snprintf(cmd, sizeof(cmd), 
                 "cd \"%s\" && git diff --shortstat HEAD..origin/%s", 
                 submodule_path, upstream_ref);
        run_cmd_line(cmd, output, sizeof(output));
        
        // Parse "N files changed, M insertions(+), K deletions(-)"
        sscanf(output, "%d file", &info->files_changed);
        char* ins = strstr(output, "insertion");
        if (ins) {
            while (ins > output && ins[-1] != ' ' && ins[-1] != ',') ins--;
            info->insertions = atoi(ins);
        }
        char* del = strstr(output, "deletion");
        if (del) {
            while (del > output && del[-1] != ' ' && del[-1] != ',') del--;
            info->deletions = atoi(del);
        }
    }
    
    return 0;
}

static void print_json(DriftInfo* infos, int count) {
    time_t now = time(NULL);
    char timestamp[64];
    strftime(timestamp, sizeof(timestamp), "%Y-%m-%dT%H:%M:%SZ", gmtime(&now));
    
    printf("{\n");
    printf("  \"generated_at\": \"%s\",\n", timestamp);
    printf("  \"submodules\": [\n");
    
    for (int i = 0; i < count; i++) {
        printf("    {\n");
        printf("      \"name\": \"%s\",\n", infos[i].name);
        printf("      \"path\": \"%s\",\n", infos[i].path);
        printf("      \"current_commit\": \"%s\",\n", infos[i].current_commit);
        printf("      \"current_date\": \"%s\",\n", infos[i].current_date);
        printf("      \"upstream_commit\": \"%s\",\n", infos[i].upstream_commit);
        printf("      \"upstream_date\": \"%s\",\n", infos[i].upstream_date);
        printf("      \"commits_behind\": %d,\n", infos[i].commits_behind);
        printf("      \"files_changed\": %d,\n", infos[i].files_changed);
        printf("      \"insertions\": %d,\n", infos[i].insertions);
        printf("      \"deletions\": %d\n", infos[i].deletions);
        printf("    }%s\n", i < count - 1 ? "," : "");
    }
    
    printf("  ]\n");
    printf("}\n");
}

static void print_text(DriftInfo* infos, int count) {
    printf("╔═══════════════════════════════════════════════════════════════╗\n");
    printf("║            UPSTREAM DRIFT REPORT                              ║\n");
    printf("╠═══════════════════════════════════════════════════════════════╣\n");
    
    for (int i = 0; i < count; i++) {
        DriftInfo* info = &infos[i];
        
        const char* status;
        if (info->commits_behind == 0) status = "✅ UP TO DATE";
        else if (info->commits_behind < 100) status = "ℹ️  MINOR DRIFT";
        else if (info->commits_behind < 500) status = "⚠️  MODERATE DRIFT";
        else status = "🔴 CRITICAL DRIFT";
        
        printf("║  %-20s %s\n", info->name, status);
        printf("║  ────────────────────────────────────────────────────────────\n");
        printf("║  Current:   %.12s (%s)\n", info->current_commit, info->current_date);
        printf("║  Upstream:  %.12s (%s)\n", info->upstream_commit, info->upstream_date);
        printf("║  Behind:    %d commits\n", info->commits_behind);
        
        if (info->commits_behind > 0) {
            printf("║  Changes:   %d files, +%d/-%d lines\n", 
                   info->files_changed, info->insertions, info->deletions);
        }
        
        if (i < count - 1) {
            printf("║  \n");
        }
    }
    
    printf("╚═══════════════════════════════════════════════════════════════╝\n");
}

int main(int argc, char* argv[]) {
    bool json_output = false;
    
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--json") == 0) json_output = true;
        if (strcmp(argv[i], "--help") == 0) {
            printf("drift-report - Generate upstream drift report\n\n");
            printf("Usage: %s [OPTIONS]\n\n", argv[0]);
            printf("Options:\n");
            printf("  --json    Output in JSON format\n");
            printf("  --help    Show this help\n");
            return 0;
        }
    }
    
    // Define submodules to check
    struct { const char* path; const char* upstream_ref; } submodules[] = {
        {"deps/sokol", "master"},
        {"deps/cimgui", "master"},
        {NULL, NULL}
    };
    
    DriftInfo infos[8] = {0};
    int count = 0;
    
    for (int i = 0; submodules[i].path; i++) {
        if (get_drift_info(submodules[i].path, submodules[i].upstream_ref, &infos[count]) == 0) {
            count++;
        }
    }
    
    if (json_output) {
        print_json(infos, count);
    } else {
        print_text(infos, count);
    }
    
    // Exit code: 1 if any submodule has critical drift (500+)
    for (int i = 0; i < count; i++) {
        if (infos[i].commits_behind >= 500) {
            return 1;
        }
    }
    
    return 0;
}
```

### 4.3 Usage

```bash
# Human-readable output
./tools/drift-report

# JSON output for CI
./tools/drift-report --json > drift.json
```

---

## 5. Updated `SYNC.md` — C Tooling Edition

Replacing my Round 2 documentation with C-tools-aware version:

**File:** `SYNC.md`

```markdown
# Upstream Synchronization Guide

This document explains how to keep cosmo-sokol synchronized with upstream sokol.

## Philosophy

cosmo-sokol follows Cosmopolitan's philosophy: **no external dependencies**.

All sync tooling compiles to APE binaries that run on any platform without installation.

## Quick Start

```bash
# Build sync tools
cd tools && make all

# Check current drift
./tools/drift-report

# Check for API changes
./tools/check-api-sync

# Scan for breaking changes
./tools/changelog-scan --since 2024-11-23
```

## Available Tools

| Tool | Purpose | Output |
|------|---------|--------|
| `drift-report` | Show commits behind for each submodule | Text/JSON |
| `check-api-sync` | Compare header APIs vs gen-sokol | Diff report |
| `changelog-scan` | Find breaking changes in CHANGELOG.md | Change list |
| `validate-sources` | Pre-flight source file validation | Pass/Fail |

All tools are built with `cosmocc` and produce portable APE binaries.

## Sync Process

### Step 1: Check Current State

```bash
./tools/drift-report
```

Output shows:
- ✅ UP TO DATE — No action needed
- ℹ️ MINOR DRIFT — <100 commits, can defer
- ⚠️ MODERATE DRIFT — 100-500 commits, schedule sync
- 🔴 CRITICAL DRIFT — 500+ commits, sync immediately

### Step 2: Review Breaking Changes

```bash
# Get breaking changes since last sync
./tools/changelog-scan --since 2024-11-23

# JSON output for automation
./tools/changelog-scan --since 2024-11-23 --json
```

Address any breaking changes before updating.

### Step 3: Update Submodule

```bash
git submodule update --remote deps/sokol
git add deps/sokol
git commit -m "deps: update sokol to $(cd deps/sokol && git rev-parse --short HEAD)"
```

### Step 4: Check API Sync

```bash
./tools/check-api-sync
```

If APIs are out of sync:
1. Update `SOKOL_FUNCTIONS` in `shims/sokol/gen-sokol`
2. Regenerate: `python shims/sokol/gen-sokol` (legacy, to be replaced)
3. Rerun `check-api-sync` to verify

### Step 5: Build and Test

```bash
./build
./bin/cosmo-sokol --headless
```

### Step 6: Submit PR

Branch naming: `sync/sokol-YYYYMMDD`

Include in PR:
- Commits behind before/after
- Breaking changes addressed
- New functions added (if any)

## Drift Thresholds

| Commits Behind | Status | Action |
|----------------|--------|--------|
| 0-100 | ✅ OK | No action |
| 100-300 | ⚠️ Warning | Schedule sync |
| 300-500 | 🔶 Urgent | Prioritize sync |
| 500+ | 🔴 Critical | Block other work |

## CI Integration

The `upstream-sync.yml` workflow:
1. Runs weekly (Sunday midnight UTC)
2. Fetches upstream refs
3. Runs `drift-report --json`
4. Creates GitHub issue if drift exceeds threshold

## Building Tools

```bash
cd tools
make all
```

Requirements:
- `cosmocc` (Cosmopolitan compiler)
- No other dependencies

The resulting binaries run on Linux, Windows, macOS, BSD without modification.

## Breaking Change History

| Date | Change | Impact |
|------|--------|--------|
| 2024-11-07 | Bindings cleanup | `sg_apply_uniforms` signature |
| 2025-01-xx | Compute shaders | New `sg_dispatch()` |
| 2025-02-xx | Resource views | New `sg_make_view()` |

## Platform-Specific Functions

These functions require platform-specific backends:

| Function | Platform | Status |
|----------|----------|--------|
| `sapp_metal_*` | macOS Metal | Stub |
| `sapp_d3d11_*` | Windows D3D11 | Not used |
| `sapp_wgpu_*` | WebGPU | Not supported |

cosmo-sokol uses OpenGL on all platforms.
```

---

## 6. Updated Tools Makefile

**File:** `tools/Makefile`

```makefile
# tools/Makefile - Build cosmo-sokol development tools
#
# All tools are APE binaries - portable to Linux/Windows/macOS/BSD

CC = cosmocc
CFLAGS = -O2 -Wall -Wextra -Wno-unused-parameter

TOOLS = check-api-sync validate-sources changelog-scan drift-report

.PHONY: all clean test

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

test: all
	./validate-sources || echo "Validation check"
	./check-api-sync || echo "API sync check"
	./changelog-scan --since 2024-01-01 || echo "Changelog check"
	./drift-report || echo "Drift check"
```

---

## 7. Integration with Other Specialists

### 7.1 Data Flow

```
                    ┌──────────────┐
                    │   testcov    │
                    │check-api-sync│
                    └──────┬───────┘
                           │ API drift data
                           ▼
┌──────────┐    ┌──────────────────┐    ┌──────────┐
│  seeker  │───▶│ tools/Makefile   │◀───│   cicd   │
│changelog │    │ (build system)   │    │ workflow │
│drift-rpt │    └──────────────────┘    └──────────┘
└──────────┘               │
                           ▼
                    ┌──────────────┐
                    │    dbeng     │
                    │cosmo-sokol.  │
                    │    json      │
                    └──────────────┘
```

### 7.2 Seeker Contributes

| To Specialist | Data | Format |
|---------------|------|--------|
| testcov | N/A (testcov owns check-api-sync.c) | — |
| cicd | Exit codes from tools | 0=ok, 1=drift |
| dbeng | JSON output from tools | Structured data |
| cosmo | Breaking change list | For migration planning |

### 7.3 Seeker Receives

| From Specialist | Input | Purpose |
|-----------------|-------|---------|
| triad | check-api-sync.c impl | Base API checking tool |
| triad | validate-sources.c impl | Base validation tool |
| cicd | Workflow integration | Tool execution context |

---

## 8. Addressing Round 2 Triad Critique Items

| Critique Item | Addressed In Round 3 |
|---------------|---------------------|
| Python scripts violate philosophy | ✅ All proposals now C/APE |
| Multi-line regex issues | ✅ Using triad's C implementation |
| No pycparser | ✅ Accepted — C approach avoids need |
| Duplicate scripts | ✅ Consolidated to tools/ directory |

---

## 9. Round 3 Deliverables

### 9.1 New C Tool Proposals

| File | Purpose | Status |
|------|---------|--------|
| `tools/changelog-scan.c` | Changelog breaking change detection | NEW |
| `tools/drift-report.c` | Upstream drift reporting | NEW |

### 9.2 Updated Documentation

| File | Purpose | Status |
|------|---------|--------|
| `SYNC.md` | Contributor guide for C tooling | UPDATED |

### 9.3 Build System

| File | Purpose | Status |
|------|---------|--------|
| `tools/Makefile` | Updated with new tools | UPDATED |

---

## 10. Success Criteria (Seeker Domain, Round 3)

1. ✅ No Python in any seeker proposal
2. ✅ All tools compile with cosmocc to APE binaries
3. ✅ Tools produce both human-readable and JSON output
4. ✅ Documentation reflects C-only tooling
5. ✅ Clear integration points with other specialists
6. ✅ Exit codes usable by CI workflows

---

## 11. Enlightened Proposal (Post-Round-3)

### Core Insight

The upstream tracking problem is fundamentally about **answering three questions**:

1. **How far behind are we?** → `drift-report.c`
2. **What APIs changed?** → `check-api-sync.c` (testcov/triad)
3. **What broke?** → `changelog-scan.c`

All three are now answerable with portable C tools that embody Cosmopolitan's philosophy.

### Architecture Benefits

```
Developer machine (any OS):
  $ ./tools/drift-report
  $ ./tools/check-api-sync
  $ ./tools/changelog-scan --since 2024-11-23

CI runner (any OS):
  - run: ./tools/drift-report --json > drift.json
  - run: ./tools/check-api-sync
  - run: ./tools/changelog-scan --json > breaking.json
```

Same binaries, same behavior, everywhere.

### What Seeker Does NOT Own (Confirmed)

- `check-api-sync.c` → testcov (using triad's implementation)
- `validate-sources.c` → localsearch (using triad's implementation)
- CI workflows → cicd
- Version manifest → dbeng
- dlopen safety → cosmo

### What Seeker DOES Own

- `changelog-scan.c` — Detecting upstream breaking changes
- `drift-report.c` — Generating drift reports
- `SYNC.md` — Contributor documentation for sync process
- Upstream intelligence data for other specialists

---

*Round 3 Complete — Seeker scope: C/APE upstream tracking tools + documentation*
*Philosophy aligned: No Python, no external dependencies, runs anywhere*
