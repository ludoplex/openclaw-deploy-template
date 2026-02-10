# Cursor IDE Binary Manifest

Generated: 2026-02-08
Binary: C:\Program Files\cursor\resources\app
Version: 2.2.44
VSCode Base: 1.105.1
Distro: 21c8d8ea1e46d97c5639a7cabda6c0e063cc8dd5
Publisher: Anysphere, Inc.

**Note:** Cursor is a closed-source fork of VS Code. This manifest is derived from observable package.json files, extension sources, and product.json. Core application logic is compiled in `out/main.js`.

---

## Core Architecture

### Entry Points
- **CLI:** `C:\Program Files\cursor\resources\app\bin\cursor.cmd`
- **Main:** `out/main.js` (compiled Electron main process)
- **Bootstrap:** `out/bootstrap-fork.js`

### Key Files
| File | Purpose |
|------|---------|
| `package.json` | App metadata, version |
| `product.json` | Product configuration, URLs, extensions |
| `out/main.js` | Compiled main application |
| `node_modules.asar` | Bundled dependencies (Electron archive) |

---

## Cursor-Specific Extensions

### `cursor-mcp`
- **Path:** `extensions/cursor-mcp/`
- **Purpose:** Model Context Protocol (MCP) integration
- **Source:** `src/main.ts` (TypeScript source available)
- **API:**
  - `CursorMcpExtensionApi.getMcpLease()` - Get MCP lease for tool access
  - OAuth deep-link handler: `cursor://anysphere.cursor-mcp/oauth/callback`
- **Activation:** `onStartupFinished`, `onUri`
- **Key Files:**
  - `src/main.ts` - Extension activation
  - `src/mcpLease.ts` - MCP lease management
  - `src/everythingProvider.ts` - Provider implementation
  - `src/commands/mcpCommands.js` - MCP commands
  - `src/commands/mcp/oauth.js` - OAuth flow

### `cursor-agent-exec`
- **Path:** `extensions/cursor-agent-exec/`
- **Purpose:** Agent execution capabilities (commands, files, tools)
- **Activation:** `*` (always active)
- **Description:** "Provides agent execution capabilities for Cursor, enabling agents to run commands, interact with files, and use tools with user permissions and approvals"

### `cursor-browser-automation`
- **Path:** `extensions/cursor-browser-automation/`
- **Purpose:** MCP server for browser automation
- **Source:** `src/browserTools.ts` (TypeScript source available)
- **Features:**
  - Accessibility tree snapshots (YAML format)
  - Origin allowlist enforcement
  - Large snapshot file redirection (`~/.cursor/browser-logs/`)
- **Key Constants:**
  - `SNAPSHOT_SIZE_THRESHOLD`: 25KB
  - `SNAPSHOT_PREVIEW_LINES`: 50 lines
- **Commands:**
  - `cursor.browserOriginAllowlist.ensureNavigationAllowed`
  - `cursor.browserOriginAllowlist.ensurePageOriginAllowed`
  - `cursor.browserView.getURL`

### `cursor-browser-connect`
- **Path:** `extensions/cursor-browser-connect/`
- **Purpose:** Browser connection management

### `cursor-browser-extension`
- **Path:** `extensions/cursor-browser-extension/`
- **Purpose:** Browser extension integration

### `cursor-retrieval`
- **Path:** `extensions/cursor-retrieval/`
- **Purpose:** Code retrieval/indexing

### `cursor-shadow-workspace`
- **Path:** `extensions/cursor-shadow-workspace/`
- **Purpose:** Shadow workspace for background operations

### `cursor-file-service`
- **Path:** `extensions/cursor-file-service/`
- **Purpose:** File service abstraction

### `cursor-deeplink`
- **Path:** `extensions/cursor-deeplink/`
- **Purpose:** Deep link handling

### `cursor-ndjson-ingest`
- **Path:** `extensions/cursor-ndjson-ingest/`
- **Purpose:** NDJSON data ingestion

### `cursor-always-local`
- **Path:** `extensions/cursor-always-local/`
- **Purpose:** Local-only operation enforcement

### `cursor-worktree-textmate`
- **Path:** `extensions/cursor-worktree-textmate/`
- **Purpose:** TextMate grammar for worktrees

---

## Extension Replacement Map

Cursor replaces certain VS Code extensions with Anysphere forks:

| Original (Microsoft) | Cursor Replacement |
|---------------------|-------------------|
| `ms-vscode-remote.remote-ssh` | `anysphere.remote-ssh` |
| `ms-vscode-remote.remote-containers` | `anysphere.remote-containers` |
| `ms-vscode-remote.remote-wsl` | `anysphere.remote-wsl` |
| `ms-python.vscode-pylance` | `anysphere.cursorpyright` |
| `ms-vscode.cpptools` | `anysphere.cpptools` |
| `ms-dotnettools.csharp` | `anysphere.csharp` |

---

## Blocked Extensions

Cannot be imported into Cursor:
- `github.copilot-chat`
- `github.copilot`
- `ms-vscode.remote-explorer`

---

## Extension Version Constraints

| Extension | Min Version | Max Version |
|-----------|-------------|-------------|
| `ms-vscode.cpptools` | 1.20.5 | 1.23.6 |
| `ms-python.vscode-pylance` | 2024.4.1 | 2024.8.1 |
| `ms-vscode-remote.remote-containers` | 0.394.0 | 0.394.0 |
| `ms-vscode-remote.remote-wsl` | 0.81.8 | 0.81.8 |
| `ms-vscode-remote.remote-ssh` | 0.113.1 | 0.113.1 |
| `ms-dotnettools.csharp` | - | 2.63.32 |
| `ms-dotnettools.csdevkit` | - | 1.16.6 |

---

## API Endpoints

| Endpoint | Purpose |
|----------|---------|
| `https://api2.cursor.sh/updates` | Update server |
| `https://api3.cursor.sh/tev1/v1` | Statsig telemetry proxy |
| `https://cursor.blob.core.windows.net/remote-releases/` | Remote server downloads |

---

## Key Dependencies

### Agent Framework
| Package | Purpose |
|---------|---------|
| `@anysphere/agent-exec` | Agent execution framework |
| `@modelcontextprotocol/sdk` | MCP SDK |

### Browser Automation
| Package | Purpose |
|---------|---------|
| `chrome-remote-interface` | Chrome DevTools Protocol |

### Telemetry
| Package | Purpose |
|---------|---------|
| `@sentry/*` | Error tracking |
| `@opentelemetry/*` | Observability |

### UI
| Package | Purpose |
|---------|---------|
| `@xterm/*` | Terminal emulator |
| `@tanstack/*` | React Query/Table |

---

## Enabled API Proposals

Cursor extensions use these non-public VS Code APIs:
- `control` - IDE control surface
- `cursor` - Cursor-specific APIs
- `cursorTracing` - Tracing/debugging

---

## Data Directories

| Path | Purpose |
|------|---------|
| `~/.cursor/` | User configuration |
| `~/.cursor-server/` | Remote server data |
| `~/.cursor/browser-logs/` | Browser automation logs |

---

## What Does NOT Exist

- ❌ **No public source repository** - Cursor is closed-source (unlike VS Code)
- ❌ **No direct API access** - Agent tools work through VS Code command surface
- ❌ **No MCP tool schema in package.json** - Tools defined in compiled code
- ❌ **No documented extension API** - Uses internal VS Code proposals
- ❌ **No standalone agent runtime** - Agents run within VS Code context
- ❌ **No OpenClaw-style sessions_spawn** - Different agent architecture
- ❌ **No hook system** - Extensions use VS Code activation events
- ❌ **No transcript files** - Conversation state managed internally

---

## Comparison with Claude Code SDK

| Feature | Cursor | Claude Code SDK |
|---------|--------|-----------------|
| Architecture | VS Code extension | CLI + SDK |
| Agent spawning | Internal | `sessions_spawn` (OpenClaw) |
| MCP support | Yes (`cursor-mcp`) | Yes (`create_sdk_mcp_server`) |
| Browser automation | Yes (`cursor-browser-automation`) | Via tools |
| Hooks | VS Code events | Hook callbacks |
| Open source | No | SDK is open |

---

## Binary Analysis Notes

### Main Process (`out/main.js`)
- Compiled/minified JavaScript
- Contains Electron main process logic
- Not suitable for direct analysis

### Extension Sources
Extensions in `extensions/cursor-*/src/` contain readable TypeScript source that compiles to `dist/`. These are the best reference for understanding Cursor's AI capabilities.

### Node Modules
- `node_modules.asar` - Electron archive, extract with `asar extract`
- `node_modules/` - Standard npm modules (readable)

---

*This manifest documents Cursor 2.2.44. Binary analysis is limited by compiled code. Extension sources provide the most reliable feature documentation.*
