# Swiss Rounds Synthesis Workflow

**Purpose:** Multi-agent deliberation with cross-examination, retrospectives, and advisory oversight before PM synthesis.

## Overview

A tournament-style approach where specialists:
1. Produce initial reports (following manifest methodology)
2. Cross-read all other reports and append addendums
3. Read feedback on their own work and produce retrospectives
4. Repeat cross-examination for deeper synthesis
5. Advisory triad validates at each phase
6. PM consumes all artifacts for final synthesis

---

## The Rounds

```
┌─────────────────────────────────────────────────────────────────┐
│                    ROUND 1: INITIAL REPORTS                      │
│                                                                  │
│   specialist_A ───→ report_A.md                                  │
│   specialist_B ───→ report_B.md                                  │
│   specialist_C ───→ report_C.md                                  │
│                                                                  │
│   ⚠️ Must follow SOURCE_MANIFEST.md or BINARY_MANIFEST.md       │
│                                                                  │
│   → TRIAD runs on all reports                                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    ROUND 2: ADDENDUM 1                           │
│                                                                  │
│   Each specialist reads ALL OTHER agents' reports               │
│   Each appends "Addendum 1" to their OWN file (with signature)  │
│                                                                  │
│   specialist_A reads B.md, C.md → appends to report_A.md        │
│   specialist_B reads A.md, C.md → appends to report_B.md        │
│   specialist_C reads A.md, B.md → appends to report_C.md        │
│                                                                  │
│   → TRIAD runs on all addendums                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                 ROUND 3: RETROSPECTIVE PART 1                    │
│                                                                  │
│   Each specialist reads addendums TO THEIR OWN FILE             │
│   (Other agents' perspectives on their work)                     │
│   Each appends "Retrospective Part 1" to their own file         │
│                                                                  │
│   specialist_A reads others' addendums on A.md → appends retro  │
│   specialist_B reads others' addendums on B.md → appends retro  │
│   specialist_C reads others' addendums on C.md → appends retro  │
│                                                                  │
│   → TRIAD runs on all retrospectives                             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    ROUND 4: ADDENDUM 2                           │
│                                                                  │
│   Each specialist reads ALL OTHER agents' Retrospective Part 1  │
│   Each provides feedback via "Addendum 2" on EACH OTHER's file  │
│                                                                  │
│   specialist_A reads B+C retros → adds addendum2 to B.md, C.md  │
│   specialist_B reads A+C retros → adds addendum2 to A.md, C.md  │
│   specialist_C reads A+B retros → adds addendum2 to A.md, B.md  │
│                                                                  │
│   → TRIAD runs on all second addendums                           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│              ROUND 5: FINAL RETROSPECTIVE (PART 2)               │
│                                                                  │
│   Each specialist reads Addendum 2s on THEIR OWN FILE           │
│   Each appends "Final Retrospective Part 2"                      │
│   This completes their deliberation                              │
│                                                                  │
│   → TRIAD runs final sequence on all completed files             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    ROUND 6: PM SYNTHESIS                         │
│                                                                  │
│   project-manager 📋 consumes ALL files:                        │
│   - All specialist reports with all addendums + retrospectives  │
│   - All triad analyses from each round                          │
│                                                                  │
│   Produces: synthesis/{project}-plan.md                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## File Structure Per Specialist

```markdown
# {Specialist} Report: {Project}
**Agent:** {id}
**Date:** {date}

## Initial Report
{Original analysis following manifest methodology}

---

## Addendum 1 (Cross-Reading)
**Signed:** {agent_id}
**Date:** {date}

After reading reports from: {list of other agents}

{Observations, agreements, disagreements, questions}

---

## Retrospective Part 1
**Date:** {date}

After reading other agents' addendums on my report:

{Response to feedback, refinements, clarifications}

---

## Addendum 2 from {other_agent_id}
**Signed:** {other_agent_id}
**Date:** {date}

{Feedback on Retrospective Part 1}

## Addendum 2 from {another_agent_id}
...

---

## Final Retrospective (Part 2)
**Date:** {date}

After reading all Addendum 2s:

{Final position, synthesis of all feedback, conclusions}
```

---

## Advisory Triad Integration

The triad (redundancy-checker → critic → solver) runs **sequentially on each round's outputs**:

| After Round | Triad Input | Purpose |
|-------------|-------------|---------|
| 1 (Initial Reports) | All specialist reports | Validate initial analyses |
| 2 (Addendum 1) | All addendums | Validate cross-reading insights |
| 3 (Retro Part 1) | All retrospectives | Validate self-assessments |
| 4 (Addendum 2) | All second addendums | Validate peer feedback |
| 5 (Final Retro) | All final retrospectives | Final validation before PM |

**Triad sequence per round:**
1. redundancy-checker 🔄 → `triad/round{N}-redundancy.md`
2. project-critic 👹 → `triad/round{N}-critique.md` (reads redundancy)
3. never-say-die 💪 → `triad/round{N}-solution.md` (reads both)

---

## Multi-Turn Orchestration

Given OpenClaw's async-only spawning, this requires **many turns**:

### Phase 1: Initial Reports
```
Turn 1: Spawn all specialists in parallel
Turns 2-N: Wait for all announcements
```

### Phase 2: Addendum 1
```
Turn N+1: Spawn each specialist to read others + append addendum
         (Can be parallel - they write to their OWN files)
Turns N+2...: Wait for announcements
```

### Phase 3: Retrospective Part 1
```
Turn M: Spawn each specialist to read their addendums + write retro
Turns M+1...: Wait for announcements
```

### Between Phases: Run Triad
```
Turn T: Spawn redundancy-checker on all current files
Turn T+1: Announcement → Spawn critic
Turn T+2: Announcement → Spawn solver
Turn T+3: Triad complete
```

### Repeat for Rounds 4, 5...

### Final: PM Synthesis
```
Turn F: Spawn project-manager with ALL files
Turn F+1: PM announces → Present to user
```

---

## Estimated Turn Count

For 4 specialists:
- Initial reports: ~4 turns (spawn + announcements)
- Addendum 1: ~4 turns
- Triad after each round: ~3 turns × 5 rounds = 15 turns
- Retrospective Part 1: ~4 turns
- Addendum 2: ~4 turns (each writes to multiple files)
- Final Retrospective: ~4 turns
- PM Synthesis: ~2 turns

**Total: ~40+ turns** for full deliberation

---

## State Tracking

Main agent must track:

```markdown
## Swiss Rounds: {project}

### Round 1: Initial Reports
- analyst: ✅ analysis/analyst-{project}.md
- ballistics: ✅ analysis/ballistics-{project}.md
- cosmo: ⏳ pending
- seeker: ✅ analysis/seeker-{project}.md
- Triad: pending (blocked on cosmo)

### Round 2: Addendum 1
- All specialists: pending (blocked on Round 1 Triad)

### Round 3-5: ...

### PM Synthesis: pending (blocked on Round 5 Triad)
```

---

## When to Use

- High-stakes strategic decisions
- Multi-domain problems requiring deep synthesis
- Decisions with significant resource commitment
- When consensus-building across perspectives matters

## When NOT to Use

- Time-critical decisions
- Simple single-domain problems
- Low-stakes choices

---

## Key Principle

**Deliberation > Speed. Cross-examination reveals blind spots. Retrospectives refine positions. Triad validates each phase. PM synthesizes the refined whole.**
