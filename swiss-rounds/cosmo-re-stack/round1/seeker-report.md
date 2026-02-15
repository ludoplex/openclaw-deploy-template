# Swiss Round 1: Cosmo-RE-Stack Seeker Report

**Date:** 2026-02-10
**Agent:** seeker (Round 1 Specialist)
**Domain:** Research, Prior Art, Undocumented APIs, Integration Patterns

---

## Executive Summary

The cosmo-re-stack vision—a universal binary RE workstation combining tedit-cosmo, e9studio, llamafile, and Cosmopolitan—is architecturally feasible with significant existing infrastructure. Key findings:

1. **E9Studio already integrates WAMR** with Cosmopolitan-specific platform layer
2. **tedit-cosmo has disasm_view.h** ready for binary analysis integration  
3. **llamafile provides OpenAI-compatible API** for LLM-assisted decompilation
4. **cosmobsd does NOT exist** as a separate project—it's BSD support *within* Cosmopolitan
5. **Critical gap:** No existing glue between these components

---

## 1. Prior Art & Similar Projects

### 1.1 Binary Rewriting Tools

| Project | Approach | Relevance |
|---------|----------|-----------|
| **E9Patch** (original) | Static ELF rewriting | Core of e9studio |
| **QBDI** | Dynamic binary instrumentation | Runtime patching alternative |
| **Frida** | JS-scriptable instrumentation | Similar IDE integration concept |
| **Ghidra** | Full RE suite, Java-based | Feature parity target |
| **Binary Ninja** | Commercial, Python API | UX reference |
| **RetDec** | Open decompiler, LLVM-based | Decompilation baseline |

### 1.2 Portable Binary Concepts

| Project | Description | Integration Opportunity |
|---------|-------------|------------------------|
| **Cosmopolitan APE** | Polyglot PE/ELF/Mach-O/ZIP | Universal target format |
| **WAMR** | Lightweight WASM runtime | JIT compilation for patches |
| **llamafile** | APE + LLM in single binary | LLM assistance already solved |
| **AppImage** | Linux portable apps | Prior art for self-contained tools |

### 1.3 Key Paper
- **E9Patch PLDI'2020**: "Binary Rewriting without Control Flow Recovery" - foundation paper
  - Source: `C:\e9studio\README.md` cites https://comp.nus.edu.sg/~gregory/papers/e9patch.pdf

---

## 2. Discovered Undocumented/Under-Documented APIs

### 2.1 E9Studio Analysis Engine (`e9analysis.h`)

**File:** `C:\e9studio\src\e9patch\analysis\e9analysis.h`

```c
// Full binary analysis context - not documented in README
E9Binary *e9_binary_create(const uint8_t *data, size_t size);
E9Binary *e9_binary_open(const char *path);
int e9_binary_analyze(E9Binary *bin);

// CFG construction - powerful but undocumented
E9CFG *e9_cfg_build(E9Binary *bin, E9Function *func);
int e9_cfg_to_dot(E9CFG *cfg, const char *path);

// Source-to-binary mapping for live patching
E9PatchSet *e9_diff_objects(const uint8_t *old_obj, size_t old_size,
                            const uint8_t *new_obj, size_t new_size);
```

### 2.2 E9Studio Decompiler (`e9decompile.h`)

**File:** `C:\e9studio\src\e9patch\analysis\e9decompile.h`

True C decompiler producing Cosmopolitan-compilable output:
```c
// Full pipeline - NOT pseudo-C, actual compilable output
E9Decompile *e9_decompile_create(struct E9Binary *bin, const E9DecompileOpts *opts);
char *e9_decompile_function_full(E9Decompile *dc, struct E9Function *func);
char *e9_decompile_binary(E9Decompile *dc);

// Cosmopolitan type mappings built-in
const char *e9_type_to_cosmo(int size_bits, bool is_signed, bool is_pointer);
```

**Key feature:** Output uses `int64_t`, `uint8_t`, etc.—directly compilable with cosmocc.

### 2.3 E9Studio Binary Patching (`e9binpatch.h`)

**File:** `C:\e9studio\src\e9patch\analysis\e9binpatch.h`

In-place binary editing without full recompilation:
```c
// Session-based patching with undo support
E9BinPatchSession *e9_binpatch_session_create(E9Binary *bin);
int e9_binpatch_bytes(E9BinPatchSession *session, uint64_t addr,
                      const uint8_t *bytes, size_t size, uint32_t flags);

// Code cave management - automatic trampoline generation
int e9_caves_find(E9BinPatchSession *session, size_t min_size);
uint64_t e9_caves_alloc(E9BinPatchSession *session, size_t size, bool executable);

// Detours with original function relocation
int e9_binpatch_detour(E9BinPatchSession *session, uint64_t func_addr,
                       const uint8_t *new_func, size_t new_func_size,
                       uint64_t *orig_func_ptr, uint32_t flags);
```

### 2.4 E9Studio WASM Host (`e9wasm_host.h`)

**File:** `C:\e9studio\src\e9patch\wasm\e9wasm_host.h`

Embedded WAMR with Fast JIT for high-performance execution:
```c
// Execution mode selection (interpreter/JIT/AOT)
void e9wasm_set_exec_mode(int mode);  // 0=interp, 1=fast_jit, 2=aot

// ZipOS manipulation - self-modifying APE!
int e9wasm_zipos_append(const char *name, const uint8_t *data, size_t size);
int e9wasm_zipos_list(E9WasmZipCallback callback, void *userdata);
const char *e9wasm_get_exe_path(void);  // For self-modification

// Zero-copy binary mapping
void *e9wasm_mmap_binary(const char *zip_path, size_t *out_size, bool writable);
```

### 2.5 E9Studio IDE Protocol (`e9ide_protocol.h`)

**File:** `C:\e9studio\src\e9patch\ide\e9ide_protocol.h`

JSON-RPC protocol for IDE integration (like LSP but for RE):
```c
// Method names
#define E9IDE_METHOD_GET_DECOMPILE   "analysis/getDecompilation"
#define E9IDE_METHOD_PATCH_APPLY     "patch/apply"
#define E9IDE_METHOD_PATCH_SAVE      "patch/save"

// Capabilities advertised
E9IDE_CAP_DECOMPILATION     = 0x0002
E9IDE_CAP_PATCHING          = 0x0008
E9IDE_CAP_LIVE_EDIT         = 0x0020
E9IDE_CAP_WASM_PLUGINS      = 0x0080
E9IDE_CAP_APE               = 0x2000
```

### 2.6 E9Studio Polyglot Analysis (`e9polyglot.h`)

**File:** `C:\e9studio\src\e9patch\analysis\e9polyglot.h`

APE-aware analysis including ZipOS parsing:
```c
// APE-specific structure
typedef struct {
    uint64_t dos_header;
    uint64_t elf_offset;
    uint64_t pe_offset;
    uint64_t shell_offset;
    uint64_t macho_offset;
    uint64_t zipos_start;
    uint64_t zipos_central_dir;
    // ...
} E9APELayout;

int e9_ape_parse(const uint8_t *data, size_t size, E9APELayout *layout);
uint8_t *e9_ape_extract_elf(const uint8_t *data, size_t size, size_t *out_size);
```

### 2.7 tedit-cosmo Disassembly View (`disasm_view.h`)

**File:** `C:\tedit-cosmo\include\disasm_view.h`

Editor-integrated disassembly already designed for binary viewing:
```c
// Section navigation
size_t disasm_view_section_count(DisasmView *view);
const DisasmSection *disasm_view_get_section(DisasmView *view, size_t index);

// Symbol lookup
const DisasmSymbol *disasm_view_symbol_at(DisasmView *view, uint64_t address);
size_t disasm_view_find_symbols(DisasmView *view, const char *prefix, ...);

// XRef analysis (basic)
size_t disasm_view_get_xrefs_to(DisasmView *view, uint64_t address, ...);
```

---

## 3. Integration Opportunities

### 3.1 Existing Infrastructure Mapping

```
┌─────────────────────────────────────────────────────────────────────┐
│                       EXISTING PIECES                               │
├─────────────────────────────────────────────────────────────────────┤
│ tedit-cosmo                    e9studio                             │
│ ┌─────────────────────┐       ┌─────────────────────────────┐      │
│ │ editor.h            │       │ e9analysis.h (CFG, symbols) │      │
│ │ disasm_view.h ──────┼───────┼─► e9decompile.h (C output)  │      │
│ │ history.h           │       │ e9binpatch.h (patching)     │      │
│ │ syntax.h            │       │ e9wasm_host.h (WAMR JIT)    │      │
│ │ buffer.h            │       │ e9ide_protocol.h (LSP-like) │      │
│ └─────────────────────┘       │ e9polyglot.h (APE parsing)  │      │
│                               └─────────────────────────────┘      │
│                                                                     │
│ llamafile                     cosmokramerpolitan                    │
│ ┌─────────────────────┐       ┌─────────────────────────────┐      │
│ │ OpenAI-compatible   │       │ ape/loader.c (bootstrap)    │      │
│ │ API on :8080/v1     │       │ ZipOS (/zip/ filesystem)    │      │
│ │ GGUF model loading  │       │ cosmocc (portable compiler) │      │
│ │ GPU acceleration    │       │ third_party/xed (disasm)    │      │
│ └─────────────────────┘       └─────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 Proposed Integration Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                    COSMO-RE-STACK.COM (Single APE)                 │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ UI Layer (tedit-cosmo derived)                                │ │
│  │  - Source editor (C/ASM)                                      │ │
│  │  - Disassembly view (integrated e9studio)                     │ │
│  │  - Decompiler pane (e9decompile output)                       │ │
│  │  - Patch queue (pending changes)                              │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                              │                                     │
│  ┌───────────────────────────┼────────────────────────────────┐   │
│  │ Analysis Engine (e9studio)│                                │   │
│  │  - e9_binary_analyze()    │                                │   │
│  │  - e9_cfg_build()         │                                │   │
│  │  - e9_decompile_function()│                                │   │
│  │  - e9_binpatch_*()        │                                │   │
│  └───────────────────────────┼────────────────────────────────┘   │
│                              │                                     │
│  ┌───────────────────────────┼────────────────────────────────┐   │
│  │ Compilation Layer         │                                │   │
│  │  - WAMR Fast JIT (patches) ← e9wasm_host                   │   │
│  │  - cosmocc (if full rebuild needed)                        │   │
│  │  - Trampoline generation                                   │   │
│  └───────────────────────────┼────────────────────────────────┘   │
│                              │                                     │
│  ┌───────────────────────────┼────────────────────────────────┐   │
│  │ LLM Assistance (llamafile)│                                │   │
│  │  - Decompile enhancement (POST /v1/chat/completions)       │   │
│  │  - Variable naming suggestions                              │   │
│  │  - Vulnerability analysis                                   │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                    │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │ ZipOS Embedded Files                                        │   │
│  │  /zip/e9patch.wasm          (core rewriter logic)          │   │
│  │  /zip/plugins/*.wasm        (analysis plugins)             │   │
│  │  /zip/model.gguf            (optional LLM weights)         │   │
│  │  /zip/target/*              (binaries under analysis)      │   │
│  └────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────┘
```

---

## 4. What is cosmobsd? (Research Finding)

### Answer: cosmobsd is NOT a separate project.

**Finding:** "cosmobsd" does not exist as a standalone repository or tool. The search for BSD-related files in `C:\cosmokramerpolitan` reveals:

```
libc\bsdstdlib.h
libc\calls\openbsd.internal.h
libc\calls\sigenter-freebsd.c
libc\calls\sigenter-netbsd.c
libc\calls\sigenter-openbsd.c
...
```

**Conclusion:** BSD support is integrated *within* Cosmopolitan Libc itself. The project supports:
- FreeBSD 13+
- OpenBSD 7.3+
- NetBSD 9.2+

All BSD support is in `libc/calls/` with platform-specific syscall implementations. There is no separate "cosmobsd" project to integrate.

---

## 5. Gaps Identified (What's MISSING)

### 5.1 Critical Missing Components

| Gap | Description | Effort Est. |
|-----|-------------|-------------|
| **Glue Layer** | No existing bridge between tedit-cosmo and e9studio | 2-3 weeks |
| **LLM Decompile Integration** | e9decompile → llamafile pipeline not implemented | 1 week |
| **WASM Patch Compiler** | WAMR JIT exists, but C→WASM→Native pipeline missing | 2-3 weeks |
| **Multi-format Output** | e9patch only outputs ELF; PE/Mach-O/APE patching needed | 3-4 weeks |
| **Cross-architecture** | e9patch is x86-64 only; AArch64 analysis exists but not patching | 4-6 weeks |

### 5.2 Feature Gaps vs Ghidra

| Feature | Ghidra | e9studio | Gap |
|---------|--------|----------|-----|
| Scripting | Java/Python | ❌ Missing | Need WASM or embedded Lua |
| Type recovery | Comprehensive | Basic | No struct/vtable detection |
| Symbolic execution | PCode | ❌ Missing | Significant effort |
| Version control | Git integration | ❌ Missing | Patch history needed |
| Collaboration | Ghidra Server | ❌ Missing | Not critical for v1 |

### 5.3 API Gaps in Existing Code

```c
// e9decompile.h - missing implementation stubs found:
int e9_decompile_structure(E9Decompile *dc, E9IRFunc *func);  // goto→structured
int e9_decompile_infer_types(E9Decompile *dc, E9IRFunc *func);  // type propagation

// e9binpatch.h - PE/Mach-O not implemented:
// Only ELF code caves and trampolines exist
// PE section handling: NOT IMPLEMENTED
// Mach-O segment handling: NOT IMPLEMENTED

// e9wasm_host.h - placeholder:
// WAMR integration is configured but minimal stub implementation
```

---

## 6. Recommendations

### 6.1 Immediate Priorities (Week 1-2)

1. **Create thin integration layer** between tedit-cosmo and e9studio
   - Expose `e9_binary_*` APIs through tedit's disasm_view
   - Add "Analyze Binary" menu item

2. **Test llamafile API integration**
   - POST decompiled C to `/v1/chat/completions`
   - Prompt: "Improve this decompiled code, suggest better variable names"

### 6.2 Short-term (Month 1)

3. **Implement WASM patch compilation**
   - Source edit → cosmocc → object → WAMR JIT
   - Use existing `e9_diff_objects()` for delta detection

4. **Add PE patching to e9binpatch**
   - Leverage existing PE parsing in `e9pe.cpp`
   - Port ELF cave-finding to PE sections

### 6.3 Medium-term (Month 2-3)

5. **Self-modifying APE support**
   - Use `e9wasm_zipos_append()` to store patches
   - Create `/zip/patches/*.patch` format

6. **LLM-enhanced analysis**
   - Function signature guessing
   - Vulnerability pattern recognition
   - "What does this function do?" queries

---

## 7. Source Citations

| Source | Location | Key APIs/Features |
|--------|----------|-------------------|
| tedit-cosmo README | `C:\tedit-cosmo\README.md` | Philosophy, INI extensibility |
| e9patch README | `C:\e9studio\README.md` | PLDI'2020 paper reference |
| cosmopolitan README | `C:\cosmokramerpolitan\README.md` | cosmocc, APE format |
| e9analysis.h | `C:\e9studio\src\e9patch\analysis\e9analysis.h` | Binary analysis APIs |
| e9decompile.h | `C:\e9studio\src\e9patch\analysis\e9decompile.h` | Decompiler IR and APIs |
| e9binpatch.h | `C:\e9studio\src\e9patch\analysis\e9binpatch.h` | Patching session APIs |
| e9wasm_host.h | `C:\e9studio\src\e9patch\wasm\e9wasm_host.h` | WAMR integration |
| e9ide_protocol.h | `C:\e9studio\src\e9patch\ide\e9ide_protocol.h` | IDE protocol spec |
| e9polyglot.h | `C:\e9studio\src\e9patch\analysis\e9polyglot.h` | APE parsing |
| disasm_view.h | `C:\tedit-cosmo\include\disasm_view.h` | Editor disasm integration |
| wamr_config.h | `C:\e9studio\src\e9patch\vendor\wamr\wamr_config.h` | WAMR feature flags |
| ape-anatomy-analysis.md | `C:\e9studio\doc\ape-anatomy-analysis.md` | APE structure docs |
| cosmopolitan-port.md | `C:\e9studio\doc\cosmopolitan-port.md` | Integration architecture |
| llamafile-help.txt | `C:\llamafile-llm\llamafile-help.txt` | CLI/API reference |

---

## 8. Conclusion

The cosmo-re-stack vision is **achievable with current components**. The major pieces exist:
- **Editing:** tedit-cosmo (with disasm_view ready for extension)
- **Analysis:** e9studio (comprehensive API surface)
- **JIT:** WAMR integration exists, needs pipeline completion
- **LLM:** llamafile provides ready API, just needs integration
- **Portability:** Cosmopolitan/APE handles universal binary output

**Primary work needed:** Integration glue, not new capabilities. The hardest remaining work is:
1. PE/Mach-O patching (ELF-only today)
2. Structured decompilation improvements
3. UI/UX polish in tedit-cosmo

**Recommended next step:** Create a proof-of-concept that:
1. Opens an APE in tedit-cosmo
2. Calls e9studio analysis APIs
3. Shows decompiled C alongside disassembly
4. Allows edit → recompile → inject cycle

---

*Report generated by seeker agent, Swiss Rounds methodology*
