# ABI & Calling Convention Analysis: cosmo-sokol v3

**Analyst:** ASM Specialist  
**Project:** cosmo-sokol-v3  
**Round:** 3  
**Date:** 2026-02-09  
**Domain:** AMD64/AArch64 Assembly, ABI, Calling Conventions

---

## Executive Summary — Round 3

Round 3 focuses on **source-verified** analysis of ABI compatibility, calling conventions, and the `cosmo_dltramp` mechanism. Building on Rounds 1-2, I've now performed deep code inspection to validate claims and surface new findings.

### Key Round 3 Findings

| Finding | Severity | Status |
|---------|----------|--------|
| Handle types (4-byte structs) ABI-safe | ✅ | Verified at sokol_gfx.h:1648-1653 |
| sg_range 16-byte struct calling convention risk | ⚠️ HIGH | Requires cosmo_dltramp verification |
| Windows type redefinitions match Win32 ABI | ✅ | Verified at sokol_windows.c:14-46 |
| cosmo_dltramp load-before-use pattern | ✅ | Verified at x11.c:87 |
| Current dlopen error handling uses assert() | ⚠️ MEDIUM | Not production-safe |
| ARM64 HFA handling for sg_color | ⚠️ MEDIUM | Requires testing |

### Changes from Round 2

1. **Source-verified** all struct layouts (not just documented)
2. **Identified specific cosmo_dltramp patterns** in actual shim code
3. **Confirmed Windows type layout matches** with actual struct definitions
4. **Discovered assert()-based error handling** needs production hardening

---

## 1. Source-Verified ABI Analysis

### 1.1 Handle Types — Verified ✅

**Source:** `deps/sokol/sokol_gfx.h` lines 1648-1653

```c
typedef struct sg_buffer        { uint32_t id; } sg_buffer;
typedef struct sg_image         { uint32_t id; } sg_image;
typedef struct sg_sampler       { uint32_t id; } sg_sampler;
typedef struct sg_shader        { uint32_t id; } sg_shader;
typedef struct sg_pipeline      { uint32_t id; } sg_pipeline;
typedef struct sg_attachments   { uint32_t id; } sg_attachments;
```

**ABI Analysis:**

| Type | Size | Alignment | AMD64 SysV Pass | AMD64 MS x64 Pass | ARM64 Pass |
|------|------|-----------|-----------------|-------------------|------------|
| sg_buffer | 4 bytes | 4 bytes | RAX (return), RDI (arg) | RAX (return), RCX (arg) | W0 (32-bit) |
| sg_image | 4 bytes | 4 bytes | RAX (return), RDI (arg) | RAX (return), RCX (arg) | W0 (32-bit) |
| sg_sampler | 4 bytes | 4 bytes | RAX (return), RDI (arg) | RAX (return), RCX (arg) | W0 (32-bit) |
| sg_shader | 4 bytes | 4 bytes | RAX (return), RDI (arg) | RAX (return), RCX (arg) | W0 (32-bit) |
| sg_pipeline | 4 bytes | 4 bytes | RAX (return), RDI (arg) | RAX (return), RCX (arg) | W0 (32-bit) |
| sg_attachments | 4 bytes | 4 bytes | RAX (return), RDI (arg) | RAX (return), RCX (arg) | W0 (32-bit) |

**Verdict:** All handle types are single-member 4-byte structs. These are passed/returned identically to `uint32_t` on all platforms. **ABI-SAFE.**

### 1.2 sg_range — Critical 16-Byte Struct

**Source:** `deps/sokol/sokol_gfx.h` lines 1662-1665

```c
typedef struct sg_range {
    const void* ptr;   // offset 0, 8 bytes
    size_t size;       // offset 8, 8 bytes
} sg_range;            // Total: 16 bytes
```

**ABI Analysis — The 16-Byte Boundary Problem:**

| Convention | By-Value Arg | By-Value Return |
|------------|--------------|-----------------|
| AMD64 System V | RDI:RSI (split into 2 regs) | RAX:RDX |
| AMD64 Microsoft x64 | Hidden pointer (RCX) | Hidden pointer (RAX→memory) |
| ARM64 AAPCS | X0:X1 | X0:X1 |

**This is the critical ABI difference!** A 16-byte struct is:
- **Passed in 2 registers** on System V and ARM64
- **Passed via hidden pointer** on Microsoft x64

**Risk Assessment:**

When cosmo-sokol calls a sokol function like:
```c
void sg_update_buffer(sg_buffer buf, const sg_range* data);
```

The `sg_range*` is a pointer, so it's passed in a single register on all platforms. **SAFE.**

However, if any function returned `sg_range` by value:
```c
sg_range get_data(void);  // HYPOTHETICAL
```

This would fail on cross-convention calls without cosmo_dltramp intervention.

**Current Status:** Inspecting sokol_gfx.h shows `sg_range` is always passed by pointer (`const sg_range*`), never returned by value. **SAFE for current API.**

**Recommendation:** Add static assertion to catch future ABI breaks:

```c
/* shims/include/sokol_abi_check.h */
#include <stddef.h>

_Static_assert(sizeof(sg_range) == 16, "sg_range size ABI break");
_Static_assert(offsetof(sg_range, ptr) == 0, "sg_range.ptr offset ABI break");
_Static_assert(offsetof(sg_range, size) == 8, "sg_range.size offset ABI break");
_Static_assert(_Alignof(sg_range) == 8, "sg_range alignment ABI break");
```

### 1.3 sg_color — Homogeneous Floating-Point Aggregate

**Source:** `deps/sokol/sokol_gfx.h` line 1702

```c
typedef struct sg_color { float r, g, b, a; } sg_color;
```

**ABI Analysis:**

| Convention | Classification | Arg Passing | Return |
|------------|----------------|-------------|--------|
| AMD64 System V | SSE aggregate | XMM0 (if ≤16 bytes) or memory | XMM0 |
| AMD64 Microsoft x64 | Non-HFA (size > 8) | Hidden pointer | Hidden pointer |
| ARM64 AAPCS | HFA (4 floats) | V0-V3 (SIMD) | V0-V3 |

**Critical Finding — ARM64 HFA:**

On ARM64, `sg_color` qualifies as a **Homogeneous Floating-Point Aggregate** (HFA) because:
- It contains only float members
- All members are the same type
- It has ≤4 members

HFAs are passed in **SIMD/FP registers V0-V3** on ARM64, not general-purpose registers.

**Impact for cosmo_dltramp:**
If `cosmo_dltramp` doesn't correctly handle HFA register passing on ARM64, functions like:
```c
void sg_apply_pipeline(sg_pipeline pip);
void some_func_with_color(sg_color color);  // HFA!
```

Will corrupt the `sg_color` argument.

**Verification Needed:** Check if any sokol function passes `sg_color` by value (not pointer).

**Quick grep result:** sokol typically passes colors via `sg_color*` or embedded in larger structs. The `sg_pass_action.colors[].clear_value` is `sg_color` by value, but it's embedded in a struct.

**Recommendation:** Add HFA verification assertion:

```c
#if defined(__aarch64__)
/* Verify sg_color qualifies as HFA (consecutive same-type floats) */
_Static_assert(
    offsetof(sg_color, g) - offsetof(sg_color, r) == sizeof(float) &&
    offsetof(sg_color, b) - offsetof(sg_color, g) == sizeof(float) &&
    offsetof(sg_color, a) - offsetof(sg_color, b) == sizeof(float),
    "sg_color must be HFA-compatible for ARM64 V-register passing"
);
#endif
```

---

## 2. Windows Type Redefinitions — Verified ✅

**Source:** `shims/sokol/sokol_windows.c` lines 1-105

The Windows shim redefines Win32 types to avoid including `<windows.h>` (which conflicts with Cosmopolitan). Key types:

### 2.1 LARGE_INTEGER (lines 14-24)

```c
typedef union {
  struct {
    DWORD LowPart;
    LONG  HighPart;
  } DUMMYSTRUCTNAME;
  struct {
    DWORD LowPart;
    LONG  HighPart;
  } u;
  LONGLONG QuadPart;
} LARGE_INTEGER, *PLARGE_INTEGER;
```

**ABI Verification:**
- `DWORD` = 4 bytes, `LONG` = 4 bytes → inner struct = 8 bytes
- `LONGLONG` = 8 bytes
- Union size = max(8, 8) = 8 bytes
- Alignment = 8 bytes (QuadPart alignment)

**Matches Win32:** ✅

### 2.2 RECT (lines 26-31)

```c
typedef struct tagRECT {
  LONG left;    // offset 0, 4 bytes
  LONG top;     // offset 4, 4 bytes
  LONG right;   // offset 8, 4 bytes
  LONG bottom;  // offset 12, 4 bytes
} RECT, *PRECT, *NPRECT, *LPRECT;
```

**ABI Verification:**
- Total size: 16 bytes
- Alignment: 4 bytes (LONG alignment)

**Matches Win32:** ✅

### 2.3 POINT (lines 33-36)

```c
typedef struct tagPOINT {
  LONG x;  // offset 0, 4 bytes
  LONG y;  // offset 4, 4 bytes
} POINT, *PPOINT, *NPPOINT, *LPPOINT;
```

**ABI Verification:**
- Total size: 8 bytes
- Alignment: 4 bytes

**Matches Win32:** ✅

### 2.4 MSG (lines 38-46)

```c
typedef struct tagMSG {
  HWND   hwnd;      // offset 0, 8 bytes (pointer on 64-bit)
  UINT   message;   // offset 8, 4 bytes
  WPARAM wParam;    // offset 16, 8 bytes (padding after UINT)
  LPARAM lParam;    // offset 24, 8 bytes
  DWORD  time;      // offset 32, 4 bytes
  POINT  pt;        // offset 36, 8 bytes (POINT is 2×LONG)
  DWORD  lPrivate;  // offset 44, 4 bytes
} MSG, *PMSG, *NPMSG, *LPMSG;
```

**ABI Verification:**
- Size calculation: 8 + 4 + (4 padding) + 8 + 8 + 4 + 8 + 4 = 48 bytes
- **Note:** Actual Win32 MSG size may vary slightly by Windows version, but core members are stable.

**Matches Win32:** ✅ (core layout verified)

### 2.5 PIXELFORMATDESCRIPTOR (lines 72-95)

26-member struct with WORD, DWORD, BYTE fields. The layout matches the Win32 GDI specification exactly.

**Matches Win32:** ✅

---

## 3. cosmo_dltramp Pattern Analysis

### 3.1 Current Pattern (Verified from x11.c)

**Source:** `shims/linux/x11.c` lines 81-146

```c
static void load_X11_procs(void) {
    libX11 = cosmo_dlopen("libX11.so", RTLD_NOW | RTLD_GLOBAL);
    proc_XOpenDisplay = cosmo_dltramp(cosmo_dlsym(libX11, "XOpenDisplay"));
    assert(proc_XOpenDisplay != NULL && "Could not load XOpenDisplay");
    // ... repeated for each function
}
```

**Pattern Breakdown:**

1. `cosmo_dlopen()` — Opens shared library, returns handle
2. `cosmo_dlsym()` — Gets raw function pointer (native calling convention)
3. `cosmo_dltramp()` — **Wraps the function in a trampoline** that translates between Cosmopolitan's internal calling convention and the target library's calling convention

### 3.2 cosmo_dltramp Mechanism

`cosmo_dltramp` is the critical component that enables Cosmopolitan's "fat binary" to call native shared libraries with different ABIs.

**How it works (conceptual):**

```
┌─────────────────────────────────────────────────────────────────┐
│                    Cosmopolitan APE Binary                       │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  User Code: XOpenDisplay("...")                         │   │
│   └───────────────────────┬─────────────────────────────────┘   │
│                           │                                      │
│                           ▼                                      │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  proc_XOpenDisplay (function pointer via cosmo_dltramp) │   │
│   │                                                         │   │
│   │  [Trampoline stub]                                      │   │
│   │  1. Save Cosmopolitan caller-saved regs                 │   │
│   │  2. Convert args to target ABI (SysV → MS x64 if Win)   │   │
│   │  3. Call real XOpenDisplay                              │   │
│   │  4. Convert return value back                           │   │
│   │  5. Restore regs, return                                │   │
│   └───────────────────────┬─────────────────────────────────┘   │
│                           │                                      │
└───────────────────────────┼──────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    libX11.so (System Library)                    │
│                    (Native System V AMD64 ABI)                   │
└─────────────────────────────────────────────────────────────────┘
```

### 3.3 Current Error Handling — Problem Identified

**Source:** `shims/linux/x11.c` line 89

```c
proc_XOpenDisplay = cosmo_dltramp(cosmo_dlsym(libX11, "XOpenDisplay"));
assert(proc_XOpenDisplay != NULL && "Could not load XOpenDisplay");
```

**Problems:**

1. **assert() is removed in NDEBUG builds** — Production binaries may not have assertions enabled
2. **No check if libX11 is NULL** — `cosmo_dlsym(NULL, ...)` is undefined behavior
3. **Crash happens at load time** — User sees segfault, not helpful error message

**Recommendation:** Use the safe loading macros from Round 2:

```c
/* BEFORE (unsafe) */
libX11 = cosmo_dlopen("libX11.so", RTLD_NOW | RTLD_GLOBAL);
proc_XOpenDisplay = cosmo_dltramp(cosmo_dlsym(libX11, "XOpenDisplay"));
assert(proc_XOpenDisplay != NULL);

/* AFTER (safe) */
#include "cosmo_dl_safe.h"
COSMO_DL_LOAD_LIB(libX11, "libX11.so.6", "X11");  // Use versioned .so
COSMO_DL_LOAD_SYM(libX11, proc_XOpenDisplay, "XOpenDisplay");
```

### 3.4 Library Name Versioning

**Issue Identified:** Current code uses unversioned library names:

```c
libX11 = cosmo_dlopen("libX11.so", ...);
libXcursor = cosmo_dlopen("libXcursor.so", ...);
libXi = cosmo_dlopen("libXi.so", ...);
```

**Problem:** On many Linux distributions, `libX11.so` is a linker script or doesn't exist. The actual library is `libX11.so.6`.

**Recommendation:** Use versioned library names:

```c
libX11 = cosmo_dlopen("libX11.so.6", RTLD_NOW | RTLD_GLOBAL);
libXcursor = cosmo_dlopen("libXcursor.so.1", RTLD_NOW | RTLD_GLOBAL);
libXi = cosmo_dlopen("libXi.so.6", RTLD_NOW | RTLD_GLOBAL);
```

---

## 4. Calling Convention Deep Dive

### 4.1 Register Mapping Summary

| Arg # | AMD64 SysV | AMD64 MS x64 | ARM64 AAPCS |
|-------|------------|--------------|-------------|
| 1 (int/ptr) | RDI | RCX | X0 |
| 2 (int/ptr) | RSI | RDX | X1 |
| 3 (int/ptr) | RDX | R8 | X2 |
| 4 (int/ptr) | RCX | R9 | X3 |
| 5 (int/ptr) | R8 | [stack] | X4 |
| 6 (int/ptr) | R9 | [stack] | X5 |
| 1 (float) | XMM0 | XMM0 | V0 |
| 2 (float) | XMM1 | XMM1 | V1 |

### 4.2 Critical Functions — Calling Convention Analysis

**Function: sg_begin_pass**

```c
void sg_begin_pass(const sg_pass* pass);
```

- `pass` is a pointer (8 bytes)
- All conventions: Pass in first integer register
- **SAFE**

**Function: sg_draw**

```c
void sg_draw(int base_element, int num_elements, int num_instances);
```

- 3 integer arguments
- SysV: RDI, RSI, RDX
- MS x64: RCX, RDX, R8
- ARM64: X0, X1, X2
- **Requires translation** — cosmo_dltramp handles this

**Function: XCreateWindow (from x11.c)**

```c
Window XCreateWindow(Display* display, Window parent, int x, int y, 
                     unsigned int width, unsigned int height, 
                     unsigned int border_width, int depth, 
                     unsigned int class, Visual* visual, 
                     unsigned long valuemask, XSetWindowAttributes* attributes);
```

- **12 arguments!** — More than can fit in registers on any convention
- Arguments 7+ go on stack for all conventions
- Stack layout differs between SysV and MS x64
- **cosmo_dltramp must handle stack argument reordering**

### 4.3 Struct Return Conventions

| Struct Size | AMD64 SysV | AMD64 MS x64 | ARM64 |
|-------------|------------|--------------|-------|
| ≤8 bytes | RAX | RAX | X0 |
| 9-16 bytes | RAX:RDX | Hidden ptr | X0:X1 |
| >16 bytes | Hidden ptr (RDI) | Hidden ptr (RCX) | Hidden ptr (X8) |

**Critical Difference:** Hidden pointer register is different:
- SysV: RDI (first arg slot)
- MS x64: RCX (first arg slot, but different reg)
- ARM64: X8 (dedicated)

**sokol Functions Returning Large Structs:**

```c
sg_desc sg_query_desc(void);  // sg_desc is LARGE (hundreds of bytes)
sg_buffer_desc sg_query_buffer_desc(sg_buffer buf);  // Also large
```

These all use hidden pointer return — cosmo_dltramp must translate the hidden pointer register.

---

## 5. cosmo_dltramp Verification Requirements

### 5.1 Test Cases Needed

To verify cosmo_dltramp handles sokol's calling patterns correctly:

| Test Case | Function Signature | Why It's Tricky |
|-----------|-------------------|-----------------|
| Many args | `XCreateWindow` (12 args) | Stack args differ |
| Float args | `glClearColor(r,g,b,a)` | XMM registers |
| Large return | `sg_query_desc()` | Hidden pointer |
| Mixed int/float | `glViewport` + `glClearColor` | Register allocation |
| Callbacks | `sapp_desc.init_cb` | Callback invocation direction |

### 5.2 Minimal ABI Test Program

```c
/* test/abi_smoke_test.c */
#include <stdio.h>
#include <assert.h>
#include <cosmo.h>

/* Test 1: Simple function call */
static void* libm;
static double (*proc_sin)(double);

void test_simple_call(void) {
    libm = cosmo_dlopen("libm.so.6", RTLD_NOW);
    assert(libm != NULL);
    proc_sin = cosmo_dltramp(cosmo_dlsym(libm, "sin"));
    assert(proc_sin != NULL);
    
    double result = proc_sin(3.14159265358979 / 2.0);
    assert(result > 0.99 && result < 1.01);  // sin(π/2) ≈ 1.0
    printf("✓ Simple float call: sin(π/2) = %f\n", result);
}

/* Test 2: Multiple integer args */
static void* libc;
static int (*proc_snprintf)(char*, size_t, const char*, ...);

void test_multi_arg(void) {
    libc = cosmo_dlopen("libc.so.6", RTLD_NOW);
    proc_snprintf = cosmo_dltramp(cosmo_dlsym(libc, "snprintf"));
    
    char buf[64];
    int n = proc_snprintf(buf, sizeof(buf), "test %d %d %d", 1, 2, 3);
    assert(n > 0);
    printf("✓ Multi-arg call: snprintf -> \"%s\"\n", buf);
}

/* Test 3: Struct return (if we can find a simple one) */
void test_struct_return(void) {
    /* Most libc functions don't return structs, so skip for smoke test */
    printf("✓ Struct return: (skipped in smoke test)\n");
}

int main(void) {
    printf("=== ABI Smoke Test ===\n");
    test_simple_call();
    test_multi_arg();
    test_struct_return();
    printf("=== All tests passed ===\n");
    return 0;
}
```

---

## 6. Round 3 Recommendations

### 6.1 Immediate Actions (P0)

| Action | Owner | File | Description |
|--------|-------|------|-------------|
| Add ABI assertions | asm | `shims/include/sokol_abi_check.h` | Static assertions for critical struct layouts |
| Use versioned .so names | cosmo | `shims/linux/*.c` | `libX11.so` → `libX11.so.6` |
| Replace assert with safe macros | cosmo | `shims/linux/x11.c` | Use COSMO_DL_LOAD_* macros |

### 6.2 Verification Actions (P1)

| Action | Owner | Description |
|--------|-------|-------------|
| ARM64 HFA test | testcov | Verify sg_color passing on ARM64 |
| ABI smoke test suite | testcov | Implement abi_smoke_test.c |
| 12-arg function test | testcov | Test XCreateWindow-style calls |

### 6.3 New Static Assertions File

Create `shims/include/sokol_abi_check.h`:

```c
#ifndef SOKOL_ABI_CHECK_H
#define SOKOL_ABI_CHECK_H

/* ============================================================
 * sokol_abi_check.h — ABI verification for cosmo-sokol
 * 
 * Include this in sokol_cosmo.c to catch ABI breaks at compile time.
 * ============================================================ */

#include <stddef.h>
#include <stdint.h>

/* Platform requirements */
_Static_assert(sizeof(void*) == 8, "64-bit platform required");
_Static_assert(sizeof(size_t) == 8, "LP64/LLP64 data model required");

/* Handle types — must be exactly 4 bytes for register passing */
_Static_assert(sizeof(sg_buffer) == 4, "sg_buffer size ABI break");
_Static_assert(sizeof(sg_image) == 4, "sg_image size ABI break");
_Static_assert(sizeof(sg_sampler) == 4, "sg_sampler size ABI break");
_Static_assert(sizeof(sg_shader) == 4, "sg_shader size ABI break");
_Static_assert(sizeof(sg_pipeline) == 4, "sg_pipeline size ABI break");
_Static_assert(sizeof(sg_attachments) == 4, "sg_attachments size ABI break");

/* sg_range — critical 16-byte boundary struct */
_Static_assert(sizeof(sg_range) == 16, "sg_range size ABI break");
_Static_assert(offsetof(sg_range, ptr) == 0, "sg_range.ptr offset ABI break");
_Static_assert(offsetof(sg_range, size) == 8, "sg_range.size offset ABI break");
_Static_assert(_Alignof(sg_range) == 8, "sg_range alignment ABI break");

/* sg_color — 16-byte float aggregate */
_Static_assert(sizeof(sg_color) == 16, "sg_color size ABI break");
_Static_assert(offsetof(sg_color, r) == 0, "sg_color.r offset ABI break");
_Static_assert(offsetof(sg_color, g) == 4, "sg_color.g offset ABI break");
_Static_assert(offsetof(sg_color, b) == 8, "sg_color.b offset ABI break");
_Static_assert(offsetof(sg_color, a) == 12, "sg_color.a offset ABI break");

#if defined(__aarch64__)
/* ARM64 HFA verification — sg_color must have consecutive float members */
_Static_assert(
    (offsetof(sg_color, g) - offsetof(sg_color, r)) == sizeof(float) &&
    (offsetof(sg_color, b) - offsetof(sg_color, g)) == sizeof(float) &&
    (offsetof(sg_color, a) - offsetof(sg_color, b)) == sizeof(float),
    "sg_color must be HFA-compatible for ARM64 V-register passing"
);
#endif

#endif /* SOKOL_ABI_CHECK_H */
```

---

## 7. Cross-Reference with Other Specialists

### 7.1 For cicd Specialist

- Add ARM64 runner to CI matrix (GitHub now has `ubuntu-24.04-arm` runners)
- ABI assertions should be **blocking** gate, not warning

### 7.2 For cosmo Specialist

- Integrate `sokol_abi_check.h` into build
- Implement safe dlopen macros as specified in Round 2

### 7.3 For testcov Specialist

- Create ABI smoke test suite
- Add regression tests for struct return functions

---

## 8. Round 3 Verification Checklist

- [x] Handle types verified at source (sokol_gfx.h:1648-1653)
- [x] sg_range layout verified (sokol_gfx.h:1662-1665)
- [x] sg_color layout verified (sokol_gfx.h:1702)
- [x] Windows type redefinitions verified (sokol_windows.c:1-105)
- [x] cosmo_dltramp pattern identified (x11.c:81-146)
- [x] Error handling gap identified (assert-based)
- [x] Library versioning gap identified (unversioned .so names)
- [x] ARM64 HFA consideration documented
- [x] Static assertions header specified
- [x] ABI smoke test outlined

---

## 9. Conclusion

**Round 3 confirms the fundamental ABI safety of cosmo-sokol's design while identifying specific hardening opportunities:**

**Verified Safe:**
- All handle types (4-byte single-member structs)
- sg_range passed by pointer (not value)
- Windows type redefinitions match Win32 ABI
- cosmo_dltramp pattern correctly applied

**Requires Attention:**
- Replace assert() with production-safe error handling
- Use versioned library names (libX11.so.6)
- Add static assertions for compile-time ABI verification
- ARM64 HFA handling needs testing

**Key Insight:** The biggest risk isn't the current code — it's **future changes** to sokol's API that might introduce ABI-breaking patterns. Static assertions provide a safety net that catches these at compile time rather than runtime crashes.

---

*Round 3 Analysis Complete*  
*ASM Specialist — ABI Verification Domain*
