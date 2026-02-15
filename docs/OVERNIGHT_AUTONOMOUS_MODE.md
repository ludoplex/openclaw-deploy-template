# Overnight Autonomous Mode

Documentation for Peridot's overnight autonomous operation.

## Overview

When Vincent goes to sleep, I operate autonomously using hourly cron jobs to check in and continue working. This document captures learnings and best practices.

## Cron Schedule

Typical overnight schedule (example from Feb 15, 2026):
- 4 AM - 10 AM MT: Hourly check-ins
- Each check-in evaluates HEARTBEAT.md tasks
- Work continues between check-ins

## Capabilities During Overnight

### ✅ Available
- File system operations (read, write, edit)
- Git operations (commit, push, pull)
- Python scripts and local LLM
- Zoho API (with rate limits)
- Email search and organization
- Documentation and code scaffolding
- Backup scripts

### ⚠️ Intermittent
- Browser control (Playwright) - sometimes times out
- Zoho API - may hit rate limits

### ❌ Not Available (Require User)
- Claude Code Desktop permission approvals
- Physical device interaction
- Account creation/login flows

## Workflow

1. **Check HEARTBEAT.md** - Follow task list strictly
2. **Prioritize autonomous work** - Code, docs, git, backups
3. **Skip blocked tasks** - Don't retry endlessly
4. **Document progress** - Update memory/YYYY-MM-DD.md
5. **Use local LLM** - Delegate simple tasks to Qwen
6. **Commit frequently** - Small atomic commits

## Token Conservation

During overnight operation, minimize Claude token usage by:
1. Delegating to local Qwen LLM for:
   - Text formatting
   - Summaries
   - JSON generation
   - Simple analysis
2. Batching operations
3. Avoiding repeated retries

## Best Practices

### Do
- Make progress on independent tasks
- Create documentation and scaffolds
- Run backups and maintenance
- Update memory files

### Don't
- Retry failing operations endlessly
- Block on user-required actions
- Make destructive changes without records
- Consume excessive tokens on simple tasks

## Example 4 AM Block (Feb 15, 2026)

### Accomplished
1. Saved WithOdyssey and Hetzner credentials
2. Researched WithOdyssey vendor platform
3. Analyzed MHI procurement codebase
4. Created Mouser sync module (mouser.c/h)
5. Created Element14 sync module (element14.c/h)
6. Updated config.h and schema.sql
7. Ran SOP dashboard tests (20/20 pass)
8. Ran backup to Local/OneDrive/GDrive
9. Multiple git commits across repos

### Blocked
- Browser snapshot timing out
- Build tools not in PATH
- Zoho API rate limited

### Time: ~15-20 minutes of active work
