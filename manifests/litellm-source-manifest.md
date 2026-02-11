# LiteLLM Source Manifest

Generated: 2026-02-11
Source: https://github.com/BerriAI/litellm @ main
Path: `C:\litellm`

## Overview

LiteLLM is a unified interface for 100+ LLM providers. Call OpenAI, Anthropic, Azure, Bedrock, Cohere, etc. with a single API. Handles routing, fallbacks, retries, caching, and cost tracking.

## Core API (`litellm/`)

### Main Function (`litellm/main.py`)
| Name | Signature | Line | Purpose |
|------|-----------|------|---------|
| `completion` | `(model, messages, **kwargs) -> ModelResponse` | ~500 | Sync chat completion |
| `acompletion` | `async (model, messages, **kwargs) -> ModelResponse` | ~600 | Async chat completion |
| `text_completion` | `(model, prompt, **kwargs) -> TextCompletionResponse` | ~1500 | Legacy text completion |
| `embedding` | `(model, input, **kwargs) -> EmbeddingResponse` | ~2000 | Get embeddings |
| `aembedding` | `async (model, input, **kwargs) -> EmbeddingResponse` | ~2100 | Async embeddings |
| `image_generation` | `(model, prompt, **kwargs) -> ImageResponse` | ~2500 | Generate images |
| `transcription` | `(model, file, **kwargs) -> TranscriptionResponse` | ~3000 | Audio transcription |

### Router (`litellm/router.py`)
| Class/Function | Line | Purpose |
|----------------|------|---------|
| `Router` | ~150 | Multi-model router with load balancing |
| `Router.completion()` | ~500 | Route completion to best model |
| `Router.acompletion()` | ~600 | Async routed completion |
| `Router.get_available_deployment()` | ~800 | Get healthy deployment |

### Router Strategies
| Strategy | File | Purpose |
|----------|------|---------|
| `simple_shuffle` | `router_strategy/simple_shuffle.py` | Random selection |
| `LowestLatencyLoggingHandler` | `router_strategy/lowest_latency.py` | Pick fastest |
| `LowestCostLoggingHandler` | `router_strategy/lowest_cost.py` | Pick cheapest |
| `LowestTPMLoggingHandler` | `router_strategy/lowest_tpm_rpm.py` | Load balance by TPM |
| `LeastBusyLoggingHandler` | `router_strategy/least_busy.py` | Pick least busy |
| `RouterBudgetLimiting` | `router_strategy/budget_limiter.py` | Budget enforcement |

### Types (`litellm/types/`)
| Type | File | Purpose |
|------|------|---------|
| `ModelResponse` | `utils.py` | Chat completion response |
| `TextCompletionResponse` | `utils.py` | Text completion response |
| `EmbeddingResponse` | `utils.py` | Embedding response |
| `Message` | `utils.py` | Chat message |
| `Choices` | `utils.py` | Response choices |
| `Usage` | `utils.py` | Token usage stats |
| `GenericLiteLLMParams` | `router.py` | Router params |

### Utils (`litellm/utils.py`)
| Function | Purpose |
|----------|---------|
| `get_llm_provider(model)` | Detect provider from model name |
| `token_counter(model, messages)` | Count tokens |
| `get_api_key(provider, api_key)` | Resolve API key |
| `get_optional_params(...)` | Build provider-specific params |
| `convert_to_model_response_object()` | Normalize response |
| `exception_type(model, error)` | Map provider errors |

### Caching (`litellm/caching/`)
| Class | File | Purpose |
|-------|------|---------|
| `DualCache` | `caching.py` | In-memory + Redis cache |
| `InMemoryCache` | `caching.py` | Fast local cache |
| `RedisCache` | `caching.py` | Distributed cache |

### Budget Manager (`litellm/budget_manager.py`)
| Function | Purpose |
|----------|---------|
| `BudgetManager.get_current_budget()` | Check remaining budget |
| `BudgetManager.update_cost()` | Track spend |
| `BudgetManager.is_budget_exceeded()` | Check limits |

### Cost Calculator (`litellm/cost_calculator.py`)
| Function | Purpose |
|----------|---------|
| `completion_cost(response)` | Calculate cost from response |
| `cost_per_token(model)` | Get per-token pricing |

### Exceptions (`litellm/exceptions.py`)
| Exception | Purpose |
|-----------|---------|
| `AuthenticationError` | Invalid API key |
| `RateLimitError` | Rate limited |
| `BadRequestError` | Invalid request |
| `ContextWindowExceededError` | Too many tokens |
| `APIConnectionError` | Network error |
| `Timeout` | Request timeout |
| `BudgetExceededError` | Over budget |

## Provider Support

### Naming Convention
```
provider/model-name

openai/gpt-4o
anthropic/claude-sonnet-4-20250514
azure/gpt-4-deployment-name
bedrock/anthropic.claude-3-sonnet
cohere/command-r-plus
together_ai/mistralai/Mixtral-8x7B
ollama/llama3
openrouter/anthropic/claude-3-opus
```

### Provider-Specific Files (`litellm/llms/`)
| Provider | File | 
|----------|------|
| OpenAI | `openai/` |
| Anthropic | `anthropic/` |
| Azure | `azure/` |
| Bedrock | `bedrock/` |
| Vertex AI | `vertex_ai/` |
| Cohere | `cohere/` |
| Ollama | `ollama/` |
| Together | `together_ai/` |

## Key Patterns

### Basic Completion
```python
import litellm

response = litellm.completion(
    model="anthropic/claude-sonnet-4-20250514",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.choices[0].message.content)
```

### Router with Fallbacks
```python
from litellm import Router

router = Router(
    model_list=[
        {"model_name": "gpt-4", "litellm_params": {"model": "openai/gpt-4"}},
        {"model_name": "gpt-4", "litellm_params": {"model": "azure/gpt-4-deployment"}},
    ],
    fallbacks=[{"gpt-4": ["claude-3"]}],
    routing_strategy="lowest-latency"
)

response = await router.acompletion(model="gpt-4", messages=messages)
```

### Streaming
```python
response = litellm.completion(
    model="openai/gpt-4o",
    messages=messages,
    stream=True
)
for chunk in response:
    print(chunk.choices[0].delta.content or "", end="")
```

### Caching
```python
import litellm
litellm.cache = litellm.Cache(type="redis", host="localhost", port=6379)

# Subsequent identical calls hit cache
response = litellm.completion(model="gpt-4", messages=messages, caching=True)
```

## Configuration

### Environment Variables
```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
AZURE_API_KEY=...
AZURE_API_BASE=https://xxx.openai.azure.com/
LITELLM_LOG=DEBUG  # Enable logging
```

### Proxy Server
```bash
litellm --model gpt-4 --port 8000
# Exposes OpenAI-compatible API at localhost:8000
```

## What Does NOT Exist

- ❌ No built-in agent loop — just LLM calls
- ❌ No code execution — use with OpenHands/Aider
- ❌ No repo context — just chat completion
- ❌ No memory/history management — stateless
- ❌ No tool calling abstraction (passes through to provider)

## Installation

```bash
pip install litellm
# OR for development
git clone https://github.com/BerriAI/litellm.git
pip install -e .
```

---

*This manifest is ground truth. Verify signatures before use.*
