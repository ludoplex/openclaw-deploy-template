# MHI Procurement App — Market Analysis

**Date:** 2026-02-09
**Entities:** MHI (GovCon), DSAIC (SaaS/ML), Computer Store (Retail/Gaming)

---

## 1. Market Context

### IT Distribution Market
- **Global IT distribution market:** ~$500B annually
- **Top distributors:** Ingram Micro, TD SYNNEX, D&H, Tech Data (merged with SYNNEX)
- **Typical VAR/reseller margins:** 5-15% on hardware, 15-40% on services

### Your Supplier Accounts
| Supplier | Account # | API Status | Strengths |
|----------|-----------|------------|-----------|
| Ingram Micro | 50-135152-000 | REST v6 ✅ | Best API, largest catalog |
| TD SYNNEX | 786379 | Digital Bridge | IBM, Lenovo strong |
| D&H | 3270340000 | REST OAS3 ✅ | Gaming, consumer focus |
| Climb Channel | CU0043054170 | No API ❌ | IBM software, specialty |

---

## 2. Pain Points in Current Procurement

### Manual Price Comparison
- **Time cost:** 15-30 min per quote checking 4 distributors
- **Opportunity cost:** Miss better pricing, leave margin on table
- **Error rate:** Manual lookup = pricing mistakes

### Multi-Entity Complexity
- Different pricing tiers per entity (MHI vs DSAIC vs Computer Store)
- Different tax exemptions (GovCon vs retail)
- Different shipping addresses

### Margin Visibility
- Hard to know which distributor offers best margin on specific SKU
- Special pricing (SPAs) buried in portals
- Rebates/incentives tracked manually

---

## 3. Competitive Landscape

### Commercial Solutions
| Solution | Cost/mo | Multi-Dist | Margin Calc | Notes |
|----------|---------|------------|-------------|-------|
| ConnectWise CPQ | $75-150/user | Yes (limited) | Yes | Heavy, MSP-focused |
| QuoteWerks | $15-40/user | Yes | Basic | Older tech |
| Quoter | $99-299/mo | No | Basic | SaaS, simple |
| Distributor portals | Free | No | Hidden | Must check each |

### Gap Analysis
- **No solution** does real-time multi-distributor comparison well
- **ConnectWise CPQ** closest but:
  - Expensive ($150/user × 3 users = $450/mo)
  - Overkill for simple quoting
  - Lock-in to ConnectWise ecosystem

---

## 4. Value Proposition

### Time Savings
| Current | With Tool | Savings |
|---------|-----------|---------|
| 30 min/quote × 20 quotes/week | 5 min/quote | 8+ hrs/week |
| $50/hr labor | | $400/week = $20k/year |

### Margin Improvement
- 2-5% better margins from always finding best price
- On $500k annual hardware sales = $10-25k/year

### Combined Value
- **Conservative:** $30k/year value
- **Optimistic:** $50k/year value

---

## 5. Build vs Buy Analysis

### Buy (ConnectWise CPQ)
- **Pro:** Already built, supported
- **Con:** $5-10k/year, doesn't match your workflow, overkill

### Build Custom
- **Pro:** Exactly what you need, multi-entity support, own the IP
- **Con:** Development time/cost

### Hybrid Recommendation
**Build minimal viable tool:**
- Query all 4 distributors for pricing
- Show comparison table with margins
- Let you pick winner and generate quote
- Multi-entity switching (MHI/DSAIC/Computer Store)

**Cost estimate:**
- API integrations: 3 have APIs (Ingram, SYNNEX, D&H)
- Climb: Manual entry or portal scraping
- UI: Simple HTMX dashboard
- Effort: 40-80 hours
- Budget: $5-10k if outsourced

---

## 6. Recommendations

### Minimum Viable Product (MVP)
1. **Ingram Micro integration first** (best API)
2. **D&H second** (gaming/consumer for Computer Store)
3. **TD SYNNEX third** (IBM for DSAIC)
4. **Climb last** (manual or scraping)

### Architecture
- **Backend:** FastAPI + Python
- **Frontend:** HTMX for speed
- **Database:** SQLite (local-first, portable)
- **Or:** Single APE binary with Cosmopolitan (matches your philosophy)

### Success Metrics
- Quote creation time < 5 minutes
- Always show best margin option
- Multi-entity support day 1

---

*Analysis based on IT channel industry knowledge. Specific pricing data needs validation against current distributor APIs.*
