# Recursive Reasoning LLM Environment

## Core Pattern

```
PLAN → IMPLEMENT → VERIFY → REFLECT → REPEAT (max N iterations)
```

This creates a self-improving loop where each iteration builds on the last.

## Implementation via Hooks + Skills

### The Reasoning Loop

```
┌─────────────────────────────────────────────────────────────┐
│                    RECURSIVE REASONING                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────┐     ┌───────────┐     ┌────────┐             │
│   │  PLAN   │ ──▶ │ IMPLEMENT │ ──▶ │ VERIFY │             │
│   └─────────┘     └───────────┘     └────────┘             │
│        ▲                                  │                 │
│        │          ┌───────────┐           │                 │
│        └───────── │  REFLECT  │ ◀─────────┘                 │
│                   └───────────┘                             │
│                        │                                    │
│                   [continue?]                               │
│                    /       \                                │
│                  yes        no                              │
│                   │          │                              │
│              [iterate]   [output]                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Hook Integration Points

| Phase | Hook Event | Purpose |
|-------|------------|---------|
| PLAN | `agent:bootstrap` | Inject reasoning framework |
| IMPLEMENT | — | Agent execution |
| VERIFY | `command:new` | Log verification results |
| REFLECT | `command:new` | Capture learnings to memory |

### Skill Support

**Reasoning Framework Skill** (inject via bootstrap):
```yaml
---
name: reason
description: Recursive reasoning. Use for complex multi-step problems.
---

## Framework
1. PLAN: State goal, decompose into steps
2. IMPLEMENT: Execute current step
3. VERIFY: Check if step succeeded
4. REFLECT: What worked? What didn't? Update approach.
5. REPEAT: If goal not met and iterations < 5, goto PLAN

## Constraints
- Max 5 iterations per problem
- Each iteration must produce observable progress
- If stuck 2 iterations, change approach fundamentally
```

## Environment Configuration

### Agent Config Pattern
```json
{
  "agents": {
    "list": [
      {
        "id": "agent-name",
        "workspace": "...",
        "reasoning": {
          "maxIterations": 5,
          "framework": "recursive",
          "verifyAfterEachStep": true
        }
      }
    ]
  }
}
```

### Hook: reasoning-tracker
```typescript
// Track reasoning iterations
const handler: HookHandler = async (event) => {
  if (event.type !== "agent" || event.action !== "bootstrap") return;
  
  // Inject iteration counter into bootstrap
  event.context.bootstrapFiles?.push({
    path: "REASONING_STATE.md",
    content: `# Reasoning State\nIteration: 0\nMax: 5\nApproach: initial`
  });
};
```

### Hook: reflection-capture
```typescript
// Capture reflections to memory
const handler: HookHandler = async (event) => {
  if (event.type !== "command" || event.action !== "new") return;
  
  // Before reset, extract REFLECT phase learnings
  const learnings = extractReflections(event.context.sessionEntry);
  await appendToMemory(event.context.workspaceDir, learnings);
};
```

## Recursive Decomposition (Feynman-Style)

### Skill: decompose
```yaml
---
name: decompose  
description: Break complex problems into first principles. Use when stuck.
---

## Method
1. State the problem in one sentence
2. What are the fundamental components?
3. For each component: Can I explain it simply?
   - Yes → Move on
   - No → Recurse: decompose that component
4. Rebuild understanding from components
5. Identify which decomposed element is blocking

## Output Format
```
PROBLEM: [original]
DECOMPOSITION:
  - Component A: [explanation]
    - Sub-component A1: [explanation]
  - Component B: [explanation]
BLOCKER: [which component needs more work]
NEXT: [specific action to resolve blocker]
```
```

## Cross-Domain Reframing

### Skill: reframe
```yaml
---
name: reframe
description: Apply concepts from other domains. Use when standard approaches fail.
---

## Method
1. Identify stuck domain (e.g., "software architecture")
2. Find analogous domain (e.g., "urban planning", "biology", "economics")
3. Map concepts:
   - What's the equivalent of X in domain Y?
   - What solutions exist there?
4. Translate back to original domain
5. Test if reframed approach unlocks progress

## Common Mappings
| From | To | Insight |
|------|-----|---------|
| Software | Biology | Evolution, immune systems, ecosystems |
| Software | Economics | Markets, incentives, scarcity |
| Software | Architecture | Load-bearing, modularity, zoning |
| Research | Detective work | Evidence, witnesses, alibis |
```

## Bayesian Confidence Tracking

### Skill: confidence
```yaml
---
name: confidence
description: Track belief updates. Use for uncertain conclusions.
---

## Method
1. State prior belief: P(H) = X%
2. New evidence: E
3. Update: P(H|E) = ?
4. State posterior with reasoning

## Output Format
```
HYPOTHESIS: [claim]
PRIOR: [X]% because [reasoning]
EVIDENCE: [what was found]
LIKELIHOOD: P(E|H) = [Y]%, P(E|¬H) = [Z]%
POSTERIOR: [W]% because [calculation/reasoning]
CONFIDENCE: HIGH|MEDIUM|LOW
```
```

## Environment Setup Checklist

- [ ] Add `reason` skill to workspace
- [ ] Add `decompose` skill to workspace  
- [ ] Add `reframe` skill to workspace
- [ ] Add `confidence` skill to workspace
- [ ] Enable `session-memory` hook (capture learnings)
- [ ] Create `reasoning-tracker` hook (iteration management)
- [ ] Set max iterations in agent config
- [ ] Create `REASONING.md` workspace file with framework

## Integration with Agent Fleet

All agents should have access to reasoning skills. Agent-specific adaptations:

| Agent | Reasoning Focus |
|-------|-----------------|
| seeker🔍 | Bayesian + decomposition heavy |
| webdev🌐 | Implementation verification loops |
| testcov🧪 | Hypothesis testing pattern |
| cicd🔄 | Pipeline debugging iterations |
| cosmo🌌 | First principles decomposition |
