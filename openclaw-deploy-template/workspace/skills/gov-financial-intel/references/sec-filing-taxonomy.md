# SEC Filing Taxonomy

Complete reference for SEC filings with search strategies.

## Registration Statements

| Form | Purpose | Key Sections |
|------|---------|--------------|
| S-1 | IPO registration | Business, risk factors, financials, use of proceeds |
| S-3 | Shelf registration (seasoned issuers) | Incorporation by reference |
| S-4 | Business combinations | Merger terms, pro forma financials |
| S-8 | Employee benefit plans | Stock options, ESPPs |
| S-11 | REITs | Real estate specific |
| F-1 | Foreign IPO | Non-US company going public |
| F-3 | Foreign shelf | Foreign seasoned issuer |
| F-4 | Foreign business combination | Cross-border mergers |

## Periodic Reports

| Form | Frequency | Deadline | Contents |
|------|-----------|----------|----------|
| 10-K | Annual | 60-90 days after FY | Full audited financials, MD&A, risk factors |
| 10-Q | Quarterly | 40-45 days after Q | Unaudited financials, MD&A update |
| 20-F | Annual (foreign) | 4 months after FY | Foreign private issuer annual |
| 40-F | Annual (Canadian) | MJDS filers | Canadian companies |

### 10-K Deep Dive

| Item | Contains | Intelligence |
|------|----------|--------------|
| 1 | Business | Operations, segments, competition |
| 1A | Risk Factors | What keeps management up at night |
| 1B | Unresolved Staff Comments | SEC concerns |
| 2 | Properties | Real estate, facilities |
| 3 | Legal Proceedings | Lawsuits, investigations |
| 4 | Mine Safety | Mining companies only |
| 5 | Market for Stock | Trading info |
| 6 | Selected Financial Data | 5-year trends |
| 7 | MD&A | Management's view of financials |
| 7A | Quantitative Risk | Derivatives, interest rate exposure |
| 8 | Financial Statements | Audited financials + notes |
| 9 | Disagreements with Accountants | Red flag if present |
| 9A | Controls and Procedures | Internal control assessment |
| 10 | Directors and Officers | Board composition |
| 11 | Executive Compensation | Pay details |
| 12 | Security Ownership | Who owns stock |
| 13 | Certain Relationships | Related party transactions |
| 14 | Principal Accountant Fees | Audit costs |

## Current Reports (8-K)

| Item | Event Type |
|------|------------|
| 1.01 | Entry into material agreement |
| 1.02 | Termination of material agreement |
| 1.03 | Bankruptcy |
| 2.01 | Acquisition/disposition of assets |
| 2.02 | Results of operations (earnings) |
| 2.03 | Creation of direct financial obligation |
| 2.04 | Triggering events (debt acceleration) |
| 2.05 | Costs of exit/restructuring |
| 2.06 | Material impairments |
| 3.01 | Delisting notice |
| 3.02 | Unregistered equity sales |
| 3.03 | Material modification to shareholder rights |
| 4.01 | Change in accountant |
| 4.02 | Non-reliance on prior financials |
| 5.01 | Change in control |
| 5.02 | Departure/election of directors/officers |
| 5.03 | Amendments to articles/bylaws |
| 5.05 | Amendments to code of ethics |
| 5.06 | Change in shell company status |
| 5.07 | Shareholder vote results |
| 7.01 | Regulation FD disclosure |
| 8.01 | Other events |
| 9.01 | Financial statements and exhibits |

## Proxy Statements

| Form | Purpose |
|------|---------|
| DEF 14A | Definitive proxy (most common) |
| PRE 14A | Preliminary proxy |
| DEFA14A | Additional proxy materials |
| DEFC14A | Contested election materials |
| DEFM14A | Merger proxy |
| DEFR14A | Revised proxy |

### DEF 14A Contents

| Section | Intelligence |
|---------|--------------|
| Voting matters | What shareholders decide |
| Board nominees | Director backgrounds |
| Executive compensation | CEO pay, peer comparisons |
| CD&A | Compensation philosophy |
| Pay vs performance | New SEC requirement |
| Related party transactions | Conflicts of interest |
| Stock ownership table | Insider/institutional holders |
| Proposal rationale | Why management recommends votes |
| Shareholder proposals | Activist demands |

## Beneficial Ownership

| Form | Trigger | Deadline | Purpose |
|------|---------|----------|---------|
| Schedule 13D | >5% with intent to influence | 10 days | Activist disclosure |
| Schedule 13G | >5% passive | 45 days after year-end | Institutional holders |
| Form 3 | Becoming insider | 10 days | Initial insider holdings |
| Form 4 | Insider transaction | 2 business days | Buy/sell by insiders |
| Form 5 | Annual insider report | 45 days after FY | Catch-all for Form 4 |
| 13F | Institutional >$100M | 45 days after Q | Hedge fund holdings |

### 13D vs 13G

| Characteristic | 13D | 13G |
|----------------|-----|-----|
| Intent | Active/influence | Passive |
| Detail required | High (plans, funding) | Low |
| Amendment trigger | Material change | Annual or 5% threshold |
| Strategy signal | Activist campaign | Index fund, passive |

### 13F Analysis

Filed by institutions with >$100M AUM. 45-day delay.

Useful for:
- Tracking hedge fund positions
- Identifying crowded trades
- Following "smart money"

Limitations:
- No short positions
- No non-US securities
- No derivatives (usually)
- 45-day stale data

## Tender Offers & M&A

| Form | Purpose |
|------|---------|
| SC TO-T | Third-party tender offer |
| SC TO-I | Issuer tender offer |
| SC 14D-9 | Target's response to tender |
| SC 13E-3 | Going-private transaction |
| Schedule 14D-1 | Tender offer statement |

## Investment Companies

| Form | Purpose |
|------|---------|
| N-1A | Mutual fund registration |
| N-2 | Closed-end fund registration |
| N-CSR | Certified shareholder report |
| N-PORT | Monthly portfolio holdings |
| N-CEN | Annual census |
| N-PX | Proxy voting record |

## Search Patterns

### By Company
```
https://www.sec.gov/cgi-bin/browse-edgar?company=COMPANY+NAME&type=&dateb=&owner=include&count=40&action=getcompany
```

### By CIK
```
https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001234567
```

### By Filing Type
```
https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=10-K&company=&dateb=&owner=include&count=40
```

### Full-Text Search
```
https://efts.sec.gov/LATEST/search-index?q="exact phrase"&dateRange=custom&startdt=2023-01-01&enddt=2024-01-01
```

### Direct Archive Access
```
https://www.sec.gov/Archives/edgar/data/[CIK]/[ACCESSION-NUMBER-NO-DASHES]/
```

### RSS Feeds
```
https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=[CIK]&type=&dateb=&owner=include&count=40&output=atom
```

## API Access

### Company Facts
```
https://data.sec.gov/api/xbrl/companyfacts/CIK[10-digit].json
```

### Submissions
```
https://data.sec.gov/submissions/CIK[10-digit].json
```

### Bulk Data
```
https://www.sec.gov/dera/data
https://www.sec.gov/data-research
```

## Red Flags in Filings

| Signal | Location | Meaning |
|--------|----------|---------|
| Auditor change | 8-K Item 4.01 | Potential accounting issues |
| Going concern | 10-K audit opinion | Survival doubt |
| Material weakness | 10-K Item 9A | Control failures |
| Restatement | 8-K Item 4.02 | Prior financials wrong |
| Related party transactions | DEF 14A | Conflicts |
| Risk factor changes | 10-K Item 1A | New worries |
| Insider selling spike | Form 4 | Executives bailing |
| Unusual 8-Ks | Multiple filings | Something happening |
| Delayed filings | NT 10-K/Q | Trouble meeting deadlines |
