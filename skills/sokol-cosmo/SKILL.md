# Sokol + Cosmopolitan Integration

Use when building GUI/graphics applications with Sokol (or similar) that need to run as Cosmopolitan APE binaries.

## Core Truth

**Cosmopolitan has NO native OpenGL/GPU support.** For graphics, you MUST use `cosmo_dlopen()` to load platform-native libraries at runtime.

This is how llamafile accesses GPUs.

## The Correct Architecture

```
┌─────────────────────────────────────────────┐
│  APE Binary (single file, ZIP container)    │
│  - Business logic, CLI, database            │
│  - Embedded: libgui.so, libgui.dll, .dylib  │
│  - Extracts correct helper at runtime       │
│  - Calls cosmo_dlopen() on extracted file   │
└─────────────────────────────────────────────┘
```

**APE binaries are ZIP archives.** Embed all platform helpers inside. One file runs everywhere with full GUI.

This is how **llamafile embeds model weights** — same pattern works for helper libraries.

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
# APE is a ZIP — just append the helpers
zip -j myapp.com libgui.so libgui.dll libgui.dylib
```

### 4. Runtime Extraction
```c
#include "libc/zip.h"
#include "libc/runtime/runtime.h"

void* load_embedded_gui(void) {
    const char* zip_path;
    if (IsWindows()) zip_path = "/zip/libgui.dll";
    else if (IsXnu()) zip_path = "/zip/libgui.dylib";
    else zip_path = "/zip/libgui.so";
    
    // Extract to temp
    char tmp[PATH_MAX];
    snprintf(tmp, sizeof(tmp), "%s/libgui%s", 
             IsWindows() ? getenv("TEMP") : "/tmp",
             IsWindows() ? ".dll" : IsXnu() ? ".dylib" : ".so");
    
    // Copy from /zip/ to temp filesystem
    int src = open(zip_path, O_RDONLY);
    int dst = open(tmp, O_WRONLY|O_CREAT|O_TRUNC, 0755);
    // ... copy bytes ...
    close(src); close(dst);
    
    return cosmo_dlopen(tmp, RTLD_NOW);
}
```

### 5. Distribution
**ONE FILE.** Runs everywhere. GUI included. No separate helper downloads.

## Code Template

### main.c (APE binary)
```c
#include "libc/dlopen/dlfcn.h"

typedef void (*gui_init_fn)(int width, int height, const char* title);
typedef bool (*gui_frame_fn)(void);
typedef void (*gui_shutdown_fn)(void);

int main(int argc, char** argv) {
    void* gui = cosmo_dlopen("libgui", RTLD_NOW);
    if (!gui) {
        // Fall back to CLI mode
        return cli_main(argc, argv);
    }
    
    gui_init_fn init = cosmo_dltramp(cosmo_dlsym(gui, "gui_init"));
    gui_frame_fn frame = cosmo_dltramp(cosmo_dlsym(gui, "gui_frame"));
    gui_shutdown_fn shutdown = cosmo_dltramp(cosmo_dlsym(gui, "gui_shutdown"));
    
    init(1280, 720, "My App");
    while (frame()) { }
    shutdown();
    
    cosmo_dlclose(gui);
    return 0;
}
```

### gui_impl.c (platform helper)
```c
#define SOKOL_IMPL
#define SOKOL_GLCORE  // or SOKOL_D3D11, SOKOL_METAL
#include "sokol_app.h"
#include "sokol_gfx.h"
#include "sokol_imgui.h"

// Export with visibility
#if defined(_WIN32)
  #define EXPORT __declspec(dllexport)
#else
  #define EXPORT __attribute__((visibility("default")))
#endif

EXPORT void gui_init(int width, int height, const char* title) {
    // Sokol setup
}

EXPORT bool gui_frame(void) {
    // Render frame, return false to quit
}

EXPORT void gui_shutdown(void) {
    // Cleanup
}
```

## Anti-Patterns (DO NOT DO)

### ❌ Shipping helpers as separate files
```bash
# WRONG - APE is a ZIP container, embed them!
myapp.com
libgui.so
libgui.dll
libgui.dylib
```
**The whole point of APE is single-file distribution. Use it.**

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

### ❌ Multiple sokol_*.c files with different backends
```c
// WRONG - causes symbol duplication
// sokol_windows.c with SOKOL_D3D11
// sokol_linux.c with SOKOL_GLCORE
// sokol_cosmo.c trying to dispatch between them
```

### ❌ Worrying about symbol collision
```c
// UNNECESSARY - all Sokol internals are static
// No _sapp_* or _sg_* symbols are exported
```

## Key Facts About Sokol

1. **All internal functions are `static`** — no symbol collision possible
2. **Platform detection is compile-time** via `#ifdef _WIN32`, `__linux__`, etc.
3. **Built-in GL loader for Windows** — no GLEW/GLAD needed
4. **Single translation unit design** — one .c file includes all headers with `SOKOL_IMPL`

## Key Facts About Cosmopolitan

1. **Platform detection is runtime** via `__hostos` global
2. **NO native OpenGL/graphics** — examples are Windows-only or terminal-based
3. **`cosmo_dlopen()` is the escape hatch** — compiles a tiny native helper at runtime
4. **Fat binaries = multiple ELF headers** — CPU arch selection, not platform dispatch

## When to Use This Pattern

- GUI applications that need to be truly portable
- Games or visualization tools
- Any APE binary that needs GPU access

## When NOT to Use This Pattern

- CLI tools (just use cosmocc directly)
- Terminal UI apps (use ncurses or raw ANSI)
- Server applications (no GUI needed)

## References

- Full analysis: `docs/cosmopolitan-internals.md`
- Sokol deep dive: `docs/sokol-internals.md`
- Build patterns: `docs/sokol-cosmo-build-patterns.md`
- Test patterns: `docs/sokol-cosmo-testing.md`
- Examples: `docs/sokol-examples-review.md`
