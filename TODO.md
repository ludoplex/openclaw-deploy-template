# TODO.md - Active Tasks

*Last updated: 2026-02-03 19:50*

---

## 🏪 Computer Store Platform
**Repo:** https://github.com/ludoplex/computerstore-platform
**Running:** http://localhost:8003

### Needs User Input
- [x] **SMTP config** - ✅ CONFIGURED (Zoho Mail rachelwilliams@mightyhouseinc.com)
  - Tested and working 2026-02-03 21:50 MST
- [ ] **Stripe keys** - Need live/test API keys in `.env`
  - `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_WEBHOOK_SECRET`
- [ ] **ggLeap API key** - Need from ggLeap admin: https://admin.ggleap.com/settings/api
  - `GGLEAP_API_KEY` in `.env`

### Needs Live Testing (ggLeap)
- [ ] **ggLeap sync** - Code complete (commit 3d73c4a), needs live ggLeap environment
  - Test `/api/lan/ggleap/status` endpoint
  - Test member sync
  - Test station status monitoring

### Recently Completed ✅
- [x] **ggLeap integration** (commit 3d73c4a):
  - GGLeapSyncService for bidirectional sync
  - Member sync endpoints
  - Station status monitoring
  - Integration documentation
- [x] **Cart functionality** - Full add-to-cart with localStorage + API validation
- [x] **Stripe checkout** (commit a8387a3)
- [x] **Email verification flow** (commit 332e2ba) - UI done, needs SMTP
- [x] **Password reset** (commit 508acea)
- [x] **Protected routes** (commit 6af48c5)
- [x] **Auth system** (commit 8ec2846)

### Integrations
- [ ] **Odyssey API** - Contact katie@withodyssey.com for direct API access
- [ ] **Set up MHI Stripe account** for vendor payments (required for Odyssey)

---

## 📊 SOP Automation Dashboard
**Status:** ✅ RUNNING
**Location:** `C:\zoho-console-api-module-system`
**URL:** http://localhost:8085

### Completed
- [x] SOP Engine (`src/modules/sop/engine.py`) - Full workflow execution
- [x] CRM Module (`src/modules/crm/`) - Records, blueprints, webhooks
- [x] CLI for supplier email search
- [x] **Web Dashboard** (FastAPI + HTMX) - `src/dashboard/`
  - Dashboard home with stats by entity
  - SOP list with filtering
  - SOP detail view with manual trigger
  - Execution history
  - CRM webhook endpoint (`/webhook/crm`)
- [x] Per-entity SOP definitions (9 total):
  - MHI: 3 (New Lead, Lead Qualification, Deal Processing)
  - DSAIC: 1 (Demo Request)
  - Computer Store: 3 (Order, Student Enrollment, Certification)
  - Cross-Entity: 2 (Student-to-Employee, Influencer Pipeline)

### To Start Dashboard
```powershell
cd C:\zoho-console-api-module-system
$env:PYTHONPATH="src"
python -c "from src.dashboard.app import app; import uvicorn; uvicorn.run(app, host='127.0.0.1', port=8085)"
```

---

## 🐦 Mixpost-Malone (Social Media Manager)
**Status:** PAUSED
**Repo:** https://github.com/ludoplex/mixpost-malone
**Waiting on:** Entity websites for MHI, DSAIC, Computer Store

- [ ] Resume after entity websites are ready
- See `memory/2026-02-03.md` for full context

---

## 🌐 Entity Websites

### MHI (Mighty House Inc)
- [x] Domain: mightyhouseinc.com (EXISTS)
- [ ] Build website (GovCon, EDWOSB, HUBZONE, IT Solutions)

### DSAIC (Data Science Applications, Inc)
- [ ] Register domain for DSAIC (NOT .ai - avoid AI association)
- [ ] Build website (SaaS/ML/DL, IBM/Climb Channel reseller)

### Computer Store
- [ ] Set up subdomain: computerstore.mightyhouseinc.com
- [ ] Point to Computer Store Platform

---

## 🔧 OpenClaw Agent Fleet
**Status:** ✅ WORKING (17 agents deployed)
**Bug Fixed:** https://github.com/openclaw/openclaw/issues/8445

Spawning works. Use `/agent <id>` or `sessions_spawn(agentId="...", task="...")`.

⚠️ Keep `hooks.internal.entries.workflow-enforcer.enabled: false` - causes .trim() error

---

## 💡 Ideas / Backlog

- [ ] **cosmo-python** - Use metaist/cosmo-python for portable Python (APE)
- [ ] **ggLeap API** - May need partner access for full docs

---

*Update this file as tasks complete or change.*
