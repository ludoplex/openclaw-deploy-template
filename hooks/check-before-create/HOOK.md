---
name: check-before-create
description: "Forces agents to check if files/resources exist before creating them"
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "events": ["tool:pre-execute"],
        "requires": { "config": ["workspace.dir"] },
      },
  }
---

# Check Before Create Hook

Prevents agents from creating files without first checking if they already exist.

## Behavior

- Intercepts `write` tool calls for new files
- Checks if the target path already exists
- If exists: blocks and tells agent to read it first
- If not exists: allows creation

## Why

Agents often recreate files that already exist, wasting tokens and potentially losing work:
- Creating a new config file when one exists
- Writing a utility function that's already in the codebase
- Reinventing helpers that are already available

This hook enforces: **check existence first, create only if needed**.
