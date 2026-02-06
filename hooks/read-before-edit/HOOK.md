---
name: read-before-edit
description: "Forces agents to read a file before editing it"
metadata:
  {
    "openclaw":
      {
        "emoji": "📖",
        "events": ["tool:pre-execute"],
        "requires": { "config": ["workspace.dir"] },
      },
  }
---

# Read Before Edit Hook

Prevents agents from editing or writing to files they haven't read in the current session.

## Behavior

- Tracks which files have been read via the `read` tool
- Blocks `edit` and `write` tool calls if the target file hasn't been read first
- Injects a warning message telling the agent to read the file first

## Why

Agents often attempt to edit files based on assumptions, leading to:
- Overwriting existing content they didn't know about
- Breaking code they haven't seen
- Missing context that would change their approach

This hook enforces the discipline: **read first, then edit**.
