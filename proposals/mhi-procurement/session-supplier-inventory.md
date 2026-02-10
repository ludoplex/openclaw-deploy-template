# MHI Procurement — Session Supplier Inventory

**Generated:** 2026-02-10 00:15 MST  
**Source:** OpenClaw session files, memory logs, and proposal documents  
**Search Agent:** localsearch

---

## 1. Confirmed Supplier Accounts

### Primary Distributors (ACTIVE ACCOUNTS)

| Supplier | Account # | API Status | Implementation |
|----------|-----------|------------|----------------|
| **Ingram Micro** | #50-135152-000 | ✅ REST v6 COMPLETE | `C:\mhi-procurement\src\sync\ingram.c` |
| **TD SYNNEX** | #786379 | ⏳ Digital Bridge API | `C:\mhi-procurement\src\sync\synnex.c` (21KB) |
| **D&H Distributing** | #3270340000 | ⏳ REST OAS3 API | `C:\mhi-procurement\src\sync\dandh.c` (18KB) |
| **Climb Channel Solutions** | #CU0043054170 | ❌ No API | Manual only |

### Developer Portal Credentials

| Portal | Email | Status |
|--------|-------|--------|
| **Ingram Micro Developer Portal** | vincentlanderson@mightyhouseinc.com | Account created, awaiting verification |
| **TD SYNNEX ECExpress** | rachelwilliams@mightyhouseinc.com | Password reset sent |
| **D&H Web Portal** | User ID 3270340000 | Security code sent to Zoho inbox |

---

## 2. API Credentials & Portal URLs

### Ingram Micro (BEST DOCUMENTED)

| Resource | URL |
|----------|-----|
| **Developer Portal** | https://developer.ingrammicro.com |
| **API Documentation** | https://developer.ingrammicro.com/reseller/api-documentation |
| **OpenAPI Spec** | https://github.com/ingrammicro-xvantage/xi-sdk-openapispec |
| **Sandbox Base URL** | `https://api.ingrammicro.com:443/sandbox/` |
| **Production Base URL** | `https://api.ingrammicro.com:443/` |
| **OAuth Endpoint** | `GET https://api.ingrammicro.com:443/oauth/oauth20/token` |

**Environment Variables:**
- `MHI_INGRAM_CLIENT_ID`
- `MHI_INGRAM_CLIENT_SECRET`

### TD SYNNEX

| Resource | URL |
|----------|-----|
| **Main Site** | https://www.tdsynnex.com/na/us/ |
| **PartnerFirst Portal** | Requires partner registration |

**Environment Variables:**
- `MHI_SYNNEX_CLIENT_ID`
- `MHI_SYNNEX_CLIENT_SECRET`

### D&H Distributing

| Resource | URL |
|----------|-----|
| **Main Site** | https://www.dandh.com |
| **Canada Site** | https://www.dandh.ca |

**Environment Variables:**
- `MHI_DANDH_API_KEY`

---

## 3. Product Enrichment APIs

### IceCat (FREE TIER AVAILABLE)

| Resource | URL |
|----------|-----|
| **Registration** | https://icecat.biz/registration |
| **Product Database** | 20M+ products (Open Icecat tier) |
| **Rate Limit** | 60 requests/minute |

**Environment Variable:** `MHI_ICECAT_USERNAME`

### NIQ Brandbank (Formerly Etilize)

- Enterprise/paid only — **SKIP for now**
- Used by Ingram Micro for reseller product content
- Contact: https://nielseniq.com/global/en/landing-page/technology-product-content-solutions/

---

## 4. Market Reference Price APIs

| Service | Purpose | Rate Limit | Env Variable |
|---------|---------|------------|--------------|
| **Best Buy API** | Market reference prices | 300 rpm | `MHI_BESTBUY_API_KEY` |
| **eBay Browse API** | Market reference prices | 3 rpm | `MHI_EBAY_CLIENT_ID`, `MHI_EBAY_CLIENT_SECRET` |

---

## 5. Sales Channels (Identified but NOT Implemented)

### References Found in Sessions

| Channel | Status | Notes |
|---------|--------|-------|
| **Amazon** | Referenced | Folder in documents: `amazon` |
| **eBay** | API ready | eBay Browse API configured in config.example.ini |
| **Newegg** | Mentioned | No implementation found |
| **Best Buy** | API ready | Best Buy API configured in config.example.ini |

---

## 6. Suppliers Under Investigation

### Mentioned but No Accounts Confirmed

| Supplier | Type | Notes |
|----------|------|-------|
| **VEX Robotics** | Robotics/STEM | "V" robotics company Vincent mentioned |
| **ASI (Advertising Specialty Institute)** | Promo products | Promotional merchandise supplier |
| **ASI Computer Technologies** | IT Distribution | Different company, same acronym as above |
| **Grainger** | Industrial supply | Not found in sessions |
| **PCBWay** | PCB manufacturing | Not found in sessions |
| **MA Labs** | IT Distribution | Not found in sessions |
| **Quill** | Office supplies | Not found in sessions |

---

## 7. Partnership Agreements & LoAs

### IBM/Climb Channel Partnership

| Item | Location |
|------|----------|
| **Agent** | `climbibm` agent configured in OpenClaw |
| **Account** | Climb #CU0043054170 |
| **Status** | Active partner (no API) |

### OEM Relationships

From session 2026-02-08:
> redundant-project-checker — Authorized seller applications inventory (Ingram, TD SYNNEX, D&H, OEMs, cloud)

**OEM seller applications** referenced but no specific documents found.

---

## 8. Cloud Services (Not Procurement)

### Zoho API Access (CONFIRMED)

| Account | Client ID | Status |
|---------|-----------|--------|
| Rachel Williams (Boss) | `1000.1B2SG47NUYWWRRHAW4FSS8D96MWGUU` | ✅ Active |
| Vincent Landerson | Configured in accounts.json | ✅ Active |

**Scopes:** ZohoCRM.modules.ALL, ZohoBooks.invoices.ALL, ZohoInventory.FullAccess.all, ZohoMail.messages.ALL

### Google Drive (Connected)

| Item | Value |
|------|-------|
| **Project** | cursor ide google drive (sound-sanctuary-481205-n2) |
| **Client ID** | `980515471840-4rv59vqclogue19di0v8sqsta1t13cs0.apps.googleusercontent.com` |
| **Remote** | gdrive-theander (rclone) |

---

## 9. Existing Implementation Files

### MHI Procurement Engine

| File | Size | Description |
|------|------|-------------|
| `C:\mhi-procurement\src\sync\ingram.c` | 32KB | Ingram Micro REST v6 (COMPLETE) |
| `C:\mhi-procurement\src\sync\ingram.h` | - | Header file |
| `C:\mhi-procurement\src\sync\synnex.c` | 21KB | TD SYNNEX OAuth2 (implemented, needs testing) |
| `C:\mhi-procurement\src\sync\synnex.h` | - | Header file |
| `C:\mhi-procurement\src\sync\dandh.c` | 18KB | D&H REST API key auth (implemented, needs testing) |
| `C:\mhi-procurement\src\sync\dandh.h` | - | Header file |
| `C:\mhi-procurement\src\net\http.c` | 48KB | HTTP client with TLS, rate limiting |
| `C:\mhi-procurement\src\db\database.c` | 27KB | SQLite SSOT database |
| `C:\mhi-procurement\config.example.ini` | - | Config template (NO credentials) |

### Commit History

- `2e2eeb2` — "Add D&H and TD SYNNEX API integrations" (2026-02-09)

---

## 10. ConnectWise CPQ Reference

**Alternative to custom build:** ConnectWise CPQ already aggregates multi-distributor pricing.

| Resource | URL |
|----------|-----|
| **CPQ Product** | https://www.connectwise.com/platform/cpq |

**Known Integrations:** BlueStar, D&H, others

Consider using ConnectWise CPQ patterns as model if building custom solution.

---

## 11. Action Items

### Immediate (Credential Validation)

1. [ ] Check Zoho inbox for D&H security code
2. [ ] Forward TD SYNNEX password reset from rachelwilliams@mightyhouseinc.com
3. [ ] Verify Ingram Micro Developer Portal email

### Short-term (API Integration)

1. [ ] Test D&H API with real credentials (`make test-dandh`)
2. [ ] Test TD SYNNEX API with real credentials (`make test-synnex`)
3. [ ] Wire up multi-supplier search in GUI

### Medium-term (Expansion)

1. [ ] Register for IceCat FREE tier
2. [ ] Research VEX Robotics partnership options
3. [ ] Evaluate ASI for promotional merchandise

---

## 12. Source Files Searched

| Location | Files Found |
|----------|-------------|
| `C:\Users\user\.openclaw\agents\*\sessions\*.jsonl` | 16 session files |
| `C:\Users\user\.openclaw\workspace\memory\*.md` | 21 memory files |
| `C:\Users\user\.openclaw\workspace\memory\external-sessions\*.md` | 84 external session files |
| `C:\Users\user\.openclaw\workspace\memory\cursor-sessions\*.jsonl` | 70 cursor session files |
| `C:\Users\user\.openclaw\workspace\proposals\mhi-procurement\*.md` | 16 proposal files |

---

*Generated by localsearch subagent on 2026-02-10*
