# Triad Analysis Workflow Pattern

**Purpose:** Comprehensive feature analysis before implementation or refactoring.

## Overview

A three-phase sequential workflow using specialized agents:

```
redundant-project-checker → project-critic → never-say-die (solver)
         ↓                        ↓                    ↓
   spawns seeker            spawns seeker         final output
         ↓                        ↓                    ↓
   redundancy.md    +      critique.md      =    solution.md
```

## Phase 1: Redundancy Check (redundant-project-checker 🔄)

**Input:** Project/codebase path
**Actions:**
1. Inventory existing implementation (file:function:variable)
2. Spawn `seeker` for GitHub/external research
3. Compare our code against mature alternatives
4. Identify: redundant, unique, missing features

**Output:** `analysis/redundancy-{project}-{date}.md`

## Phase 2: Critical Review (project-critic 👹)

**Input:** Redundancy analysis file
**Actions:**
1. Review redundancy findings
2. Spawn `seeker` for validation/additional research
3. Identify risks, assumptions, failure modes
4. Challenge keep/replace/augment decisions

**Output:** `analysis/critique-{project}-{date}.md`

## Phase 3: Solution Engineering (never-say-die 💪)

**Input:** BOTH redundancy and critique files
**Actions:**
1. Synthesize findings from both phases
2. Enumerate ALL features with precision: file → line → function → variable
3. Produce actionable implementation plan
4. Address every concern raised by critic

**Output:** `analysis/solution-{project}-{date}.md`

## Spawning Pattern

```javascript
// Phase 1
sessions_spawn(agentId="redundant-project-checker", task="...")
// Wait for completion announcement

// Phase 2 (after Phase 1 completes)
sessions_spawn(agentId="project-critic", task="Review: {path to redundancy.md}")
// Wait for completion announcement

// Phase 3 (after Phase 2 completes)
sessions_spawn(agentId="never-say-die", task="Solve using: {redundancy.md} AND {critique.md}")
// Wait for completion announcement
```

## When to Use

- Before implementing new features
- Before major refactoring
- When evaluating tech stack choices
- When auditing existing implementations

## Output Location

All analysis files go to: `{agent_workspace}/analysis/`

## Key Principle

**Sequential, not parallel.** Each phase builds on the previous. Never skip phases.
