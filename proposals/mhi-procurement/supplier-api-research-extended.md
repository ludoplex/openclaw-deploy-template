# Supplier API Research - Extended Suppliers

**Research Date:** 2026-02-10  
**Status:** Initial Research Complete

---

## 1. MA Labs (California Components Distributor)

**Website:** https://www.malabs.com

### API Availability

| Aspect | Status |
|--------|--------|
| REST API | ❌ No public REST API documented |
| SOAP/XML Services | ⚠️ Unknown - requires reseller account |
| EDI | ⚠️ Likely available for established resellers |
| Developer Portal | ❌ Not found |

### Summary

MA Labs is a traditional IT components distributor focused on PC hardware, servers, and consumer electronics. Their website appears to require authentication for most functionality.

**Integration Options:**
- Contact sales for reseller account and integration options
- Traditional EDI may be available for B2B orders
- No public API documentation found

**Contact for API Access:**
- Must establish reseller account first
- Contact via https://www.malabs.com/company/contact

### Recommended Approach

1. Establish reseller relationship
2. Request B2B integration documentation
3. May need to work with traditional EDI or proprietary web portal

---

## 2. Quill (Staples Subsidiary - Office Supplies)

**Website:** https://www.quill.com  
**Parent Company:** Staples Business (https://www.staplesadvantage.com)

### API Availability

| Aspect | Status |
|--------|--------|
| REST API | ❌ No public REST API |
| Punchout Catalog | ✅ Supported via Staples Business |
| EDI | ✅ Available through Staples Business |
| Developer Portal | ❌ Not available |

### Integration Details

Staples Business Advantage (which includes Quill) offers:
- **Punchout Catalog Integration** - Supports 170+ procurement platforms
- **EDI Integration** - For order processing
- **Procurement System Integration** - Coupa, Ariba, SAP, etc.

**Key Finding:** Staples facilitates integration with over 170 purchasing platforms for enterprise customers. This is punchout-based, not a REST API.

### Supported Procurement Platforms (Punchout)
- Coupa
- SAP Ariba
- Oracle Procurement Cloud
- Workday
- Jaggaer
- Most major eProcurement systems

### Registration Process

1. Create Staples Business account at https://www.staplesadvantage.com
2. Contact enterprise sales for B2B integration
3. Request punchout catalog setup for your procurement platform

### SDKs

❌ No SDKs available - integration is via punchout protocols (cXML, OCI)

---

## 3. VEX Robotics (STEM/Robotics Education)

**Website:** https://www.vexrobotics.com (Cloudflare protected)  
**Education Portal:** https://education.vex.com

### API Availability

| Aspect | Status |
|--------|--------|
| E-commerce REST API | ❌ No public API |
| Robot Programming API | ✅ PROS (Open Source) |
| VEXcode API | ✅ C/C++ for robot hardware |
| Developer Portal | ❌ Not for procurement |

### Robot Development APIs (PROS)

While VEX doesn't offer e-commerce APIs, they have excellent programming APIs for their hardware:

**PROS - Open Source VEX V5 Development**
- **Website:** https://pros.cs.purdue.edu
- **GitHub:** https://github.com/purduesigbots/pros
- **Languages:** C/C++ (C23 & C++23 with GNU extensions)
- **Platforms:** Windows, macOS, Linux
- **IDE:** VS Code plugin available

**OkapiLib** (C++ Library for PROS)
- **Docs:** https://okapilib.github.io/OkapiLib
- **Purpose:** High-level robot control abstractions

### PROS API Features
- Motor control (C and C++ APIs)
- Sensor interfaces (Distance, GPS, IMU, Optical, Rotation, Vision)
- ADI (TriPort) interfaces
- RTOS facilities
- VEX Link communication

### Procurement Integration

❌ **No e-commerce or ordering API available**

For bulk purchases and educational accounts:
- Contact VEX Robotics sales directly
- Educational discounts available
- Potential for custom ordering arrangements

### Recommended Approach

1. Contact VEX sales for educational/bulk pricing
2. Request if custom ordering portal or integration is available
3. May require manual ordering or EDI arrangement for large volumes

---

## 4. ASI (Advertising Specialty Institute) - Promotional Products

**Website:** https://asicentral.com  
**ESP Platform:** https://esp.asicentral.com

### API Availability

| Aspect | Status |
|--------|--------|
| REST API | ⚠️ Moving toward REST (see PromoStandards) |
| SOAP Web Services | ✅ PromoStandards compliant |
| SDK | ✅ PHP, C#, Java examples available |
| Developer Portal | ✅ Via PromoStandards membership |
| OpenAPI/Swagger | ❌ Currently SOAP/WSDL based |

### PromoStandards Integration

ASI is a key member of **PromoStandards** - the industry-standard API for promotional products.

**PromoStandards Website:** https://promostandards.org

#### Available Services (SOAP-based)
- **Product Data Service** - Product information and catalogs
- **Product Pricing and Configuration** - Real-time pricing
- **Media Content Service** - Product images and media
- **Inventory Service** - Real-time stock levels
- **Order Status Service** - Track order progress
- **Purchase Order Service** - Submit and manage orders

### Authentication
- **Type:** SOAP WS-Security or basic auth
- **Access:** Requires PromoStandards membership

### Rate Limits
- Not strictly documented
- Reasonable use expected
- Contact PromoStandards for enterprise needs

### SDKs Available

**Official PromoStandards Examples (GitHub):**
- https://github.com/promostandards

| Language | Repository | Purpose |
|----------|------------|---------|
| PHP (Yii) | productDemoPhp | Product, Pricing, Media, Inventory, PO |
| C# | DotNetClients | Product Pricing, Config, Data, Media |
| Java | OrderStatusDemoJava | Order Status |

⚠️ **No official Node.js/TypeScript SDK** - would need to generate from WSDL

### ESP+ Platform Features
- Fast product search
- CRM integration
- Order processing
- Project management
- Live client presentations

### Registration Process

1. **Join PromoStandards:** https://promostandards.org/membership-application/
2. **Access Documentation:** https://promostandards.org/standards-services/
3. **Get Endpoints:** https://promostandards.org/standards-endpoints/
4. **Implement using examples from GitHub**

### Future Direction
- PromoStandards is discussing REST migration
- Currently planning REST alongside SOAP
- Check PromoStandards monthly office hours for updates

---

## 5. ASI Computer Technologies (IT Distributor)

**Note:** This is a DIFFERENT company from ASI (Advertising Specialty Institute)

⚠️ **CLARIFICATION NEEDED:** Multiple companies use "ASI Computer" naming:

### ASI Computer Systems (Promotional Products Software)
**Website:** https://asicomp.com → https://sales.asicomp.com

This company provides **software** for the promotional products industry (partner to ASI Central), NOT IT hardware distribution.

**Products:**
- **ASI SmartBooks** - Business management software
- **ProfitMaker** - Order processing and CRM
- Both integrate with ESP (ASI Central's platform)

**Integration Capabilities:**
| Feature | Status |
|---------|--------|
| EDI Integration | ✅ Full EDI support |
| Punchout Sites | ✅ Integrates with customer procurement |
| REST API | ❌ Not documented publicly |
| eCommerce Integration | ✅ Web store integration |

**Contact:** (800) 544-1274

### If Looking for IT Hardware Distributor

The original request mentioned "ASI Computer Technologies" as an IT distributor separate from ASI Central. 

**Possible entities:**
- May be a regional/local distributor
- Could be using a similar name in different market

**Recommended Action:**
- Clarify the exact company name and website
- Check if this is https://www.asicomputer.com (returns 404 for direct access)
- May need to contact via phone to verify API capabilities

---

## Summary Comparison Table

| Supplier | REST API | EDI | Punchout | SDK | Public Docs |
|----------|----------|-----|----------|-----|-------------|
| MA Labs | ❌ | ⚠️ | ❓ | ❌ | ❌ |
| Quill/Staples | ❌ | ✅ | ✅ (170+) | ❌ | ❌ |
| VEX Robotics | ❌ | ❌ | ❌ | ✅ (PROS) | Hardware only |
| ASI (Promo) | ⚠️ SOAP | ✅ | N/A | ✅ | ✅ PromoStandards |
| ASI Computer Tech | ❌ | ⚠️ | ⚠️ | ❌ | ❌ |

### Legend
- ✅ Available
- ⚠️ Limited/Requires partnership
- ❌ Not available
- ❓ Unknown

---

## Recommendations

### For Modern API Integration

**Best Option:** ASI (Advertising Specialty Institute) via PromoStandards
- Well-documented SOAP services
- Industry standard
- SDK examples available
- Active development community

### For Enterprise Procurement

**Best Option:** Quill/Staples Business
- Punchout catalog integration
- Supports 170+ procurement platforms
- EDI available
- Enterprise-ready

### Requiring Partnership

**MA Labs, VEX Robotics, ASI Computer Technologies:**
- Will require direct contact with sales
- Custom integration arrangements likely needed
- May involve EDI or proprietary portal access

---

## Next Steps

1. **ASI/PromoStandards:** Apply for PromoStandards membership to access API specs
2. **Quill/Staples:** Contact enterprise sales for punchout integration
3. **MA Labs:** Establish reseller account and request integration options
4. **VEX Robotics:** Contact sales for bulk ordering arrangements
5. **ASI Computer Tech:** Clarify exact company and contact for integration options

---

## Resources

### PromoStandards
- Main Site: https://promostandards.org
- Service API: https://promostandards.org/standards-services-api/
- Endpoints: https://promostandards.org/standards-endpoints/
- GitHub: https://github.com/promostandards

### PROS (VEX Development)
- Main Site: https://pros.cs.purdue.edu
- API Docs: https://pros.cs.purdue.edu/v5/api/
- GitHub: https://github.com/purduesigbots/pros
- OkapiLib: https://okapilib.github.io/OkapiLib

### Staples Business
- Enterprise: https://www.staplesadvantage.com
- Quill: https://www.quill.com
