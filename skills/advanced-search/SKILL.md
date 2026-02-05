---
name: advanced-search
description: Expert search query formulation using advanced operators and combinations. Activates when Claude needs to search effectively — web research, finding specific documents, locating technical resources, investigating topics, or any task requiring precise information retrieval. Covers Google, Bing, DuckDuckGo operators, boolean logic, site/filetype/date filters, query refinement strategies, and multi-engine tactics.
---

# Advanced Search

Precision search through operator mastery.

## Core Principle

Default searches return noise. Operators cut through it. The goal: fewest queries, highest signal.

## Universal Operators

These work across major engines (Google, Bing, DuckDuckGo):

| Operator | Function | Example |
|----------|----------|---------|
| `"exact phrase"` | Match exact sequence | `"buffer overflow"` |
| `-term` | Exclude term | `python -snake` |
| `site:domain` | Restrict to domain | `site:github.com` |
| `filetype:ext` | Specific file type | `filetype:pdf` |
| `OR` | Either term (must be caps) | `CVE OR vulnerability` |
| `*` | Wildcard (single word) | `"how to * in python"` |

## Google-Specific Operators

| Operator | Function | Example |
|----------|----------|---------|
| `intitle:` | Term in page title | `intitle:configuration` |
| `allintitle:` | All terms in title | `allintitle:nginx reverse proxy` |
| `inurl:` | Term in URL | `inurl:admin` |
| `allinurl:` | All terms in URL | `allinurl:api docs` |
| `intext:` | Term in body text | `intext:password` |
| `allintext:` | All terms in body | `allintext:default credentials` |
| `related:` | Similar sites | `related:stackoverflow.com` |
| `cache:` | Cached version | `cache:example.com/page` |
| `define:` | Dictionary definition | `define:idempotent` |
| `AROUND(n)` | Terms within n words | `CEO AROUND(3) resigned` |
| `before:YYYY-MM-DD` | Before date | `before:2024-01-01` |
| `after:YYYY-MM-DD` | After date | `after:2023-06-01` |
| `daterange:` | Julian date range | `daterange:2459580-2459945` |

## Bing-Specific Operators

| Operator | Function | Example |
|----------|----------|---------|
| `contains:` | Page contains file type | `contains:pdf` |
| `loc:` or `location:` | Country/region | `loc:US` |
| `language:` | Page language | `language:en` |
| `prefer:` | Emphasis term | `prefer:tutorial` |
| `feed:` | RSS/Atom feeds | `feed:security` |
| `ip:` | Sites on IP address | `ip:192.168.1.1` |
| `url:` | URL contains | `url:api` |

## DuckDuckGo-Specific

| Operator | Function | Example |
|----------|----------|---------|
| `!bang` | Redirect to site search | `!gh python requests` |
| `region:` | Region filter | `region:uk-en` |
| `sort:date` | Sort by date | `security sort:date` |

Useful bangs: `!g` (Google), `!gh` (GitHub), `!so` (StackOverflow), `!w` (Wikipedia), `!scholar` (Google Scholar), `!arxiv` (arXiv)

## Operator Combinations

### Pattern: Domain + Filetype
```
site:gov filetype:pdf "climate report"
site:edu filetype:ppt "machine learning"
```

### Pattern: Title + Exclusion
```
intitle:guide -beginner -introduction
intitle:API documentation -deprecated
```

### Pattern: URL Structure Exploitation
```
inurl:admin inurl:login
inurl:/api/v2/ site:example.com
inurl:wp-content/uploads filetype:pdf
```

### Pattern: Temporal Scoping
```
"supply chain attack" after:2023-01-01
CVE-2024 site:nvd.nist.gov
```

### Pattern: Boolean Stacking
```
(python OR golang) "web scraping" -selenium
(AWS OR Azure OR GCP) "cost optimization" filetype:pdf
```

### Pattern: Exact + Wildcard
```
"the * of programming"
"how to * without *"
"* is the new *"
```

### Pattern: Proximity Search (Google)
```
CEO AROUND(5) "stepped down"
vulnerability AROUND(3) exploit
```

## Query Formulation Process

### Step 1: Define Information Need
- What exactly am I looking for?
- What format is it likely in?
- Who would have created it?
- Where would they publish it?

### Step 2: Identify Key Terms
- Domain-specific terminology (insider words)
- Likely document titles
- Associated proper nouns
- Technical identifiers (CVE, RFC, etc.)

### Step 3: Select Operators
| Need | Operator Choice |
|------|-----------------|
| Specific site | `site:` |
| Specific format | `filetype:` |
| Recent only | `after:` |
| Exact terminology | `"quotes"` |
| Alternative terms | `OR` |
| Noise removal | `-exclusion` |
| URL patterns | `inurl:` |
| Page titles | `intitle:` |

### Step 4: Construct Query
Start narrow, expand if needed:
```
[most specific term] [critical operator] [second operator]
```

### Step 5: Iterate
- Too few results → remove operators, broaden terms
- Too many results → add operators, narrow terms
- Wrong results → change terminology, add exclusions

## Domain-Specific Strategies

### Academic/Research
```
site:arxiv.org OR site:scholar.google.com "term"
filetype:pdf site:edu "literature review"
"et al" "2024" [topic] filetype:pdf
```

### Technical Documentation
```
site:docs.* OR site:documentation.* [product]
inurl:docs [product] [feature]
site:readthedocs.io [library]
```

### Code/Repositories
```
site:github.com [function] language:python
site:github.com inurl:blob [specific code pattern]
site:gist.github.com [snippet description]
```

### Security Research
```
site:nvd.nist.gov CVE-[year]
site:exploit-db.com [product]
"proof of concept" OR "PoC" [vulnerability]
site:cve.mitre.org [vendor]
```

### Legal/Government
```
site:gov filetype:pdf [regulation]
site:courtlistener.com [case name]
site:sec.gov filetype:10-K [company]
```

### News/Current Events
```
site:reuters.com OR site:apnews.com [topic]
[topic] after:[recent date] -opinion -editorial
```

## Troubleshooting

### Query Returns Nothing
1. Remove operators one by one
2. Try synonym terminology
3. Check operator syntax (caps for OR, no space after colon)
4. Try different search engine

### Too Much Noise
1. Add `"exact phrases"` for key terms
2. Add `-common_irrelevant_term`
3. Narrow with `site:` or `filetype:`
4. Add temporal constraints

### Results Are Outdated
1. Add `after:YYYY-MM-DD`
2. Sort by date (engine-dependent)
3. Add current year in query

### Can't Find Specific Document Type
1. Try multiple extensions: `filetype:pdf OR filetype:doc`
2. Use `contains:` (Bing) for pages linking to files
3. Search document repositories directly

## Multi-Engine Strategy

Different engines have different indices. When one fails:

| Engine | Strength |
|--------|----------|
| Google | Largest index, best operator support |
| Bing | Better for recent content, some unique sites |
| DuckDuckGo | Bang shortcuts, privacy, aggregated results |
| Yandex | Eastern European content, reverse image |
| Baidu | Chinese content |

For comprehensive research, query multiple engines with adapted syntax.

## Reference Files

- `references/operators-complete.md` — Full operator reference with edge cases
- `references/query-templates.md` — Copy-paste templates for common scenarios
