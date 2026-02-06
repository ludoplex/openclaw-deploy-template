# Query Templates

Copy-paste templates for common search scenarios. Replace bracketed values.

## Technical Documentation

```
# Official docs for a product
site:docs.[product].com OR site:[product].io/docs "[feature]"

# ReadTheDocs projects
site:readthedocs.io "[library]" "[function]"

# GitHub documentation
site:github.com/[org]/[repo] inurl:docs "[topic]"

# API reference
"[product] API" inurl:reference OR inurl:docs "[endpoint]"

# Configuration guides
"[product]" (configuration OR config OR setup) filetype:md OR filetype:rst

# Man pages / CLI help
"[command]" (man page OR --help OR usage)
```

## Code Search

```
# Function implementation on GitHub
site:github.com "[function_name]" language:[lang] inurl:blob

# Code examples
"[library]" example OR sample OR demo filetype:[ext]

# Specific error message
"[exact error message]" site:github.com OR site:stackoverflow.com

# Package/module source
site:github.com "[package]" inurl:src OR inurl:lib filetype:[ext]

# Configuration files
"[tool]" (config OR rc OR settings) filetype:json OR filetype:yaml OR filetype:toml

# Gists and snippets
site:gist.github.com "[description]"
```

## Stack Overflow & Q&A

```
# Specific error
site:stackoverflow.com "[error message]" [language]

# How to do X
site:stackoverflow.com "how to" "[task]" [language] is:answer

# Best practices
site:stackoverflow.com "[topic]" "best practice" OR "recommended"

# Comparison questions
site:stackoverflow.com "[thing1]" vs OR versus "[thing2]"
```

## Security Research

```
# CVE lookup
site:nvd.nist.gov CVE-[YEAR]-[NUMBER]

# Vulnerability in product
("[product]" OR "[vendor]") (vulnerability OR CVE OR exploit)

# Proof of concept
"[CVE]" ("proof of concept" OR PoC OR exploit)

# Security advisories
site:[vendor].com/security OR inurl:advisory "[product]"

# Exploit database
site:exploit-db.com "[product]" [version]

# Bug bounty writeups
"[target]" ("bug bounty" OR writeup OR disclosed) site:hackerone.com OR site:medium.com
```

## Academic Research

```
# Recent papers on topic
"[topic]" filetype:pdf after:[YYYY-01-01]

# Papers from arXiv
site:arxiv.org "[topic]" "[method]"

# Google Scholar results
site:scholar.google.com "[topic]"

# Literature reviews
"[topic]" "literature review" OR "systematic review" filetype:pdf

# Citations to specific paper
"[paper title]" OR "[author] et al" -site:[original source]

# Theses and dissertations
"[topic]" (thesis OR dissertation) filetype:pdf site:edu

# Conference papers
"[topic]" (proceedings OR conference) "[conference name]" filetype:pdf
```

## Legal & Government

```
# US government documents
site:gov "[topic]" filetype:pdf

# Regulations
site:ecfr.gov OR site:federalregister.gov "[regulation]"

# SEC filings
site:sec.gov "[company]" (10-K OR 10-Q OR 8-K)

# Court cases
site:courtlistener.com OR site:casetext.com "[case name]"

# Patents
site:patents.google.com "[invention]" "[company]"

# FOIA documents
"[topic]" FOIA OR "freedom of information" filetype:pdf
```

## News & Current Events

```
# Major news sources
site:reuters.com OR site:apnews.com "[topic]" after:[YYYY-MM-DD]

# Excluding opinion pieces
"[topic]" -opinion -editorial -op-ed site:[news site]

# Press releases
"[company]" "press release" OR "announces" after:[YYYY-MM-DD]

# Specific date coverage
"[event]" after:[YYYY-MM-DD] before:[YYYY-MM-DD]

# News archives
site:archive.org "[topic]" "[year]"
```

## Products & Companies

```
# Company information
"[company]" (about OR overview OR profile) -jobs -careers

# Product reviews
"[product]" review -affiliate -sponsored after:[YYYY-01-01]

# Pricing information
"[product]" (pricing OR cost OR price OR "how much")

# Comparison
"[product1]" vs OR versus OR compared "[product2]"

# Employee insights
site:glassdoor.com OR site:levels.fyi "[company]"

# Startup funding
"[company]" (funding OR raised OR series) (million OR billion)
```

## Technical Troubleshooting

```
# Exact error lookup
"[exact error text]" (solution OR fix OR resolve OR solved)

# Logs/stack traces
"[key error fragment]" [technology] -site:github.com/issues

# Version-specific issues
"[product]" "[version]" (bug OR issue OR problem)

# Configuration errors
"[product]" (configuration error OR config OR misconfiguration) "[setting]"

# Dependency issues
"[package]" (dependency OR conflict OR incompatible) "[version]"
```

## Data & Statistics

```
# Datasets
"[topic]" dataset OR data filetype:csv OR filetype:json

# Statistics
"[topic]" statistics OR data "[year]" site:gov OR site:org

# Research data
"[topic]" "supplementary data" OR "raw data" filetype:xlsx OR filetype:csv

# APIs for data
"[topic]" API (free OR public OR open) data
```

## File Discovery

```
# PDFs on a topic
"[topic]" filetype:pdf -site:pinterest.com -site:scribd.com

# Spreadsheets
"[topic]" filetype:xlsx OR filetype:csv

# Presentations
"[topic]" filetype:pptx OR filetype:ppt

# Configuration files
"[product]" filetype:conf OR filetype:ini OR filetype:yaml

# Database dumps (careful with legality)
"[topic]" filetype:sql OR filetype:db

# Log files
"[product]" filetype:log
```

## Regional/International

```
# Country-specific
"[topic]" site:[country TLD]

# Language-specific
"[topic]" language:[lang code] site:[country]

# Regional news
"[topic]" site:[regional news site]

# Localized content
"[topic]" "[city]" OR "[country]"
```

## Social Media & Forums

```
# Reddit discussions
site:reddit.com/r/[subreddit] "[topic]"

# Hacker News
site:news.ycombinator.com "[topic]"

# Twitter/X (limited)
site:twitter.com OR site:x.com "[topic]" from:[username]

# Discord (indexed content)
site:discord.com "[topic]"

# Forum threads
"[topic]" (forum OR thread OR discussion) "[community]"
```

## Caching & Archives

```
# Cached version
cache:[URL]

# Wayback Machine
site:web.archive.org "[URL or topic]"

# Removed content
"[exact text]" site:archive.org OR site:archive.is
```
