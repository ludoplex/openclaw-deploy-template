# Complete Operator Reference

Comprehensive operator documentation with syntax details, edge cases, and gotchas.

## Google Operators

### Site Restriction

**`site:`** — Restrict results to a domain or subdomain.

```
site:example.com                    # Entire domain
site:docs.example.com               # Specific subdomain
site:*.example.com                  # All subdomains (sometimes works)
site:example.com/path/              # Specific path (unreliable)
site:.edu                           # TLD only
site:gov.uk                         # Country-specific TLD
```

Edge cases:
- No space after colon
- Subpaths are unreliable — use `inurl:` for path matching
- Can combine: `site:github.com OR site:gitlab.com`
- Negation works: `-site:pinterest.com`

### File Type

**`filetype:`** or **`ext:`** — Match file extension.

```
filetype:pdf
filetype:docx
filetype:xlsx
filetype:pptx
filetype:txt
filetype:csv
filetype:json
filetype:xml
filetype:sql
filetype:log
filetype:conf
filetype:ini
filetype:env
```

Edge cases:
- `ext:` is an alias for `filetype:`
- Some formats indexed poorly (zip, exe)
- Can combine: `filetype:pdf OR filetype:doc`
- HTML/HTM usually not needed (default)

### Title Operators

**`intitle:`** — Single term must appear in title.
**`allintitle:`** — All following terms must appear in title.

```
intitle:configuration               # "configuration" in title
intitle:"exact phrase"              # Exact phrase in title
allintitle:nginx reverse proxy      # All three in title
```

Edge cases:
- `intitle:` only applies to immediately following term
- `allintitle:` applies to all following terms (use once)
- Can stack: `intitle:guide intitle:complete`
- Title tags, not visible page titles

### URL Operators

**`inurl:`** — Term appears in URL.
**`allinurl:`** — All terms appear in URL.

```
inurl:admin
inurl:login
inurl:dashboard
inurl:api
inurl:/v2/
inurl:wp-admin
allinurl:api docs v2
```

Edge cases:
- Matches anywhere in URL (domain, path, params)
- Case-insensitive
- Hyphens matched: `inurl:user-guide` finds `/user-guide/`
- Path separators not needed: `inurl:admin` matches `/admin/`

### Text Operators

**`intext:`** — Term in page body.
**`allintext:`** — All terms in body.

```
intext:password
intext:"default credentials"
allintext:username password default
```

Edge cases:
- Excludes title, URL, metadata
- Useful when term appears in titles but you want body matches
- Rarely needed (default behavior is full-page search)

### Exact Match

**`"quotes"`** — Exact phrase matching.

```
"buffer overflow vulnerability"
"error: cannot find module"
"configuration file located at"
```

Edge cases:
- Punctuation usually ignored inside quotes
- Very long phrases may not match
- Hyphenated words: `"self-signed"` matches variations
- Can use multiple: `"term one" "term two"`

### Exclusion

**`-term`** — Exclude results containing term.

```
python -snake -monty
java -coffee -island
apple -fruit -cider
```

Edge cases:
- No space between minus and term
- Can exclude operators: `-site:pinterest.com`
- Can exclude phrases: `-"for beginners"`
- Multiple exclusions: `-term1 -term2 -term3`

### OR Operator

**`OR`** or **`|`** — Match either term.

```
python OR golang
(AWS OR Azure) certification
vulnerability | exploit
```

Edge cases:
- Must be uppercase: `OR` not `or`
- Pipe `|` is an alias
- Group with parentheses for complex logic
- Default is AND (all terms required)

### Wildcard

**`*`** — Single word wildcard.

```
"how to * in python"
"the * of *"
"* is considered harmful"
```

Edge cases:
- Matches one word (sometimes zero or multiple)
- Only works inside quotes
- Multiple wildcards: `"* * *"` (unreliable)
- Not a regex — simple word replacement

### Proximity

**`AROUND(n)`** — Terms within n words of each other.

```
CEO AROUND(3) resigned
climate AROUND(5) disaster
python AROUND(2) tutorial
```

Edge cases:
- Google-specific
- Order doesn't matter
- Must be uppercase
- Works with phrases: `"term one" AROUND(5) "term two"`
- n is maximum distance, not exact

### Date Operators

**`before:`** and **`after:`** — Date filtering.

```
before:2024-01-01
after:2023-06-15
after:2023-01-01 before:2023-12-31
```

Edge cases:
- Format: YYYY-MM-DD
- Based on Google's date detection (unreliable)
- Some pages have no date
- `daterange:` uses Julian dates (rarely used)

### Other Google Operators

**`related:`** — Similar sites.
```
related:stackoverflow.com
```

**`cache:`** — Google's cached version.
```
cache:example.com/page
```

**`define:`** — Dictionary definition.
```
define:idempotent
```

**`info:`** — Page info (deprecated, limited).
```
info:example.com
```

---

## Bing Operators

Bing shares most Google operators plus:

**`contains:`** — Page contains link to file type.
```
contains:pdf
contains:xls
```

**`loc:` / `location:`** — Geographic restriction.
```
loc:US
location:GB
```

**`language:`** — Page language.
```
language:en
language:de
```

**`prefer:`** — Boost term in ranking.
```
python tutorial prefer:advanced
```

**`feed:`** — Find RSS/Atom feeds.
```
feed:security news
```

**`ip:`** — Sites hosted on IP.
```
ip:93.184.216.34
```

**`url:`** — URL contains (alias for inurl).
```
url:documentation
```

Bing-specific notes:
- `near:` for proximity (like AROUND)
- `hasfeed:` finds pages with feeds
- Operators generally less reliable than Google

---

## DuckDuckGo Operators

DuckDuckGo supports basic operators plus bangs:

### Bangs (Direct Site Search)

```
!g term          # Google
!b term          # Bing
!gh term         # GitHub
!so term         # Stack Overflow
!w term          # Wikipedia
!yt term         # YouTube
!a term          # Amazon
!r term          # Reddit
!tw term         # Twitter/X
!scholar term    # Google Scholar
!arxiv term      # arXiv
!npm term        # npm registry
!pypi term       # PyPI
!mdn term        # MDN Web Docs
!man term        # Linux man pages
!wa term         # Wolfram Alpha
```

Over 13,000 bangs available. Format: `!shortcode query`

### DDG-Specific

**`region:`** — Region filter.
```
region:uk-en
region:de-de
```

**Sort modifiers** (in some contexts):
```
sort:date
```

---

## Operator Combination Rules

### Precedence
1. Quotes (highest)
2. Operators (site:, filetype:, etc.)
3. Exclusions
4. OR
5. Default AND (lowest)

### Grouping
Parentheses control evaluation:
```
(python OR golang) "web framework"        # Either language, exact phrase
python OR (golang "web framework")        # Different meaning
```

### Stacking
Multiple operators combine with AND:
```
site:github.com filetype:py intitle:scraper
```
Means: on github.com AND .py files AND "scraper" in title

### Limits
- Most engines: ~32 terms/operators max
- Very complex queries may be simplified by engine
- Some operator combinations ignored silently

---

## Common Gotchas

1. **Space after colon** — `site: example.com` fails; use `site:example.com`

2. **OR must be caps** — `or` treated as regular word

3. **Quotes break operators** — `"site:example.com"` searches for literal text

4. **Operators not in quotes** — `"filetype:pdf"` won't filter file type

5. **Subdomains vs domains** — `site:example.com` may or may not include subdomains

6. **Order can matter** — Put most restrictive operators first

7. **Engines differ** — Test syntax per engine; not all operators universal

8. **Cached behavior** — Same query may return different results over time

9. **Personalization** — Results vary by user, location, history

10. **Rate limiting** — Automated queries may be blocked
