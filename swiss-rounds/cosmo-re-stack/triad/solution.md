# Solution Synthesis: Cosmo-RE-Stack Final Decisions

**Date:** 2026-02-10  
**Role:** Triad Phase 3/3 — Solution Arbiter  
**Mission:** End the debate. Ship decisions.

---

## Executive Summary

**From 13 repos to 8, phased across 3 milestones.**

| Phase | Repos | Milestone |
|-------|-------|-----------|
| **v1.0 Core** | 5 | Functional RE workstation |
| **v1.5 Quality** | +1 | Production-grade decompilation |
| **v2.0 Platform** | +2 | cosmo-bsd-ai integration |

**Cut permanently:** 3 repos  
**Merge:** 1 repo into e9studio

---

## The Architectural Answer

**Q: Is cosmo-bsd a deployment target or the foundational platform?**

**A: It's the foundational platform — but not for v1.**

The Critic correctly identified that cosmo-bsd's daemon architecture (llmd, skilld, mcpd, agentd, reasond, hookd) represents the philosophical endpoint: a UNIX-native AI operating system where the RE workstation is just one set of tools among many.

But the Auditor correctly identified that shipping v1 requires focus.

**Resolution:** cosmo-bsd is the North Star, not the first milestone. Build the tools first (v1), then integrate them into the platform (v2).

---

## Final Decisions by Repo

### ✅ KEEP: Core Stack (v1.0)

| Repo | Verdict | Justification |
|------|---------|---------------|
| **tedit-cosmo** | KEEP | UI layer. Irreplaceable. |
| **e9studio** | KEEP | Analysis engine + WAMR JIT + patching. The core. |
| **cosmokramerpolitan** | KEEP | Build infrastructure (cosmocc), libc, XED. Foundation. |
| **llamafile-llm** | KEEP | LLM runtime. Vision requires AI assistance. |
| **ludofile** | KEEP | Unique format detection via polyfile signatures. |

**Ludofile Justification:**  
The Auditor asked "what does ludofile do that e9studio can't?" The answer: e9studio handles ELF/PE/Mach-O/APE — the big four. Ludofile's polyfile heritage gives it 10,000+ format signatures for firmware, game ROMs, encrypted containers, obscure archives. In RE, you often encounter embedded data that isn't a standard executable. Ludofile solves the long-tail problem.

---

### ⏳ DEFER: Quality Layer (v1.5)

| Repo | Verdict | Justification |
|------|---------|---------------|
| **opentau** | DEFER to v1.5 | Type inference improves decompilation quality significantly, but v1 works without it. |

**Opentau Trade-off:**  
The Critic argues opentau is core because "edit C" is in the vision and type inference makes decompiled C actually editable. True. But the seeker report shows e9decompile already outputs Cosmopolitan-compatible C with basic size-based types (int8_t, int64_t, etc.). That's functional, if ugly.

For v1: Ship with size-based types. Users can edit.  
For v1.5: Add opentau for semantic types (char*, FILE*, struct foo*). Users enjoy.

---

### ⏳ DEFER: Platform Layer (v2.0)

| Repo | Verdict | Justification |
|------|---------|---------------|
| **cosmo-bsd** | DEFER to v2.0 | The destination, not the first stop. |
| **mir** | DEFER to v2.0 | Only needed for cosmo-bsd's skilld daemon. |

**cosmo-bsd Decision:**  
The Critic's strongest argument: cosmo-bsd isn't tangential — it's the integration target where e9studio becomes a skill. Valid. But:

1. e9studio doesn't exist yet as a shippable product
2. Building the platform before the tools is premature
3. The daemon architecture requires the tools to work first

**Resolution:** cosmo-bsd waits for v2. When v1.0 ships a working RE workstation, v2.0 integrates it into the cosmo-bsd-ai platform as skilld-compatible skills.

**mir Decision:**  
mir vs WAMR is a false dichotomy — they serve different contexts. WAMR's sandbox makes sense for untrusted patch code in e9studio. mir's direct JIT makes sense for jail-isolated skills in cosmo-bsd's skilld. But since cosmo-bsd is deferred, mir is deferred with it.

---

### 🔀 MERGE: cosmo-disasm

| Repo | Verdict | Action |
|------|---------|--------|
| **cosmo-disasm** | MERGE | AArch64 backend → e9studio. Delete rest. |

**Justification:**  
- XED (already in cosmokramerpolitan) handles x86/x86-64 disassembly
- cosmo-disasm's x86 backend is redundant with XED
- cosmo-disasm's AArch64 backend is unique and valuable
- The asm-report confirms: "ARM64 disassembly exists in cosmo-disasm"

**Action Items:**
1. Port `cosmo_a64_disasm_one()` and supporting code into e9studio
2. Create thin wrapper that routes x86 to XED, ARM64 to ported code
3. Delete cosmo-disasm repo after merge

---

### ❌ CUT: Permanently Removed

| Repo | Verdict | Justification |
|------|---------|---------------|
| **polytracker** | CUT | LLVM dependency violates Cosmopolitan philosophy ("no LLVM, no Python, no npm"). Fatal incompatibility. |
| **binaryen** | CUT | WAMR already has optimization. Binaryen's AOT focus is overkill for JIT patches. |
| **rose-1** | CUT | 33K files for speculative "source-to-source transforms." No concrete use case. |

**Rose-1 Autopsy:**  
The Critic suggested rose-1 could transform non-portable code to Cosmopolitan-compatible code. Interesting, but:
1. cosmocc already handles most portability via libc abstraction
2. Source transforms are an academic luxury, not an RE requirement
3. 33K files is an absurd cost for a "maybe someday" feature

If source portability becomes a hard requirement, revisit. Until then: killed.

---

### ⏳ DEFER: Nice-to-Have (v2+)

| Repo | Verdict | Justification |
|------|---------|---------------|
| **LLM4Decompile** | DEFER to v2+ | Specialized decompilation models. General LLMs via llamafile are sufficient for v1. |

---

## Phased Roadmap

### Phase 1: v1.0 — Core RE Workstation

**Goal:** Edit C/ASM → WAMR JIT patches → any binary format

**Repos (5):**
```
tedit-cosmo          → UI layer
e9studio             → Analysis + patching + WAMR
  └── (merged: cosmo-disasm AArch64 backend)
cosmokramerpolitan   → Build infra + XED + libc
llamafile-llm        → LLM runtime
ludofile             → Format detection
```

**Deliverable:** `cosmo-re-stack.com` — single APE binary that:
- Opens any binary (ELF/PE/Mach-O/APE + 10K formats via ludofile)
- Disassembles (x86-64 via XED, ARM64 via merged backend)
- Decompiles to editable C (e9decompile, size-based types)
- Compiles patches via WAMR JIT
- Applies patches to target binary
- LLM assistance via embedded llamafile

**Dependencies for v1:**
- Glue layer between tedit-cosmo and e9studio (seeker report: 2-3 weeks)
- C → WASM → Native pipeline (seeker report: 2-3 weeks)
- Multi-format output (ELF works, need PE/Mach-O/APE patching: 3-4 weeks)

---

### Phase 2: v1.5 — Production Quality

**Goal:** Decompilation output humans actually want to read

**Addition:** opentau

**Impact:**
- Type inference: `int64_t arg0` → `struct person *p`
- Variable naming hints
- Struct/vtable detection

**Deliverable:** `cosmo-re-stack.com` v1.5 with readable decompilation

---

### Phase 3: v2.0 — AI-Native Platform

**Goal:** cosmo-bsd-ai integration

**Additions:** cosmo-bsd, mir

**Architecture:**
```
cosmo-bsd-ai (~4-8GB image)
├── llmd     (llamafile daemon)
├── hookd    (event routing)
├── skilld   (tool execution in jails)
│   ├── e9studio skill (patching)
│   ├── ludofile skill (format detection)
│   └── custom skills...
├── mcpd     (MCP protocol)
├── reasond  (structured reasoning)
└── agentd   (multi-agent coordination)
```

**mir's Role:**
- skilld executes skills in FreeBSD jails
- Jails provide isolation (no need for WASM sandbox)
- mir JITs skill code directly to native (faster than WASM pipeline)
- WAMR remains for e9studio's untrusted patch code

**Deliverable:** Bootable `cosmo-bsd-ai.img` — complete AI-native OS in a single image

---

## Implementation Notes

### XED vs cosmo-disasm

The asm-report confirms XED is x86 only. The solution:

```c
// Unified disassembly API in e9studio
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

### WAMR vs mir Contexts

| Context | JIT | Sandbox | Rationale |
|---------|-----|---------|-----------|
| e9studio patch code | WAMR | WASM sandbox | Untrusted user patches need isolation |
| cosmo-bsd skilld | mir | FreeBSD jail | Jail is the sandbox; mir is faster |

Both JITs coexist. Different tools for different contexts.

### ludofile Integration

ludofile becomes e9studio's format detection frontend:

```c
// In e9studio analysis pipeline
E9Binary *e9_binary_open(const char *path) {
    // Try ludofile first for format detection
    LudoFormat *fmt = ludo_detect(path);
    if (fmt->type == LUDO_EXECUTABLE) {
        // Standard executable — use e9 native parsers
        return e9_binary_open_native(path, fmt->arch);
    } else {
        // Exotic format — extract if container, analyze if data
        return e9_binary_open_exotic(path, fmt);
    }
}
```

---

## Questions Resolved

### 1. "What does ludofile do that e9studio can't?"

**Answer:** 10,000+ format signatures beyond ELF/PE/Mach-O/APE. RE often involves embedded data, firmware blobs, game assets. ludofile's polyfile heritage covers the long tail.

### 2. "Why was rose-1 ever considered?"

**Answer:** Source-to-source transforms sounded useful for portability. But cosmocc already handles portability at libc level. 33K files for academic transforms is unjustified.

### 3. "Is AArch64 patching a v1 requirement?"

**Answer:** No. x86-64 is the primary target. AArch64 disassembly (via merged cosmo-disasm) enables analysis, but ARM64 trampolines can defer to v1.5.

### 4. "What's the LLM decompilation roadmap?"

**Answer:** 
- v1: General LLM via llamafile (function explanation, variable naming hints)
- v2+: LLM4Decompile for specialized decompilation models (if general models insufficient)

### 5. "Who asked for taint tracking?"

**Answer:** Nobody with a concrete use case. polytracker was scope creep. Cut.

---

## Final Component Map

```
┌─────────────────────────────────────────────────────────────────┐
│ v1.0 CORE                                                       │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ tedit-cosmo          │ e9studio (+ merged ARM64 disasm)    │ │
│ │ UI/Editor            │ Analysis + WAMR JIT + Patching      │ │
│ └──────────────────────┴──────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ cosmokramerpolitan   │ llamafile-llm    │ ludofile         │ │
│ │ Build/XED/libc       │ LLM Runtime      │ Format Detection │ │
│ └──────────────────────┴──────────────────┴──────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│ v1.5 QUALITY                                                    │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ opentau — Type Inference for readable decompilation         │ │
│ └─────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│ v2.0 PLATFORM                                                   │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ cosmo-bsd                                                   │ │
│ │ ┌──────────┬──────────┬──────────┬──────────┬────────────┐ │ │
│ │ │  llmd    │  hookd   │  skilld  │  mcpd    │  agentd    │ │ │
│ │ │ (llama)  │ (events) │ (tools)  │ (MCP)    │ (agents)   │ │ │
│ │ └──────────┴──────────┴──────────┴──────────┴────────────┘ │ │
│ │ mir — JIT for skilld (jail-isolated skills)                 │ │
│ └─────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│ ❌ CUT                                                           │
│ polytracker (LLVM), binaryen (redundant), rose-1 (bloat)        │
│ cosmo-disasm (merged, then deleted)                             │
├─────────────────────────────────────────────────────────────────┤
│ ⏳ FUTURE (v2+)                                                  │
│ LLM4Decompile — specialized models when general LLMs insufficient│
└─────────────────────────────────────────────────────────────────┘
```

---

## Actionable Next Steps

### Immediate (This Week)

1. **Merge cosmo-disasm ARM64 → e9studio**
   - Port `cosmo_a64_disasm_one()` and dependencies
   - Create unified disasm API routing x86→XED, ARM64→ported code
   - Test on sample ARM64 binaries
   - Delete cosmo-disasm repo after verification

2. **Archive cut repos**
   - Move polytracker, binaryen, rose-1 to archive/ (not delete — historical reference)
   - Update any references in build systems

3. **Create v1.0 integration branch**
   - Set up monorepo or submodule structure for: tedit-cosmo, e9studio, cosmokramerpolitan, llamafile, ludofile

### Short-term (Month 1)

4. **Build tedit-cosmo ↔ e9studio glue layer**
   - Expose `e9_binary_*` APIs through tedit's disasm_view
   - "Analyze Binary" menu item
   - Decompiler pane alongside disassembly

5. **Complete WASM patch pipeline**
   - Source edit → cosmocc → object → e9_diff_objects → WAMR JIT
   - Test on simple function patches

### Medium-term (Month 2-3)

6. **PE patching support**
   - Port e9patch's ELF cave-finding to PE sections
   - Test on Windows binaries

7. **v1.0 release**
   - `cosmo-re-stack.com` single APE
   - Documentation, examples, tutorials

### Long-term (v1.5, v2.0)

8. **opentau integration (v1.5)**
9. **cosmo-bsd-ai integration (v2.0)**

---

## Debate Closed

The Auditor was right about:
- 13 repos is too many
- polytracker/binaryen/rose-1 are cut
- cosmo-disasm merges into e9studio
- Focus beats scope

The Critic was right about:
- cosmo-bsd is the destination, not tangential
- ludofile has unique value (format signatures)
- opentau matters for decompilation quality
- mir and WAMR serve different contexts

Both were wrong about:
- Auditor: Treating cosmo-bsd as "just a BSD distro" (it's the platform)
- Critic: Wanting everything in v1 (phasing matters)

**The synthesis:** Phase it. Build the tools (v1), add quality (v1.5), integrate into platform (v2).

---

*Solution Arbiter, Triad Phase 3/3*  
*"The best architecture is the one that ships."*
