# TODO.md - Active Tasks

*Last updated: 2026-02-03 19:50*

---

## 🏪 Computer Store Platform
**Repo:** https://github.com/ludoplex/computerstore-platform
**Running:** http://localhost:8003

### Needs User Input
- [ ] **SMTP config** - Need SMTP credentials for email verification
  - Server, port, username, password, from address
  - Suggest: Zoho Mail SMTP or any provider
- [ ] **Stripe keys** - Need live/test API keys in `.env`
  - `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_WEBHOOK_SECRET`

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
**Status:** Part of zoho-console-api-module-system
**Location:** `C:\zoho-console-api-module-system`
**Running:** http://localhost:8080 (uvicorn)

- [ ] Review current state of SOP module
- [ ] Continue per `docs/zoho-crm-sop-plan.md`

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

## 🔧 OpenClaw Agent Spawning
**Status:** BLOCKED
**Bug:** https://github.com/openclaw/openclaw/issues/8445

All `sessions_spawn` calls fail with:
```
TypeError: Cannot read properties of undefined (reading 'trim')
```

Workaround: Work directly in main session until fixed.

---

## 💡 Ideas / Backlog

- [ ] **cosmo-python** - Use metaist/cosmo-python for portable Python (APE)
- [ ] **ggLeap API** - May need partner access for full docs

---

*Update this file as tasks complete or change.*
