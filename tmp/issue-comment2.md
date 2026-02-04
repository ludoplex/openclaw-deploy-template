**Update:** Creating a `handler.js` still causes the same error.

The hook registers successfully ("Registered hook: workflow-enforcer -> agent:bootstrap") but subagent spawns still fail with the `.trim()` error.

The handler pushes an object to `event.context.bootstrapFiles`:
```js
event.context.bootstrapFiles.push({
  path: "WORKFLOW_REMINDER.md",
  content: WORKFLOW_REMINDER,
  source: "hook:workflow-enforcer",
});
```

Something downstream expects a different object shape or the array modification causes issues.

**Workaround:** Disabling the hook allows subagent spawns to work.

This appears to be a bug in how OpenClaw processes hook-injected bootstrap files, not just user error.
