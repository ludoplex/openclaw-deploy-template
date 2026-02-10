# MHI Procurement App — Local Resources Discovery

**Search Date:** 2026-02-09
**Search Locations:** C:\mhi-procurement\, C:\dev\, C:\Users\user\.openclaw\workspace\, C:\Users\user\Documents\

---

## Summary

Found **two major procurement-related codebases**:
1. **C:\mhi-procurement\** — Complete C-based procurement engine with Ingram Micro API integration (FULLY IMPLEMENTED)
2. **C:\dev\computerstore-platform\** — Python/FastAPI platform that syncs FROM the MHI procurement DB

---

## 1. MHI Procurement Engine (PRIMARY)

**Location:** `C:\mhi-procurement\`
**Language:** C with Cosmopolitan Libc (cross-platform APE binary)
**Status:** PRODUCTION-READY with Ingram Micro integration complete

### Key Source Files

| File | Size | Description |
|------|------|-------------|
| `src/sync/ingram.c` | 32KB | **Ingram Micro REST v6 API integration** (COMPLETE) |
| `src/net/http.c` | 48KB | HTTP client with TLS, rate limiting |
| `src/net/config.h` | ~25KB | Configuration management, credential loading |
| `src/db/database.c` | 27KB | SQLite SSOT database operations |
| `src/main.c` | 21KB | CLI entry point, commands |
| `src/ui/gui.c` | 22KB | CImGui/Sokol GUI implementation |

### Distributor API Support

| Distributor | Account # | API Type | Status | Implementation |
|-------------|-----------|----------|--------|----------------|
| **Ingram Micro** | #50-135152-000 | REST v6 | ✅ COMPLETE | `src/sync/ingram.c` |
| **TD SYNNEX** | #786379 | Digital Bridge | 🔲 Planned | Credential struct ready |
| **D&H** | #3270340000 | REST OAS3 | 🔲 Planned | Credential struct ready |
| **Climb** | #CU0043054170 | Manual | 🔲 No API | - |

### Ingram Micro Integration Details

From `src/sync/ingram.c`:

```c
/* MHI Procurement Engine — Ingram Micro API Sync Implementation
 * REST v6 at developer.ingrammicro.com
 * Account: #50-135152-000
 *
 * Implements:
 *   - OAuth2 client credentials authentication
 *   - Product catalog search
 *   - Price and availability lookup
 *   - Mapping to SSOT (mhi_product_t, mhi_offering_t)
 *   - Full sync to database with audit trail
 *
 * Ingram Micro API v6 endpoints used:
 *   POST /oauth/oauth30/token              — OAuth2 token
 *   GET  /resellers/v6/catalog             — Product search
 *   POST /resellers/v6/catalog/priceandavailability — P&A
 *   GET  /resellers/v6/catalog/{sku}       — Product detail
 *   POST /resellers/v6/orders              — Create order
 */
```

### Configuration Management

**Config File:** `config.example.ini` (template provided)

**Environment Variables Supported:**
- `MHI_INGRAM_CLIENT_ID`, `MHI_INGRAM_CLIENT_SECRET`
- `MHI_SYNNEX_CLIENT_ID`, `MHI_SYNNEX_CLIENT_SECRET`
- `MHI_DANDH_API_KEY`
- `MHI_BESTBUY_API_KEY`
- `MHI_EBAY_CLIENT_ID`, `MHI_EBAY_CLIENT_SECRET`
- `MHI_ICECAT_USERNAME`
- `MHI_DB_PATH`, `MHI_AUDIT_LOG_PATH`

### Reusable Components

1. **OAuth2 Client Credentials Flow** — `src/sync/ingram.c`
   - Token acquisition, refresh, caching
   - Automatic retry on 401

2. **HTTP Client with Rate Limiting** — `src/net/http.c`
   - TLS 1.2/1.3 via mbedTLS
   - Exponential backoff
   - Request/response logging

3. **INI Config Parser** — `src/net/config.h`
   - Config file parsing
   - Environment variable override
   - Secure credential handling

4. **SQLite Database Layer** — `src/db/database.c`
   - SSOT product schema
   - Margin analysis views
   - Audit logging

### Tests

| Test File | Coverage |
|-----------|----------|
| `tests/test_ingram.c` | Ingram API integration tests |
| `tests/test_http.c` | HTTP client tests |
| `tests/test_database.c` | Database operations |
| `tests/test_basket_po.c` | Basket & PO generation |
| `tests/test_search.c` | Product search |

### Build System

```bash
make cosmo          # CLI-only APE binary
make cosmo-gui      # Full GUI APE
make cosmo-full     # CLI + Ingram sync APE
make native         # Native dev build
make test           # Run tests
```

---

## 2. Computer Store Platform (SECONDARY)

**Location:** `C:\dev\computerstore-platform\`
**Language:** Python with FastAPI
**Purpose:** Reads from MHI procurement SQLite DB, syncs to PostgreSQL

### Key Procurement Files

| File | Description |
|------|-------------|
| `backend/app/integrations/procurement.py` | ProcurementService class — reads from MHI SQLite DB |
| `backend/app/api/routes/procurement.py` | FastAPI routes for procurement sync |
| `backend/alembic/versions/005_add_procurement_fields.py` | DB migration for procurement fields |
| `backend/tests/test_procurement.py` | Procurement sync tests |

### ProcurementService Capabilities

```python
class ProcurementService:
    """Service for syncing products from the MHI Procurement Engine."""
    
    def get_procurement_products()    # Fetch products with margin analysis
    def get_procurement_stats()       # Stats (counts, suppliers, categories)
    def sync_product()                # Sync single product to store DB
    def sync_all()                    # Full sync with dry-run support
    def sync_single()                 # Sync by procurement product ID
    def get_status()                  # Sync status and last sync time
```

### API Endpoints

- `POST /procurement/sync` — Full sync from procurement DB
- `GET /procurement/status` — Sync status and stats
- `GET /procurement/preview` — Dry-run preview
- `POST /procurement/sync/{product_id}` — Single product sync

---

## 3. Credentials & Config Locations

### Located Config Files

| Location | Purpose | Contains Credentials |
|----------|---------|---------------------|
| `C:\mhi-procurement\config.example.ini` | Template config | NO (placeholders) |
| `C:\mhi-procurement\src\net\config.h` | Config management code | NO (structure only) |

### Credential Storage Pattern

All credentials should be stored via:
1. **Environment variables** (recommended) — e.g., `MHI_INGRAM_CLIENT_ID`
2. **Config file** with chmod 600 — `config.ini` (not committed)

**NO credentials found committed to the codebase** ✅

---

## 4. Vendored Dependencies

### C:\mhi-procurement\vendor\

| Vendor | Purpose | Version/Notes |
|--------|---------|---------------|
| `cosmocc/` | Cosmopolitan C compiler | Cross-platform APE builds |
| `sqlite/` | SQLite amalgamation | `sqlite3.c`, `sqlite3.h` |
| `sokol/` | Sokol headers | App/GFX/Audio for GUI |
| `cimgui/` | CImGui + Dear ImGui | Immediate mode GUI |

---

## 5. Market Price APIs (Configured but not fully implemented)

From `config.example.ini`:

| Service | Purpose | Rate Limit |
|---------|---------|------------|
| Best Buy API | Market reference prices | 300 rpm |
| eBay Browse API | Market reference prices | 3 rpm |
| Icecat | Product enrichment (25.8M+ items) | 60 rpm |

---

## 6. Zoho Integration

**Status:** NOT FOUND in local filesystem

No Zoho CRM or Zoho Books integration code was found. This would need to be developed from scratch if required.

---

## 7. Recommendations

### Reusable from C:\mhi-procurement\

1. **Ingram Micro OAuth2 + API client** — Already complete, production-tested
2. **Config management pattern** — Env var override, secure handling
3. **HTTP client with rate limiting** — Exponential backoff, TLS
4. **Database schema** — SSOT product/offering/margin analysis

### To Be Developed

1. **TD SYNNEX API client** — Digital Bridge (account ready)
2. **D&H API client** — OAS3 REST (account ready)
3. **Zoho CRM/Books integration** — Not found, needs development

### Integration Approach

The `computerstore-platform` already syncs FROM the MHI procurement SQLite DB.  
New distributor integrations should be added to `C:\mhi-procurement\src\sync\` following the `ingram.c` pattern.

---

## 8. File Paths Quick Reference

```
C:\mhi-procurement\
├── src\
│   ├── sync\ingram.c          # Ingram API (COMPLETE)
│   ├── net\http.c             # HTTP client
│   ├── net\config.h           # Config management
│   ├── db\database.c          # SQLite SSOT
│   ├── main.c                 # CLI
│   └── ui\gui.c               # CImGui GUI
├── tests\
│   ├── test_ingram.c
│   ├── test_http.c
│   └── test_database.c
├── config.example.ini         # Config template
├── README.md                  # Docs
└── vendor\                    # Dependencies

C:\dev\computerstore-platform\backend\
├── app\integrations\procurement.py   # Reads MHI SQLite DB
├── app\api\routes\procurement.py     # FastAPI routes
└── tests\test_procurement.py
```

---

*Generated by localsearch agent on 2026-02-09*
