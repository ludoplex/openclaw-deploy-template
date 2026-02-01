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

---

## Lessons Learned

### 2026-01-31: llamafile > Ollama
User prefers Cosmopolitan/APE philosophy (jart). Use llamafile for local LLM, not Ollama. Single portable binaries, no daemons.

---

*Update this file with significant learnings and decisions.*
