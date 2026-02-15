# ABI & Calling Convention Analysis: cosmo-sokol

**Agent:** asm  
**Date:** 2026-02-09  
**Round:** 1 - Initial Analysis  
**Repository:** [ludoplex/cosmo-sokol](https://github.com/ludoplex/cosmo-sokol)

---

## Executive Summary

The cosmo-sokol project uses a runtime dispatch architecture where Sokol functions are compiled once per platform (Linux, Windows, macOS) with platform prefixes, then dispatched at runtime based on `IsLinux()`, `IsWindows()`, or `IsXnu()`. This creates **critical ABI sensitivity** at multiple layers:

1. **Structure layout compatibility** between Cosmopolitan and native platform ABIs
2. **Calling convention matching** via dlopen/dlsym shims
3. **Function pointer signature alignment** in the dispatch layer

When upstream Sokol changes structs or function signatures, these can **silently break binary compatibility** across the shim boundary.

---

## 1. Calling Convention Analysis

### 1.1 Platform Dispatch Pattern

The project uses a shim generator (`gen-sokol`) that creates runtime dispatch functions:

```c
// sokol_cosmo.c (generated)
void sapp_run(const sapp_desc* desc) {
    if (IsLinux()) {
        linux_sapp_run(desc);
        return;
    }
    if (IsWindows()) {
        windows_sapp_run(desc);
        return;
    }
    if (IsXnu()) {
        macos_sapp_run(desc);
        return;
    }
}
```

**Key Observation:** All platforms receive the **same struct pointer** (`const sapp_desc*`). The struct layout must be identical across all compilation units.

### 1.2 dlopen/dlsym ABI Boundary (Linux)

Linux uses `cosmo_dlopen`/`cosmo_dlsym` with `cosmo_dltramp` for thunk generation:

```c
// x11.c shim pattern
static int (*proc_XPending)(Display* display) = NULL;

static void load_X11_procs(void) {
    libX11 = cosmo_dlopen("libX11.so", RTLD_NOW | RTLD_GLOBAL);
    proc_XPending = cosmo_dltramp(cosmo_dlsym(libX11, "XPending"));
}

int XPending(Display* display) {
    if (libX11 == NULL) { load_X11_procs(); }
    return proc_XPending(display);
}
```

**ABI Risks:**
- `cosmo_dltramp` wraps function pointers to handle calling convention differences
- Native X11/GL libraries use System V AMD64 ABI (Linux), while Cosmopolitan may have subtle differences
- **Function pointer casts are implicit** — signature mismatches cause silent corruption

### 1.3 Calling Convention Summary by Platform

| Platform | ABI | Register Order (int args) | Return Value | Float Args |
|----------|-----|--------------------------|--------------|------------|
| Linux x86_64 | System V AMD64 | RDI, RSI, RDX, RCX, R8, R9 | RAX | XMM0-7 |
| Windows x64 | Microsoft x64 | RCX, RDX, R8, R9 | RAX | XMM0-3 |
| macOS ARM64 | AAPCS64 | X0-X7 | X0 | V0-V7 |
| macOS x86_64 | System V AMD64 | Same as Linux | RAX | XMM0-7 |

**Critical:** Cosmopolitan must handle these transparently. The `cosmo_dltramp` mechanism is essential for Windows/Linux ABI bridging when loading native DLLs.

---

## 2. ABI-Sensitive Structures

### 2.1 High-Risk Structures (Passed by Value)

These structures are returned by value from functions, making their **exact layout ABI-critical**:

| Structure | Size Risk | Fields | Used In |
|-----------|-----------|--------|---------|
| `sg_buffer` | Low (4B) | `uint32_t id` | Many return values |
| `sg_image` | Low (4B) | `uint32_t id` | Many return values |
| `sg_desc` | **HIGH** | 20+ fields | `sg_query_desc()` returns by value |
| `sapp_desc` | **HIGH** | 50+ fields | `sapp_query_desc()` returns by value |
| `sg_features` | Medium | ~15 bools | `sg_query_features()` |
| `sg_limits` | Medium | ~20 ints | `sg_query_limits()` |
| `sg_frame_stats` | **HIGH** | Large nested | `sg_query_frame_stats()` |

**Why This Matters:** When upstream adds/removes/reorders fields:
- Return value register allocation changes
- Stack frame layout changes  
- Caller/callee disagree on struct size → silent memory corruption

### 2.2 Pointer-Passed Structures (Safer, But Still Sensitive)

```c
// These are passed as const pointers - safer for ABI
void sg_setup(const sg_desc* desc);
void sg_apply_bindings(const sg_bindings* bindings);
void sapp_run(const sapp_desc* desc);
```

**Risk Level:** Medium — the pointer is stable, but:
- Field access by **offset** must match
- Padding/alignment differences cause silent corruption
- Adding fields at the end is usually safe
- Reordering or inserting fields is **breaking**

### 2.3 sg_bindings Structure (Critical for Rendering)

```c
typedef struct sg_bindings {
    uint32_t _start_canary;  // Debug sentinel
    sg_buffer vertex_buffers[SG_MAX_VERTEXBUFFER_BINDSLOTS];  // 8 slots
    int vertex_buffer_offsets[SG_MAX_VERTEXBUFFER_BINDSLOTS]; // 8 slots
    sg_buffer index_buffer;
    int index_buffer_offset;
    sg_image images[SG_MAX_IMAGE_BINDSLOTS];     // 16 slots
    sg_sampler samplers[SG_MAX_SAMPLER_BINDSLOTS]; // 16 slots
    sg_buffer storage_buffers[SG_MAX_STORAGEBUFFER_BINDSLOTS]; // 8 slots
    uint32_t _end_canary;    // Debug sentinel
} sg_bindings;
```

**Breaking Changes If:**
- Any `SG_MAX_*` constant changes
- Field order changes
- New arrays are added in the middle
- Canary positions move (debug builds affected)

**Estimated Size:** ~232 bytes on 64-bit (varies with padding)

---

## 3. Function Signature Sensitivity

### 3.1 Currently Exported Functions (from gen-sokol)

The shim exports **~180 functions** across `sokol_app` and `sokol_gfx`. Sample signatures:

```c
// Simple - ABI stable
bool sapp_isvalid(void);
int sapp_width(void);
float sapp_dpi_scale(void);

// Pointer params - moderately stable  
void sg_setup(const sg_desc* desc);
sg_buffer sg_make_buffer(const sg_buffer_desc* desc);

// Returns large struct BY VALUE - dangerous
sapp_desc sapp_query_desc(void);
sg_desc sg_query_desc(void);
sg_frame_stats sg_query_frame_stats(void);

// Function pointer params - complex
sg_trace_hooks sg_install_trace_hooks(const sg_trace_hooks* trace_hooks);
```

### 3.2 Function Signature Change Categories

| Change Type | Example | ABI Impact |
|-------------|---------|------------|
| New parameter added | `void sg_draw(int base, int num, int inst)` → add `int base_instance` | **BREAKING** |
| Parameter type widened | `int` → `int64_t` | **BREAKING** (register allocation) |
| Return type changed | `void*` → `struct handle` | **BREAKING** |
| Struct param added field | `sg_desc.new_field` | Safe if at end, breaks if reordered |
| New function added | `sg_new_feature()` | Safe (just add to shim) |
| Function removed | Rare in Sokol | **BREAKING** (linker error, obvious) |

### 3.3 Callback Function Pointers

**In sapp_desc:**
```c
void (*init_cb)(void);
void (*frame_cb)(void);
void (*cleanup_cb)(void);
void (*event_cb)(const sapp_event*);
void (*event_userdata_cb)(const sapp_event*, void*);
```

**ABI Risk:** These callbacks are invoked by platform code. The `sapp_event` structure layout is critical.

---

## 4. Platform-Specific Concerns

### 4.1 x86_64 Linux

- Uses System V AMD64 ABI
- OpenGL loaded via `cosmo_dlopen("libGL.so")`
- X11 functions shimmed identically
- **Float returns:** XMM0 (SSE), must match native GL expectations

**Known Issue Pattern:**
```c
// GL function: float-heavy
void glClearColor(GLfloat r, GLfloat g, GLfloat b, GLfloat a);
// Cosmopolitan passes in XMM0-3, native GL expects same → OK
```

### 4.2 Windows x64

- Microsoft x64 calling convention (4 register args vs 6)
- Uses WGL for OpenGL
- Win32 functions imported via Cosmopolitan's `master.sh` mechanism
- **Struct return:** Large structs returned via hidden pointer (first arg)

**Hidden Pointer Convention:**
```c
// When sg_desc is large:
// Caller passes hidden pointer in RCX (Windows) or RDI (SysV)
sg_desc sg_query_desc(void);
// Compiled as: void sg_query_desc(sg_desc* hidden_return);
```

**Cross-platform risk:** If struct size triggers hidden pointer on one platform but not another, dispatch fails.

### 4.3 macOS (Currently Stub)

The macOS backend is unimplemented but designed for Objective-C runtime calls via `objc_msgSend`. Key concerns:

```c
// Objective-C runtime ABI
id objc_msgSend(id self, SEL _cmd, ...);
```

- ARM64: Uses AAPCS64 with different struct return rules
- x86_64: Compatible with Linux conventions
- Metal API structs have platform-specific alignment

---

## 5. Silent Breakage Scenarios

### 5.1 Upstream Adds Field to sg_bindings

**Before:**
```c
sg_buffer storage_buffers[8];
uint32_t _end_canary;
```

**After:**
```c
sg_buffer storage_buffers[8];
sg_image storage_images[8];    // NEW
uint32_t _end_canary;
```

**Result:**
- Old compiled code writes `_end_canary` at old offset
- New Sokol reads `_end_canary` at new offset → garbage
- No linker error, no compile error, silent rendering corruption

### 5.2 Upstream Increases SG_MAX_* Constant

```c
#define SG_MAX_IMAGE_BINDSLOTS 16  // Was 16
#define SG_MAX_IMAGE_BINDSLOTS 24  // Now 24
```

**Result:**
- `sg_bindings` struct grows by 32 bytes (8 * sizeof(sg_image))
- All subsequent field offsets shift
- Total ABI incompatibility, silent corruption

### 5.3 Function Parameter Added

```c
// Old:
void sg_draw(int base_element, int num_elements, int num_instances);

// New (hypothetical):
void sg_draw(int base_element, int num_elements, int num_instances, int base_instance);
```

**Result:**
- Old caller passes 3 args
- New callee expects 4 args
- 4th arg is garbage from stack/register → unpredictable behavior

---

## 6. Recommendations for Upstream Tracking

### 6.1 Critical Files to Monitor

| File | What to Watch |
|------|---------------|
| `sokol_gfx.h` | All `typedef struct sg_*`, `SG_MAX_*` constants, function signatures |
| `sokol_app.h` | `sapp_desc`, `sapp_event`, callback signatures |
| Both | Any `SOKOL_API_DECL` function changes |

### 6.2 Automated Detection Strategy

1. **Extract struct layouts** from headers at each release
2. **Compare field names, types, and offsets**
3. **Hash function signatures** for quick change detection
4. **Verify `SG_MAX_*` constants** haven't changed

### 6.3 ABI Stability Assertions

Consider adding compile-time checks:
```c
_Static_assert(sizeof(sg_bindings) == 232, "sg_bindings ABI changed!");
_Static_assert(offsetof(sg_bindings, index_buffer) == 64, "field offset changed!");
```

---

## 7. dlopen/dlsym Specific Issues

### 7.1 Trampoline Requirements

The `cosmo_dltramp` function creates thunks for calling convention translation:

```c
// Pseudocode for what cosmo_dltramp does:
void* cosmo_dltramp(void* native_fn) {
    // Generate thunk that:
    // 1. Marshals args from Cosmopolitan convention
    // 2. Calls native function
    // 3. Marshals return value back
    return thunk_address;
}
```

**Failure Modes:**
- Variadic functions (e.g., `printf`) need special handling
- Struct returns may use different conventions
- Float/double passing in XMM registers must match exactly

### 7.2 Symbol Resolution Risks

```c
// Current pattern:
proc_glClear = cosmo_dltramp(cosmo_dlsym(libGL, "glClear"));
assert(proc_glClear != NULL);  // Only checks existence
```

**Missing Validation:**
- No signature verification
- No version checking
- If Mesa/NVIDIA changes internal glClear implementation → undefined behavior

---

## 8. Summary: ABI Risk Matrix

| Component | Risk Level | Detection | Mitigation |
|-----------|------------|-----------|------------|
| Resource handles (sg_buffer, etc.) | 🟢 Low | Compile | Stable by design |
| SG_MAX_* constants | 🔴 High | Script | Monitor upstream |
| Large struct returns | 🔴 High | Runtime | Add size assertions |
| Callback function pointers | 🟡 Medium | Compile | Type-safe wrappers |
| dlopen function signatures | 🟡 Medium | Runtime | Version checks |
| Struct field reordering | 🔴 High | Script | Offset verification |
| New optional parameters | 🟡 Medium | Compile | Default param wrappers |

---

## 9. Next Steps for Automation

1. **Parse sokol_gfx.h and sokol_app.h** to extract all struct definitions
2. **Generate struct layout fingerprints** (field names, types, offsets)
3. **Compare against pinned baseline** when updating upstream
4. **Fail loudly** on any ABI-breaking change
5. **Auto-regenerate shims** when safe changes detected

---

*End of ABI Analysis Report*
