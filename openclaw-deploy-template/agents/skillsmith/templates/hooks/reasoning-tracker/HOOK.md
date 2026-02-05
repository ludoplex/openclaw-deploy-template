---
name: reasoning-tracker
description: "Track reasoning iterations and inject framework"
metadata: { "openclaw": { "emoji": "🔄", "events": ["agent:bootstrap"] } }
---

# Reasoning Tracker

Injects reasoning framework and iteration state into agent bootstrap.

## What It Does
- Adds REASONING.md to bootstrap files
- Tracks iteration count across session
- Enforces max 5 iterations

## Config
```json
{
  "hooks": {
    "internal": {
      "entries": {
        "reasoning-tracker": {
          "enabled": true,
          "maxIterations": 5
        }
      }
    }
  }
}
```
