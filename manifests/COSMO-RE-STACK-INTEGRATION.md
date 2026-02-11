# Cosmopolitan RE + AI Stack Integration Plan

Generated: 2026-02-11

## Vision

A **portable, single-binary reverse engineering IDE with AI-powered decompilation and type inference**, running on cosmo-bsd.

## The Stack

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                               │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  tedit-cosmo / e9studio (cosmo-sokol GUI)                   │    │
│  │  - Editor + Disasm view + Decompile view + Type browser     │    │
│  └─────────────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────────────┤
│                         AI INFERENCE                                 │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐           │
│  │  llamafile    │  │ LLM4Decompile │  │   opentau     │           │
│  │  (local LLM)  │  │ (decompile)   │  │ (type infer)  │           │
│  └───────────────┘  └───────────────┘  └───────────────┘           │
├─────────────────────────────────────────────────────────────────────┤
│                         ANALYSIS LIBS                                │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐           │
│  │ cosmo-disasm  │  │    resym      │  │  tree-sitter  │           │
│  │ (disassembly) │  │ (PDB types)   │  │ (code parse)  │           │
│  └───────────────┘  └───────────────┘  └───────────────┘           │
├─────────────────────────────────────────────────────────────────────┤
│                         FOUNDATION                                   │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  cosmokramerpolitan + cosmo-bsd                             │    │
│  │  (Actually Portable Executables, runs everywhere)           │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Status

| Component | Repo | Status | Cosmo Ready |
|-----------|------|--------|-------------|
| cosmokramerpolitan | `C:\cosmokramerpolitan` | ✅ Cloned | ✅ IS Cosmo |
| cosmo-bsd | `C:\cosmo-bsd` | ✅ Exists | ✅ IS Cosmo |
| cosmo-sokol | `C:\cosmo-sokol` | ✅ Exists | ✅ IS Cosmo |
| tedit-cosmo | `C:\tedit-cosmo` | ✅ Refactored | 🚧 Needs build test |
| e9studio | `C:\e9studio` | ✅ Exists | 🚧 Needs integration |
| cosmo-disasm | `C:\cosmo-disasm` | ✅ Exists | ✅ Built for Cosmo |
| llamafile | `C:\llamafile-llm` | ✅ Exists | ✅ IS Cosmo |
| LLM4Decompile | `C:\LLM4Decompile` | ✅ Cloned | ❌ Needs GGUF export |
| opentau | `C:\opentau` | ✅ Cloned | ❌ Rust, needs WASM |
| resym | `C:\resym` | ✅ Cloned | ❌ Rust, needs WASM |
| tree-sitter | `C:\tree-sitter` | ✅ Cloned | ⚠️ C, can port |

## Integration Phases

### Phase 1: Core IDE (tedit-cosmo + e9studio)
1. ✅ Port tedit-cosmo to cosmo-sokol (done, awaiting build test)
2. 🚧 Integrate cosmo-disasm for binary view
3. 🚧 Merge e9studio binary patching into tedit-cosmo
4. Add file browser, project management

### Phase 2: AI Decompilation
1. Export LLM4Decompile-6.7B to GGUF format
2. Integrate llamafile for inference
3. Pipe: cosmo-disasm → LLM4Decompile → source view
4. Add iterative refinement (edit → recompile → compare)

### Phase 3: Type Inference
1. WASM-ify opentau (run in WAMR)
2. Integrate with tree-sitter for code parsing
3. Auto-infer types for decompiled C code
4. Optional: resym for PDB type extraction (Windows binaries)

### Phase 4: cosmo-bsd Integration
1. Package as single APE binary
2. Boot from USB/network
3. Air-gapped RE workstation

## Model Requirements

| Model | Size (Quantized) | VRAM | Purpose |
|-------|------------------|------|---------|
| LLM4Decompile-1.3B | ~1GB (Q4) | 2GB | Fast decompilation |
| LLM4Decompile-6.7B | ~4GB (Q4) | 6GB | Best decompilation |
| Qwen2.5-7B-Coder | ~5GB (Q5) | 6GB | Type inference, code gen |

## File Layout (Proposed)

```
cosmo-re-ide.com (single APE binary)
├── /zip/                        # ZipOS embedded assets
│   ├── models/                  # Quantized GGUF models
│   │   ├── llm4decompile-1.3b-q4.gguf
│   │   └── qwen-7b-coder-q5.gguf
│   ├── grammars/                # tree-sitter grammars
│   ├── themes/                  # Editor themes
│   └── config/                  # Default config
├── tedit-cosmo core             # Editor + GUI
├── cosmo-disasm                 # Disassembly
├── llamafile runtime            # LLM inference
└── WAMR + opentau.wasm          # Type inference
```

## Build Strategy

```makefile
# Step 1: Build core with cosmocc
cosmocc -o tedit.com src/*.c -Ideps/sokol -Ideps/cimgui

# Step 2: Embed models
zip -r cosmo-re-ide.com /zip/models/*.gguf

# Step 3: Embed WASM modules
zip -r cosmo-re-ide.com /zip/wasm/opentau.wasm
```

## Related Manifests

- `aider-source-manifest.md` — Reference for auto-lint/test patterns
- `tree-sitter-source-manifest.md` — Code parsing API
- `litellm-source-manifest.md` — LLM abstraction (not needed, use llamafile)
- `openhands-source-manifest.md` — Action/Observation pattern (reference)

## Action Items

1. [ ] Build tedit-cosmo with cosmocc
2. [ ] Export LLM4Decompile to GGUF
3. [ ] Create cosmo-re-ide integration branch
4. [ ] WASM-ify opentau
5. [ ] Design unified UI for RE workflow
6. [ ] Package as single APE

---

*This is the integration roadmap. Individual manifests have API details.*
