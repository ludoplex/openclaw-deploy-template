# OpenTau Source Manifest

Generated: 2026-02-11
Source: https://github.com/ludoplex/opentau (fork of GammaTauAI/opentau)
Path: `C:\opentau`

## Overview

OpenTau uses Large Language Models for Gradual Type Inference. It infers types for TypeScript and Python programs using a search-based approach with LLM-generated type candidates.

**Key Innovation:** Tree-based program decomposition + fill-in-the-type fine-tuning achieves 47.4% files type-checking (14.5% improvement).

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      OpenTau                             │
├─────────────────────────────────────────────────────────┤
│  Source Code → Decomposition → LLM → Type Candidates    │
│      ↓              ↓            ↓         ↓            │
│  Compiler ← Type Check ← Search ← Ranking               │
└─────────────────────────────────────────────────────────┘
```

## Key Components

### Client (`client/`)
| File | Purpose |
|------|---------|
| `client/src/main.rs` | CLI entry point |
| `client/src/lib.rs` | Library interface |

### Evaluator (`evaluator/`)
| File | Purpose |
|------|---------|
| `evaluator/src/main.rs` | Evaluation harness |
| `evaluator/scripts/eval_dataset_analysis.py` | Dataset analysis |
| `evaluator/scripts/get_typecheck_stats.py` | Type-check statistics |

### Python AST Tools (`py-ast/`)
| File | Purpose |
|------|---------|
| `py-ast/main.py` | Python AST processing |
| `py-ast/check.py` | Type checking |
| `py-ast/printer.py` | AST pretty printing |
| `py-ast/stub_printer.py` | Stub file generation |

### Utils (`utils/`)
| File | Purpose |
|------|---------|
| `utils/filter_testfiles.py` | Filter test files |
| `utils/remove_comments.py` | Strip comments |
| `utils/remove_whitespace.py` | Normalize whitespace |

## Supported Languages

| Language | Compiler | Status |
|----------|----------|--------|
| TypeScript | `tsc` via `ts-node` | ✅ Full support |
| Python | `mypy` / `pyright` | 🚧 Work in progress |

## Models Supported

| Model | Type | Notes |
|-------|------|-------|
| SantaCoder | Local | Requires GPU |
| Incoder | Local | Requires GPU |
| OpenAI | API | Unmaintained |

## Protocol

OpenTau defines two protocols:
1. **Compiler Protocol** — Interface for type checkers
2. **Model Protocol** — Interface for LLM servers

Implementing these allows adding new languages/models.

## Dependencies

```
rust              # Core implementation
torch             # Model inference
tokenizers>=0.12  # Tokenization
transformers      # Model loading
ts-node, tsc      # TypeScript
mypy | pyright    # Python (optional)
```

## Usage

```bash
# Build
make

# Type-infer a TypeScript file
./out/client --file example.ts --model santacoder

# Evaluate on dataset
./out/evaluator --dataset typescript_dataset --model santacoder
```

## Integration with Cosmopolitan

**Goal:** Run OpenTau inference via llamafile on cosmo-bsd.

**Approach:**
1. Fine-tune Qwen/DeepSeek-Coder for fill-in-the-type
2. Export to GGUF for llamafile
3. Call from tedit-cosmo for IDE integration

## What Does NOT Exist

- ❌ No C/C++ type inference — TypeScript/Python only
- ❌ No real-time inference — batch processing
- ❌ No llamafile integration (yet)
- ❌ No Cosmopolitan build (Rust-based)

## Papers

- [Type Prediction With Program Decomposition and Fill-in-the-Type Training](https://arxiv.org/abs/2305.17145)

---

*This manifest is ground truth. Verify before integration.*
