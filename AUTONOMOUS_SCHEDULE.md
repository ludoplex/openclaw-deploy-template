# Autonomous Operations Schedule
**Created:** February 15, 2026 at 3:04 AM MT
**Mode:** Overnight autonomous operation

## Hour-by-Hour Schedule (3 AM - 10 AM MT)

| Hour | Focus Area | Tasks | Cron Job |
|------|------------|-------|----------|
| **3:00 AM** | Setup & Planning | Create this schedule, commit workspace, check background searches | N/A (manual) |
| **4:00 AM** | Credential Hunt | Check background search results, search OneDrive for WithOdyssey creds, Hetzner info | `credential-search-check` |
| **5:00 AM** | Procurement Analysis | Analyze `C:\mhi-procurement` codebase, document API integration status | `procurement-codebase-review` |
| **6:00 AM** | WithOdyssey Research | Browser research on each state portal, document login flows | `withodyssey-research` |
| **7:00 AM** | Documentation | Update manifests, memory files, commit changes | `documentation-sync` |
| **8:00 AM** | Email Check | Check Zoho for supplier responses (D&H, TD SYNNEX, Arrow) | `supplier-email-check` |
| **9:00 AM** | Testing | Test working API credentials (Ingram, Mouser, Element14) | `api-credential-test` |
| **10:00 AM** | Morning Report | Compile overnight progress report, send to Vincent | `morning-report` |

## Priority Tasks (Execute When Time Allows)

### P1 - Critical Path
1. **WithOdyssey Credentials** - Find login creds for state portals
2. **Hetzner Account Info** - Find existing account or document signup needs
3. **Git Commit** - Commit 80+ uncommitted workspace changes

### P2 - Value-Add
4. **Procurement App Analysis** - Document `database.c`, `http.c`, supplier modules
5. **API Testing** - Verify Ingram/Mouser/Element14 credentials work
6. **NixOS Config Draft** - Start creating NixOS configuration for VPS

### P3 - Background
7. **Memory Maintenance** - Update MEMORY.md with learnings
8. **Documentation** - Update manifests and READMEs
9. **Calendar Sync** - Keep OPENCLAW_WORK_CALENDAR.md current

## Capabilities Available

| Capability | Status | Notes |
|------------|--------|-------|
| Browser (Playwright) | ✅ Ready | profile="openclaw" for headless |
| Email Read (Zoho) | ✅ Ready | Rachel PRIMARY, Vincent SECONDARY |
| Email Send (SMTP) | ✅ Ready | From: Rachel, Reply-To: Vincent |
| File Operations | ✅ Ready | Full workspace access |
| Git Operations | ✅ Ready | Commit, push to GitHub |
| Local LLM | ✅ Ready | llamafile delegate for simple tasks |
| GUI Automation | ⚠️ Limited | Scripts exist, need testing |
| Memory Search | ⚠️ Issues | Direct SQLite works, tool has session corruption |

## Enforcement Mechanism

Cron jobs fire systemEvent reminders to main session.
HEARTBEAT.md checks provide backup enforcement every ~30 min.

## Success Criteria for Morning Report

- [ ] WithOdyssey credentials located OR documented as unfindable
- [ ] Hetzner account info found OR documented signup steps
- [ ] Workspace committed to GitHub
- [ ] At least 3 supplier APIs tested
- [ ] Procurement app structure documented
- [ ] No critical errors or failures overnight
