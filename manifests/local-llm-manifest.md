# Local LLM Stack Source Manifest (Mac M4)

Generated: 2026-02-10
Target Hardware: Apple M4 (16GB Unified Memory)
Purpose: Self-hosted LLM for customer support integration (Chatwoot/Vapi)

---

## Table of Contents
1. [Qwen 2.5 Models](#qwen-25-models)
2. [llama.cpp (Mac ARM64)](#llamacpp-mac-arm64)
3. [MLX Framework](#mlx-framework)
4. [Integration Patterns](#integration-patterns)
5. [Performance Benchmarks](#performance-benchmarks)
6. [Quick Start Guide](#quick-start-guide)

---

## Qwen 2.5 Models

### Overview
Qwen 2.5 is Alibaba Cloud's latest LLM series with significant improvements in coding, mathematics, instruction following, and structured output (JSON). Supports 128K context window and generates up to 8K tokens.

### Model Specifications

| Model | Parameters | Layers | Attention Heads | Context | License |
|-------|-----------|--------|-----------------|---------|---------|
| Qwen2.5-0.5B-Instruct | 0.5B | 24 | 14Q/2KV | 32K | Apache-2.0 |
| Qwen2.5-1.5B-Instruct | 1.5B | 28 | 12Q/2KV | 32K | Apache-2.0 |
| Qwen2.5-3B-Instruct | 3B | 36 | 16Q/2KV | 32K | Apache-2.0 |
| Qwen2.5-7B-Instruct | 7.61B (6.53B non-embed) | 28 | 28Q/4KV | 32K | Apache-2.0 |
| Qwen2.5-14B-Instruct | 14B | 40 | 40Q/8KV | 32K | Apache-2.0 |

### Memory Requirements (16GB M4)

| Model | Quantization | VRAM Requirement | Fits in 16GB? | Recommended |
|-------|-------------|------------------|---------------|-------------|
| Qwen2.5-7B | Q8_0 | ~8.5GB | ✅ Yes | For quality |
| Qwen2.5-7B | Q5_K_M | ~5.5GB | ✅ Yes | **Best balance** |
| Qwen2.5-7B | Q4_K_M | ~4.5GB | ✅ Yes | For speed |
| Qwen2.5-7B | Q4_0 | ~4.2GB | ✅ Yes | Fastest |
| Qwen2.5-14B | Q4_K_M | ~9GB | ✅ Yes | Higher quality |
| Qwen2.5-14B | Q8_0 | ~16GB | ⚠️ Tight | Not recommended |

### GGUF Model Downloads (llama.cpp)

**Source:** https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF

```bash
# Install huggingface-cli
pip install -U huggingface_hub

# Download Q5_K_M (recommended for M4 16GB)
huggingface-cli download Qwen/Qwen2.5-7B-Instruct-GGUF \
  --include "qwen2.5-7b-instruct-q5_k_m*.gguf" \
  --local-dir ./models \
  --local-dir-use-symlinks False

# For split files, merge them
llama-gguf-split --merge \
  qwen2.5-7b-instruct-q5_k_m-00001-of-00002.gguf \
  qwen2.5-7b-instruct-q5_k_m.gguf
```

**Available Quantizations:**
- `q2_K` - Smallest, lowest quality
- `q3_K_M` - Very small
- `q4_0` - Small, fast
- `q4_K_M` - Small, good quality
- `q5_0` - Medium
- `q5_K_M` - Medium, better quality **← Recommended**
- `q6_K` - Large, high quality
- `q8_0` - Largest, highest quality

### MLX Model Downloads

**Source:** https://huggingface.co/mlx-community/Qwen2.5-7B-Instruct-4bit

```bash
# MLX models download automatically on first use
# Or pre-download:
pip install mlx-lm huggingface_hub

python -c "from mlx_lm import load; load('mlx-community/Qwen2.5-7B-Instruct-4bit')"
```

**Available MLX versions:**
- `mlx-community/Qwen2.5-7B-Instruct` - Full precision (bf16)
- `mlx-community/Qwen2.5-7B-Instruct-4bit` - 4-bit quantized **← Recommended**
- `mlx-community/Qwen2.5-7B-Instruct-8bit` - 8-bit quantized

---

## llama.cpp (Mac ARM64)

### Source Repository
- **URL:** https://github.com/ggml-org/llama.cpp
- **License:** MIT
- **Apple Silicon:** First-class citizen with ARM NEON, Accelerate, and Metal

### Installation Methods

#### Method 1: Homebrew (Easiest)
```bash
brew install llama.cpp
```

#### Method 2: Build from Source (Recommended for Metal)
```bash
# Clone repository
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp

# Build with Metal acceleration (default on macOS)
cmake -B build
cmake --build build --config Release -j $(sysctl -n hw.ncpu)

# Binaries in build/bin/
# - llama-cli        (interactive CLI)
# - llama-server     (OpenAI-compatible server)
# - llama-gguf-split (merge/split GGUF files)
```

#### Build Flags for Metal Acceleration
```bash
# Metal is enabled by default on macOS, but explicitly:
cmake -B build \
  -DGGML_METAL=ON \
  -DGGML_ACCELERATE=ON \
  -DCMAKE_BUILD_TYPE=Release

# Verify Metal is enabled in build output:
# -- ggml-metal: found
# -- Accelerate: found
```

### Server Mode (llama-server)

#### Starting the Server
```bash
# Basic server with Qwen 2.5
./llama-server \
  -m ./models/qwen2.5-7b-instruct-q5_k_m.gguf \
  --host 0.0.0.0 \
  --port 8080 \
  -ngl 99 \
  -c 8192

# Full options for production
./llama-server \
  -m ./models/qwen2.5-7b-instruct-q5_k_m.gguf \
  --host 0.0.0.0 \
  --port 8080 \
  -ngl 99 \
  -c 8192 \
  --threads $(sysctl -n hw.physicalcpu) \
  --n-predict 2048 \
  --parallel 4 \
  --cont-batching \
  --flash-attn \
  --mlock
```

**Key Parameters:**
| Flag | Description | Recommended Value |
|------|-------------|-------------------|
| `-ngl` | GPU layers (99 = all on GPU) | `99` |
| `-c` | Context size | `8192` (for M4 16GB) |
| `--threads` | CPU threads | `$(sysctl -n hw.physicalcpu)` |
| `--parallel` | Concurrent requests | `2-4` |
| `--cont-batching` | Continuous batching | Enable |
| `--flash-attn` | Flash attention | Enable (faster) |
| `--mlock` | Lock model in RAM | Enable |

#### API Endpoints (OpenAI Compatible)

**Base URL:** `http://localhost:8080`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/chat/completions` | POST | Chat completions (streaming) |
| `/v1/completions` | POST | Text completions |
| `/v1/models` | GET | List loaded models |
| `/health` | GET | Server health check |
| `/props` | GET | Server properties |
| `/metrics` | GET | Prometheus metrics |

#### Chat Completions Example
```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5-7b-instruct",
    "messages": [
      {"role": "system", "content": "You are a helpful customer support agent."},
      {"role": "user", "content": "I need help with my order"}
    ],
    "temperature": 0.7,
    "max_tokens": 500,
    "stream": true
  }'
```

### Python Bindings (llama-cpp-python)

#### Installation
```bash
# With Metal support (recommended for Mac)
CMAKE_ARGS="-DGGML_METAL=on" pip install llama-cpp-python

# Or use pre-built wheel
pip install llama-cpp-python \
  --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/metal
```

#### Python API Usage
```python
from llama_cpp import Llama

# Initialize model
llm = Llama(
    model_path="./models/qwen2.5-7b-instruct-q5_k_m.gguf",
    n_gpu_layers=-1,  # All layers on GPU
    n_ctx=8192,       # Context window
    chat_format="chatml",
    verbose=False
)

# Chat completion
response = llm.create_chat_completion(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    max_tokens=500,
    temperature=0.7
)

print(response['choices'][0]['message']['content'])
```

#### Streaming Generation
```python
from llama_cpp import Llama

llm = Llama(
    model_path="./models/qwen2.5-7b-instruct-q5_k_m.gguf",
    n_gpu_layers=-1,
    n_ctx=8192
)

for chunk in llm.create_chat_completion(
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
):
    delta = chunk['choices'][0].get('delta', {})
    if 'content' in delta:
        print(delta['content'], end='', flush=True)
```

#### OpenAI-Compatible Server (Python)
```python
# Run as server
python -m llama_cpp.server \
  --model ./models/qwen2.5-7b-instruct-q5_k_m.gguf \
  --host 0.0.0.0 \
  --port 8080 \
  --n_gpu_layers -1 \
  --n_ctx 8192
```

### Batch Inference
```python
from llama_cpp import Llama

llm = Llama(
    model_path="./models/qwen2.5-7b-instruct-q5_k_m.gguf",
    n_gpu_layers=-1,
    n_ctx=8192,
    n_batch=512  # Batch size for prompt processing
)

# Process multiple prompts efficiently
prompts = [
    "What is machine learning?",
    "Explain quantum computing",
    "How do neural networks work?"
]

for prompt in prompts:
    response = llm.create_chat_completion(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    print(f"Q: {prompt}\nA: {response['choices'][0]['message']['content']}\n")
```

---

## MLX Framework

### Overview
MLX is Apple's machine learning framework optimized for Apple Silicon. Provides native Metal acceleration without requiring external dependencies.

**Repository:** https://github.com/ml-explore/mlx
**LLM Package:** https://github.com/ml-explore/mlx-lm

### Installation
```bash
# Install MLX-LM (includes MLX)
pip install mlx-lm

# Or via conda
conda install -c conda-forge mlx-lm
```

### Qwen Support Status
✅ **Fully Supported** - Qwen2/Qwen2.5 models work natively with MLX-LM. Thousands of pre-converted models available in the [MLX Community](https://huggingface.co/mlx-community) on Hugging Face.

### Python API

#### Basic Generation
```python
from mlx_lm import load, generate

# Load model (downloads automatically)
model, tokenizer = load("mlx-community/Qwen2.5-7B-Instruct-4bit")

# Generate with chat template
messages = [{"role": "user", "content": "Hello!"}]
prompt = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    tokenize=False
)

response = generate(
    model, 
    tokenizer, 
    prompt=prompt,
    max_tokens=500,
    verbose=True
)
print(response)
```

#### Streaming Generation
```python
from mlx_lm import load, stream_generate

model, tokenizer = load("mlx-community/Qwen2.5-7B-Instruct-4bit")

messages = [{"role": "user", "content": "Tell me a story"}]
prompt = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    tokenize=False
)

for response in stream_generate(model, tokenizer, prompt, max_tokens=512):
    print(response.text, end="", flush=True)
print()
```

#### CLI Usage
```bash
# Generate text
mlx_lm.generate --model mlx-community/Qwen2.5-7B-Instruct-4bit \
  --prompt "Hello, how are you?"

# Interactive chat
mlx_lm.chat --model mlx-community/Qwen2.5-7B-Instruct-4bit
```

### Converting Custom Models
```python
from mlx_lm import convert

# Convert HuggingFace model to MLX format
convert(
    "Qwen/Qwen2.5-7B-Instruct",
    quantize=True,  # 4-bit quantization
    upload_repo="your-username/Qwen2.5-7B-Instruct-4bit-mlx"
)
```

### Prompt Caching (Long Context)
```bash
# Cache a long system prompt
echo "You are a customer support agent for Acme Corp..." | \
  mlx_lm.cache_prompt \
  --model mlx-community/Qwen2.5-7B-Instruct-4bit \
  --prompt - \
  --prompt-cache-file support_prompt.safetensors

# Use cached prompt (faster subsequent requests)
mlx_lm.generate \
  --prompt-cache-file support_prompt.safetensors \
  --prompt "Customer: I need help with my order"
```

### MLX vs llama.cpp Comparison

| Feature | llama.cpp | MLX |
|---------|-----------|-----|
| **Installation** | Requires compilation | pip install |
| **Model Format** | GGUF | Safetensors |
| **Quantization** | 2-8 bit | 4/8 bit |
| **Metal Acceleration** | ✅ Yes | ✅ Native |
| **OpenAI API Server** | ✅ Built-in | ❌ Need wrapper |
| **Memory Efficiency** | Better with quantization | Good |
| **Prompt Caching** | ✅ Yes | ✅ Yes |
| **Fine-tuning** | ❌ No | ✅ LoRA/QLoRA |
| **Multimodal** | ✅ LLaVA, etc. | ✅ LLaVA |
| **Community Models** | HF (GGUF) | MLX Community |
| **Inference Speed** | ~15-20% faster | Easier to use |

**Recommendation:** Use **llama.cpp** for production (OpenAI-compatible API, better performance). Use **MLX** for rapid prototyping and fine-tuning.

---

## Integration Patterns

### HTTP API for Chatwoot Integration

#### Option 1: Direct llama-server Integration
```python
# chatwoot_webhook.py
from fastapi import FastAPI, Request
import httpx

app = FastAPI()
LLAMA_SERVER = "http://localhost:8080"

SYSTEM_PROMPT = """You are a helpful customer support agent for Acme Corp.
Be concise, friendly, and professional.
If you don't know something, say so and offer to escalate to a human agent.
"""

@app.post("/webhook/chatwoot")
async def chatwoot_webhook(request: Request):
    data = await request.json()
    
    # Extract message from Chatwoot webhook
    if data.get("event") != "message_created":
        return {"status": "ignored"}
    
    message = data.get("content", "")
    conversation_id = data.get("conversation", {}).get("id")
    
    # Call local LLM
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{LLAMA_SERVER}/v1/chat/completions",
            json={
                "model": "qwen2.5-7b-instruct",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": message}
                ],
                "max_tokens": 500,
                "temperature": 0.7
            },
            timeout=30.0
        )
    
    llm_response = response.json()
    reply = llm_response["choices"][0]["message"]["content"]
    
    # Send reply back to Chatwoot
    # (Use Chatwoot API to send message)
    return {"reply": reply, "conversation_id": conversation_id}
```

#### Option 2: Vapi Voice Integration
```python
# vapi_integration.py
from fastapi import FastAPI, WebSocket
import httpx
import json

app = FastAPI()
LLAMA_SERVER = "http://localhost:8080"

@app.websocket("/vapi")
async def vapi_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    async with httpx.AsyncClient() as client:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "transcript":
                user_text = message.get("text", "")
                
                # Stream response from LLM
                async with client.stream(
                    "POST",
                    f"{LLAMA_SERVER}/v1/chat/completions",
                    json={
                        "model": "qwen2.5-7b-instruct",
                        "messages": [
                            {"role": "system", "content": "You are a voice assistant."},
                            {"role": "user", "content": user_text}
                        ],
                        "stream": True,
                        "max_tokens": 200
                    }
                ) as response:
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            chunk = json.loads(line[6:])
                            if chunk.get("choices"):
                                delta = chunk["choices"][0].get("delta", {})
                                if "content" in delta:
                                    await websocket.send_json({
                                        "type": "response",
                                        "text": delta["content"]
                                    })
```

### Prompt Templates for Support Responses

#### Basic Customer Support Template
```python
SUPPORT_TEMPLATE = """<|im_start|>system
You are a customer support agent for {company_name}.
Your role: {role_description}

Guidelines:
- Be concise and helpful
- Use a friendly, professional tone
- If unsure, offer to escalate to a human agent
- Never make up information about products/policies
- Acknowledge customer emotions when appropriate

Product knowledge:
{product_knowledge}

Current date: {current_date}
<|im_end|>
<|im_start|>user
{customer_message}
<|im_end|>
<|im_start|>assistant
"""
```

#### With Conversation History
```python
def build_messages(history: list, new_message: str, system_prompt: str):
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add conversation history (limit to last N turns)
    for msg in history[-10:]:  # Last 5 exchanges
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    
    messages.append({"role": "user", "content": new_message})
    return messages
```

### Context Window Management

```python
from transformers import AutoTokenizer

# Load tokenizer for token counting
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-7B-Instruct")

def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))

def manage_context(
    messages: list,
    max_context: int = 8000,  # Leave room for response
    max_response: int = 500
):
    """Trim conversation history to fit context window."""
    available = max_context - max_response
    
    # Always keep system prompt
    system_msg = messages[0]
    system_tokens = count_tokens(system_msg["content"])
    available -= system_tokens
    
    # Keep messages from end, remove old ones if needed
    kept_messages = [system_msg]
    current_tokens = system_tokens
    
    for msg in reversed(messages[1:]):
        msg_tokens = count_tokens(msg["content"])
        if current_tokens + msg_tokens <= available:
            kept_messages.insert(1, msg)
            current_tokens += msg_tokens
        else:
            break
    
    return kept_messages
```

### Structured JSON Output
```python
# Qwen 2.5 has improved JSON output capabilities
import json
from llama_cpp import Llama

llm = Llama(
    model_path="./models/qwen2.5-7b-instruct-q5_k_m.gguf",
    n_gpu_layers=-1,
    n_ctx=8192,
    chat_format="chatml"
)

# Request JSON output
response = llm.create_chat_completion(
    messages=[
        {"role": "system", "content": "You output valid JSON only."},
        {"role": "user", "content": "Extract: 'John Smith called about order #12345 for a refund'"}
    ],
    response_format={
        "type": "json_object",
        "schema": {
            "type": "object",
            "properties": {
                "customer_name": {"type": "string"},
                "order_id": {"type": "string"},
                "issue_type": {"type": "string"},
                "sentiment": {"type": "string", "enum": ["positive", "neutral", "negative"]}
            },
            "required": ["customer_name", "order_id", "issue_type"]
        }
    }
)

result = json.loads(response['choices'][0]['message']['content'])
# {"customer_name": "John Smith", "order_id": "12345", "issue_type": "refund", "sentiment": "neutral"}
```

---

## Performance Benchmarks

### Expected Performance on M4 (16GB)

**Model: Qwen2.5-7B-Instruct-Q5_K_M**

| Metric | llama.cpp (Metal) | MLX |
|--------|------------------|-----|
| Prompt Processing | ~250-350 tokens/sec | ~200-300 tokens/sec |
| Token Generation | ~35-50 tokens/sec | ~30-45 tokens/sec |
| First Token Latency | ~100-200ms | ~150-250ms |
| Memory Usage | ~5.5GB | ~5.8GB |

**Model: Qwen2.5-7B-Instruct-Q4_K_M**

| Metric | llama.cpp (Metal) | MLX |
|--------|------------------|-----|
| Prompt Processing | ~300-400 tokens/sec | ~250-350 tokens/sec |
| Token Generation | ~45-60 tokens/sec | ~40-55 tokens/sec |
| First Token Latency | ~80-150ms | ~120-200ms |
| Memory Usage | ~4.5GB | ~4.8GB |

### Concurrent Request Performance

With `--parallel 4` on llama-server:

| Concurrent Requests | Tokens/sec (total) | Latency P50 | Latency P99 |
|--------------------|-------------------|-------------|-------------|
| 1 | ~45 | 200ms | 300ms |
| 2 | ~80 | 250ms | 400ms |
| 4 | ~120 | 400ms | 800ms |

### Memory vs Context Window

| Context Size | Additional Memory | Max Parallel |
|--------------|------------------|--------------|
| 2048 | +0.5GB | 6 |
| 4096 | +1.0GB | 4 |
| 8192 | +2.0GB | 3 |
| 16384 | +4.0GB | 2 |
| 32768 | +8.0GB | 1 |

**Recommendation for 16GB M4:**
- Context: 8192 tokens
- Parallel: 2-4 requests
- Model: Q5_K_M or Q4_K_M

---

## Quick Start Guide

### 1. Install Dependencies
```bash
# Homebrew (recommended for llama.cpp)
brew install llama.cpp cmake

# Python packages
pip install llama-cpp-python \
  --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/metal

pip install mlx-lm huggingface_hub httpx fastapi uvicorn
```

### 2. Download Model
```bash
mkdir -p ~/llm-models

huggingface-cli download Qwen/Qwen2.5-7B-Instruct-GGUF \
  --include "qwen2.5-7b-instruct-q5_k_m*.gguf" \
  --local-dir ~/llm-models \
  --local-dir-use-symlinks False

# Merge if split
cd ~/llm-models
llama-gguf-split --merge \
  qwen2.5-7b-instruct-q5_k_m-00001-of-00002.gguf \
  qwen2.5-7b-instruct-q5_k_m.gguf
```

### 3. Start Server
```bash
llama-server \
  -m ~/llm-models/qwen2.5-7b-instruct-q5_k_m.gguf \
  --host 0.0.0.0 \
  --port 8080 \
  -ngl 99 \
  -c 8192 \
  --parallel 2 \
  --cont-batching \
  --flash-attn
```

### 4. Test API
```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Hello!"}
    ],
    "max_tokens": 100
  }'
```

### 5. Production Systemd Service (macOS launchd)
```xml
<!-- ~/Library/LaunchAgents/com.llm.server.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.llm.server</string>
    <key>ProgramArguments</key>
    <array>
        <string>/opt/homebrew/bin/llama-server</string>
        <string>-m</string>
        <string>/Users/you/llm-models/qwen2.5-7b-instruct-q5_k_m.gguf</string>
        <string>--host</string>
        <string>0.0.0.0</string>
        <string>--port</string>
        <string>8080</string>
        <string>-ngl</string>
        <string>99</string>
        <string>-c</string>
        <string>8192</string>
        <string>--parallel</string>
        <string>2</string>
        <string>--cont-batching</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/llm-server.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/llm-server.err</string>
</dict>
</plist>
```

```bash
# Load service
launchctl load ~/Library/LaunchAgents/com.llm.server.plist

# Unload service
launchctl unload ~/Library/LaunchAgents/com.llm.server.plist
```

---

## Additional Resources

### Official Documentation
- llama.cpp: https://github.com/ggml-org/llama.cpp
- llama-cpp-python: https://llama-cpp-python.readthedocs.io/
- MLX-LM: https://github.com/ml-explore/mlx-lm
- Qwen 2.5: https://qwen.readthedocs.io/

### Model Repositories
- GGUF Models: https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF
- MLX Models: https://huggingface.co/mlx-community

### Community
- llama.cpp Discussions: https://github.com/ggml-org/llama.cpp/discussions
- MLX Community on HuggingFace: https://huggingface.co/mlx-community

---

*Last updated: 2026-02-10*
