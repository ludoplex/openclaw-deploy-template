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

### GUNDOM — Ballistics Calculator
- **Repo:** https://github.com/ludoplex/GUNDOM | **Path:** `C:\GUNDOM`
- **PR #34:** Architecture refactor — deleted 6,195 lines Swift SQLite, replaced with C bridge (+2,660 lines)
- **Rule:** C core IS the product. Swift/iOS is temporary skin. ALL persistence in C.
- **CI Status:** 3 checks failing (Database Tests, Swift Unit Tests, Verify Binary Linking)
- **Tests:** ~90+ added (SQLiteIntegrationTests, CBridgeIntegrationTests, etc.)
- **Legacy:** `C:\BallisticsCalculator` is old prototype, NOT a git repo — don't use

### Apeswarm — SaaS Composition Platform
- **Repo:** https://github.com/ludoplex/apeswarm | **Path:** `C:\apeswarm`
- **Pushed:** commit 2408bfd (security, performance, ~165 tests, CI/CD)
- **SaaS priority:** IDP/RAG first (Q1), then AI Governance (Q2)
- **Differentiator:** Portable datacenter + single-binary = air-gapped AI moat

### Cosmo Toolchain
- **tedit-cosmo:** `C:\tedit-cosmo` — disasm view integrated (commit eee9060), 90 Unity tests
- **cosmo-disasm:** `C:\cosmo-disasm` → github.com/ludoplex/cosmo-disasm (3,027 lines)
- **e9studio:** `C:\e9studio`
- **llamafile-llm:** `C:\llamafile-llm`

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

## Claude.ai Skill Library (Created Jan 10, 2026)
**Source:** Claude.ai Max plan conversation "Creating a skill together"
**Location on Claude.ai:** `/mnt/skills/user/`
**Status:** NOT ported to OpenClaw yet

8 skills created in a marathon session:
1. **operational-substrate** — Always-on Seven Lenses reasoning (G/F/R/B/E/X/L). Core loop: OBSERVE→ORIENT→SEEK→RETRIEVE→DECOMPOSE→ANALYZE→VERIFY→OUTPUT. Anti-patterns tracked. This is THE meta-cognition layer.
2. **advanced-search** — Expert search operator combinations (Google/Bing/DDG). Query refinement, multi-engine tactics.
3. **web-reconnaissance** — Tech stack fingerprinting, URI conventions, markup taxonomy, microformats, structured data.
4. **gov-financial-intel** — SEC/CFIUS filings, super PACs, lobbyists, IRS/DOE/EPA/DOJ/BLM databases, wealth indices.
5. **deep-directory-index** — Gov/corporate/nonprofit/academic directories, libraries, internet directories, offline resources.
6. **industry-power-map** — NAICS-organized US industry dominance map. C-suite, activist investors, unions, foreign entities. Includes infra backbone, CDNs, carrier hotels, shipping.
7. **tech-security-analysis** — Cybersecurity narrative vs reality. $215B spending gap analysis. Cross-references search + tech skills.
8. **tampermonkey-llm-hub** — Browser automation via Tampermonkey + LLM_hub userscript.

**Key principle:** operational-substrate is always-on, shapes all reasoning. No methodology theater — lenses work underneath.

**TODO:** Port critical skills (operational-substrate, advanced-search, web-reconnaissance) to OpenClaw format for all 20 agents.

---

### Claude.ai Skills Ported to OpenClaw ✅
**Added: 2026-02-04**
7 skills, 40 files, 293KB → `C:\Users\user\.openclaw\workspace\skills\`
Committed `f44d87d`. Now visible in `<available_skills>` and WORKING!
Skills: operational-substrate, advanced-search, web-reconnaissance, gov-financial-intel, deep-directory-index, industry-power-map, tech-security-analysis
tampermonkey-llm-hub intentionally NOT ported (browser-specific).

### Statistical Analysis Agent (statanalysis 📈)
**Added: 2026-02-04**
Agent #21. Focus: anomaly detection, pattern recognition, statistical rigor.
Workspace: `C:\Users\user\.openclaw\agents\statanalysis`

### AI Void/Anomaly Analysis — 4 Public Repos
**Added: 2026-02-04**
- https://github.com/ludoplex/ai-void-analysis (main)
- https://github.com/ludoplex/ai-elevenlabs-analysis
- https://github.com/ludoplex/ai-arena-analysis
- https://github.com/ludoplex/ai-grok-analysis
ElevenLabs finding: 15.5% void cluster density, z=+6.69, p<0.00001
Scope expanded to ALL anomalies, not just void.

### Chrome Relay Lessons
- Relay drops after gateway restarts and tab navigation
- Blob URL download works for bulk data extraction
- Don't navigate existing tabs — open new ones instead

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

### MHI Procurement Engine
**Added: 2026-02-04**
Cross-platform desktop procurement app. CImGui + Sokol + Cosmopolitan single APE binary (~15MB).
- **Reference**: bullno1/cosmo-sokol (★33, active Jan 2026) — fork as starting point
- **Stack**: C core, SQLite, Lua plugins for supplier adapters
- **Suppliers**: Ingram Micro (REST v6, best), TD SYNNEX (Digital Bridge), D&H (REST OAS3), Climb (no API)
- **Free MVP**: Best Buy API + eBay Browse (prices), ShipEngine free (shipping), Icecat (product data), Zoho manual tax
- **Accounts**: Ingram #50-135152-000, Climb #CU0043054170, D&H #3270340000, TD SYNNEX #786379
- ⚠️ Amazon PA-API dying April 2026 — don't build on it
- ⚠️ Icecat > Etilize (free vs paid, same IT coverage)

### Peridot TTS Voice
**Added: 2026-02-04**
- Free tier: MS Edge AriaNeural w/ pitch/rate boost → tts_peridot.py
- Next: ElevenLabs for real Peridot voice (Shelby Rabara)
- Utility: `~/.openclaw/agents/neteng/tts_peridot.py`

### Research Rule
**Added: 2026-02-04**
DO NOT use Brave/web_search. Use Chrome relay (`profile="chrome"`) or headless (`profile="openclaw"`).
Fallback chain: browser → web_fetch → web_search (last resort only).

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
**Updated: 2026-02-04** — 20 agents total (added ballistics, climbibm, analyst)
**Spawning enabled:** (config: main.subagents.allowAgents)

20 specialized agents with isolated workspaces at `~/.openclaw/agents/`:

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
| ballistics🎯 | GUNDOM ballistics SME — ADVISORY ONLY. Advises asm, cosmo, testcov, cicd, neteng. Does NOT code directly. |
| climbibm🏔️ | IBM/Climb channel partnership |
| analyst📊 | Market analysis, competitive research |

**Switch:** `/agent <id>` or `sessions_spawn(agentId="...", task="...")`

### Recursive Reasoning Pattern
All agents follow: `PLAN → IMPLEMENT → VERIFY → REFLECT → REPEAT (max 5)`
Pattern doc: `~/.openclaw/workspace/patterns/RECURSIVE_REASONING.md`

---

## Blockers

### ggLeap API - UNBLOCKED
**Status:** Full API docs accessed via browser relay (admin.ggleap.com/public-api-documentation)
**Base URL:** https://api.ggleap.com/production
**Next:** Test endpoints with live credentials

### Computer Store SMTP - RESOLVED
**Configured:** 2026-02-03
- Zoho Mail: rachelwilliams@mightyhouseinc.com
- App password created for "Computer Store Platform"

### Computer Store Stripe - PENDING
Need API keys from dashboard.stripe.com

### workflow-enforcer Hook - FIXED ✅
**Added: 2026-02-03 | Fixed: 2026-02-04**
Was causing `sessions_spawn` to fail with `.trim()` error.
- **Root cause:** OpenClaw loads `handler.ts` before `handler.js` in candidate order. Raw TypeScript import fails with `.trim()`.
- **Fix:** Renamed `handler.ts` → `handler.ts.bak` so only compiled `handler.js` is found.
- Issue: https://github.com/openclaw/openclaw/issues/8445
- Status: ✅ ENABLED and working

### GUNDOM PR #34 CI Failures
3 checks failing: Database Tests, Swift Unit Tests, Verify Binary Linking
Copilot reviewed stale commit (pre-refactor), needs re-review after fix

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
