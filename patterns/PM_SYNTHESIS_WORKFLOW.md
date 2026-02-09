# Project Manager Synthesis Workflow

**Purpose:** Coordinate multi-agent collaboration with final synthesis, respecting OpenClaw's async architecture.

## OpenClaw Constraints (from source manifest)

1. **`sessions_spawn` is NON-BLOCKING** — Returns immediately
2. **Parallel spawns are safe for INDEPENDENT tasks** — If no dependencies, spawn together
3. **Synthesis requires ALL inputs** — PM waits for all specialist reports
4. **Multi-turn orchestration** — Track state across conversation turns

---

## The Pattern

```
┌─────────────────────────────────────────────────────────┐
│                   Parallel Specialists                   │
│                                                         │
│   analyst 📊    ballistics 🎯    cosmo 🌌    seeker 🔍   │
│       ↓              ↓             ↓            ↓       │
│   market.md      domain.md    technical.md  research.md │
│                                                         │
└─────────────────────────────────────────────────────────┘
                          ↓
                    All complete
                          ↓
┌─────────────────────────────────────────────────────────┐
│              project-manager 📋 (Synthesis)              │
│                                                         │
│   Reads: ALL specialist outputs                         │
│   Produces: synthesis/{project}-plan.md                 │
│                                                         │
│   Contents:                                             │
│   - Executive summary                                   │
│   - Unified recommendations                             │
│   - Timeline with milestones                            │
│   - Budget/resource allocation                          │
│   - Risk register + mitigations                         │
│   - Decision matrix                                     │
└─────────────────────────────────────────────────────────┘
```

---

## Multi-Turn Flow

### Turn 1: Spawn Specialists

Specialists are INDEPENDENT — safe to spawn in parallel:

```javascript
// All can run simultaneously
sessions_spawn(agentId: "analyst", task: "Market analysis: {project}")
sessions_spawn(agentId: "ballistics", task: "Domain requirements: {project}")
sessions_spawn(agentId: "cosmo", task: "Technical architecture: {project}")
sessions_spawn(agentId: "seeker", task: "Competitive research: {project}")
```

**Respond:**
> "Dispatched 4 specialists in parallel. Will synthesize with project-manager once all report."

### Turns 2-N: Track Announcements

As each announcement arrives, update tracking:

```markdown
## Active Synthesis: {project}
- analyst: ✅ analysis/market-{project}.md
- ballistics: ✅ analysis/domain-{project}.md
- cosmo: ⏳ pending
- seeker: ✅ analysis/research-{project}.md
- PM synthesis: blocked on cosmo
```

### Turn N+1: All Complete → Spawn PM

When ALL specialists have announced:

```javascript
sessions_spawn(
  agentId: "project-manager",
  task: `Synthesize all specialist reports into actionable plan:

Inputs:
- Market: analysis/market-{project}.md
- Domain: analysis/domain-{project}.md
- Technical: analysis/technical-{project}.md
- Research: analysis/research-{project}.md

Output: synthesis/{project}-plan.md

Include:
1. Executive summary (1 page max)
2. Unified recommendations with priorities
3. Timeline (milestones, dependencies)
4. Budget (hours, dollars, resources)
5. Risk register (risk, probability, impact, mitigation)
6. Go/no-go decision matrix`
)
```

**Respond:**
> "All 4 specialist reports received. Dispatching project-manager for final synthesis."

### Final Turn: Present Synthesis

When PM announces, read `synthesis/{project}-plan.md` and present to user.

---

## Specialist Responsibilities

| Agent | Focus | Output |
|-------|-------|--------|
| analyst 📊 | Market size, competition, positioning | `analysis/market-{project}.md` |
| ballistics 🎯 | Domain requirements, user needs | `analysis/domain-{project}.md` |
| cosmo 🌌 | Technical architecture, stack choices | `analysis/technical-{project}.md` |
| seeker 🔍 | External research, prior art | `analysis/research-{project}.md` |
| project-manager 📋 | Synthesis, economics, timeline | `synthesis/{project}-plan.md` |

---

## PM Output Format

```markdown
# {Project} — Synthesis Report

## Executive Summary
{1-paragraph decision recommendation}

## Recommendations (Prioritized)
1. {Highest impact, lowest effort first}
2. ...

## Timeline
| Milestone | Owner | Target | Dependencies |
|-----------|-------|--------|--------------|
| ... | ... | ... | ... |

## Budget
- Hours: {estimate}
- Dollars: {estimate}
- Key resources: {list}

## Risks
| Risk | P | I | Mitigation |
|------|---|---|------------|
| ... | L/M/H | L/M/H | ... |

## Decision Matrix
| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| ... | ... | ... | ... |
```

---

## When to Use

- Strategic project decisions
- Multi-domain analysis (market + technical + domain)
- Resource allocation decisions
- Go/no-go gates
- Quarterly planning

## When NOT to Use

- Simple single-agent tasks
- Trivial changes
- Time-critical responses

---

## Key Principle

**Specialists go deep. PM goes wide. Synthesis > sum of parts.**
