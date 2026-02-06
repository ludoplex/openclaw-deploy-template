---
name: resource-paths-injector
description: "Injects relevant resource file paths into agent bootstrap context"
metadata:
  {
    "openclaw":
      {
        "emoji": "📂",
        "events": ["agent:bootstrap"],
        "requires": { "config": ["workspace.dir"] },
      },
  }
---

# Resource Paths Injector Hook

Injects file paths to relevant resources (especially .md files) into the agent's bootstrap context.

## Behavior

- Scans workspace for important resource files
- Injects a RESOURCES.md bootstrap file listing all paths
- Agent sees these paths at session start and knows what to READ

## Why

Agents can't read files they don't know exist:
- Documentation files they should consult
- Config files with important settings
- README files with project context
- Memory files with past decisions

This hook ensures agents are **told where resources are** so they can actually read them.
