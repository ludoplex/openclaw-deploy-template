# MHI Procurement Triad Decision Analysis

**Date:** 2026-02-09 21:45 MST  
**Deadline:** 2026-02-10 12:00 MST (~14 hours)  
**Decision Required:** Extend C codebase vs. new TypeScript web app

---

## Executive Summary

**RECOMMENDATION: EXTEND THE C CODEBASE (Option A)**

The existing C codebase is far more complete and production-ready than initially described. Starting fresh with TypeScript would squander ~3,600 lines of working, tested code and miss the deadline. The C code follows excellent patterns that can be replicated for TD SYNNEX and D&H.

---

## Part 1: Existing Codebase Analysis

### What Actually Exists

| Component | Status | Lines | Notes |
|-----------|--------|-------|-------|
| **HTTP/HTTPS client** | ✅ COMPLETE | 1,164 | mbedTLS, connection pooling, retries, rate limiting, OAuth2 |
| **SQLite SSOT database** | ✅ COMPLETE | 585 | Full schema, parameterized queries, margin views |
| **Ingram Micro API** | ✅ COMPLETE | 735 | OAuth2, search, pricing, orders, catalog sync |
| **CImGui/Sokol GUI** | 🟡 Skeleton | 533 | Panels exist, needs wiring to full features |
| **CLI** | ✅ COMPLETE | 510 | Search, margins, sync commands |
| **Cosmopolitan build** | ✅ WORKING | — | 6.8MB APE binary, runs on all platforms |

**Total working code:** ~3,600 lines of C
**Binary size:** 6.8MB (GUI), 3.7MB (CLI)

### What's Actually Reusable

**100% Reusable:**
- `http.c` — Full HTTP client with TLS, rate limiting, OAuth2 token caching, retries, connection pooling
- `database.c` — SQLite SSOT with products, offerings, margins, basket, purchase orders
- `config.h` — Environment variable + INI file credential loading
- Schema — Already has `synnex`, `dandh`, `climb` suppliers seeded

**70% Reusable (needs extension):**
- `gui.c` — Panels exist for search/detail/basket/sync; need supplier picker and more features
- Build system — Makefile already handles multiple targets

**Copy/Adapt Pattern:**
- `ingram.c` — Well-structured 735 lines that serve as template for synnex.c and dandh.c

### Code Quality Assessment

**Strengths:**
- Security-conscious (parameterized SQL, credential redaction, secure zeroing)
- Proper error handling throughout
- Connection pooling and rate limiting built-in
- TLS certificate verification by default
- Audit logging for all API calls
- Clean separation: net/db/sync/ui

**Weaknesses:**
- Hand-rolled JSON parsing (adequate for API responses, but brittle)
- GUI is functional but basic
- No async/threading yet (but single-threaded is fine for procurement tool)

---

## Part 2: Effort Estimates

### Option A: Extend C Codebase

| Task | Hours | Notes |
|------|-------|-------|
| **TD SYNNEX API** | 3-4h | Copy ingram.c, adapt auth (Digital Bridge), same patterns |
| **D&H API** | 3-4h | Similar; D&H has clean OAS3 REST API |
| **Multi-entity config** | 1h | Extend config.h with entity_id field, add to requests |
| **"Search all" UI** | 1h | Already has search; add parallel supplier calls |
| **Wire sync buttons** | 1h | `gui_panel_sync()` has TODO comments |
| **Basic orders UI** | 2h | Basket→PO already works; add order status display |
| **Buffer/polish** | 1-2h | Testing, edge cases |

**Total: 12-15 hours** — Tight but achievable

### Option B: New TypeScript Web App

| Task | Hours | Notes |
|------|-------|-------|
| Project setup | 1h | Next.js/React, TypeScript config |
| HTTP client + OAuth2 | 3h | Even with axios, need token refresh logic |
| Database schema + ORM | 2h | Prisma/Drizzle setup, migrations |
| **Ingram Micro API** | 4h | Reimplement from scratch |
| **TD SYNNEX API** | 4h | Still need to learn their API |
| **D&H API** | 4h | Still need to learn their API |
| Multi-entity logic | 2h | Config, tenant switching |
| Search UI | 2h | |
| Product detail UI | 2h | |
| Basket + orders UI | 3h | |
| Margin analysis | 2h | |
| Sync status UI | 1h | |
| **Total** | **30+ hours** | **IMPOSSIBLE in 14h deadline** |

**TypeScript is a non-starter for this deadline.**

---

## Part 3: Redundancy Analysis

### QuoteWerks

QuoteWerks is a quoting tool, not a procurement tool. It:
- Creates customer-facing quotes
- Doesn't do multi-supplier price comparison
- Doesn't auto-route orders to cheapest supplier
- Doesn't track supplier margins
- Costs money per seat

**Verdict:** NOT redundant. MHI Procurement solves a different problem.

### What MHI Procurement Does That QuoteWerks Doesn't

1. **SSOT across all suppliers** — Single database with Ingram, TD SYNNEX, D&H normalized
2. **Margin analysis** — Real-time visibility into MSRP margin, market margin, supplier spread
3. **Cheapest supplier routing** — Automatic selection of best price
4. **Cross-supplier search** — One search, all suppliers
5. **Cosmopolitan deployment** — Single binary, no installation, runs everywhere

---

## Part 4: Recommended Implementation Plan

### Phase 1: Foundation (2-3h) — Tonight

1. **Create `synnex.c` and `dandh.c` stubs**
   - Copy `ingram.c` structure
   - Implement config loading (credentials from env/config.ini)
   - Add supplier ID constants

2. **Add multi-entity to config**
   ```c
   // In config.h
   typedef struct {
       char entity_code[16];  // "mhi", "dsaic", "computerstore"
       char entity_name[64];
       // Per-supplier account numbers
       char ingram_customer_num[32];
       char synnex_account[32];
       char dandh_account[32];
   } mhi_entity_t;
   ```

### Phase 2: TD SYNNEX API (3-4h)

TD SYNNEX Digital Bridge API:
- **Auth:** OAuth2 client credentials → same as Ingram
- **Endpoints:** Similar REST structure
- **Reuse:** `http.c` handles OAuth2 token refresh automatically

```c
// synnex.c — follows exact same pattern as ingram.c
int synnex_auth(synnex_config_t *cfg);
int synnex_search(synnex_config_t *cfg, const char *query, ...);
int synnex_get_price(synnex_config_t *cfg, const char *sku, ...);
int synnex_sync_catalog(sqlite3 *db, synnex_config_t *cfg, ...);
```

### Phase 3: D&H API (3-4h)

D&H REST API:
- **Auth:** API key header (simpler than OAuth2)
- **OAS3 spec:** Well-documented, clean endpoints
- **Mapping:** Same product/offering database tables

### Phase 4: UI Wiring (2-3h)

1. **Sync Panel** — Add working buttons:
   ```c
   if (igMenuItem_Bool("Sync TD SYNNEX", NULL, false, true)) {
       synnex_sync_catalog(g_gui.db, &synnex_cfg, 25, 10);
       gui_load_sync_log();
   }
   ```

2. **Search All Suppliers**
   - Call `ingram_search()`, `synnex_search()`, `dandh_search()` in sequence
   - Merge results into search_results array
   - UI already handles displaying results

3. **Entity Selector**
   - Add dropdown in main menu
   - Store selected entity in gui_state_t
   - Pass to API calls

### Phase 5: Orders + Tracking (if time permits)

Ingram already has `ingram_create_order()` — expose in UI:
- Add "Submit PO" button in Basket panel
- Show order confirmation dialog
- Add order tracking panel

---

## Part 5: Risk Assessment

### Option A Risks (C Extension)

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| TD SYNNEX auth differs | Low | They use standard OAuth2; http.c handles it |
| D&H API quirks | Low | OAS3 spec is clean; simpler than Ingram |
| CImGui bugs | Low | GUI is optional; CLI works |
| Time overrun | Medium | Cut scope to search+sync only; defer orders |

### Option B Risks (TypeScript)

| Risk | Likelihood | Impact |
|------|------------|--------|
| Miss deadline | **CERTAIN** | Project fails |
| Throw away working code | Certain | Waste of prior investment |
| New bugs in HTTP/OAuth | High | C version is tested and working |

---

## Conclusion

### Why Option A (Extend C)

1. **~3,600 lines of working code** — HTTP client, OAuth2, database, Ingram API all DONE
2. **Clean patterns** — `ingram.c` is a 735-line template; copy for synnex/dandh
3. **Time math works** — 12-15h of work, 14h deadline = achievable with focus
4. **No redundancy** — QuoteWerks doesn't do this; MHI Procurement fills a real gap
5. **Cosmopolitan value** — One 6.8MB binary replaces "run npm install on every machine"

### Why NOT Option B (TypeScript)

1. **30+ hours minimum** — Deadline is 14 hours
2. **Throw away working Ingram integration** — Already tested, production-ready
3. **Re-solve solved problems** — OAuth2, rate limiting, connection pooling
4. **New dependency hell** — Node.js, npm, package vulnerabilities
5. **No actual advantage** — "Modern" doesn't mean "better for this use case"

---

## Appendix: File Reference

```
C:\mhi-procurement\
├── src/
│   ├── db/
│   │   ├── database.c    # 585 lines — Full SSOT implementation
│   │   ├── database.h
│   │   └── schema.sql    # Products, offerings, margins, basket, POs
│   ├── net/
│   │   ├── http.c        # 1,164 lines — HTTP/TLS/OAuth2/rate limiting
│   │   ├── http.h
│   │   └── config.h      # Credential loading
│   ├── sync/
│   │   ├── ingram.c      # 735 lines — Complete Ingram API
│   │   ├── ingram.h
│   │   └── market.h      # (placeholder for market prices)
│   ├── ui/
│   │   ├── gui.c         # 533 lines — CImGui panels
│   │   └── sokol_imgui_impl.c
│   ├── main.c            # 510 lines — CLI
│   └── gui_main.c        # 57 lines — GUI entry point
└── dist/
    ├── mhi-procurement.com       # 3.7 MB CLI APE
    └── mhi-procurement-gui.com   # 6.8 MB GUI APE
```

---

**Decision: Proceed with Option A (Extend C codebase)**

Start with TD SYNNEX API tonight. If time runs short, D&H can be stubbed and completed post-deadline — search-all-suppliers with just Ingram+SYNNEX still delivers value.
