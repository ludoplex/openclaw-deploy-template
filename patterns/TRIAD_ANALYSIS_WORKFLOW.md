# Triad Analysis Workflow Pattern

**Purpose:** Comprehensive analysis before implementation, respecting OpenClaw's async architecture.

## OpenClaw Constraints (from source manifest)

1. **`sessions_spawn` is NON-BLOCKING** — Returns `{status: "accepted"}` immediately
2. **Announcements arrive asynchronously** — As separate messages to the session
3. **No synchronous waiting** — Cannot block for subagent results
4. **Multi-turn orchestration required** — Each spawn/response is a turn

## Triad Sequence (MANDATORY ORDER)

```
redundant-project-checker 🔄 → project-critic 👹 → never-say-die 💪
         ↓                           ↓                    ↓
   redundancy.md              critique.md           solution.md
   (standalone)           (reads redundancy)     (reads both)
```

**Why sequential?** Each phase builds on the previous. Critic needs redundancy findings. Solver needs both to address everything.

---

## Multi-Turn Orchestration Pattern

### Turn 1: Spawn Redundancy Checker
```javascript
sessions_spawn(
  agentId: "redundant-project-checker",
  task: `Analyze: {request}
  
Output to: analysis/redundancy-{project}-{date}.md
Spawn seeker for GitHub/external research.
Document: redundant features, unique features, mature alternatives.`
)
```

**Respond to user:**
> "Phase 1/3: Dispatched redundancy-checker. Will spawn critic once analysis arrives."

### Turn 2: See Announcement → Spawn Critic
When redundancy-checker announcement arrives:

```javascript
sessions_spawn(
  agentId: "project-critic",
  task: `Review redundancy analysis at: {path to redundancy.md}
  
Output to: analysis/critique-{project}-{date}.md
Spawn seeker to validate claims.
Document: risks, assumptions, failure modes, challenges to decisions.`
)
```

**Respond to user:**
> "Phase 2/3: Redundancy analysis complete. Dispatched critic. Will spawn solver once critique arrives."

### Turn 3: See Announcement → Spawn Solver
When critic announcement arrives:

```javascript
sessions_spawn(
  agentId: "never-say-die",
  task: `Synthesize and solve using:
- Redundancy: {path to redundancy.md}
- Critique: {path to critique.md}

Output to: analysis/solution-{project}-{date}.md
Address EVERY concern raised by critic.
Enumerate features: file → line → function → variable.
Produce actionable implementation plan.`
)
```

**Respond to user:**
> "Phase 3/3: Critique complete. Dispatched solver for final synthesis."

### Turn 4: Synthesize
When solver announcement arrives:

**Read all three files and synthesize:**
- Redundancy findings (what exists, what's mature elsewhere)
- Critic's concerns (risks, failure modes)
- Solver's mitigations (how to address each concern)
- Final recommendation with tradeoffs

---

## Session State Tracking

The main agent must track triad state across turns:

```markdown
<!-- In memory/YYYY-MM-DD.md or session context -->
## Active Triad: {project}
- Phase: 2/3 (waiting for critic)
- Redundancy: analysis/redundancy-{project}-{date}.md ✅
- Critique: pending
- Solution: pending
```

---

## Subagent Responsibilities

### redundant-project-checker 🔄
**Input:** Project description or codebase path
**Actions:**
1. Inventory existing implementation (file:function:variable)
2. Spawn `seeker` for external research
3. Compare against mature alternatives
4. Identify: redundant, unique, missing features

**Output:** `analysis/redundancy-{project}-{date}.md`

### project-critic 👹
**Input:** Path to redundancy analysis
**Actions:**
1. Read redundancy findings
2. Spawn `seeker` for validation
3. Challenge each decision
4. Enumerate risks, assumptions, failure modes

**Output:** `analysis/critique-{project}-{date}.md`

### never-say-die 💪
**Input:** Paths to BOTH redundancy and critique files
**Actions:**
1. Read both analyses
2. Address every critic concern
3. Provide mitigations for all risks
4. Produce actionable implementation plan

**Output:** `analysis/solution-{project}-{date}.md`

---

## When to Use

- Before implementing new features
- Before major refactoring
- When evaluating tech stack choices
- When auditing existing implementations
- When investment is significant

## When to Skip

- Simple queries, file reads
- Trivial changes (typos, formatting)
- User explicitly says "just do it"

---

## Anti-Patterns

❌ **Spawning all three in parallel** — Critic can't review what doesn't exist yet
❌ **Skipping phases** — Solver without critic = unaddressed risks
❌ **Waiting synchronously** — `sessions_spawn` doesn't block
❌ **Losing state between turns** — Track phase in memory

---

## Key Principle

**Sequential, async, multi-turn.** Respect OpenClaw's architecture. Each phase depends on the previous. Orchestrate across conversation turns.
