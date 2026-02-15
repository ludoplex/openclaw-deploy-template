# HEARTBEAT.md - Periodic Tasks

## 🌙 Overnight Autonomous Mode (Feb 15, 2026)
**Status:** ACTIVE until ~10 AM MT
**Schedule:** See `AUTONOMOUS_SCHEDULE.md`
**Cron Jobs:** 7 jobs set (4 AM - 10 AM hourly checks)

### Current Focus
1. Check background search results (rapid-shoal, quiet-sable)
2. Find WithOdyssey credentials
3. Find Hetzner account info
4. Commit 80+ workspace changes
5. Analyze procurement codebase

### Capabilities Available
- ✅ Browser (Playwright headless)
- ✅ Email read/send (Zoho/SMTP)
- ✅ File & Git operations
- ⚠️ memory_search broken (use direct SQLite)

## Backup Check (every 4 hours)
- Run `scripts/backup.ps1` if last backup > 4 hours ago
- Verify GitHub is in sync (no uncommitted changes)

## PR Reviews
*(none active)*

## Project Status
- SOP Dashboard actively in development
- Check for any failed services (dashboard:8080, llamafile:8081)

## Claude Code Desktop Monitoring
- **Session:** "compile openclaw with cosmopolitan on windows" (C:\ project)
- **Check:** `C:\Users\user\.claude\projects\C--\*.jsonl` for recent activity
- **Action if stale (>30 min):** Alert Vincent — may need to approve permissions in GUI
- ⚠️ **Cannot auto-approve:** Permission dialogs require human click in Claude Code UI
