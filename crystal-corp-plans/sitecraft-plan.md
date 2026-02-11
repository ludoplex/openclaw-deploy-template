# Sitecraft Agent Plan — Crystal Corp Website & Legal

**Agent:** sitecraft  
**Phase:** Foundation (Weeks 1-2)  
**Focus:** Domain Registration, Astro Website, Legal Pages, Age Verification

---

## Scope

Register domain with privacy-focused registrar, build the Astro static site with all public pages, implement legal compliance (ToS, Privacy Policy, Age Gate), and create the marketing landing page for Crystal Arcade.

---

## Deliverables

| ID | Deliverable | Description |
|----|-------------|-------------|
| S1 | Domain registration | crystalarcade.gg via Njalla |
| S2 | Astro project | Static site with optimized Core Web Vitals |
| S3 | Landing page | Marketing homepage with value proposition |
| S4 | Age verification gate | 18+ confirmation before content access |
| S5 | Terms of Service | Legal ToS page (from template) |
| S6 | Privacy Policy | GDPR/CCPA compliant policy |
| S7 | 2257 compliance statement | Adult content compliance |
| S8 | DMCA page | Takedown procedure and agent info |
| S9 | Character showcase | Free tier character gallery |
| S10 | Email capture | Newsletter signup integration |

---

## Task Schedule

### Week 1: Domain & Site Foundation

| Day | Task | Hours | Output |
|-----|------|-------|--------|
| 1 | Register crystalarcade.gg via Njalla | 1 | Domain active |
| 1 | Configure Njalla to use Cloudflare nameservers | 1 | DNS delegation |
| 2 | Initialize Astro 4.x project | 2 | Project scaffold |
| 2 | Set up project structure (pages, components, layouts) | 2 | Clean architecture |
| 3 | Create base layout with header/footer | 3 | Responsive layout |
| 3 | Implement dark theme (adult gaming aesthetic) | 2 | Theme complete |
| 4 | Build landing page (hero, features, CTA) | 4 | Homepage live |
| 5 | Create character showcase gallery (free tier) | 3 | Gallery component |
| 5 | Implement lazy loading for images | 2 | Performance optimized |
| 6 | Build email capture component | 2 | Listmonk integration ready |
| 6 | Create "Coming Soon" game preview section | 2 | Teaser content |
| 7 | Test on mobile devices | 2 | Responsive verified |
| 7 | Optimize Core Web Vitals (LCP, CLS, FID) | 2 | 90+ Lighthouse score |

### Week 2: Legal & Compliance

| Day | Task | Hours | Output |
|-----|------|-------|--------|
| 8 | Purchase ToS template from TermsFeed | 1 | Template received |
| 8 | Customize ToS for Crystal Arcade | 3 | ToS page complete |
| 9 | Purchase Privacy Policy template | 1 | Template received |
| 9 | Customize Privacy Policy (GDPR + CCPA) | 3 | Privacy page complete |
| 10 | Implement age verification gate (modal/interstitial) | 4 | Age gate working |
| 10 | Add cookie consent banner | 2 | GDPR compliance |
| 11 | Create 2257 compliance statement page | 2 | 2257 page live |
| 11 | Register DMCA designated agent ($6) | 1 | Registration submitted |
| 12 | Create DMCA takedown page | 2 | DMCA page live |
| 12 | Add legal links to footer | 1 | Navigation complete |
| 13 | Create FAQ page | 3 | FAQ live |
| 14 | Final QA pass on all pages | 3 | All pages verified |
| 14 | Deploy to production via Caddy | 2 | Site live |

---

## Inputs Required

| Input | Source | Required By |
|-------|--------|-------------|
| Cloudflare nameservers | neteng agent | Day 1 |
| HTTPS working on domain | neteng agent | Day 4 |
| Listmonk API endpoint | ops agent | Day 6 |
| Character images (free tier) | webdev prep | Day 5 |
| Brand assets (logo, colors) | Design direction | Day 2 |

---

## Outputs Produced

| Output | Location | Consumer |
|--------|----------|----------|
| Domain (crystalarcade.gg) | Njalla | All agents |
| Static site files | /var/www/crystalarcade | neteng (Caddy) |
| Age gate implementation | Site-wide | webdev (game pages) |
| Legal pages | /terms, /privacy, /dmca, /2257 | ops (compliance) |
| Email capture endpoint | /api/subscribe | social (campaigns) |

---

## Success Criteria

| Criterion | Measurement | Target |
|-----------|-------------|--------|
| Domain active | DNS resolution | Resolves within 24h |
| Lighthouse score | PageSpeed Insights | 90+ performance |
| Mobile responsive | Manual testing | Works on iOS/Android |
| Age gate functional | User testing | Blocks without confirmation |
| Legal pages complete | Checklist | All 4 pages live |
| Email capture works | Test submission | Adds to Listmonk list |

---

## Handoff to Next Phase

**To webdev (Week 3):**
- Astro project structure and build system
- Age gate component (reuse for game pages)
- Character gallery component (extend for full game)
- Design system (colors, typography, components)

**To social (Week 5):**
- Landing page live for marketing links
- Email capture functional
- Character showcase for promotional content

**To ops (Week 5):**
- Legal pages for SubscribeStar application reference
- DMCA agent registration complete
- Cookie consent implementation

---

## Technical Specifications

### Astro Project Structure

```
crystal-arcade/
├── src/
│   ├── components/
│   │   ├── AgeGate.astro
│   │   ├── CharacterCard.astro
│   │   ├── EmailCapture.astro
│   │   ├── Header.astro
│   │   ├── Footer.astro
│   │   └── CookieConsent.astro
│   ├── layouts/
│   │   ├── BaseLayout.astro
│   │   └── LegalLayout.astro
│   ├── pages/
│   │   ├── index.astro
│   │   ├── characters.astro
│   │   ├── terms.astro
│   │   ├── privacy.astro
│   │   ├── dmca.astro
│   │   ├── 2257.astro
│   │   └── faq.astro
│   └── styles/
│       └── global.css
├── public/
│   ├── images/
│   └── fonts/
├── astro.config.mjs
└── package.json
```

### Design System

```css
:root {
  /* Colors - Dark Gaming Aesthetic */
  --color-bg: #0a0a0f;
  --color-surface: #1a1a24;
  --color-primary: #ff4d6d;
  --color-secondary: #7c3aed;
  --color-text: #f0f0f5;
  --color-muted: #888899;
  
  /* Typography */
  --font-display: 'Orbitron', sans-serif;
  --font-body: 'Inter', sans-serif;
  
  /* Spacing */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-4: 1rem;
  --space-8: 2rem;
}
```

---

## Risk Mitigations

| Risk | Mitigation |
|------|------------|
| Njalla unavailable | Alternative: Porkbun (also privacy-focused) |
| Template legal docs inadequate | Have lawyer review before launch (escalate to Vincent) |
| Age gate bypassed | Implement cookie + localStorage, add to game pages too |
| Poor Core Web Vitals | Optimize images via Bunny CDN, lazy load below fold |
