# ASM Specialist Work Plan

**Date:** 2026-02-10  
**Agent:** asm-specialist  
**Role:** Binary analysis, disassembly, patching, WAMR JIT, architecture support

---

## Mission Statement

Own the binary analysis and patching pipeline. You're the low-level expert: instruction decoding, control flow graphs, decompilation, trampoline generation, and making patches actually work on real binaries.

---

## Phase 1: v1.0 — Core Analysis & Patching

### 1.1 Merge cosmo-disasm ARM64 Backend into e9studio

**Priority:** CRITICAL — Week 1 blocker

**Task:** Port ARM64 disassembly from cosmo-disasm into e9studio. Delete cosmo-disasm repo after merge.

**Source files to port:**
```
C:\cosmo-disasm\src\cosmo_disasm_arm64.c
C:\cosmo-disasm\include\cosmo_disasm.h (ARM64 portions)
```

**Target location:**
```
C:\e9studio\src\e9patch\analysis\e9disasm_arm64.c
```

**Unified API design:**
```c
// In e9studio: unified disasm dispatcher
int e9_disasm(E9Binary *bin, uint64_t addr, E9Instruction *insn) {
    switch (bin->arch) {
    case E9_ARCH_X86_64:
    case E9_ARCH_X86_32:
        return e9_disasm_xed(bin, addr, insn);  // Use XED from cosmo
    case E9_ARCH_AARCH64:
        return e9_disasm_arm64(bin, addr, insn);  // Merged from cosmo-disasm
    default:
        return E9_ERR_UNSUPPORTED_ARCH;
    }
}
```

**ARM64 instructions already implemented (from asm-report):**
- PC-relative: ADR, ADRP
- Add/Sub: ADD, ADDS, SUB, SUBS, CMP
- Move wide: MOVN, MOVZ, MOVK
- Branches: B, BL, B.cond, CBZ, CBNZ, TBZ, TBNZ, BR, BLR, RET
- Load/Store: LDR, STR, LDP, STP
- Logical: AND, ORR, EOR, BIC, ANDS
- System: NOP, DSB, DMB, ISB, MSR, MRS
- Exception: SVC, HVC, SMC, BRK, HLT
- PAC: PACIASP, PACIBSP, RETAA, RETAB

**Deliverables:**
- [ ] ARM64 backend ported to e9studio
- [ ] Unified `e9_disasm()` API routing to XED or ARM64
- [ ] Tests: disassemble ARM64 ELF binary
- [ ] Delete cosmo-disasm repo after verification

**Effort:** 1 week

### 1.2 XED Integration for x86 Disassembly

**Task:** Use XED from cosmokramerpolitan instead of custom x86 disassembly.

**Coordinate with:** Cosmo specialist (they provide headers)

**Files:**
```
C:\cosmokramerpolitan\third_party\xed\x86ild.greg.c
C:\cosmokramerpolitan\libc\x86isa.h
```

**Wrapper:**
```c
// e9disasm_xed.c
#include <x86isa.h>

int e9_disasm_xed(E9Binary *bin, uint64_t addr, E9Instruction *insn) {
    struct XedDecodedInst xed;
    int len = x86ild(&xed, bin->data + addr, bin->size - addr);
    if (len < 0) return E9_ERR_DECODE;
    
    insn->address = addr;
    insn->length = len;
    insn->mnemonic = GetMnemonic(&xed);
    // ... fill other fields
    return 0;
}
```

**Deliverables:**
- [ ] XED wrapper in e9studio
- [ ] Remove custom x86 disassembly code
- [ ] Verify: same output as before

**Effort:** 3-5 days

### 1.3 C → WASM → JIT Patch Pipeline

**Priority:** CRITICAL — Core functionality

**Task:** Complete the patch compilation pipeline.

**Current state (from seeker report):**
- WAMR is integrated in e9studio
- Fast JIT mode works
- ZipOS integration exists
- **Missing:** C → WASM compilation step

**Pipeline:**
```
User edits C code
      │
      ▼
┌─────────────┐
│   cosmocc   │ → Compile to object file
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ e9_diff_    │ → Compute delta vs original
│ objects()   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ C → WASM    │ → Convert patch to WASM (wasm2c or clang --target=wasm32)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ WAMR JIT    │ → Compile WASM to native
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ e9_binpatch │ → Inject into target binary
│ _apply()    │
└─────────────┘
```

**Key APIs (already exist):**
```c
// Object diffing
E9PatchSet *e9_diff_objects(const uint8_t *old_obj, size_t old_size,
                            const uint8_t *new_obj, size_t new_size);

// WAMR execution
void e9wasm_set_exec_mode(int mode);  // 0=interp, 1=fast_jit, 2=aot
int e9wasm_init(const E9WasmConfig *config);
void *e9wasm_load_module(const char *path);
int e9wasm_call(void *module, const char *func_name, int argc, const char *argv[]);

// Binary patching
E9BinPatchSession *e9_binpatch_session_create(E9Binary *bin);
int e9_binpatch_bytes(E9BinPatchSession *session, uint64_t addr,
                      const uint8_t *bytes, size_t size, uint32_t flags);
```

**Missing piece:** C → WASM compiler invocation

**Options:**
1. Shell out to `cosmocc --target=wasm32` (if supported)
2. Embed wasm2c
3. Pre-compile patch templates to WASM

**Deliverables:**
- [ ] C → WASM compilation working
- [ ] Object diff → WASM → JIT → inject flow
- [ ] Test: simple function patch on ELF binary

**Effort:** 2-3 weeks

### 1.4 PE Patching Support

**Task:** Port ELF patching techniques to PE format.

**Current state:**
- PE parsing exists (`e9pe.cpp`)
- Trampoline generation is ELF-only
- Code caves: ELF sections → PE sections

**Key differences:**
| Aspect | ELF | PE |
|--------|-----|-----|
| Sections | Flexible | Fixed alignment (0x1000) |
| Code caves | .text padding | .text padding or new section |
| Imports | GOT/PLT | IAT/ILT |
| Relocations | RELA | .reloc section |

**Approach:**
1. Find code caves in PE sections
2. Generate PE-compatible trampolines
3. Update PE headers (optional sections, relocations)

**Files to study:**
```
C:\e9studio\src\e9patch\e9pe.cpp
C:\e9studio\src\e9patch\e9x86_64.cpp (trampoline generation)
C:\cosmokramerpolitan\tool\decode\pe2.c (PE parsing reference)
```

**Deliverables:**
- [ ] PE code cave finder
- [ ] PE trampoline generation
- [ ] Test: patch Windows .exe, verify it runs

**Effort:** 3-4 weeks

### 1.5 Mach-O Patching Support

**Task:** Add Mach-O binary patching.

**Current state:**
- Mach-O parsing exists (cosmokramerpolitan)
- No Mach-O patching in e9studio

**Files to study:**
```
C:\cosmokramerpolitan\tool\decode\macho.c
```

**Key Mach-O concepts:**
- Load commands (LC_SEGMENT_64, LC_SYMTAB, etc.)
- __TEXT and __DATA segments
- Code signing (may need to strip/re-sign)

**Deliverables:**
- [ ] Mach-O code cave finder
- [ ] Mach-O trampoline generation
- [ ] Test: patch macOS binary (ad-hoc signed)

**Effort:** 2 weeks

### 1.6 APE Patching Support

**Task:** Patch APE polyglot binaries.

**APE structure (from seeker report):**
```c
typedef struct {
    uint64_t dos_header;
    uint64_t elf_offset;
    uint64_t pe_offset;
    uint64_t shell_offset;
    uint64_t macho_offset;
    uint64_t zipos_start;
    uint64_t zipos_central_dir;
} E9APELayout;
```

**Approach:**
1. Parse APE to find all embedded formats
2. Patch each format's code section consistently
3. Update ZIP central directory if ZipOS modified

**Key API (exists):**
```c
int e9_ape_parse(const uint8_t *data, size_t size, E9APELayout *layout);
uint8_t *e9_ape_extract_elf(const uint8_t *data, size_t size, size_t *out_size);
uint8_t *e9_ape_extract_pe(const uint8_t *data, size_t size, size_t *out_size);
```

**Deliverables:**
- [ ] APE-aware patching (patch all embedded formats)
- [ ] Test: patch APE, verify on Linux and Windows

**Effort:** 1-2 weeks

---

## Phase 2: v1.5 — Type Inference Integration

### 2.1 opentau ↔ e9decompile Integration

**Task:** Feed decompiled IR into opentau for type inference.

**Current decompiler output (size-based):**
```c
int64_t func1(int64_t arg0, int64_t arg1) {
    int64_t local8 = arg1 + 8;
    int64_t local16 = *(int64_t*)local8;
    return local16;
}
```

**Target output (semantic):**
```c
const char *get_name(struct person *p, int index) {
    const char **names = p->names;
    return names[index];
}
```

**Integration points:**
```c
// e9decompile.h - existing
E9IRFunc *e9_decompile_lift(E9Decompile *dc, E9Function *func);
char *e9_decompile_emit_c(E9Decompile *dc, E9IRFunc *func);

// New: insert opentau between lift and emit
int e9_decompile_infer_types(E9Decompile *dc, E9IRFunc *func);  // Calls opentau
```

**Deliverables:**
- [ ] opentau API wrapper for e9studio
- [ ] Type inference pass in decompilation pipeline
- [ ] Before/after comparison on test binaries

**Effort:** 2 weeks

### 2.2 Type Propagation Pipeline

**Task:** Propagate inferred types through the IR.

**Challenges:**
- Pointer arithmetic vs array indexing
- Struct member access detection
- vtable/function pointer recovery

**Deliverables:**
- [ ] Type propagation pass
- [ ] Struct detection heuristics
- [ ] vtable pattern recognition

**Effort:** 2 weeks

---

## Phase 3: v2.0 — Platform Integration

### 3.1 e9studio as cosmo-bsd Skill

**Task:** Wrap e9studio as a skilld-compatible skill.

**Skill format:**
```
/usr/local/share/skills/e9studio/
├── SKILL.conf
├── run.sh
└── schema.json
```

**SKILL.conf:**
```ini
[skill]
name=e9studio
description=Binary analysis and patching
version=1.0
jail=yes
timeout=300
```

**run.sh:**
```sh
#!/bin/sh
# Receives JSON on stdin, outputs JSON on stdout
e9studio.com --skill-mode "$@"
```

**Deliverables:**
- [ ] `--skill-mode` flag for e9studio
- [ ] JSON input/output for skill execution
- [ ] Integration test with mock skilld

**Effort:** 1 week

### 3.2 ARM64 Trampoline Generation (Optional for v2.0)

**Current state:** ARM64 disassembly exists, but no patching.

**Challenge:** ARM64 instructions are fixed 4 bytes. Trampolines require:
- B (branch) instruction: ±128MB range
- For longer jumps: ADRP + BR sequence

**Trampoline patterns:**
```asm
; Short jump (within ±128MB)
B target

; Long jump (anywhere in address space)
ADRP X16, target@PAGE
ADD X16, X16, target@PAGEOFF
BR X16
```

**Deliverables:**
- [ ] ARM64 trampoline generation
- [ ] ARM64 code cave finder
- [ ] Test: patch ARM64 ELF

**Effort:** 3-4 weeks (deferred if not critical for v2.0)

---

## Architecture Support Matrix

| Feature | x86-64 | x86-32 | AArch64 | ARM32 |
|---------|--------|--------|---------|-------|
| Disassembly | ✅ XED | ✅ XED | ✅ Merged | ❌ Future |
| ELF parsing | ✅ | ✅ | ✅ | ✅ |
| PE parsing | ✅ | ✅ | ⚠️ | ❌ |
| Mach-O parsing | ⚠️ | ❌ | ⚠️ | ❌ |
| Trampolines | ✅ | ⚠️ | ❌ v2.0 | ❌ |
| WAMR JIT | ✅ | ⚠️ | ✅ | ❌ |

**v1.0 target:** x86-64 full support, AArch64 analysis-only, others best-effort.

---

## Key Files Reference

### e9studio Analysis Engine
```
C:\e9studio\src\e9patch\analysis\e9analysis.h    (binary analysis)
C:\e9studio\src\e9patch\analysis\e9decompile.h   (decompiler)
C:\e9studio\src\e9patch\analysis\e9binpatch.h    (binary patching)
C:\e9studio\src\e9patch\analysis\e9polyglot.h    (APE parsing)
```

### e9studio WAMR Integration
```
C:\e9studio\src\e9patch\wasm\e9wasm_host.h       (WAMR host)
C:\e9studio\src\e9patch\vendor\wamr\wamr_config.h (WAMR config)
```

### e9studio Format Support
```
C:\e9studio\src\e9patch\e9elf.cpp                (ELF patching)
C:\e9studio\src\e9patch\e9pe.cpp                 (PE patching)
C:\e9studio\src\e9patch\e9x86_64.cpp             (x86-64 trampolines)
```

---

## Integration Points

### With Cosmo Specialist

| Interface | Direction | Description |
|-----------|-----------|-------------|
| XED headers | Cosmo → ASM | XED API for x86 disassembly |
| cosmocc WASM | Cosmo → ASM | C → WASM compilation support |
| Build system | Cosmo → ASM | Makefile.cosmo for e9studio |

### With Seeker Specialist

| Interface | Direction | Description |
|-----------|-----------|-------------|
| Glue layer | Seeker + ASM | tedit-cosmo ↔ e9studio integration |
| API surface | ASM → Seeker | Which e9studio APIs to expose |
| llamafile | Seeker → ASM | LLM-assisted decompilation hints |

---

## Token Budget

| Task | Complexity | Est. Tokens |
|------|------------|-------------|
| ARM64 merge | Medium | 50K-100K |
| XED integration | Low | 20K-30K |
| WASM patch pipeline | High | 150K-250K |
| PE patching | High | 100K-150K |
| Mach-O patching | Medium | 50K-80K |
| APE patching | Medium | 40K-60K |
| opentau integration | Medium | 60K-100K |
| Type propagation | Medium | 60K-100K |
| e9studio skill wrapper | Low | 20K-30K |
| ARM64 trampolines | High | 100K-150K |
| **Total** | | **~650K-1.05M** |

---

## Success Metrics

### v1.0
- [ ] x86-64 binaries: disassemble, decompile, patch, inject ✓
- [ ] AArch64 binaries: disassemble, decompile ✓ (patching deferred)
- [ ] ELF, PE, Mach-O, APE: all formats patchable (x86-64)

### v1.5
- [ ] Decompiled output has semantic types
- [ ] Struct/vtable detection working

### v2.0
- [ ] e9studio runs as cosmo-bsd skill
- [ ] ARM64 patching (if prioritized)

---

## Immediate Next Steps (Week 1)

1. **Day 1-2:** Port cosmo-disasm ARM64 backend to e9studio
2. **Day 3-4:** Create unified `e9_disasm()` dispatcher
3. **Day 5:** Test ARM64 disassembly on sample binary
4. **Week 1 deliverable:** ARM64 disassembly working in e9studio

---

*"The patch is mightier than the sword — if you can inject it."*
