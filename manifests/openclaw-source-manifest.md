# OpenClaw Source Manifest

Generated: 2026-02-08
Source: npm package `openclaw@2026.2.6-3`
Commit: 85ed6c7fa4a61b68b277184b033a55bf125dbed3
Built: 2026-02-07T08:44:25.602Z
Package: C:\Users\user\AppData\Local\npm-cache\_npx\8718c3904bb5fece\node_modules\openclaw

**Note:** OpenClaw distributes compiled JS bundles in `dist/`. Source TypeScript is not in the npm package. This manifest is derived from official documentation and observed behavior.

---

## Core Tools (Agent Surface)

### `exec`
- **File:** `docs/tools/index.md` L185-211
- **Purpose:** Run shell commands in workspace
- **Parameters:**
  - `command` (required)
  - `yieldMs` (auto-background after timeout, default 10000)
  - `background` (immediate background)
  - `timeout` (seconds, default 1800)
  - `elevated` (run on host if sandboxed)
  - `host` (`sandbox | gateway | node`)
  - `security` (`deny | allowlist | full`)
  - `ask` (`off | on-miss | always`)
  - `node` (node id/name for `host=node`)
  - `pty` (true for real TTY)

### `process`
- **File:** `docs/tools/index.md` L213-225
- **Purpose:** Manage background exec sessions
- **Actions:** `list`, `poll`, `log`, `write`, `kill`, `clear`, `remove`

### `web_search`
- **File:** `docs/tools/index.md` L227-240
- **Purpose:** Search via Brave Search API
- **Parameters:** `query` (required), `count` (1-10)
- **Requires:** `BRAVE_API_KEY` + `tools.web.search.enabled`

### `web_fetch`
- **File:** `docs/tools/index.md` L242-260
- **Purpose:** Fetch URL content as markdown/text
- **Parameters:** `url` (required), `extractMode`, `maxChars`
- **Requires:** `tools.web.fetch.enabled`

### `browser`
- **File:** `docs/tools/index.md` L262-299
- **Purpose:** Control OpenClaw-managed browser
- **Actions:**
  - Lifecycle: `status`, `start`, `stop`, `tabs`, `open`, `focus`, `close`
  - Content: `snapshot` (aria/ai), `screenshot`, `act`, `navigate`, `console`, `pdf`, `upload`, `dialog`
  - Profiles: `profiles`, `create-profile`, `delete-profile`, `reset-profile`
- **Parameters:**
  - `profile` (defaults to `browser.defaultProfile`)
  - `target` (`sandbox | host | node`)
  - `node` (optional pin)

### `canvas`
- **File:** `docs/tools/index.md` L301-316
- **Purpose:** Drive node Canvas (present, eval, A2UI)
- **Actions:** `present`, `hide`, `navigate`, `eval`, `snapshot`, `a2ui_push`, `a2ui_reset`

### `nodes`
- **File:** `docs/tools/index.md` L318-351
- **Purpose:** Paired node discovery, notifications, camera/screen capture
- **Actions:**
  - Discovery: `status`, `describe`
  - Pairing: `pending`, `approve`, `reject`
  - macOS: `notify`, `run`
  - Media: `camera_snap`, `camera_clip`, `screen_record`
  - Location: `location_get`

### `image`
- **File:** `docs/tools/index.md` L353-368
- **Purpose:** Analyze image with configured image model
- **Parameters:** `image` (path/URL), `prompt`, `model`, `maxBytesMb`
- **Requires:** `agents.defaults.imageModel` configured

### `message`
- **File:** `docs/tools/index.md` L370-395
- **Purpose:** Cross-platform messaging (Discord/Google Chat/Slack/Telegram/WhatsApp/Signal/iMessage/MS Teams)
- **Actions:**
  - Core: `send`, `poll`, `react`, `reactions`, `read`, `edit`, `delete`
  - Pins: `pin`, `unpin`, `list-pins`
  - Threads: `thread-create`, `thread-list`, `thread-reply`
  - Search: `search`
  - Members: `member-info`, `role-info`, `role-add`, `role-remove`
  - Channels: `channel-info`, `channel-list`
  - Voice: `voice-status`
  - Events: `event-list`, `event-create`
  - Moderation: `timeout`, `kick`, `ban`
  - Assets: `sticker`, `emoji-list`, `emoji-upload`, `sticker-upload`

### `cron`
- **File:** `docs/tools/index.md` L397-410
- **Purpose:** Manage Gateway cron jobs and wakeups
- **Actions:** `status`, `list`, `add`, `update`, `remove`, `run`, `runs`, `wake`

### `gateway`
- **File:** `docs/tools/index.md` L412-428
- **Purpose:** Restart or update Gateway process
- **Actions:** `restart`, `config.get`, `config.schema`, `config.apply`, `config.patch`, `update.run`
- **Requires:** `commands.restart: true` for restart action

---

## Session Management Tools

### `sessions_list`
- **File:** `docs/tools/index.md` L430-450
- **Purpose:** List sessions
- **Parameters:** `kinds?`, `limit?`, `activeMinutes?`, `messageLimit?`

### `sessions_history`
- **File:** `docs/tools/index.md` L430-450
- **Purpose:** Inspect transcript history
- **Parameters:** `sessionKey` (or `sessionId`), `limit?`, `includeTools?`

### `sessions_send`
- **File:** `docs/tools/index.md` L430-450
- **Purpose:** Send message to another session
- **Parameters:** `sessionKey`, `message`, `timeoutSeconds?` (0 = fire-and-forget)
- **Behavior:** Runs reply-back ping-pong (max turns via `session.agentToAgent.maxPingPongTurns`)

### `sessions_spawn`
- **File:** `docs/tools/index.md` L430-450
- **Purpose:** Start sub-agent run with announce reply
- **Parameters:** `task`, `label?`, `agentId?`, `model?`, `runTimeoutSeconds?`, `cleanup?`
- **Behavior:** **Non-blocking** - returns `status: "accepted"` immediately
- **Important:** Cannot wait for results synchronously; announce arrives async

### `session_status`
- **File:** `docs/tools/index.md` L430-450
- **Purpose:** Get current session status
- **Parameters:** `sessionKey?`, `model?` (`default` clears override)

### `agents_list`
- **File:** `docs/tools/index.md` L451-459
- **Purpose:** List agent IDs for spawn targeting
- **Respects:** Per-agent `subagents.allowAgents` allowlist

---

## Memory Tools

### `memory_search`
- **File:** `docs/tools/index.md` (group:memory)
- **Purpose:** Search memory store
- **Requires:** `memorySearch.enabled` in agent config

### `memory_get`
- **File:** `docs/tools/index.md` (group:memory)
- **Purpose:** Retrieve memory entries

---

## File System Tools

### `read`
- **File:** `docs/tools/index.md` (group:fs)
- **Purpose:** Read file contents

### `write`
- **File:** `docs/tools/index.md` (group:fs)
- **Purpose:** Write file contents

### `edit`
- **File:** `docs/tools/index.md` (group:fs)
- **Purpose:** Edit file contents

### `apply_patch`
- **File:** `docs/tools/index.md` L180-184
- **Purpose:** Apply structured patches (multi-hunk edits)
- **Experimental:** Enable via `tools.exec.applyPatch.enabled` (OpenAI models only)

---

## Tool Groups

| Group | Expands To |
|-------|------------|
| `group:runtime` | `exec`, `bash`, `process` |
| `group:fs` | `read`, `write`, `edit`, `apply_patch` |
| `group:sessions` | `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `session_status` |
| `group:memory` | `memory_search`, `memory_get` |
| `group:web` | `web_search`, `web_fetch` |
| `group:ui` | `browser`, `canvas` |
| `group:automation` | `cron`, `gateway` |
| `group:messaging` | `message` |
| `group:nodes` | `nodes` |
| `group:openclaw` | All built-in OpenClaw tools |

---

## Tool Profiles

| Profile | Tools |
|---------|-------|
| `minimal` | `session_status` only |
| `coding` | `group:fs`, `group:runtime`, `group:sessions`, `group:memory`, `image` |
| `messaging` | `group:messaging`, `sessions_list`, `sessions_history`, `sessions_send`, `session_status` |
| `full` | No restriction |

---

## Hook System

### Hook Events
- **File:** `docs/hooks.md`
- **Events:**
  - Command: `command:new`, `command:reset`, `command:stop`
  - Lifecycle: `agent:start`, `agent:stop`
  - Custom events via plugins

### Hook Structure
```
hook-name/
├── HOOK.md          # Metadata in YAML frontmatter
└── handler.ts       # HookHandler implementation
```

### HookHandler Signature
- **File:** `docs/hooks.md` L174-196
- **Signature:** `async (event: HookEvent) => void`
- **Event fields:**
  - `type`: `"command"` | `"lifecycle"` | etc.
  - `action`: `"new"` | `"reset"` | `"stop"` | etc.
  - `sessionKey`: Current session key
  - `timestamp`: Event timestamp
  - `messages`: Array to push user-visible messages

### Hook Locations (precedence order)
1. Workspace: `<workspace>/hooks/`
2. Managed: `~/.openclaw/hooks/`
3. Bundled: `<openclaw>/dist/hooks/bundled/`

### Bundled Hooks
- `session-memory` - Save context to memory on `/new`
- `command-logger` - Log commands to `~/.openclaw/logs/commands.log`
- `boot-md` - Run `BOOT.md` on gateway start
- `soul-evil` - Swap SOUL.md during purge window

---

## Session Management

### Session Store
- **File:** `~/.openclaw/agents/<agentId>/sessions/sessions.json`
- **Type:** Key/value map `sessionKey -> SessionEntry`

### Transcript Storage
- **File:** `~/.openclaw/agents/<agentId>/sessions/<sessionId>.jsonl`
- **Format:** JSONL with tree structure (`id` + `parentId`)

### Session Entry Fields
- `sessionId`: Current transcript ID
- `updatedAt`: Last activity timestamp
- `chatType`: `direct | group | room`
- `provider`, `subject`, `room`, `space`, `displayName`: Metadata
- Toggles: `thinkingLevel`, `verboseLevel`, `reasoningLevel`, `elevatedLevel`, `sendPolicy`
- Model: `providerOverride`, `modelOverride`, `authProfileOverride`
- Tokens: `inputTokens`, `outputTokens`, `totalTokens`, `contextTokens`
- `compactionCount`: Auto-compaction count

### Session Key Patterns
- Main/direct: `agent:<agentId>:<mainKey>` (default `main`)
- Group: `agent:<agentId>:<channel>:group:<id>`
- Room: `agent:<agentId>:<channel>:room:<id>`
- Cron: `cron:<job.id>`
- Webhook: `hook:<uuid>`

---

## Configuration (`openclaw.json`)

### Agent Configuration
- **Path:** `~/.openclaw/openclaw.json`
- **Key sections:**
  - `agents.defaults` - Default agent settings
  - `agents.list[]` - Per-agent configurations
  - `browser` - Browser profiles and settings
  - `auth.profiles` - Auth configurations
  - `tools` - Tool allow/deny lists

### Per-Agent Settings
- `id`: Agent identifier
- `workspace`: Agent workspace path
- `identity.emoji`: Agent emoji
- `subagents.allowAgents[]`: Allowed spawn targets
- `model.primary`: Default model (e.g., `anthropic/claude-opus-4-5`)
- `memorySearch`: Memory search configuration
- `contextPruning`: Context pruning mode
- `compaction`: Compaction settings
- `heartbeat`: Heartbeat interval

---

## Extensions/Channels

### Available Extensions
- `telegram`, `whatsapp`, `discord`, `slack`, `signal`
- `msteams`, `googlechat`, `matrix`, `mattermost`
- `line`, `imessage`, `bluebubbles`
- `twitch`, `nostr`, `tlon`
- `feishu`, `zalo`, `nextcloud-talk`

### Extension Structure
Each extension in `extensions/` contains:
- `package.json` - Extension metadata
- Handler implementation

---

## What Does NOT Exist

- ❌ **No blocking `wait_for_subagent()`** - `sessions_spawn` is async-only, returns immediately
- ❌ **No hook mutation of bootstrapFiles** - Hooks cannot modify spawned agent bootstrap
- ❌ **No `sessions_spawn` result waiting** - Announcements arrive asynchronously
- ❌ **No source TypeScript in npm package** - Only compiled bundles in `dist/`
- ❌ **No Claude Code SDK integration** - OpenClaw wraps Claude API directly, not SDK
- ❌ **No `agent:bootstrap` hook for spawn injection** - Hooks fire on events, not spawn
- ❌ **No synchronous advisory triad** - All subagent coordination is async
- ❌ **No transcript mutation API** - Transcripts are append-only JSONL

---

## Key Architectural Constraints

### 1. Subagent Spawning is Non-Blocking
```typescript
// sessions_spawn returns immediately
sessions_spawn(agentId: "project-critic", task: "Analyze proposal")
// Returns: { status: "accepted" }
// Announcement arrives later as separate message
```

### 2. Two-Turn Advisory Pattern Required
```
Turn 1: User request → Agent spawns advisors → "Dispatched, will synthesize"
Turn 2: Announcements arrive → Agent synthesizes → Final response
```

### 3. Hook Capabilities
Hooks CAN:
- Run code on events (command:new, etc.)
- Push messages to user
- Write files to workspace
- Call external APIs

Hooks CANNOT:
- Mutate spawned agent bootstrap files
- Block and wait for subagent results
- Modify tool schemas at runtime

---

## Dependencies (Key)

| Package | Purpose |
|---------|---------|
| `@agentclientprotocol/sdk` | Agent Client Protocol |
| `@mariozechner/pi-coding-agent` | Coding agent core |
| `@mariozechner/pi-tui` | Terminal UI |
| `@whiskeysockets/baileys` | WhatsApp Web API |
| `grammy` | Telegram Bot API |
| `playwright-core` | Browser automation |
| `sqlite-vec` | Vector search |

---

*This manifest documents OpenClaw 2026.2.6 features. Verify against `docs/` before writing integration code.*
