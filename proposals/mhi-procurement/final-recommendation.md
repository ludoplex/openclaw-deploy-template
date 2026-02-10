# MHI Procurement App — Final Recommendation

**Date:** 2026-02-09  
**Status:** DECISION READY  
**Goal:** "Fastest, easiest, and cheapest procurement app possible, with complete UI containing every feature suppliers expose, best deals and highest margins"

---

## Executive Summary

**The full custom build is premature and risky.** However, "don't build" isn't the right answer either. 

**Recommended path:** A **phased hybrid approach** that validates critical unknowns before committing to a full build, delivers immediate value through existing tools, and progressively builds custom components only where proven necessary.

**TL;DR Decision:**
1. **Week 1-2:** Trial QuoteWerks ($40/user, 30-day trial) — validate if "dated UI" is actually a blocker
2. **Week 1-4:** Validate API access for TD SYNNEX and D&H in writing
3. **If QuoteWerks works:** DONE. Use it. $1,440/year for 3 users.
4. **If QuoteWerks fails AND APIs confirmed:** Build Ingram-only MVP first (60-80 hours)
5. **Scale up only as each phase proves value**

---

## Synthesis of Findings

### What We Know ✅

| Finding | Source | Confidence |
|---------|--------|------------|
| Ingram Micro has excellent REST API with SDKs | API Research | HIGH |
| TD SYNNEX and D&H have no public API docs | API Research | HIGH |
| Climb Channel has no API | All sources | CONFIRMED |
| ConnectWise CPQ and QuoteWerks integrate with all distributors | Redundancy Check | HIGH |
| Estimated value: $30-50k/year from time savings + margin improvement | Market Analysis | MEDIUM |
| Original 40-80 hour estimate is 2-3x too low | Critic Review | HIGH |
| Multi-entity support is 3x more complex than assumed | Critic Review | HIGH |

### Critical Unknowns ❓

| Unknown | Impact if Wrong | How to Validate |
|---------|-----------------|-----------------|
| Can MHI get API access to TD SYNNEX/D&H? | No build possible for those | Call partner support, get in writing |
| Are there API costs or volume minimums? | Budget blowout | Ask distributors directly |
| Rate limits per distributor? | Tool could be unusable | Request documentation |
| Does QuoteWerks actually fail your needs? | Building when you should buy | 30-day trial |
| Multi-entity: shared credentials or separate? | Architecture decision | Ask each distributor |

---

## Creative Alternatives Evaluated

### Option A: Full Custom Build (Original Plan)
- **Scope:** All 4 distributors, multi-entity, complete UI
- **Realistic estimate:** 160-280 hours, $20-35k Year 1 TCO
- **Risk:** HIGH — depends on unconfirmed API access
- **Verdict:** ❌ **PREMATURE** — don't commit until unknowns resolved

### Option B: Buy QuoteWerks
- **Scope:** All distributors already integrated
- **Cost:** $40/user perpetual OR ~$15-40/user/month
- **Risk:** LOW — established product, 30-day trial available
- **Downside:** "Dated Windows UI" — but is that actually a blocker?
- **Verdict:** ⚠️ **VALIDATE FIRST** — trial it before deciding it's inadequate

### Option C: Ingram-Only MVP
- **Scope:** Just Ingram API (confirmed available), single entity first
- **Estimate:** 60-80 hours, $6-10k
- **Risk:** MEDIUM — known API, but captures only ~40-50% of purchases
- **Value:** If Ingram handles majority of volume, still captures most value
- **Verdict:** ✅ **VIABLE** as Phase 1 if QuoteWerks fails

### Option D: Browser Automation for Portal-Only Distributors
- **Scope:** Playwright/Puppeteer scraping for D&H, SYNNEX portals
- **Estimate:** 40-80 hours per portal, high maintenance
- **Risk:** HIGH — fragile, breaks on UI changes, possibly ToS violation
- **Verdict:** ⚠️ **LAST RESORT** — use only for Climb (no other option)

### Option E: Hybrid — QuoteWerks + Custom Margin Layer
- **Scope:** Use QuoteWerks for pricing, build thin custom layer for margin optimization
- **Estimate:** QuoteWerks license + 20-40 hours custom work
- **Risk:** LOW — gets 80% value immediately
- **Verdict:** ✅ **SMART COMPROMISE** if QuoteWerks works but lacks margin features

### Option F: Phased Build with Gates
- **Scope:** Build incrementally, prove value at each phase before continuing
- **Risk:** LOW — fails fast if assumptions wrong
- **Verdict:** ✅ **RECOMMENDED** — detailed below

---

## Recommended Path: Phased Approach with Decision Gates

### Phase 0: Validation Sprint (2 weeks, ~$0-500)

**Goal:** Answer critical unknowns before committing any development budget.

| Task | Owner | Deadline | Exit Criteria |
|------|-------|----------|---------------|
| Start QuoteWerks trial | User | Day 1 | Trial active |
| Use QuoteWerks for 5+ real quotes | User | Day 14 | Document specific pain points |
| Call TD SYNNEX partner support | User | Day 3 | Written confirmation of API access path |
| Call D&H partner development | User | Day 3 | Written confirmation of API access path |
| Request rate limit docs from Ingram | User | Day 5 | Documented limits |
| Clarify multi-entity credential model | User | Day 7 | Single app or per-entity? |

**Decision Gate 0:**
- ✅ QuoteWerks meets needs → **STOP. Use QuoteWerks. Project complete.**
- ❌ QuoteWerks fails AND API access confirmed → Proceed to Phase 1
- ❌ API access denied for SYNNEX/D&H → Consider Ingram-only or browser automation

---

### Phase 1: Ingram-Only MVP (6-8 weeks, $8-12k)

**Goal:** Capture value from the best API first. Single entity (pick highest volume: MHI or DSAIC).

**Scope:**
- Ingram Micro Price & Availability API integration
- Simple web UI (HTMX or similar)
- Search products, get pricing, show margin calculations
- Single entity credentials only
- **NO ordering** — quote only (reduce scope)

**Deliverables:**
- Working prototype that can query Ingram pricing in <5 seconds
- Margin calculator showing cost vs sale price
- Basic quote export (PDF or CSV)

**Effort:** 60-80 hours
**Budget:** $8,000-12,000 if outsourced

**Decision Gate 1:**
- ✅ MVP saves 2+ hours/week → Proceed to Phase 2
- ❌ API integration was 2x harder than expected → Reassess full build viability
- ❌ Ingram pricing is stale/inaccurate → Validate with distributor, may need different approach

---

### Phase 2: Add Second Distributor (4-6 weeks, $6-10k)

**Goal:** Add D&H or TD SYNNEX (whichever has easier API access).

**Scope:**
- Second distributor API integration
- Data normalization layer (map different field names)
- Cross-distributor price comparison view
- Still single entity

**Prerequisite:** API access confirmed in Phase 0

**Effort:** 50-70 hours
**Budget:** $6,000-10,000

**Decision Gate 2:**
- ✅ Cross-distributor comparison working → Proceed to Phase 3
- ❌ Second API was nightmare → Don't add third, consider hybrid with QuoteWerks

---

### Phase 3: Third Distributor + Climb Workaround (4-6 weeks, $6-10k)

**Goal:** Add remaining distributor API. Handle Climb (no API).

**Scope:**
- Third distributor integration
- Climb Channel: Options in order of preference:
  1. Manual entry (user types in Climb prices from portal)
  2. CSV import (export from Climb portal, import to app)
  3. Browser automation (last resort, high maintenance)

**Effort:** 50-70 hours
**Budget:** $6,000-10,000

---

### Phase 4: Multi-Entity Support (3-4 weeks, $5-8k)

**Goal:** Support MHI, DSAIC, and Computer Store in same app.

**Scope:**
- Entity switcher in UI
- Credential management (up to 12 credential sets: 4 distributors × 3 entities)
- Entity-specific margin rules
- Entity-specific tax handling (exempt vs taxable)
- Quote attribution to entity

**Effort:** 40-60 hours
**Budget:** $5,000-8,000

---

### Phase 5: Full Feature Build-Out (6-8 weeks, $10-15k)

**Goal:** "Complete UI containing every feature suppliers expose"

**Scope:**
- Webhooks for inventory updates
- Order placement via API (significant new complexity)
- Historical pricing trends
- Saved product lists / favorites
- Customer-specific pricing (SPA integration if available)
- Quote templates

**Effort:** 80-120 hours
**Budget:** $10,000-15,000

---

## Total Investment by Path

| Path | Year 1 Cost | Ongoing Cost | Time to Value |
|------|-------------|--------------|---------------|
| **QuoteWerks (if it works)** | $500-1,500 | $500-1,500/year | 2 weeks |
| **Phase 1 only (Ingram MVP)** | $8-12k | $2-3k/year maintenance | 2 months |
| **Through Phase 3** | $20-32k | $5-8k/year | 4-5 months |
| **Full build (Phase 5)** | $35-55k | $8-12k/year | 8-12 months |
| **ConnectWise CPQ (buy)** | $5,400/year | $5,400/year | 1 month |

---

## Decision Criteria

### Choose QuoteWerks if:
- ✅ 30-day trial proves it handles your workflow
- ✅ "Dated UI" is tolerable for $30k+ savings
- ✅ Multi-distributor pricing works for your accounts
- ✅ Multi-entity can be handled (separate installs or built-in)

### Choose Ingram-Only MVP if:
- ✅ QuoteWerks fails specific requirements (document them)
- ✅ Ingram represents 50%+ of your purchasing volume
- ✅ You're willing to manually check D&H/SYNNEX for rest
- ✅ API access confirmed, rate limits acceptable

### Choose Full Custom Build if:
- ✅ QuoteWerks trial failed with documented reasons
- ✅ API access confirmed for all 3 distributors
- ✅ Rate limits and costs documented and acceptable
- ✅ You have budget for $35-55k Year 1
- ✅ You're committed to ongoing maintenance ($8-12k/year)
- ✅ Value proposition ($30-50k/year) justifies investment

### Choose ConnectWise CPQ if:
- ✅ QuoteWerks too dated but budget allows $5.4k/year
- ✅ Already in ConnectWise ecosystem
- ✅ MSP-focused features are acceptable
- ✅ Willing to adapt workflow to their system

---

## If You Build: Technical Recommendations

### Architecture (Keep It Simple)
```
┌─────────────────────────────────────────────────┐
│                  Web UI (HTMX)                  │
├─────────────────────────────────────────────────┤
│              FastAPI Backend (Python)           │
├───────────┬───────────┬───────────┬─────────────┤
│  Ingram   │  D&H API  │  SYNNEX   │   Climb     │
│  SDK      │  (custom) │  (custom) │   (manual)  │
└───────────┴───────────┴───────────┴─────────────┘
                      │
              SQLite (local-first)
```

### Tech Stack
- **Backend:** Python + FastAPI (async, good for multiple API calls)
- **Frontend:** HTMX + Alpine.js (minimal JS, fast development)
- **Database:** SQLite (portable, no server needed)
- **Deployment:** Single binary with embedded assets (matches your APE philosophy)
- **SDK:** Use Ingram's official Python SDK: `pip install xi.sdk.resellers`

### Key Design Decisions
1. **Async all the things** — Query 3 distributors in parallel, not serial
2. **Cache aggressively** — Price lookups with 15-minute TTL reduce API calls
3. **Fail gracefully** — If one distributor is down, show others
4. **Log everything** — GovCon compliance may require audit trail

---

## Immediate Next Steps

### This Week:
1. [ ] **Start QuoteWerks trial** — https://www.quotewerks.com/trial.asp
2. [ ] **Call TD SYNNEX partner support** — Ask about REST API access, timeline, requirements
3. [ ] **Call D&H partner development** — Same questions
4. [ ] **Register at Ingram developer portal** — https://developer.ingrammicro.com
5. [ ] **Get Ingram sandbox credentials** — Start experimenting with their API

### Script for Distributor Calls:
> "Hi, I'm a reseller with account [X]. We're looking to automate our procurement workflow. Do you offer a REST API for pricing and availability lookups? What's the process to get API access? Are there any costs, volume minimums, or rate limits I should know about? Can I get this information in writing?"

### Week 2:
- [ ] Use QuoteWerks for 5+ real customer quotes
- [ ] Document specific pain points (not just "dated UI")
- [ ] Review API access responses from distributors
- [ ] Make Phase 0 decision

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| API access denied | Validated in Phase 0 before spending money |
| Build takes 3x longer | Phase gates allow early exit |
| QuoteWerks doesn't work | Trial is free/cheap; document specific failures |
| Pricing is stale/inaccurate | Discovered in Phase 1 with real testing |
| Multi-entity is harder than expected | Deferred to Phase 4; core value proven first |
| Distributor APIs change | Budget maintenance costs; use official SDKs where available |

---

## Summary

**Don't build the full system yet.** But don't give up either.

The smart path is:
1. **Validate unknowns first** (2 weeks, minimal cost)
2. **Try the cheap option** (QuoteWerks trial)
3. **Build incrementally** if needed, with decision gates at each phase
4. **Prove value before scaling** — Ingram-only MVP → add distributors → add entities

The "fastest, easiest, and cheapest" approach is to prove QuoteWerks doesn't work before spending $35k+ on a custom build. If QuoteWerks handles 80% of your needs for $1,500/year, that's the right answer — even if the UI is dated.

If QuoteWerks genuinely fails, you'll have documented evidence of why, validated API access from distributors, and a phased plan that limits your risk at every step.

---

**Final Recommendation:** Start Phase 0 validation this week. Decision point in 2 weeks.

---

*Document prepared by synthesis of market analysis, redundancy check, API research, and technical critique. All estimates include 50% buffer from original projections based on critic review.*
