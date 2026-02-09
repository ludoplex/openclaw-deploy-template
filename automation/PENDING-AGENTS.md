# Pending Agent Spawns

## After Automation Project Complete:

### 1. Hindsight Agent
```
sessions_spawn(agentId="hindsight", task="Post-mortem: MHI Automation System")
```
**Output:** `~/.openclaw/workspace/hindsight/mhi-automation-2026-02-08.md`

**Capture:**
- What worked well
- What didn't work
- Time/effort estimates vs reality
- Lessons learned about multi-agent coordination
- Playwright vs Selenium learnings
- Zoho API patterns discovered

### 2. Foresight Agent
```
sessions_spawn(agentId="foresight", task="Review against hindsight archive: {next proposal}")
```
**Output:** `~/.openclaw/workspace/foresight/{proposal}-{date}.md`

**Use for:**
- GPU server deployment (Wednesday)
- Any future automation projects
- Portal integration decisions

---

*Trigger: When all current agents complete and automation system is tested*
