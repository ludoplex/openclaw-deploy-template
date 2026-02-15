# Specialist Plan: cosmo

**Specialist:** cosmo  
**Domain:** Cosmopolitan libc internals, dlopen/dltramp, C tooling  
**Priority:** #1 (Critical Path)  
**Dependencies:** None (first in sequence)  
**Estimated Effort:** 8 hours

---

## Mission

Implement the core C/APE tooling that forms the foundation of the cosmo-sokol sync infrastructure. All other specialists depend on your deliverables.

## Deliverables

| File | Priority | Description |
|------|----------|-------------|
| `tools/check-api-sync.c` | P0 | API synchronization checker |
| `tools/validate-sources.c` | P0 | Source file validator |
| `shims/include/cosmo_dl_safe.h` | P0 | Safe dlopen macros |
| `shims/linux/x11.c` (update) | P1 | Use safe dlopen macros |

## Technical Specifications

### check-api-sync.c

**Purpose:** Compare sokol header APIs with gen-sokol.h bindings

**Inputs:**
- `deps/sokol/sokol_app.h` (~61 functions)
- `deps/sokol/sokol_gfx.h` (~100 functions)
- `shims/include/gen-sokol.h`

**Algorithm:**
1. Read all three files
2. Extract `SOKOL_APP_API_DECL` and `SOKOL_GFX_API_DECL` functions
3. Extract `gen_sapp_*` and `gen_sg_*` function declarations
4. Compare signatures (name, return type, parameters)
5. Report mismatches with exit code 1

**Key Functions to Implement:**
```c
static char* read_file(const char* path);
static void normalize_whitespace(char* str);
static void strip_inline_comments_from_sig(char* sig);  // P1 fix
static void normalize_pointer_spaces(char* type);       // P2 fix
static int extract_api_functions(const char* content, const char* api_macro, 
                                  FunctionList* out);
static int compare_function_lists(FunctionList* header, FunctionList* gen);
```

**Exit Codes:**
- 0: API in sync
- 1: API mismatch detected
- 2: File read error

**Critical Fixes to Include:**
1. Multi-line declaration handling (strip inline comments)
2. Empty file handling (minimum size check)
3. Pointer type normalization (`const void*` vs `const void *`)

### validate-sources.c

**Purpose:** Verify required source files exist and have valid content

**Files to Check:**
```c
static const char* REQUIRED_FILES[] = {
    "shims/include/gen-sokol.h",
    "deps/sokol/sokol_app.h",
    "deps/sokol/sokol_gfx.h",
    "deps/sokol/sokol_glue.h",
    NULL
};
```

**Validation Rules:**
- File exists
- File size > 0
- Header files contain expected markers

### cosmo_dl_safe.h

**Purpose:** Platform-aware dlopen macros with error handling

**Core Macros:**
```c
// Library loading with platform hints
#define COSMO_DL_LOAD_LIB(handle_var, lib_name, required) do { \
    const char* hints = cosmo_dl_get_hints(lib_name); \
    (handle_var) = cosmo_dlopen_hints(hints); \
    if ((handle_var) == NULL && (required)) { \
        fprintf(stderr, "FATAL: Cannot load %s: %s\n", lib_name, dlerror()); \
        exit(1); \
    } \
} while(0)

// Symbol loading
#define COSMO_DL_LOAD_SYM(handle, sym_ptr, sym_name, required) do { \
    *(void**)&(sym_ptr) = cosmo_dltramp(cosmo_dlsym((handle), (sym_name))); \
    if ((sym_ptr) == NULL && (required)) { \
        fprintf(stderr, "FATAL: Cannot find symbol %s: %s\n", sym_name, dlerror()); \
        exit(1); \
    } \
} while(0)

// Optional symbol (no error on missing)
#define COSMO_DL_LOAD_SYM_OPT(handle, sym_ptr, sym_name) do { \
    *(void**)&(sym_ptr) = cosmo_dltramp(cosmo_dlsym((handle), (sym_name))); \
} while(0)
```

**Platform Hints:**
```c
static const char* cosmo_dl_get_hints(const char* lib_name) {
    if (IsLinux()) {
        if (strcmp(lib_name, "X11") == 0) return "libX11.so.6:libX11.so";
        if (strcmp(lib_name, "GL") == 0) return "libGL.so.1:libGL.so";
        // ...
    } else if (IsMacOS()) {
        if (strcmp(lib_name, "GL") == 0) return "/System/Library/Frameworks/OpenGL.framework/OpenGL";
        // ...
    } else if (IsWindows()) {
        if (strcmp(lib_name, "GL") == 0) return "opengl32.dll";
        // ...
    }
    return lib_name;  // Fallback
}
```

## Success Criteria

- [ ] `check-api-sync.c` compiles with `cosmocc`
- [ ] `check-api-sync` exits 0 with current repo state
- [ ] `validate-sources.c` compiles with `cosmocc`
- [ ] `validate-sources` exits 0 with current repo state
- [ ] `cosmo_dl_safe.h` includes cleanly in x11.c
- [ ] x11.c uses safe macros (no raw dlopen calls)
- [ ] All binaries run on Linux, Windows, macOS

## File Locations

```
C:\cosmo-sokol\
├── tools\
│   ├── check-api-sync.c      # CREATE
│   └── validate-sources.c    # CREATE
└── shims\
    ├── include\
    │   └── cosmo_dl_safe.h   # CREATE
    └── linux\
        └── x11.c             # UPDATE
```

## Dependencies

- **Requires:** cosmocc toolchain (3.9.5 or 3.9.6)
- **Provides to:** seeker (Makefile targets), neteng (CI integration)

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Multi-line parsing fails | Include comment stripping from Round 3 critique |
| Platform detection wrong | Test on all 3 platforms before merge |
| Symbol not wrapped with dltramp | Static analysis / review |

---

*cosmo Plan Complete*
