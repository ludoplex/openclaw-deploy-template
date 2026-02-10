# MHI Procurement — THE PATH FORWARD

**Solver:** Never Say Die  
**Date:** 2026-02-09 21:49 MST  
**Deadline:** 2026-02-10 12:00 MST  
**Time Available:** ~14 hours  

---

## THE VERDICT

### 🎯 C EXTENSION. D&H FIRST. SKIP SYNNEX TONIGHT.

The critic is right about one thing: the SYNNEX XML problem is real. But the critic missed that **D&H is the easier target** and the config infrastructure already exists.

---

## THE MATH THAT MATTERS

| Asset | Status | Evidence |
|-------|--------|----------|
| Ingram OAuth2 | ✅ WORKING | Account #50-135152-000 active, code tested |
| Ingram in C | ✅ 735 lines | `ingram.c` complete with search, P&A, sync, orders |
| D&H Account | ✅ ACTIVE | #3270340000 — partner access confirmed |
| SYNNEX Account | ✅ ACTIVE | #786379 — but XML API is a 4h+ time sink |
| Config structs | ✅ DONE | `mhi_dandh_creds_t` exists in config.h |
| HTTP/TLS | ✅ DONE | 1,164 lines, connection pooling, retries |
| Database | ✅ DONE | 585 lines, schema has `dandh` supplier seeded |

**The D&H account numbers are ALREADY in config.h defaults:**
```c
cfg_set(cfg->dandh.account_number, sizeof(cfg->dandh.account_number), "3270340000");
cfg_set(cfg->synnex.account_number, sizeof(cfg->synnex.account_number), "786379");
```

---

## WHY D&H BEFORE SYNNEX

| Factor | D&H | SYNNEX |
|--------|-----|--------|
| API Format | REST/JSON | XML Web Services |
| C Integration | Copy ingram.c pattern exactly | Need XML parser (+2-4h) |
| Auth | API key header (simple) | OAuth2 (same as Ingram) |
| Time to working MVP | 3-4 hours | 6-8 hours |
| Risk | Low | Medium-High |

**SYNNEX is valuable but it's a PHASE 2 item.** Don't let XML parsing blow the deadline.

---

## THE BUILD ORDER

### TONIGHT (9:30 PM → 2:00 AM = 4.5 hours)

#### Hour 1: Validate & Setup (9:30 PM - 10:30 PM)

```
[ ] 15 min — Create dandh.h/dandh.c stubs following ingram.h pattern
[ ] 15 min — Set MHI_DANDH_API_KEY env var, verify config loads it
[ ] 15 min — Research D&H API endpoints (login to partner portal)
[ ] 15 min — Make ONE test API call to D&H (curl first, then C)
```

**STOP/GO GATE:** If D&H test call fails, pivot to SYNNEX with yxml parser.

#### Hour 2-3: D&H Core Implementation (10:30 PM - 12:30 AM)

```
[ ] 30 min — dandh_auth(): API key header injection
[ ] 45 min — dandh_search(): Product search, parse JSON response
[ ] 45 min — dandh_get_price(): Price & availability lookup
```

#### Hour 4: D&H Sync (12:30 AM - 1:30 AM)

```
[ ] 45 min — dandh_sync_catalog(): Catalog pagination, upsert to SSOT
[ ] 15 min — Wire to CLI: `mhi-procurement sync dandh`
```

#### Hour 4.5: Commit & Sleep (1:30 AM - 2:00 AM)

```
[ ] 15 min — Test full D&H sync cycle
[ ] 15 min — Git commit, push, update build
```

**TONIGHT'S DELIVERABLE:** D&H search + sync working via CLI

---

### TOMORROW MORNING (7:00 AM → 12:00 PM = 5 hours)

#### Hour 5-6: Multi-Supplier Search (7:00 AM - 9:00 AM)

```
[ ] 30 min — Add `search_all()` function that calls ingram + dandh sequentially
[ ] 30 min — Merge results, dedupe by MFR part number
[ ] 30 min — CLI: `mhi-procurement search-all <query>`
[ ] 30 min — Wire GUI search panel to call both suppliers
```

#### Hour 7: GUI Wiring (9:00 AM - 10:00 AM)

```
[ ] 30 min — Sync panel: Add working "Sync D&H" button
[ ] 30 min — Search results: Add "Supplier" column, show Ingram/D&H
```

#### Hour 8: Multi-Entity (10:00 AM - 11:00 AM)

```
[ ] 30 min — Add entity_code to config (hardcode MHI, DSAIC, ComputerStore)
[ ] 30 min — GUI entity selector dropdown, swap credentials on select
```

#### Hour 9: Testing & Polish (11:00 AM - 12:00 PM)

```
[ ] 30 min — Full workflow test: search → add to basket → verify prices
[ ] 15 min — Build final APE binaries
[ ] 15 min — Write quick-start README
```

---

## WHAT SHIPS AT NOON

### ✅ Delivered

| Feature | Status |
|---------|--------|
| **Ingram Micro** | Full: Search, P&A, Sync, Orders |
| **D&H Distributing** | Search, P&A, Sync |
| **Multi-Supplier Search** | Query Ingram + D&H in one command |
| **Entity Switching** | MHI / DSAIC / Computer Store |
| **CLI** | All commands working |
| **GUI** | Basic panels functional |
| **Cosmopolitan APE** | Single binary, runs everywhere |

### ⏸️ Deferred to Phase 2

| Feature | Why Deferred |
|---------|--------------|
| **TD SYNNEX** | XML parsing adds 4+ hours |
| **Climb** | Manual-only per requirements |
| **Orders via D&H** | Core ordering works via Ingram |
| **Returns/RMA** | Nice-to-have, not MVP |
| **Parallel Search** | Sequential works for demo |
| **Freight Calculator** | Post-MVP |

---

## THE SYNNEX SOLUTION (PHASE 2)

Two options for after the deadline:

### Option A: Add yxml to C (Recommended)

[yxml](https://dev.yorhel.nl/yxml) is a ~1KB, zero-dependency XML parser.

```c
// Add to project:
// 1. Download yxml.c and yxml.h
// 2. Add to Makefile
// 3. Use streaming parser for SYNNEX responses

#include "yxml.h"

int synnex_parse_response(const char *xml, size_t len, product_t *out) {
    yxml_t x;
    char buf[4096];
    yxml_init(&x, buf, sizeof(buf));
    // Parse XML elements into product struct
}
```

**Time estimate:** 3-4 hours to add yxml + implement SYNNEX.

### Option B: Node.js Sidecar (If C XML is painful)

Create a tiny Node service that wraps `synnex-xml-sdk`:

```javascript
// synnex-proxy/index.js
const express = require('express');
const SynnexSDK = require('synnex-xml-sdk');

app.post('/search', async (req, res) => {
  const results = await SynnexSDK.search(req.body.query);
  res.json(results); // Returns JSON, C consumes it
});
```

C app calls `localhost:3001/search` — gets JSON back. No XML in C.

**Time estimate:** 2-3 hours to scaffold + test.

---

## CRITICAL PATH RISKS

| Risk | Probability | Mitigation |
|------|-------------|------------|
| D&H API key doesn't work | Low | Verify in Hour 1; pivot to SYNNEX if fails |
| D&H API is XML not JSON | Low | Webdev report says REST; verify early |
| GUI won't build | Low | CLI is the MVP; GUI is bonus |
| Fatigue after 2 AM | High | Sleep is mandatory. Coffee isn't enough. |

---

## DECISION TREE

```
START
  │
  ├─► Test D&H API (15 min)
  │     │
  │     ├─► WORKS → Continue with D&H (default path)
  │     │
  │     └─► FAILS → Test SYNNEX API
  │           │
  │           ├─► SYNNEX WORKS + JSON → Do SYNNEX instead
  │           │
  │           └─► SYNNEX WORKS + XML → Add yxml, do SYNNEX
  │                                    (add 2h to timeline)
  │
  └─► If BOTH fail → Ship Ingram-only MVP
                     (still valuable, 2 suppliers is Phase 2)
```

---

## FILES TO CREATE TONIGHT

```
C:\mhi-procurement\src\sync\
├── dandh.h      # Header (copy ingram.h pattern)
└── dandh.c      # Implementation (~400-600 lines)

C:\mhi-procurement\
└── Makefile     # Add dandh.o to build targets
```

### dandh.h Template

```c
#ifndef MHI_SYNC_DANDH_H
#define MHI_SYNC_DANDH_H

#include "../net/config.h"
#include "../db/database.h"

/* D&H API Functions */
int dandh_search(const mhi_dandh_creds_t *creds, 
                 const char *query, 
                 product_t *results, 
                 int max_results);

int dandh_get_price(const mhi_dandh_creds_t *creds,
                    const char *sku,
                    offering_t *offering);

int dandh_sync_catalog(sqlite3 *db,
                       const mhi_dandh_creds_t *creds,
                       int page_size,
                       int max_pages);

#endif
```

---

## THE BOTTOM LINE

| Question | Answer |
|----------|--------|
| C or TypeScript? | **C** — 3,600 lines of working code wins |
| SYNNEX or D&H first? | **D&H** — JSON API, faster to integrate |
| What about SYNNEX XML? | **Phase 2** — yxml or Node sidecar |
| Real MVP scope? | **Ingram + D&H + entity switching** |
| Can we ship by noon? | **YES** — if D&H API works and we stay focused |

---

## EXECUTE NOW

1. **Open terminal**
2. **Create dandh.h/dandh.c stubs**
3. **Set `MHI_DANDH_API_KEY` env var**
4. **Make one test curl to D&H API**
5. **GO/NO-GO decision by 10:00 PM**

The clock is running. Ship it.

---

*"Perfect is the enemy of good enough by noon."*

