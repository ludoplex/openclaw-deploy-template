# Technical Critique: MHI Procurement App Proposal

**Review Date:** 2026-02-09  
**Reviewer:** Technical Critic (Subagent)  
**Status:** ⚠️ SIGNIFICANT GAPS IDENTIFIED

---

## Executive Summary

The research is a solid starting point but dangerously incomplete for actual build decisions. **The 40-80 hour estimate is unrealistic by 2-3x** given undocumented integration complexity. Key findings:

1. Only 1 of 3 "API-ready" distributors has publicly accessible documentation
2. Rate limits, costs, and partner requirements are unresearched
3. Multi-entity switching is harder than assumed
4. Product matching across distributors is unsolved
5. Real-time pricing has accuracy caveats not addressed

---

## 1. API Rate Limits & Costs — UNRESEARCHED ⛔

### What the research says:
Nothing. Zero mention of rate limits or API costs.

### Reality check:

**Ingram Micro XI API:**
- Rate limits exist but aren't published in public docs
- OAuth tokens have expiration windows (typically 1-4 hours)
- Unknown: Is there per-call pricing? Per-SKU pricing lookup costs?
- Unknown: Sandbox vs production rate limit differences

**TD SYNNEX:**
- No documentation found = no rate limit info
- Historical "XMLconnect" systems often had strict call quotas (e.g., 1000/day)
- Enterprise integrations may require volume commitments

**D&H:**
- No public API = complete unknown
- ConnectWise CPQ integration exists, but that doesn't mean open API access

### Specific issue:
A "price comparison" tool that queries 4 SKUs × 3 distributors = 12 API calls per lookup. At 20 quotes/day with 5 products each = 1,200 calls/day minimum. **Rate limits could make this unusable.**

### Action required:
Before any build estimate, get written confirmation from each distributor:
- Calls per minute/hour/day limits
- Cost per API call (if any)
- Sandbox limitations vs production

---

## 2. Authentication Complexity — UNDERESTIMATED ⚠️

### What the research says:
"OAuth 2.0" for Ingram. That's it.

### Reality check:

**Ingram Micro OAuth 2.0:**
- Requires application registration and approval process
- Client credentials flow needs secure secret storage
- Token refresh logic must handle expiration gracefully
- **Multi-entity problem:** Can one API app serve MHI + DSAIC + Computer Store? Or does each entity need separate credentials?

**TD SYNNEX Digital Bridge:**
- Unknown auth method. If it's SAML/SSO enterprise auth, that's a different complexity tier than OAuth.
- If XMLconnect (legacy), may be API key + shared secret — but keys likely tied to specific reseller accounts.

**D&H:**
- Unknown. ConnectWise CPQ integration suggests some auth mechanism exists.
- May require signing a data agreement before API credentials issued.

### Specific issue:
**Multi-entity is NOT just "switching."** If each entity (MHI, DSAIC, Computer Store) has a separate reseller account with separate credentials:
- You need 3 sets of OAuth tokens per distributor = 9 credential sets
- Token refresh logic × 9
- Each API call must route to correct credential based on entity
- Some distributors may not allow multi-account API access from single app

### Missed research:
- Is there a "sub-account" or "parent-child" structure for multi-entity?
- Can API credentials be shared across entities under same ownership?

---

## 3. Data Format Inconsistencies — NOT ADDRESSED ⛔

### What the research says:
OpenAPI specs exist for Ingram and D&H (claimed). No schema comparison.

### Reality check:

**Product identification differs by distributor:**
| Field | Ingram | TD SYNNEX | D&H |
|-------|--------|-----------|-----|
| Their Part # | `ingramPartNumber` | Unknown | Unknown |
| MFG Part # | `vendorPartNumber` | Likely different field name | Unknown |
| UPC/EAN | May or may not be present | Unknown | Unknown |

**Price structure likely differs:**
- Ingram: Net price, list price, customer price, SPA price?
- SYNNEX: Similar but different field names?
- D&H: Same products, different price object structure?

**Availability formats:**
- Ingram returns warehouse-level availability (documented)
- SYNNEX/D&H warehouse mapping = unknown
- Shipping estimates: Ingram has freight estimate API; others?

### Specific issue:
**The entire value prop rests on comparing apples-to-apples.** If Ingram returns `priceNet: 142.50` and D&H returns `dealer_cost: "142.50"` and SYNNEX returns a nested `{"unitPrice": {"amount": 14250, "currency": "USD"}}` — you need normalization logic for EVERY field.

### What's missing:
- Actual response schemas from each distributor
- Mapping table: Ingram field → unified schema
- Handling of missing fields (e.g., one distributor doesn't return ETA)

---

## 4. Real-Time Pricing Accuracy — NAIVE ASSUMPTIONS ⚠️

### What the research assumes:
API = real-time = accurate.

### Reality check:

**Pricing staleness:**
- Distributor APIs often cache pricing (15 min - 1 hour lag)
- Special Pricing Authorizations (SPAs) may not appear in API responses
- Promotional pricing may be portal-only
- Rebates/backend incentives are NEVER in API pricing

**Availability mismatches:**
- API may show "in stock" but warehouse reality differs
- Multi-location distributors: Which warehouse? Ship time differs.
- Ingram webhooks for stock updates exist but require setup.

**Quote vs Order price:**
- Prices are NOT locked until order placed
- "Price valid for 24 hours" clauses common
- Customer sees quote price X, distributor charges X+$5 at order time = margin erosion

### Specific issue:
The value proposition claims "$10-25k/year from better margins." But if pricing accuracy is ±2% due to staleness and SPA non-inclusion, you might pick the "wrong" distributor anyway.

### What's missing:
- How stale are prices? What's the cache TTL per distributor?
- Do APIs return SPA/deal-specific pricing?
- How to handle price changes between quote and order?

---

## 5. Multi-Entity Complications — SEVERELY UNDERESTIMATED ⛔

### What the research says:
"Multi-entity support day 1" and "entity switcher."

### Reality check:

**Separate pricing tiers:**
- MHI (GovCon) may have different pricing than DSAIC (SaaS) at same distributor
- Computer Store (retail) likely has consumer-tier pricing
- **You can't just "switch entities" — you're calling different API credentials with different pricing.**

**Tax implications:**
- MHI: Government = likely tax exempt
- Computer Store: Retail = taxable
- API response may or may not include tax. If not, you need tax calculation.

**Shipping address complexity:**
- Each entity has different ship-to
- Some distributors pre-configure ship-to addresses
- API order placement needs correct address ID per entity

**Audit and compliance:**
- GovCon (MHI) may have procurement requirements (DFARS, FAR)
- Can you prove price competition for audit? Need logging.

### Specific issue:
"Entity switcher" implies UI toggle. Real implementation:
1. Select entity → load entity's credentials for each distributor
2. Query pricing APIs with entity-specific credentials
3. Apply entity-specific margin rules
4. Apply entity-specific tax rules
5. Store quote with entity attribution
6. If ordering: use entity-specific ship-to

This is 3x the complexity of single-entity.

---

## 6. Build Time Estimate — UNREALISTIC ⛔

### What the research says:
"40-80 hours"

### Realistic breakdown:

| Task | Estimated | Actual (Conservative) |
|------|-----------|----------------------|
| Ingram API integration | 8-16 hrs | 16-24 hrs (OAuth, testing, error handling) |
| TD SYNNEX integration | 8-16 hrs | 24-40 hrs (undocumented API, partner approval process 2-4 weeks) |
| D&H integration | 8-16 hrs | 24-40 hrs (no docs, partner approval) |
| Climb workaround | 4-8 hrs | 8-16 hrs (scraping = maintenance liability) |
| Data normalization | Not estimated | 16-24 hrs (field mapping, edge cases) |
| Product matching (cross-distributor) | Not estimated | 24-40 hrs (SKU mapping logic) |
| Multi-entity logic | Not estimated | 16-24 hrs |
| UI (HTMX dashboard) | 8-16 hrs | 16-24 hrs |
| Testing | Not estimated | 16-24 hrs |
| **TOTAL** | **40-80 hrs** | **160-256 hrs** |

### What's driving the gap:

1. **TD SYNNEX and D&H have no public APIs.** Getting access takes weeks minimum, possibly months.
2. **Product matching isn't even mentioned.** Matching "Dell Latitude 5540" across 3 distributors with different SKUs requires MFG part number indexing.
3. **Error handling for 3 different APIs** (retries, rate limits, downtime) isn't trivial.
4. **Multi-entity** isn't a toggle — it's multiplying complexity.

### Outsourcing at $5-10k:
At $100-150/hr (typical for senior integration work), $10k = 66-100 hours. That's barely enough for Ingram alone done properly.

---

## 7. Hidden Costs — NOT DISCOVERED ⚠️

### API access costs:
- **Unknown.** Research says "has API" but not "free API."
- Enterprise distributors often charge for API access or require volume minimums.

### Partner requirements:
- TD SYNNEX and D&H likely require:
  - Minimum annual purchase volume
  - Partner tier qualification
  - Signed data use agreements
  - Security questionnaires

### Ongoing maintenance:
- API versions change (Ingram is on v6/v7 already)
- Distributor deprecates endpoint = your app breaks
- OAuth credential rotation

### Infrastructure:
- SSL certificates for OAuth callbacks
- Secret management for 9+ credential sets
- Logging/audit for GovCon compliance

### Research says $5-10k build. Real TCO Year 1:
| Item | Cost |
|------|------|
| Development (realistic) | $15,000-25,000 |
| Possible API fees | $0-5,000/year (unknown) |
| Maintenance/changes | $3,000-5,000/year |
| Infrastructure | $500-1,000/year |
| **Total Year 1** | **$20,000-35,000** |

Compare to ConnectWise CPQ at $150/user × 3 users × 12 months = $5,400/year. Breakeven is 4+ years assuming custom works.

---

## 8. What's Missing From Research ⛔

### Critical gaps:

1. **Actual API access status:**
   - Is MHI currently approved for API access at each distributor?
   - What's the approval timeline for TD SYNNEX/D&H APIs?

2. **Product catalog overlap:**
   - What % of products are available from all 3 distributors?
   - If Ingram has it but D&H doesn't, comparison is impossible

3. **Order placement:**
   - Research focuses on pricing lookup
   - Do you need ordering via API? That's a much bigger scope.

4. **Historical pricing:**
   - Can you query past prices for trend analysis?
   - Useful for "usually cheaper at X" heuristics

5. **Customer-specific pricing:**
   - SPAs, registered deals, promotional pricing
   - If these don't appear in API, the "best price" is wrong

6. **Competitor validation:**
   - Why doesn't QuoteWerks work? "Dated UI" isn't a real objection.
   - What specifically is missing from ConnectWise CPQ?
   - A $5k/year solution that works > $25k custom that might not

---

## 9. Recommendations

### Before proceeding:

1. **Validate API access is possible**
   - Call TD SYNNEX partner support. Ask: "Do you have a REST API for pricing? How do I get access?"
   - Call D&H. Same question.
   - Get this in writing. No API access = no project.

2. **Get rate limit and cost documentation**
   - In writing. From each distributor.

3. **Pull actual API responses**
   - Even just from Ingram sandbox
   - See what fields you really get vs what you assume

4. **Trial QuoteWerks or ConnectWise CPQ**
   - Actually use them. Document specific failings.
   - "Dated UI" might be tolerable for $30k savings

5. **Scope Phase 1 realistically**
   - Ingram only. Single entity. Price lookup only (no ordering).
   - If that takes 40 hours, project is viable.
   - If that takes 100+ hours, custom build is wrong choice.

### Risk-adjusted recommendation:

**HIGH RISK:** Custom multi-distributor build
- Depends on API access you don't have confirmation for
- Depends on costs you haven't researched
- Build estimates are 2-3x optimistic

**MEDIUM RISK:** Ingram-only MVP + manual for others
- Use Ingram API (confirmed available)
- Manual lookup for D&H/SYNNEX
- Still saves time on highest-volume distributor

**LOW RISK:** Extended trial of QuoteWerks
- $40/user/month = $120/month
- Already has D&H/SYNNEX/Ingram integrations
- "Dated" but functional beats "modern" but unbuilt

---

## Summary Table

| Issue | Severity | Impact |
|-------|----------|--------|
| Rate limits unknown | ⛔ Critical | Could make tool unusable |
| 2 of 3 APIs undocumented | ⛔ Critical | Can't estimate build without access |
| Multi-entity × 3 distributors = 9 credential sets | ⚠️ High | 3x complexity |
| Product matching unsolved | ⚠️ High | Can't compare without it |
| Price staleness unaddressed | ⚠️ High | May pick "wrong" distributor |
| Build estimate 2-3x too low | ⛔ Critical | Budget/timeline failure |
| Hidden costs unresearched | ⚠️ High | TCO may exceed buy option |

---

*Critique complete. Recommend pausing build until API access and costs are confirmed in writing from all distributors.*
