# Markup Language Taxonomy

Complete reference for markup language identification and implications.

## Hierarchy

```
Markup Languages
├── SGML-based
│   ├── HTML (all versions)
│   ├── XHTML
│   └── XML
│       ├── SVG
│       ├── MathML
│       ├── RSS/Atom
│       ├── XSLT
│       ├── DocBook
│       └── Domain-specific (XAML, XBRL, etc.)
├── Lightweight Markup
│   ├── Markdown (and variants)
│   ├── reStructuredText
│   ├── AsciiDoc
│   ├── Textile
│   ├── Org-mode
│   └── Wiki markup (MediaWiki, etc.)
├── Data Serialization
│   ├── JSON
│   ├── YAML
│   ├── TOML
│   └── INI
└── Specialized
    ├── LaTeX/TeX
    ├── troff/groff
    └── PostScript
```

## HTML Versions

### Detection

| DOCTYPE | Version |
|---------|---------|
| `<!DOCTYPE html>` | HTML5 |
| `<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"...>` | HTML 4.01 Strict |
| `<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"...>` | HTML 4.01 Transitional |
| `<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0...>` | XHTML 1.0 |
| `<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1...>` | XHTML 1.1 |
| No DOCTYPE | Quirks mode (legacy) |

### Version Implications

| Version | Implication |
|---------|-------------|
| HTML5 | Modern site, likely uses CSS3, ES6+ |
| HTML 4.01 | Legacy, may have compatibility issues |
| XHTML | Strict XML parsing, older standards |
| Quirks mode | Very old, inconsistent rendering |

### HTML5 Feature Detection

Semantic elements indicate HTML5:
```html
, , , , , , , 
```

Modern APIs indicate contemporary development:
```html
, , ,  (inline)

data-* attributes
```

## XML Family

### Root Element Identification

| Root Element | Document Type |
|--------------|---------------|
| `<rss>` | RSS feed |
| `<feed>` (Atom namespace) | Atom feed |
| `<svg>` | SVG image |
| `<math>` | MathML |
| `<xsl:stylesheet>` | XSLT |
| `<book>`, `<article>` (DocBook ns) | DocBook |
| `<html>` (XHTML namespace) | XHTML |
| `<urlset>` | XML Sitemap |
| `<sitemapindex>` | Sitemap index |
| `<project>` | Maven POM |
| `<configuration>` | .NET config |
| `<manifest>` | Android manifest |
| `<plist>` | Apple property list |

### Namespace Indicators

| Namespace | Technology |
|-----------|------------|
| `http://www.w3.org/1999/xhtml` | XHTML |
| `http://www.w3.org/2000/svg` | SVG |
| `http://www.w3.org/1998/Math/MathML` | MathML |
| `http://www.w3.org/2005/Atom` | Atom |
| `http://www.sitemaps.org/schemas/sitemap/0.9` | Sitemap |
| `http://schemas.android.com/apk/res/android` | Android |
| `urn:oasis:names:tc:xliff:*` | XLIFF (localization) |

## Lightweight Markup

### Markdown Variants

| Variant | Identifier | Extensions |
|---------|------------|------------|
| CommonMark | Strict spec | Baseline |
| GFM | GitHub | Tables, task lists, autolinks |
| MDX | React ecosystem | JSX components |
| Obsidian | Note-taking | Wikilinks, callouts |
| R Markdown | Data science | Code execution |
| Pandoc | Universal | Citations, footnotes |
| MultiMarkdown | Academic | Metadata, citations |

Detection:
- `---` front matter → YAML metadata (Jekyll, Hugo, Astro)
- `+++` front matter → TOML metadata (Hugo)
- `{.class}` or `{#id}` → Attribute syntax (Pandoc, Kramdown)
- `:::` → Fenced divs (Pandoc, Obsidian)
- `[[wikilink]]` → Wiki-style links (Obsidian, Roam)
- `import`, `export` → MDX

### reStructuredText

Detection:
```rst
Title
=====

Subtitle
--------

.. directive::
   content

:field: value
```

Context: Python ecosystem (Sphinx, ReadTheDocs)

### AsciiDoc

Detection:
```asciidoc
= Document Title
Author Name
:toc:

== Section

[source,python]
----
code
----
```

Context: Technical documentation, Antora

## Data Formats

### JSON

Structure types:
```json
{"key": "value"}     // Object
["item1", "item2"]   // Array
```

Contextual identification:
- `package.json` → Node.js project
- `composer.json` → PHP Composer
- `*.json` in API response → REST API
- `manifest.json` → Browser extension, PWA

### YAML

Detection:
```yaml
key: value
list:
  - item1
  - item2
```

Context clues:
- `.github/workflows/*.yml` → GitHub Actions
- `docker-compose.yml` → Docker Compose
- `.gitlab-ci.yml` → GitLab CI
- `_config.yml` → Jekyll
- `mkdocs.yml` → MkDocs
- `ansible.yml`, `playbook.yml` → Ansible
- `values.yaml` → Helm
- `serverless.yml` → Serverless Framework

### TOML

Detection:
```toml
[section]
key = "value"

[[array]]
item = 1
```

Context clues:
- `Cargo.toml` → Rust project
- `pyproject.toml` → Python project (modern)
- `config.toml` → Hugo
- `netlify.toml` → Netlify config
- `.goreleaser.toml` → GoReleaser

## Specialized Markup

### LaTeX

Detection:
```latex
\documentclass{article}
\begin{document}
\section{Title}
\end{document}
```

Context: Academic papers, arXiv, Overleaf

### SVG (Inline)

Detection:
```html

  

```

Intelligence: Custom graphics, icons, animations, data visualization

## Template Languages

| Syntax | Language | Framework |
|--------|----------|-----------|
| `{{ variable }}` | Jinja2, Twig, Liquid, Handlebars, Django | Python, PHP, Ruby, JS |
| `<%= code %>` | ERB | Ruby/Rails |
| `<?php ?>` | PHP | PHP |
| `@directive` | Blade | Laravel |
| `#if`, `#each` | Handlebars, Svelte | JS |
| `{#if}`, `{:else}` | Svelte | Svelte |
| `v-if`, `v-for` | Vue template | Vue.js |
| `*ngIf`, `*ngFor` | Angular template | Angular |
| `{expression}` | JSX | React |

## Document Format Detection

### Office Documents (ZIP-based)

All are ZIP archives with specific internal structure:

| Format | Internal File |
|--------|---------------|
| `.docx` | `word/document.xml` |
| `.xlsx` | `xl/workbook.xml` |
| `.pptx` | `ppt/presentation.xml` |
| `.odt` | `content.xml` + `mimetype` |
| `.epub` | `META-INF/container.xml` |
| `.jar` | `META-INF/MANIFEST.MF` |

### PDF Structure

```
%PDF-1.7
...objects...
xref
trailer
%%EOF
```

Version in header indicates PDF spec version (1.0-2.0).
