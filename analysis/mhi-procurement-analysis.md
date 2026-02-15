# MHI Procurement Engine — Codebase Analysis
**Date:** 2026-02-15 04:15 AM MT
**Path:** C:\mhi-procurement\

## Overview
Cross-platform procurement tool built with Cosmopolitan Libc. Single portable binary (APE) with GUI compiled in.

## Codebase Stats
- **Source Files:** 20 C/H files
- **Size:** ~267.5 KB source code
- **Build Targets:** CLI-only APE, Full GUI APE, Native builds

## Architecture
```
┌─────────────────────────────────────────┐
│          CImGui + Sokol (GUI)           │
├─────────────────────────────────────────┤
│           CLI Interface                 │
├─────────────────────────────────────────┤
│     SQLite SSOT (database.c)            │
├──────────┬──────────┬──────────┬────────┤
│ Ingram   │ TD SYNNEX│ D&H     │ Climb  │
│ REST v6  │ Dig.Brdg │ OAS3    │ Manual │
├──────────┴──────────┴──────────┴────────┤
│ Market: Best Buy API | eBay Browse API  │
│ Enrichment: Icecat (free, 25.8M+ items) │
└─────────────────────────────────────────┘
```

## Source Structure
```
src/
├── main.c              # CLI + GUI entry point
├── db/
│   ├── database.c/h    # SQLite operations, CRUD
│   ├── schema.sql      # SSOT schema (products, offerings, POs)
│   └── schema_sql.h    # Embedded SQL for APE
├── net/
│   ├── http.c/h        # HTTP client (mbedTLS)
│   └── config.h        # INI config parser
├── sync/
│   ├── ingram.c/h      # Ingram Micro REST v6 (IMPLEMENTED ✅)
│   ├── synnex.c/h      # TD SYNNEX (STUB)
│   └── dandh.c/h       # D&H (STUB)
└── ui/
    ├── gui.c           # CImGui + Sokol GUI
    └── sokol_imgui_impl.c
```

## API Integration Status

| Supplier | Status | Implementation |
|----------|--------|----------------|
| **Ingram Micro** | ✅ WORKING (Sandbox) | Full REST v6: OAuth2, catalog, P&A, orders |
| **Mouser** | ✅ API KEY ACTIVE | Search API ready, need sync module |
| **Element14** | ✅ API KEY ACTIVE | Search API ready, need sync module |
| **TD SYNNEX** | ❌ Stub only | Need API credentials |
| **D&H** | ❌ Stub only | Need API credentials |
| **Climb** | ⚠️ Manual | Portal login only (no API) |

## Database Schema (SQLite)

### Core Tables
- **products** — SSOT product catalog (UPC, MFR part, name, MSRP, specs)
- **suppliers** — Supplier definitions (Ingram, SYNNEX, D&H, Climb)
- **supplier_offerings** — Per-supplier pricing, availability, warehouse
- **market_prices** — Best Buy, eBay reference prices
- **basket_items** — Shopping cart
- **purchase_orders** — PO headers
- **po_line_items** — PO detail lines
- **sync_log** — API sync audit trail

### Key View
- **v_margin_analysis** — Pre-computed margins:
  - MSRP margin %
  - Market margin %
  - Best/worst supplier cost
  - Cost spread across suppliers
  - Total available quantity

## Ingram Micro Integration (ingram.c)

### Implemented Features
- ✅ OAuth2 client credentials auth (auto-refresh)
- ✅ Token caching
- ✅ Product catalog search
- ✅ Price & availability lookup
- ✅ Rate limiting (60 req/min)
- ✅ Correlation ID tracking
- ✅ Audit logging
- ✅ Error handling with retries

### API Endpoints Used
```
POST /oauth/oauth30/token              — OAuth2 token
GET  /resellers/v6/catalog             — Product search
POST /resellers/v6/catalog/priceandavailability — P&A
GET  /resellers/v6/catalog/{sku}       — Product detail
POST /resellers/v6/orders              — Create order
```

### Required Headers
```c
Authorization: Bearer <token>
IM-CustomerNumber: 50-135152-000
IM-SenderID: MHI-Procurement
IM-CorrelationID: <uuid>
Content-Type: application/json
Accept: application/json
```

## Config (config.ini)

### Active Credentials
| Section | Key Fields | Status |
|---------|------------|--------|
| `[ingram]` | client_id, client_secret, customer_number | ✅ Sandbox working |
| `[mouser]` | search_api_key, order_api_key | ✅ Ready |
| `[element14]` | api_key | ✅ Ready |
| `[climb]` | username, password, account_num | ✅ Portal creds |
| `[synnex]` | — | ❌ Empty |
| `[dandh]` | — | ❌ Empty |

## Next Steps (Priority Order)

### 1. Mouser Sync Module (mouser.c)
- API key already in config.ini
- Search API at api.mouser.com/api/v1
- Rate limit: 30 req/min

### 2. Element14 Sync Module (element14.c)
- API key already in config.ini
- Search at api.element14.com
- Rate limit: 120 req/min (2 calls/sec)

### 3. TD SYNNEX & D&H API Credentials
- Search Rachel's Zoho email for API docs/keys
- D&H confirmed to have APIs (per MEMORY.md)

### 4. Production Ingram Migration
- Currently using sandbox
- Need to apply for production access

## Build Commands

```bash
# CLI-only APE
make cosmo

# Full GUI APE (recommended)
make cosmo-gui

# Native dev build
make native

# Run tests
make test-all
```

## Notes
- Clean C11 codebase, no external dependencies for APE
- SQLite amalgamation compiled in
- CImGui/Sokol GUI compiled directly into binary
- Single file distribution — one binary runs everywhere
