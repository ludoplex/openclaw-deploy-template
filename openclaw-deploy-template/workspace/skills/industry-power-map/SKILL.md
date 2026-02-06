---
name: us-industry-power-map
description: Comprehensive mapping of US industries by NAICS classification with dominant entities, market share, C-suite executives, organizational structures, activist investor relationships, union relations, and foreign entity associations. Covers all major sectors including network infrastructure (backbone providers, CDNs, carrier hotels), transportation/logistics (trucking, rail, air, maritime), financial services, healthcare, energy, manufacturing, and technology. Activates when researching industry concentration, corporate power structures, executive leadership, labor relations, activist campaigns, or competitive dynamics.
---

# US Industry Power Map

Comprehensive reference for US industry structure organized by NAICS (North American Industry Classification System).

## NAICS Structure

| Code | Sector |
|------|--------|
| 11 | Agriculture, Forestry, Fishing, Hunting |
| 21 | Mining, Quarrying, Oil & Gas |
| 22 | Utilities |
| 23 | Construction |
| 31-33 | Manufacturing |
| 42 | Wholesale Trade |
| 44-45 | Retail Trade |
| 48-49 | Transportation & Warehousing |
| 51 | Information |
| 52 | Finance & Insurance |
| 53 | Real Estate |
| 54 | Professional Services |
| 55 | Management of Companies |
| 56 | Administrative & Waste Services |
| 61 | Educational Services |
| 62 | Health Care & Social Assistance |
| 71 | Arts, Entertainment, Recreation |
| 72 | Accommodation & Food Services |
| 81 | Other Services |
| 92 | Public Administration |

## Reference Files

### Sector Profiles (by NAICS)
- `references/naics-21-mining-energy.md` — Oil/gas, mining, commodities trading
- `references/naics-22-utilities.md` — Electric, gas, water utilities
- `references/naics-31-33-manufacturing.md` — Food processing, chemicals, steel, aerospace, auto
- `references/naics-44-45-retail.md` — Mass retail, grocery, e-commerce
- `references/naics-48-49-transportation.md` — Rail, trucking, air cargo, maritime, logistics
- `references/naics-51-information.md` — Telecom, media, software, data processing
- `references/naics-52-finance.md` — Banking, insurance, asset management, PE, payments
- `references/naics-53-real-estate.md` — REITs, brokerages, developers
- `references/naics-62-healthcare.md` — Insurance, pharma, distributors, providers

### Cross-Sector References
- `references/network-infrastructure.md` — Backbone providers, CDNs, IXPs, carrier hotels
- `references/activist-investors.md` — Major activist funds, campaigns, tactics
- `references/union-relations.md` — Major unions by industry, recent campaigns
- `references/foreign-ownership.md` — SWFs, Chinese entities, European conglomerates
- `references/org-charts.md` — ASCII organizational structures for major entities

## Entity Profile Format

Each dominant entity includes:
```
COMPANY NAME (Ticker)
├── NAICS: Primary code
├── Revenue: $XXB (Year)
├── Market Share: XX%
├── HQ: City, State
├── C-Suite:
│   ├── CEO: Name (Since Year)
│   ├── CFO: Name
│   ├── COO: Name (if applicable)
│   └── Key: Other notable executives
├── Activist Relations: [Fund] - [Campaign status]
├── Union Relations: [Union] - [Status]
└── Foreign Ties: [Entity] - [Relationship]
```

## Market Concentration Metrics

| HHI Range | Classification |
|-----------|----------------|
| <1,000 | Unconcentrated |
| 1,000-1,800 | Moderate |
| 1,800-2,500 | Concentrated |
| >2,500 | Highly Concentrated |

## Usage

1. Identify sector via NAICS code
2. Load relevant sector reference file
3. Cross-reference with activist/union/foreign ownership files as needed
4. Use org-charts reference for structural visualization
