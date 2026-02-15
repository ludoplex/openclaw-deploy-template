# Triad Solutions — cosmo-sokol-v4 Round 1

**Phase:** Triad Phase 3 — Solutions  
**Generated:** 2026-02-09T19:25:00-07:00  
**Project Philosophy:** NO Python. ALL tooling must be C compiled with cosmocc into APE binaries.

---

## Executive Summary

Three critical issues were identified. All have straightforward solutions. The line number inaccuracy across all specialist reports reveals a systemic problem in how we generate manifests — this is fixable with proper tooling.

**Minimum viable path:** Fix GLX shim (showstopper) → Add dispatch fallback (safety) → Replace gen-sokol (philosophy). In that order.

---

## 🔧 Solution 1: GLX Shim — SHOWSTOPPER FIX

### Problem

Linux builds crash because `shims/linux/gl.c` provides core OpenGL functions but **not GLX context management functions**. Sokol on Linux X11 requires GLX to create an OpenGL context before any GL calls can work.

### Solution: Create `shims/linux/glx.c`

GLX functions are exported from the same `libGL.so.1` as core GL functions. Create a new file with the GLX shims:

```c
// shims/linux/glx.c — GLX Context Management Shim

#include <libc/dlopen/dlfcn.h>

// GLX types (from glx.h)
typedef struct __GLXcontextRec *GLXContext;
typedef struct __GLXFBConfigRec *GLXFBConfig;
typedef XID GLXDrawable;
typedef XID GLXWindow;
typedef XID GLXPixmap;

// Function pointers
static GLXContext (*proc_glXCreateContext)(Display*, XVisualInfo*, GLXContext, Bool);
static Bool (*proc_glXMakeCurrent)(Display*, GLXDrawable, GLXContext);
static void (*proc_glXSwapBuffers)(Display*, GLXDrawable);
static void (*proc_glXDestroyContext)(Display*, GLXContext);
static void* (*proc_glXGetProcAddress)(const GLubyte*);
static void* (*proc_glXGetProcAddressARB)(const GLubyte*);
static XVisualInfo* (*proc_glXChooseVisual)(Display*, int, int*);
static GLXFBConfig* (*proc_glXChooseFBConfig)(Display*, int, const int*, int*);
static GLXContext (*proc_glXCreateNewContext)(Display*, GLXFBConfig, int, GLXContext, Bool);
static GLXContext (*proc_glXGetCurrentContext)(void);
static GLXDrawable (*proc_glXGetCurrentDrawable)(void);
static Bool (*proc_glXQueryExtension)(Display*, int*, int*);
static Bool (*proc_glXQueryVersion)(Display*, int*, int*);
static int (*proc_glXGetConfig)(Display*, XVisualInfo*, int, int*);
static XVisualInfo* (*proc_glXGetVisualFromFBConfig)(Display*, GLXFBConfig);
static int (*proc_glXGetFBConfigAttrib)(Display*, GLXFBConfig, int, int*);
static GLXWindow (*proc_glXCreateWindow)(Display*, GLXFBConfig, Window, const int*);
static void (*proc_glXDestroyWindow)(Display*, GLXWindow);

static void *libGL;

void load_GLX_procs(void) {
    if (libGL) return;
    libGL = cosmo_dlopen("libGL.so.1", RTLD_LAZY);
    if (!libGL) return;
    
    proc_glXCreateContext = cosmo_dltramp(cosmo_dlsym(libGL, "glXCreateContext"));
    proc_glXMakeCurrent = cosmo_dltramp(cosmo_dlsym(libGL, "glXMakeCurrent"));
    proc_glXSwapBuffers = cosmo_dltramp(cosmo_dlsym(libGL, "glXSwapBuffers"));
    proc_glXDestroyContext = cosmo_dltramp(cosmo_dlsym(libGL, "glXDestroyContext"));
    proc_glXGetProcAddress = cosmo_dltramp(cosmo_dlsym(libGL, "glXGetProcAddress"));
    proc_glXGetProcAddressARB = cosmo_dltramp(cosmo_dlsym(libGL, "glXGetProcAddressARB"));
    proc_glXChooseVisual = cosmo_dltramp(cosmo_dlsym(libGL, "glXChooseVisual"));
    proc_glXChooseFBConfig = cosmo_dltramp(cosmo_dlsym(libGL, "glXChooseFBConfig"));
    proc_glXCreateNewContext = cosmo_dltramp(cosmo_dlsym(libGL, "glXCreateNewContext"));
    proc_glXGetCurrentContext = cosmo_dltramp(cosmo_dlsym(libGL, "glXGetCurrentContext"));
    proc_glXGetCurrentDrawable = cosmo_dltramp(cosmo_dlsym(libGL, "glXGetCurrentDrawable"));
    proc_glXQueryExtension = cosmo_dltramp(cosmo_dlsym(libGL, "glXQueryExtension"));
    proc_glXQueryVersion = cosmo_dltramp(cosmo_dlsym(libGL, "glXQueryVersion"));
    proc_glXGetConfig = cosmo_dltramp(cosmo_dlsym(libGL, "glXGetConfig"));
    proc_glXGetVisualFromFBConfig = cosmo_dltramp(cosmo_dlsym(libGL, "glXGetVisualFromFBConfig"));
    proc_glXGetFBConfigAttrib = cosmo_dltramp(cosmo_dlsym(libGL, "glXGetFBConfigAttrib"));
    proc_glXCreateWindow = cosmo_dltramp(cosmo_dlsym(libGL, "glXCreateWindow"));
    proc_glXDestroyWindow = cosmo_dltramp(cosmo_dlsym(libGL, "glXDestroyWindow"));
}

// Wrapper functions
GLXContext glXCreateContext(Display* dpy, XVisualInfo* vis, GLXContext share, Bool direct) {
    return proc_glXCreateContext(dpy, vis, share, direct);
}

Bool glXMakeCurrent(Display* dpy, GLXDrawable drawable, GLXContext ctx) {
    return proc_glXMakeCurrent(dpy, drawable, ctx);
}

void glXSwapBuffers(Display* dpy, GLXDrawable drawable) {
    proc_glXSwapBuffers(dpy, drawable);
}

// ... (remaining wrapper functions follow same pattern)
```

### Integration

Add `#include "glx.c"` to the Linux build, or link separately. Call `load_GLX_procs()` during X11 initialization, after X11 is loaded but before any GL context creation.

### Effort: ~2 hours

---

## 🔧 Solution 2: Dispatch Fallback — SAFETY FIX

### Problem

Every dispatch function in `sokol_cosmo.c` has no fallback for unsupported platforms:

```c
bool sapp_isvalid(void) {
    if (IsLinux()) { return linux_sapp_isvalid(); }
    if (IsWindows()) { return windows_sapp_isvalid(); }
    if (IsXnu()) { return macos_sapp_isvalid(); }
    // FALLS THROUGH WITH UNDEFINED RETURN VALUE!
}
```

The `#pragma GCC diagnostic ignored "-Wreturn-type"` hides this bug.

### Solution: Add Platform Assert + Abort

Two options, in order of preference:

**Option A: Static Assert Pattern (Compile-time safe)**

Won't work here because platform detection is runtime. Skip.

**Option B: Runtime Abort with Clear Message**

```c
#include <stdio.h>
#include <stdlib.h>

#define UNSUPPORTED_PLATFORM() do { \
    fprintf(stderr, "FATAL: Unsupported platform in %s\n", __func__); \
    fprintf(stderr, "cosmo-sokol supports: Linux, Windows, macOS\n"); \
    abort(); \
} while(0)

bool sapp_isvalid(void) {
    if (IsLinux()) { return linux_sapp_isvalid(); }
    if (IsWindows()) { return windows_sapp_isvalid(); }
    if (IsXnu()) { return macos_sapp_isvalid(); }
    UNSUPPORTED_PLATFORM();
}
```

**Option C: __builtin_unreachable() (Minimal)**

If you're confident the three platforms are exhaustive:

```c
bool sapp_isvalid(void) {
    if (IsLinux()) { return linux_sapp_isvalid(); }
    if (IsWindows()) { return windows_sapp_isvalid(); }
    if (IsXnu()) { return macos_sapp_isvalid(); }
    __builtin_unreachable();  // Tell compiler this path is impossible
}
```

**Recommendation:** Use Option B. It fails loudly and explains why. `__builtin_unreachable()` is dangerous — if someone runs on FreeBSD, it causes undefined behavior instead of a helpful crash.

### Implementation

Update the code generator (see Solution 3) to emit `UNSUPPORTED_PLATFORM()` at the end of every dispatch function.

### Effort: 30 minutes (manual) or 0 (if baked into new code generator)

---

## 🔧 Solution 3: Replace Python gen-sokol — PHILOSOPHY FIX

### Problem

`shims/sokol/gen-sokol` is a 280-line Python script. This violates the core project philosophy: **NO interpreters. ALL tooling must be C/APE.**

### Solution: Write C Code Generator

A simple C program that:
1. Reads a list of sokol function signatures (from a `.txt` file or parsed from headers)
2. Outputs `sokol_cosmo.c` with dispatch functions
3. Optionally outputs platform-specific header macros

### Design: gen-sokol.c (~250 lines)

```c
// tools/gen-sokol.c — Sokol Dispatch Code Generator
// Compile: cosmocc -o gen-sokol.com gen-sokol.c

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function signature struct
typedef struct {
    const char *return_type;
    const char *name;
    const char *params;      // e.g., "int x, float y"
    const char *call_args;   // e.g., "x, y"
} SokolFunc;

// Hardcoded function list (or parse from file)
static const SokolFunc funcs[] = {
    {"bool", "sapp_isvalid", "void", ""},
    {"int", "sapp_width", "void", ""},
    {"int", "sapp_height", "void", ""},
    {"float", "sapp_widthf", "void", ""},
    {"float", "sapp_heightf", "void", ""},
    {"int", "sapp_color_format", "void", ""},
    {"int", "sapp_depth_format", "void", ""},
    {"int", "sapp_sample_count", "void", ""},
    {"bool", "sapp_high_dpi", "void", ""},
    {"float", "sapp_dpi_scale", "void", ""},
    {"void", "sapp_show_keyboard", "bool show", "show"},
    {"bool", "sapp_keyboard_shown", "void", ""},
    {"bool", "sapp_is_fullscreen", "void", ""},
    {"void", "sapp_toggle_fullscreen", "void", ""},
    {"void", "sapp_show_mouse", "bool show", "show"},
    {"bool", "sapp_mouse_shown", "void", ""},
    {"void", "sapp_request_quit", "void", ""},
    {"void", "sapp_cancel_quit", "void", ""},
    {"void", "sapp_quit", "void", ""},
    // ... add remaining ~100 functions
    {NULL, NULL, NULL, NULL}  // Sentinel
};

static void emit_header(FILE *out) {
    fprintf(out, "// sokol_cosmo.c — Auto-generated dispatch layer\n");
    fprintf(out, "// Generated by gen-sokol.com — DO NOT EDIT\n\n");
    fprintf(out, "#include <stdio.h>\n");
    fprintf(out, "#include <stdlib.h>\n");
    fprintf(out, "#include <libc/runtime/runtime.h>  // IsLinux(), etc.\n\n");
    fprintf(out, "#define UNSUPPORTED_PLATFORM() do { \\\n");
    fprintf(out, "    fprintf(stderr, \"FATAL: Unsupported platform in %%s\\n\", __func__); \\\n");
    fprintf(out, "    abort(); \\\n");
    fprintf(out, "} while(0)\n\n");
}

static void emit_function(FILE *out, const SokolFunc *f) {
    fprintf(out, "%s %s(%s) {\n", f->return_type, f->name, f->params);
    
    // Linux
    fprintf(out, "    if (IsLinux()) { ");
    if (strcmp(f->return_type, "void") == 0) {
        fprintf(out, "linux_%s(%s); return; ", f->name, f->call_args);
    } else {
        fprintf(out, "return linux_%s(%s); ", f->name, f->call_args);
    }
    fprintf(out, "}\n");
    
    // Windows
    fprintf(out, "    if (IsWindows()) { ");
    if (strcmp(f->return_type, "void") == 0) {
        fprintf(out, "windows_%s(%s); return; ", f->name, f->call_args);
    } else {
        fprintf(out, "return windows_%s(%s); ", f->name, f->call_args);
    }
    fprintf(out, "}\n");
    
    // macOS
    fprintf(out, "    if (IsXnu()) { ");
    if (strcmp(f->return_type, "void") == 0) {
        fprintf(out, "macos_%s(%s); return; ", f->name, f->call_args);
    } else {
        fprintf(out, "return macos_%s(%s); ", f->name, f->call_args);
    }
    fprintf(out, "}\n");
    
    // Fallback
    fprintf(out, "    UNSUPPORTED_PLATFORM();\n");
    fprintf(out, "}\n\n");
}

int main(int argc, char **argv) {
    FILE *out = stdout;
    if (argc > 1) {
        out = fopen(argv[1], "w");
        if (!out) { perror(argv[1]); return 1; }
    }
    
    emit_header(out);
    
    for (const SokolFunc *f = funcs; f->name; f++) {
        emit_function(out, f);
    }
    
    if (out != stdout) fclose(out);
    return 0;
}
```

### Build and Use

```bash
# Build the generator as APE binary
cosmocc -O2 -o tools/gen-sokol.com tools/gen-sokol.c

# Generate the dispatch layer
./tools/gen-sokol.com > shims/sokol/sokol_cosmo.c
```

### Advantages Over Python

| Aspect | Python gen-sokol | C gen-sokol.com |
|--------|------------------|-----------------|
| Dependencies | Python 3 runtime | None |
| Portability | Requires interpreter | APE runs everywhere |
| Philosophy | ❌ Violates | ✅ Compliant |
| CI/CD | Needs Python install | Self-contained |
| Binary size | N/A | ~50KB APE |

### Effort: 2-3 hours for full implementation

---

## 📍 Line Number Inaccuracy — Root Cause & Prevention

### Why It Happened

**Root cause:** The specialist reports were generated without direct file access. Line numbers were either:
1. Cached from stale analysis
2. Estimated from function order
3. Hallucinated when actual file wasn't available

**Evidence:** Every specialist had *different* wrong numbers for the same functions. If they had actual file access, they would at least be consistently wrong. The variance proves independent guessing.

### Prevention for Round 2

**1. Use `grep -n` for all line number claims:**
```bash
# Correct way to get line numbers
grep -n "bool sapp_isvalid" shims/sokol/sokol_cosmo.c
# Output: 12:bool sapp_isvalid(void) {
```

**2. Generate manifests with ctags:**
```bash
# Build ctags as APE
cosmocc -o tools/ctags.com deps/ctags/*.c

# Generate function manifest
./tools/ctags.com -x --c-kinds=f shims/**/*.c > manifest.txt
```

**3. Add verification step to CI:**
```makefile
verify-manifest:
    @echo "Verifying line numbers..."
    @./tools/verify-manifest.com manifest.txt
```

**4. Document in CONTRIBUTING.md:**
```markdown
## Line Number Accuracy

All reports referencing line numbers MUST use `grep -n` to verify.
Do NOT estimate or recall line numbers from memory.
```

### Systemic Fix

For Round 2, require specialists to:
1. Run `grep -n "function_name" file.c` before citing any line
2. Include the grep output in their evidence
3. Flag if file wasn't directly accessible

---

## 🎯 Prioritized Action Plan — Minimum Viable Path

### Priority 1: GLX Shim (MUST — Blocks Linux)

**What:** Create `shims/linux/glx.c` with 18 GLX function shims  
**Why:** Linux won't display a window without GLX context management  
**Effort:** 2 hours  
**Dependencies:** None  

### Priority 2: Dispatch Fallback (SHOULD — Safety)

**What:** Add `UNSUPPORTED_PLATFORM()` macro to all dispatch functions  
**Why:** Currently returns garbage on FreeBSD/NetBSD  
**Effort:** 30 minutes  
**Dependencies:** None (can be done by hand or wait for gen-sokol.com)  

### Priority 3: Replace gen-sokol (MUST — Philosophy)

**What:** Write `tools/gen-sokol.c`, compile with cosmocc  
**Why:** Python violates project core philosophy  
**Effort:** 2-3 hours  
**Dependencies:** None  
**Note:** This fix also includes the dispatch fallback (baked into generator output)

### Timeline

| Day | Task | Output |
|-----|------|--------|
| Day 1, AM | Create glx.c | Linux builds run |
| Day 1, PM | Write gen-sokol.c | Python eliminated |
| Day 2, AM | Regenerate sokol_cosmo.c | Dispatch fallback included |
| Day 2, PM | Test on Linux/Windows | Verified working |

### What Can Wait (v2 Scope)

- macOS full implementation (stubs are fine for v1)
- ARM64 testing (nice to have, not blocking)
- Audio backend (not started, out of scope)
- D3D11 backend (OpenGL-only is fine)

---

## Summary

| Issue | Solution | Effort | Priority |
|-------|----------|--------|----------|
| Missing GLX | Create glx.c shim | 2 hours | 🔴 P1 |
| No dispatch fallback | UNSUPPORTED_PLATFORM() macro | 30 min | 🟠 P2 |
| Python gen-sokol | Rewrite as gen-sokol.c | 2-3 hours | 🔴 P1 |
| Line number errors | Use grep -n, add to CI | 1 hour | 🟡 P3 |

**Total effort:** ~6 hours of focused work.  
**Result:** Linux builds work, philosophy restored, safety improved.

---

*Generated by Solutions Architect for Swiss Rounds v4 — Triad Phase 3*
