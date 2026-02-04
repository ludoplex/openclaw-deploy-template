# TODO.md - Active Tasks

*Last updated: 2026-02-03*

---

## 🏪 Computer Store Platform
**Repo:** https://github.com/ludoplex/computerstore-platform
**Running:** http://localhost:8003 (ports 8000-8002 have ghost connections)

### In Progress
- [ ] Email verification flow (send actual emails - need SMTP config)
- [ ] Add products to cart (frontend JS)
- [ ] Set up Stripe keys in .env for live testing

### Recently Completed
- [x] **Stripe checkout integration** (commit a8387a3):
  - PaymentIntent creation API
  - Stripe Elements in checkout page
  - Webhook handler for payment_intent.succeeded
  - Auto-create orders on successful payment
  - Added stripe_customer_id to User, user_id to Order
- [x] **Password reset flow** (commit 508acea):
  - Forgot password page with email submission
  - Token generation (1-hour expiry)
  - Reset password page with token validation
  - Clears lockout on password reset
- [x] **Protected routes & user pages** (commit 6af48c5):
  - Protected routes: /account, /checkout, /orders, /orders/{id}
  - Redirect to login with ?next= param
  - Updated nav with user dropdown when authenticated
  - New templates: account.html, checkout.html, orders.html, order_detail.html
  - Profile update + password change endpoints
- [x] **Auth implementation** (commit 8ec2846):
  - User model with password hashing (bcrypt)
  - JWT tokens with python-jose
  - Login/register with HTMX flash messages
  - Cookie-based sessions with remember-me
  - Account lockout after failed attempts
  - `/api/auth/register`, `/api/auth/login`, `/api/auth/logout`, `/api/auth/me`, `/api/auth/check`, `/api/auth/token`
- [x] Wire orders API to real DB operations (commit 574ac93)
- [x] Wire members API to real DB operations (commit 574ac93)
- [x] Wire training API to real DB operations (commit 574ac93)
- [x] Lint cleanup with ruff (commit 1c11752)

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
