# TODO.md - Active Tasks

*Last updated: 2026-02-03*

---

## 🏪 Computer Store Platform
**Repo:** https://github.com/ludoplex/computerstore-platform
**Running:** http://localhost:8002 (port 8000 has ghost connections)

### In Progress
- [ ] Wire auth routes (login/register actual functionality)
- [ ] Wire orders API to real DB operations
- [ ] Wire members API to real DB operations  
- [ ] Wire training API to real DB operations

### Integrations
- [ ] **ggLeap sync** - API docs captured, need to implement JWT auth + data sync
- [ ] **Odyssey API** - Contact katie@withodyssey.com for direct API access
- [ ] **Set up MHI Stripe account** for vendor payments (required for Odyssey)

### Completed ✅
- [x] All database models + Alembic migrations
- [x] HTMX stack pivot (FastAPI + Jinja2 + Tailwind + Alpine.js)
- [x] Products API with full CRUD, pagination, search
- [x] All page templates (index, products, product_detail, training, lan, esa, cart, login, register)
- [x] ggLeap API documentation captured
- [x] Odyssey payment process documented (Net 30, Stripe ACH)

---

## 📊 SOP Automation Dashboard
**Status:** Active development
**Running:** http://localhost:8080

- [ ] Continue development per ROADMAP.md

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
- [ ] Register domain: dsaic.ai
- [ ] Build website (SaaS/ML/DL, IBM/Climb Channel reseller)

### Computer Store
- [ ] Set up subdomain: computerstore.mightyhouseinc.com
- [ ] Point to Computer Store Platform

---

## 🔧 OpenClaw Browser Extension
**Status:** Workaround accepted

- [x] Diagnosed Chrome limitation (silent disconnect on cross-origin nav)
- [x] Added persistentTabs + webNavigation listeners
- [ ] Document cross-origin limitation in usage guide
- [ ] Consider periodic "ping" to detect stale connections

---

## 💡 Ideas / Backlog

- [ ] **Python 3 Cosmopolitan Port** - Native APE binary (see MEMORY.md)
- [ ] **ggLeap API blocker** - May need partner access, contact support

---

*Update this file as tasks complete or change.*
