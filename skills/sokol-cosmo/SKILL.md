# cosmo-sokol Integration (NOT raw Sokol!)

## ⚠️ CRITICAL DISTINCTION

| Term | Meaning |
|------|---------|
| **sokol** | Raw sokol library. Uses compile-time `#ifdef` for platform selection. NOT directly usable with Cosmopolitan. |
| **cosmo-sokol** | The bullno1 pattern for Cosmopolitan. ALL backends compiled INTO the APE with prefixes. Runtime dispatch. NO separate helpers. |

**When building for Cosmopolitan APE, you MUST use the cosmo-sokol pattern, NOT raw sokol.**

## The cosmo-sokol Pattern (bullno1/cosmo-sokol)

Reference: https://github.com/bullno1/cosmo-sokol

### How It Works

1. **Compile ALL platform backends INTO the APE** (not ifdef, not separate files)
2. **Prefix trick** to avoid symbol collisions:
   ```c
   // Before including sokol_app.h for Linux:
   #define sapp_show_keyboard linux_sapp_show_keyboard
   #define sapp_run linux_sapp_run
   // ... all public functions
   
   // Before including for Windows:
   #define sapp_show_keyboard windows_sapp_show_keyboard
   #define sapp_run windows_sapp_run
   ```
3. **Runtime dispatch shim** (`sokol_cosmo.c`) selects the correct implementation:
   ```c
   void sapp_run(const sapp_desc* desc) {
       if (IsWindows()) {
           windows_sapp_run(desc);
       } else if (IsXnu()) {
           macos_sapp_run(desc);
       } else {
           linux_sapp_run(desc);
       }
   }
   ```
4. **System libraries loaded via dlopen** — X11, OpenGL, etc. are dynamically loaded from the HOST system
5. **ONE APE BINARY** — everything is compiled in, no separate helper files

### What Gets dlopen'd

The APE uses dlopen for **SYSTEM libraries only**:
- Linux: `libX11.so`, `libGL.so`, `libXi.so`, `libXcursor.so`
- Windows: Uses Cosmopolitan's NT import mechanism
- macOS: Framework loading

**NOT** for our own code. Sokol code lives IN the APE.

## Anti-Patterns (DO NOT DO)

### ❌ WRONG: Separate helper DSOs (llamafile pattern misapplied)
```
# This is WRONG for cosmo-sokol:
myapp.com
libgui.so      # NO!
libgui.dll     # NO!
libgui.dylib   # NO!
```
The llamafile pattern (extract DSO from /zip/) is for GPU backends like CUDA/Metal compute — NOT for sokol GUI code.

### ❌ WRONG: Raw sokol with cosmocc
```bash
# This will NOT work — sokol uses compile-time ifdefs
cosmocc -o myapp.com main.c sokol_app.c sokol_gfx.c
```

### ❌ WRONG: Thinking Cosmopolitan has OpenGL
```c
// Cosmopolitan has NO native graphics!
// You MUST dlopen system graphics libraries
```

## Correct Build Process

### 1. Generate prefixed headers and shims
Use bullno1's generator scripts:
- `gen-sokol` — generates #define prefixes and cosmo shim
- `gen-x11` — generates X11 function stubs for dlopen
- `gen-gl` — generates OpenGL function stubs for dlopen

### 2. Compile each platform backend with prefixes
```bash
# Linux backend (with linux_ prefix)
cosmocc -c -DLINUX_BUILD sokol_linux.c -o sokol_linux.o

# Windows backend (with windows_ prefix)  
cosmocc -c -DWINDOWS_BUILD sokol_windows.c -o sokol_windows.o

# macOS backend (with macos_ prefix)
cosmocc -c -DMACOS_BUILD sokol_macos.c -o sokol_macos.o
```

### 3. Compile the runtime dispatch shim
```bash
cosmocc -c sokol_cosmo.c -o sokol_cosmo.o
```

### 4. Link everything into ONE APE
```bash
cosmocc -o myapp.com main.o sokol_linux.o sokol_windows.o sokol_macos.o sokol_cosmo.o
```

### 5. Result: Single APE with all backends
```
myapp.com  # Contains Linux, Windows, macOS sokol code
           # Runtime dispatch picks the right one
           # dlopen loads system X11/GL/etc.
```

## Key Facts

1. **Everything is in the APE** — no separate helper files to distribute
2. **Prefix trick prevents collisions** — `linux_sapp_run` vs `windows_sapp_run`
3. **Runtime dispatch** — `sokol_cosmo.c` checks `IsWindows()`, `IsLinux()`, etc.
4. **System libs via dlopen** — X11, OpenGL come from the host system
5. **cosmo-sokol ≠ sokol** — don't confuse them

## When to Use This

- GUI applications with Cosmopolitan APE
- Games or visualization tools
- Any APE that needs graphics

## When NOT to Use This

- CLI tools (just use cosmocc directly)
- Terminal UI (use ncurses)
- Server applications

## llamafile Pattern vs cosmo-sokol

| Aspect | llamafile (CUDA/Metal compute) | cosmo-sokol (GUI) |
|--------|-------------------------------|-------------------|
| What's in APE | Stub + embedded DSO in /zip/ | ALL platform code compiled in |
| What's extracted | GPU compute library | Nothing |
| What's dlopen'd | Extracted DSO from app cache | System libs (X11, GL) |
| Use case | GPU compute acceleration | Cross-platform GUI |

**Do NOT mix these patterns.** cosmo-sokol does NOT use the /zip/ extraction pattern.

## References

- **bullno1/cosmo-sokol**: https://github.com/bullno1/cosmo-sokol
- Generator scripts in that repo: `gen-sokol`, `gen-x11`, `gen-gl`
- Cosmopolitan docs: https://github.com/jart/cosmopolitan
