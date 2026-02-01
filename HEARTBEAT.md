# HEARTBEAT.md - Periodic Tasks

## Backup Check (every 4 hours)
- Run `scripts/backup.ps1` if last backup > 4 hours ago
- Verify GitHub is in sync (no uncommitted changes)

## PR Reviews (check every 2 hours until merged)
- [ ] mixpost-malone PR #1: `.\scripts\pr-review.ps1 -Repo "ludoplex/mixpost-malone" -PR 1`
- Fix any issues flagged by Copilot/Sourcery, push updates

## Project Status
- SOP Dashboard actively in development
- Check for any failed services (dashboard:8080, llamafile:8081)
