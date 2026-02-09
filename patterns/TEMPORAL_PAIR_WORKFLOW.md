# Temporal Pair Workflow (Hindsight → Foresight)

**Purpose:** Accumulate organizational wisdom and apply it to new proposals.

## OpenClaw Constraints (from source manifest)

1. **`sessions_spawn` is NON-BLOCKING** — Returns immediately
2. **Hindsight builds archive over time** — Each post-mortem adds to the corpus
3. **Foresight consumes entire archive** — Reads ALL hindsight/*.md
4. **Sequential relationship** — Can't foresight without hindsight corpus

---

## The Pattern

```
                    TIME →

Project A done    Project B done    Project C done
      ↓                ↓                 ↓
  hindsight 🔍     hindsight 🔍      hindsight 🔍
      ↓                ↓                 ↓
  hindsight/       hindsight/        hindsight/
  projectA.md      projectB.md       projectC.md
      ↓                ↓                 ↓
      └────────────────┴─────────────────┘
                       ↓
              ARCHIVE ACCUMULATES
                       ↓
┌──────────────────────────────────────────────┐
│              New Proposal                     │
│                    ↓                          │
│              foresight 🔮                     │
│                    ↓                          │
│         reads ALL hindsight/*.md              │
│                    ↓                          │
│         foresight/{proposal}.md               │
│                                               │
│   "Based on past lessons, here's what to     │
│    watch out for with this proposal..."       │
└──────────────────────────────────────────────┘
```

---

## Hindsight (Post-Completion)

### When to Spawn
- Project shipped/merged/deployed
- Feature explicitly completed
- Sprint/milestone ended
- User says "done" or "complete"

### Spawn Pattern

```javascript
sessions_spawn(
  agentId: "hindsight",
  task: `Post-mortem analysis:

Project: {name}
Path: {project_path}
Duration: {start_date} to {end_date}

Analyze:
1. What worked well?
2. What didn't work?
3. Time estimate vs actual
4. Unexpected blockers
5. Lessons for next time

Output: hindsight/{project}-{date}.md`
)
```

### Output Format

```markdown
# Hindsight: {Project}
**Date:** {date}
**Duration:** {actual} vs {estimated}

## What Worked
- ...

## What Didn't
- ...

## Unexpected Blockers
- ...

## Lessons Learned
1. {Actionable insight}
2. ...

## Time Analysis
- Estimated: X hours
- Actual: Y hours
- Variance: +/-Z%
- Cause of variance: ...

## Recommendations for Similar Projects
- ...
```

---

## Foresight (Pre-Proposal)

### When to Spawn
- Before presenting significant proposal
- Before architecture decisions
- Before resource commitments
- Before timeline promises

### Spawn Pattern

```javascript
sessions_spawn(
  agentId: "foresight",
  task: `Review proposal against hindsight archive:

Proposal: {description}
Estimated effort: {estimate}
Key assumptions: {list}

Read ALL: ~/.openclaw/workspace/hindsight/*.md

For each relevant past lesson, assess:
- Does this proposal repeat a past mistake?
- Are time estimates realistic based on history?
- What blockers should we anticipate?

Output: foresight/{proposal}-{date}.md`
)
```

### Output Format

```markdown
# Foresight: {Proposal}
**Date:** {date}

## Relevant Past Lessons

### From {past_project_1}
- Lesson: {what happened}
- Applies because: {relevance}
- Risk to proposal: {assessment}
- Mitigation: {recommendation}

### From {past_project_2}
- ...

## Time Estimate Assessment
- Proposal estimates: X hours
- Similar past projects averaged: Y hours
- Confidence: {high/medium/low}
- Recommendation: {adjust estimate?}

## Anticipated Blockers
Based on past experience:
1. {likely blocker} — {mitigation}
2. ...

## Green Flags
This proposal avoids these past mistakes:
- ...

## Red Flags
This proposal may repeat these patterns:
- ...

## Overall Assessment
{Proceed / Proceed with caution / Reconsider}
```

---

## Synergy

| Phase | Direction | Value |
|-------|-----------|-------|
| Hindsight | Past → Archive | "What actually happened" |
| Foresight | Archive → Future | "What will likely happen" |

**Compound effect:** More hindsight = better foresight. Organizational learning accumulates.

---

## Directory Structure

```
~/.openclaw/workspace/
├── hindsight/
│   ├── gundom-2026-01-15.md
│   ├── apeswarm-2026-01-20.md
│   ├── computerstore-2026-02-01.md
│   └── ...
└── foresight/
    ├── mhi-procurement-2026-02-05.md
    ├── sop-automation-2026-02-08.md
    └── ...
```

---

## Key Principle

**Past informs future. Archive grows. Foresight improves. Never repeat the same mistake twice.**
