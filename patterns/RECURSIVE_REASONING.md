# Recursive Reasoning Pattern

A workflow pattern for AI-assisted development that ensures correctness through iterative verification.

## The Loop

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   ┌─────────┐    ┌───────────┐    ┌────────┐    ┌────────┐ │
│   │  PLAN   │───▶│ IMPLEMENT │───▶│ VERIFY │───▶│ PASS?  │ │
│   └─────────┘    └───────────┘    └────────┘    └────────┘ │
│        ▲                                             │      │
│        │              ┌──────────┐                   │      │
│        └──────────────│ REFLECT  │◀──────NO─────────┘      │
│                       └──────────┘           │              │
│                                              YES            │
│                                              │              │
│                                         ┌────▼────┐         │
│                                         │  DONE   │         │
│                                         └─────────┘         │
└─────────────────────────────────────────────────────────────┘
```

## Phases

### 1. Plan (max 5 bullets)
- Identify what needs to be done
- List affected files
- Propose implementation strategy
- Identify potential risks

### 2. Implement
- Apply minimal, focused changes
- One file at a time
- Follow language/framework conventions
- Document non-obvious decisions

### 3. Verify
- Run ALL verification commands
- Check for: syntax errors, lint warnings, type errors, test failures, build errors
- Capture FULL error output

### 4. Reflect (on failure)
- Read error messages CAREFULLY
- Identify root cause (not symptoms)
- Update mental model
- Return to Plan with new context

## Iteration Limits

| Complexity | Max Iterations |
|------------|----------------|
| Simple fix | 3 |
| New feature | 5 |
| Refactor | 7 |
| Complex debug | 10 |

If limit reached without success → escalate to human.

## Per-Language Verification

### Luau (Roblox)
```bash
stylua --check src
selene src
rojo build -o build.rbxlx
```

### Python
```bash
ruff check .
ruff format --check .
python -m pytest
```

### TypeScript
```bash
tsc --noEmit
eslint .
npm test
```

### C (Cosmopolitan)
```bash
cosmocc -Wall -Werror -c *.c
# or make with strict flags
```

### Assembly
```bash
nasm -f elf64 -o out.o in.asm
# Check for assembler errors
```

## Integration with OpenClaw

### Agent System Prompt Addition
```
When developing, follow the Recursive Reasoning Pattern:
1. Plan (5 bullets max)
2. Implement (minimal changes)
3. Verify (run ALL checks)
4. If fail: Reflect, identify root cause, return to 1
5. Max iterations: 5
6. If stuck: summarize attempts and ask for human guidance
```

### Hook Trigger
Agents can trigger verification via:
- `make check` (if Makefile exists)
- Direct command execution
- File watcher hooks

## Anti-Patterns

❌ **Don't**: Make multiple changes without verifying
❌ **Don't**: Ignore lint warnings
❌ **Don't**: Skip verification "just this once"
❌ **Don't**: Exceed iteration limit without escalating
❌ **Don't**: Fix symptoms instead of root cause

## Success Metrics

✅ Verification passes on first try: Excellent
✅ 1-2 iterations: Good
✅ 3-5 iterations: Acceptable
⚠️ 5+ iterations: Review approach
❌ Hit limit without success: Escalate
