# Hook Events Reference

## Command Events

| Event | When | Use For |
|-------|------|---------|
| `command` | Any command | Audit logging |
| `command:new` | `/new` issued | Session memory save |
| `command:reset` | `/reset` issued | State cleanup |
| `command:stop` | `/stop` issued | Graceful shutdown tasks |

## Agent Events

| Event | When | Use For |
|-------|------|---------|
| `agent:bootstrap` | Before workspace files injected | SOUL swapping, file injection |

**Note:** `context.bootstrapFiles` can be mutated in bootstrap hooks.

## Gateway Events

| Event | When | Use For |
|-------|------|---------|
| `gateway:startup` | After channels start, hooks loaded | Boot tasks, health checks |

## Event Object Shape

```typescript
{
  type: 'command' | 'session' | 'agent' | 'gateway',
  action: string,           // 'new', 'reset', 'stop', etc.
  sessionKey: string,
  timestamp: Date,
  messages: string[],       // Push to send user messages
  context: {
    sessionEntry?: SessionEntry,
    sessionId?: string,
    commandSource?: string, // 'whatsapp', 'telegram', etc.
    senderId?: string,
    workspaceDir?: string,
    bootstrapFiles?: WorkspaceBootstrapFile[],
    cfg?: OpenClawConfig
  }
}
```

## Handler Pattern

```typescript
const handler: HookHandler = async (event) => {
  // 1. Filter early
  if (event.type !== "command" || event.action !== "new") return;
  
  // 2. Do minimal work
  const result = await quickOperation();
  
  // 3. Fire-and-forget slow work
  void slowBackgroundTask(event);
  
  // 4. Optionally notify user
  event.messages.push("✓ Done");
};
```
