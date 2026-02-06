# Sokol + Cosmopolitan Integration

Use when building GUI/graphics applications with Sokol (or similar) that need to run as Cosmopolitan APE binaries.

## Core Truth

**Cosmopolitan has NO native OpenGL/GPU support.** For graphics, you MUST use `cosmo_dlopen()` to load platform-native libraries.

**APE binaries use PKZIP format** for embedded assets. Files in `/zip/...` are accessible via standard file I/O.

## llamafile's Pattern (THE REFERENCE IMPLEMENTATION)

From `llamafile/cuda.c` — this is exactly how GPU support works:

```c
// 1. Pre-built DSOs embedded in /zip/
static bool extract_cuda_dso(const char *dso, const char *name) {
    char zip[80];
    strlcpy(zip, "/zip/", sizeof(zip));
    strlcat(zip, name, sizeof(zip));
    strlcat(zip, ".", sizeof(zip));
    strlcat(zip, GetDsoExtension(), sizeof(zip));  // .so/.dll/.dylib
    
    if (!FileExists(zip))
        return false;
    
    // Extract to app directory (persistent, cached)
    return llamafile_extract(zip, dso);
}

// 2. Load extracted library via cosmo_dlopen
static bool link_cuda_dso(const char *dso, const char *dir) {
    void *lib = cosmo_dlopen(dso, RTLD_LAZY);
    if (!lib) return false;
    
    // Import functions via cosmo_dlsym
    ggml_cuda.buffer_type = cosmo_dlsym(lib, "ggml_backend_cuda_buffer_type");
    // ...
}
```

**Why extraction is required:** OS dynamic linker (ld.so, LoadLibrary) cannot read from APE's `/zip/` virtual filesystem. Libraries must exist on real filesystem for the OS to load them.

## The Correct Architecture

```
┌─────────────────────────────────────────────┐
│  APE Binary (single file, PKZIP format)       │
│  Contains:                                  │
│    - Main executable code                   │
│    - /zip/libgui.so (Linux helper)         │
│    - /zip/libgui.dll (Windows helper)      │
│    - /zip/libgui.dylib (macOS helper)      │
├─────────────────────────────────────────────┤
│  At runtime:                                │
│  1. Detect platform via IsWindows() etc.   │
│  2. Extract correct helper to app dir      │
│  3. cosmo_dlopen() the extracted file      │
│  4. Import functions via cosmo_dlsym()     │
└─────────────────────────────────────────────┘
```

**ONE FILE. Runs everywhere. GUI included.**

## Build Process

### 1. Main APE Binary (cosmocc)
```bash
cosmocc -o myapp.com main.c database.c -lsqlite3
```

### 2. Platform Helpers (native toolchains)
```bash
# Linux
gcc -shared -fPIC -o libgui.so gui_impl.c -lGL -lX11

# Windows  
cl /LD gui_impl.c opengl32.lib user32.lib gdi32.lib /Fe:libgui.dll

# macOS
clang -dynamiclib -o libgui.dylib gui_impl.m -framework Metal -framework Cocoa
```

### 3. Bundle Helpers INTO the APE
```bash
# APE uses PKZIP format — just append the helpers
zip -j myapp.com libgui.so libgui.dll libgui.dylib
```

### 4. Runtime: Extract and Load
```c
#include <cosmo.h>
#include <dlfcn.h>
#include <sys/stat.h>

// Get app directory (persistent, not temp)
static void get_app_dir(char *buf, size_t size) {
    if (IsWindows()) {
        snprintf(buf, size, "%s/.myapp/", getenv("LOCALAPPDATA"));
    } else {
        snprintf(buf, size, "%s/.myapp/", getenv("HOME"));
    }
    mkdir(buf, 0755);
}

// Extract from /zip/ to app directory
static bool extract_helper(const char *zip_path, const char *out_path) {
    int src = open(zip_path, O_RDONLY);
    if (src < 0) return false;
    
    int dst = open(out_path, O_WRONLY|O_CREAT|O_TRUNC, 0755);
    if (dst < 0) { close(src); return false; }
    
    char buf[32768];
    ssize_t n;
    while ((n = read(src, buf, sizeof(buf))) > 0)
        write(dst, buf, n);
    
    close(src);
    close(dst);
    return true;
}

void* load_gui_helper(void) {
    // Determine correct helper
    const char *zip_name;
    const char *ext;
    if (IsWindows()) { zip_name = "libgui.dll"; ext = ".dll"; }
    else if (IsXnu()) { zip_name = "libgui.dylib"; ext = ".dylib"; }
    else { zip_name = "libgui.so"; ext = ".so"; }
    
    // Build paths
    char zip_path[PATH_MAX], out_path[PATH_MAX], app_dir[PATH_MAX];
    get_app_dir(app_dir, sizeof(app_dir));
    snprintf(zip_path, sizeof(zip_path), "/zip/%s", zip_name);
    snprintf(out_path, sizeof(out_path), "%slibgui%s", app_dir, ext);
    
    // Extract if needed (check mtime for caching)
    struct stat zst, ost;
    if (stat(out_path, &ost) || stat(zip_path, &zst) || zst.st_mtime > ost.st_mtime) {
        if (!extract_helper(zip_path, out_path)) {
            fprintf(stderr, "Failed to extract GUI helper\n");
            return NULL;
        }
    }
    
    // Load via cosmo_dlopen
    return cosmo_dlopen(out_path, RTLD_NOW);
}
```

## Anti-Patterns (DO NOT DO)

### ❌ Shipping helpers as separate files
```bash
# WRONG - defeats the purpose of APE single-file distribution
myapp.com
libgui.so
libgui.dll
libgui.dylib
```

### ❌ Static linking Sokol with cosmocc
```c
// WRONG - Cosmopolitan has no OpenGL!
cosmocc -o myapp.com main.c sokol.c  
```

### ❌ Platform dispatchers on top of Sokol
```c
// WRONG - Sokol already handles this at compile time
void my_gl_init() {
    if (IsWindows()) { windows_gl_init(); }
    else if (IsLinux()) { linux_gl_init(); }
}
```

### ❌ Worrying about symbol collision in Sokol
```c
// UNNECESSARY - all Sokol internals are static
// No _sapp_* or _sg_* symbols are exported
```

### ❌ Extracting to temp directory
```c
// WRONG - use persistent app directory for caching
// Temp = re-extract every run = slow startup
char tmp[PATH_MAX];
snprintf(tmp, sizeof(tmp), "/tmp/libgui.so");  // BAD
```

## Key Facts About Sokol

1. **All internal functions are `static`** — no symbol collision possible
2. **Platform detection is compile-time** via `#ifdef _WIN32`, `__linux__`, etc.
3. **Built-in GL loader for Windows** — no GLEW/GLAD needed
4. **Single translation unit design** — one .c file includes all headers with `SOKOL_IMPL`

## Key Facts About Cosmopolitan

1. **Platform detection is runtime** via `__hostos` global and `IsWindows()`, `IsLinux()`, etc.
2. **NO native OpenGL/graphics** — examples are Windows-only or terminal-based
3. **APE uses PKZIP format** for embedded assets, accessible via `/zip/...` paths
4. **`cosmo_dlopen()` requires extraction** — OS loader can't read from `/zip/`
5. **Fat binaries** = multiple ELF headers for different CPU architectures (x86_64, aarch64)

## When to Use This Pattern

- GUI applications that need to be truly portable
- Games or visualization tools
- Any APE binary that needs GPU access

## When NOT to Use This Pattern

- CLI tools (just use cosmocc directly)
- Terminal UI apps (use ncurses or raw ANSI)
- Server applications (no GUI needed)

## References

- **llamafile source** — `llamafile/cuda.c` shows the production pattern
- Full analysis: `docs/cosmopolitan-internals.md`
- Sokol deep dive: `docs/sokol-internals.md`
- Build patterns: `docs/sokol-cosmo-build-patterns.md`
- Test patterns: `docs/sokol-cosmo-testing.md`
- Examples: `docs/sokol-examples-review.md`
