# Hindsight Enforcer Hook

## Trigger
`project:complete` — Fires when any agent marks a project as complete

## Detection Patterns
Hook activates when agent output contains:
- "project complete"
- "implementation complete"
- "task complete"
- "finished implementing"
- "deployed"
- "merged"
- "shipped"
- Commit messages indicating completion

## Action
Spawn `hindsight` agent with context:
- Project directory path
- Session ID that completed the work
- List of agents involved
- Completion timestamp

## Enforcement
**BLOCKING**: The completing agent's session cannot close until hindsight produces its report.

## Output Location
`C:\Users\user\.openclaw\workspace\hindsight\{project-name}-{YYYY-MM-DD}.md`
