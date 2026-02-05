# Microformats & Structured Data

Detailed patterns for structured data extraction and recognition.

## JSON-LD (Recommended by Google)

### Detection
```html

{
  "@context": "https://schema.org",
  "@type": "...",
  ...
}

```

### Common Types

#### Organization
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Company Name",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://twitter.com/company",
    "https://linkedin.com/company/..."
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+1-...",
    "contactType": "customer service"
  }
}
```

#### Article/BlogPosting
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "...",
  "author": {"@type": "Person", "name": "..."},
  "datePublished": "2024-01-15",
  "dateModified": "2024-01-16",
  "publisher": {"@type": "Organization", "name": "..."},
  "image": "..."
}
```

#### Product (E-commerce)
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "...",
  "image": "...",
  "offers": {
    "@type": "Offer",
    "price": "29.99",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "reviewCount": "120"
  }
}
```

#### FAQPage (Featured Snippets)
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "Question text?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Answer text."
    }
  }]
}
```

#### LocalBusiness
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "...",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "...",
    "addressLocality": "...",
    "postalCode": "..."
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "...",
    "longitude": "..."
  },
  "openingHours": "Mo-Fr 09:00-17:00"
}
```

#### BreadcrumbList (Navigation)
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [{
    "@type": "ListItem",
    "position": 1,
    "name": "Home",
    "item": "https://example.com"
  }, {
    "@type": "ListItem",
    "position": 2,
    "name": "Category",
    "item": "https://example.com/category"
  }]
}
```

### Intelligence Value

| Type | Reveals |
|------|---------|
| Organization | Company info, social profiles |
| Product | Pricing, availability, ratings |
| Article | Authorship, dates, publisher |
| LocalBusiness | Physical location, hours |
| Event | Dates, locations, pricing |
| Person | Contact info, social profiles |
| SoftwareApplication | App details, ratings, requirements |
| Recipe | Ingredients, nutrition, time |
| VideoObject | Duration, upload date, description |
| JobPosting | Employment details, salary |

## Open Graph Protocol

### Detection
```html

```

### Core Properties
```html







```

### Type-Specific Properties

#### Article
```html






```

#### Product
```html



```

#### Video
```html





```

### Facebook-Specific
```html


```

## Twitter Cards

### Detection
```html

```

### Card Types

#### Summary
```html





```

#### Summary Large Image
```html

```

#### Player (Video/Audio)
```html




```

## Microformats v2

### Detection
Classes prefixed with: `h-`, `p-`, `u-`, `dt-`, `e-`

### h-card (People/Orgs)
```html

  
  Name
  Organization
  Email
  +1-555-...
  
    City
    Country
  

```

### h-entry (Posts/Articles)
```html

  Post Title
  Jan 15, 2024
  Author Name
  
    Post content...
  
  Permalink

```

### h-event
```html

  Event Name
  June 15
  5pm
  
    Venue Name
  
  Description...

```

### h-feed
```html

  Feed Title
  ...
  ...

```

## RDFa

### Detection
Attributes: `vocab`, `typeof`, `property`, `resource`, `prefix`

```html

  Name
  Title
  Website

```

## Microdata

### Detection
Attributes: `itemscope`, `itemtype`, `itemprop`

```html

  Product Name
  $29.99
  

```

## Extraction Strategy

### Priority Order
1. JSON-LD (cleanest, most complete)
2. Microdata (inline, reliable)
3. RDFa (inline, verbose)
4. Microformats (class-based)
5. Open Graph (meta tags)
6. Twitter Cards (meta tags)

### Validation Tools
- Google Rich Results Test
- Schema.org Validator
- Facebook Sharing Debugger
- Twitter Card Validator
- Microformats parser (pin13.net/mf2/)
