# Agency Databases

Full database inventory for federal agencies with query strategies.

## IRS Databases

### Tax-Exempt Organization Search
**URL**: https://apps.irs.gov/app/eos/

Search by:
- Organization name
- EIN
- City/State
- Exempt status

### Form 990 Series Access

| Source | Coverage | Cost |
|--------|----------|------|
| IRS EOS | Basic search | Free |
| ProPublica Nonprofit Explorer | Full 990s, searchable | Free |
| GuideStar/Candid | Full 990s, analysis | Freemium |
| Foundation Directory | Foundations focus | Paid |
| CitizenAudit | Bulk downloads | Free |
| Open990 | API access | Free |

### ProPublica Nonprofit Explorer
**URL**: https://projects.propublica.org/nonprofits/

Features:
- Full Form 990 PDFs
- Searchable text
- Executive compensation
- Revenue/expense trends
- Related organizations

### IRS Statistics of Income (SOI)
**URL**: https://www.irs.gov/statistics

Aggregate tax data:
- Individual returns by income
- Corporate returns
- Estate tax
- Tax-exempt organizations

### IRS Data Book
Annual statistics on IRS operations, enforcement, collections.

### Master File Extracts
Business Master File (BMF) extracts for tax-exempt organizations:
- https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-bulk-data-downloads

## DOE Databases

### Loan Programs Office (LPO)
**URL**: https://www.energy.gov/lpo/projects

Tracks:
- Loan guarantees (clean energy, vehicles)
- Direct loans
- Project status
- Amounts committed/disbursed

### ARPA-E Projects
**URL**: https://arpa-e.energy.gov/technologies/projects

Advanced energy research funding.

### Energy Information Administration (EIA)
**URL**: https://www.eia.gov/

| Database | Contains |
|----------|----------|
| Electricity | Generation, sales, prices |
| Petroleum | Production, imports, prices |
| Natural Gas | Production, storage, prices |
| Coal | Production, consumption |
| Renewables | Capacity, generation |
| State profiles | State-level energy data |

### EIA APIs
```
https://api.eia.gov/
```

### Office of Scientific and Technical Information (OSTI)
**URL**: https://www.osti.gov/

DOE-funded research outputs.

### Environmental Management (Cleanup)
**URL**: https://www.energy.gov/em/environmental-management

Nuclear cleanup sites, budgets, contractors.

### Federal Energy Regulatory Commission (FERC)
**URL**: https://www.ferc.gov/

- Pipeline applications
- Electric rate filings
- Hydropower licenses
- Market oversight

eLibrary search: https://elibrary.ferc.gov/eLibrary/

## EPA Databases

### ECHO (Enforcement & Compliance History)
**URL**: https://echo.epa.gov/

| Data Type | Search Method |
|-----------|---------------|
| Facility info | Name, address, ID |
| Permits | Permit number, type |
| Inspections | Date range, type |
| Violations | Permit type, severity |
| Enforcement | Action type, penalty |
| Compliance | Status, history |

### Facility Search
```
https://echo.epa.gov/facilities/facility-search
```

### Detailed Facility Report
```
https://echo.epa.gov/detailed-facility-report?fid=[FACILITY_ID]
```

### TRI (Toxics Release Inventory)
**URL**: https://www.epa.gov/toxics-release-inventory-tri-program

Annual toxic chemical release data from facilities.

TRI Explorer: https://enviro.epa.gov/triexplorer/

### Envirofacts
**URL**: https://enviro.epa.gov/

Multi-system query tool:
- Air (AFS, ICIS-Air)
- Water (PCS, ICIS-NPDES)
- Waste (RCRAInfo, CERCLIS)
- Toxics (TRI)
- Radiation (RADInfo)

### Superfund (CERCLIS)
**URL**: https://www.epa.gov/superfund

National Priorities List sites, cleanup status.

SEMS search: https://www.epa.gov/enviro/sems-search

### EJSCREEN
**URL**: https://ejscreen.epa.gov/

Environmental justice mapping tool. Demographic and environmental indicators.

### NEPAssist
**URL**: https://nepassisttool.epa.gov/

Environmental review for NEPA compliance.

### Air Quality
- AirData: https://www.epa.gov/outdoor-air-quality-data
- AQS API: https://aqs.epa.gov/aqsweb/documents/data_api.html

### Water Quality
- WATERS: https://www.epa.gov/waterdata/waters-geospatial-data-downloads
- How's My Waterway: https://mywaterway.epa.gov/

## DOJ Databases

### Press Releases
**URL**: https://www.justice.gov/news

Filter by:
- Component (FBI, DEA, USAO, etc.)
- Topic
- Date

### PACER (Court Records)
**URL**: https://pacer.uscourts.gov/

Federal court dockets, filings, opinions.

| Court Level | Site |
|-------------|------|
| District Courts | ecf.[district].uscourts.gov |
| Bankruptcy | ecf.[district].uscourts.gov |
| Appellate | ecf.[circuit].uscourts.gov |
| Supreme Court | supremecourt.gov |

### Free Alternatives to PACER
| Source | URL |
|--------|-----|
| RECAP/CourtListener | courtlistener.com/recap |
| Justia Dockets | dockets.justia.com |
| Google Scholar | scholar.google.com (opinions) |
| Court websites | Individual court sites |

### FARA (Foreign Agents)
**URL**: https://efile.fara.gov/

Foreign agent registrations and filings.

Search: https://efile.fara.gov/ords/fara/f?p=1381:1

| Filing | Contains |
|--------|----------|
| Registration | Agent, foreign principal, activities |
| Supplemental | Updated activities |
| Exhibit A | Copy of agreement |
| Exhibit B | Political activities |
| Short Form | Individual agents |
| Informational materials | Propaganda distributed |

### BOP Inmate Locator
**URL**: https://www.bop.gov/inmateloc/

Federal prisoner search.

### DEA Diversion Control
**URL**: https://www.deadiversion.usdoj.gov/

Controlled substance registrations, actions.

### FBI Records Vault
**URL**: https://vault.fbi.gov/

FOIA releases, historical records.

### FOIA Reading Room
**URL**: https://www.justice.gov/oip/foia-library

Released documents by DOJ components.

## BLM Databases

### General Land Office Records
**URL**: https://glorecords.blm.gov/

Historical land patents, survey plats, field notes.

### Mining Claims
Search: https://glorecords.blm.gov/search/default.aspx

Data includes:
- Claim name
- Claimant
- Location
- Status (active/closed)
- Commodities
- Case disposition

### LR2000 (Legacy Rehost 2000)
Land and mineral case records.

Queries:
- Serial number
- Case type
- Geographic area
- Action code

### Oil & Gas
| Resource | URL |
|----------|-----|
| Lease sales | blm.gov/programs/energy-and-minerals/oil-and-gas/leasing |
| Production data | onrr.gov (Office of Natural Resources Revenue) |
| Well data | State oil/gas commissions |

### ONRR (Royalties)
**URL**: https://onrr.gov/

Federal mineral revenue data.

Statistical Information: https://statistics.onrr.gov/

### GeoCommunicator
**URL**: https://www.geocommunicator.gov/

GIS data for public lands.

### Public Land Statistics
**URL**: https://www.blm.gov/about/data/public-land-statistics

Annual reports on land use, permits, leases.

## Cross-Agency Resources

### USASpending.gov
**URL**: https://www.usaspending.gov/

All federal contracts, grants, loans, direct payments.

### FPDS (Federal Procurement)
**URL**: https://www.fpds.gov/

Federal contract data.

### SAM.gov
**URL**: https://sam.gov/

- Entity registrations (contractors)
- Exclusions (debarments)
- Federal opportunities
- Wage determinations

### Data.gov
**URL**: https://data.gov/

Federal open data catalog.

### FOIA.gov
**URL**: https://www.foia.gov/

FOIA request portal, agency reading rooms.

### Regulations.gov
**URL**: https://www.regulations.gov/

Proposed rules, comments, dockets.
