# Spawn Roster Hook

Injects agent roster when spawning sub-agents, so the spawning agent knows all available specialists.

## Trigger
- Event: `agent:spawn` (before spawn)
- Event: `session:start` (on new session)

## Behavior
Prepends a reminder of all 23 agents and their specializations to help with delegation decisions.
