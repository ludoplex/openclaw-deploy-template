# Sokol Internals Deep Dive

This document analyzes how Sokol headers handle cross-platform concerns. **Key insight: Sokol already solves most cross-platform issues at compile-time via preprocessor - we overengineered our Cosmopolitan build by not understanding this.**

## 1. Platform Detection (#ifdef Patterns)

Sokol uses a clean, hierarchical platform detection system at the top of `sokol_app.h` and `sokol_gfx.h`:

### Primary Platform Detection (sokol_app.h lines 2290-2365)

```c
#if defined(__APPLE__)
    #define _SAPP_APPLE (1)
    #include <TargetConditionals.h>
    #if defined(TARGET_OS_IPHONE) && !TARGET_OS_IPHONE
        #define _SAPP_MACOS (1)
        // Requires: SOKOL_METAL, SOKOL_GLCORE, or SOKOL_WGPU
    #else
        #define _SAPP_IOS (1)
        // Requires: SOKOL_METAL or SOKOL_GLES3
    #endif
#elif defined(__EMSCRIPTEN__)
    #define _SAPP_EMSCRIPTEN (1)
    // Requires: SOKOL_GLES3 or SOKOL_WGPU
#elif defined(_WIN32)
    #define _SAPP_WIN32 (1)
    // Requires: SOKOL_D3D11, SOKOL_GLCORE, SOKOL_WGPU, SOKOL_VULKAN, or SOKOL_NOAPI
#elif defined(__ANDROID__)
    #define _SAPP_ANDROID (1)
    // Requires: SOKOL_GLES3
#elif defined(__linux__) || defined(__unix__)
    #define _SAPP_LINUX (1)
    // Requires: SOKOL_GLCORE, SOKOL_GLES3, SOKOL_WGPU, or SOKOL_VULKAN
    #if defined(SOKOL_GLCORE)
        #if defined(SOKOL_FORCE_EGL)
            #define _SAPP_EGL (1)
        #else
            #define _SAPP_GLX (1)
        #endif
    #endif
#else
    #error "sokol_app.h: Unknown platform"
#endif
```

### Backend Unification

```c
#if defined(SOKOL_GLCORE) || defined(SOKOL_GLES3)
    #define _SAPP_ANY_GL (1)
#endif
```

**Key Pattern**: Internal `_SAPP_*` defines are derived from compiler-defined macros (`_WIN32`, `__APPLE__`, etc.) plus user-defined backend selection (`SOKOL_GLCORE`, `SOKOL_D3D11`, etc.).

## 2. SOKOL_GLCORE Backend Implementation

### Windows WGL (lines 8399-8692)

The Windows GL backend dynamically loads `opengl32.dll` and uses WGL extensions:

```c
_SOKOL_PRIVATE void _sapp_wgl_init(void) {
    _sapp.wgl.opengl32 = LoadLibraryA("opengl32.dll");
    _sapp.wgl.CreateContext = (PFN_wglCreateContext) GetProcAddress(..., "wglCreateContext");
    _sapp.wgl.DeleteContext = (PFN_wglDeleteContext) GetProcAddress(..., "wglDeleteContext");
    _sapp.wgl.GetProcAddress = (PFN_wglGetProcAddress) GetProcAddress(..., "wglGetProcAddress");
    _sapp.wgl.MakeCurrent = (PFN_wglMakeCurrent) GetProcAddress(..., "wglMakeCurrent");
    // ... creates helper window for extension loading
}
```

Extensions loaded via `wglGetProcAddress`:
- `wglGetExtensionsStringEXT/ARB`
- `wglCreateContextAttribsARB`
- `wglSwapIntervalEXT`
- `wglGetPixelFormatAttribivARB`

Context creation uses `WGL_ARB_create_context_profile`:
```c
const int attrs[] = {
    WGL_CONTEXT_MAJOR_VERSION_ARB, gl_major,
    WGL_CONTEXT_MINOR_VERSION_ARB, gl_minor,
    WGL_CONTEXT_FLAGS_ARB, WGL_CONTEXT_FORWARD_COMPATIBLE_BIT_ARB,
    WGL_CONTEXT_PROFILE_MASK_ARB, WGL_CONTEXT_CORE_PROFILE_BIT_ARB,
    0, 0
};
```

### Linux GLX (lines 11850-12160)

GLX is loaded dynamically from `libGL.so`:

```c
_SOKOL_PRIVATE void _sapp_glx_init(void) {
    _sapp.glx.libgl = dlopen("libGL.so.1", RTLD_NOW | RTLD_GLOBAL);
    // Fall back to libGL.so if .1 fails
    
    // Load GLX functions via dlsym
    _sapp.glx.GetFBConfigs = dlsym(_sapp.glx.libgl, "glXGetFBConfigs");
    _sapp.glx.MakeCurrent = dlsym(_sapp.glx.libgl, "glXMakeCurrent");
    _sapp.glx.SwapBuffers = dlsym(_sapp.glx.libgl, "glXSwapBuffers");
    // ...
    
    // Extensions via glXGetProcAddressARB
    _sapp.glx.CreateContextAttribsARB = _sapp.glx.GetProcAddressARB("glXCreateContextAttribsARB");
}
```

### Linux EGL Alternative

When `SOKOL_FORCE_EGL` is defined with `SOKOL_GLCORE`:
```c
_SOKOL_PRIVATE void _sapp_egl_init(void) {
    eglBindAPI(EGL_OPENGL_API);  // Not ES!
    _sapp.egl.display = eglGetDisplay((EGLNativeDisplayType)_sapp.x11.display);
    // ... context attrs include EGL_OPENGL_BIT, EGL_CONTEXT_OPENGL_CORE_PROFILE_BIT
}
```

### macOS NSOpenGL (lines 5089-5150)

```c
_SOKOL_PRIVATE void _sapp_macos_gl_init(NSRect window_rect) {
    NSOpenGLPixelFormatAttribute attrs[32];
    attrs[i++] = NSOpenGLPFAOpenGLProfile;
    switch(glVersion) {
        case 32: attrs[i++] = NSOpenGLProfileVersion3_2Core; break;
        case 41: attrs[i++] = NSOpenGLProfileVersion4_1Core; break;
    }
    // NOTE: macOS GL is deprecated, max version is 4.1
}
```

## 3. Symbol Export and Collision Avoidance

### API Declaration Pattern (lines 1340-1355)

```c
#if defined(SOKOL_API_DECL) && !defined(SOKOL_APP_API_DECL)
    #define SOKOL_APP_API_DECL SOKOL_API_DECL
#endif

#ifndef SOKOL_APP_API_DECL
    #if defined(_WIN32) && defined(SOKOL_DLL) && defined(SOKOL_APP_IMPL)
        #define SOKOL_APP_API_DECL __declspec(dllexport)
    #elif defined(_WIN32) && defined(SOKOL_DLL)
        #define SOKOL_APP_API_DECL __declspec(dllimport)
    #else
        #define SOKOL_APP_API_DECL extern
    #endif
#endif
```

### Private Symbol Prefix (lines 2380-2385)

**ALL internal functions use `_SOKOL_PRIVATE` macro**:

```c
#ifndef _SOKOL_PRIVATE
    #if defined(__GNUC__) || defined(__clang__)
        #define _SOKOL_PRIVATE __attribute__((unused)) static
    #else
        #define _SOKOL_PRIVATE static
    #endif
#endif
```

This means:
1. **All internal functions are `static`** - no symbol export, no collision possible
2. The `unused` attribute suppresses warnings for functions conditionally compiled out
3. Only public API functions (prefixed `sapp_`, `sg_`, etc.) are externally visible

### Internal Naming Conventions

| Prefix | Meaning | Example |
|--------|---------|---------|
| `_sapp_` | sokol_app private | `_sapp_wgl_init()` |
| `_sg_` | sokol_gfx private | `_sg_gl_setup_backend()` |
| `_SAPP_` | sokol_app private macro/constant | `_SAPP_WIN32`, `_SAPP_GLX` |
| `_SG_` | sokol_gfx private macro/constant | `_SG_GL_CHECK_ERROR` |
| `sapp_` | sokol_app public API | `sapp_width()` |
| `sg_` | sokol_gfx public API | `sg_setup()` |

### Global State Encapsulation

All global state is in a single static struct per header:

```c
// sokol_app.h
static _sapp_state _sapp;

// sokol_gfx.h  
static _sg_state_t _sg;
```

Platform-specific sub-structures are conditionally included:
```c
typedef struct {
    // ... common fields ...
    #if defined(_SAPP_MACOS)
        _sapp_macos_t macos;
    #elif defined(_SAPP_WIN32)
        _sapp_win32_t win32;
        #if defined(SOKOL_D3D11)
            _sapp_d3d11_t d3d11;
        #elif defined(SOKOL_GLCORE)
            _sapp_wgl_t wgl;
        #endif
    #elif defined(_SAPP_LINUX)
        _sapp_x11_t x11;
        #if defined(_SAPP_GLX)
            _sapp_glx_t glx;
        #endif
    #endif
} _sapp_state;
```

## 4. GL Function Loading (sokol_gfx.h)

sokol_gfx.h has its **own built-in GL loader for Windows** (lines 9042-9200):

```c
#define _SG_GL_FUNCS \
    _SG_XMACRO(glBindVertexArray, void, (GLuint array)) \
    _SG_XMACRO(glGenFramebuffers, void, (GLsizei n, GLuint* framebuffers)) \
    _SG_XMACRO(glBindFramebuffer, void, (GLenum target, GLuint framebuffer)) \
    // ... 100+ GL functions ...

// On Windows, define function pointers
#define _SG_XMACRO(name, ret, args) typedef ret (GL_APIENTRY* PFN_##name) args;
_SG_GL_FUNCS
#undef _SG_XMACRO

#define _SG_XMACRO(name, ret, args) static PFN_##name name;
_SG_GL_FUNCS
#undef _SG_XMACRO

// Load at init time
_SOKOL_PRIVATE void _sg_gl_load_opengl(void) {
    #define _SG_XMACRO(name, ret, args) name = (PFN_##name) _sg_gl_getprocaddr(#name, ...);
    _SG_GL_FUNCS
    #undef _SG_XMACRO
}
```

**This means on Windows, Sokol doesn't need GLEW, GLAD, or any external GL loader!**

Linux/macOS don't need this because:
- Linux: `GL_GLEXT_PROTOTYPES` defined, functions come from `libGL.so`
- macOS: OpenGL framework provides all functions

## 5. Implications for Cosmopolitan Build

### What We DON'T Need to Do

1. **No runtime platform detection** - Sokol handles this at compile time
2. **No GL loader abstraction** - Sokol has one built-in
3. **No symbol collision worries** - Everything internal is `static`
4. **No conditional compilation for backends** - User defines `SOKOL_GLCORE` etc.

### What Cosmopolitan Build SHOULD Do

1. **Define the right macros at compile time**:
   ```c
   #if defined(__COSMOPOLITAN__)
       // Cosmopolitan magic will pick right path at runtime
       #define SOKOL_GLCORE
       #define SOKOL_NO_ENTRY  // We handle main()
   #endif
   ```

2. **Compile multiple platform variants** if needed:
   - Sokol is designed to be compiled once per target
   - For APE, we might need to compile multiple times or use fat binary approach

3. **Let Sokol do the heavy lifting**:
   - Sokol already handles WGL/GLX/NSOpenGL differences
   - We just need to ensure the right `#define`s are set

### The Overengineering We Did

We likely:
1. Tried to abstract platform differences that Sokol already abstracts
2. Wrote runtime detection for things Sokol handles at compile time
3. Worried about symbol collisions that can't happen (everything is `static`)
4. May have fought with GL loaders when Sokol has one built-in

### Simplified Cosmopolitan Approach

```c
// cosmo_sokol.c - Single file!

// Tell Sokol what we want
#define SOKOL_IMPL
#define SOKOL_GLCORE

// Cosmopolitan will set these based on runtime OS:
// - _WIN32 on Windows
// - __linux__ on Linux  
// - __APPLE__ on macOS (if Cosmopolitan supports it)

#include "sokol_app.h"
#include "sokol_gfx.h"
#include "sokol_glue.h"
```

The real challenge for Cosmopolitan is that Sokol expects these to be **compile-time** decisions. Options:
1. Build separate object files per platform, link all
2. Use Cosmopolitan's runtime dispatch at a higher level
3. Patch Sokol to add runtime dispatch (unnecessary complexity)

## Summary

Sokol is elegantly designed for single-platform compilation with all complexity hidden behind preprocessor conditionals. The internal implementation is completely isolated via `static` functions. For Cosmopolitan, the right approach is to compile platform-specific variants and let Cosmopolitan's fat binary mechanism handle runtime selection - NOT to add another abstraction layer on top of Sokol's already-complete abstraction.
