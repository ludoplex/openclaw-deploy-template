# Swiss Rounds Orchestration

**Version:** 2.0
**Updated:** 2026-02-09

---

## Overview

Swiss Rounds is a multi-agent deliberation workflow that produces high-quality, validated proposals through iterative cross-reading and feedback. This document defines the orchestration rules for the main agent.

---

## Bootstrap (GENERIC) — All Agents

Every agent (specialists, triad, PM) follows these steps:

```
1. READ all sources listed in state.sources FIRST
   - For type="source": Follow SOURCE_MANIFEST.md exactly
   - For type="binary": Follow BINARY_MANIFEST.md exactly

2. Distinguish each source UNIQUELY (upstream vs fork vs dependency)

3. Create a file containing all information required by .md instructions 
   in step 1 AND append your domain-specific analysis to it afterward

4. Select an agent report to read and read ALL OF IT

5. Provide feedback to selected agent report by appending to it, then 
   if there is another agent report you have not yet read and provided 
   feedback to this phase return to step 4, otherwise proceed to step 6

6. REREAD ALL OF YOUR FILE CREATED IN step 3, NO EXCEPTIONS, then append 
   a new enlightened proposal of your domain-specific work which must be done

7. If you are main agent and all other agents have completed steps 1-6, 
   spawn triad or PM depending on phase appropriateness
```

---

## Phase Appropriateness Rules

| Phase | Condition | Action |
|-------|-----------|--------|
| **Setup** | User requests proposal for described project | Clone all relevant repos |
| **Setup** | Repos cloned AND verified with user | **Spawn specialists** (Round 1) |
| **Rounds** | Specialists pending | Wait |
| **Rounds** | Specialists complete, triad pending | **Spawn triad** |
| **Rounds** | Triad complete, `currentRound < totalRounds` | Advance round, **spawn specialists** |
| **PM** | `currentRound == totalRounds` AND triad complete | **Spawn PM** |
| **Complete** | `pmComplete` | Deliver to user |

**Rhythm:** `specialists → triad → specialists → triad → ... → PM → done`

---

## PM Bootstrap

PM follows the same source-truth-first pattern:

```
1. READ all sources following SOURCE_MANIFEST.md / BINARY_MANIFEST.md

2. CREATE overarching plan file containing all information required by 
   .md instructions in step 1 (features/files/linenumbers/functions/variables)

3. CONSUME all specialist domain reports completely

4. APPEND overarching plan to the file created in step 2:
   - Execution phases and dependencies
   - Critical path
   - Success criteria

5. DECIDE specialist assignment sequence, APPEND to file:
   - Ordered list with justification
   - Write to state: pm.sequence = [...]

6. FOR EACH specialist in pm.sequence:
   a. REREAD that specialist's final report completely
   b. CREATE individual plan: {project}/synthesis/{specialist}-plan.md
   c. CREATE stage prompts: {project}/synthesis/{specialist}-prompts.md
   d. UPDATE state: pm.specialistPlans[specialist].complete = true

7. VERIFY all specialists assigned → pm.complete = true

8. SIGNAL completion to main agent
```

---

## State Schema

```json
{
  "project": "example-project",
  "mode": "new|revision",
  "phase": "setup|rounds|pm|complete",
  "sources": [
    { 
      "name": "upstream", 
      "repo": "org/upstream", 
      "path": "/path/to/upstream", 
      "type": "source", 
      "verified": true 
    },
    { 
      "name": "fork", 
      "repo": "user/fork", 
      "path": "/path/to/fork", 
      "type": "source", 
      "verified": true 
    },
    { 
      "name": "binary-dep", 
      "path": "/path/to/binary", 
      "type": "binary", 
      "verified": true 
    }
  ],
  "userVerified": true,
  "specialists": ["seeker", "localsearch", "asm", "cosmo", "dbeng", "neteng", "cicd", "testcov"],
  "currentRound": 2,
  "totalRounds": 5,
  "rounds": {
    "1": { "specialistsComplete": true, "triadComplete": true, "completed": [...], "pending": [] },
    "2": { "specialistsComplete": false, "triadComplete": false, "completed": ["seeker"], "pending": ["localsearch", "asm", ...] }
  },
  "pm": {
    "started": false,
    "overarchingPlanComplete": false,
    "sequence": [],
    "specialistPlans": {},
    "complete": false
  },
  "revision": {
    "priorPlanPath": null,
    "scope": null,
    "triggeredBy": null
  },
  "startedAt": "2026-02-09T20:00:00Z"
}
```

---

## Directory Structure

```
~/.openclaw/workspace/swiss-rounds/{project}/
├── state.json
├── reports/
│   ├── seeker-{project}.md
│   ├── localsearch-{project}.md
│   ├── asm-{project}.md
│   └── ... (one per specialist)
├── triad/
│   ├── round1-redundancy.md
│   ├── round1-critique.md
│   ├── round1-solution.md
│   ├── round2-redundancy.md
│   └── ... (three per round)
└── synthesis/
    ├── overarching-plan.md      ← PM creates (with source manifest first)
    ├── seeker-plan.md           ← Individual plans
    ├── seeker-prompts.md        ← Stage prompts
    └── ... (two files per specialist)
```

---

## Revision Mode

Revision is NOT a shortcut. It's a **full Swiss Rounds run** focused on the revision scope.

### Revision Flow

| Step | Action |
|------|--------|
| **1. Trigger** | User or agents identify revision needed |
| **2. Scope** | Define what's being revised and why |
| **3. Approval** | User approves revision scope |
| **4. Process** | Full Swiss Rounds (specialists → triad × 5 rounds → PM) |
| **5. Apply** | Only after PM completes, revision applied to original plan |

### Phase Appropriateness (Revision)

| Phase | Condition | Action |
|-------|-----------|--------|
| **Revision Setup** | Revision need identified | Document scope, get user approval |
| **Revision Setup** | User approves scope | Set `mode: "revision"`, load prior plans, **spawn specialists** |
| **Rounds** | (Same as new mode) | specialists → triad → repeat × 5 rounds |
| **PM** | All rounds complete | PM produces updated plans referencing prior + revision |
| **Apply** | `pmComplete` | Apply revision, archive prior version, deliver to user |

### What Specialists Receive (Revision Mode)

1. Prior PM overarching plan (context)
2. Prior individual plans (context)  
3. Revision scope (what's changing and why)
4. Same source repos (re-read per manifest methodology)

All specialists follow **Bootstrap (GENERIC)** — no shortcuts.

### What PM Produces (Revision Mode)

1. Updated overarching plan (referencing both prior + revision justification)
2. Updated individual plans for affected specialists
3. Updated stage prompts
4. **Changelog** (what changed from prior plan and why)

PM follows **PM Bootstrap** — source manifest first, then synthesis.

---

## Hook Enforcement

The `swiss-rounds-enforcer` hook automatically injects:

1. **On `command:new`:** Phase appropriateness context for main agent
2. **On `agent:bootstrap` for specialists:** Generic Bootstrap with source manifest methodology
3. **On `agent:bootstrap` for triad:** Triad Bootstrap (source-first, then validate reports)
4. **On `agent:bootstrap` for PM:** PM Bootstrap (source manifest → overarching plan → individual plans)

---

## Management Script

```powershell
# Check status
.\scripts\swiss-rounds.ps1 -Action status

# Start new project
.\scripts\swiss-rounds.ps1 -Action start -Project "my-project" -Specialists "seeker,asm,cosmo"

# Validate current round
.\scripts\swiss-rounds.ps1 -Action validate -Project "my-project"

# Advance to next phase
.\scripts\swiss-rounds.ps1 -Action advance -Project "my-project"

# Abort project
.\scripts\swiss-rounds.ps1 -Action abort -Project "my-project"
```

---

## Anti-Patterns

❌ **Skipping source reading** — All agents MUST read sources first
❌ **Conceptual analysis** — All claims must be verified against source
❌ **Inflated scores** — Triad must challenge, not rubber-stamp
❌ **PM without source truth** — PM file starts with manifest, not strategy
❌ **Spawning without verification** — Main agent must confirm repos with user first

---

## Success Criteria

A Swiss Rounds run is successful when:

1. All sources verified by user before specialists spawn
2. Each specialist produces manifest-based analysis (file:line:function)
3. Each round includes genuine cross-reading and feedback
4. Triad provides individual feedback per specialist
5. PM produces overarching plan rooted in source manifest
6. Each specialist receives individual plan + self-contained stage prompts
7. All artifacts exist and reference actual source locations
