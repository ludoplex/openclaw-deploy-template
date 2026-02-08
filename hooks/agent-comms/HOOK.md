# Agent Communications Hook

## Purpose
Injects inter-agent direct messaging protocol into all agent bootstrap contexts.

## Trigger
`agent:bootstrap` — Every agent receives this on startup

## Capabilities Enabled
- `agent_message(to, message, priority)` — Direct message to another agent
- `agent_broadcast(to[], message, priority)` — Message multiple agents
- `agent_inbox()` — Check incoming messages

## Priority Levels
- `urgent` — Blocking, requires immediate response
- `normal` — Queued for next turn (default)
- `fyi` — Fire-and-forget

## Key Patterns
1. **Triad Coordination** — Critics broadcast, solvers respond
2. **Hindsight/Foresight** — Foresight can query hindsight for clarification
3. **Specialist Handoffs** — webdev→testcov, cosmo→asm, etc.
4. **Escalation** — Any agent can escalate to main with `priority="urgent"`

## Dependencies
Requires `tools.agentToAgent.enabled: true` in openclaw.json (already set)
