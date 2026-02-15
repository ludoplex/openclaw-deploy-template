# Supplier API Signup Guide

**Account:** vincentlanderson@mightyhouseinc.com

## 1. TD SYNNEX (Priority: HIGH)
**Status:** Have account #786379, need API credentials

**Portal:** https://developer.tdsynnex.com/
**Steps:**
1. Log in with TD SYNNEX reseller credentials
2. Navigate to Developer Portal
3. Create new application
4. Request "EC (eCommerce)" API access
5. Note: May require approval (1-3 business days)

**APIs Needed:**
- Product Catalog
- Pricing/Availability
- Order API (later)

---

## 2. D&H Distributing (Priority: HIGH)
**Status:** Have account #3270340000, need API credentials

**Portal:** https://www.dandh.com/
**Steps:**
1. Log in to D&H dealer portal
2. Go to "My Account" → "API Access"
3. Request API key
4. They use OAS3 (OpenAPI 3.0) REST API

**Documentation:** https://api.dandh.com/docs

---

## 3. Best Buy (Priority: MEDIUM)
**Purpose:** Market price reference

**Portal:** https://bestbuyapis.github.io/api-reference/
**Steps:**
1. Create developer account
2. Register application
3. Get API key (instant)
4. Free tier: 5 req/sec

---

## 4. eBay Browse API (Priority: MEDIUM)
**Purpose:** Market price reference

**Portal:** https://developer.ebay.com/
**Steps:**
1. Create developer account (can use existing eBay account)
2. Create application in Developer Program
3. Get OAuth credentials
4. Request Browse API access

**Note:** 5000 calls/day on free tier

---

## 5. Icecat (Priority: LOW)
**Purpose:** Product enrichment (specs, images)

**Portal:** https://icecat.biz/
**Steps:**
1. Register for free Open Icecat account
2. Get username (password is same as Open Icecat)
3. Access 25.8M+ product datasheets

---

## Already Have Credentials ✅

| Supplier | Account | Status |
|----------|---------|--------|
| Ingram Micro | #50-135152-000 | Sandbox working, prod in review |
| Mouser | vincentlanderson@mightyhouseinc.com | Search API active |
| Element14/Farnell | mhi_vincenta | Active |
| Climb Channel | CU0043054170 | Portal login only |

---

## Config Location
`C:\mhi-procurement\config.ini`

After getting credentials, add them to the appropriate sections.
