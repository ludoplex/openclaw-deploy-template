# Edit Guardian Hook

## Purpose
Prevents agents from editing files without proper due diligence:
1. **Read Before Edit** — Must read a file before modifying it
2. **Specialist Consultation** — Certain file types require asking the appropriate specialist agent

## Triggers
- `tool:Edit` — Before any file edit
- `tool:Write` — Before any file write (to existing files)

## Logic

### Rule 1: Read Before Edit
Tracks files read via `tool:Read` in session state. If an edit is attempted on a file that wasn't read first, inject a warning and suggest reading it.

### Rule 2: Specialist Routing
For certain file patterns, remind the agent to consult specialists:

| Pattern | Specialist | Reason |
|---------|------------|--------|
| `.github/workflows/*` | cicd | CI/CD expertise |
| `scripts/build-*.ps1` | cicd, testcov | Build/test verification |
| `scripts/build-*.sh` | cicd, testcov | Build/test verification |
| `Makefile*` | cicd, cosmo | Build system |
| `tests/*` | testcov | Test coverage |
| `src/db/*` | ops | Database layer |
| `src/net/*`, `src/sync/*` | neteng | Network/sync |
| `helpers/gui_*` | cosmo, asm | Platform helpers |
| `*.asm`, `*.s` | asm | Assembly |
| `vendor/*` | cosmo | Third-party deps |

### Exceptions
- Files the agent created in this session (new files)
- AGENTS.md, SOUL.md, memory/* (agent workspace files)
- Explicit override via `--force` comment in edit

## State
Maintains per-session state:
- `filesRead: Set<string>` — Files read this session
- `filesCreated: Set<string>` — Files created this session
- `specialistsConsulted: Map<string, string[]>` — File → agents consulted

## Output
Injects system message when rules are violated, doesn't block (advisory).
