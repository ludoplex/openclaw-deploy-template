# Recursive Reasoning Pattern

## Overview

All agents in this fleet can use recursive reasoning for complex problems.

## The Loop

```
PLAN → IMPLEMENT → VERIFY → REFLECT → REPEAT (max 5)
```

## When to Use

- Complex multi-step problems
- Debugging that isn't working
- Research with uncertainty
- Any task where first attempt might fail

## How to Invoke

Simply state: "Using recursive reasoning:" then follow the loop.

Or use the `reason` skill if installed.

## Constraints

1. **Max 5 iterations** — Prevents infinite loops
2. **Progress required** — Each iteration must advance
3. **Approach change after 2 stuck** — Don't repeat failures
4. **Persist learnings** — Write reflections to memory

## Skills Support

| Skill | Purpose |
|-------|---------|
| `reason` | Framework injection |
| `decompose` | Feynman-style breakdown |
| `reframe` | Cross-domain analogies |
| `confidence` | Bayesian tracking |

## Hook Support

| Hook | Event | Purpose |
|------|-------|---------|
| `reasoning-tracker` | `agent:bootstrap` | Inject framework |
| `session-memory` | `command:new` | Capture reflections |

## Installation

Skills and hooks available from skillsmith agent:
```
~/.openclaw/agents/skillsmith/templates/
├── skills/
│   ├── reason/SKILL.md
│   └── decompose/SKILL.md
├── hooks/
│   └── reasoning-tracker/
└── REASONING.md
```

Copy to agent workspace as needed.
