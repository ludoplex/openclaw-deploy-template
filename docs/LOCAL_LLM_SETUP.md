# Local LLM Setup for Token Delegation

## Overview

Run a local LLM on RTX 4060 (8GB VRAM) to handle simple tasks, saving Claude tokens for complex reasoning.

**Philosophy:** We use llamafile (Cosmopolitan APE) for portability and alignment with ApeSwarm patterns.

## Hardware

- **GPU:** NVIDIA GeForce RTX 4060
- **VRAM:** 8GB (6.8GB available)
- **Sufficient for:** 7B Q3/Q4 quantized models

## Current Setup

| Component | Details |
|-----------|---------|
| Binary | `bin/llamafile.exe` (v0.9.3, 307MB) |
| Model | `models/qwen2.5-7b-instruct-q3_k_m.gguf` (3.5GB) |
| GPU Layers | 29/29 offloaded to CUDA |
| Performance | ~23ms/token, ~43 tok/s |

## Option 1: llamafile (Recommended - APE Philosophy)

```powershell
# Install Ollama
winget install Ollama.Ollama

# Pull a model
ollama pull qwen2.5:7b

# Run as server (auto-starts on port 11434)
ollama serve

# Test
curl http://localhost:11434/api/generate -d '{"model":"qwen2.5:7b","prompt":"Hello"}'
```

## Option 2: llamafile (Single Binary)

```powershell
# Download llamafile + model
Invoke-WebRequest -Uri "https://huggingface.co/Mozilla/Mistral-7B-Instruct-v0.3-llamafile/resolve/main/Mistral-7B-Instruct-v0.3-Q4_K_M.llamafile" -OutFile "mistral-7b.llamafile"

# Make executable and run
./mistral-7b.llamafile --server --port 8081 --gpu-layers 99
```

## Option 3: llama.cpp (Most Control)

```powershell
# Clone and build with CUDA
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release

# Download model from HuggingFace
# Run server
./build/bin/llama-server -m models/qwen2.5-7b-instruct-q4_k_m.gguf -ngl 99 --port 8081
```

## OpenClaw Integration

Add to `openclaw.json`:

```json
{
  "agents": {
    "defaults": {
      "cliBackends": {
        "local": {
          "command": "curl",
          "args": ["-s", "http://localhost:11434/api/chat", "-d"],
          "input": "stdin",
          "output": "json"
        }
      }
    }
  }
}
```

Or configure as a model provider:

```json
{
  "models": {
    "providers": {
      "ollama": {
        "baseUrl": "http://localhost:11434/v1",
        "api": "openai-completions",
        "models": [
          {"id": "qwen2.5:7b", "name": "Qwen 2.5 7B (Local)", "contextWindow": 32768}
        ]
      }
    }
  }
}
```

## Delegation Strategy

**Use Local LLM for:**
- Text formatting and cleanup
- Simple summaries (< 500 words)
- Data extraction from structured text
- Template variable substitution
- JSON/YAML validation
- Basic code formatting

**Use Claude for:**
- Complex reasoning
- Multi-step planning
- Code generation with context
- Creative writing
- Tool use coordination
- Anything requiring deep understanding

## Token Savings Estimate

| Task Type | Claude Tokens | Local Handling | Savings |
|-----------|---------------|----------------|---------|
| Format text | 500-1000 | ✓ | ~$0.01/task |
| Summarize | 1000-2000 | ✓ | ~$0.02/task |
| Extract data | 500-1500 | ✓ | ~$0.015/task |
| Generate content | 2000+ | ✗ | - |
| Complex reasoning | 5000+ | ✗ | - |

With ~50 simple tasks/day delegated: **~$15-30/month savings**

## Quick Start

```powershell
# 1. Install Ollama
winget install Ollama.Ollama

# 2. Pull model (one-time, ~4.5GB download)
ollama pull qwen2.5:7b

# 3. Test
ollama run qwen2.5:7b "Summarize: The quick brown fox jumps over the lazy dog."

# 4. Keep running as service (already auto-starts)
```
