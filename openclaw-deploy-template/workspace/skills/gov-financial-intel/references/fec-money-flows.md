# FEC Money Flows

Campaign finance tracing, PAC structures, and dark money patterns.

## Committee Types

| Type | Code | Contribution Limits | Disclosure |
|------|------|---------------------|------------|
| Candidate committee | H/S/P | Yes | Full |
| Party committee | X/Y/Z | Yes | Full |
| Traditional PAC | N/Q | Yes ($5K/candidate) | Full |
| Super PAC | O | None | Full (donors disclosed) |
| Hybrid PAC | V | Split accounts | Partial |
| Leadership PAC | D | Yes | Full |
| 501(c)(4) | N/A | None | Minimal (dark money) |
| 501(c)(6) | N/A | None | Minimal (trade assocs) |

## Super PAC Structure

### Formation
1. File FEC Form 1 (Statement of Organization)
2. Select committee type "O" (Independent Expenditure-Only)
3. Certify no coordination with candidates

### Money Flow
```
Individual/Corp Donor → Super PAC → Independent Expenditures
                                  ↓
                        (Ads for/against candidates)
```

### Required Disclosures
- All contributions >$200 (donor name, employer, occupation)
- All expenditures
- Purpose of expenditure
- Candidate supported/opposed

### Search
```
https://www.fec.gov/data/committees/?committee_type=O
https://www.fec.gov/data/independent-expenditures/
```

## Dark Money Pathways

### 501(c)(4) to Super PAC
```
Anonymous Donor → 501(c)(4) "Social Welfare" Org → Super PAC
                  (no donor disclosure)              (discloses c4 as donor)
```

The 501(c)(4) shields original donor identity.

### LLC Conduit
```
Individual → LLC (single member) → Super PAC
             (may not disclose beneficial owner)
```

Some states require LLC member disclosure; federal doesn't.

### Donor-Advised Fund (DAF)
```
Donor → DAF (Fidelity Charitable, etc.) → 501(c)(4) → Super PAC
        (gets immediate tax deduction)    (anonymous)
```

### Tracing Dark Money

1. **Super PAC Disclosures**: Look for 501(c)(4) or LLC donors
2. **IRS Form 990**: 501(c)(4)s disclose some activities
3. **State Filings**: Some states require more disclosure
4. **990 Schedule B**: Major donors (>$5K) to 501(c)(3)s
5. **News/FOIA**: Investigative reporting, leaked documents

## Individual Contributions

### Limits (2023-2024 cycle)

| Recipient | Limit |
|-----------|-------|
| Candidate committee | $3,300/election |
| National party | $41,300/year |
| State/local party | $10,000/year combined |
| Traditional PAC | $5,000/year |
| Super PAC | Unlimited |

### Bundling
Fundraisers "bundle" others' contributions. Tracked via:
- Lobbyist bundling reports (LDA)
- Campaign disclosures of bundlers
- News reports

### Search Individual Donors
```
https://www.fec.gov/data/receipts/individual-contributions/
```

## Corporate & Union Money

### Direct to Candidates
Prohibited (corporations and unions cannot contribute directly).

### To PACs
- PAC can solicit restricted class (executives, shareholders, members)
- PAC contributions are disclosed

### To Super PACs
Unlimited corporate/union contributions allowed since Citizens United.

### Independent Expenditures
Corporations can spend unlimited amounts independently (no coordination).

## Tracking Money Flow

### Contribution Search
```
# By donor name
https://www.fec.gov/data/receipts/individual-contributions/?contributor_name=NAME

# By employer
https://www.fec.gov/data/receipts/individual-contributions/?contributor_employer=COMPANY

# By committee
https://www.fec.gov/data/committee/C[COMMITTEE_ID]/
```

### Expenditure Search
```
# Independent expenditures
https://www.fec.gov/data/independent-expenditures/?candidate_id=H0XX00000

# Operating expenditures
https://www.fec.gov/data/disbursements/?committee_id=C00000000
```

### Bulk Data
```
https://www.fec.gov/data/browse-data/?tab=bulk-data
```

## Key Filing Types

| Form | Purpose | Frequency |
|------|---------|-----------|
| Form 1 | Committee registration | Once |
| Form 3 | Candidate report | Quarterly + pre/post election |
| Form 3P | Presidential candidate | Same |
| Form 3X | PAC/Party report | Quarterly or monthly |
| Form 5 | Independent expenditure | 24/48 hour reports |
| Form 6 | 48-hour contribution notice | Within 48 hours (>$1000) |
| Form 9 | Electioneering communication | Within 24 hours |
| Form 99 | Miscellaneous text | As needed |

## Connected Organizations

Many PACs are "connected" to sponsoring organizations:
- Corporate PACs (connected to corporation)
- Union PACs (connected to union)
- Trade association PACs (connected to association)

The connected org can pay PAC admin costs.

Search connected orgs: Check Form 1, Line 6.

## Coordination Rules

Super PACs cannot coordinate with candidates. Coordination = contribution.

### What's Prohibited
- Sharing polling data
- Discussing ad strategy
- Using same vendors for strategic work
- Candidate fundraising for Super PAC

### Gray Areas
- Public information
- Former staff with "cooling off" period
- Common vendors for non-strategic work

## State-Level

FEC covers federal races only. State races require state searches:

| Resource | URL |
|----------|-----|
| NCSL tracker | ncsl.org/research/elections |
| FollowTheMoney | followthemoney.org |
| State disclosure sites | Varies by state |

## OpenSecrets Integration

OpenSecrets (opensecrets.org) aggregates FEC data with analysis:

- Donor lookup: opensecrets.org/donor-lookup
- Industry totals: opensecrets.org/industries
- PAC profiles: opensecrets.org/pacs
- Lobbying: opensecrets.org/federal-lobbying
- Revolving door: opensecrets.org/revolving
