# cosmo-disasm Source Manifest

Generated: 2026-02-11
Source: https://github.com/ludoplex/cosmo-disasm
Path: `C:\cosmo-disasm`

## Overview

A lightweight, cross-platform disassembler library for x86-64 and AArch64, built with Cosmopolitan Libc. Zero dependencies, self-contained, produces Actually Portable Executables.

**Extracted from e9studio** — unified for use in tedit-cosmo, e9studio, and future llamafile-llm JIT introspection.

## API (`include/cosmo_disasm.h`)

### Types

| Type | Purpose |
|------|---------|
| `CosmoArch` | Architecture enum: `COSMO_ARCH_X86_64`, `COSMO_ARCH_AARCH64`, `COSMO_ARCH_X86_32` |
| `CosmoDisasm` | Opaque disassembler context |
| `CosmoInsn` | Disassembled instruction |
| `CosmoOp` | Instruction operand |
| `CosmoRegClass` | Unified register classes |
| `CosmoOpType` | Operand types: `REG`, `IMM`, `MEM`, `LABEL` |

### Core Functions

| Function | Signature | Purpose |
|----------|-----------|---------|
| `cosmo_disasm_create` | `(CosmoArch arch) -> CosmoDisasm*` | Create context |
| `cosmo_disasm_free` | `(CosmoDisasm *ctx)` | Free context |
| `cosmo_disasm_one` | `(ctx, code, size, addr, *insn) -> int` | Disassemble single instruction |
| `cosmo_disasm_block` | `(ctx, code, size, addr, *insns, max) -> int` | Disassemble block |

### Instruction Analysis

| Function | Signature | Purpose |
|----------|-----------|---------|
| `cosmo_insn_is_branch` | `(CosmoInsn *insn) -> bool` | Check if branch |
| `cosmo_insn_is_call` | `(CosmoInsn *insn) -> bool` | Check if call |
| `cosmo_insn_is_ret` | `(CosmoInsn *insn) -> bool` | Check if return |
| `cosmo_insn_is_prologue` | `(CosmoInsn *insn) -> bool` | Check if function prologue |
| `cosmo_insn_is_epilogue` | `(CosmoInsn *insn) -> bool` | Check if function epilogue |

### CosmoInsn Structure

```c
typedef struct {
    uint64_t address;       /* Instruction address */
    size_t size;            /* Instruction size in bytes */
    uint8_t bytes[16];      /* Raw bytes */
    char mnemonic[32];      /* Mnemonic string */
    char op_str[128];       /* Operands string */
    char text[160];         /* Full text: mnemonic + operands */
    
    /* Structured operands */
    int op_count;
    CosmoOp operands[4];
    
    /* Analysis flags */
    bool is_branch;
    bool is_call;
    bool is_ret;
    bool is_privileged;
    int64_t branch_target;  /* For branches: target address */
} CosmoInsn;
```

## Architecture Support

| Architecture | Status | Notes |
|--------------|--------|-------|
| x86-64 | ✅ Full | All common instructions |
| AArch64 | ✅ Full | All common instructions |
| x86-32 | 🚧 Partial | Basic support |
| ARM32 | ❌ Future | Planned |

## Files

| Path | Purpose |
|------|---------|
| `include/cosmo_disasm.h` | Public API header |
| `src/cosmo_disasm.c` | Core implementation |
| `src/cosmo_disasm_x86.c` | x86-64 backend |
| `src/cosmo_disasm_x86.h` | x86-64 internals |
| `src/cosmo_disasm_arm64.c` | AArch64 backend |
| `src/cosmo_disasm_arm64.h` | AArch64 internals |
| `test/test_disasm.c` | Unit tests |
| `Makefile` | Build with cosmocc |

## Build

```bash
# Requires cosmocc in PATH
make

# Run tests
make test

# Install
make install PREFIX=/opt/cosmo
```

## Usage Example

```c
#include "cosmo_disasm.h"

CosmoDisasm *ctx = cosmo_disasm_create(COSMO_ARCH_X86_64);

uint8_t code[] = { 0x55, 0x48, 0x89, 0xE5, 0xC3 };  // push rbp; mov rbp,rsp; ret
CosmoInsn insn;
size_t offset = 0;

while (offset < sizeof(code)) {
    int len = cosmo_disasm_one(ctx, code + offset, sizeof(code) - offset,
                               0x1000 + offset, &insn);
    if (len <= 0) break;
    
    printf("%016llx  %s\n", insn.address, insn.text);
    offset += len;
}

cosmo_disasm_free(ctx);
```

## Integration Points

| Project | Use Case |
|---------|----------|
| tedit-cosmo | Binary file disassembly view |
| e9studio | Binary patching and analysis |
| llamafile-llm | JIT code introspection (future) |
| mhi-procurement | None (but pattern reference) |

## What Does NOT Exist

- ❌ No symbolic resolution — raw disassembly only
- ❌ No control flow graph generation
- ❌ No PE/ELF/Mach-O parsing — bring your own
- ❌ No decompilation — use LLM4Decompile for that

---

*This manifest is ground truth. 3,027 lines of C, zero dependencies.*
