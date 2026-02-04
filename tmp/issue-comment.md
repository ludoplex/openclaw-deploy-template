**Root cause identified:**

The failure was caused by a user-defined internal hook (`workflow-enforcer`) that had a `handler.ts` file but no compiled `handler.js`.

When OpenClaw attempted to load the hook, something in the load path returned undefined, leading to the `.trim()` error during subagent initialization.

**Fix:** Disabling the hook in config resolved the issue:
```json
"hooks": {
  "internal": {
    "entries": {
      "workflow-enforcer": { "enabled": false }
    }
  }
}
```

**Suggestion:** OpenClaw should either:
1. Gracefully skip hooks with only `.ts` files (no compiled `.js`)
2. Provide a clearer error message indicating which hook failed to load

This is user error (uncompiled TypeScript), but the error message gave no indication the hook was the problem.
