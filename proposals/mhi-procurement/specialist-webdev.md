# MHI Procurement Web App — Feasibility Analysis
**Date:** 2026-02-09 21:45 MST  
**Deadline:** 2026-02-10 12:00 MST (~14 hours)  
**Analyst:** webdev specialist

---

## Executive Summary

**Verdict: 14 hours is NOT realistic for a complete, production-ready solution.**

However, a functional MVP with core features is achievable. Here's the breakdown:

| Scenario | Hours | Feasibility |
|----------|-------|-------------|
| Full feature parity (all APIs, complete UI) | 40-60h | ❌ Not possible |
| Solid MVP (2 suppliers, core search/order) | 14-16h | ⚠️ Barely possible (crunch mode) |
| Proof-of-concept (1 supplier, basic UI) | 6-8h | ✅ Achievable |

---

## SDK Availability Analysis

### ✅ Ingram Micro — Official TypeScript SDK Available
```
Package: xi_sdk_resellers@1.2.0
Published: 2025-01-27 (current, maintained)
Maintainer: xvantage-integration (official Ingram)
Docs: https://developer.ingrammicro.com/reseller
```
**Features covered by SDK:**
- Product search & catalog
- Price & availability
- Order creation & tracking
- Returns & renewals
- Quote creation
- Freight estimates

**Time savings: ~6-8 hours** (vs building from scratch)

### ✅ TD SYNNEX — Community TypeScript SDK Available
```
Package: synnex-xml-sdk@1.1.24
Published: 2025-08-17
Type: XML-based service wrapper
Dependencies: axios, xml2js
```
**Features covered:**
- Product lookup
- Pricing
- Inventory/availability
- Order submission
- Order status tracking

**Caveat:** Community SDK, not official. May need verification/patches.  
**Time savings: ~4-6 hours**

### ⚠️ D&H Distributing — No SDK, REST API Available
```
API Base: https://api.dandh.com
Type: REST API (JSON)
Documentation: Requires partner portal access
```
**Must build from scratch:**
- Custom API client wrapper
- Auth flow (likely OAuth2 or API key)
- Type definitions for all endpoints
- Error handling

**Estimated build time: 4-6 hours** for basic coverage

### 📋 Climb Channel Solutions — Manual Only
Per requirements, Climb is manual. No API integration needed.  
**Implementation:** Simple form to generate PO PDFs, manual tracking.  
**Time: ~1 hour** for basic UI

---

## Existing Assets Review

### SQLite Schema: REUSABLE ✅
```
C:\mhi-procurement\src\db\schema.sql
```

The existing schema is **well-designed** and **fully reusable**:

| Table | Purpose | Reuse |
|-------|---------|-------|
| `products` | SSOT for product data | ✅ Perfect |
| `suppliers` | Already seeded with all 4 suppliers | ✅ Perfect |
| `supplier_offerings` | Price/inventory by supplier+warehouse | ✅ Perfect |
| `market_prices` | Competitor pricing | ✅ Perfect |
| `basket_items` | Shopping cart | ✅ Perfect |
| `purchase_orders` + `po_line_items` | Order tracking | ✅ Perfect |
| `sync_log` | API sync audit trail | ✅ Perfect |
| `v_margin_analysis` | Margin calculation view | ✅ Perfect |

**No schema changes needed.** The existing design handles multi-supplier, multi-warehouse scenarios elegantly.

### Existing Codebase: NOT REUSABLE
The existing `mhi-procurement` is a **C++/CImGui desktop app** (Cosmopolitan-based). None of the application code is portable to web.

---

## Framework Recommendation

### Winner: **Next.js 14+ (App Router)**

| Factor | Next.js | SvelteKit |
|--------|---------|-----------|
| **TypeScript** | Native, excellent DX | Good, but more setup |
| **Component ecosystem** | shadcn/ui, Radix, etc. | Smaller ecosystem |
| **Server actions** | Built-in, great for forms | Similar capability |
| **API routes** | Native in app/api/ | Native |
| **Auth** | NextAuth.js mature | Auth.js (same lib) |
| **SQLite** | better-sqlite3 works well | Same |
| **Familiarity** | More tutorials/examples | Steeper curve |
| **Deployment** | Vercel, self-host, etc. | Same |

**Decision rationale:**
- Faster to scaffold with familiar patterns
- shadcn/ui gives us a complete component library for tables, forms, dialogs
- Server components for efficient data loading
- React Query for real-time stock polling

---

## Detailed Time Estimates

### Phase 1: Scaffolding & Foundation (2-3 hours)
| Task | Time |
|------|------|
| `npx create-next-app` with TypeScript | 5 min |
| Install core deps (shadcn/ui, Tailwind, Drizzle ORM) | 15 min |
| Port SQLite schema, configure better-sqlite3 | 30 min |
| Auth setup (NextAuth.js with multi-entity) | 45 min |
| Basic layout, navigation | 30 min |
| Entity/supplier credential management UI | 30 min |

### Phase 2: Ingram Micro Integration (2-3 hours)
| Task | Time |
|------|------|
| Install & configure `xi_sdk_resellers` | 15 min |
| Auth/credential flow per entity | 30 min |
| Product search endpoint | 30 min |
| Price & availability | 30 min |
| Order creation | 30 min |
| Order tracking | 20 min |
| Returns/quotes (if time) | 30 min |

### Phase 3: TD SYNNEX Integration (2-3 hours)
| Task | Time |
|------|------|
| Install & configure `synnex-xml-sdk` | 15 min |
| Auth flow | 20 min |
| Product search | 30 min |
| Pricing/availability | 30 min |
| Order submission | 45 min |
| Testing & debugging XML quirks | 30 min |

### Phase 4: D&H Integration (4-6 hours)
| Task | Time |
|------|------|
| Research API docs (partner portal) | 30 min |
| Build custom API client class | 60 min |
| Define TypeScript interfaces | 30 min |
| Auth implementation | 30 min |
| Product search | 45 min |
| Price/availability | 30 min |
| Order endpoints | 60 min |
| Testing | 30 min |

### Phase 5: Core UI (3-4 hours)
| Component | Time |
|-----------|------|
| Product search page (unified, all suppliers) | 45 min |
| Search results table with supplier comparison | 45 min |
| Product detail modal | 30 min |
| Shopping cart | 30 min |
| Order creation flow | 45 min |
| Order history & tracking | 30 min |
| Entity selector (MHI/DSAIC/Computer Store) | 20 min |

### Phase 6: Advanced UI (4+ hours) — NOT IN MVP
| Feature | Time |
|---------|------|
| Returns management | 60 min |
| Quote generation | 60 min |
| Freight calculator | 45 min |
| Margin analysis dashboard | 60 min |
| Market price comparison | 45 min |
| Bulk import/export | 60 min |

---

## Realistic 14-Hour Plan

### MVP Scope (what's achievable):

✅ **Included:**
- [ ] Next.js app with shadcn/ui
- [ ] SQLite database (existing schema)
- [ ] Multi-entity auth (MHI, DSAIC, Computer Store)
- [ ] Ingram Micro: full integration via SDK
- [ ] TD SYNNEX: full integration via SDK
- [ ] Unified product search
- [ ] Price comparison across suppliers
- [ ] Basic order creation
- [ ] Order tracking

❌ **Deferred:**
- D&H integration (no SDK, 4-6 hours alone)
- Climb (manual, low priority)
- Returns management
- Quote generation
- Freight calculator
- Advanced analytics

### Timeline

| Hour | Task |
|------|------|
| 0-2 | Scaffold Next.js, deps, SQLite, auth |
| 2-4 | Ingram Micro SDK integration |
| 4-6 | TD SYNNEX SDK integration |
| 6-9 | Product search UI, comparison table |
| 9-11 | Cart & order creation flow |
| 11-13 | Order tracking, entity switching |
| 13-14 | Testing, bug fixes, deployment |

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| SDK auth issues | Medium | High | Test credentials early (hour 1) |
| SYNNEX SDK bugs | Medium | Medium | Have XML fallback plan |
| D&H API access | High | High | Defer to post-MVP |
| Scope creep | High | High | Strict MVP boundary |
| Multi-entity auth complexity | Medium | Medium | Start simple, iterate |

---

## Alternative Approaches

### Option A: Extend Existing Desktop App
**Pros:** Schema already integrated, some business logic exists  
**Cons:** C++ to TypeScript = rewrite anyway, no web benefits  
**Verdict:** ❌ Not recommended

### Option B: Python + FastAPI + React
**Pros:** Could use Python Ingram SDK directly  
**Cons:** Need to wire up frontend anyway, no time savings  
**Verdict:** ❌ More complexity

### Option C: Low-code (Retool, Appsmith)
**Pros:** Fastest for CRUD interfaces  
**Cons:** API integration still manual, limited customization  
**Verdict:** ⚠️ Consider for admin dashboard post-MVP

---

## Credentials Required

Before starting, need from client:
- [ ] Ingram Micro API credentials (per entity: MHI, DSAIC, CS)
- [ ] TD SYNNEX API credentials (per entity)
- [ ] D&H API access (partner portal login)
- [ ] Climb login (for manual reference)

---

## Recommendation

### If deadline is hard: Build MVP (2 suppliers)
14 hours → Ingram + SYNNEX + core UI. Defer D&H, Climb.

### If quality matters: Request extension
24-30 hours → All 3 API suppliers + complete UI  
40 hours → Production-ready with all features

### If must demo something: Proof of concept
6 hours → Ingram only, basic search + order flow

---

## Quick Start Commands

```bash
# Create app
npx create-next-app@latest mhi-procurement --typescript --tailwind --eslint --app --src-dir

cd mhi-procurement

# Core dependencies
npm install xi_sdk_resellers synnex-xml-sdk
npm install better-sqlite3 drizzle-orm drizzle-kit
npm install next-auth @auth/drizzle-adapter
npm install @tanstack/react-query
npm install zod react-hook-form @hookform/resolvers

# UI components
npx shadcn@latest init
npx shadcn@latest add button input table dialog select card tabs form toast

# Dev tools
npm install -D @types/better-sqlite3
```

---

## Files to Create

```
mhi-procurement/
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   ├── ingram/[...route]/route.ts
│   │   │   ├── synnex/[...route]/route.ts
│   │   │   └── auth/[...nextauth]/route.ts
│   │   ├── search/page.tsx
│   │   ├── orders/page.tsx
│   │   ├── cart/page.tsx
│   │   └── layout.tsx
│   ├── lib/
│   │   ├── db/
│   │   │   ├── schema.ts (Drizzle types from SQL)
│   │   │   └── client.ts
│   │   ├── suppliers/
│   │   │   ├── ingram.ts (SDK wrapper)
│   │   │   ├── synnex.ts (SDK wrapper)
│   │   │   └── types.ts (unified interfaces)
│   │   └── auth.ts
│   └── components/
│       ├── product-search.tsx
│       ├── price-comparison-table.tsx
│       ├── cart.tsx
│       └── entity-selector.tsx
├── procurement.db (SQLite)
└── drizzle.config.ts
```

---

**Bottom line:** 14 hours is a brutal crunch for the full scope. Recommend negotiating for either reduced scope (2 suppliers) or extended timeline (24-30h for proper implementation).

*— webdev specialist*
