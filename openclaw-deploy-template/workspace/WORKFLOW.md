# WORKFLOW.md - Task Execution Framework

*Minimize token consumption. Maximize quality. Use the right tool for the job.*

---

## Phase 1: Planning 🧠

**Goal:** Define the approach before writing code.

### Tools
| Tool | Use Case | Access |
|------|----------|--------|
| **lmarena.ai** | Multi-model brainstorming | Browser |
| **Local LLM** | Quick validation, format checks | Local server |
| **Whiteboard** | Architecture diagrams | Paper/draw.io |

### Process
1. **Define the problem** in 1-2 sentences
2. **Open lmarena.ai** → Side-by-side mode
3. **Prompt all models** with the problem + constraints
4. **Compare responses** → extract best ideas from each
5. **Document decision** in `memory/YYYY-MM-DD.md`

---

## Phase 2: Setup 🔧

**Goal:** Generate boilerplate without burning Claude tokens.

### Tools (Priority Order)
1. **Templates** - Project/file templates
2. **Local LLM** - Simple code generation
3. **lmarena.ai** - Complex generation (multi-model vote)

### Code Validation (Before Using)
Always validate generated code with linters and type checkers.

---

## Phase 3: Execution ⚡

**Goal:** Use tools and scripts, not tokens.

### Principle
> If a shell command can do it, don't use Claude for it.

### Tool Mapping

| Task | Tool | NOT Claude |
|------|------|------------|
| File search | `rg`, `fd`, `grep` | ❌ |
| Code formatting | `prettier`, `ruff format` | ❌ |
| Linting | `eslint`, `ruff`, `clippy` | ❌ |
| Git operations | `git`, `gh` | ❌ |
| API testing | `curl`, `httpie` | ❌ |
| JSON processing | `jq` | ❌ |
| File transforms | `sed`, `awk` | ❌ |
| Bulk operations | PowerShell/Bash loops | ❌ |

### Execution Checklist

Before asking Claude to do something:
- [ ] Can a shell command do this?
- [ ] Can a local LLM handle this?
- [ ] Is there a template for this?
- [ ] Can I use an existing script?

---

## Quick Reference

### Token-Saving Decision Tree

```
Need to do X?
│
├─ Is X a file/text operation?
│  └─ YES → Use shell tools (grep, sed, jq, etc.)
│
├─ Is X simple code generation?
│  └─ YES → Use local LLM or template
│
├─ Is X a planning/architecture decision?
│  └─ YES → Use lmarena.ai (multi-model)
│
├─ Is X complex reasoning or multi-step?
│  └─ YES → Use Claude (that's me)
│
└─ Default → Start with cheapest option, escalate if needed
```

---

*Update this as new patterns emerge.*
