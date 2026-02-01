# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## Local LLM (Ollama)

- **Ollama**: v0.15.2
- **Model**: qwen2.5:7b (4.7GB)
- **Path**: `C:\Users\user\AppData\Local\Programs\Ollama\`
- **API**: `http://localhost:11434`
- **GPU**: RTX 4060 (8GB VRAM)
- **Performance**: ~0.2s warm, ~51s cold start

### Usage
```python
import requests
response = requests.post(
    'http://localhost:11434/api/generate',
    json={"model": "qwen2.5:7b", "prompt": "...", "stream": False}
)
print(response.json()["response"])
```

### Delegate to Local LLM
- Text formatting/cleanup
- Simple summaries (<500 words)
- Data extraction
- JSON/YAML validation
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
