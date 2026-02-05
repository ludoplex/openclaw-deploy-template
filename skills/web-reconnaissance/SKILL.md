---
name: web-reconnaissance
description: Tech stack recognition, URI/URL/URN analysis, markup language identification, and web technology fingerprinting. Activates when Claude processes search results, analyzes URLs, examines web content structure, identifies frameworks/CMSs/servers, or needs to understand web resource conventions. Covers HTTP headers, HTML meta patterns, microformats, structured data, file signatures, and technology indicators.
---

# Web Reconnaissance

Extract intelligence from web artifacts. URLs, headers, markup, and metadata reveal technology, structure, and intent.

## URI/URL/URN Fundamentals

### URI Structure
```
scheme://[userinfo@]host[:port]/path[?query][#fragment]
```

| Component | Intelligence Value |
|-----------|-------------------|
| Scheme | Protocol, security posture (http vs https) |
| Host | Infrastructure, CDN, cloud provider |
| Port | Non-standard = interesting (8080, 3000, 8443) |
| Path | Framework conventions, API versioning, CMS structure |
| Query | Parameters reveal backend logic, session handling |
| Fragment | Client-side routing (SPA indicator) |

### URL Path Patterns

| Pattern | Indicates |
|---------|-----------|
| `/wp-content/`, `/wp-admin/` | WordPress |
| `/sites/default/files/` | Drupal |
| `/media/`, `/static/`, `/assets/` | Django, generic |
| `/node_modules/`, `/_next/` | Node.js, Next.js |
| `/api/v1/`, `/api/v2/` | Versioned REST API |
| `/graphql` | GraphQL endpoint |
| `/.well-known/` | Standardized metadata (security.txt, etc.) |
| `/cdn-cgi/` | Cloudflare |
| `/__` prefix | Framework internals (Next.js, Nuxt) |
| `/pub/`, `/dist/`, `/build/` | Build artifacts |
| `.aspx`, `.asp` | ASP.NET / Classic ASP |
| `.php` | PHP |
| `.jsp`, `.do`, `.action` | Java (JSP, Struts) |
| `.cgi`, `.pl` | Perl CGI |
| `.cfm` | ColdFusion |

### Query Parameter Patterns

| Pattern | Indicates |
|---------|-----------|
| `?id=`, `?pid=`, `?uid=` | Database-driven, possible injection surface |
| `?page=`, `?p=` | Pagination, WordPress |
| `?utm_*` | Marketing tracking |
| `?fbclid=`, `?gclid=` | Facebook/Google ad tracking |
| `?token=`, `?key=`, `?api_key=` | Authentication tokens (sensitive) |
| `?redirect=`, `?next=`, `?url=` | Redirect parameter (SSRF/open redirect surface) |
| `?debug=`, `?test=` | Debug modes |
| `?v=`, `?ver=`, `?_=` | Cache busting |

### URN vs URL
- **URL**: Locator — where to find it
- **URN**: Name — persistent identifier, location-independent
- **URI**: Superset of both

URN examples:
```
urn:isbn:0451450523          # Book ISBN
urn:ietf:rfc:3986            # IETF RFC
urn:uuid:6e8bc430-...        # UUID
urn:oid:2.16.840...          # OID (X.500)
```

## HTTP Header Fingerprinting

### Server Headers

| Header | Intelligence |
|--------|--------------|
| `Server` | Web server (nginx, Apache, IIS, cloudflare) |
| `X-Powered-By` | Backend framework (PHP, ASP.NET, Express) |
| `X-AspNet-Version` | .NET version |
| `X-Generator` | CMS (WordPress, Drupal) |
| `Via` | Proxy chain |
| `X-Cache` | CDN cache status |
| `CF-Ray` | Cloudflare |
| `X-Amz-*` | AWS infrastructure |
| `X-Azure-*` | Azure infrastructure |
| `X-Vercel-*` | Vercel deployment |

### Security Headers (presence/absence)

| Header | Implication if Missing |
|--------|------------------------|
| `Strict-Transport-Security` | No HSTS, downgrade possible |
| `Content-Security-Policy` | XSS surface |
| `X-Frame-Options` | Clickjacking possible |
| `X-Content-Type-Options` | MIME sniffing |
| `X-XSS-Protection` | Legacy XSS filter |

### Cookie Attributes

| Attribute | Meaning |
|-----------|---------|
| `HttpOnly` | Not accessible via JS |
| `Secure` | HTTPS only |
| `SameSite` | CSRF protection |
| `__Host-` prefix | Strict security requirements |
| `__Secure-` prefix | Requires Secure flag |

Cookie names reveal frameworks:
- `PHPSESSID` → PHP
- `JSESSIONID` → Java
- `ASP.NET_SessionId` → .NET
- `connect.sid` → Express.js
- `_session_id` → Rails
- `csrftoken` → Django

## HTML/Markup Fingerprinting

### Meta Tags

```html




```

### Script/Link Patterns

| Pattern | Indicates |
|---------|-----------|
| `wp-includes`, `wp-content` | WordPress |
| `jquery.min.js` | jQuery (version in filename) |
| `react.production.min.js` | React |
| `vue.global.prod.js` | Vue.js |
| `angular.min.js`, `@angular` | Angular |
| `_next/static` | Next.js |
| `_nuxt/` | Nuxt.js |
| `gatsby-` | Gatsby |
| `bundle.js`, `main.chunk.js` | Webpack |
| `assets/application-*.js` | Rails asset pipeline |

### Data Attributes

| Attribute | Framework |
|-----------|-----------|
| `data-reactroot`, `data-reactid` | React |
| `ng-*`, `data-ng-*` | AngularJS |
| `v-*`, `:*`, `@*` | Vue.js |
| `data-turbo-*` | Hotwire/Turbo |
| `data-controller` | Stimulus |
| `x-data`, `x-bind` | Alpine.js |
| `hx-*` | HTMX |

### Comment Signatures

```html



```

## Structured Data & Microformats

### JSON-LD (Schema.org)
```html

{"@context": "https://schema.org", "@type": "Organization", ...}

```

Common types: `Organization`, `Product`, `Article`, `Person`, `Event`, `LocalBusiness`, `FAQPage`, `HowTo`, `Recipe`

### Microdata
```html

  Product Name

```

### Microformats (v2)
```html

  Name
  Website

```

Classes: `h-card`, `h-entry`, `h-event`, `h-feed`, `h-adr`, `h-geo`

### Open Graph
```html



```

### Twitter Cards
```html


```

### RDFa
```html

  Name

```

## File Format Signatures

### By Extension

| Extension | Format | Notes |
|-----------|--------|-------|
| `.html`, `.htm` | HTML | Check DOCTYPE for version |
| `.xhtml` | XHTML | XML-based HTML |
| `.xml` | XML | Check root element for type |
| `.json` | JSON | Check structure for API type |
| `.yaml`, `.yml` | YAML | Config files, CI/CD |
| `.toml` | TOML | Rust ecosystem, config |
| `.md`, `.markdown` | Markdown | Docs, READMEs |
| `.rst` | reStructuredText | Python docs |
| `.adoc` | AsciiDoc | Technical docs |
| `.tex` | LaTeX | Academic |
| `.svg` | SVG | Vector graphics (XML-based) |
| `.wasm` | WebAssembly | Binary, high-performance |

### By Content (Magic Bytes)

| Signature | Format |
|-----------|--------|
| `<!DOCTYPE html` | HTML5 |
| `<?xml` | XML family |
| `{` or `[` | JSON (likely) |
| `---` (YAML front matter) | Markdown with metadata |
| `%PDF` | PDF |
| `PK` | ZIP-based (docx, xlsx, epub, jar) |

## Technology Indicators by Domain

### Static Site Generators
- **Jekyll**: `_site/`, `_posts/`, `_layouts/`, `Gemfile`
- **Hugo**: `/posts/`, date-based URLs, `config.toml`
- **Gatsby**: `gatsby-*`, `__gatsby`
- **11ty**: `.eleventy.js`, `_includes/`
- **Astro**: `astro.config.mjs`, `/_astro/`

### JavaScript Frameworks
- **React**: `data-reactroot`, `__REACT_DEVTOOLS_*`
- **Vue**: `__VUE__`, `data-v-*` scoped styles
- **Angular**: `ng-version`, `_ngcontent-*`
- **Svelte**: `svelte-*` classes
- **Next.js**: `__NEXT_DATA__`, `/_next/`
- **Nuxt**: `__NUXT__`, `/_nuxt/`

### CMS Platforms
- **WordPress**: `/wp-content/`, `/wp-includes/`, `?p=`
- **Drupal**: `/sites/default/`, `/modules/`, `?q=`
- **Joomla**: `/components/`, `/modules/`, `/templates/`
- **Shopify**: `.myshopify.com`, `cdn.shopify.com`
- **Squarespace**: `static1.squarespace.com`
- **Wix**: `static.wixstatic.com`
- **Webflow**: `webflow.com`, `assets.website-files.com`

### E-commerce
- **Magento**: `/skin/`, `/js/mage/`, `PHPSESSID`
- **WooCommerce**: `/wp-content/plugins/woocommerce/`
- **Shopify**: `Shopify.theme`, `myshopify.com`
- **BigCommerce**: `bigcommerce.com/`
- **PrestaShop**: `/modules/`, `prestashop`

### Cloud/CDN Indicators
- **Cloudflare**: `cf-ray`, `__cfduid`, `cdn-cgi`
- **AWS CloudFront**: `x-amz-cf-*`, `.cloudfront.net`
- **Fastly**: `x-served-by`, `fastly`
- **Akamai**: `akamai`, `edgekey`
- **Vercel**: `.vercel.app`, `x-vercel-*`
- **Netlify**: `.netlify.app`, `x-nf-*`

## Reference Files

- `references/markup-taxonomy.md` — Complete markup language reference (HTML, XML, SGML, lightweight markup)
- `references/microformats-structured-data.md` — Detailed structured data patterns and extraction
- `references/tech-fingerprints.md` — Comprehensive technology signature database
