# Distributor API Research for MHI Procurement App

**Research Date:** 2026-02-09  
**Purpose:** Document available APIs for multi-distributor pricing aggregation

---

## 1. Ingram Micro REST API (Xvantage Integration - XI)

### Overview
Ingram Micro's **Xvantage Integration (XI)** provides comprehensive REST APIs for resellers to connect and consume Xvantage data. This is their most well-documented and modern API offering.

### Developer Resources
- **Developer Portal:** https://developer.ingrammicro.com
- **API Documentation:** https://developer.ingrammicro.com/reseller/api-documentation
- **OpenAPI Spec:** https://github.com/ingrammicro-xvantage/xi-sdk-openapispec
- **Getting Started:** https://developer.ingrammicro.com/reseller/getting-started/api-overview

### Endpoints

| Environment | Base URL |
|-------------|----------|
| **Sandbox** | `https://api.ingrammicro.com:443/sandbox/` |
| **Production** | `https://api.ingrammicro.com:443/` |

### Authentication
- **Method:** OAuth 2.0
- **Endpoint:** `GET https://api.ingrammicro.com:443/oauth/oauth20/token`

### Key APIs for Procurement

#### Product Catalog APIs
| API | Method | Endpoint |
|-----|--------|----------|
| **Price and Availability (PNA)** | POST | `/resellers/v6/catalog/priceandavailability` |
| **Search Products** | GET | `/resellers/v6/catalog` |
| **Product Details** | GET | `/resellers/v6/catalog/details/{ingramPartNumber}` |

#### Order Management APIs
| API | Method | Endpoint |
|-----|--------|----------|
| Create Order | POST | `/resellers/v6/orders` |
| Create Order V7 | POST | `/resellers/v7/orders` |
| Modify Order | PUT | `/resellers/v6/orders/{orderNumber}` |
| Get Order Details | GET | `/resellers/v6.1/orders/{ordernumber}` |
| Search Orders | GET | `/resellers/v6/orders/search` |
| Cancel Orders | DELETE | `/resellers/v6/orders/{OrderNumber}` |

#### Additional APIs
- **Quotes:** Search, Details, Validation
- **Invoices:** Search, Details
- **Renewals:** Search, Details
- **Deals:** Search, Details
- **Returns:** Search, Details, Create
- **Freight Estimate:** POST `/resellers/v6/freightestimate`

### Webhooks
- **Order Status:** `/resellers/v1/webhooks/orderstatusevent`
- **Stock Update:** `/resellers/v1/webhooks/availabilityupdate`

### Official SDKs Available
| Language | Package |
|----------|---------|
| C# | `Install-Package xi.sdk.resellers` (NuGet) |
| Java | GitHub: xi-sdk-resellers-java |
| Node.js | `npm i xi_sdk_resellers` |
| Python | `pip install xi.sdk.resellers` |
| Go | `github.com/ingrammicro-xvantage/xi-sdk-resellers-go` |

### Integration Notes
- Well-documented with OpenAPI specifications
- Multiple official SDKs reduce development time
- Sandbox environment available for testing
- Webhooks for real-time inventory updates
- **Best documented** of all distributors researched

---

## 2. TD SYNNEX API Integration

### Overview
TD SYNNEX (formed from SYNNEX + Tech Data merger) offers integration through their **Digital Bridge** platform and **XMLconnect** services.

### Known Integration Services
From the TD SYNNEX website navigation:
- **Digital Bridge** - Their digital integration platform
- **B2B Connectivity** - Business-to-business integration
- **StreamOne Ion** - Cloud services platform

### Identified Services Menu
- Digital Bridge
- Atlas (appears to be a portal)
- B2B Connectivity
- Strategic Procurement

### Integration Challenges
- **No public API documentation found** via standard URL patterns
- API access appears to require partner registration
- Legacy "XMLconnect" may still be in use (XML-based, not REST)
- Documentation likely behind partner portal authentication

### Recommended Next Steps
1. Contact TD SYNNEX partner support for API access
2. Register at PartnerFirst portal: https://www.tdsynnex.com (PartnerFirst links)
3. Request Digital Bridge API documentation
4. Inquire about StreamOne Ion API for cloud services

### Known Platform Capabilities
- Solutions Aggregation
- Global Sales Solutions
- Renewals management
- Strategic Procurement services

---

## 3. D&H Distributing API

### Overview
D&H is a leading technology distributor serving SMB and Consumer markets in North America.

### Current Status
- **No public API documentation discovered**
- API integration pages return 404 errors
- Integration likely requires direct partner engagement

### Company Information
- D&H is 100% employee-owned (ESOP)
- Serves resellers and retailers across North America
- Has Canadian subsidiary: https://www.dandh.ca

### Integration Path
D&H is listed as an integration partner for **ConnectWise CPQ**, suggesting they have:
- E-commerce/procurement API
- Pricing feed integration
- Order placement capability

### Recommended Next Steps
1. Contact D&H partner development team
2. Inquire about API access for existing reseller accounts
3. May require minimum volume or specific partner tier
4. Check if ConnectWise CPQ integration documentation reveals D&H API specs

---

## 4. ConnectWise CPQ (Sell)

### Overview
ConnectWise CPQ is a Configure-Price-Quote solution designed for MSPs that includes **multi-distributor pricing integration**.

### Key Features Relevant to Procurement

#### Multi-Distributor Integration
- **Pull and compare pricing from multiple distribution partners**
- Real-time pricing integrations
- Integrates with: BlueStar, D&H, and likely others

#### Procurement Automation
From ConnectWise documentation:
- Quote templates and automated workflows
- Third-party integrations to reduce manual entry
- Online quote delivery with e-signature
- Place e-orders through preferred distributors
- Automated opportunity conversions (with ConnectWise PSA)

#### Additional Features
- Renewal reminders (warranties, agreements)
- Pricing rules to lock down discounts
- Customer catalogs integration
- Proposal building automation

### Platform Integration
- Integrates with ConnectWise PSA
- CRM integrations available
- Tax software integrations
- Leasing company integrations

### Consideration for Custom Build
ConnectWise CPQ already solves multi-distributor pricing aggregation. Options:
1. **Use ConnectWise CPQ directly** if acceptable
2. **Study their integration patterns** as a model
3. **Build custom solution** if ConnectWise licensing/workflow doesn't fit

---

## 5. Procurement Aggregation Platforms

### Pax8

#### Overview
Pax8 is a **cloud marketplace platform** for MSPs - focused primarily on SaaS/cloud subscription products rather than hardware.

#### Platform Capabilities
- 40,000+ partners
- Marketplace with 70%+ of vendors using AI
- PSA and billing integrations
- Custom product support (can add non-Pax8 items)
- Solutions Builder for bundling

#### API/Integration Features
- **Integrations Hub** with pre-built and custom integrations
- **MCP (Model Context Protocol)** - New standard for AI agent integration
- Automated provisioning
- Billing and invoicing automation
- Opportunity Explorer (AI-driven sales insights)

#### Relevance
- **Not ideal for hardware procurement** - focused on cloud/SaaS
- Good model for marketplace/aggregation UX
- May be useful for cloud services portion of MSP procurement

### NIQ Brandbank (formerly Etilize)

#### Overview
Now part of **NielsenIQ**, provides standardized product data catalogs for 20+ million technology products worldwide.

#### Services
- Product data catalogs
- Product images and marketing text
- Product specifications
- Merchandising information
- Rich media content

#### Notable Clients
- **Ingram Micro** - Uses for reseller product content
- NewEgg
- S.P. Richards
- Acer, Vertiv

#### Relevance
- **Product content enrichment** rather than pricing
- Could supplement distributor APIs with product data
- Useful for product matching across distributors (via SKU/UPC normalization)

### IQ Metrix

#### Overview
IQ Metrix is focused on **telecom retail** - not relevant for general IT distribution procurement.

#### Capabilities (for reference)
- POS for wireless retail
- Device activation
- Inventory management
- B2B integrations

**Not recommended** for IT hardware procurement - too telecom-specific.

---

## 6. Summary & Recommendations

### API Maturity Rankings

| Distributor | API Maturity | Documentation | SDK Support |
|-------------|--------------|---------------|-------------|
| **Ingram Micro** | ⭐⭐⭐⭐⭐ | Excellent (Public OpenAPI) | Official SDKs (5 languages) |
| **TD SYNNEX** | ⭐⭐⭐ | Unknown (Behind portal) | Unknown |
| **D&H** | ⭐⭐ | None public | None known |

### Recommended Integration Approach

#### Phase 1: Ingram Micro First
- Best documented, official SDKs available
- Use their Price & Availability API as the baseline
- Sandbox available for development

#### Phase 2: TD SYNNEX
- Requires partner relationship to access docs
- May need to implement XMLconnect (legacy) or Digital Bridge
- Higher integration effort expected

#### Phase 3: D&H
- Explore ConnectWise CPQ documentation for hints
- Contact partner development directly
- May be simpler API than expected once access granted

### Alternative Considerations

1. **ConnectWise CPQ** - Already aggregates multi-distributor pricing
   - Consider using rather than building
   - If building custom, study their patterns

2. **NIQ Brandbank** - For product data enrichment
   - Cross-reference products across distributors
   - Normalize SKUs and product information

3. **Build Product Matching Layer**
   - Map Ingram Part # ↔ D&H SKU ↔ TD SYNNEX SKU
   - Use manufacturer part numbers as common key
   - NIQ Brandbank data could help

### Next Steps for Development

1. ✅ Register at Ingram Micro Developer Portal
2. ✅ Obtain sandbox API credentials
3. 🔲 Contact TD SYNNEX for Digital Bridge access
4. 🔲 Contact D&H partner development
5. 🔲 Build unified pricing service layer
6. 🔲 Create SKU/product matching database
7. 🔲 Implement price comparison logic

---

## Appendix: Key URLs

### Ingram Micro
- Developer Portal: https://developer.ingrammicro.com
- GitHub SDKs: https://github.com/ingrammicro-xvantage
- API Base (Prod): https://api.ingrammicro.com:443/

### TD SYNNEX
- Main Site: https://www.tdsynnex.com/na/us/
- PartnerFirst Portal: (requires registration)

### D&H
- Main Site: https://www.dandh.com
- Canada: https://www.dandh.ca

### ConnectWise
- CPQ Product: https://www.connectwise.com/platform/cpq

### Product Data
- NIQ Brandbank: https://nielseniq.com/global/en/landing-page/technology-product-content-solutions/

### Cloud Marketplace (Reference)
- Pax8: https://www.pax8.com/en-us/marketplace/
