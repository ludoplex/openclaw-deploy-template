# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Headless Browser (All Agents)

Built-in headless browser available to all agents.

- **Profile**: `profile="openclaw"` (autonomous, no user attachment required)
- **Use for**: Google searches, JS-rendered sites, documentation, interactive pages

### Fallback Chain
1. `browser` with `profile="openclaw"` — full browser, handles JS
2. `web_fetch` — lightweight, static content only
3. `web_search` — search API, quick search results

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
