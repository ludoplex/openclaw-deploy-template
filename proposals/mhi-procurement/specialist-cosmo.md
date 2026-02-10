# MHI Procurement Feature Parity Assessment

**Analyst:** Cosmo (Claude Opus)  
**Date:** 2026-02-09 21:44 MST  
**Deadline:** 2026-02-10 12:00 MST (14 hours)

---

## Executive Summary

**Can we achieve full feature parity in 14 hours?**

### 🔴 NO — Minimum realistic estimate: 18-24 hours

However, a **reduced scope MVP** is achievable in 12-14 hours.

---

## Codebase Analysis

### Current State (Analyzed)

| File | Size | Status | Notes |
|------|------|--------|-------|
| `ingram.c` | 32KB | ✅ Complete | OAuth2, search, P&A, catalog sync, pricing sync, order creation |
| `database.c` | 27KB | ✅ Complete | Full CRUD, margin analysis, basket, PO creation |
| `gui.c` | 22KB | 🟡 Partial | Search, detail, basket, sync panels — missing order/tracking/returns UI |
| `http.c` | 48KB | ✅ Complete | TLS, connection pooling, OAuth2, rate limiting, retry logic |
| `config.h` | ~15KB | ✅ Scaffolded | Credential structures for ALL suppliers already exist |
| `schema.sql` | ~5KB | 🟡 Partial | Missing: shipments, returns, quotes tables |

### Key Finding: Config Infrastructure Exists!

```c
// Already defined in config.h:
mhi_synnex_creds_t  synnex;   // client_id, client_secret, base_url, account_number
mhi_dandh_creds_t   dandh;    // api_key, base_url, account_number
```

This saves ~1 hour on credential management.

---

## Detailed Time Estimates

### 1. SYNNEX Integration (`synnex.c`)

**Template:** `ingram.c` pattern is directly reusable

| Task | Hours | Notes |
|------|-------|-------|
| Study TD SYNNEX API docs | 0.5 | XML API vs REST — need to verify current API |
| OAuth2 auth adaptation | 0.5 | Same flow, different endpoints |
| Search implementation | 1.0 | Map to SSOT product structure |
| P&A lookup | 0.5 | Price and availability endpoint |
| Catalog sync | 1.0 | Pagination, rate limiting |
| Order creation | 0.5 | PO submission |
| **Subtotal** | **4.0** | |

**Risk:** SYNNEX API may require XML parsing (+1-2 hours if XML)

### 2. D&H Integration (`dandh.c`)

| Task | Hours | Notes |
|------|-------|-------|
| Study D&H API docs | 0.5 | REST API with API key auth |
| Auth implementation | 0.25 | Simpler than OAuth2 (API key header) |
| Search implementation | 1.0 | |
| P&A lookup | 0.5 | |
| Catalog sync | 1.0 | |
| Order creation | 0.5 | |
| **Subtotal** | **3.75** | |

### 3. Multi-Entity Credential Switching

| Task | Hours | Notes |
|------|-------|-------|
| Extend config.h for entity array | 0.5 | `mhi_entity_t entities[8]` |
| Entity selection in each supplier module | 0.5 | Add `entity_id` param to config loads |
| Database entity_id column | 0.25 | Track which entity owns each record |
| Config file parser updates | 0.5 | INI sections per entity |
| Entity selector UI | 0.5 | Dropdown in menu bar |
| **Subtotal** | **2.25** | |

**Shortcut Option:** Hardcode 2-3 entities, save ~1 hour

### 4. Parallel Search Across All Suppliers

| Task | Hours | Notes |
|------|-------|-------|
| Threading infrastructure | 0.75 | pthreads, mutex for result collection |
| Concurrent API dispatch | 0.5 | Fire searches to Ingram + SYNNEX + D&H |
| Result aggregation | 0.5 | Dedupe by UPC/MFR part |
| Combined results UI | 0.5 | Unified table with supplier column |
| Error handling per supplier | 0.25 | Partial success handling |
| **Subtotal** | **2.5** | |

### 5. Complete CImGui UI

#### Current Panels (Done)
- ✅ Product Search
- ✅ Product Detail / Margin Analysis  
- ✅ Basket (basic)
- ✅ Sync Status

#### Missing Panels

| Panel | Hours | Complexity |
|-------|-------|------------|
| **Orders Management** | 1.5 | PO list, status, details, line items |
| **Order Tracking** | 1.5 | Shipments table, tracking numbers, carrier links |
| **Returns/RMA** | 1.5 | Return requests, RMA status, history |
| **Quotes** | 1.25 | Quote creation, expiry, conversion to PO |
| **Freight Calculator** | 1.0 | Weight-based estimates, carrier comparison |
| **Entity Switcher** | 0.5 | Dropdown + credential status indicator |
| **Parallel Search Results** | 0.5 | Multi-supplier result table |
| **Subtotal** | **7.75** | |

---

## Total Estimate Summary

| Component | Minimum | Realistic | With Issues |
|-----------|---------|-----------|-------------|
| SYNNEX Integration | 4.0h | 4.5h | 6.0h |
| D&H Integration | 3.75h | 4.0h | 5.0h |
| Multi-Entity | 2.25h | 2.5h | 3.0h |
| Parallel Search | 2.5h | 3.0h | 4.0h |
| Complete UI | 7.75h | 8.5h | 10.0h |
| **TOTAL** | **20.25h** | **22.5h** | **28.0h** |

---

## Recommended Approach: MVP in 14 Hours

### Scope Reduction Options

| Cut | Hours Saved | Impact |
|-----|-------------|--------|
| Drop D&H (Phase 2) | 3.75h | Ingram + SYNNEX = 2 suppliers |
| Simplify multi-entity | 1.0h | Hardcode 3 entities, no dynamic config |
| Sequential search (no threading) | 1.5h | Slower but works |
| Basic UI only (Orders + Tracking) | 4.0h | Defer Returns, Quotes, Freight |

### Achievable 14-Hour Scope

1. ✅ **SYNNEX Integration** (4h)
2. ✅ **Basic Multi-Entity** (1.5h hardcoded)
3. ✅ **Sequential Multi-Supplier Search** (1h)
4. ✅ **Orders Panel** (1.5h)
5. ✅ **Tracking Panel** (1.5h)
6. ✅ **Entity Switcher UI** (0.5h)
7. ⏸️ Testing & Integration (4h)

**Total: ~14 hours** — Achievable but tight

### What Gets Deferred (Phase 2)

- D&H integration
- Returns/RMA panel
- Quotes panel
- Freight calculator
- Parallel search (use sequential)
- Dynamic entity configuration

---

## Risk Factors

| Risk | Probability | Mitigation |
|------|-------------|------------|
| SYNNEX API uses XML, not JSON | Medium | +2h for XML parser, or find JSON endpoint |
| API rate limits hit during testing | Low | Use sandbox/test accounts |
| OAuth2 token refresh edge cases | Low | Copy proven ingram.c pattern |
| CImGui layout issues on Windows | Low | Sokol is well-tested |
| Config parser bugs | Medium | Keep entity config simple |

---

## Recommendation

### For 12:00 Noon Deadline:

**Execute the 14-hour MVP scope:**

1. Start with SYNNEX immediately (highest value)
2. Hardcode multi-entity (don't over-engineer)
3. Add sequential search (simplest working solution)
4. Orders + Tracking UI (core business value)
5. Leave Returns/Quotes/Freight for Phase 2

### If More Time Available (16-18h):

Add parallel search threading — significant UX improvement.

### If Blocked on SYNNEX API:

Pivot to D&H first (simpler API key auth) — lose SYNNEX, gain D&H.

---

## Files to Create

```
C:\mhi-procurement\src\sync\
├── synnex.h       # Header following ingram.h pattern
├── synnex.c       # ~800-1000 lines (following ingram.c)
├── dandh.h        # (Phase 2)
└── dandh.c        # (Phase 2)

C:\mhi-procurement\src\db\
└── schema_v2.sql  # Add shipments, returns, quotes tables

C:\mhi-procurement\src\ui\
└── gui.c          # Extend with Orders, Tracking panels
```

---

## Bottom Line

| Question | Answer |
|----------|--------|
| Full feature parity in 14h? | **No** |
| Useful MVP in 14h? | **Yes** — Ingram + SYNNEX + Orders + Tracking |
| Risk level | **Medium** — SYNNEX API unknowns |
| Confidence | **70%** on MVP scope |

**Start immediately on SYNNEX integration.**
