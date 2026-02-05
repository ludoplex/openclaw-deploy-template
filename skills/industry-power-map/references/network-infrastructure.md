# Network Infrastructure

Backbone providers, CDNs, Internet Exchange Points (IXPs), carrier hotels, and interconnection.

## NAICS: 517111, 517311, 518210

## Tier 1 Backbone Providers

Tier 1 = settlement-free peering with all other Tier 1 networks (no transit payments).

```
LUMEN TECHNOLOGIES (LUMN)
├── NAICS: 517311
├── Revenue: $14B (2024)
├── Fiber Miles: 450,000+
├── HQ: Monroe, LA
├── C-Suite:
│   ├── CEO: Kate Johnson (2023)
│   ├── CFO: Chris Stansbury
│   └── CTO: Ashley Haynes-Gaspar
├── Networks: AS3356 (Level 3), AS209
├── Activist: None active
├── Union: CWA (legacy workers)
├── Assets: Largest enterprise fiber, voice
└── Position: #1 North American backbone

AT&T (T)
├── NAICS: 517311/517111
├── Revenue: $122B (2024)
├── Backbone: AS7018
├── HQ: Dallas, TX
├── C-Suite:
│   ├── CEO: John Stankey (2020)
│   ├── CFO: Pascal Desroches
│   └── COO: Jeff McElfresh
├── Activist: Elliott (previously, $3.2B stake)
├── Union: CWA, IBEW (150,000+ union workers)
└── Position: Tier 1, largest US telco

VERIZON (VZ)
├── NAICS: 517311/517111
├── Revenue: $134B (2024)
├── Backbone: AS701, AS702
├── HQ: New York, NY
├── C-Suite:
│   ├── CEO: Hans Vestberg (2018)
│   ├── CFO: Tony Skiadas
│   └── EVP Network: Joe Russo
├── Activist: None
├── Union: CWA, IBEW (60,000+ union)
├── Acquisition: Frontier ($20B, 2024)
└── Position: Tier 1, largest fiber footprint

COGENT COMMUNICATIONS (CCOI)
├── NAICS: 517311
├── Revenue: $1.1B (2024)
├── Fiber Miles: 100,000+
├── HQ: Washington, DC
├── C-Suite:
│   ├── CEO: Dave Schaeffer (founder)
│   └── CFO: Thaddeus Weed
├── Networks: AS174
├── Acquisition: Sprint wireline assets
├── Strategy: Aggressive pricing, peering disputes
└── Position: Tier 1, pure-play internet backbone

GTT COMMUNICATIONS (Private)
├── NAICS: 517311
├── Revenue: $1.5B (2024)
├── HQ: McLean, VA
├── C-Suite:
│   ├── CEO: Ernie Ortega
│   └── Owner: PE consortium (post-restructuring)
├── Networks: AS3257
└── Position: Tier 1, enterprise focus

NTT COMMUNICATIONS (Japan)
├── NAICS: 517311
├── Revenue: $2B+ (Americas)
├── Parent: NTT (Japan)
├── Networks: AS2914
└── Position: Tier 1, global enterprise

TELIA CARRIER (Now Arelion)
├── NAICS: 517311
├── Revenue: $1B+ (2024)
├── HQ: Stockholm (US: NYC)
├── Parent: Polhem Infra (spun from Telia)
├── Networks: AS1299
└── Position: Tier 1, transatlantic leader

LIBERTY GLOBAL (LBTYA)
├── Subsidiary: Cogeco Peer 1, VM Business
├── Networks: AS6830
└── Position: Tier 1 (European focus, US presence)
```

### Backbone Network Map
```
┌─────────────────────────────────────────────────────────┐
│            US INTERNET BACKBONE TOPOLOGY                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  SEATTLE ──────────────── CHICAGO ─────── NEW YORK     │
│     │                        │               │          │
│     │                        │               │          │
│ SAN FRANCISCO              │           ASHBURN         │
│     │                      │               │           │
│     └──── LOS ANGELES ─────┼─── DALLAS ────┘           │
│              │             │       │                    │
│              │             │       │                    │
│           PHOENIX ────── DENVER  ATLANTA               │
│                                    │                    │
│                                  MIAMI                  │
│                                                         │
│  ═══ Lumen (Level 3)    ─── AT&T    ... Verizon       │
│  ─── Cogent             ─── Zayo    ─── GTT           │
├─────────────────────────────────────────────────────────┤
│ Key Hubs: Ashburn VA (largest), Chicago, Dallas        │
└─────────────────────────────────────────────────────────┘
```

## Tier 2/Regional Backbone

```
ZAYO GROUP (Private)
├── NAICS: 517311
├── Revenue: $2.8B (2024)
├── Fiber Miles: 140,000+
├── HQ: Boulder, CO
├── C-Suite:
│   ├── CEO: Matt Steinfort
│   └── Owner: Digital Colony, EQT
├── Focus: Fiber infrastructure, dark fiber
├── Networks: AS6461
└── Position: #1 dark fiber provider

CROWN CASTLE (CCI)
├── NAICS: 517311/531120
├── Revenue: $6.6B (2024)
├── Fiber Miles: 85,000+
├── Small Cells: 115,000+
├── HQ: Houston, TX
├── C-Suite:
│   ├── CEO: Steven Moskowitz (2024)
│   └── CFO: Dan Schlanger
├── Activist: Elliott (won seats, CEO departed)
├── Structure: REIT
└── Position: #1 small cell, #3 fiber

WINDSTREAM (Private)
├── NAICS: 517311
├── Revenue: $4B (2024)
├── Fiber Miles: 170,000
├── HQ: Little Rock, AR
├── C-Suite:
│   ├── CEO: Tony Thomas
│   └── Owner: Post-bankruptcy restructure
├── Union: CWA
└── Position: Regional enterprise fiber

CONSOLIDATED COMMUNICATIONS (CNSL)
├── NAICS: 517311
├── Revenue: $1B (2024)
├── Fiber Miles: 57,000
├── HQ: Mattoon, IL
├── C-Suite:
│   ├── CEO: Bob Udell
│   └── Major Owner: Searchlight Capital (33%)
├── Focus: Rural/suburban fiber-to-home
└── Position: Regional ILEC/fiber overbuilder
```

## Content Delivery Networks (CDN)

```
AKAMAI TECHNOLOGIES (AKAM)
├── NAICS: 518210
├── Revenue: $4B (2024)
├── PoPs: 4,200+ (130+ countries)
├── Traffic: 15-30% of global web traffic
├── HQ: Cambridge, MA
├── C-Suite:
│   ├── CEO: Tom Leighton (co-founder)
│   ├── CFO: Ed McGowan
│   └── CTO: Robert Blumofe
├── Activist: None
├── Union: None
├── Services: CDN, security, edge compute
└── Position: #1 pure-play CDN

CLOUDFLARE (NET)
├── NAICS: 518210
├── Revenue: $1.7B (2024)
├── PoPs: 310+ cities
├── Traffic: ~20% of web traffic
├── HQ: San Francisco, CA
├── C-Suite:
│   ├── CEO: Matthew Prince (co-founder)
│   ├── CFO: Thomas Seifert
│   └── COO: Michelle Zatlyn (co-founder)
├── Activist: None
├── Services: CDN, DDoS, zero trust, DNS
└── Position: #1 DDoS mitigation, fastest-growing CDN

FASTLY (FSLY)
├── NAICS: 518210
├── Revenue: $550M (2024)
├── PoPs: 80+
├── HQ: San Francisco, CA
├── C-Suite:
│   ├── CEO: Todd Nightingale (2022)
│   └── CFO: Ron Kisling
├── Focus: Edge cloud, real-time CDN
└── Position: Developer-focused CDN

LIMELIGHT/EDGIO (Bankrupt)
├── Status: Filed Chapter 11 (2024)
├── Assets: Sold to Akamai, others
└── Lesson: CDN commoditization pressure
```

### Hyperscaler CDNs (Internal + External)

```
AMAZON CLOUDFRONT
├── Parent: Amazon Web Services
├── PoPs: 600+ (90+ cities)
├── Market Share: ~15% CDN traffic
└── Integration: AWS ecosystem

GOOGLE CLOUD CDN
├── Parent: Google Cloud
├── Network: Private Google backbone
├── Market Share: ~10%
└── Integration: GCP services

MICROSOFT AZURE CDN
├── Parent: Microsoft Azure
├── PoPs: 150+
├── Partners: Akamai, Verizon (white-label)
└── Integration: Azure/O365/Xbox

APPLE CDN (Internal)
├── Purpose: App Store, Apple TV+, iCloud
├── Backbone: Invested $10B+ in own network
└── Traffic: Top 5 internet traffic source
```

## Internet Exchange Points (IXPs)

```
EQUINIX INTERNET EXCHANGE
├── NAICS: 518210
├── Locations: 40+
├── Participants: 2,600+
├── Parent: Equinix (EQIX)
├── Key Sites: Ashburn, Chicago, LA, NYC
└── Position: #1 global IX operator

DE-CIX
├── HQ: Frankfurt (US: NYC, Dallas, Phoenix)
├── Participants: 800+ (US)
├── Traffic: 20+ Tbps peak (global)
└── Position: Largest IX by traffic

AMS-IX
├── HQ: Amsterdam (US: Chicago, Bay Area)
├── US Expansion: Growing presence
└── Position: #2 global IX

SIX (Seattle Internet Exchange)
├── Location: Seattle
├── Model: Non-profit
└── Position: Major Pacific Northwest hub

ANY2 EXCHANGE
├── Parent: CoreSite
├── Location: Los Angeles
├── Participants: 300+
└── Position: West Coast hub

CHICAGO IX (ChIX)
├── Location: Chicago
├── Model: Non-profit
└── Position: Midwest hub
```

## Carrier Hotels / Data Center Interconnection

```
EQUINIX (EQIX)
├── NAICS: 518210
├── Revenue: $8.2B (2024)
├── Data Centers: 270+ (71 metros, 33 countries)
├── HQ: Redwood City, CA
├── C-Suite:
│   ├── CEO: Charles Meyers
│   ├── CFO: Keith Taylor
│   └── COO: Brandi Galvin Morandi
├── Activist: None
├── Structure: REIT
├── Key Sites:
│   ├── Ashburn VA: DC1-DC15
│   ├── Silicon Valley: SV1-SV11
│   ├── New York: NY1-NY13
│   └── Chicago: CH1-CH4
└── Position: #1 carrier-neutral colocation

DIGITAL REALTY (DLR)
├── NAICS: 518210
├── Revenue: $5.5B (2024)
├── Data Centers: 300+
├── HQ: Austin, TX
├── C-Suite:
│   ├── CEO: Andy Power (2023)
│   ├── CFO: Matt Mercier
│   └── Owner: (Brookfield bid rejected)
├── Activist: Land & Buildings, Starboard
├── Structure: REIT
├── Key Sites:
│   ├── Ashburn VA: Campus
│   ├── Dallas: Mega-campus
│   └── Chicago: 350 E Cermak (largest single)
└── Position: #2 carrier-neutral colo

CORESITE REALTY (COR)
├── NAICS: 518210
├── Parent: American Tower (acquired 2021, $10B)
├── Data Centers: 27
├── HQ: Denver, CO
├── Focus: US carrier-neutral
├── Key Sites:
│   ├── Los Angeles: One Wilshire
│   ├── Reston VA: VA1-VA3
│   └── Denver: DE1-DE2
└── Position: #3 carrier-neutral colo (US)

CYRUSONE (Private)
├── NAICS: 518210
├── Owner: KKR, Global Infrastructure Partners
├── Acquired: $15B (2021)
├── Data Centers: 50+
└── Position: #4 carrier-neutral

QTS REALTY (Private)
├── NAICS: 518210
├── Owner: Blackstone
├── Acquired: $10B (2021)
├── Data Centers: 30+
└── Position: Major hyperscale provider

VANTAGE DATA CENTERS (Private)
├── Owner: Digital Bridge
├── Focus: Hyperscale
├── Expansion: Rapid growth in N. America
└── Position: Growing hyperscale player
```

### Major Carrier Hotels (Neutral Interconnection Buildings)

```
ONE WILSHIRE (Los Angeles)
├── Address: 624 S Grand Ave, Los Angeles, CA
├── Operator: CoreSite (One Wilshire)
├── Carriers: 300+
├── Status: Western US primary interconnect hub
└── Position: #1 West Coast carrier hotel

60 HUDSON STREET (New York)
├── Address: 60 Hudson St, New York, NY
├── Operator: Multiple (Equinix, etc.)
├── Carriers: 200+
├── Status: Historic hub, transatlantic landing
└── Position: #1 NYC carrier hotel

111 8TH AVENUE (New York)
├── Address: 111 8th Ave, New York, NY
├── Owner: Google
├── Status: Major Google presence, carrier-rich
└── Position: #2 NYC carrier hotel

350 E CERMAK (Chicago)
├── Address: 350 E Cermak Rd, Chicago, IL
├── Operator: Digital Realty
├── Size: 1.1M sq ft (largest single data center)
├── Status: Midwest primary hub
└── Position: #1 Midwest carrier hotel

ASHBURN (Northern Virginia)
├── Campus: Multiple buildings, "Data Center Alley"
├── Operators: Equinix, Digital Realty, CoreSite, QTS
├── Traffic: ~70% of global internet traffic touches
├── Subsea: MAE-East origin, gov't proximity
└── Position: #1 global interconnection hub

NAP OF THE AMERICAS (Miami)
├── Address: 50 NE 9th St, Miami, FL
├── Operator: Equinix (MI1)
├── Status: Latin America gateway
└── Position: #1 Latin America interconnect

WESTIN BUILDING (Seattle)
├── Address: 2001 6th Ave, Seattle, WA
├── Operator: Digital Realty
├── Status: Pacific Rim, Alaska gateway
└── Position: #1 Pacific Northwest carrier hotel
```

## Subsea Cable Operators

```
SUBSEA CABLE SYSTEMS (US Landings):
├── MAREA (Microsoft/Meta): Virginia Beach - Bilbao
├── DUNANT (Google): Virginia Beach - France
├── HAVFRUE (Google/Facebook): New Jersey - Denmark
├── GRACE HOPPER (Google): NYC - UK/Spain
├── JUPITER (Amazon): US West - Japan
├── CURIE (Google): LA - Chile
├── FIRMINA (Google): US East - Argentina
└── ECHO/BIFROST (Meta/Google): US West - Singapore

US CABLE OPERATORS:
├── SubCom (Cerberus owned): #1 cable installer
├── TE SubCom: Major installer
└── Alcatel Submarine Networks (Nokia): Equipment
```

## Sector Concentration

| Segment | Top 3 Share | HHI |
|---------|-------------|-----|
| Tier 1 Backbone | ~60% | ~1,500 |
| CDN (Enterprise) | ~70% | ~2,000 |
| Carrier-Neutral Colo | ~80% | ~2,400 |
| IXP Traffic | ~50% | ~1,200 |

Critical Infrastructure Note: Network infrastructure increasingly consolidated. Ashburn VA concentration creates systemic risk.
