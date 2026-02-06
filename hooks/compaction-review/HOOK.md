# Compaction Review Hook

## Purpose
Captures the last N conversation turns before compaction occurs, allowing the agent to review the original context against the compaction summary to catch mis-summarizations.

## Events
- `agent:before-compaction` - Fires before context compaction begins
- `agent:after-compaction` - Fires after compaction with the summary

## Behavior
1. On `before-compaction`: Saves the last 20 turns to a temporary file
2. On `after-compaction`: Injects the saved turns + summary into context for agent review
3. Agent is prompted to verify the summary accurately captures key details

## Files
- `handler.js` - Hook implementation
