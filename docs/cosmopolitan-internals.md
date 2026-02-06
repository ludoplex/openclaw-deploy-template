# Cosmopolitan Libc Internals

Deep dive into Cosmopolitan Libc source code (https://github.com/jart/cosmopolitan).
Based on source code analysis, not assumptions.

---

## 1. Fat Binaries & APE Format

### How APE Works

APE (Actually Portable Executable) files are **polyglot binaries** that are simultaneously:

1. **PE** (Windows Portable Executable)
2. **ELF** (Linux/BSD)
3. **Mach-O** (macOS - embedded as printf statements)
4. **Shell script** (Unix bootloader)
5. **BIOS bootable** disk image (optional)

### The Magic Header

From `ape/specification.md`:

```
MZ Magic: "MZqFpD='\n" (hex: 4d 5a 71 46 70 44 3d 27 0a)
```

This is simultaneously:
- Valid MS-DOS MZ header (Windows recognizes it)
- Valid x86 instructions (jumps to PE stub)
- Valid shell variable assignment (Unix shells parse it)

### Multi-Architecture Fat Binaries

Fat binaries embed **multiple ELF headers** as printf statements in the shell script header:

```sh
printf '\177ELF\2\1\1\011...'  # AMD64 ELF header
printf '\177ELF\2\1\1\011...'  # ARM64 ELF header
```

From `ape/loader.c`:
```c
// elf program headers may appear anywhere in the binary
if (READ64(ebuf->buf) == READ64("MZqFpD='") ||
    READ64(ebuf->buf) == READ64("jartsr='") ||
    READ64(ebuf->buf) == READ64("APEDBG='")) {
  for (p = ebuf->buf; p < pe; ++p) {
    if (READ64(p) != READ64("printf '")) {
      continue;
    }
    // Parse octal-encoded ELF header
    // Check e_machine field to select correct architecture
  }
}
```

The `e_machine` field distinguishes architectures:
- `EM_NEXGEN32E` (62) = x86-64/AMD64
- `EM_AARCH64` (183) = ARM64

**Key insight**: The APE loader parses ALL printf statements and selects the one matching the current CPU architecture. No separate binary per platform.

---

## 2. Platform Detection (Runtime vs Compile Time)

### ⚠️ CRITICAL: Platform Detection is RUNTIME, Not Compile Time

We were wrong about needing platform dispatchers. **Cosmopolitan detects the platform at runtime.**

### The `__hostos` Global Variable

From `libc/dce.h`:
```c
extern const int __hostos;

#define _HOSTLINUX   1
#define _HOSTMETAL   2
#define _HOSTWINDOWS 4
#define _HOSTXNU     8
#define _HOSTOPENBSD 16
#define _HOSTFREEBSD 32
#define _HOSTNETBSD  64
```

### Runtime Detection Logic

**On Unix systems** (from `ape/loader.c` - `ApeLoader()`):
```c
// detect freebsd
if (SupportsXnu() && dl == XNU) {
  os = XNU;
} else if (SupportsFreebsd() && di) {
  os = FREEBSD;
  sp = (long *)di;
} else {
  os = 0;
}

// detect openbsd
if (SupportsOpenbsd() && !os && !auxv[0]) {
  os = OPENBSD;
}

// detect netbsd
for (ap = auxv; ap[0]; ap += 2) {
  if (SupportsNetbsd() && !os && ap[0] == AT_EXECFN_NETBSD) {
    os = NETBSD;
  }
}

// the default operating system
if (!os) {
  os = LINUX;
}
```

**On Windows** (from `libc/runtime/winmain.greg.c`):
```c
abi int64_t WinMain(...) {
  extern char os asm("__hostos");
  os = _HOSTWINDOWS;  // Set immediately at entry
  // ...
}
```

**On ARM64/Non-x86** (from `libc/runtime/cosmo2.c`):
```c
if (!(hostos = os)) {
  if (SupportsFreebsd() && is_freebsd) {
    hostos = _HOSTFREEBSD;
  } else if (SupportsXnu() && m1) {
    hostos = _HOSTXNU;
  } else if (SupportsLinux()) {
    hostos = _HOSTLINUX;
  }
}
```

### Compile-Time Support Vector (Dead Code Elimination)

The `SUPPORT_VECTOR` bitmask enables compile-time dead code elimination:

```c
#ifndef SUPPORT_VECTOR
#ifdef __x86_64__
#define SUPPORT_VECTOR 255  // All platforms on x86
#else
#define SUPPORT_VECTOR (_HOSTLINUX | _HOSTXNU | _HOSTFREEBSD)  // Subset on ARM
#endif
#endif
```

### The IsXxx() Macros

These combine compile-time and runtime checks:

```c
#define IsLinux()   (SupportsLinux() && (__hostos & _HOSTLINUX))
#define IsWindows() (SupportsWindows() && (__hostos & _HOSTWINDOWS))
#define IsXnu()     (SupportsXnu() && (__hostos & _HOSTXNU))
// etc.
```

**How it works:**
1. `SupportsLinux()` is a compile-time check (can eliminate dead code)
2. `__hostos & _HOSTLINUX` is a runtime check (actual detection)

---

## 3. OpenGL/Graphics Support

### ⚠️ There Is NO Native OpenGL Support in Cosmopolitan

Looking at `examples/`:
- `gui.c` - **Windows-only**, uses raw Win32 API (not portable!)
- `asteroids.c` - Terminal-based graphics (ANSI escape codes)
- `nesemu1.cc` - Terminal-based NES emulator (dsp/tty)
- `vga.c` - Bare metal VGA text mode (BIOS boot only)

From `examples/gui.c`:
```c
int main(int argc, char *argv[]) {
  if (!IsWindows()) {
    fputs("Sorry! This GUI demo only runs on Windows\n", stderr);
    return 1;
  }
  Gui();  // Win32 API calls
}
```

### The `cosmo_dlopen()` Approach

From `ape/specification.md`:
> Cosmopolitan Libc provides a solution that enables APE binaries have
> limited access to dlopen(). By manually loading a platform-specific
> executable and asking the OS-specific libc's dlopen() to load
> OS-specific libraries, it becomes possible to use GPUs and GUIs.
> **This has worked great for AI projects like llamafile.**

From `libc/dlopen/dlopen.c`:
```c
/**
 * @fileoverview Cosmopolitan Dynamic Linker.
 *
 * Every program built using Cosmopolitan is statically-linked. However
 * there are some cases, e.g. GUIs and video drivers, where linking the
 * host platform libraries is desirable. So what we do in such cases is
 * launch a stub executable using the host platform's libc, and longjmp
 * back into this executable.
 */
```

### How `cosmo_dlopen()` Works

1. **First call**: Compiles a tiny C helper using the host's native `cc`:
```c
#define HELPER \
  "#include <dlfcn.h>\n\
   int main(int argc, char **argv, char **envp) {\n\
     return ((int (*)(void *))addr)((void *[]){\n\
       dlopen, dlsym, dlclose, dlerror,\n\
     });\n\
   }\n"
```

2. **Loads helper**: The helper returns pointers to the host's dlopen/dlsym
3. **Thunking**: Wraps foreign functions with ABI translation (System V ↔ MS x64)

From `cosmo_dlopen()`:
```c
void *cosmo_dlopen(const char *path, int mode) {
  if (IsWindows()) {
    res = dlopen_nt(path, mode);  // LoadLibrary()
  } else if (IsXnuSilicon()) {
    res = dlopen_silicon(path, mode);  // Direct via __syslib
  } else if (IsXnu()) {
    dlerror_set("dlopen() isn't supported on x86-64 MacOS");
  } else if (foreign_init()) {
    res = __foreign.dlopen(path, mode);  // Via helper
  }
}
```

### Path Normalization

`cosmo_dlopen()` automatically converts `.so` extensions:
- Windows: `.so` → `.dll`
- macOS: `.so` → `.dylib`

---

## 4. Sokol/GUI in Cosmopolitan

### There Are NO Sokol Examples in the Repo

Searched entire codebase - no Sokol, no SDL, no OpenGL code.

### Correct Approach for Sokol + Cosmo

Based on the codebase analysis, the correct architecture is:

#### Option A: Platform Helpers (llamafile approach)

```
┌─────────────────────────────────────────────┐
│  APE Binary (main app, static linked)       │
├─────────────────────────────────────────────┤
│  cosmo_dlopen("libgui.so", RTLD_NOW)        │
│  → Windows: loads libgui.dll                │
│  → Linux: loads libgui.so                   │
│  → macOS: loads libgui.dylib                │
├─────────────────────────────────────────────┤
│  Platform Helper (built with native cc)     │
│  - Sokol implementation                     │
│  - Links native OpenGL/Vulkan/Metal         │
│  - Exports C interface                      │
└─────────────────────────────────────────────┘
```

Build process:
1. Build main APE binary with cosmocc
2. Build platform-specific helpers with native toolchains:
   - Linux: `cc -shared -o libgui.so gui_linux.c -lGL -lX11`
   - Windows: `cl /LD gui_win.c opengl32.lib`
   - macOS: `cc -dynamiclib -o libgui.dylib gui_mac.m -framework Metal`

#### Option B: Software Rendering Only

Use Sokol's `sokol_gfx.h` with a software backend (if available), render to buffer, and display via terminal/framebuffer. Limited but truly portable.

---

## 5. Key Architectural Insights

### What We Got Wrong

1. **No platform dispatchers needed** - `__hostos` is set at runtime
2. **No compile-time branching** - The same code runs on all platforms
3. **No OpenGL polyfill** - Must use cosmo_dlopen() for GPU

### What Cosmopolitan Does Provide

1. **Unified binary** - One file runs everywhere
2. **POSIX polyfill** - `read()`, `write()`, `mmap()` work everywhere
3. **Runtime detection** - `IsLinux()`, `IsWindows()` for branching
4. **Dynamic loading** - `cosmo_dlopen()` for platform libraries

### The "One Binary" Philosophy

From the specification:
> There is no way for an Actually Portable Executable to interact with
> OS-specific dynamic shared object extension modules to programming
> languages. [...] This is primarily because different OSes define
> incompatible ABIs.

But `cosmo_dlopen()` provides an escape hatch for GPU/GUI when needed.

---

## 6. Practical Implications for Our Project

### For mhi-procurement (CImGui + Sokol + SQLite)

The correct architecture is:

```c
// main.c - Built with cosmocc

#include "libc/dlopen/dlfcn.h"
#include "libc/dce.h"

// Define function pointer types
typedef void (*gui_init_fn)(void);
typedef void (*gui_frame_fn)(void);

int main() {
    // Load platform-specific GUI module
    void *gui = cosmo_dlopen("libgui", RTLD_NOW);
    if (!gui) {
        fprintf(stderr, "GUI not available: %s\n", cosmo_dlerror());
        return 1;
    }
    
    gui_init_fn init = cosmo_dltramp(cosmo_dlsym(gui, "gui_init"));
    gui_frame_fn frame = cosmo_dltramp(cosmo_dlsym(gui, "gui_frame"));
    
    init();
    while (running) {
        frame();
    }
    
    cosmo_dlclose(gui);
    return 0;
}
```

Platform helpers (built separately):
```c
// gui_linux.c - Built with gcc
#define SOKOL_IMPL
#define SOKOL_GLCORE
#include "sokol_app.h"
#include "sokol_gfx.h"

__attribute__((visibility("default")))
void gui_init(void) { /* ... */ }

__attribute__((visibility("default")))
void gui_frame(void) { /* ... */ }
```

### Alternative: Terminal UI

For maximum portability without helpers, use terminal-based rendering like nesemu1.cc does with `dsp/tty/tty.h`.

---

## Summary

| Feature | How Cosmopolitan Handles It |
|---------|---------------------------|
| Multi-OS binary | APE polyglot format |
| Multi-arch binary | Multiple ELF headers in printf statements |
| Platform detection | `__hostos` global set at runtime |
| POSIX API | Polyfilled across all platforms |
| OpenGL/GPU | `cosmo_dlopen()` + platform helpers |
| GUI | `cosmo_dlopen()` or native API (not portable) |
| Sokol | Not included - must build as separate helpers |

**The key insight**: Cosmopolitan handles portability at runtime, not compile time. The same code runs everywhere, with `IsLinux()` etc. for conditional behavior. For GPU/GUI, you MUST use the dlopen approach.
