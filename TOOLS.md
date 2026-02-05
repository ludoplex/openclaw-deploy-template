# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## Local LLM (llamafile - APE)

- **llamafile**: v0.9.3 (Cosmopolitan APE binary)
- **Model**: Qwen2.5-7B-Instruct Q3_K_M (3.5GB)
- **Binary**: `bin/llamafile.exe`
- **Model**: `models/qwen2.5-7b-instruct-q3_k_m.gguf`
- **GPU**: RTX 4060 (8GB VRAM, 29/29 layers offloaded)
- **Performance**: ~23ms/token, ~43 tok/s

### Why llamafile?
- Single portable executable (Cosmopolitan Libc)
- No daemon/service required
- Cross-platform (Windows/Linux/Mac)
- Aligns with ApeSwarm/jart philosophy

### Usage (CLI)
```bash
./bin/llamafile.exe -m models/qwen2.5-7b-instruct-q3_k_m.gguf \
  -p "Your prompt here" -n 100 --no-display-prompt -ngl 99
```

### Usage (Server mode)
```bash
./bin/llamafile.exe -m models/qwen2.5-7b-instruct-q3_k_m.gguf \
  --server --port 8081 -ngl 99
# API at http://localhost:8081/v1/chat/completions
```

### Python Helper (USE THIS!)
**Location**: `local_llm.py` in workspace root

```python
# Import from workspace
import sys; sys.path.insert(0, r"C:\Users\user\.openclaw\workspace")
from local_llm import ask_local, generate_json, summarize, format_for_platform

# Simple prompt
result = ask_local("Reformat this as bullet points: ...")

# Generate JSON from description
data = generate_json("user with name, email, role")

# Summarize text
summary = summarize(long_text, max_words=100)

# Format for platform (Discord, WhatsApp, Telegram, Twitter)
formatted = format_for_platform(text, "discord")
```

### Delegate to Local LLM
- Text formatting/cleanup
- Simple summaries (<500 words)
- Data extraction
- JSON/YAML generation
- Template substitution

### Keep on Claude
- Complex reasoning
- Multi-step planning  
- Code generation with context
- Tool use coordination

---

## Zoho API System

- **Path**: `C:\zoho-console-api-module-system\`
- **APIs**: CRM, Books, Inventory, Desk, Analytics, Projects, Cliq, Sign
- **Auth**: OAuth 2.0 with auto-refresh

---

## Headless Browser (All Agents)

Built-in headless browser available to all agents — no Chrome relay needed.

- **Profile**: `profile="openclaw"` (autonomous, no user attachment required)
- **CDP Port**: 18801
- **Use for**: Google searches, JS-rendered sites, documentation, interactive pages
- **Skill**: `browser-research` — see skill for full usage patterns

```
browser profile:"openclaw" action:"launch" url:"https://www.google.com/search?q=query"
browser profile:"openclaw" action:"snapshot"
```

### Fallback Chain
1. `browser` with `profile="openclaw"` — full browser, handles JS
2. `web_fetch` — lightweight, static content only
3. `web_search` — Brave API, quick search results

## Chrome Browser Relay (Optional)

- `profile="chrome"` — requires user to attach a Chrome tab via OpenClaw Browser Relay toolbar button
- Use when you need the user's authenticated session (logged-in sites)

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
