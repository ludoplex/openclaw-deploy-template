# MHI Procurement Codebase Analysis

**Generated:** February 15, 2026 at 3:30 AM MT
**Path:** `C:\mhi-procurement`

## Overview

Cross-platform procurement tool built with Cosmopolitan Libc. Single APE binary runs on Windows, Linux, macOS, FreeBSD.

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
└─────────────────────────────────────────┘
```

## Source Files (by component)

### Core
| File | Size | Purpose |
|------|------|---------|
| `src/main.c` | 26KB | CLI entry point, command handling |
| `src/gui_main.c` | 1.8KB | GUI entry point |
| `src/gui_interface.h` | 18KB | GUI interface definitions |

### Database Layer
| File | Size | Purpose |
|------|------|---------|
| `src/db/database.c` | 27KB | SQLite operations, SSOT |
| `src/db/database.h` | 6KB | Database API |
| `src/db/schema_sql.h` | 8KB | Embedded SQL schema |

### HTTP/Network
| File | Size | Purpose |
|------|------|---------|
| `src/net/http.c` | 49KB | HTTP client (mbedTLS) |
| `src/net/http.h` | 11KB | HTTP API |
| `src/net/config.h` | 23KB | Configuration parsing |

### Supplier Modules
| File | Size | Status | Notes |
|------|------|--------|-------|
| `src/sync/ingram.c` | 33KB | ✅ Working | OAuth2, REST v6 |
| `src/sync/ingram.h` | 1.5KB | ✅ Working | Account #50-135152-000 |
| `src/sync/synnex.c` | 22KB | ❌ Needs creds | Digital Bridge API |
| `src/sync/synnex.h` | 1.7KB | ❌ Needs creds | Account #786379 |
| `src/sync/dandh.c` | 19KB | ❌ Needs creds | REST OAS3 |
| `src/sync/dandh.h` | 1.5KB | ❌ Needs creds | Account #3270340000 |
| `src/sync/market.h` | 2KB | ⚠️ Partial | Best Buy, eBay |

### GUI
| File | Size | Purpose |
|------|------|---------|
| `src/ui/gui.c` | 22KB | ImGui implementation |
| `src/ui/sokol_imgui_impl.c` | 0.8KB | Sokol+ImGui bridge |

**Total Source:** ~273KB of C code

## API Credential Status (from config.ini)

| Supplier | Credentials | Status |
|----------|-------------|--------|
| **Ingram Micro** | `client_id`, `client_secret`, `secret_key` | ✅ Sandbox working |
| **Mouser** | `search_api_key`, `order_api_key` | ✅ Search active |
| **Element14** | `api_key` | ✅ Active |
| **Climb** | `username`, `password`, `account_num` | ✅ Portal login |
| **TD SYNNEX** | Empty | ❌ Request sent to mikko.dizon@tdsynnex.com |
| **D&H** | Empty | ❌ Request sent to RISmith@dandh.com |
| **Best Buy** | Empty | ❌ Need to register |
| **eBay** | Empty | ❌ Need to register |
| **Icecat** | Empty | ❌ Need to register (free) |

## Compiled Binary

- **File:** `mhi-procurement.com`
- **Size:** 5.4MB (APE format)
- **Database:** `procurement.db` (98KB SQLite)

## Build Targets

```bash
make cosmo       # CLI-only APE
make cosmo-gui   # Full GUI APE (recommended)
make cosmo-full  # CLI + supplier sync APE
make native      # Native CLI (dev)
make native-gui  # Native GUI (dev)
```

## Current State

**Working:**
- Core database operations
- Ingram Micro API (sandbox)
- CLI interface
- GUI framework (Sokol + CImGui)

**Blocked on credentials:**
- TD SYNNEX Digital Bridge API
- D&H REST API
- Best Buy API
- eBay Browse API

**Next Steps:**
1. Follow up on D&H/TD SYNNEX API requests if no response in 48h
2. Register for Best Buy API (free)
3. Register for eBay developer account
4. Register for Icecat (free product enrichment)
5. Test Ingram Micro production API (currently sandbox)

## Key Observations

1. **Well-architected:** Clean separation between database, HTTP, and supplier modules
2. **Cosmopolitan-first:** True single-binary philosophy, all deps vendored
3. **OAuth2 implementation:** Ingram module shows proper token refresh pattern
4. **GUI ready:** Sokol + CImGui compiled in, just needs supplier data to be useful
5. **Database schema:** SQLite SSOT with products, prices, suppliers tables
