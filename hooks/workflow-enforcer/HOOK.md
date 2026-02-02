---
name: workflow-enforcer
description: "Injects workflow enforcement reminder into agent bootstrap context"
homepage: https://docs.openclaw.ai/hooks
metadata:
  {
    "openclaw":
      {
        "emoji": "🔀",
        "events": ["agent:bootstrap"],
        "requires": { "config": ["workspace.dir"] },
      },
  }
---

# Workflow Enforcer Hook

Injects a workflow enforcement reminder into the agent's bootstrap context at session start.

## What It Does

1. Listens for `agent:bootstrap` events
2. Appends workflow routing instructions to the bootstrap files
3. Reminds the agent to use the right tool for each task:
   - **Qwen (local LLM)**: Simple code gen, formatting, JSON
   - **Shell tools**: File ops, git, curl, API testing
   - **lmarena.ai**: Architecture/planning decisions
   - **Claude**: Complex reasoning, multi-step orchestration

## Why

Token cost matters. This hook ensures the agent considers cheaper alternatives before using Claude for tasks that don't require complex reasoning.

## Configuration

No configuration needed. Enable via:

```bash
openclaw hooks enable workflow-enforcer
```
