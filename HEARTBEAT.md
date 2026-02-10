# HEARTBEAT.md - Periodic Tasks

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
