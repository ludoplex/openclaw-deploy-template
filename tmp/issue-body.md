## Bug Description

`sessions_spawn` calls fail with:

```
TypeError: Cannot read properties of undefined (reading 'trim')
```

## Environment

- **Version:** 2026.2.2 (also tested on 2026.1.30)
- **OS:** Windows_NT 10.0.26200 (x64)
- **Node:** v24.11.1

## Reproduction

Any `sessions_spawn` call fails. Tested:

```json
{"agentId": "webdev", "task": "Quick test", "runTimeoutSeconds": 60}
{"task": "Test spawn without specific agent"}
```

Both return `status: "accepted"` with a `childSessionKey` and `runId`, then immediately fail.

## Observed Output

```
runtime 0s • tokens n/a
TypeError: Cannot read properties of undefined (reading 'trim')
Findings: (no output)
```

## Evidence

1. No transcript file is created at the reported path
2. `runtime 0s` indicates failure before any LLM call
3. Error is identical across all tested agents (webdev, ggleap, roblox, cosmo, main)
4. Error persists when spawning without `agentId` (defaults to main)

## Config

```json
{
  "agents": {
    "defaults": {
      "subagents": { "maxConcurrent": 8 }
    },
    "list": [
      {
        "id": "main",
        "default": true,
        "workspace": "C:\\Users\\user\\.openclaw\\workspace",
        "subagents": {
          "allowAgents": ["webdev", "ggleap", "roblox", "cosmo", "ops", "social", "course", "pearsonvue", "asm", "metaquest", "neteng"]
        }
      },
      {
        "id": "webdev",
        "workspace": "C:\\Users\\user\\.openclaw\\agents\\webdev",
        "tools": { "profile": "coding" }
      }
    ]
  }
}
```

## Workspace Contents (webdev example)

```
C:\Users\user\.openclaw\agents\webdev\
├── AGENTS.md (1194 bytes)
├── HEARTBEAT.md (168 bytes)
├── IDENTITY.md (635 bytes)
├── SOUL.md (343 bytes)
├── TOOLS.md (860 bytes)
├── USER.md (481 bytes)
├── agent\auth-profiles.json (460 bytes)
└── sessions\sessions.json (13183 bytes)
```
