# Advisory Triad Hook

Automatically spawns the three advisory agents whenever main receives a user message, ensuring every response benefits from comprehensive analysis.

## Trigger
- Event: `user:message` (when user sends message to main agent)

## The Triad
1. **redundant-project-checker** 🔄 — Checks if mature alternatives exist
2. **project-critic** 👹 — Identifies all failure modes and risks
3. **never-say-die** 💪 — Provides solutions to all identified problems

## Behavior
When main receives a user message:
1. Spawn all three advisory agents in parallel
2. Each agent analyzes the user's message and main's potential approach
3. Advisory agents exchange reasoning with main
4. Main synthesizes their input before responding to user

## Purpose
- Prevent reinventing the wheel (redundant-project-checker)
- Surface hidden risks before they become problems (project-critic)
- Ensure no blocker goes unaddressed (never-say-die)

## Configuration
Agents: `redundant-project-checker`, `project-critic`, `never-say-die`
Mode: Parallel spawn, synchronous exchange before main responds
