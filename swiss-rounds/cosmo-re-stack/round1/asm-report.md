# Cosmo RE Stack - Round 1 Assembly Report

**Generated:** 2026-02-10
**Analyst:** asm-specialist (Claude)
**Domain:** Assembly, disassembly, machine code, CPU architectures, binary formats

---

## Executive Summary

The Cosmo RE Stack consists of four integrated projects forming a universal binary reverse engineering workstation:

| Project | Purpose | Architecture Support | Status |
|---------|---------|---------------------|--------|
| **cosmo-disasm** | Disassembler library | x86-64 ✅, AArch64 ✅, x86-32 ⚠️, ARM32 🚧 | Complete |
| **e9studio** | Binary analysis + WAMR patching | x86-64 ✅, AArch64 ⚠️ | Active development |
| **tedit-cosmo** | Portable systems editor | Via cosmo-disasm | Complete |
| **llamafile-llm** | LLM runtime (JIT aspects) | x86-64, AArch64 | Reference only |

**Vision:** Universal binary RE workstation where WAMR JIT compiles patches → e9-style injection into ANY binary (ELF/PE/Mach-O/APE). Not just Linux ELF like vanilla e9patch.

---

## Source Manifest: cosmo-disasm

**Repository:** `C:\cosmo-disasm`
**License:** ISC

### Public API (`include/cosmo_disasm.h`)

#### Architecture Enumeration

| Name | Value | Purpose | Line |
|------|-------|---------|------|
| `CosmoArch` | enum | Architecture selector | 34-39 |
| `COSMO_ARCH_UNKNOWN` | 0 | Unknown/unsupported | 35 |
| `COSMO_ARCH_X86_64` | 1 | AMD64/x86-64 | 36 |
| `COSMO_ARCH_AARCH64` | 2 | ARM64/AArch64 | 37 |
| `COSMO_ARCH_X86_32` | 3 | i386/x86 32-bit | 38 |
| `COSMO_ARCH_ARM32` | 4 | ARM 32-bit (future) | 39 |

#### Core Disassembly Functions

| Function | Signature | File | Line | Purpose |
|----------|-----------|------|------|---------|
| `cosmo_disasm_create` | `CosmoDisasm *(CosmoArch arch)` | `cosmo_disasm.h` | 152 | Create disassembler context |
| `cosmo_disasm_free` | `void(CosmoDisasm *ctx)` | `cosmo_disasm.h` | 153 | Destroy context |
| `cosmo_disasm_set_arch` | `void(CosmoDisasm *ctx, CosmoArch arch)` | `cosmo_disasm.h` | 156 | Change architecture |
| `cosmo_disasm_get_arch` | `CosmoArch(const CosmoDisasm *ctx)` | `cosmo_disasm.h` | 157 | Get current architecture |
| `cosmo_disasm_one` | `int(CosmoDisasm *ctx, const uint8_t *code, size_t size, uint64_t address, CosmoInsn *insn)` | `cosmo_disasm.h` | 166 | Disassemble single instruction |
| `cosmo_disasm_many` | `size_t(CosmoDisasm *ctx, const uint8_t *code, size_t size, uint64_t address, size_t max_count, CosmoInsn **insns)` | `cosmo_disasm.h` | 173 | Disassemble multiple instructions |
| `cosmo_disasm_free_insns` | `void(CosmoInsn *insns, size_t count)` | `cosmo_disasm.h` | 179 | Free instruction array |

#### Analysis Helpers

| Function | Signature | File | Line | Purpose |
|----------|-----------|------|------|---------|
| `cosmo_is_prologue` | `bool(CosmoArch arch, const uint8_t *code, size_t size)` | `cosmo_disasm.h` | 186 | Detect function prologue |
| `cosmo_is_epilogue` | `bool(CosmoArch arch, const uint8_t *code, size_t size)` | `cosmo_disasm.h` | 189 | Detect function epilogue |
| `cosmo_insn_length` | `int(CosmoArch arch, const uint8_t *code, size_t size)` | `cosmo_disasm.h` | 192 | Get instruction length without full decode |
| `cosmo_insn_writes_reg` | `bool(const CosmoInsn *insn, int reg_id)` | `cosmo_disasm.h` | 195 | Check if instruction writes register |
| `cosmo_insn_reads_reg` | `bool(const CosmoInsn *insn, int reg_id)` | `cosmo_disasm.h` | 196 | Check if instruction reads register |

#### Architecture Detection

| Function | Signature | File | Line | Purpose |
|----------|-----------|------|------|---------|
| `cosmo_detect_arch_elf` | `CosmoArch(const uint8_t *data, size_t size)` | `cosmo_disasm.h` | 212 | Detect arch from ELF header |
| `cosmo_detect_arch_pe` | `CosmoArch(const uint8_t *data, size_t size)` | `cosmo_disasm.h` | 213 | Detect arch from PE header |
| `cosmo_detect_arch_ape` | `CosmoArch(const uint8_t *data, size_t size)` | `cosmo_disasm.h` | 216 | Detect arch from APE binary |

### Core Data Structures

#### `CosmoInsn` (Line 117-145)

```c
typedef struct {
    uint64_t address;
    uint8_t bytes[COSMO_MAX_INSN_LEN];  // Max 15 bytes
    int length;
    
    char mnemonic[32];
    char text[128];                     // Full formatted instruction
    
    CosmoInsnCategory category;
    CosmoArch arch;
    
    int num_operands;
    CosmoOperand operands[COSMO_MAX_OPERANDS];  // Max 4 operands
    
    bool is_branch;
    bool is_call;
    bool is_return;
    bool is_conditional;
    uint64_t branch_target;
    
    bool reads_memory;
    bool writes_memory;
    
    // x86-specific
    bool has_lock;
    bool has_rep;
    bool has_rex;
    uint8_t rex;
    
    // ARM-specific
    uint32_t encoding;                  // Full 32-bit instruction word
} CosmoInsn;
```

### x86-64 Backend (`src/cosmo_disasm_x86.c`)

| Function | Line | Purpose |
|----------|------|---------|
| `cosmo_x86_disasm_create` | 115 | Create x86 context (mode: 16/32/64) |
| `cosmo_x86_disasm_free` | 131 | Free x86 context |
| `cosmo_x86_disasm_set_mode` | 136 | Switch between 16/32/64-bit mode |
| `cosmo_x86_disasm_one` | 210 | Disassemble single x86 instruction |
| `cosmo_x86_reg_name` | 142 | Get register name string |
| `cosmo_x86_reg_size` | 151 | Get register size in bytes |
| `cosmo_x86_is_prologue` | 550 | Detect x86 function prologue |
| `cosmo_x86_is_epilogue` | 573 | Detect x86 function epilogue |
| `cosmo_x86_insn_length` | 590 | Get instruction length |

**Implemented x86 Instructions:**
- NOP (0x90, multi-byte 0F 1F)
- PUSH/POP reg (0x50-0x5F)
- MOV r,imm (0xB8-0xBF), MOV r/m,r (0x89), MOV r,r/m (0x8B)
- LEA (0x8D)
- CALL rel32 (0xE8), JMP rel32/rel8 (0xE9, 0xEB)
- Jcc rel8/rel32 (0x70-0x7F, 0x0F 0x80-0x8F)
- RET (0xC3), LEAVE (0xC9)
- XOR r/m,r (0x31), ADD/SUB/AND/OR/XOR/CMP imm8 (0x83)
- TEST r/m,r (0x85), CMP r/m,r (0x39)
- SYSCALL (0x0F 0x05), CPUID (0x0F 0xA2)
- INT3 (0xCC), HLT (0xF4)

### AArch64 Backend (`src/cosmo_disasm_arm64.c`)

| Function | Line | Purpose |
|----------|------|---------|
| `cosmo_a64_disasm_create` | 54 | Create ARM64 context |
| `cosmo_a64_disasm_free` | 60 | Free ARM64 context |
| `cosmo_a64_disasm_one` | 126 | Disassemble single ARM64 instruction |
| `cosmo_a64_reg_name` | 64 | Get register name string |
| `cosmo_a64_reg_size` | 75 | Get register size in bytes |
| `cosmo_a64_is_prologue` | 413 | Detect ARM64 function prologue |
| `cosmo_a64_is_epilogue` | 430 | Detect ARM64 function epilogue |

**Implemented ARM64 Instructions:**
- PC-relative: ADR, ADRP
- Add/Sub immediate: ADD, ADDS, SUB, SUBS, CMP (alias)
- Move wide: MOVN, MOVZ, MOVK
- Unconditional branch: B, BL
- Compare and branch: CBZ, CBNZ
- Conditional branch: B.cond (eq, ne, cs, cc, mi, pl, vs, vc, hi, ls, ge, lt, gt, le)
- Test and branch: TBZ, TBNZ
- Branch register: BR, BLR, RET
- Load/Store: LDR, STR (unsigned immediate), LDP, STP
- Logical: AND, ORR, EOR, BIC, ORN, EON, ANDS, BICS, MOV (alias)
- Add/Sub register: ADD, ADDS, SUB, SUBS, CMP
- System: NOP, YIELD, WFE, WFI, SEV, SEVL, DSB, DMB, ISB, CLREX, MSR, MRS
- Exception: SVC, HVC, SMC, BRK, HLT
- PAC: PACIASP, PACIBSP (prologue), RETAA, RETAB (epilogue)

---

## Source Manifest: e9studio

**Repository:** `C:\e9studio`
**License:** GPLv3+

### Directory Structure

```
e9studio/
├── src/
│   ├── e9patch/           # Core patching engine
│   │   ├── analysis/      # Analysis engine
│   │   ├── ide/           # IDE integration
│   │   ├── platform/      # Platform abstraction
│   │   ├── vendor/        # Vendored dependencies
│   │   ├── wasm/          # WAMR integration
│   │   ├── e9elf.cpp      # ELF handling
│   │   ├── e9pe.cpp       # PE handling
│   │   └── ...
│   └── e9tool/            # Frontend tool
└── Makefile.cosmo         # Cosmopolitan build
```

### WAMR Integration API (`src/e9patch/wasm/e9wasm_host.h`)

#### Configuration

```c
typedef struct {
    size_t stack_size;          // WASM stack size (default: 64KB)
    size_t heap_size;           // WASM heap size (default: 16MB)
    size_t shared_buffer_size;  // Shared buffer for binary data (default: 64MB)
    bool enable_wasi;           // Enable WASI imports
    bool enable_debug;          // Enable debug logging
    const char *module_path;    // Path to main WASM module (in ZipOS)
} E9WasmConfig;
```

#### Execution Modes

| Mode | Value | Description |
|------|-------|-------------|
| `E9_WASM_MODE_INTERP` | 0 | Fast interpreter (portable) |
| `E9_WASM_MODE_FAST_JIT` | 1 | Fast JIT compilation (default) |
| `E9_WASM_MODE_AOT` | 2 | Ahead-of-time compiled |

#### Core Functions

| Function | Signature | Line | Purpose |
|----------|-----------|------|---------|
| `e9wasm_set_exec_mode` | `void(int mode)` | 30 | Set JIT/interpreter mode BEFORE init |
| `e9wasm_init` | `int(const E9WasmConfig *config)` | 36 | Initialize WAMR runtime |
| `e9wasm_shutdown` | `void(void)` | 41 | Shutdown WAMR runtime |
| `e9wasm_load_module` | `void *(const char *path)` | 47 | Load WASM module from ZipOS |
| `e9wasm_call` | `int(void *module, const char *func_name, int argc, const char *argv[])` | 53 | Call exported WASM function |
| `e9wasm_get_shared_buffer` | `uint8_t *(size_t *out_size)` | 59 | Get shared buffer for binary data |
| `e9wasm_load_binary` | `size_t(const char *zip_path)` | 65 | Load binary from ZipOS into shared buffer |
| `e9wasm_mmap_binary` | `void *(const char *zip_path, size_t *out_size, bool writable)` | 71 | Memory-map binary (zero-copy) |
| `e9wasm_munmap_binary` | `void(void *addr, size_t size)` | 76 | Unmap binary |
| `e9wasm_apply_patch` | `int(void *mapped, size_t offset, const uint8_t *data, size_t size)` | 83 | Apply patch to mapped binary |
| `e9wasm_flush_icache` | `void(void *addr, size_t size)` | 88 | Flush instruction cache after patching |

#### ZipOS Integration

| Function | Signature | Line | Purpose |
|----------|-----------|------|---------|
| `e9wasm_zipos_available` | `int(void)` | 113 | Check if ZipOS is accessible |
| `e9wasm_zipos_file_exists` | `int(const char *name)` | 120 | Safe existence check |
| `e9wasm_zipos_read` | `uint8_t *(const char *name, size_t *out_size)` | 127 | Read file from ZipOS |
| `e9wasm_zipos_append` | `int(const char *name, const uint8_t *data, size_t size)` | 102 | Append to APE's own ZipOS |

### Analysis Engine API (`src/e9patch/analysis/e9analysis.h`)

#### Binary Analysis

| Function | Signature | Line | Purpose |
|----------|-----------|------|---------|
| `e9_binary_create` | `E9Binary *(const uint8_t *data, size_t size)` | 217 | Create from memory |
| `e9_binary_open` | `E9Binary *(const char *path)` | 222 | Open from file |
| `e9_binary_free` | `void(E9Binary *bin)` | 227 | Free context |
| `e9_binary_detect` | `int(E9Binary *bin)` | 232 | Detect architecture and format |
| `e9_binary_analyze` | `int(E9Binary *bin)` | 237 | Run full analysis pipeline |

#### Disassembly (e9analysis internal)

| Function | Signature | Line | Purpose |
|----------|-----------|------|---------|
| `e9_disasm_instruction` | `E9Instruction *(E9Binary *bin, uint64_t addr)` | 246 | Disassemble single (allocates) |
| `e9_disasm` | `int(E9Binary *bin, uint64_t addr, E9Instruction *insn)` | 252 | Disassemble into provided struct |
| `e9_disasm_range` | `E9Instruction *(E9Binary *bin, uint64_t start, uint64_t end)` | 258 | Disassemble address range |
| `e9_disasm_str` | `const char *(E9Binary *bin, E9Instruction *insn, char *buf, size_t bufsize)` | 263 | Format instruction string |

#### CFG and Decompilation

| Function | Signature | Line | Purpose |
|----------|-----------|------|---------|
| `e9_cfg_build` | `E9CFG *(E9Binary *bin, E9Function *func)` | 302 | Build control flow graph |
| `e9_cfg_free` | `void(E9CFG *cfg)` | 307 | Free CFG |
| `e9_cfg_to_dot` | `int(E9CFG *cfg, const char *path)` | 312 | Export to DOT format |
| `e9_decompile_function` | `char *(E9Binary *bin, E9Function *func)` | 322 | Decompile to C |
| `e9_decompile_block` | `char *(E9Binary *bin, E9BasicBlock *block)` | 327 | Decompile basic block |
| `e9_generate_header` | `char *(E9Binary *bin)` | 332 | Generate C header |
| `e9_generate_source` | `char *(E9Binary *bin)` | 337 | Generate complete C source |

### Decompiler Engine (`src/e9patch/analysis/e9decompile.h`)

#### IR Operations

| Category | Operations |
|----------|------------|
| Constants/Variables | `E9_IR_CONST`, `E9_IR_REG`, `E9_IR_LOCAL`, `E9_IR_GLOBAL`, `E9_IR_PARAM`, `E9_IR_TEMP` |
| Memory | `E9_IR_LOAD`, `E9_IR_STORE` |
| Arithmetic | `E9_IR_ADD`, `E9_IR_SUB`, `E9_IR_MUL`, `E9_IR_DIV`, `E9_IR_MOD`, `E9_IR_NEG` |
| Bitwise | `E9_IR_AND`, `E9_IR_OR`, `E9_IR_XOR`, `E9_IR_NOT`, `E9_IR_SHL`, `E9_IR_SHR`, `E9_IR_SAR` |
| Comparison | `E9_IR_EQ`, `E9_IR_NE`, `E9_IR_LT`, `E9_IR_LE`, `E9_IR_GT`, `E9_IR_GE`, `E9_IR_LTU`, `E9_IR_LEU`, `E9_IR_GTU`, `E9_IR_GEU` |
| Type Conversion | `E9_IR_CAST`, `E9_IR_SEXT`, `E9_IR_ZEXT`, `E9_IR_TRUNC` |
| Control Flow | `E9_IR_CALL`, `E9_IR_RET`, `E9_IR_BRANCH`, `E9_IR_GOTO` |
| Special | `E9_IR_PHI`, `E9_IR_ADDRESS`, `E9_IR_DEREF`, `E9_IR_MEMBER`, `E9_IR_INDEX` |

#### Structured Control Flow

| Type | C Equivalent |
|------|--------------|
| `E9_STRUCT_SEQ` | Sequential execution |
| `E9_STRUCT_IF` | `if (cond) { } else { }` |
| `E9_STRUCT_WHILE` | `while (cond) { }` |
| `E9_STRUCT_DOWHILE` | `do { } while (cond)` |
| `E9_STRUCT_FOR` | `for (;;) { }` |
| `E9_STRUCT_SWITCH` | `switch (expr) { }` |
| `E9_STRUCT_BREAK` | `break;` |
| `E9_STRUCT_CONTINUE` | `continue;` |

#### Decompiler API

| Function | Signature | Line | Purpose |
|----------|-----------|------|---------|
| `e9_decompile_create` | `E9Decompile *(E9Binary *bin, const E9DecompileOpts *opts)` | 178 | Create decompiler |
| `e9_decompile_free` | `void(E9Decompile *dc)` | 183 | Free decompiler |
| `e9_decompile_lift` | `E9IRFunc *(E9Decompile *dc, E9Function *func)` | 188 | Lift to IR |
| `e9_decompile_structure` | `int(E9Decompile *dc, E9IRFunc *func)` | 193 | Convert gotos to structured control flow |
| `e9_decompile_infer_types` | `int(E9Decompile *dc, E9IRFunc *func)` | 198 | Type inference pass |
| `e9_decompile_emit_c` | `char *(E9Decompile *dc, E9IRFunc *func)` | 203 | Generate C code from IR |
| `e9_decompile_function_full` | `char *(E9Decompile *dc, E9Function *func)` | 208 | Full pipeline |
| `e9_decompile_binary` | `char *(E9Decompile *dc)` | 213 | Decompile entire binary |

### Binary Format Support

#### ELF (`src/e9patch/e9elf.h`)

| Function | Signature | Purpose |
|----------|-----------|---------|
| `parseElf` | `bool(Binary *B)` | Parse ELF file |
| `emitElf` | `size_t(Binary *B, const MappingSet &mappings, size_t mapping_size)` | Emit patched ELF |
| `emitLoaderMap` | `size_t(uint8_t *data, intptr_t addr, size_t len, off_t offset, bool r, bool w, bool x, uint32_t type, intptr_t *ub)` | Emit loader map entry |

#### PE (`src/e9patch/e9pe.h`)

| Function | Signature | Purpose |
|----------|-----------|---------|
| `parsePE` | `void(Binary *B)` | Parse PE file |
| `emitPE` | `size_t(Binary *B, const MappingSet &mappings, size_t mapping_size)` | Emit patched PE |

### Polyglot Support (`src/e9patch/analysis/e9polyglot.h`)

| Function | Signature | Line | Purpose |
|----------|-----------|------|---------|
| `e9_polyglot_analyze` | `E9PolyglotAnalysis *(const uint8_t *data, size_t size)` | 122 | Detect polyglot properties |
| `e9_is_ape` | `bool(const uint8_t *data, size_t size)` | 134 | Check for APE format |
| `e9_signature_scan` | `E9FormatRegion *(const uint8_t *data, size_t size)` | 149 | Binwalk-style signature scan |
| `e9_entropy_analyze` | `E9EntropyResult(const uint8_t *data, size_t size)` | 168 | Shannon entropy analysis |
| `e9_ape_parse` | `int(const uint8_t *data, size_t size, E9APELayout *layout)` | 216 | Parse APE structure |
| `e9_ape_extract_elf` | `uint8_t *(const uint8_t *data, size_t size, size_t *out_size)` | 221 | Extract ELF from APE |
| `e9_ape_extract_pe` | `uint8_t *(const uint8_t *data, size_t size, size_t *out_size)` | 222 | Extract PE from APE |
| `e9_ape_extract_zipos` | `uint8_t *(const uint8_t *data, size_t size, size_t *out_size)` | 223 | Extract ZipOS from APE |

---

## WAMR JIT Integration Analysis

### How WAMR JIT Compiles Patches

The WAMR integration in e9studio uses three execution modes:

1. **Fast Interpreter** (`Mode_Fast_Interp`): Portable, works everywhere
2. **Fast JIT** (`Mode_Fast_JIT`): JIT compilation without LLVM dependency (default)
3. **AOT** (`Mode_LLVM_AOT`): Pre-compiled native code

**Runtime Initialization Flow:**

```
e9wasm_init()
  ├── wasm_runtime_full_init() with running_mode
  ├── Register native host functions (zipos_read, apply_patch, etc.)
  ├── Allocate shared buffer via mmap (64MB default)
  └── Store executable path for self-modification
```

**Patch Application Flow:**

```
e9wasm_load_module("/zip/e9patch.wasm")
  ├── Read WASM from ZipOS
  ├── wasm_runtime_load() → parse WASM
  ├── wasm_runtime_instantiate() → create memory
  └── wasm_runtime_create_exec_env() → JIT if enabled

e9wasm_call(module, "apply_patches", ...)
  ├── JIT compiles function on first call (Fast JIT mode)
  ├── WASM calls native_apply_patch() via host function
  │   └── Writes patch bytes to shared_buffer at offset
  └── WASM calls native_flush_icache() to synchronize
```

**Native Host Functions Registered:**

| Function | Signature | Purpose |
|----------|-----------|---------|
| `zipos_read` | `(iiii)i` | Read from ZipOS into WASM memory |
| `apply_patch` | `(iii)i` | Apply patch to shared buffer |
| `get_shared_buffer_info` | `(i)i` | Get buffer address/size |
| `log` | `(ii)` | Log message from WASM |
| `flush_icache` | `(ii)` | Flush instruction cache |

### Architecture Support in JIT

**x86-64 JIT:**
- WAMR Fast JIT generates x86-64 machine code directly
- `e9wasm_flush_icache()` is no-op (x86 has coherent I/D cache)

**AArch64 JIT:**
- WAMR generates ARM64 code
- `e9wasm_flush_icache()` calls `__builtin___clear_cache()`
- Required because ARM64 has separate I/D caches

---

## Pipeline: cosmo-disasm → e9studio → tedit-cosmo

### Integration Points

```
┌─────────────────────────────────────────────────────────────────┐
│ tedit-cosmo (src/disasm_view.c)                                 │
│   • detect_arch() → cosmo_detect_arch_{elf,pe,ape}()           │
│   • cosmo_disasm_create(arch) → get context                    │
│   • cosmo_disasm_one() → fill DisasmLine for display           │
│   • Fallback: stub disasm without library                      │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ cosmo-disasm (unified API)                                      │
│   • CosmoDisasm context holds arch-specific backends           │
│   • Routes to cosmo_x86_disasm_one() or cosmo_a64_disasm_one() │
│   • Returns CosmoInsn with unified fields                      │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ e9studio (analysis layer)                                       │
│   • e9_binary_analyze() uses cosmo-disasm for raw disassembly  │
│   • E9Function discovery via prologue detection                 │
│   • E9CFG construction from disassembly                         │
│   • e9_decompile_* lifts to IR, structures, emits C            │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ e9studio (patching layer)                                       │
│   • WAMR loads e9patch.wasm from ZipOS                         │
│   • JIT compiles patch logic                                    │
│   • Applies patches via trampoline generation                   │
│   • Emits ELF/PE/APE with modifications                        │
└─────────────────────────────────────────────────────────────────┘
```

### tedit-cosmo Disasm View (`src/disasm_view.c`)

Key integration with cosmo-disasm:

```c
#ifdef HAVE_COSMO_DISASM
#include <cosmo_disasm.h>
#endif

// Architecture mapping
switch (view->arch) {
case DISASM_ARCH_X86_64:  cosmo_arch = COSMO_ARCH_X86_64; break;
case DISASM_ARCH_AARCH64: cosmo_arch = COSMO_ARCH_AARCH64; break;
default:                  cosmo_arch = COSMO_ARCH_X86_64; break;
}

view->disasm = cosmo_disasm_create(cosmo_arch);

// Disassembly
CosmoInsn insn;
int len = cosmo_disasm_one(view->disasm, 
                           view->data + offset, remaining,
                           vaddr, &insn);
```

---

## Architecture Support Gaps

### Current State

| Feature | x86-64 | x86-32 | AArch64 | ARM32 |
|---------|--------|--------|---------|-------|
| **cosmo-disasm** |
| Basic disassembly | ✅ | ⚠️ Partial | ✅ | ❌ |
| ModR/M decoding | ✅ | ✅ | N/A | N/A |
| SIB decoding | ✅ | ✅ | N/A | N/A |
| REX prefixes | ✅ | N/A | N/A | N/A |
| Prologue detection | ✅ | ❌ | ✅ | ❌ |
| Epilogue detection | ✅ | ❌ | ✅ | ❌ |
| **e9studio** |
| ELF parsing | ✅ | ✅ | ✅ | ✅ |
| PE parsing | ✅ | ✅ | ⚠️ | ❌ |
| Mach-O parsing | ⚠️ | ❌ | ⚠️ | ❌ |
| APE parsing | ✅ | N/A | ⚠️ | N/A |
| Trampoline generation | ✅ | ⚠️ | ❌ | ❌ |
| WAMR JIT | ✅ | ⚠️ | ✅ | ❌ |
| **tedit-cosmo** |
| Disasm view | ✅ | ⚠️ | ✅ | ❌ |

### Critical Gaps

1. **ARM32 disassembly**: `COSMO_ARCH_ARM32` defined but not implemented
   - Location: `src/cosmo_disasm.c` lines 45-46 (empty switch cases)
   - Impact: Cannot analyze 32-bit ARM binaries

2. **AArch64 trampoline generation**: e9patch core is x86-64 focused
   - Location: `src/e9patch/e9x86_64.cpp` — no ARM64 equivalent
   - Impact: Cannot apply e9-style patches to ARM64 binaries

3. **PE ARM64 support**: PE parsing exists but ARM64 untested
   - Machine type detection: 0xAA64 in `cosmo_detect_arch_pe()`
   - No corresponding trampoline generation

4. **Mach-O support**: Format detection exists but no patching
   - Would require new `e9macho.cpp` module

### Recommended Priority

1. **High**: ARM32 disassembler backend (complete instruction set coverage)
2. **High**: AArch64 trampoline generation for e9patch
3. **Medium**: Mach-O patching support
4. **Medium**: Complete x86-32 instruction coverage
5. **Low**: RISC-V support (future architecture)

---

## Cosmopolitan Type Mappings

From `e9decompile.h`, the decompiler maps register sizes to portable Cosmopolitan types:

| Size | Signed | Unsigned |
|------|--------|----------|
| 8-bit | `int8_t` | `uint8_t` |
| 16-bit | `int16_t` | `uint16_t` |
| 32-bit | `int32_t` | `uint32_t` |
| 64-bit | `int64_t` | `uint64_t` |
| Pointer | `void *` | Typed pointer |

Helper function: `e9_type_to_cosmo(int size_bits, bool is_signed, bool is_pointer)`

---

## What Does NOT Exist

Based on source analysis, the following expected features are NOT implemented:

### cosmo-disasm
- ❌ `cosmo_disasm_arm32_*()` — ARM32 backend stub only
- ❌ AVX/AVX-512 instruction decode for x86
- ❌ Thumb mode for ARM
- ❌ VFP/NEON instruction decode for ARM64

### e9studio
- ❌ `e9_aarch64_trampoline_*()` — No ARM64 trampolines
- ❌ `e9macho.cpp` — No Mach-O patching
- ❌ `e9_patch_apply_live()` — No in-memory patching (file-based only)
- ❌ Remote debugging integration (CDP stubs only)

### tedit-cosmo
- ❌ ARM32 view mode
- ❌ Mach-O section parsing

---

## Conclusion

The Cosmo RE Stack provides a solid foundation for universal binary analysis with:

- **Unified disassembly API** via cosmo-disasm (x86-64 and AArch64 complete)
- **WAMR JIT integration** for sandboxed patch execution
- **APE polyglot support** for truly portable reverse engineering tools
- **Decompilation to Cosmopolitan C** for readable output

**Primary gaps** are in architecture breadth (ARM32 missing) and cross-platform patching (ARM64 trampolines needed). The vision of universal binary RE is achievable with targeted implementation of:

1. ARM32 disassembler backend
2. AArch64 trampoline generation
3. Mach-O patching module

The WAMR JIT path is well-designed and provides the flexibility to run patch logic in either interpreted or JIT-compiled mode, with proper instruction cache handling for both x86-64 and ARM64.
