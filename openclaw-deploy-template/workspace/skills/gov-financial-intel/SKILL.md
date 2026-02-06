---
name: gov-financial-intel
description: Public records intelligence from US government sources — SEC filings (EDGAR), CFIUS, FEC (Super PACs, campaign finance), lobbying disclosures, and federal agency data (IRS, DOE, EPA, DOJ, BLM). Also covers global wealth tracking (billionaires, corporations). Activates when researching corporate ownership, political money flows, regulatory filings, government contracts, environmental compliance, or wealth/power mapping.
---

# Government Financial Intelligence

Public records reveal power structures. Know where to look.

## SEC / EDGAR

### Access
- **URL**: https://www.sec.gov/cgi-bin/browse-edgar
- **Full-text search**: https://efts.sec.gov/LATEST/search-index
- **API**: https://data.sec.gov/

### Key Filing Types

| Form | Purpose | Intelligence Value |
|------|---------|-------------------|
| 10-K | Annual report | Full financials, risk factors, legal proceedings |
| 10-Q | Quarterly report | Recent performance, emerging issues |
| 8-K | Current events | Material events, acquisitions, executive changes |
| DEF 14A | Proxy statement | Executive comp, board members, shareholder proposals |
| 13-F | Institutional holdings | What hedge funds own (quarterly, 45-day delay) |
| 13-D | Activist stake >5% | Hostile takeover signals, activist intentions |
| 13-G | Passive stake >5% | Large passive holders |
| S-1 | IPO registration | Pre-IPO company deep dive |
| 4 | Insider transactions | Executive buying/selling (2-day filing) |
| 144 | Intent to sell restricted stock | Insider selling signal |
| SC 13D/G | Beneficial ownership | Who controls what |
| DEFA14A | Additional proxy materials | Contested board fights |
| 6-K | Foreign private issuer | Non-US company events |
| 20-F | Foreign annual report | Non-US company financials |

### Search Strategies
```
site:sec.gov/cgi-bin/browse-edgar "company name"
site:sec.gov 10-K "risk factors" "company name"
site:sec.gov/Archives/edgar/data/[CIK]/
```

CIK lookup: https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany

## CFIUS (Committee on Foreign Investment)

### What It Covers
Reviews foreign acquisitions of US businesses for national security.

### Public Information
- **Annual reports**: https://home.treasury.gov/policy-issues/international/the-committee-on-foreign-investment-in-the-united-states-cfius
- **Covered transactions** (limited disclosure)
- **Presidential decisions** (blocked deals are public)
- **Enforcement actions**

### Search Strategy
CFIUS doesn't publish transaction details. Intelligence comes from:
- SEC filings mentioning CFIUS review
- News reports of blocked deals
- Treasury press releases
- Congressional testimony

```
site:treasury.gov CFIUS
site:sec.gov "CFIUS" filetype:htm
"CFIUS approval" OR "CFIUS clearance" "company name"
```

## FEC / Campaign Finance

### Access
- **URL**: https://www.fec.gov/data/
- **API**: https://api.open.fec.gov/

### Key Data

| Record Type | Contains |
|-------------|----------|
| Committee filings | PAC/Super PAC receipts and disbursements |
| Candidate filings | Campaign contributions |
| Independent expenditures | Outside spending for/against candidates |
| Party committee filings | National/state party money |
| Electioneering communications | Issue ads near elections |

### Super PACs
Independent expenditure-only committees. No contribution limits.

Search: https://www.fec.gov/data/committees/?committee_type=O

Key fields:
- Total raised/spent
- Top donors (individuals, organizations)
- Connected organizations
- Expenditure targets (which candidates)

### Dark Money Trail
501(c)(4) "social welfare" orgs can donate to Super PACs without disclosing donors.

Trace via:
- Super PAC disclosures showing 501(c)(4) donors
- IRS Form 990 for the 501(c)(4)
- State incorporation records

## Lobbying Disclosures

### Federal (LDA)
- **URL**: https://lda.senate.gov/system/public/
- **House**: https://disclosures.house.gov/
- **Search**: https://lda.senate.gov/filings/public/filing/search/

### Required Disclosures
- LD-1: Initial registration
- LD-2: Quarterly activity reports (issues, agencies contacted, lobbyists)
- LD-203: Semiannual contribution reports

### Key Fields
| Field | Intelligence |
|-------|--------------|
| Client | Who's paying |
| Registrant | Lobbying firm |
| Lobbyists | Individual lobbyists (often former officials) |
| Issues | What they're lobbying on (general) |
| Specific issues | Actual bills, regulations |
| Agencies contacted | Which parts of government |
| Amount | How much spent |

### K Street Research
```
site:lda.senate.gov "company name"
site:opensecrets.org/federal-lobbying "company name"
"revolving door" "agency name" lobbyist
```

OpenSecrets aggregates: https://www.opensecrets.org/federal-lobbying

## IRS Public Data

### Nonprofit/Tax-Exempt
- **Form 990 Search**: https://apps.irs.gov/app/eos/
- **Bulk data**: https://www.irs.gov/statistics/soi-tax-stats-annual-extract-of-tax-exempt-organization-financial-data

### Form 990 Contents
| Section | Contains |
|---------|----------|
| Part I | Revenue, expenses, assets summary |
| Part VII | Compensation of officers, directors, key employees |
| Part VIII | Revenue breakdown |
| Part IX | Expense breakdown |
| Schedule B | Contributors (not always public) |
| Schedule I | Grants to organizations |
| Schedule J | Compensation details |
| Schedule L | Transactions with interested persons |
| Schedule O | Supplemental information |

### Search Tools
- ProPublica Nonprofit Explorer: https://projects.propublica.org/nonprofits/
- GuideStar/Candid: https://www.guidestar.org/
- Foundation Directory: https://fdo.foundationcenter.org/

### Private Foundations (990-PF)
Must disclose:
- All grants made
- Investment holdings
- Trustees and compensation

## DOE (Department of Energy)

### Public Data
- **Loans & Guarantees**: https://www.energy.gov/lpo/projects
- **Grants**: https://www.energy.gov/office-management/grants
- **FOIA Reading Room**: https://www.energy.gov/management/foia-reading-room

### Key Databases
| Database | URL |
|----------|-----|
| Loan Programs Office | energy.gov/lpo |
| ARPA-E projects | arpa-e.energy.gov/technologies/projects |
| EIA data | eia.gov |
| Environmental cleanup | energy.gov/em |

## EPA (Environmental Protection Agency)

### Public Databases

| Database | Contains | URL |
|----------|----------|-----|
| ECHO | Enforcement, compliance | echo.epa.gov |
| TRI | Toxic releases | epa.gov/toxics-release-inventory-tri-program |
| Envirofacts | Multi-system query | enviro.epa.gov |
| CERCLIS | Superfund sites | epa.gov/superfund |
| NEPAssist | Environmental review | nepassisttool.epa.gov |
| EJSCREEN | Environmental justice | ejscreen.epa.gov |

### ECHO (Enforcement and Compliance History Online)
Search by facility, permit, enforcement action.

Key data:
- Permit violations
- Inspections
- Enforcement actions
- Penalties assessed
- Compliance status

### TRI (Toxics Release Inventory)
Annual reporting of toxic chemical releases by facilities.

## DOJ (Department of Justice)

### Public Records

| Source | Contains | URL |
|--------|----------|-----|
| Press releases | Indictments, settlements | justice.gov/news |
| PACER | Federal court filings | pacer.uscourts.gov |
| FARA | Foreign agent registration | fara.us |
| BOP Inmate Locator | Federal prisoners | bop.gov/inmateloc |
| FOIA Reading Room | Released documents | justice.gov/oip/foia-library |

### FARA (Foreign Agents Registration Act)
Foreign lobbying disclosures.

- **Search**: https://efile.fara.gov/ords/fara/f?p=1381:1
- Required for anyone representing foreign governments/entities in political or quasi-political capacity

### PACER Strategy
Federal court docket search. $0.10/page, capped at $3/document.

Free alternatives:
- RECAP Archive: https://www.courtlistener.com/recap/
- Justia: https://dockets.justia.com/

## BLM (Bureau of Land Management)

### Public Databases

| Database | Contains | URL |
|----------|----------|-----|
| LR2000 | Land & mineral records | glorecords.blm.gov |
| Mining claims | Active/closed claims | glorecords.blm.gov |
| Oil & gas leases | Federal lease data | blm.gov/programs/energy-and-minerals |
| AFMSS | Mining claim recordation | blm.gov |
| GeoCommunicator | GIS data | geocommunicator.gov |

### Mining Claims Search
General Land Office Records: https://glorecords.blm.gov/

### Oil & Gas Leasing
- Lease sale results
- Producing leases
- Royalty data (via ONRR: onrr.gov)

## Wealth Tracking

### Billionaire Lists
| Source | URL | Update Frequency |
|--------|-----|------------------|
| Forbes World's Billionaires | forbes.com/billionaires | Real-time |
| Bloomberg Billionaires | bloomberg.com/billionaires | Daily |
| Forbes 400 (US) | forbes.com/forbes-400 | Annual |
| Hurun Global Rich List | hurun.net | Annual |

### Corporate Rankings
| Source | URL | Focus |
|--------|-----|-------|
| Fortune Global 500 | fortune.com/global500 | Revenue |
| Forbes Global 2000 | forbes.com/global2000 | Multi-metric |
| S&P 500 | By market cap | |
| Fortune 500 (US) | fortune.com/fortune500 | US revenue |

### Ownership Tracing
- SEC 13-F filings (institutional)
- Proxy statements (DEF 14A) for insider holdings
- Form 4 for insider transactions
- Foreign equivalents (UK: Companies House, EU: national registries)

## Reference Files

- `references/sec-filing-taxonomy.md` — Complete SEC form reference with search patterns
- `references/fec-money-flows.md` — Campaign finance tracing, PAC structures, dark money patterns
- `references/agency-databases.md` — Full database inventory for IRS, DOE, EPA, DOJ, BLM with query strategies
