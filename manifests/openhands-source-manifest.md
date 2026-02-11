# OpenHands Source Manifest

Generated: 2026-02-11
Source: https://github.com/All-Hands-AI/OpenHands @ main
Path: `C:\OpenHands`

## Overview

OpenHands (formerly OpenDevin) is an AI software development agent framework. Uses Action/Observation pattern with Docker sandboxing. **Note: V0 is deprecated (removal April 2026), V1 uses Software Agent SDK.**

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    OpenHands Agent                       │
├─────────────────────────────────────────────────────────┤
│  Controller → Memory → LLM → Actions → Runtime → Docker │
└─────────────────────────────────────────────────────────┘
```

## Core Modules (`openhands/`)

| Directory | Purpose |
|-----------|---------|
| `core/` | Main loop, config, setup |
| `controller/` | Agent control flow, state machine |
| `events/` | Action/Observation event system |
| `runtime/` | Docker sandboxed execution |
| `llm/` | LLM integration (litellm-based) |
| `memory/` | Context/history management |
| `agenthub/` | Agent implementations |
| `linter/` | Code linting integration |
| `mcp/` | Model Context Protocol |
| `server/` | Web server |
| `app_server/` | V1 application server |

## Core Functions

### Entry Point (`openhands/core/main.py`)
| Name | Signature | Line | Purpose |
|------|-----------|------|---------|
| `run_controller` | `async (config, initial_action, ...) -> State` | ~65 | Main async controller loop |

### Agent Loop (`openhands/core/loop.py`)
| Name | Signature | Line | Purpose |
|------|-----------|------|---------|
| `run_agent_until_done` | `async (controller, runtime, memory, end_states) -> None` | ~20 | Run until terminal state |

### Setup (`openhands/core/setup.py`)
| Name | Purpose |
|------|---------|
| `create_agent()` | Instantiate agent from config |
| `create_controller()` | Create controller with agent |
| `create_memory()` | Initialize memory system |
| `create_runtime()` | Create Docker runtime |
| `generate_sid()` | Generate session ID |
| `initialize_repository_for_runtime()` | Clone repo into runtime |

### Controller (`openhands/controller/`)
| Class | File | Purpose |
|-------|------|---------|
| `AgentController` | `agent_controller.py` | Main controller class |
| `State` | `state/state.py` | Agent state container |
| `ReplayManager` | `replay.py` | Replay previous sessions |

### Events (`openhands/events/`)

**Actions (agent → environment):**
| Class | File | Purpose |
|-------|------|---------|
| `Action` | `action/action.py` | Base action class |
| `CmdRunAction` | `action/commands.py` | Run shell command |
| `FileReadAction` | `action/files.py` | Read file |
| `FileWriteAction` | `action/files.py` | Write file |
| `BrowseURLAction` | `action/browse.py` | Open URL |
| `MessageAction` | `action/message.py` | Send message |
| `AgentFinishAction` | `action/agent.py` | Agent done |

**Observations (environment → agent):**
| Class | File | Purpose |
|-------|------|---------|
| `Observation` | `observation/observation.py` | Base observation |
| `CmdOutputObservation` | `observation/commands.py` | Command output |
| `FileReadObservation` | `observation/files.py` | File contents |
| `ErrorObservation` | `observation/error.py` | Error message |
| `BrowserOutputObservation` | `observation/browse.py` | Browser content |

### Runtime (`openhands/runtime/`)
| Class | File | Purpose |
|-------|------|---------|
| `Runtime` | `base.py` | Abstract runtime base |
| `DockerRuntime` | `docker/runtime.py` | Docker sandbox |
| `LocalRuntime` | `local/runtime.py` | Local execution (dev) |
| `RemoteRuntime` | `remote/runtime.py` | Remote execution |

### Agent Hub (`openhands/agenthub/`)
| Agent | File | Purpose |
|-------|------|---------|
| `CodeActAgent` | `codeact_agent/` | Default coding agent |
| `BrowsingAgent` | `browsing_agent/` | Web browsing agent |
| `DelegatorAgent` | `delegator_agent/` | Multi-agent delegation |

### Memory (`openhands/memory/`)
| Class | File | Purpose |
|-------|------|---------|
| `Memory` | `memory.py` | Main memory class |
| `ShortTermMemory` | `short_term_memory.py` | Recent context |
| `LongTermMemory` | `long_term_memory.py` | Persistent memory |

### LLM (`openhands/llm/`)
| Class | File | Purpose |
|-------|------|---------|
| `LLM` | `llm.py` | LLM wrapper (uses litellm) |

### Config (`openhands/core/config/`)
| Class | File | Purpose |
|-------|------|---------|
| `OpenHandsConfig` | `openhands_config.py` | Main config |
| `AgentConfig` | `agent_config.py` | Agent settings |
| `LLMConfig` | `llm_config.py` | LLM settings |
| `SandboxConfig` | `sandbox_config.py` | Runtime settings |

## Key Patterns

### Action/Observation Loop
```python
while not done:
    action = agent.step(state)  # Agent decides action
    observation = runtime.run(action)  # Execute in sandbox
    state.history.append((action, observation))
    if isinstance(action, AgentFinishAction):
        done = True
```

### Docker Sandboxing
```python
runtime = DockerRuntime(config.sandbox)
await runtime.connect()
obs = await runtime.run(CmdRunAction("pytest tests/"))
```

## V1 Migration (Software Agent SDK)

V0 code in `openhands/core/` is deprecated. V1 uses:
- **SDK**: https://github.com/OpenHands/software-agent-sdk
- **App Server**: `openhands/app_server/`

## What Does NOT Exist

- ❌ No built-in linting loop (unlike Aider's auto-lint)
- ❌ No tree-sitter integration for repo maps
- ❌ No auto-commit after changes
- ❌ No `--watch` mode for file monitoring
- ❌ No direct CLI for single prompts (web server only)
- ❌ V0 core scheduled for removal April 2026

## Installation

```bash
pip install openhands
# OR for development
git clone https://github.com/All-Hands-AI/OpenHands.git
cd OpenHands
pip install -e .
```

## CLI Usage (V0)

```bash
python -m openhands.core.main -t "Fix the bug in main.py"
```

---

*This manifest is ground truth. V0 paths deprecated — check V1 SDK for new development.*
