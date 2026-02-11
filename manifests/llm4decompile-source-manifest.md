# LLM4Decompile Source Manifest

Generated: 2026-02-11
Source: https://github.com/ludoplex/LLM4Decompile (fork of albertan017/LLM4Decompile)
Path: `C:\LLM4Decompile`

## Overview

LLM4Decompile is the pioneering open-source LLM for decompilation. Converts Linux x86_64 binaries (GCC O0-O3) back to human-readable C source code. Achieves up to **64.9% re-executability** (code that compiles and passes tests).

## Architecture

```
Binary → objdump (ASM) → LLM → C Source Code
           ↓                        ↓
      Disassembly              Re-compile + Test
```

Two approaches:
1. **LLM4Decompile-End** — Direct binary-to-source
2. **LLM4Decompile-Ref** — Refine Ghidra pseudo-code

## Models (Hugging Face)

| Model | Size | Re-executability | HF Link |
|-------|------|------------------|---------|
| llm4decompile-1.3b-v1.5 | 1.3B | 27.3% | `LLM4Binary/llm4decompile-1.3b-v1.5` |
| llm4decompile-6.7b-v1.5 | 6.7B | 45.4% | `LLM4Binary/llm4decompile-6.7b-v1.5` |
| llm4decompile-1.3b-v2 | 1.3B | 46.0% | `LLM4Binary/llm4decompile-1.3b-v2` |
| llm4decompile-6.7b-v2 | 6.7B | 52.7% | `LLM4Binary/llm4decompile-6.7b-v2` |
| **llm4decompile-9b-v2** | 9B | **64.9%** | `LLM4Binary/llm4decompile-9b-v2` |
| llm4decompile-22b-v2 | 22B | 63.6% | `LLM4Binary/llm4decompile-22b-v2` |

## Key Files

### Evaluation (`evaluation/`)
| File | Purpose |
|------|---------|
| `run_evaluation_llm4decompile.py` | Main evaluation script |
| `run_evaluation_llm4decompile_singleGPU.py` | Single GPU version |
| `run_evaluation_llm4decompile_vllm.py` | vLLM accelerated |
| `server/text_generation.py` | Inference server |

### Ghidra Integration (`ghidra/`)
| File | Purpose |
|------|---------|
| `decompile.py` | Ghidra decompilation wrapper |
| `demo.py` | Demo script |

### SK²Decompile (`sk2decompile/`)
Two-phase approach: Skeleton → Skin
| File | Purpose |
|------|---------|
| `evaluation/evaluate_exe.py` | Executability eval |
| `evaluation/inf_type.py` | Type inference |
| `evaluation/gpt_judge.py` | GPT-based quality judge |

### Decompile Benchmark (`decompile-bench/`)
| File | Purpose |
|------|---------|
| `metrics/cal_edit_sim.py` | Edit similarity |
| `metrics/cal_execute_rate.py` | Re-executability |
| `llm_server.py` | LLM server |
| `run_exe_rate.py` | Run exe rate tests |

## Datasets

| Dataset | Description |
|---------|-------------|
| HumanEval-Decompile | 164 C functions, standard libs only |
| ExeBench | 2,621 real-world functions |
| decompile-bench | 2M training + 70K eval pairs |
| decompile-ghidra-100k | 100k Ghidra training samples |

## Usage

### Quick Start (Transformers)
```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained(
    "LLM4Binary/llm4decompile-6.7b-v2",
    torch_dtype=torch.bfloat16
).cuda()
tokenizer = AutoTokenizer.from_pretrained("LLM4Binary/llm4decompile-6.7b-v2")

# Assembly from objdump
asm = """<func0>:
   0:   push   %rbp
   1:   mov    %rsp,%rbp
   ...
"""

prompt = f"# This is the assembly code:\n{asm}\n# What is the source code?\n"
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=512)
print(tokenizer.decode(outputs[0]))
```

### With Ghidra (V2 models)
```python
# 1. Get Ghidra pseudo-code
ghidra_output = run_ghidra(binary_path)

# 2. Refine with LLM4Decompile-Ref
prompt = f"# Ghidra pseudo-code:\n{ghidra_output}\n# Refined C code:\n"
```

## Integration with Cosmopolitan

**Goal:** Run LLM4Decompile via llamafile in tedit-cosmo/e9studio.

**Approach:**
1. Quantize 6.7B model to GGUF (Q4_K_M)
2. Load via llamafile (~4GB VRAM)
3. Pipe objdump output → LLM → source display
4. Integrate with cosmo-disasm for disassembly

**Challenges:**
- 6.7B needs ~4-6GB VRAM quantized
- 9B (best) needs ~6-8GB VRAM
- Consider 1.3B for resource-constrained

## What Does NOT Exist

- ❌ No Windows PE support — Linux x86_64 only
- ❌ No ARM64 support (yet)
- ❌ No real-time decompilation — batch inference
- ❌ No GGUF models published (need to convert)
- ❌ No Cosmopolitan build

## Papers

- [Reverse Engineering: Decompiling Binary Code with Large Language Models](https://arxiv.org/abs/2403.05286)

---

*This manifest is ground truth. Model weights on Hugging Face.*
