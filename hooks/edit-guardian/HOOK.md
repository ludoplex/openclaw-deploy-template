# Edit Guardian Hook

## Purpose
Prevents agents from editing files outside their domain:
1. **Read Before Edit** — Must read a file before modifying it
2. **Delegate to Specialists** — Domain-specific files must be handled BY the specialist, not just reviewed

## Core Principle
**"Consult" ≠ "Delegate"**

- ❌ WRONG: Ask specialist for advice, then do the work yourself
- ✅ RIGHT: Spawn the specialist to DO the work in their domain

## Triggers
- `tool:Edit` — Before any file edit
- `tool:Write` — Before any file write (to existing files)

## Logic

### Rule 1: Read Before Edit
Tracks files read via `tool:Read` in session state. If an edit is attempted on a file that wasn't read first, inject a warning.

### Rule 2: Delegate to Domain Specialists (MANDATORY)
For certain file patterns, the agent MUST:
1. Call `agents_list()` to see all available specialists
2. Call `sessions_list()` to check if a specialist is already working
3. **SPAWN the specialist to do the work** — don't do it yourself

**The specialist does the work. You review the result if needed.**

| Pattern | Specialist | Domain |
|---------|------------|--------|
| `.github/workflows/*` | cicd | CI/CD workflows |
| `scripts/build-*.ps1` | cicd | Build scripts |
| `scripts/build-*.sh` | cicd | Build scripts |
| `Makefile*` | cicd, cosmo | Build system |
| `tests/*` | testcov | Test files |
| `src/db/*` | ops | Database layer |
| `src/net/*`, `src/sync/*` | neteng | Network/sync |
| `helpers/gui_*` | cosmo, asm | Platform helpers |
| `*.asm`, `*.s` | asm | Assembly |
| `vendor/*` | cosmo | Third-party deps |

### Correct Delegation Pattern
```
# 1. Check roster
agents_list()
sessions_list({ activeMinutes: 30 })

# 2. DELEGATE the work (not just ask for advice)
sessions_spawn(
  agentId="cicd",
  task="Fix the symbol verification in build-windows.ps1. 
        Use objdump from MSYS2 as primary method.
        Commit and push when done."
)

# 3. Wait for completion, review result
```

### What Delegation Means
- The specialist **reads the file**
- The specialist **makes the edit**
- The specialist **tests/verifies**
- The specialist **commits**
- You review the outcome

### Exceptions
- Files the agent created in this session (new files)
- AGENTS.md, SOUL.md, memory/* (agent workspace files)
- Agent IS the designated specialist for that domain
- Explicit override with clear justification

## State
- `filesRead: Set<string>` — Files read this session
- `filesCreated: Set<string>` — Files created this session  
- `rosterChecked: boolean` — Called agents_list()?
- `activeSessionsChecked: boolean` — Called sessions_list()?

## Output
Injects blocking message when rules are violated. Does NOT allow proceeding without delegation for domain-specific files.
