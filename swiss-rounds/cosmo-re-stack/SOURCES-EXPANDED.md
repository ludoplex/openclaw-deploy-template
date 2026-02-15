# Expanded Source List (Added During Round 1)

**Note:** These sources were identified after specialists were dispatched. Round 2 specialists should incorporate these.

## Core Stack (Original)
| Repo | Path | Purpose |
|------|------|---------|
| tedit-cosmo | `C:\tedit-cosmo` | Portable systems editor |
| e9studio | `C:\e9studio` | Binary analysis + WAMR patching |
| llamafile-llm | `C:\llamafile-llm` | LLM runtime |
| cosmokramerpolitan | `C:\cosmokramerpolitan` | Cosmopolitan toolkit (17,929 files) |
| cosmo-disasm | `C:\cosmo-disasm` | Cross-arch disassembler |

## Newly Identified (Clone Complete)
| Repo | Path | Files | Purpose |
|------|------|-------|---------|
| **cosmo-bsd** | `C:\cosmo-bsd` | 54 | Cosmopolitan KISS BSD — portable datacenter in single binary |
| **ludofile** | `C:\ludofile` | 62 | Portable polyfile impl + polytracker + deep learning parsing + hex viewer |
| **polytracker** | `C:\polytracker` | 594 | LLVM taint tracking (to be integrated into ludofile) |
| **LLM4Decompile** | `C:\LLM4Decompile` | 92 | LLM decompilation models |
| **opentau** | `C:\opentau` | 158 | LLM gradual type inference |
| **mir** | `C:\mir` | 1,599 | Lightweight JIT compiler (MIR + C11 JIT) |
| **rose-1** | `C:\rose-1` | 33,125 | LLNL source-to-source compiler infrastructure |
| **binaryen** | `C:\binaryen` | 2,781 | WebAssembly optimizer/compiler toolchain |

## Integration Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     COSMO-RE-STACK: Universal Binary RE                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  FORMAT DETECTION              ANALYSIS                  AI LAYER          │
│  ┌─────────────┐              ┌─────────────┐           ┌─────────────┐    │
│  │  ludofile   │              │  e9studio   │           │LLM4Decompile│    │
│  │  (polyfile  │──────────────│  cosmo-     │───────────│  opentau    │    │
│  │  polytracker│              │  disasm     │           │  (types)    │    │
│  │  hex view)  │              └──────┬──────┘           └─────────────┘    │
│  └─────────────┘                     │                                     │
│                                      ▼                                     │
│  COMPILATION                   PATCHING                  RUNTIME           │
│  ┌─────────────┐              ┌─────────────┐           ┌─────────────┐    │
│  │   rose-1    │              │    WAMR     │           │ llamafile   │    │
│  │  (source    │──────────────│  binaryen   │───────────│  (LLM)      │    │
│  │  transform) │              │  (wasm opt) │           └─────────────┘    │
│  └─────────────┘              └──────┬──────┘                              │
│                                      │                                     │
│  JIT                                 ▼                                     │
│  ┌─────────────┐              ┌─────────────┐           ┌─────────────┐    │
│  │    mir      │              │ tedit-cosmo │           │  cosmo-bsd  │    │
│  │  (C11 JIT)  │──────────────│  (editor)   │───────────│  (OS layer) │    │
│  └─────────────┘              └─────────────┘           └─────────────┘    │
│                                                                             │
│  ALL BUILT WITH: cosmokramerpolitan (cosmocc → APE binaries)               │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Key Relationships

1. **ludofile** = polyfile + polytracker + cosmo-disasm (semi-forked, integrated)
2. **mir** = lightweight JIT alternative to WAMR for faster patch compilation
3. **rose-1** = source-to-source transforms (could generate optimized patch code)
4. **binaryen** = WASM optimization (already in e9studio's WAMR pipeline)
5. **cosmo-bsd** = potential target OS layer for the whole stack

## Questions for Round 2

1. How does mir compare to WAMR Fast JIT for patch compilation speed?
2. Can rose-1 source transforms optimize C patches before WASM compilation?
3. What's the relationship between ludofile's polytracker integration and e9studio's taint analysis?
4. Should cosmo-bsd be the deployment target or a separate product?
