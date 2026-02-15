# Redundancy Analysis: Cosmo-RE-Stack

**Date:** 2026-02-10  
**Analyst:** Stack Auditor (Triad Phase 1/3)  
**Input:** seeker-report.md, asm-report.md, cosmo-report.md, SOURCES-EXPANDED.md

---

## Executive Summary: KILL LIST

**Verdict: 13 repos is absurd. Cut to 6-7.**

| Repo | Files | Verdict | Reason |
|------|-------|---------|--------|
| tedit-cosmo | — | ✅ KEEP | Core UI, irreplaceable |
| e9studio | — | ✅ KEEP | Core analysis/patching engine |
| cosmokramerpolitan | 17,929 | ✅ KEEP | Build infrastructure, libc |
| llamafile-llm | — | ✅ KEEP | LLM runtime (vision requires it) |
| cosmo-disasm | — | ⚠️ MERGE | Merge into e9studio or use XED |
| cosmo-bsd | 54 | ❌ CUT | Tangential to RE vision |
| ludofile | 62 | ⚠️ QUESTION | Overlaps e9studio hex/format detection |
| polytracker | 594 | ❌ CUT | LLVM dependency, ludofile claims integration |
| LLM4Decompile | 92 | ⚠️ DEFER | Nice-to-have, not core |
| opentau | 158 | ❌ CUT | Type inference is gravy, not steak |
| mir | 1,599 | ⚠️ QUESTION | Alternative to WAMR — pick ONE |
| rose-1 | 33,125 | ❌ CUT | 33K files for what? Absurd bloat |
| binaryen | 2,781 | ❌ CUT | WAMR already has optimizer |

**Recommended core:** tedit-cosmo + e9studio + cosmokramerpolitan + llamafile = 4 repos  
**Maybe add:** mir OR keep WAMR (not both), LLM4Decompile (if LLM decompile is priority)

---

## 1. DISASSEMBLER REDUNDANCY (Critical)

### The Problem: THREE Disassemblers

| Component | Location | Arch Support | Status |
|-----------|----------|--------------|--------|
| **XED** | cosmokramerpolitan/third_party/xed | x86 only | Already in cosmo |
| **cosmo-disasm** | C:\cosmo-disasm | x86-64, AArch64 | Separate repo |
| **e9_disasm_*()** | e9studio analysis/ | Via cosmo-disasm | Wrapper |

**Why this is stupid:**
1. XED is 42K+ lines of battle-tested Intel disassembler ALREADY IN COSMOPOLITAN
2. cosmo-disasm is a custom implementation that duplicates this effort
3. e9studio wraps cosmo-disasm when it could just use XED directly

**The seeker report says:**
> "e9studio uses cosmo-disasm for raw disassembly"

**The cosmo report says:**
> "XED... Already APE-ready. Reusability: ★★★★★ Perfect for e9studio disassembly."

**Resolution:**
- For x86: Use XED from cosmopolitan (already there!)
- For AArch64: Need one solution — either extend XED or keep cosmo-disasm's ARM64 backend only
- **Merge cosmo-disasm's AArch64 backend into e9studio, delete the rest**

### Counter-argument for cosmo-disasm
The asm-report notes cosmo-disasm has a unified API across architectures. XED is x86-only. If multi-arch is priority, cosmo-disasm's API wrapper makes sense. But then:
- Don't reinvent x86 disassembly — call XED under the hood
- cosmo-disasm should be a thin wrapper, not a full reimplementation

---

## 2. JIT REDUNDANCY: WAMR vs mir

### The Problem: Two JIT Solutions

| JIT | Files | Language | Approach |
|-----|-------|----------|----------|
| **WAMR** | In e9studio | WebAssembly | WASM → JIT native |
| **mir** | 1,599 | C11 | Direct C → machine code |

**The vision says:**
> "WAMR JIT compiles patches → e9-style injection"

**The sources ask:**
> "Is WAMR the right choice vs mir?"

### Analysis

**WAMR (current choice):**
- Already integrated in e9studio
- Sandboxed execution (security win)
- WASM is portable intermediate format
- Requires C → WASM → JIT pipeline (slower cold start)
- Fast JIT mode avoids LLVM dependency

**mir (alternative):**
- Direct C11 → machine code (faster cold path)
- No WASM intermediate step
- Less sandboxing (patches run native)
- 1,599 files = significant new dependency
- Not currently integrated

### My Take: STICK WITH WAMR

**Rationale:**
1. WAMR is already integrated — switching costs are real
2. WASM provides sandboxing for untrusted patch code
3. Binaryen (if kept) can optimize WASM before JIT
4. mir solves a problem you don't have (cold start is not the bottleneck)

**Cut mir** unless profiling proves WAMR's cold start is unacceptable.

---

## 3. ROSE-1: THE ELEPHANT IN THE ROOM

### 33,125 Files. Thirty-three THOUSAND.

The SOURCES-EXPANDED.md says:
> "rose-1 = source-to-source transforms (could generate optimized patch code)"

**"Could"** — that's a fantasy, not a use case.

### What is ROSE?

LLNL's ROSE is a source-to-source compiler infrastructure for:
- Parallel code optimization
- Static analysis
- Source transformation

**What it's NOT for:**
- Binary reverse engineering
- JIT patch compilation
- Anything in the stated vision

### The Question Nobody Asked

**What specific problem does ROSE solve that e9studio + cosmocc can't?**

If the answer is "we might want source transforms someday" — that's not a reason to include 33K files.

**Verdict: CUT IMMEDIATELY**

If you need source transforms later, cosmocc + a simple AST library is 100x lighter.

---

## 4. COSMO-BSD: Wrong Stack

### What It Is

From SOURCES-EXPANDED:
> "cosmo-bsd: Cosmopolitan KISS BSD — portable datacenter in single binary"

This is a **deployment target** or **OS layer**, not an RE tool.

### Why It's Here (Probably)

Someone thought: "We're building universal binaries, maybe we should target a universal OS."

**But the vision is:**
> "Universal binary RE workstation — edit C/ASM → WAMR JIT patches → any binary format"

cosmo-bsd doesn't help you analyze binaries. It's a distraction.

**Verdict: CUT**

Keep it as a separate project if you want a portable datacenter. Don't pollute the RE stack.

---

## 5. POLYTRACKER: LLVM Dependency Smell

### The Claim

polytracker: "LLVM taint tracking (to be integrated into ludofile)"

### The Problem

1. LLVM is a massive dependency (Cosmopolitan explicitly avoids LLVM)
2. "To be integrated" = not integrated
3. Taint tracking is nice-to-have, not core to the vision

### The Pattern

This is scope creep. The vision is:
> "edit C/ASM → WAMR JIT patches → any binary format"

Taint tracking is analysis tooling. Useful? Yes. Core? No.

**Verdict: CUT for v1**

Add taint tracking when the core edit-patch-inject loop works.

---

## 6. LLM LAYER OVERLAP

### Two LLM Components

| Repo | Purpose |
|------|---------|
| **llamafile** | LLM runtime (OpenAI-compatible API) |
| **LLM4Decompile** | Decompilation-specific models |

### This Is Actually Fine

llamafile = runtime, LLM4Decompile = models. Not redundant.

**But:** LLM4Decompile is an enhancement, not core.

**Verdict:**
- KEEP llamafile (LLM runtime is core to vision)
- DEFER LLM4Decompile (load models later, get edit-patch loop working first)

---

## 7. OPENTAU: Premature Optimization

### What It Does

> "opentau: LLM gradual type inference"

### Reality Check

Type inference is a polish feature. The vision doesn't mention it.

You're trying to build:
1. Disassemble any binary ✅
2. Edit decompiled C ✅
3. JIT compile patches ✅
4. Inject into binary ✅

Type inference helps with (2) but isn't blocking.

**Verdict: CUT**

Add after core loop works.

---

## 8. BINARYEN: Redundant with WAMR

### What It Does

WebAssembly optimizer/compiler toolchain.

### The Question

WAMR already has optimization passes. Why add another WASM tool?

### When Binaryen Makes Sense

- You're generating WASM and want maximum optimization
- You're doing WASM-to-WASM transforms
- You're ahead-of-time compiling WASM to native

### The Reality

e9studio's WAMR integration uses Fast JIT. Binaryen's optimization is for AOT scenarios.

**Verdict: CUT**

If profiling shows JIT'd WASM patches are slow, consider AOT via Binaryen. Until then, it's speculative.

---

## 9. LUDOFILE: Overlaps or Complements?

### What It Claims

> "ludofile: Portable polyfile impl + polytracker + deep learning parsing + hex viewer"

### The Overlap

e9studio already has:
- Hex viewing (via `e9wasm_mmap_binary`)
- Format detection (ELF, PE, Mach-O, APE parsing)
- Deep analysis

### What Ludofile Might Add

- polyfile's signature database (more format detection)
- polytracker integration (but we're cutting polytracker)

### The Question

**Does ludofile do something e9studio can't?**

If yes: What specifically? Document it.  
If no: Why is it here?

**Verdict: ⚠️ NEEDS JUSTIFICATION**

The burden is on ludofile to prove its worth. "More format detection" isn't compelling if e9studio already handles ELF/PE/Mach-O/APE.

---

## 10. CONSOLIDATED RECOMMENDATIONS

### The Minimal Viable Stack (4 repos)

```
tedit-cosmo       → UI layer (editor with disasm view)
e9studio          → Analysis engine + WAMR JIT + patching
cosmokramerpolitan → Build infrastructure (cosmocc → APE)
llamafile-llm     → LLM runtime for AI assistance
```

This covers the vision: "edit C/ASM → WAMR JIT patches → any binary format"

### The "Maybe" List (2 repos)

| Repo | Condition |
|------|-----------|
| **cosmo-disasm** | Merge AArch64 backend into e9studio, delete the rest. XED handles x86. |
| **LLM4Decompile** | Add when LLM-enhanced decompilation is priority (Phase 2?) |

### The Kill List (7 repos)

| Repo | Reason |
|------|--------|
| **cosmo-bsd** | Tangential (deployment, not RE) |
| **polytracker** | LLVM dependency, not core |
| **opentau** | Polish feature, not core |
| **mir** | Redundant with WAMR |
| **rose-1** | 33K files of bloat for speculative use case |
| **binaryen** | Redundant with WAMR's optimizer |
| **ludofile** | Overlaps e9studio (needs justification to survive) |

---

## 11. ARCHITECTURAL RECOMMENDATIONS

### Use XED for x86 Disassembly

Stop maintaining parallel x86 disassembly code. XED is:
- Already in cosmopolitan
- Battle-tested by Intel
- APE-ready

cosmo-disasm should be:
1. A thin wrapper around XED for x86
2. A custom implementation ONLY for AArch64

### Decide: Decompilation Priority?

If LLM-assisted decompilation is core:
- Keep LLM4Decompile
- Integrate with e9decompile output

If decompilation is "nice to have":
- e9studio's built-in decompiler is good enough
- llamafile can enhance output ad-hoc

### WAMR is the JIT — Stop Second-Guessing

mir is interesting but:
- WAMR is already integrated
- WASM provides sandboxing
- Switching JITs is a distraction

Focus on completing the WAMR pipeline instead of evaluating alternatives.

---

## 12. QUESTIONS FOR ROUND 2

1. **What does ludofile do that e9studio can't?** Specific features, not hand-waving.

2. **Why was rose-1 ever considered?** 33K files solves what problem?

3. **Is AArch64 patching a v1 requirement?** If not, cosmo-disasm can be deferred entirely.

4. **What's the LLM decompilation roadmap?** If core, keep LLM4Decompile. If gravy, defer.

5. **Who asked for taint tracking?** polytracker seems like a solution looking for a problem.

---

## 13. FINAL VERDICT

**From 13 repos to 4-6 repos.**

The original vision is achievable with:
- **tedit-cosmo** (UI)
- **e9studio** (analysis + patching)
- **cosmokramerpolitan** (build infra)
- **llamafile** (LLM)
- Maybe: **cosmo-disasm** (AArch64 backend only)
- Maybe: **LLM4Decompile** (if LLM decompile is priority)

Everything else is:
- Scope creep (rose-1, polytracker, opentau)
- Tangential (cosmo-bsd)
- Redundant (mir, binaryen)
- Unjustified (ludofile)

**Kill your darlings. Ship the core.**

---

*Stack Auditor, Triad Phase 1/3*
