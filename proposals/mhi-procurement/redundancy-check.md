# MHI Procurement App — Redundancy Check

**Date:** 2026-02-09
**Purpose:** Find existing mature tools before building custom

---

## 1. Commercial CPQ/Quoting Platforms

### ConnectWise CPQ (formerly Sell/Quosal)
- **URL:** connectwise.com/platform/cpq
- **Cost:** ~$75-150/user/month
- **Multi-distributor:** Yes (Ingram, D&H, SYNNEX integrations)
- **Pros:** Full-featured, established, D&H integration confirmed
- **Cons:** Expensive, MSP-focused, heavy ecosystem lock-in
- **Verdict:** ⚠️ POSSIBLE — but overkill and expensive

### QuoteWerks
- **URL:** quotewerks.com
- **Cost:** $15-40/user (perpetual license available)
- **Multi-distributor:** Yes (Ingram, Tech Data, SYNNEX, D&H)
- **Pros:** Cheaper, perpetual option, long history
- **Cons:** Older Windows app, dated UI
- **Verdict:** ⚠️ POSSIBLE — cheap but dated

### Quoter
- **URL:** quoter.com
- **Cost:** $99-299/month
- **Multi-distributor:** Limited
- **Pros:** Modern SaaS, simple
- **Cons:** Fewer distributor integrations
- **Verdict:** ❌ NOT SUITABLE — missing key integrations

### Zomentum
- **URL:** zomentum.com
- **Cost:** $99-199/user/month
- **Multi-distributor:** Some
- **Pros:** Modern, proposal-focused
- **Cons:** Limited distributor pricing integration
- **Verdict:** ❌ NOT SUITABLE — not procurement focused

---

## 2. Distributor-Provided Tools

### Ingram Micro Cloud Blue
- **What:** Ingram's own marketplace/platform
- **Pros:** Free, direct pricing
- **Cons:** Only Ingram products
- **Verdict:** ❌ Single-source only

### TD SYNNEX StreamOne
- **What:** SYNNEX cloud marketplace
- **Pros:** Direct access
- **Cons:** Only SYNNEX
- **Verdict:** ❌ Single-source only

### D&H Direct Portal
- **What:** D&H's ordering system
- **Pros:** Real-time pricing
- **Cons:** Only D&H
- **Verdict:** ❌ Single-source only

---

## 3. Aggregation/Data Services

### Etilize (now NIQ Brandbank)
- **What:** Product content/data for 20M+ tech products
- **Pros:** Comprehensive specs, images
- **Cons:** Content only, no pricing
- **Verdict:** ❌ NOT FOR PRICING — but useful for product data

### IceCat
- **What:** Open product catalog
- **Pros:** Free tier available
- **Cons:** No pricing
- **Verdict:** ❌ NOT FOR PRICING

### ScanSource/Intelisys
- **What:** Telecom/cloud distributor aggregation
- **Cons:** Wrong vertical (telecom, not IT hardware)
- **Verdict:** ❌ WRONG MARKET

---

## 4. Open Source Options

### ERPNext
- **URL:** erpnext.com
- **What:** Full ERP with procurement module
- **Pros:** Free, comprehensive
- **Cons:** Massive overkill, no distributor integrations
- **Verdict:** ❌ OVERKILL

### Odoo
- **What:** ERP with purchase module
- **Pros:** Modular, good UI
- **Cons:** No IT distributor integrations built-in
- **Verdict:** ⚠️ POSSIBLE BASE — would need custom integrations

### Custom GitHub Projects
- Searched for: "ingram micro api" "distributor pricing comparison"
- **Result:** No mature open source projects found
- **Verdict:** ❌ NOTHING EXISTS

---

## 5. Browser Extensions/Automation

### Existing Extensions
- No known extensions for cross-distributor price comparison
- Some generic price comparison tools (Honey, etc.) don't work for B2B portals

### Potential Approach
- Tampermonkey script to scrape portal pricing
- Could work for Climb (no API)
- **Verdict:** ⚠️ VIABLE FOR CLIMB — not primary solution

---

## 6. Summary Matrix

| Solution | Cost | Multi-Dist | Real-time | Multi-Entity | Verdict |
|----------|------|------------|-----------|--------------|---------|
| ConnectWise CPQ | $$$$ | ✅ | ✅ | ❓ | Expensive overkill |
| QuoteWerks | $$ | ✅ | ✅ | ❓ | Dated but functional |
| Quoter | $$$ | ❌ | ❌ | ✅ | Missing integrations |
| Distributor portals | Free | ❌ | ✅ | ✅ | Manual comparison |
| Custom build | $$ | ✅ | ✅ | ✅ | **Best fit** |

---

## 7. Recommendation

### No Perfect Solution Exists

The gap in the market:
- **ConnectWise CPQ** is closest but expensive and MSP-focused
- **QuoteWerks** is cheaper but Windows-only and dated
- **No solution** optimized for small VAR with 3 entities needing margin visibility

### Build Recommendation

**Custom tool is justified because:**
1. No existing tool handles multi-entity cleanly (MHI/DSAIC/Computer Store)
2. Your requirement for "every feature suppliers expose" isn't met by commercial tools
3. You want best margins — existing tools don't optimize for this
4. Cosmopolitan/APE philosophy aligns with portable single-binary approach

### Accelerators Available

Use these to speed up custom build:
- **Ingram Micro API v6:** Well-documented REST API
- **D&H OAS3 spec:** OpenAPI = code generation possible
- **ConnectWise integration patterns:** Study their approach

### MVP Scope
1. Single binary (APE) with embedded web UI
2. Ingram + D&H APIs (both have good REST)
3. SYNNEX if API access granted
4. Climb manual entry (no API)
5. Margin calculator built-in
6. Entity switcher (MHI/DSAIC/Computer Store)

---

*Redundancy check complete. Custom build recommended.*
