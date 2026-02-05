# Agent-Specific Hooks Matrix

## Recommended Hooks by Agent Type

### Coding Agents
**Agents:** webdev🌐, cosmo🌌, asm⚙️, roblox🧱

| Hook | Event | Purpose |
|------|-------|---------|
| `pre-commit-check` | `command:new` | Remind about uncommitted changes |
| `test-status` | `gateway:startup` | Show failing tests on boot |
| `lint-summary` | `command:new` | Surface lint warnings |

### Research Agents  
**Agents:** seeker🔍

| Hook | Event | Purpose |
|------|-------|---------|
| `source-log` | `command:new` | Log sources consulted |
| `confidence-tracker` | `command:new` | Record confidence assessments |

### Business/Ops Agents
**Agents:** ops📊, pearsonvue🎓

| Hook | Event | Purpose |
|------|-------|---------|
| `audit-trail` | `command` | Log all actions |
| `sync-status` | `gateway:startup` | Check external system sync |

### Infrastructure Agents
**Agents:** cicd🔄, neteng🔌, sitecraft🏗️

| Hook | Event | Purpose |
|------|-------|---------|
| `change-log` | `command:new` | Record infrastructure changes |
| `rollback-point` | `command:new` | Create restore points |
| `deploy-verify` | `command:new` | Verify last deployment health |

### Communication Agents
**Agents:** social📱

| Hook | Event | Purpose |
|------|-------|---------|
| `rate-limiter` | `command` | Prevent spam |
| `tone-check` | `agent:bootstrap` | Inject tone guidelines |

### Gaming Agents
**Agents:** ggleap🎮, metaquest🥽

| Hook | Event | Purpose |
|------|-------|---------|
| `session-tracker` | `command:new` | Log gaming sessions |
| `usage-stats` | `gateway:startup` | Show usage summary |

## Universal Hooks (All Agents)

| Hook | Event | Recommendation |
|------|-------|----------------|
| `session-memory` | `command:new` | **Always enable** |
| `command-logger` | `command` | Enable for audit needs |
| `boot-md` | `gateway:startup` | Enable if agent has startup routine |

## Hook Priority

1. **Essential:** session-memory (context preservation)
2. **Recommended:** Agent-specific primary hook
3. **Optional:** Audit/logging hooks
4. **Avoid:** Multiple hooks on same event (complexity)
