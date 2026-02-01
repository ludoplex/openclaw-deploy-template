# WORKFLOW.md - Task Execution Framework

*Minimize token consumption. Maximize quality. Use the right tool for the job.*

---

## Phase 1: Planning 🧠

**Goal:** Define the approach before writing code.

### Tools
| Tool | Use Case | Access |
|------|----------|--------|
| **lmarena.ai** | Multi-model brainstorming (GPT 5.2, Opus 4.5, Gemini) | Browser |
| **Local Qwen** | Quick validation, format checks | `local_llm.py` |
| **Whiteboard** | Architecture diagrams | Paper/draw.io |

### Process
1. **Define the problem** in 1-2 sentences
2. **Open lmarena.ai** → Side-by-side mode
3. **Prompt all models** with the problem + constraints
4. **Compare responses** → extract best ideas from each
5. **Document decision** in `memory/YYYY-MM-DD.md`

### Planning Prompt Template
```
Task: [brief description]
Constraints: [tech stack, time, dependencies]
Question: What's the best approach? Consider:
- Architecture patterns
- Edge cases
- Error handling
- Testing strategy
```

---

## Phase 2: Setup 🔧

**Goal:** Generate boilerplate without burning Claude tokens.

### Tools (Priority Order)
1. **Cookiecutter** - Project/file templates
2. **Local Qwen** - Simple code generation
3. **puter.js** - Browser-based AI assistance
4. **lmarena.ai** - Complex generation (multi-model vote)

### Cookiecutter Templates

Location: `~/.openclaw/workspace/templates/`

```bash
# Create from template
cookiecutter templates/laravel-provider
cookiecutter templates/python-module
cookiecutter templates/fastapi-route
```

### Local Qwen Delegation

```python
from local_llm import ask_local, generate_json

# Generate boilerplate
code = ask_local("""
Generate a PHP trait for OAuth authentication with methods:
- getAuthorizationUrl()
- requestAccessToken()
- refreshToken()
Follow Laravel conventions.
""")

# Generate config/data structures
config = generate_json("Laravel service class with credentials array")
```

### Code Validation (Before Using)

Always validate generated code:
```python
from local_llm import ask_local

# Quick syntax check
result = ask_local(f"Check this PHP for syntax errors. Reply ONLY with errors or 'OK':\n{code}")
```

---

## Phase 3: Execution ⚡

**Goal:** Use tools and scripts, not tokens.

### Principle
> If a shell command can do it, don't use Claude for it.

### Tool Mapping

| Task | Tool | NOT Claude |
|------|------|------------|
| File search | `rg`, `fd`, `grep` | ❌ |
| Code formatting | `prettier`, `php-cs-fixer` | ❌ |
| Linting | `eslint`, `phpstan`, `ruff` | ❌ |
| Git operations | `git`, `gh` | ❌ |
| API testing | `curl`, `httpie` | ❌ |
| JSON processing | `jq` | ❌ |
| File transforms | `sed`, `awk` | ❌ |
| Bulk operations | PowerShell/Bash loops | ❌ |

### Helper Scripts

Location: `~/.openclaw/workspace/scripts/`

```powershell
# scripts/new-provider.ps1 - Create MixPost provider scaffold
# scripts/validate-php.ps1 - Run PHP syntax check
# scripts/pr-review.ps1 - Fetch and format PR review comments
```

### Execution Checklist

Before asking Claude to do something:
- [ ] Can a shell command do this?
- [ ] Can local Qwen handle this?
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
│  └─ YES → Use local Qwen or template
│
├─ Is X a planning/architecture decision?
│  └─ YES → Use lmarena.ai (multi-model)
│
├─ Is X complex reasoning or multi-step?
│  └─ YES → Use Claude (that's me)
│
└─ Default → Start with cheapest option, escalate if needed
```

### URLs

- **lmarena.ai**: https://lmarena.ai (multi-model chat)
- **puter.js**: https://puter.com (browser AI)
- **Qwen**: localhost:8081 (local LLM server)

---

## Templates Catalog

### Available
- `laravel-provider/` - MixPost social provider scaffold
- `python-module/` - Python package with tests
- `fastapi-route/` - FastAPI endpoint with validation

### To Create
- [ ] Laravel Service class
- [ ] React component
- [ ] OpenClaw skill

---

*Update this as new patterns emerge.*
