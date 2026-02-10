# Claude Code Source Manifest

Generated: 2026-02-08
Source: https://github.com/anthropics/claude-agent-sdk-python @ main
SHA256: (commit hash changes frequently - verify with `gh api repos/anthropics/claude-agent-sdk-python/commits/main --jq '.sha'`)

**Note:** The Claude Code CLI binary itself is closed-source. This manifest covers the **public Python Agent SDK** which is the interface for programmatic interaction.

---

## Core API

### `query()` - One-shot Query Function
- **File:** `src/claude_agent_sdk/query.py`
- **Line:** 12-110
- **Signature:** `async def query(*, prompt: str | AsyncIterable[dict[str, Any]], options: ClaudeAgentOptions | None = None, transport: Transport | None = None) -> AsyncIterator[Message]`
- **Purpose:** Fire-and-forget queries, batch processing, stateless operations

### `ClaudeSDKClient` - Interactive Client Class
- **File:** `src/claude_agent_sdk/client.py`
- **Line:** 19-350+
- **Signature:** Class with async context manager
- **Purpose:** Bidirectional conversations, streaming, interrupts, session management

#### `ClaudeSDKClient.connect()`
- **Line:** 70-150
- **Signature:** `async def connect(self, prompt: str | AsyncIterable[dict[str, Any]] | None = None) -> None`
- **Purpose:** Establish connection to Claude Code CLI

#### `ClaudeSDKClient.query()`
- **Line:** 175-195
- **Signature:** `async def query(self, prompt: str | AsyncIterable[dict[str, Any]], session_id: str = "default") -> None`
- **Purpose:** Send new request in streaming mode

#### `ClaudeSDKClient.receive_messages()`
- **Line:** 155-165
- **Signature:** `async def receive_messages(self) -> AsyncIterator[Message]`
- **Purpose:** Receive all messages from Claude

#### `ClaudeSDKClient.receive_response()`
- **Line:** 290-330
- **Signature:** `async def receive_response(self) -> AsyncIterator[Message]`
- **Purpose:** Receive until ResultMessage (convenience wrapper)

#### `ClaudeSDKClient.interrupt()`
- **Line:** 197-202
- **Signature:** `async def interrupt(self) -> None`
- **Purpose:** Send interrupt signal (streaming mode only)

#### `ClaudeSDKClient.set_permission_mode()`
- **Line:** 204-225
- **Signature:** `async def set_permission_mode(self, mode: str) -> None`
- **Purpose:** Change permission mode during conversation

#### `ClaudeSDKClient.set_model()`
- **Line:** 227-248
- **Signature:** `async def set_model(self, model: str | None = None) -> None`
- **Purpose:** Change AI model during conversation

#### `ClaudeSDKClient.rewind_files()`
- **Line:** 250-280
- **Signature:** `async def rewind_files(self, user_message_id: str) -> None`
- **Purpose:** Rewind tracked files to state at specific user message
- **Requires:** `enable_file_checkpointing=True`

#### `ClaudeSDKClient.get_mcp_status()`
- **Line:** 282-305
- **Signature:** `async def get_mcp_status(self) -> dict[str, Any]`
- **Purpose:** Get MCP server connection status

#### `ClaudeSDKClient.get_server_info()`
- **Line:** 307-330
- **Signature:** `async def get_server_info(self) -> dict[str, Any] | None`
- **Purpose:** Get server initialization info (commands, output styles)

---

## MCP Server Support

### `create_sdk_mcp_server()`
- **File:** `src/claude_agent_sdk/__init__.py`
- **Line:** 110-220
- **Signature:** `def create_sdk_mcp_server(name: str, version: str = "1.0.0", tools: list[SdkMcpTool[Any]] | None = None) -> McpSdkServerConfig`
- **Purpose:** Create in-process MCP server (no IPC overhead)

### `@tool` Decorator
- **File:** `src/claude_agent_sdk/__init__.py`
- **Line:** 55-105
- **Signature:** `def tool(name: str, description: str, input_schema: type | dict[str, Any], annotations: ToolAnnotations | None = None) -> Callable[...]`
- **Purpose:** Define MCP tools with type safety

---

## Configuration Types

### `ClaudeAgentOptions`
- **File:** `src/claude_agent_sdk/types.py`
- **Line:** 540-610
- **Fields:**
  - `tools: list[str] | ToolsPreset | None`
  - `allowed_tools: list[str]`
  - `system_prompt: str | SystemPromptPreset | None`
  - `mcp_servers: dict[str, McpServerConfig] | str | Path`
  - `permission_mode: PermissionMode | None` (default, acceptEdits, plan, bypassPermissions)
  - `continue_conversation: bool`
  - `resume: str | None`
  - `max_turns: int | None`
  - `max_budget_usd: float | None`
  - `disallowed_tools: list[str]`
  - `model: str | None`
  - `fallback_model: str | None`
  - `betas: list[SdkBeta]`
  - `cwd: str | Path | None`
  - `cli_path: str | Path | None`
  - `settings: str | None`
  - `add_dirs: list[str | Path]`
  - `env: dict[str, str]`
  - `extra_args: dict[str, str | None]`
  - `can_use_tool: CanUseTool | None`
  - `hooks: dict[HookEvent, list[HookMatcher]] | None`
  - `include_partial_messages: bool`
  - `fork_session: bool`
  - `agents: dict[str, AgentDefinition] | None`
  - `setting_sources: list[SettingSource] | None`
  - `sandbox: SandboxSettings | None`
  - `plugins: list[SdkPluginConfig]`
  - `max_thinking_tokens: int | None`
  - `output_format: dict[str, Any] | None`
  - `enable_file_checkpointing: bool`

### `PermissionMode`
- **File:** `src/claude_agent_sdk/types.py`
- **Line:** 18
- **Type:** `Literal["default", "acceptEdits", "plan", "bypassPermissions"]`

### `SdkBeta`
- **File:** `src/claude_agent_sdk/types.py`
- **Line:** 21
- **Type:** `Literal["context-1m-2025-08-07"]`

---

## Hook System

### Hook Events (HookEvent)
- **File:** `src/claude_agent_sdk/types.py`
- **Line:** 130-145
- **Values:**
  - `PreToolUse` - Before tool execution
  - `PostToolUse` - After successful tool execution
  - `PostToolUseFailure` - After failed tool execution
  - `UserPromptSubmit` - When user submits prompt
  - `Stop` - Agent stopping
  - `SubagentStop` - Subagent stopping
  - `PreCompact` - Before context compaction
  - `Notification` - Notification events
  - `SubagentStart` - Subagent starting
  - `PermissionRequest` - Permission request events

### Hook Input Types
- **File:** `src/claude_agent_sdk/types.py`
- **Lines:** 147-220
- **Types:**
  - `PreToolUseHookInput` - L157-165
  - `PostToolUseHookInput` - L168-178
  - `PostToolUseFailureHookInput` - L181-192
  - `UserPromptSubmitHookInput` - L195-201
  - `StopHookInput` - L204-210
  - `SubagentStopHookInput` - L213-222
  - `PreCompactHookInput` - L225-232
  - `NotificationHookInput` - L235-243
  - `SubagentStartHookInput` - L246-253
  - `PermissionRequestHookInput` - L256-264

### Hook Output Types
- **File:** `src/claude_agent_sdk/types.py`
- **Lines:** 268-350
- **Key Fields:**
  - `continue_`: Whether to proceed (converted to "continue" for CLI)
  - `async_`: Defer execution (converted to "async" for CLI)
  - `decision`: "block" to block action
  - `permissionDecision`: "allow", "deny", "ask"
  - `updatedInput`: Modified tool input
  - `additionalContext`: Extra context for Claude

### `HookMatcher`
- **File:** `src/claude_agent_sdk/types.py`
- **Line:** 355-365
- **Fields:**
  - `matcher: str | None` - Tool name pattern (e.g., "Bash", "Write|MultiEdit|Edit")
  - `hooks: list[HookCallback]` - Python hook functions
  - `timeout: float | None` - Timeout in seconds (default: 60)

---

## Message Types

### `Message` Union Type
- **File:** `src/claude_agent_sdk/types.py`
- **Line:** 525
- **Type:** `UserMessage | AssistantMessage | SystemMessage | ResultMessage | StreamEvent`

### `UserMessage`
- **Line:** 490-497
- **Fields:** `content`, `uuid`, `parent_tool_use_id`, `tool_use_result`

### `AssistantMessage`
- **Line:** 500-508
- **Fields:** `content: list[ContentBlock]`, `model`, `parent_tool_use_id`, `error`

### `ResultMessage`
- **Line:** 517-525
- **Fields:** `subtype`, `duration_ms`, `duration_api_ms`, `is_error`, `num_turns`, `session_id`, `total_cost_usd`, `usage`, `result`, `structured_output`

### Content Block Types
- **Line:** 465-485
- `TextBlock` - `text: str`
- `ThinkingBlock` - `thinking: str`, `signature: str`
- `ToolUseBlock` - `id`, `name`, `input`
- `ToolResultBlock` - `tool_use_id`, `content`, `is_error`

---

## Agent Definition

### `AgentDefinition`
- **File:** `src/claude_agent_sdk/types.py`
- **Line:** 36-42
- **Fields:**
  - `description: str`
  - `prompt: str`
  - `tools: list[str] | None`
  - `model: Literal["sonnet", "opus", "haiku", "inherit"] | None`

---

## Sandbox Configuration

### `SandboxSettings`
- **File:** `src/claude_agent_sdk/types.py`
- **Line:** 430-460
- **Fields:**
  - `enabled: bool`
  - `autoAllowBashIfSandboxed: bool`
  - `excludedCommands: list[str]`
  - `allowUnsandboxedCommands: bool`
  - `network: SandboxNetworkConfig`
  - `ignoreViolations: SandboxIgnoreViolations`
  - `enableWeakerNestedSandbox: bool`

### `SandboxNetworkConfig`
- **Line:** 400-415
- **Fields:** `allowUnixSockets`, `allowAllUnixSockets`, `allowLocalBinding`, `httpProxyPort`, `socksProxyPort`

---

## Permission System

### `PermissionResult`
- **File:** `src/claude_agent_sdk/types.py`
- **Line:** 75-90
- **Type:** `PermissionResultAllow | PermissionResultDeny`

### `PermissionUpdate`
- **Line:** 55-72
- **Types:**
  - `addRules` / `replaceRules` / `removeRules`
  - `setMode`
  - `addDirectories` / `removeDirectories`

### `CanUseTool` Callback
- **Line:** 95-100
- **Signature:** `Callable[[str, dict[str, Any], ToolPermissionContext], Awaitable[PermissionResult]]`

---

## Errors

### Error Classes
- **File:** `src/claude_agent_sdk/_errors.py`
- **Exports:**
  - `ClaudeSDKError` - Base SDK error
  - `CLIConnectionError` - Connection failure
  - `CLINotFoundError` - CLI binary not found
  - `CLIJSONDecodeError` - Invalid JSON from CLI
  - `ProcessError` - Process execution error

---

## MCP Server Types

### `McpServerConfig`
- **File:** `src/claude_agent_sdk/types.py`
- **Line:** 380-400
- **Type:** `McpStdioServerConfig | McpSSEServerConfig | McpHttpServerConfig | McpSdkServerConfig`

### Server Config Variants
- `McpStdioServerConfig` - `command`, `args`, `env`
- `McpSSEServerConfig` - `url`, `headers`
- `McpHttpServerConfig` - `url`, `headers`
- `McpSdkServerConfig` - `name`, `instance` (in-process)

---

## What Does NOT Exist

- ❌ **No synchronous API** - All operations are async
- ❌ **No `spawn_agent()` function** - Subagent spawning is not exposed in SDK (CLI internal)
- ❌ **No direct tool calling** - Tools are called by Claude, not user code
- ❌ **No transcript reading API** - Transcripts are file-based, no API
- ❌ **No cross-context ClaudeSDKClient** - Cannot use across different async runtime contexts (trio nurseries, asyncio task groups)
- ❌ **No blocking `wait_for_subagent()`** - Subagent announcements are async only
- ❌ **No `sessions_spawn()` in SDK** - This is OpenClaw-specific, not Claude Code SDK
- ❌ **No hook mutation of bootstrapFiles** - Hooks can only mutate hook output, not spawn triggers
- ❌ **No `output_style` setting in SDK** - Output styles are CLI configuration, not SDK
- ❌ **No direct Anthropic API calls** - SDK wraps CLI, which handles API

---

## CLI Binary Features (Closed Source)

The following features exist in the CLI but are not directly exposed in the SDK:

| Feature | CLI | SDK |
|---------|-----|-----|
| Tool execution | ✅ | Via prompts only |
| File operations | ✅ | Via prompts only |
| Subagent spawn | ✅ | ❌ Not exposed |
| Transcript management | ✅ | ❌ File-based only |
| Permission prompts | ✅ | Via callbacks |
| Model switching | ✅ | `set_model()` |
| Session resume | ✅ | `resume` option |

---

## SDK Control Protocol (Internal)

These are internal protocol types for CLI communication:

- **File:** `src/claude_agent_sdk/types.py`
- **Lines:** 610-680
- **Types:**
  - `SDKControlInterruptRequest`
  - `SDKControlPermissionRequest`
  - `SDKControlInitializeRequest`
  - `SDKControlSetPermissionModeRequest`
  - `SDKHookCallbackRequest`
  - `SDKControlMcpMessageRequest`
  - `SDKControlRewindFilesRequest`

---

*This manifest is ground truth for Claude Agent SDK Python capabilities. Verify before calling any API.*
