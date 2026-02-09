# Swiss Rounds Orchestration Guide

**For: Main Agent (Peridot)**

This guide documents how to orchestrate Swiss Rounds given OpenClaw's async-only `sessions_spawn`.

---

## Starting a Project

```powershell
.\scripts\swiss-rounds.ps1 -Action start -Project {name} -Specialists "analyst,ballistics,cosmo,seeker"
```

This creates:
- `swiss-rounds/{project}/state.json` — Workflow state
- `swiss-rounds/{project}/reports/` — Specialist reports
- `swiss-rounds/{project}/triad/` — Triad validation outputs
- `swiss-rounds/{project}/synthesis/` — PM outputs

---

## Round 1: Initial Reports

### Turn 1 — Spawn All Specialists (Parallel OK)

```
sessions_spawn(agentId="analyst", task=`
Swiss Rounds Round 1 — Initial Report for: {project}

Read your SWISS_ROUND_INSTRUCTIONS.md (injected by hook).
Produce: ~/.openclaw/workspace/swiss-rounds/{project}/reports/analyst-{project}.md

Follow MANIFEST_METHODOLOGY. Be thorough.
`)
```

Repeat for each specialist. They can run in parallel since Round 1 reports are independent.

### Turns 2-N — Wait for Announcements

Track completions. When ALL specialists announce, proceed to triad.

### Triad Sequence (MUST BE SEQUENTIAL)

```
# Wait for all Round 1 reports

sessions_spawn(agentId="redundant-project-checker", task=`
Swiss Rounds Triad — Round 1 Validation

Read all reports in: ~/.openclaw/workspace/swiss-rounds/{project}/reports/
Output: ~/.openclaw/workspace/swiss-rounds/{project}/triad/round1-redundancy.md
`)

# Wait for announcement

sessions_spawn(agentId="project-critic", task=`
Swiss Rounds Triad — Round 1 Critique

Read:
- All reports: ~/.openclaw/workspace/swiss-rounds/{project}/reports/
- Redundancy: ~/.openclaw/workspace/swiss-rounds/{project}/triad/round1-redundancy.md

Output: ~/.openclaw/workspace/swiss-rounds/{project}/triad/round1-critique.md
`)

# Wait for announcement

sessions_spawn(agentId="never-say-die", task=`
Swiss Rounds Triad — Round 1 Solution

Read:
- All reports
- round1-redundancy.md
- round1-critique.md

Output: ~/.openclaw/workspace/swiss-rounds/{project}/triad/round1-solution.md
`)
```

### Advance to Round 2

```powershell
.\scripts\swiss-rounds.ps1 -Action advance -Project {project}
```

---

## Round 2: Addendum 1 (Cross-Reading)

### Spawn All Specialists (Parallel OK)

Each specialist reads others' reports and appends Addendum 1 to their OWN file.

```
sessions_spawn(agentId="analyst", task=`
Swiss Rounds Round 2 — Addendum 1 for: {project}

Read your SWISS_ROUND_INSTRUCTIONS.md for detailed instructions.

Summary:
1. Read ALL OTHER specialists' Round 1 reports
2. Append "## Addendum 1 (Cross-Reading)" to YOUR report
3. Include: Agreements, Disagreements, Questions, Synthesis
`)
```

### Triad → Advance

Same pattern: sequential triad on all addendums, then advance.

---

## Round 3: Retrospective Part 1

Each specialist reads addendums written ABOUT their work (in other reports mentioning them), then adds retrospective to their own file.

---

## Round 4: Addendum 2 (Cross-Feedback)

Each specialist reads others' Retrospective Part 1, then appends "Addendum 2 from {agentId}" to OTHERS' files.

⚠️ **Multiple files modified per specialist** — They write to others' reports, not their own.

---

## Round 5: Final Retrospective

Each specialist reads Addendum 2s on their OWN file (written by others), produces final position.

---

## PM Synthesis

After Round 5 triad completes:

```
sessions_spawn(agentId="project-manager", task=`
Swiss Rounds PM Synthesis for: {project}

Read your SWISS_PM_INSTRUCTIONS.md for full details.

Consume ALL:
- 4 specialist reports (with all addendums + retrospectives)
- 15 triad validation files (3 per round × 5 rounds)

Produce:
- synthesis/{project}-plan.md — Master plan
- synthesis/{specialist}-plan.md — Per-agent implementation plans
- Kickstart sessions_spawn commands for each specialist
`)
```

---

## State Tracking Template

Paste this into your working memory and update as you go:

```markdown
## Swiss Rounds: {project}
**Started:** {date}
**Specialists:** analyst, ballistics, cosmo, seeker

### Round 1: Initial Reports
- [ ] analyst: pending
- [ ] ballistics: pending  
- [ ] cosmo: pending
- [ ] seeker: pending
- [ ] Triad: redundancy → critique → solution

### Round 2: Addendum 1
- [ ] All specialists
- [ ] Triad

### Round 3: Retrospective Part 1
- [ ] All specialists
- [ ] Triad

### Round 4: Addendum 2
- [ ] All specialists
- [ ] Triad

### Round 5: Final Retrospective
- [ ] All specialists
- [ ] Triad

### PM Synthesis
- [ ] project-manager
- [ ] Kickstart all agents
```

---

## Turn Estimation

Per round:
- Spawn specialists: 1 turn (parallel)
- Wait for specialists: N turns (typically 4-8, depends on complexity)
- Triad (3 sequential spawns): 3 turns minimum

**5 rounds × ~7 turns = ~35 turns minimum**
**Plus PM synthesis: ~2 turns**
**Total: ~40 turns**

---

## Validation Before Advancing

Always run before `advance`:

```powershell
.\scripts\swiss-rounds.ps1 -Action validate -Project {project}
```

Never advance if artifacts are missing.

---

## Abort

If project needs to be cancelled:

```powershell
.\scripts\swiss-rounds.ps1 -Action abort -Project {project}
```

State file is deleted. Report files remain for potential restart.
