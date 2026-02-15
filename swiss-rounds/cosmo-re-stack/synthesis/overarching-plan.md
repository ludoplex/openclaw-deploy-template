# Cosmo-RE-Stack: Overarching Implementation Plan

**Date:** 2026-02-10  
**Synthesized by:** PM Agent  
**Status:** Final — Ready for Execution

---

## Executive Summary

**Vision:** Universal binary RE workstation where you edit C/ASM → WAMR JIT compiles patches → inject into any binary format (ELF/PE/Mach-O/APE). The entire stack eventually deploys as cosmo-bsd, a UNIX-native AI operating system.

**Scope Reduction:** From 13 repos → 8 repos across 3 phases.

| Phase | Target | Repos | Deliverable |
|-------|--------|-------|-------------|
| **v1.0** | Core RE Workstation | 5 | `cosmo-re-stack.com` — single APE binary |
| **v1.5** | Production Quality | +1 | Semantic type inference in decompiled C |
| **v2.0** | AI-Native Platform | +2 | `cosmo-bsd-ai.img` — bootable AI OS |

---

## Phase 1: v1.0 — Core RE Workstation

### Objective
Functional edit-compile-patch-inject loop for universal binaries.

### Repos Included

| Repo | Role | Critical Path? |
|------|------|----------------|
| **tedit-cosmo** | UI layer (editor with disasm view) | ✅ Yes |
| **e9studio** | Analysis engine + WAMR JIT + patching | ✅ Yes |
| **cosmokramerpolitan** | Build infrastructure (cosmocc), libc, XED | ✅ Yes |
| **llamafile-llm** | LLM runtime for AI assistance | No (optional enhancement) |
| **ludofile** | Format detection (10K+ signatures) | No (extends format coverage) |

### Key Integration Work

| Task | Owner | Est. Effort | Dependencies |
|------|-------|-------------|--------------|
| tedit-cosmo ↔ e9studio glue layer | Seeker + ASM | 2-3 weeks | None |
| Merge cosmo-disasm ARM64 → e9studio | ASM | 1 week | None |
| C → WASM → Native patch pipeline | ASM + Cosmo | 2-3 weeks | Glue layer |
| PE patching (port ELF caves to PE sections) | ASM | 3-4 weeks | Analysis APIs |
| Mach-O patching support | ASM | 2 weeks | PE patching |
| APE self-modification | Cosmo | 1-2 weeks | ZipOS mastery |
| llamafile API integration | Seeker | 1 week | Glue layer |
| ludofile format detection frontend | Seeker | 1 week | None |

### Success Criteria

1. **Opens any binary:** ELF ✓, PE ✓, Mach-O ✓, APE ✓, + ludofile long-tail
2. **Disassembles:** x86-64 (via XED) ✓, AArch64 (via merged backend) ✓
3. **Decompiles:** e9decompile outputs editable C (size-based types)
4. **Patches:** Edit C → WAMR JIT → inject into target binary
5. **Ships as single APE:** `cosmo-re-stack.com` runs on Linux/macOS/Windows/BSD

### Estimated Timeline

| Week | Milestone |
|------|-----------|
| 1-2 | cosmo-disasm ARM64 merge complete |
| 2-4 | tedit-cosmo ↔ e9studio glue layer functional |
| 4-6 | C → WASM → JIT pipeline working |
| 6-8 | PE patching complete |
| 8-10 | Mach-O + APE patching complete |
| 10-12 | Integration testing, polish, docs |
| **12** | **v1.0 Release** |

### Token Budget Estimate (v1.0)

| Component | Complexity | Est. Agent Tokens |
|-----------|------------|-------------------|
| Glue layer design + impl | High | 200K-300K |
| ARM64 disasm merge | Medium | 50K-100K |
| WASM patch pipeline | High | 150K-250K |
| PE/Mach-O patching | High | 200K-300K |
| llamafile integration | Low | 30K-50K |
| ludofile integration | Low | 30K-50K |
| **Total v1.0** | | **~600K-1M tokens** |

---

## Phase 2: v1.5 — Production Quality

### Objective
Decompilation output humans actually want to read and edit.

### Addition

| Repo | Role |
|------|------|
| **opentau** | LLM gradual type inference |

### Impact

| Before (v1.0) | After (v1.5) |
|---------------|--------------|
| `int64_t arg0` | `struct person *p` |
| `int64_t local8 = *(int64_t*)(arg0 + 8)` | `const char *name = p->name` |
| Size-based types only | Semantic types inferred |

### Integration Work

| Task | Owner | Est. Effort |
|------|-------|-------------|
| opentau ↔ e9decompile integration | Seeker + ASM | 2 weeks |
| Type propagation pipeline | ASM | 2 weeks |
| LLM-assisted type refinement | Seeker | 1 week |

### Success Criteria

1. Decompiled functions have semantic type annotations
2. Struct/vtable detection working
3. Variable names inferred from usage patterns

### Timeline
**v1.5 Release:** v1.0 + 4-6 weeks

### Token Budget Estimate (v1.5)

| Component | Est. Agent Tokens |
|-----------|-------------------|
| opentau integration | 100K-150K |
| Type propagation | 80K-120K |
| LLM type refinement | 50K-80K |
| **Total v1.5** | **~230K-350K** |

---

## Phase 3: v2.0 — AI-Native Platform

### Objective
cosmo-bsd-ai: Complete UNIX-native AI operating system where the RE workstation is one set of skills among many.

### Additions

| Repo | Role |
|------|------|
| **cosmo-bsd** | Daemon architecture (llmd, hookd, skilld, mcpd, reasond, agentd) |
| **mir** | C11 → machine code JIT for skilld (jail-isolated skills) |

### Architecture

```
cosmo-bsd-ai (~4-8GB image, boots from RAM)
├── llmd     (llamafile daemon — LLM inference)
├── hookd    (event routing — system events → LLM)
├── skilld   (skill execution in FreeBSD jails)
│   ├── e9studio skill (binary patching)
│   ├── ludofile skill (format detection)
│   └── custom skills...
├── mcpd     (Model Context Protocol daemon)
├── reasond  (PLAN→IMPLEMENT→VERIFY→REFLECT loop)
└── agentd   (multi-agent communication via jail mailboxes)
```

### JIT Context Clarification

| Context | JIT | Sandbox | Rationale |
|---------|-----|---------|-----------|
| e9studio patches | WAMR | WASM sandbox | Untrusted user patches need isolation |
| cosmo-bsd skilld | mir | FreeBSD jail | Jail is the sandbox; mir is faster |

Both JITs coexist. Different tools for different contexts.

### Integration Work

| Task | Owner | Est. Effort |
|------|-------|-------------|
| e9studio → skilld skill wrapper | ASM + Cosmo | 2 weeks |
| mir integration for skilld | Cosmo | 3 weeks |
| Daemon IPC (UNIX sockets) | Cosmo | 2 weeks |
| Jail management (agent isolation) | Cosmo | 2 weeks |
| Image build pipeline | Cosmo | 2 weeks |

### Success Criteria

1. cosmo-bsd-ai boots from single image
2. llmd serves LLM inference via UNIX socket
3. skilld executes e9studio as a skill in jail
4. agentd routes messages between agent jails
5. Full UNIX philosophy: everything is a file, daemons do one thing

### Timeline
**v2.0 Release:** v1.5 + 8-12 weeks

### Token Budget Estimate (v2.0)

| Component | Est. Agent Tokens |
|-----------|-------------------|
| skilld integration | 150K-200K |
| mir JIT integration | 100K-150K |
| Daemon IPC layer | 80K-120K |
| Jail management | 100K-150K |
| Image build | 50K-80K |
| **Total v2.0** | **~480K-700K** |

---

## Dependency Graph

```
                    ┌─────────────────────────────────────────┐
                    │              v1.0 CORE                  │
                    │                                         │
                    │  tedit-cosmo ←→ e9studio (glue layer)  │
                    │       ↑              ↑                  │
                    │       │              │                  │
                    │  cosmokramerpolitan (XED, cosmocc)      │
                    │       │              │                  │
                    │  llamafile ←─────────┘                  │
                    │  ludofile ←──────────────────────────   │
                    │                                         │
                    │  [Merge: cosmo-disasm ARM64 → e9studio] │
                    └─────────────────┬───────────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────────┐
                    │            v1.5 QUALITY                 │
                    │                                         │
                    │  opentau ──→ e9decompile integration    │
                    │                                         │
                    └─────────────────┬───────────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────────┐
                    │            v2.0 PLATFORM                │
                    │                                         │
                    │  cosmo-bsd daemons                      │
                    │    ├── llmd (llamafile wrapper)         │
                    │    ├── skilld (executes e9studio)       │
                    │    └── agentd (multi-agent jails)       │
                    │                                         │
                    │  mir ──→ skilld JIT                     │
                    │                                         │
                    └─────────────────────────────────────────┘
```

---

## Risk Register

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **PE patching harder than expected** | Medium | High | Start with read-only PE analysis; defer patching to v1.1 if needed |
| **WAMR cold start too slow** | Low | Medium | Profile early; consider AOT compilation if JIT insufficient |
| **ARM64 trampoline generation complex** | High | Medium | Defer ARM64 patching to v1.5; v1.0 is analysis-only for ARM64 |
| **Sokol multi-platform shims break** | Low | High | tedit-cosmo already solved this; follow their pattern |
| **cosmo-disasm merge conflicts** | Low | Low | ARM64 backend is isolated; merge should be clean |
| **LLM decompilation quality insufficient** | Medium | Low | General models (Qwen, LLaMA) are baseline; add LLM4Decompile in v2+ if needed |
| **cosmo-bsd scope creep** | High | High | Hard phase gate: v1.0 ships before ANY v2.0 work begins |
| **mir vs WAMR confusion** | Medium | Low | Document clearly: WAMR for e9studio, mir for cosmo-bsd skilld |

---

## Repos: Final Disposition

### Keep (8 repos)

| Repo | Phase | Role |
|------|-------|------|
| tedit-cosmo | v1.0 | UI layer |
| e9studio | v1.0 | Analysis + patching engine |
| cosmokramerpolitan | v1.0 | Build infrastructure |
| llamafile-llm | v1.0 | LLM runtime |
| ludofile | v1.0 | Format detection |
| opentau | v1.5 | Type inference |
| cosmo-bsd | v2.0 | Daemon platform |
| mir | v2.0 | skilld JIT |

### Merge (1 repo)

| Repo | Action |
|------|--------|
| **cosmo-disasm** | Port ARM64 backend to e9studio; delete repo after merge |

### Cut (4 repos)

| Repo | Reason |
|------|--------|
| **polytracker** | LLVM dependency violates Cosmopolitan philosophy |
| **binaryen** | WAMR already has optimizer; overkill for JIT patches |
| **rose-1** | 33K files for speculative source transforms; no concrete use case |
| **LLM4Decompile** | Defer to v2+; general models sufficient for v1 |

---

## Governance

### Phase Gates

| Gate | Criteria | Approver |
|------|----------|----------|
| v1.0 → v1.5 | v1.0 shipped, edit-patch-inject loop working | Vincent |
| v1.5 → v2.0 | v1.5 shipped, type inference integrated | Vincent |

### Weekly Checkpoints

- **Monday:** Status sync (blockers, progress, next steps)
- **Friday:** Demo day (show working code, not slides)

### Escalation Path

1. Agent-level: Try for 1 hour
2. Inter-agent: Collaborate for 1 day
3. PM escalation: Vincent notified

---

## Total Token Budget Summary

| Phase | Est. Tokens | Cumulative |
|-------|-------------|------------|
| v1.0 | 600K-1M | 600K-1M |
| v1.5 | 230K-350K | 830K-1.35M |
| v2.0 | 480K-700K | 1.3M-2M |

**Total project estimate:** 1.3M-2M tokens across all phases.

---

## Next Actions

### This Week (Week 1)

1. **ASM Agent:** Begin cosmo-disasm ARM64 merge
2. **Seeker Agent:** Map all e9studio APIs for glue layer design
3. **Cosmo Agent:** Verify XED integration path, document cosmocc build flow

### Next Week (Week 2)

1. **ASM + Seeker:** Glue layer design doc (tedit-cosmo ↔ e9studio)
2. **ASM:** ARM64 merge complete, PR ready
3. **Cosmo:** ZipOS bundling prototype

### Week 3-4

1. **All:** Glue layer implementation
2. **ASM:** Begin WASM patch pipeline

---

*"The best architecture is the one that ships." — Solution Arbiter*
