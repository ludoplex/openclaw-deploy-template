# Distributor API Research — Specialist Report

**Generated:** 2026-02-09 21:45 MST  
**Task:** Research distributor API documentation for TD SYNNEX, D&H, and Ingram Micro

---

## 1. Ingram Micro Xvantage API (v6/v6.1/v7)

### Overview
Ingram Micro has the **most mature public API offering** among the three distributors. Their Xvantage Integration (XI) platform exposes comprehensive RESTful APIs with full OpenAPI 3.0 specifications, official SDKs, and public documentation.

### Authentication
- **Method:** OAuth 2.0 (Client Credentials flow)
- **Endpoint:** `GET https://api.ingrammicro.com:443/oauth/oauth20/token`
- **Parameters:** `grant_type=client_credentials`, `client_id`, `client_secret`
- **Scopes:** `read`, `write`

### Base URLs
- **Production:** `https://api.ingrammicro.com:443`
- **Sandbox:** `https://api.ingrammicro.com:443/sandbox/`

### Full Endpoint List (v6/v6.1/v7)

| Category | Endpoint | Method | Path | Description |
|----------|----------|--------|------|-------------|
| **Auth** | Get Access Token | GET | `/oauth/oauth20/token` | OAuth2 token generation |
| **Product Catalog** | Price & Availability | POST | `/resellers/v6/catalog/priceandavailability` | Real-time pricing/stock |
| **Product Catalog** | Search Products | GET | `/resellers/v6/catalog` | Product search |
| **Product Catalog** | Product Details (by IPN) | GET | `/resellers/v6/catalog/details/{ingramPartNumber}` | Single product details |
| **Product Catalog** | Product Details (CMP) | GET | `/resellers/v6/catalog/details` | Product details (alt) |
| **Orders** | Create Order v6 | POST | `/resellers/v6/orders` | Place order |
| **Orders** | Create Order v7 | POST | `/resellers/v7/orders` | Place order (newer) |
| **Orders** | Modify Order | PUT | `/resellers/v6/orders/{orderNumber}` | Update existing order |
| **Orders** | Get Order Details v6.1 | GET | `/resellers/v6.1/orders/{ordernumber}` | Retrieve order |
| **Orders** | Search Orders | GET | `/resellers/v6/orders/search` | Order search |
| **Orders** | Cancel Order | DELETE | `/resellers/v6/orders/{OrderNumber}` | Cancel order |
| **Quotes** | Quote Search | GET | `/resellers/v6/quotes/search` | Search quotes |
| **Quotes** | Quote Details | GET | `/resellers/v6/quotes/{quoteNumber}` | Get quote |
| **Quotes** | Validate Quote | GET | `/resellers/v6/q2o/validatequote` | Quote validation |
| **Invoices** | Search Invoices | GET | `/resellers/v6/invoices/` | Invoice search |
| **Invoices** | Invoice Details v6.1 | GET | `/resellers/v6.1/invoices/{invoiceNumber}` | Get invoice |
| **Renewals** | Renewals Search | POST | `/resellers/v6/renewals/search` | Search renewals |
| **Renewals** | Renewals Details | GET | `/resellers/v6/renewals/{renewalId}` | Get renewal |
| **Deals** | Deals Search | GET | `/resellers/v6/deals/search` | Search deals |
| **Deals** | Deals Details | GET | `/resellers/v6/deals/{dealId}` | Get deal |
| **Returns** | Returns Search | GET | `/resellers/v6/returns/search` | Search returns |
| **Returns** | Returns Details | GET | `/resellers/v6/returns/{caseRequestNumber}` | Get return |
| **Returns** | Create Return | POST | `/resellers/v6/returns/create` | Initiate RMA |
| **Freight** | Freight Estimate | POST | `/resellers/v6/freightestimate` | Shipping cost estimate |
| **Webhooks** | Order Status | POST | `/resellers/v1/webhooks/orderstatusevent` | Order status notifications |
| **Webhooks** | Stock Update | POST | `/resellers/v1/webhooks/availabilityupdate` | Inventory updates |

### Rate Limits
- Not explicitly documented in public materials
- Contact: xi_support@ingrammicro.com for rate limit details

### TypeScript/JavaScript SDK
- **Package:** `xi_sdk_resellers`
- **npm:** `npm install xi_sdk_resellers`
- **GitHub:** https://github.com/ingrammicro-xvantage/xi-sdk-resellers-node
- **Status:** ✅ Official, actively maintained (updated Nov 2025)

### Additional SDKs Available
| Language | Package | Installation |
|----------|---------|--------------|
| Python | `xi.sdk.resellers` | `pip install xi.sdk.resellers` |
| C# | `xi.sdk.resellers` | `Install-Package xi.sdk.resellers` |
| Java | GitHub only | Maven/Gradle from GitHub |
| Go | GitHub only | `go get github.com/ingrammicro-xvantage/xi-sdk-resellers-go` |

### Key Resources
- **Developer Portal:** https://developer.ingrammicro.com
- **OpenAPI Spec:** https://github.com/ingrammicro-xvantage/xi-sdk-openapispec
- **Postman Collection:** Available in openapispec repo
- **Support:** xi_support@ingrammicro.com

---

## 2. TD SYNNEX Digital Bridge API

### Overview
TD SYNNEX offers B2B connectivity solutions through their **Digital Bridge** platform, accessible via their eSolutions portal. Public API documentation is **not available** — requires partner login through ECExpress.

### Authentication
- **Method:** Partner credentials (ECExpress account required)
- **Portal:** https://ec.synnex.com/ecx/
- **eSolutions Page:** https://www.tdsynnex.com/na/esolutions/ (requires login)

### Known API Gateway
- **URL:** `api.synnex.com` (confirmed active, IP-restricted)
- **Error Response Format:** JSON with `requestId`, `errorCode`, `errorMessage`
- **Access:** Whitelisted IPs only (external IPs rejected)

### Available Integration Methods (from public materials)
Based on their eSolutions marketing, TD SYNNEX offers:

1. **XML Web Services** — Traditional XML-based API
2. **EDI** — Electronic Data Interchange
3. **eStorefront** — White-label ecommerce

### Suspected Endpoints (based on industry standards)
| Function | Likely Capability |
|----------|-------------------|
| Product Search | SKU/keyword lookup |
| Price & Availability | Real-time pricing/inventory |
| Order Submission | Purchase order creation |
| Order Status | Tracking/status updates |
| Invoice Retrieval | Invoice download |

### Rate Limits
- Unknown (documentation behind login)

### TypeScript/JavaScript SDK
- **Status:** ❌ No public SDK available
- **GitHub (tdsynnex):** Organization exists but has no public repositories

### How to Access
1. Become a TD SYNNEX customer
2. Apply for ECExpress access
3. Contact: HelpdeskUS@tdsynnex.com
4. Phone: 416-240-2900 (M-F 7:30AM-9PM ET)

---

## 3. D&H Distributing REST API

### Overview
D&H Distributing provides integration options for partners, but **no public REST API documentation** is available. API access requires an active D&H partner account.

### Authentication
- **Method:** Unknown (requires partner portal access)
- **Portal:** https://www.dandh.com/v4/view?pageReq=dhMainNS

### Known Integration Options (from public materials)
D&H mentions "Web Services" but specific documentation is behind their partner portal.

### Suspected Capabilities
Based on industry standards and competitor offerings:
| Function | Expected Availability |
|----------|----------------------|
| Product Catalog | Product search, details |
| Pricing | Partner-specific pricing |
| Inventory | Stock availability by warehouse |
| Orders | Order placement, modification |
| Tracking | Shipment tracking |
| Invoices | Invoice retrieval |

### OAS3 Specification
- **Status:** ❌ No public OpenAPI spec found
- No SwaggerHub presence detected
- No public GitHub repositories

### Rate Limits
- Unknown

### TypeScript/JavaScript SDK  
- **Status:** ❌ No public SDK available

### How to Access
1. Sign up as D&H customer: https://www.dandh.com/v4/view?pageReq=NSNewCust
2. Initial purchase requirement: $1,000+ within first 30 days for $100 AMEX bonus
3. Contact D&H support for API access details

---

## Summary Comparison

| Feature | Ingram Micro | TD SYNNEX | D&H |
|---------|--------------|-----------|-----|
| **Public API Docs** | ✅ Excellent | ❌ Login required | ❌ Login required |
| **OpenAPI/OAS3 Spec** | ✅ Full spec on GitHub | ❌ Unknown | ❌ Unknown |
| **Auth Method** | OAuth 2.0 | Unknown | Unknown |
| **Node.js SDK** | ✅ Official npm package | ❌ None | ❌ None |
| **Sandbox/Testing** | ✅ Available | ❓ Unknown | ❓ Unknown |
| **Webhook Support** | ✅ Order status, inventory | ❓ Unknown | ❓ Unknown |
| **Developer Portal** | ✅ developer.ingrammicro.com | ❌ Behind ECExpress | ❌ Behind portal |

---

## Recommendations for MHI Procurement Project

### Immediate Actions
1. **Ingram Micro:** Ready to implement. Install `xi_sdk_resellers` and use OpenAPI spec for type generation
2. **TD SYNNEX:** Request API documentation through ECExpress portal or contact HelpdeskUS@tdsynnex.com
3. **D&H:** Contact D&H support to request REST API documentation and OAS3 spec if available

### Implementation Priority
1. **Start with Ingram Micro** — Full documentation, SDK, sandbox available
2. **TD SYNNEX second** — Larger footprint, worth the onboarding effort
3. **D&H third** — Valuable for SMB/consumer but requires investigation

### SDK Development Strategy
- Use Ingram Micro's official Node.js SDK as reference architecture
- For TD SYNNEX and D&H, plan to build custom clients once specs are obtained
- Consider OpenAPI Generator for type-safe clients once specs are available

---

## Appendix: Ingram Micro Quick Start

```typescript
import * as XiSdkResellers from 'xi_sdk_resellers';

// Get access token
const api = new XiSdkResellers.AccesstokenApi();

api.getAccesstoken(
  'client_credentials',
  process.env.IM_CLIENT_ID,
  process.env.IM_CLIENT_SECRET,
  (error, data, response) => {
    if (error) {
      console.error(error);
    } else {
      console.log('Token:', data.access_token);
    }
  }
);
```

---

*Report generated by specialist-seeker subagent*
