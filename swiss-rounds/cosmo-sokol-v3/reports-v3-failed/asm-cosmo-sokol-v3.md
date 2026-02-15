# ABI Analysis Report: cosmo-sokol

**Analyst:** ASM Specialist  
**Project:** cosmo-sokol-v3  
**Round:** 1  
**Date:** 2026-02-09

## Executive Summary

The cosmo-sokol project enables building sokol applications with Cosmopolitan libc for true "compile once, run anywhere" portability across Linux, Windows, and macOS from a single binary. This analysis examines the ABI (Application Binary Interface) implications of the runtime dispatch pattern used to achieve this portability.

**Key Finding:** The current architecture is ABI-safe for the supported platforms because:
1. Sokol uses fixed-size types (uint32_t, float, bool) extensively
2. The platform dispatch happens at the function level, not struct level
3. All platforms share the same header definitions compiled together

**Risk Areas:** The main ABI concerns center around `size_t` in structs and callback function pointers, which require careful attention during upstream synchronization.

---

## 1. Architecture Overview

### 1.1 Runtime Dispatch Pattern

cosmo-sokol uses a clever preprocessor trick to compile all platform backends into a single binary:

```
┌─────────────────────────────────────────────────────────────┐
│                    User Application                         │
│                         │                                    │
│                    sg_setup()                                │
│                         │                                    │
├─────────────────────────────────────────────────────────────┤
│                   sokol_cosmo.c                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  if (IsLinux())   → linux_sg_setup()                │    │
│  │  if (IsWindows()) → windows_sg_setup()              │    │
│  │  if (IsXnu())     → macos_sg_setup()                │    │
│  └─────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│ linux_  │ windows_  │ macos_   (prefixed implementations)   │
└─────────────────────────────────────────────────────────────┘
```

The `gen-sokol` Python script:
1. Generates `sokol_{platform}.h` files with `#define` prefixes
2. Generates `sokol_cosmo.c` with runtime dispatch functions

### 1.2 Repositories and Sync Points

```
floooh/sokol (upstream headers)
     │
     └──► C:\cosmo-sokol\deps\sokol\ (git submodule)
             │
     ┌───────┴───────┐
     │               │
bullno1/cosmo-sokol  ludoplex/cosmo-sokol (fork)
(upstream wrapper)   (adds macOS support)
```

**Current State:**
- ludoplex fork: 2 commits ahead (macOS stub support)
- sokol submodule: eaa1ca7 (recent)

---

## 2. ABI-Critical Structures

### 2.1 Handle Types (✅ SAFE)

Sokol uses opaque 32-bit handle types that are ABI-stable across all platforms:

```c
typedef struct sg_buffer      { uint32_t id; } sg_buffer;
typedef struct sg_image       { uint32_t id; } sg_image;
typedef struct sg_sampler     { uint32_t id; } sg_sampler;
typedef struct sg_shader      { uint32_t id; } sg_shader;
typedef struct sg_pipeline    { uint32_t id; } sg_pipeline;
typedef struct sg_attachments { uint32_t id; } sg_attachments;
```

**Analysis:** These 4-byte structs are passed by value and have identical layout on all platforms.

### 2.2 Range Structures (⚠️ CAUTION)

```c
typedef struct sg_range {
    const void* ptr;   // 8 bytes on x64
    size_t size;       // 8 bytes on x64
} sg_range;

typedef struct sapp_range {
    const void* ptr;
    size_t size;
} sapp_range;
```

**Analysis:**
- `size_t` is 8 bytes on all 64-bit targets (Linux, Windows x64, macOS x64)
- Cosmopolitan targets x86_64 exclusively, so this is safe
- **Risk:** If arm64 support were added, this would need verification

**Struct Size:** 16 bytes (2 × 8-byte members, naturally aligned)

### 2.3 Color Structure (✅ SAFE)

```c
typedef struct sg_color { float r, g, b, a; } sg_color;
```

**Struct Size:** 16 bytes (4 × 4-byte floats)

### 2.4 Descriptor Structures

These large configuration structures contain many nested types. Key members to watch:

| Structure | Notable Members | ABI Notes |
|-----------|-----------------|-----------|
| `sg_desc` | pointers, callback functions | Passed by pointer, safe |
| `sapp_desc` | function pointers, strings | Passed by pointer, safe |
| `sg_buffer_desc` | `sg_range data` | Contains `size_t` |
| `sg_image_desc` | `sg_image_data` | Contains `sg_range` arrays |
| `sg_shader_desc` | string pointers | Cross-platform string handling |

### 2.5 Callback Function Pointers (⚠️ CRITICAL)

```c
// From sapp_allocator
typedef struct sapp_allocator {
    void* (*alloc_fn)(size_t size, void* user_data);
    void (*free_fn)(void* ptr, void* user_data);
    void* user_data;
} sapp_allocator;
```

**Calling Convention Analysis:**

| Platform | Convention | Register Usage |
|----------|------------|----------------|
| Linux x64 | System V AMD64 | RDI, RSI, RDX, RCX, R8, R9 |
| Windows x64 | Microsoft x64 | RCX, RDX, R8, R9 |
| macOS x64 | System V AMD64 | RDI, RSI, RDX, RCX, R8, R9 |

**Key Point:** The dispatch shim calls the correct platform implementation, which then uses the platform's native calling convention for any callbacks. This is correct because:
- Callbacks are invoked from platform-specific code
- The callback was registered by user code compiled with the same conventions
- Cosmopolitan handles the ABI translation at the system call level

---

## 3. Platform-Specific Type Definitions

### 3.1 Windows Type Shims (`sokol_windows.c`)

The Windows backend redefines Win32 types to avoid conflicts with Cosmopolitan's headers:

```c
typedef union {
  struct { DWORD LowPart; LONG HighPart; } DUMMYSTRUCTNAME;
  LONGLONG QuadPart;
} LARGE_INTEGER;

typedef struct tagRECT { LONG left, top, right, bottom; } RECT;
typedef struct tagPOINT { LONG x, y; } POINT;
typedef struct tagMSG { HWND hwnd; UINT message; ... } MSG;
```

**Analysis:** These must match the Win32 ABI exactly. Current definitions are correct.

### 3.2 Linux Type Shims

X11 types are shimmed via dynamically loaded functions:
- `gen-x11` generates `x11.c` with dlsym-based forwarding
- `gen-gl` generates `gl.c` for OpenGL function loading

### 3.3 macOS Stub

Currently non-functional. Future implementation via `objc_msgSend` will require:
- Correct alignment for Objective-C object pointers (8 bytes)
- Metal resource handles (opaque pointers)
- Cocoa struct types (NSRect, NSPoint, etc.)

---

## 4. Upstream Synchronization Guidelines

### 4.1 When Updating floooh/sokol

1. **Check struct changes in sokol_gfx.h and sokol_app.h:**
   ```bash
   git diff --stat OLD_COMMIT..NEW_COMMIT -- sokol_*.h | grep typedef
   ```

2. **Watch for new public API functions:**
   - Must be added to `SOKOL_FUNCTIONS` list in `gen-sokol`
   - Run `./gen-sokol` to regenerate shims

3. **Search for new `size_t` or pointer usage:**
   ```bash
   grep -n "size_t\|void\*" sokol_gfx.h | head -50
   ```

### 4.2 When Updating bullno1/cosmo-sokol

1. **Check gen-sokol for function list changes**
2. **Verify Win32 type definitions in sokol_windows.c**
3. **Test X11/GL shim generation scripts**

### 4.3 Automated Sync Detection

Recommend adding to CI:
```yaml
- name: Check upstream
  run: |
    cd deps/sokol
    LOCAL=$(git rev-parse HEAD)
    REMOTE=$(git ls-remote origin master | cut -f1)
    if [ "$LOCAL" != "$REMOTE" ]; then
      echo "::warning::Upstream sokol has updates"
    fi
```

---

## 5. ABI Verification Test Strategy

### 5.1 Struct Size Assertions

Add to build process:
```c
_Static_assert(sizeof(sg_buffer) == 4, "sg_buffer size mismatch");
_Static_assert(sizeof(sg_range) == 16, "sg_range size mismatch");
_Static_assert(sizeof(sg_color) == 16, "sg_color size mismatch");
_Static_assert(sizeof(void*) == 8, "64-bit pointers required");
_Static_assert(sizeof(size_t) == 8, "64-bit size_t required");
```

### 5.2 Runtime Consistency Checks

```c
// In initialization
assert(offsetof(sg_range, ptr) == 0);
assert(offsetof(sg_range, size) == 8);
```

### 5.3 Cross-Compile Verification

Test matrix:
- Linux native build, run on Linux ✓
- Linux native build, run on Windows (via Cosmopolitan) ✓
- Windows build would use same binary
- macOS: stub currently, verify when implemented

---

## 6. Specific Recommendations

### 6.1 Immediate Actions

1. **Add SOKOL_FUNCTIONS completeness check:**
   - Parse sokol headers for `SOKOL_GFX_API_DECL` functions
   - Compare against gen-sokol function list
   - Fail CI if mismatch

2. **Document breaking change detection:**
   - Add changelog monitoring for sokol updates
   - Create upgrade checklist

### 6.2 For macOS Implementation

When implementing the macOS backend via objc_msgSend:

1. **Ensure correct struct packing for Cocoa types:**
   ```c
   typedef struct { double x, y; } NSPoint;      // 16 bytes
   typedef struct { double w, h; } NSSize;       // 16 bytes
   typedef struct { NSPoint origin; NSSize size; } NSRect;  // 32 bytes
   ```

2. **Handle objc_msgSend variants correctly:**
   - `objc_msgSend` for general calls
   - `objc_msgSend_stret` for struct returns > 16 bytes
   - `objc_msgSend_fpret` for floating point returns

### 6.3 Version Pinning Alternative

If manual sync becomes too burdensome, consider:
1. Git submodule update script with diff review
2. Semantic versioning for sokol dependency
3. Automated PR generation for upstream changes

---

## 7. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Struct layout change in sokol | Medium | High | Static asserts, upgrade checklist |
| New API function missed | Medium | Medium | Header parsing in CI |
| Callback convention mismatch | Low | Critical | Platform-specific testing |
| size_t behavior on new platform | Low | High | Explicit 64-bit checks |
| Win32 type definition drift | Low | Medium | Version-locked definitions |

---

## 8. Conclusion

The cosmo-sokol architecture is fundamentally sound from an ABI perspective. The function-level dispatch pattern avoids most ABI pitfalls by ensuring each platform uses its native implementation with matching type definitions.

**Primary maintenance burden:** Keeping the function list in `gen-sokol` synchronized with upstream sokol public API additions.

**Recommended automation priority:**
1. Struct size static assertions (immediate)
2. Function list completeness checker (high)
3. Upstream update notifications (medium)
4. Automated upgrade PR generation (optional)

---

*Report generated by ASM Specialist for Swiss Rounds v3 analysis*
