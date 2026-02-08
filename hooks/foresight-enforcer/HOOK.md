# Foresight Enforcer Hook

## Trigger
`proposal:prepare` — Fires when any agent is preparing a proposal

## Detection Patterns
Hook activates when agent output contains:
- "I propose"
- "my recommendation is"
- "the plan is"
- "here's the approach"
- "implementation plan"
- "architecture proposal"
- "technical design"
- "I suggest we"

## Action
Spawn `foresight` agent with context:
- Full session history leading to proposal
- Proposed approach/plan text
- Proposing agent ID

## Pre-Requisite
Foresight MUST read all files in:
`C:\Users\user\.openclaw\workspace\hindsight\*.md`

## Enforcement
**BLOCKING**: Proposal cannot be presented to user until foresight produces its review.

## Output Location
`C:\Users\user\.openclaw\workspace\foresight\{proposal-name}-{YYYY-MM-DD}.md`

## Override
User can say "skip foresight" to bypass for trivial proposals.
