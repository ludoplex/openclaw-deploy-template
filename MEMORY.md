# MEMORY.md - Long-Term Memory

*Curated knowledge that persists across sessions.*

## Tools & Capabilities

### Local LLM Delegation
**Added: 2026-01-31**

I have a local Qwen 2.5 7B model running via llamafile (Cosmopolitan APE).

**Use it for simple tasks to save Claude tokens:**
```python
import sys; sys.path.insert(0, r"C:\Users\user\.openclaw\workspace")
from local_llm import ask_local, generate_json, summarize, format_for_platform
```

- `ask_local(prompt)` - General simple prompts
- `generate_json(description)` - Create JSON from description
- `summarize(text, max_words)` - Summarize long text
- `format_for_platform(text, platform)` - Adapt for Discord/WhatsApp/etc.

**Delegate:** Formatting, summaries, JSON gen, data extraction
**Keep for Claude:** Reasoning, planning, tool use, complex code

### Zoho API System
**Path:** `C:\zoho-console-api-module-system\`
**APIs:** CRM, Books, Inventory, Desk, Analytics, Projects, Cliq, Sign
**Auth:** OAuth 2.0 with auto-refresh

---

## User Preferences

*(To be filled as I learn them)*

---

## Active Projects

### SOP Automation Dashboard
- **Repo:** https://github.com/ludoplex/sop-automation-dashboard
- **Entities:** MHI (GovCon), DSAIC (SaaS), Computer Store (Gaming)
- **Stack:** FastAPI + HTMX, llamafile for content gen
- **Target:** 2026-02-07

### Mixpost-Malone (Social Media Manager) - PAUSED
- **Repo:** https://github.com/ludoplex/mixpost-malone
- **Status:** Entity/brand feature complete, local deploy ready
- **Local:** `C:\dev\mixpost-app` (Docker) + `C:\dev\mixpost-malone` (package)
- **Waiting on:** Entity websites for MHI, DSAIC, Computer Store
- **Resume:** See `memory/2026-02-03.md` for full details

### Entity Websites - IN PLANNING
**MHI (Mighty House Inc):**
- Domain: mightyhouseinc.com ✅ EXISTS
- GovCon, EDWOSB, HUBZONE, IT Solutions
- Location: 977 Gilchrist St, Wheatland WY 82201

**DSAIC (Data Science Applications, Inc):**
- Domain: TBD (NOT .ai - user explicitly stated no AI association)
- SaaS/ML/DL - original + IBM/Climb Channel reseller
- Independent brand, MHI-backed

**Computer Store:**
- Domain: computerstore.mightyhouseinc.com (FREE SUBDOMAIN)
- Clearly MHI-affiliated
- Retail + Esports/LAN + Training/Certification

---

## Lessons Learned

### 2026-01-31: llamafile > Ollama
User prefers Cosmopolitan/APE philosophy (jart). Use llamafile for local LLM, not Ollama. Single portable binaries, no daemons.

---

## Ideas / Future Projects

### Python 3 Cosmopolitan Port - ALREADY EXISTS ✅
**Added: 2026-01-31 | Resolved: 2026-02-03**

**No need to build!** `cosmo-python` by metaist already provides Python 3.10-3.14 as APE binaries.
- Repo: https://github.com/metaist/cosmo-python
- ~45MB single-file executables
- Known limitations: no tkinter, no dlopen, ctypes callbacks broken on macOS ARM64

Use `cosmo-python` for interpreter, `cosmofy` to bundle apps, `cosmoext` for pre-compiled C extensions.

---

## Workflow

### PR Review Process (mixpost-malone)
**Added: 2026-02-01**

1. Create feature branch for new work
2. Push and create PR → triggers Sourcery AI + Copilot review
3. Check PR comments: `gh pr view <num> --repo ludoplex/mixpost-malone --json reviews,comments`
4. Fix issues, push updates
5. Merge when approved

### Qwen Delegation Checklist
Before using Claude for a task, ask: "Can Qwen handle this?"

**YES → Qwen:**
- Code formatting/cleanup
- Simple summaries (<500 words)
- JSON/YAML generation
- Platform-specific text formatting
- Boilerplate code generation
- Comment/docstring writing

**NO → Claude:**
- Complex reasoning/planning
- Multi-file refactoring
- API design decisions
- Security-sensitive code
- Tool orchestration

### ⚠️ CRITICAL: Workflow Applies to ALL Work
**Added: 2026-02-02**

User explicitly stated: workflow enforcement applies to EVERYTHING, not just specific projects.

**Before ANY task:**
1. Run `.\scripts\should-use-claude.ps1 "task description"` 
2. Or mentally route: Qwen → Shell → lmarena → Claude (escalate only when needed)

**For planning/architecture:**
- Open lmarena.ai for multi-model comparison
- Document decision in memory

**This is not optional.** Token cost matters.

---

## Multi-Agent Fleet
**Added: 2026-02-03**
**Updated: 2026-02-03** — Added cicd, testcov, seeker
**Spawning enabled:** (config: main.subagents.allowAgents)

17 specialized agents with isolated workspaces at `~/.openclaw/agents/`:

| Agent | Focus |
|-------|-------|
| main🦞 | Personal, general (default) |
| ops📊 | MHI/DSAIC/ComputerStore business, Zoho |
| webdev🌐 | FastAPI, HTMX, Python |
| cosmo🌌 | Cosmopolitan/jart, APE, C |
| social📱 | Mixpost, social media |
| course📚 | Training/certification content |
| pearsonvue🎓 | Testing center operations |
| ggleap🎮 | LAN center management |
| asm⚙️ | AMD64, AArch64, MASM64 |
| metaquest🥽 | Meta Quest 3 VR |
| neteng🔌 | Network/systems/deployment/AD |
| roblox🧱 | Roblox/Luau |
| cicd🔄 | GitHub Actions, CI/CD workflows |
| testcov🧪 | Test coverage, pytest, jest, property testing |
| seeker🔍 | Advanced search: Fravia methods, Feynman decomposition, Bayesian game theory |
| sitecraft🏗️ | Domain registration, hosting, website dev/maintenance |
| skillsmith⚒️ | Minimal skills, agent hooks, token optimization |

**Switch:** `/agent <id>` or `sessions_spawn(agentId="...", task="...")`

### Recursive Reasoning Pattern
All agents follow: `PLAN → IMPLEMENT → VERIFY → REFLECT → REPEAT (max 5)`
Pattern doc: `~/.openclaw/workspace/patterns/RECURSIVE_REASONING.md`

### Recursive Reasoning Pattern
All agents follow: `PLAN → IMPLEMENT → VERIFY → REFLECT → REPEAT (max 5)`
Pattern doc: `~/.openclaw/workspace/patterns/RECURSIVE_REASONING.md`

---

## Blockers

### ggLeap API
**Status:** Docs require admin login; integration code written but untested
**Next:** Test endpoints with live ggLeap credentials

### workflow-enforcer Hook (DISABLED)
**Added: 2026-02-03**
Hook causes `sessions_spawn` to fail with `.trim()` error.
- Issue: https://github.com/openclaw/openclaw/issues/8445
- Workaround: Keep `hooks.internal.entries.workflow-enforcer.enabled: false`
- Don't re-enable until OpenClaw team fixes bootstrap file injection

---

## Deployment Lessons

### Docker Not Always Easier (2026-02-02)
For **mixpost-malone** deployment, Docker via GitHub Codespaces added friction:
- Codespaces stuck in "Queued" state
- Services showing "No running process"
- No SSH access without sshd feature

**Solution**: Direct PHP devcontainer without Docker. Simpler = faster debugging.

### Mixpost is a Package
Mixpost needs a Laravel host app. Setup:
```bash
composer create-project laravel/laravel mixpost-app
cd mixpost-app
composer config repositories.mixpost-malone path ../mixpost-malone
composer require inovector/mixpost:@dev --ignore-platform-req=ext-pcntl
composer require laravel/breeze --dev --ignore-platform-req=ext-pcntl
php artisan breeze:install blade --no-interaction
php artisan migrate
```

### pcntl Extension Workaround
Horizon requires pcntl (Unix process control). In dev containers without it:
```bash
composer install --ignore-platform-req=ext-pcntl
```

---

*Update this file with significant learnings and decisions.*
