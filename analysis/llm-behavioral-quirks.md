# LLM Behavioral Quirks & Characteristics
## Comprehensive Analysis of Top-Tier Coding/Reasoning Models
*Last Updated: February 2026*

---

## Table of Contents
1. [Claude Opus 4 Series](#claude-opus-4-series)
2. [Claude Sonnet 4](#claude-sonnet-4)
3. [OpenAI Reasoning Models (o1/o3/GPT-5)](#openai-reasoning-models)
4. [Qwen 2.5 Coder](#qwen-25-coder)
5. [DeepSeek Coder V2/V3](#deepseek-coder-v2v3)
6. [Other Local Coding LLMs](#other-local-coding-llms)
7. [Model Comparison Matrix](#model-comparison-matrix)
8. [Prompting Best Practices](#prompting-best-practices)

---

## Claude Opus 4 Series

### Claude Opus 4 (May 2025)
**Model ID:** `claude-opus-4`

#### Key Characteristics
- **Hybrid Reasoning Model**: Offers both instant responses and extended thinking modes
- **1M Token Context Window**: Massive context for large codebases
- **Sustained Performance**: Can work continuously for several hours on long-running tasks
- **Background Task Support**: Can run Claude Code independently for long-running coding tasks

#### Behavioral Patterns
- **High Autonomy**: Excels at complex, multi-step agentic workflows with less hand-holding
- **Minimal Shortcuts**: 65% less likely to use shortcuts/loopholes than Sonnet 3.7 on agentic tasks
- **Memory Files**: When given local file access, skilled at creating and maintaining "memory files" to store key information
- **Thinking Summaries**: Uses smaller model to condense lengthy thought processes (~5% of the time)

#### Coding Style Preferences
- **Production-Ready Code**: Delivers code with minimal oversight
- **Strong Code Review**: Catches its own mistakes during debugging
- **Large Codebase Navigation**: Superior understanding of complex codebase architecture
- **Careful Planning**: Plans before executing, runs longer with sustained effort

#### Benchmarks
- **SWE-bench Verified**: 72.5%
- **Terminal-bench**: 43.2%
- **GPQA Diamond**: 74.9% (without extended thinking)
- **AIME**: 33.9% (without extended thinking)

#### Known Failure Modes
- Can be verbose when simpler responses would suffice
- Extended thinking increases latency and cost
- May over-engineer solutions for simple problems

#### Best Use Cases
- Complex multi-file refactoring
- Long-horizon agentic tasks
- Deep research and analysis
- Multi-system debugging
- Production code generation

---

### Claude Opus 4.1 (August 2025)
**Model ID:** `claude-opus-4-1`

#### Improvements over 4.0
- Drop-in replacement with superior performance
- More rigor and attention to detail
- Better handling of complex, multi-step problems

---

### Claude Opus 4.5 (November 2025)
**Model ID:** `claude-opus-4-5`

#### Key Behavioral Changes
- **Token Efficiency**: Uses dramatically fewer tokens than predecessors for similar/better outcomes
- **"Gets It" Factor**: Handles ambiguity and reasons about tradeoffs without hand-holding
- **Effort Control**: API parameter `effort` (low/medium/high) balances performance vs. latency
- **Near-Impossible Tasks**: Tasks that were challenging for Sonnet 4.5 became achievable

#### Notable Characteristics
- **Price Drop**: $5/$25 per million tokens (input/output) - Opus-level at lower cost
- **Robust Alignment**: Most robustly aligned model released, best-aligned frontier model by any developer
- **Prompt Injection Resistance**: Harder to trick than any other frontier model

#### Performance Highlights
- At medium effort: Matches Sonnet 4.5's best SWE-bench score with **76% fewer output tokens**
- At high effort: Exceeds Sonnet 4.5 by 4.3 percentage points while using **48% fewer tokens**
- Higher than any human candidate on Anthropic's notoriously difficult take-home exam (within 2-hour limit)

#### Customer Feedback Patterns
- "Opus 4.5 just 'gets it'"
- "Figures out the fix" when pointed at complex multi-system bugs
- Higher success rates, more surgical code edits
- 50-75% reductions in tool calling errors and build/lint errors

---

### Claude Opus 4.6 (February 2026)
**Model ID:** `claude-opus-4-6`

#### Latest Improvements
- **65.4% on Terminal-Bench 2.0** (industry-leading)
- **72.7% on OSWorld** (best computer-using model)
- Enhanced precision for production-ready code
- Better subagent orchestration for complex multi-agent systems

#### Behavioral Patterns
- **Active Subagent Management**: Tracks how sub-agents are doing, proactively steers them, terminates when needed
- **Complex Task Chains**: Handles longer, more complex task chains with fewer errors
- **Agentic Planning Excellence**: Breaks complex tasks into independent subtasks, runs tools/subagents in parallel

---

## Claude Sonnet 4

**Model ID:** `claude-sonnet-4`

### Key Differences from Opus

| Aspect | Sonnet 4 | Opus 4 |
|--------|----------|--------|
| Speed | Faster responses | Slower, more thorough |
| Token Efficiency | Good | Better (with effort control) |
| Long-horizon Tasks | Good | Excellent |
| Steerability | Enhanced | Standard |
| Price | $3/$15 per MTok | $5-15/$25-75 per MTok |

### Behavioral Characteristics
- **State-of-the-Art Coding**: 72.7% on SWE-bench (matches Opus on this benchmark)
- **Enhanced Steerability**: Greater control over implementations
- **Balanced Performance**: Optimal mix of capability and practicality
- **Reduced Navigation Errors**: From 20% to near zero in codebase navigation

### Best Use Cases
- Day-to-day coding tasks
- When speed matters more than absolute thoroughness
- Internal and external use cases requiring balance
- Autonomous multi-feature app development

---

## OpenAI Reasoning Models

### GPT-5 / o-series Models

**Model IDs:** `gpt-5`, `gpt-5-mini`, `gpt-5-nano`, `o3-mini`

#### Reasoning Token Architecture
- **Hidden Reasoning**: Models generate internal "reasoning tokens" for thinking
- **Reasoning Effort**: API parameter `effort` (low/medium/high) controls depth
- **Cost Implications**: Reasoning tokens billed as output tokens but not visible

#### Key Behavioral Patterns
- **Chain of Thought**: Long internal reasoning before responding
- **Self-Correction**: Models check their own work during reasoning
- **Tool Alternation**: Can alternate between reasoning and tool use

#### Prompting Differences from Claude
> "A reasoning model is like a senior co-worker—you can give them a goal and trust them to work out the details. A GPT model is like a junior coworker—they'll perform best with explicit instructions."

- Reasoning models work better with **high-level guidance**
- GPT models often benefit from **very precise instructions**

#### o3-mini Specifics (January 2025)
- **STEM Optimized**: Exceptional in science, math, and coding
- **First Small Reasoning Model** with function calling, Structured Outputs, developer messages
- **24% Faster** than o1-mini (7.7s vs 10.16s average response)
- **Three Effort Levels**: Low (speed), Medium (balanced), High (accuracy)
- **No Vision**: Use o1 for visual reasoning tasks

#### Context Window Management
- Reserve at least **25,000 tokens** for reasoning and outputs when starting
- Reasoning tokens can range from hundreds to tens of thousands
- Context window length differs across model snapshots

#### Encrypted Reasoning Items
- For stateless/zero-retention mode, must pass `reasoning.encrypted_content` in include parameter
- Required for multi-turn conversations with function calling

### Benchmarks (o3-mini)
| Benchmark | Low Effort | Medium Effort | High Effort |
|-----------|------------|---------------|-------------|
| AIME (math) | ~o1-mini level | ~o1 level | Exceeds o1 |
| SWE-bench Verified | - | Good | 39-61% (with scaffolding) |
| Codeforces | Exceeds o1-mini | Matches o1 | Above o1 |

### Known Quirks
- Can run out of tokens during reasoning with no visible output (still billed)
- Response quality varies significantly with effort setting
- Structured Outputs sometimes need careful schema design

---

## Qwen 2.5 Coder

**Model Sizes:** 0.5B, 1.5B, 3B, 7B, 14B, 32B

### Architecture & Training
- Built on Qwen2.5 architecture
- **5.5 trillion tokens** of training data (source code, text-code grounding, synthetic data)
- **128K token context** support
- **92 programming languages** covered
- Apache 2.0 license

### Size Recommendations

| Size | Best For | VRAM Required | Notes |
|------|----------|---------------|-------|
| 7B | Local development, quick tasks | ~8GB (Q4) | Sweet spot for quality/speed |
| 14B | Complex tasks, multi-file | ~12GB (Q4) | Good balance |
| 32B | Production-quality code | ~24GB (Q4) | Matches GPT-4o capabilities |

### Behavioral Patterns

#### Strengths
- **Multi-Language Excellence**: Performs well across 40+ languages including niche ones
- **Code Reasoning**: Strong correlation between code reasoning and instruction following
- **Math-Code Synergy**: Excellent at both math and code tasks ("science student")
- **General Ability Retention**: Maintains Qwen2.5's general capabilities

#### 7B-Instruct Benchmarks
| Benchmark | Score |
|-----------|-------|
| HumanEval | Competitive with larger models |
| MATH | 66.8 |
| GSM8K | 86.7 |
| AIME24 | 10.0 |
| MMLU | 68.5 |
| C-Eval | 61.4 |

### Compared to DeepSeek-Coder-V2-Lite
- Better on Math (66.8 vs 61.0)
- Better on MMLU-Pro (45.5 vs 42.4)
- Better on GPQA (35.6 vs 27.6)

### Known Issues
- Context window performance degrades without YaRN scaling for >32K tokens
- Needs `rope_scaling` config for full 128K context
- Can be verbose in explanations

### Best Prompting Practices
- Use system message: "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."
- Clear, structured prompts work well
- Benefits from explicit output format specifications

---

## DeepSeek Coder V2/V3

### DeepSeek-Coder-V2

**Architecture:** Mixture-of-Experts (MoE)
**Versions:** 
- Lite: 16B total / 2.4B active
- Full: 236B total / 21B active

#### Key Features
- **338 Programming Languages** (expanded from 86)
- **128K Context Length** (expanded from 16K)
- Performance comparable to GPT-4-Turbo on code tasks
- Based on DeepSeek-V2 architecture (MLA + DeepSeekMoE)

#### Benchmarks
| Task | Lite (16B/2.4B) | Full (236B/21B) |
|------|-----------------|-----------------|
| HumanEval | 81.1% | 90.2% |
| MBPP+ | 68.8% | 76.2% |
| LiveCodeBench | 24.3% | 43.4% |
| MATH | 61.8% | 75.7% |
| Aider | 44.4% | 73.7% |

#### Known Quirks (16B-Lite)
- **Chat Template Sensitivity**: Space after "Assistant:" can cause:
  - English questions receiving Chinese responses
  - Garbled text in responses
  - Excessive repetition
- Fixed in latest Ollama versions

### DeepSeek-V3

**Architecture:** 671B total / 37B activated MoE

#### Innovations
- **Auxiliary-Loss-Free Load Balancing**: Minimizes performance degradation
- **Multi-Token Prediction (MTP)**: Beneficial for performance + speculative decoding
- **FP8 Mixed Precision Training**: First validation at extremely large scale
- **Knowledge Distillation from DeepSeek-R1**: Incorporates verification and reflection patterns

#### Training Efficiency
- Only **2.788M H800 GPU hours** for full training
- Remarkably stable - no irrecoverable loss spikes or rollbacks
- 14.8 trillion diverse, high-quality tokens

#### Benchmarks
| Category | Benchmark | Score |
|----------|-----------|-------|
| Code | HumanEval | 65.2% |
| Code | LiveCodeBench | 40.5% |
| Code | SWE Verified | 42.0% |
| Math | AIME 2024 | 39.2% |
| Math | MATH-500 | 90.2% |
| General | MMLU | 88.5% |
| Writing | AlpacaEval 2.0 | 70.0% |

#### Behavioral Characteristics
- Strong at open-ended generation (85.5% Arena-Hard)
- Excellent long-context handling (128K verified via NIAH)
- Competitive with Claude 3.5 Sonnet and GPT-4o

---

## Other Local Coding LLMs

### CodeLlama 70B
- Meta's code-specialized Llama 2
- Good for Python, but limited multi-language support
- 100K context window (Python-focused variant)
- Becoming dated compared to newer options

### StarCoder 2
- BigCode project (15.5B, 7B, 3B sizes)
- **619 programming languages**
- Strong on The Stack v2 benchmark
- Open-source friendly licensing

### WizardCoder
- Fine-tuned from various base models
- Evol-Instruct method for code
- Good instruction following
- Multiple size variants available

### Phind CodeLlama 34B
- Based on CodeLlama 34B
- Optimized for developer Q&A
- Strong on HumanEval (67.6%)
- Good at explaining code

### Recommendations by Use Case

| Use Case | Best Local Option | Why |
|----------|-------------------|-----|
| Quick coding help | Qwen 2.5 Coder 7B | Fast, capable, small |
| Complex projects | Qwen 2.5 Coder 32B | Near-GPT4 quality |
| Multi-language | DeepSeek-Coder-V2-Lite | 338 languages |
| Low resources | Qwen 2.5 Coder 1.5B | Runs anywhere |
| Research/experiments | DeepSeek-V3 (API) | Best open-source quality |

---

## Model Comparison Matrix

### Coding Benchmarks Summary

| Model | SWE-bench | HumanEval | Context | Price (MTok) |
|-------|-----------|-----------|---------|--------------|
| Claude Opus 4.6 | ~72%+ | - | 1M | $5/$25 |
| Claude Sonnet 4 | 72.7% | - | 200K | $3/$15 |
| GPT-5 | - | - | Varies | Varies |
| o3-mini (high) | 39-61%* | - | Varies | Low |
| Qwen 2.5 Coder 32B | - | ~85% | 128K | Free (local) |
| DeepSeek-V3 | 42% | 65.2% | 128K | $0.27/$1.10 |

*With scaffolding

### Behavioral Trade-offs

| Model | Verbosity | Refusal Rate | Speed | Autonomy |
|-------|-----------|--------------|-------|----------|
| Claude Opus 4.x | Medium-High | Low | Slow-Medium | Very High |
| Claude Sonnet 4 | Medium | Low | Fast | High |
| GPT-5/o-series | Variable | Medium | Variable | Medium-High |
| Qwen 2.5 Coder | Medium | Very Low | Fast (local) | Medium |
| DeepSeek-V3 | Medium | Low | Medium | High |

---

## Prompting Best Practices

### For Claude Models
```
- Give high-level goals, let the model plan
- Use extended thinking for complex problems
- For coding: emphasize testing and edge cases
- Provide context files via memory/file access
- Use effort control: low for quick, high for thorough
```

### For OpenAI Reasoning Models
```
- High-level guidance works better than detailed instructions
- Let the model reason - don't micromanage
- Reserve 25K+ tokens for reasoning overhead
- Use effort parameter strategically
- For function calling: keep reasoning items across turns
```

### For Local Models (Qwen/DeepSeek)
```
- More explicit instructions help
- Provide code context inline when possible
- Use appropriate chat templates exactly
- Temperature 0.0-0.3 for code tasks
- Consider breaking complex tasks into steps
```

### Universal Tips
```
1. Be clear about expected output format
2. Provide relevant context/examples
3. Specify constraints and requirements upfront
4. For coding: include error messages, logs
5. For debugging: show minimal reproducible example
6. Ask model to think step-by-step for complex logic
```

---

## Sources

- Anthropic Blog/Documentation (anthropic.com)
- OpenAI Platform Documentation (platform.openai.com)
- Qwen Technical Reports (qwenlm.github.io, arXiv:2409.12186)
- DeepSeek GitHub Repositories (github.com/deepseek-ai)
- SWE-bench Leaderboard (swebench.com)
- Model system cards and announcements

---

*Note: Benchmarks and capabilities change rapidly. Always check official sources for latest data.*
