# Triad Phase 3: Solutions — cosmo-sokol-v3 — Round 2

**Triad Role:** Solution Architect  
**Date:** 2026-02-09  
**Reports Analyzed:** Round 2 Critique + Redundancy reports  
**Critical Finding:** Fundamental philosophy violation — Python tooling in a Cosmopolitan project

---

## Executive Summary

### The Bigger Problem

The Round 2 specialists did excellent work addressing Round 1 issues. **However, there's a fundamental problem that was missed:**

> **Python tooling has no place in a Cosmopolitan project.**

Cosmopolitan's entire philosophy is:
- ✅ No runtime dependencies
- ✅ Single portable binary (APE)
- ✅ Runs on any OS without installation

The specialists proposed:
- ❌ `check-api-sync.py` — requires Python 3.11
- ❌ `validate-source-files.py` — requires Python
- ❌ `function_coverage.py` — requires Python
- ❌ Various Python scripts for automation

**This violates the project's core identity.** A Cosmopolitan project's tooling should ALSO be Cosmopolitan — portable C programs that compile to APE binaries.

### Solution Overview

| Problem Category | Items | Solution |
|------------------|-------|----------|
| P0 Bugs | 3 | Fixes provided below |
| P1 Bugs | 5 | Fixes provided below |
| Philosophy Violation | All Python scripts | Replace with C/APE tools |

---

## Part 1: P0 Bug Fixes (CRITICAL — Must Fix Before Merge)

### 1.1 P0: Xvfb Not Installed (neteng)

**Bug:** Smoke test calls `Xvfb :99` but Xvfb is not in the apt package list.

**File:** `.github/workflows/build.yml`

**Fix:**
```yaml
# BEFORE (incomplete package list)
- name: Install deps
  uses: awalsh128/cache-apt-pkgs-action@a6c3917cc929dd0345bfb2d3feaf9101823370ad
  with:
    packages: libx11-dev libgl-dev libxcursor-dev libxi-dev
    version: "1.0"

# AFTER (add xvfb and xauth)
- name: Install deps
  uses: awalsh128/cache-apt-pkgs-action@a6c3917cc929dd0345bfb2d3feaf9101823370ad
  with:
    packages: libx11-dev libgl-dev libxcursor-dev libxi-dev xvfb xauth
    version: "1.1"  # Bump version to force cache refresh
```

---

### 1.2 P0: Regex Matches #define Lines (testcov)

**Bug:** The whitespace normalization causes `#define SG_RANGE(x)` to be mismatched as a function declaration.

**Root Cause:** Preprocessor directives aren't filtered before regex matching.

**The Python Fix (for reference only — will be replaced with C):**
```python
def extract_functions(content, macro):
    # CRITICAL: Remove preprocessor directives BEFORE whitespace normalization
    content = re.sub(r'#\s*define\s+[^\n]*(?:\\\n[^\n]*)*', '', content)
    content = re.sub(r'#\s*(?:if|ifdef|ifndef|else|elif|endif|include|pragma)[^\n]*', '', content)
    content = normalize_whitespace(content)
    # ... rest of extraction
```

**The Real Fix:** See Part 2 — replace with C implementation.

---

### 1.3 P0: Platform Hints Show Linux Commands on Windows (cosmo)

**Bug:** `_cosmo_dl_install_hint()` always returns Linux package manager commands, even on Windows.

**File:** `shims/include/cosmo_dl_safe.h`

**Fix:**
```c
#include <string.h>  // Required for strstr (also fixes P1 bug 2.2)

// Platform detection - use Cosmopolitan's runtime macros
extern bool IsWindows(void);
extern bool IsXnu(void);
extern bool IsLinux(void);

static inline const char* _cosmo_dl_install_hint(const char* lib_name) {
    // Windows — different error messages
    if (IsWindows()) {
        if (strstr(lib_name, "opengl32") || strstr(lib_name, "OpenGL")) {
            return "  OpenGL is included with Windows.\n"
                   "  Update your graphics drivers from your GPU vendor's website.\n";
        }
        if (strstr(lib_name, "user32") || strstr(lib_name, "gdi32") || 
            strstr(lib_name, "kernel32")) {
            return "  This is a core Windows system library.\n"
                   "  Your Windows installation may be corrupted.\n";
        }
        return "  Ensure the required DLL is in your PATH or application directory.\n"
               "  You may need to install Visual C++ Redistributable.\n";
    }
    
    // macOS — different library locations and no package manager
    if (IsXnu()) {
        if (strstr(lib_name, "libobjc")) {
            return "  libobjc.dylib is part of macOS.\n"
                   "  Your macOS installation may be corrupted.\n";
        }
        if (strstr(lib_name, "OpenGL") || strstr(lib_name, "libGL")) {
            return "  OpenGL.framework is included with macOS.\n"
                   "  Check System Preferences > Security & Privacy > Privacy > Developer Tools.\n";
        }
        if (strstr(lib_name, "Metal")) {
            return "  Metal.framework requires macOS 10.11 or later.\n"
                   "  Ensure Xcode Command Line Tools are installed: xcode-select --install\n";
        }
        return "  This library should be part of macOS.\n"
               "  Try: xcode-select --install\n";
    }
    
    // Linux — the original package manager hints
    if (strstr(lib_name, "X11")) {
        return "  Ubuntu/Debian: sudo apt install libx11-dev\n"
               "  Fedora/RHEL:   sudo dnf install libX11-devel\n"
               "  Arch Linux:    sudo pacman -S libx11\n";
    }
    if (strstr(lib_name, "Xcursor")) {
        return "  Ubuntu/Debian: sudo apt install libxcursor-dev\n"
               "  Fedora/RHEL:   sudo dnf install libXcursor-devel\n"
               "  Arch Linux:    sudo pacman -S libxcursor\n";
    }
    if (strstr(lib_name, "Xi")) {
        return "  Ubuntu/Debian: sudo apt install libxi-dev\n"
               "  Fedora/RHEL:   sudo dnf install libXi-devel\n"
               "  Arch Linux:    sudo pacman -S libxi\n";
    }
    if (strstr(lib_name, "GL") || strstr(lib_name, "gl")) {
        return "  Ubuntu/Debian: sudo apt install libgl1-mesa-dev\n"
               "  Fedora/RHEL:   sudo dnf install mesa-libGL-devel\n"
               "  Arch Linux:    sudo pacman -S mesa\n";
    }
    
    return "  Check your system's package manager for the required library.\n";
}
```

---

## Part 2: P1 Bug Fixes

### 2.1 P1: String Comparison Instead of Numeric (cicd)

**Bug:** `if: steps.sokol.outputs.behind > 0` does string comparison, not numeric.

**File:** `.github/workflows/upstream-sync.yml`

**Fix:**
```yaml
# BEFORE (string comparison)
- name: Check API drift
  if: steps.sokol.outputs.behind > 0

# AFTER (numeric comparison via fromJSON)
- name: Check API drift
  if: ${{ fromJSON(steps.sokol.outputs.behind) > 0 }}
```

And for the issue creation threshold:
```yaml
# BEFORE
- name: Create drift issue
  if: steps.sokol.outputs.behind > 100

# AFTER  
- name: Create drift issue
  if: ${{ fromJSON(steps.sokol.outputs.behind) > 100 && steps.check_existing.outputs.exists == 'false' }}
```

---

### 2.2 P1: Duplicate Issue Creation (cicd)

**Bug:** Multiple workflow runs can create duplicate "upstream-drift" issues.

**Fix:** Add deduplication check:
```yaml
- name: Check for existing drift issue
  id: check_existing
  run: |
    EXISTING=$(gh issue list --label "upstream-drift" --state open --json number --jq 'length')
    if [ "$EXISTING" -gt 0 ]; then
      echo "exists=true" >> $GITHUB_OUTPUT
      echo "Drift issue already exists, skipping creation"
    else
      echo "exists=false" >> $GITHUB_OUTPUT
    fi
  env:
    GH_TOKEN: ${{ github.token }}

- name: Create drift issue
  if: ${{ fromJSON(steps.sokol.outputs.behind) > 100 && steps.check_existing.outputs.exists == 'false' }}
  uses: peter-evans/create-issue-from-file@v5
  with:
    title: "sokol submodule is ${{ steps.sokol.outputs.behind }} commits behind"
    labels: upstream-drift
```

---

### 2.3 P1: API Rate Limit on Unauthenticated Requests (neteng)

**Bug:** Unauthenticated GitHub API calls may hit rate limits (60/hour).

**File:** `.github/workflows/build.yml`

**Fix:**
```yaml
# BEFORE (unauthenticated)
- name: Download cosmocc
  run: |
    COSMOCC_VERSION="3.9.6"
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
      "https://api.github.com/repos/jart/cosmopolitan/releases/tags/${COSMOCC_VERSION}")

# AFTER (authenticated)
- name: Download cosmocc
  run: |
    COSMOCC_VERSION="3.9.6"
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
      -H "Authorization: Bearer ${{ github.token }}" \
      "https://api.github.com/repos/jart/cosmopolitan/releases/tags/${COSMOCC_VERSION}")
```

---

### 2.4 P1: Missing string.h Include (cosmo)

**Bug:** `cosmo_dl_safe.h` uses `strstr()` without including `<string.h>`.

**Fix:** Already incorporated in Part 1, Section 1.3 — the fixed header includes `<string.h>`.

---

### 2.5 P1: Duplicate dlopen Headers (asm/cosmo)

**Bug:** Both asm and cosmo specialists created similar dlopen safety headers.

**Resolution:** Use **cosmo's `cosmo_dl_safe.h`** as the authoritative implementation.

| Header | Owner | Status |
|--------|-------|--------|
| `cosmo_dl_safe.h` | cosmo | ✅ AUTHORITATIVE |
| `cosmo_dlopen_safe.h` | asm | ❌ DEPRECATED — use cosmo's version |

**asm's responsibility:** Update any references to use `cosmo_dl_safe.h` instead.

---

## Part 3: THE REAL FIX — Replace Python with C/APE Tooling

### 3.1 Philosophy Alignment

**Cosmopolitan's Promise:**
> "Build once, run anywhere — no dependencies, no runtime, no installation."

**Current Tooling (WRONG):**
```
scripts/
├── check-api-sync.py      # Requires Python 3.11
├── validate-source-files.py  # Requires Python
├── function_coverage.py   # Requires Python
└── gen-sokol              # Python script
```

**Proposed Tooling (RIGHT):**
```
tools/
├── check-api-sync.c       # Compiles to APE binary
├── validate-sources.c     # Compiles to APE binary
├── gen-sokol.c            # Compiles to APE binary
└── Makefile               # Uses cosmocc
```

### 3.2 C Implementation: `check-api-sync.c`

This replaces `check-api-sync.py` — a single portable binary that works on Linux, Windows, macOS, BSD, etc.

**File:** `tools/check-api-sync.c`

```c
/**
 * check-api-sync - Verify API sync between sokol headers and gen-sokol
 * 
 * Compiled with: cosmocc -o tools/check-api-sync tools/check-api-sync.c
 * 
 * This is a Cosmopolitan APE binary - runs on Linux, Windows, macOS, BSD
 * without any dependencies or installation.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>

#define MAX_FUNCTIONS 512
#define MAX_SIG_LEN 512
#define MAX_LINE_LEN 4096
#define MAX_FILE_SIZE (2 * 1024 * 1024)  // 2 MB

typedef struct {
    char name[128];
    char signature[MAX_SIG_LEN];
} Function;

typedef struct {
    Function funcs[MAX_FUNCTIONS];
    int count;
} FunctionList;

// Strip leading/trailing whitespace
static char* strip(char* s) {
    while (isspace(*s)) s++;
    char* end = s + strlen(s) - 1;
    while (end > s && isspace(*end)) *end-- = '\0';
    return s;
}

// Collapse multiple whitespace into single space
static void normalize_whitespace(char* s) {
    char* src = s;
    char* dst = s;
    bool in_space = false;
    
    while (*src) {
        if (isspace(*src)) {
            if (!in_space) {
                *dst++ = ' ';
                in_space = true;
            }
        } else {
            *dst++ = *src;
            in_space = false;
        }
        src++;
    }
    *dst = '\0';
}

// Check if line is a preprocessor directive
static bool is_preprocessor(const char* line) {
    const char* p = line;
    while (isspace(*p)) p++;
    return *p == '#';
}

// Extract function name from signature
static bool extract_func_name(const char* sig, char* name_out, size_t name_size) {
    // Find the opening parenthesis
    const char* paren = strchr(sig, '(');
    if (!paren) return false;
    
    // Walk backwards to find the function name
    const char* name_end = paren - 1;
    while (name_end > sig && isspace(*name_end)) name_end--;
    
    const char* name_start = name_end;
    while (name_start > sig && (isalnum(name_start[-1]) || name_start[-1] == '_')) {
        name_start--;
    }
    
    size_t len = name_end - name_start + 1;
    if (len >= name_size) len = name_size - 1;
    
    strncpy(name_out, name_start, len);
    name_out[len] = '\0';
    
    return len > 0;
}

// Normalize parameters: treat () and (void) as equivalent
static void normalize_params(char* sig) {
    char* start = strchr(sig, '(');
    char* end = strrchr(sig, ')');
    
    if (!start || !end || end <= start) return;
    
    // Extract params
    size_t len = end - start - 1;
    char params[256] = {0};
    strncpy(params, start + 1, len < 255 ? len : 255);
    
    char* p = strip(params);
    
    // If empty or "void", normalize to void
    if (*p == '\0' || strcmp(p, "void") == 0) {
        // Replace params with "void"
        memmove(start + 1, "void", 4);
        memmove(start + 5, end, strlen(end) + 1);
    }
}

// Read entire file into buffer
static char* read_file(const char* path) {
    FILE* f = fopen(path, "rb");
    if (!f) {
        fprintf(stderr, "Error: Cannot open file: %s\n", path);
        return NULL;
    }
    
    fseek(f, 0, SEEK_END);
    long size = ftell(f);
    fseek(f, 0, SEEK_SET);
    
    if (size > MAX_FILE_SIZE) {
        fprintf(stderr, "Error: File too large: %s (%ld bytes)\n", path, size);
        fclose(f);
        return NULL;
    }
    
    char* buf = malloc(size + 1);
    if (!buf) {
        fprintf(stderr, "Error: Out of memory\n");
        fclose(f);
        return NULL;
    }
    
    fread(buf, 1, size, f);
    buf[size] = '\0';
    fclose(f);
    
    return buf;
}

// Strip C comments from content
static void strip_comments(char* content) {
    char* src = content;
    char* dst = content;
    
    while (*src) {
        // Block comment
        if (src[0] == '/' && src[1] == '*') {
            src += 2;
            while (*src && !(src[0] == '*' && src[1] == '/')) src++;
            if (*src) src += 2;
            *dst++ = ' ';  // Replace with space
            continue;
        }
        // Line comment
        if (src[0] == '/' && src[1] == '/') {
            while (*src && *src != '\n') src++;
            continue;
        }
        *dst++ = *src++;
    }
    *dst = '\0';
}

// Remove preprocessor directives from content
static void strip_preprocessor(char* content) {
    char* src = content;
    char* dst = content;
    bool at_line_start = true;
    
    while (*src) {
        if (at_line_start && *src == '#') {
            // Skip entire preprocessor directive (handle line continuations)
            while (*src) {
                if (*src == '\\' && src[1] == '\n') {
                    src += 2;
                } else if (*src == '\n') {
                    src++;
                    break;
                } else {
                    src++;
                }
            }
            at_line_start = true;
            continue;
        }
        
        at_line_start = (*src == '\n');
        *dst++ = *src++;
    }
    *dst = '\0';
}

// Extract functions with given API_DECL macro prefix
static int extract_api_functions(const char* content, const char* macro_prefix, 
                                  FunctionList* list) {
    char pattern[64];
    snprintf(pattern, sizeof(pattern), "%s_API_DECL", macro_prefix);
    
    const char* p = content;
    int count = 0;
    
    while ((p = strstr(p, pattern)) != NULL) {
        // Skip to after the macro
        p += strlen(pattern);
        
        // Find the semicolon (end of declaration)
        const char* semi = strchr(p, ';');
        if (!semi) break;
        
        // Extract the declaration
        size_t len = semi - p;
        if (len >= MAX_SIG_LEN) len = MAX_SIG_LEN - 1;
        
        char sig[MAX_SIG_LEN];
        strncpy(sig, p, len);
        sig[len] = '\0';
        
        // Skip if this contains "typedef" (it's not a function decl)
        if (strstr(sig, "typedef")) {
            p = semi + 1;
            continue;
        }
        
        // Normalize
        normalize_whitespace(sig);
        normalize_params(sig);
        
        // Extract function name
        char name[128];
        if (!extract_func_name(sig, name, sizeof(name))) {
            p = semi + 1;
            continue;
        }
        
        // Add to list
        if (list->count < MAX_FUNCTIONS) {
            strncpy(list->funcs[list->count].name, name, 127);
            strncpy(list->funcs[list->count].signature, strip(sig), MAX_SIG_LEN - 1);
            list->count++;
            count++;
        }
        
        p = semi + 1;
    }
    
    return count;
}

// Extract functions from gen-sokol script (parses SOKOL_FUNCTIONS list)
static int extract_gensokol_functions(const char* content, FunctionList* list) {
    // Find SOKOL_FUNCTIONS = [
    const char* start = strstr(content, "SOKOL_FUNCTIONS");
    if (!start) {
        fprintf(stderr, "Error: Cannot find SOKOL_FUNCTIONS in gen-sokol\n");
        return 0;
    }
    
    start = strchr(start, '[');
    if (!start) return 0;
    
    const char* end = strchr(start, ']');
    if (!end) return 0;
    
    // Extract quoted strings
    const char* p = start;
    int count = 0;
    
    while (p < end && (p = strchr(p, '"')) != NULL && p < end) {
        p++;  // Skip opening quote
        const char* q = strchr(p, '"');
        if (!q || q >= end) break;
        
        size_t len = q - p;
        if (len >= MAX_SIG_LEN) len = MAX_SIG_LEN - 1;
        
        char sig[MAX_SIG_LEN];
        strncpy(sig, p, len);
        sig[len] = '\0';
        
        normalize_whitespace(sig);
        normalize_params(sig);
        
        char name[128];
        if (extract_func_name(sig, name, sizeof(name))) {
            if (list->count < MAX_FUNCTIONS) {
                strncpy(list->funcs[list->count].name, name, 127);
                strncpy(list->funcs[list->count].signature, strip(sig), MAX_SIG_LEN - 1);
                list->count++;
                count++;
            }
        }
        
        p = q + 1;
    }
    
    return count;
}

// Find function by name in list
static Function* find_function(FunctionList* list, const char* name) {
    for (int i = 0; i < list->count; i++) {
        if (strcmp(list->funcs[i].name, name) == 0) {
            return &list->funcs[i];
        }
    }
    return NULL;
}

// Compare signatures (ignoring whitespace differences)
static bool signatures_match(const char* a, const char* b) {
    char norm_a[MAX_SIG_LEN], norm_b[MAX_SIG_LEN];
    strncpy(norm_a, a, MAX_SIG_LEN - 1);
    strncpy(norm_b, b, MAX_SIG_LEN - 1);
    
    normalize_whitespace(norm_a);
    normalize_whitespace(norm_b);
    normalize_params(norm_a);
    normalize_params(norm_b);
    
    return strcmp(strip(norm_a), strip(norm_b)) == 0;
}

static void print_usage(const char* prog) {
    printf("check-api-sync - Verify sokol API sync\n\n");
    printf("Usage: %s [OPTIONS]\n\n", prog);
    printf("Options:\n");
    printf("  --list-header    List functions from sokol headers\n");
    printf("  --list-gen       List functions from gen-sokol\n");
    printf("  --verbose        Show detailed comparison\n");
    printf("  --help           Show this help\n");
}

int main(int argc, char* argv[]) {
    bool list_header = false;
    bool list_gen = false;
    bool verbose = false;
    
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--list-header") == 0) list_header = true;
        else if (strcmp(argv[i], "--list-gen") == 0) list_gen = true;
        else if (strcmp(argv[i], "--verbose") == 0) verbose = true;
        else if (strcmp(argv[i], "--help") == 0 || strcmp(argv[i], "-h") == 0) {
            print_usage(argv[0]);
            return 0;
        }
    }
    
    // Read sokol headers
    char* sokol_app = read_file("deps/sokol/sokol_app.h");
    char* sokol_gfx = read_file("deps/sokol/sokol_gfx.h");
    char* gen_sokol = read_file("shims/sokol/gen-sokol");
    
    if (!sokol_app || !sokol_gfx || !gen_sokol) {
        fprintf(stderr, "\nHint: Run from cosmo-sokol repository root.\n");
        fprintf(stderr, "Required files:\n");
        fprintf(stderr, "  deps/sokol/sokol_app.h\n");
        fprintf(stderr, "  deps/sokol/sokol_gfx.h\n");
        fprintf(stderr, "  shims/sokol/gen-sokol\n");
        return 1;
    }
    
    // Preprocess headers: strip comments and preprocessor directives
    strip_comments(sokol_app);
    strip_comments(sokol_gfx);
    strip_preprocessor(sokol_app);
    strip_preprocessor(sokol_gfx);
    normalize_whitespace(sokol_app);
    normalize_whitespace(sokol_gfx);
    
    // Extract functions
    FunctionList header_funcs = {0};
    FunctionList gen_funcs = {0};
    
    int app_count = extract_api_functions(sokol_app, "SOKOL_APP", &header_funcs);
    int gfx_count = extract_api_functions(sokol_gfx, "SOKOL_GFX", &header_funcs);
    int gen_count = extract_gensokol_functions(gen_sokol, &gen_funcs);
    
    free(sokol_app);
    free(sokol_gfx);
    free(gen_sokol);
    
    // List mode
    if (list_header) {
        printf("Functions from sokol headers (%d total):\n", header_funcs.count);
        for (int i = 0; i < header_funcs.count; i++) {
            printf("  %s\n", header_funcs.funcs[i].name);
        }
        return 0;
    }
    
    if (list_gen) {
        printf("Functions from gen-sokol (%d total):\n", gen_funcs.count);
        for (int i = 0; i < gen_funcs.count; i++) {
            printf("  %s\n", gen_funcs.funcs[i].name);
        }
        return 0;
    }
    
    // Compare
    int missing = 0;
    int extra = 0;
    int changed = 0;
    
    // Check for functions in headers but not in gen-sokol
    for (int i = 0; i < header_funcs.count; i++) {
        Function* f = find_function(&gen_funcs, header_funcs.funcs[i].name);
        if (!f) {
            if (missing == 0) printf("\n❌ MISSING from gen-sokol (added upstream):\n");
            printf("  + %s\n", header_funcs.funcs[i].name);
            missing++;
        } else if (!signatures_match(header_funcs.funcs[i].signature, f->signature)) {
            if (changed == 0) printf("\n⚠️  SIGNATURE CHANGED:\n");
            printf("  %s\n", header_funcs.funcs[i].name);
            if (verbose) {
                printf("    header:    %s\n", header_funcs.funcs[i].signature);
                printf("    gen-sokol: %s\n", f->signature);
            }
            changed++;
        }
    }
    
    // Check for functions in gen-sokol but not in headers
    for (int i = 0; i < gen_funcs.count; i++) {
        Function* f = find_function(&header_funcs, gen_funcs.funcs[i].name);
        if (!f) {
            if (extra == 0) printf("\n⚠️  EXTRA in gen-sokol (removed upstream?):\n");
            printf("  - %s\n", gen_funcs.funcs[i].name);
            extra++;
        }
    }
    
    // Summary
    if (missing == 0 && extra == 0 && changed == 0) {
        printf("[OK] API in sync\n");
        printf("  sokol_app: %d functions\n", app_count);
        printf("  sokol_gfx: %d functions\n", gfx_count);
        printf("  gen-sokol: %d functions\n", gen_count);
        return 0;
    }
    
    printf("\n❌ API DRIFT DETECTED\n");
    printf("  Missing:  %d\n", missing);
    printf("  Extra:    %d\n", extra);
    printf("  Changed:  %d\n", changed);
    printf("\nTo fix: Update SOKOL_FUNCTIONS in shims/sokol/gen-sokol\n");
    
    return 1;
}
```

### 3.3 C Implementation: `validate-sources.c`

Replaces `validate-source-files.py`:

```c
/**
 * validate-sources - Pre-flight validation for cosmo-sokol source files
 * 
 * Verifies:
 * - Required files exist
 * - Files meet minimum size requirements  
 * - Required symbols are present
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

typedef struct {
    const char* path;
    long min_size;
    const char* required_symbols[8];
} FileSpec;

static const FileSpec REQUIRED_FILES[] = {
    {
        "deps/sokol/sokol_app.h",
        100000,
        {"SOKOL_APP_API_DECL", "sapp_run", "sapp_width", NULL}
    },
    {
        "deps/sokol/sokol_gfx.h",
        200000,
        {"SOKOL_GFX_API_DECL", "sg_setup", "sg_shutdown", NULL}
    },
    {
        "shims/sokol/gen-sokol",
        5000,
        {"SOKOL_FUNCTIONS", "sokol_app", "sokol_gfx", NULL}
    },
    {NULL, 0, {NULL}}
};

static bool file_contains(const char* path, const char* needle) {
    FILE* f = fopen(path, "rb");
    if (!f) return false;
    
    fseek(f, 0, SEEK_END);
    long size = ftell(f);
    fseek(f, 0, SEEK_SET);
    
    char* buf = malloc(size + 1);
    if (!buf) {
        fclose(f);
        return false;
    }
    
    fread(buf, 1, size, f);
    buf[size] = '\0';
    fclose(f);
    
    bool found = strstr(buf, needle) != NULL;
    free(buf);
    
    return found;
}

static long file_size(const char* path) {
    FILE* f = fopen(path, "rb");
    if (!f) return -1;
    
    fseek(f, 0, SEEK_END);
    long size = ftell(f);
    fclose(f);
    
    return size;
}

int main(void) {
    printf("=== Source File Validation ===\n\n");
    
    int errors = 0;
    int warnings = 0;
    
    for (const FileSpec* spec = REQUIRED_FILES; spec->path; spec++) {
        printf("Checking: %s\n", spec->path);
        
        // Check existence
        long size = file_size(spec->path);
        if (size < 0) {
            printf("  ❌ ERROR: File not found\n");
            errors++;
            continue;
        }
        
        // Check size
        if (size < spec->min_size) {
            printf("  ⚠️  WARNING: File smaller than expected (%ld < %ld)\n",
                   size, spec->min_size);
            warnings++;
        } else {
            printf("  ✓ Size OK (%ld bytes)\n", size);
        }
        
        // Check required symbols
        for (int i = 0; spec->required_symbols[i]; i++) {
            const char* sym = spec->required_symbols[i];
            if (!file_contains(spec->path, sym)) {
                printf("  ❌ ERROR: Missing required symbol: %s\n", sym);
                errors++;
            }
        }
    }
    
    printf("\n=== Results ===\n");
    printf("  Errors:   %d\n", errors);
    printf("  Warnings: %d\n", warnings);
    
    if (errors > 0) {
        printf("\n❌ Validation FAILED\n");
        printf("\nHint: Did you forget to initialize submodules?\n");
        printf("  git submodule update --init --recursive\n");
        return 1;
    }
    
    printf("\n✓ Validation PASSED\n");
    return 0;
}
```

### 3.4 Build System for Tools

**File:** `tools/Makefile`

```makefile
# tools/Makefile - Build cosmo-sokol development tools
#
# All tools are built with cosmocc and produce portable APE binaries
# that run on Linux, Windows, macOS, BSD without modification.

CC = cosmocc
CFLAGS = -O2 -Wall -Wextra

TOOLS = check-api-sync validate-sources

.PHONY: all clean

all: $(TOOLS)

check-api-sync: check-api-sync.c
	$(CC) $(CFLAGS) -o $@ $<

validate-sources: validate-sources.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TOOLS) *.o
```

### 3.5 Updated CI Configuration

**File:** `.github/workflows/build.yml` (tool build section)

```yaml
jobs:
  build-tools:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive
          
      - name: Setup cosmocc
        uses: bjia56/setup-cosmocc@main
        
      - name: Build tools
        run: |
          cd tools
          make all
          
      - name: Upload tools as artifacts
        uses: actions/upload-artifact@v4
        with:
          name: cosmo-sokol-tools
          path: |
            tools/check-api-sync
            tools/validate-sources
            
  validate:
    needs: build-tools
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive
          
      - uses: actions/download-artifact@v4
        with:
          name: cosmo-sokol-tools
          path: tools/
          
      - name: Validate sources
        run: |
          chmod +x tools/validate-sources
          ./tools/validate-sources
          
      - name: Check API sync
        run: |
          chmod +x tools/check-api-sync
          ./tools/check-api-sync
```

---

## Part 4: Why C Tooling Is Better

### 4.1 Alignment with Project Philosophy

| Aspect | Python Tooling | C/APE Tooling |
|--------|----------------|---------------|
| Dependencies | Requires Python 3.11+ | None |
| Portability | Needs Python runtime | Runs anywhere |
| CI complexity | Setup Python step | Just download and run |
| Developer setup | `pip install` | Just copy binary |
| Philosophy | Contradicts cosmo | Embraces cosmo |

### 4.2 Practical Benefits

**For Contributors:**
```bash
# With Python (current)
python3 --version  # Hope it's 3.11+
python scripts/check-api-sync.py

# With C/APE (proposed)
./tools/check-api-sync  # Just works
```

**For CI:**
```yaml
# With Python (current)
- uses: actions/setup-python@v5
  with:
    python-version: '3.11'
- run: python scripts/check-api-sync.py

# With C/APE (proposed)  
- run: ./tools/check-api-sync
```

### 4.3 Eating Your Own Dog Food

A Cosmopolitan project should showcase Cosmopolitan's strengths. Having Python scripts in the repo sends the message: "Cosmopolitan is cool, but we still need Python for the important stuff."

Having C/APE tools says: "Everything in this project — from the app to the tooling — is portable and dependency-free."

---

## Part 5: Migration Path

### Phase 1: Immediate (This PR)
1. Apply P0 bug fixes
2. Apply P1 bug fixes
3. Create `tools/` directory with C implementations
4. Update CI to build and use C tools

### Phase 2: Deprecation Notice
1. Keep Python scripts for 1 release with deprecation warning
2. Document C tools as the preferred approach

### Phase 3: Removal
1. Remove Python scripts
2. Remove Python setup from CI
3. Update all documentation

---

## Part 6: Complete File Listing

### Files to Create

| File | Purpose |
|------|---------|
| `tools/check-api-sync.c` | API sync verification (replaces Python) |
| `tools/validate-sources.c` | Source validation (replaces Python) |
| `tools/Makefile` | Build system for tools |

### Files to Modify

| File | Changes |
|------|---------|
| `shims/include/cosmo_dl_safe.h` | Add string.h, platform-aware hints |
| `.github/workflows/build.yml` | Add xvfb, API token, build C tools |
| `.github/workflows/upstream-sync.yml` | Fix numeric comparison, dedup issues |

### Files to Deprecate (Phase 2)

| File | Replacement |
|------|-------------|
| `scripts/check-api-sync.py` | `tools/check-api-sync` |
| `scripts/validate-source-files.py` | `tools/validate-sources` |
| `scripts/function_coverage.py` | Future C implementation |

---

## Summary

This solution addresses:

1. **3 P0 Critical Bugs:** Fixed with specific code changes
2. **5 P1 High Bugs:** Fixed with specific code changes
3. **Philosophy Violation:** Proposed complete replacement of Python tooling with C/APE binaries

The result is a cosmo-sokol project that truly embodies the Cosmopolitan philosophy from application code through to development tooling — everything is portable, dependency-free, and runs anywhere.

---

*Triad Round 2 Solution Complete*
*Ready for implementation*
