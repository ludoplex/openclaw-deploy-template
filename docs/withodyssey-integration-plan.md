# WithOdyssey Integration Plan

**Updated:** 2026-02-15

## State Portals Discovered

See `withodyssey-state-portals.md` for full list.

**Key URLs (MHI approved states):**
- Wyoming: https://wyoming-vendors.withodyssey.com/
- Utah: https://ufa-vendors.withodyssey.com/registration/

## Overview
WithOdyssey is a product listing/sync platform. We need to:
1. Generate CSVs from MHI Procurement database
2. Upload to WithOdyssey
3. Sync to Amazon (mightyhouseinc.com seller account)

## CSV Generation Requirements

### From Procurement App
```bash
./mhi-procurement export --products --file products.csv
./mhi-procurement export --margins --file margins.csv
```

### Fields Needed for WithOdyssey
- SKU (our internal)
- UPC/EAN
- Title/Name
- Manufacturer
- MPN (Manufacturer Part Number)
- Cost (from best supplier)
- MSRP
- Category
- Weight (if available)
- Description

## Amazon Margin Analysis

### Factors to Consider
1. **Supplier Cost** (from procurement app)
2. **Amazon Referral Fee** (8-15% depending on category)
3. **FBA Fees** (if using FBA) OR
4. **Merchant Fulfilled Shipping** (to end customer)
5. **Amazon enforced minimum price** (some categories)
6. **Sales tax** (collected by Amazon but affects margin)

### Profitability Formula
```
Net Profit = Sale Price - Supplier Cost - Amazon Fees - Shipping - Tax Liability
Margin % = Net Profit / Sale Price × 100
```

### Target Metrics
- Minimum margin: 15%
- Target margin: 25-35%
- Flag items below 10% (not worth listing)

## Automation Flow

```
┌─────────────────────┐
│ MHI Procurement DB  │
│ (SQLite SSOT)       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ CSV Export Script   │
│ (margin filtering)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ WithOdyssey Upload  │
│ (API or manual)     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Amazon Listings     │
│ (mightyhouseinc.com)│
└─────────────────────┘
```

## Next Steps
1. [ ] Get WithOdyssey API documentation
2. [ ] Determine upload format (CSV schema)
3. [ ] Build export command with margin filtering
4. [ ] Test with small batch of high-margin items
5. [ ] Automate daily/weekly sync

## Notes
- Need to check Amazon's restricted product categories
- Some items may have MAP (Minimum Advertised Price) restrictions
- Consider Amazon's "Buy Box" algorithm for pricing strategy
