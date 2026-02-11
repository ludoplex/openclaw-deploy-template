# Crystal Corp - Domain & Website Requirements Analysis
**Date:** 2026-02-10  
**Purpose:** Comprehensive analysis of domain registration, hosting, and website stack options for Crystal Corp (adult gaming platform).

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Domain Selection](#domain-selection)
3. [Website Hosting Analysis](#website-hosting-analysis)
4. [Website Components](#website-components)
5. [Tech Stack Recommendations](#tech-stack-recommendations)
6. [Cost Breakdown](#cost-breakdown)
7. [Recommendations](#recommendations)

---

## Executive Summary

Crystal Corp requires a web presence for an adult-oriented gaming platform (Crystal Arcade). This creates unique requirements around:
- **Content-friendly hosting** (adult content policies)
- **Privacy-focused domain registration** (WHOIS protection)
- **Age verification** (legal compliance)
- **Payment integration** (SubscribeStar for adult-friendly payments)

**Key Finding:** Self-hosting on M4 VM is the **safest and most flexible option** for adult content. Most mainstream hosting platforms (Vercel, Netlify, GitHub Pages) have restrictive or ambiguous TOS that could result in account termination.

---

## Domain Selection

### Recommended Domain Names

| Priority | Domain | Use Case | Notes |
|----------|--------|----------|-------|
| 1 | `crystalcorp.gg` | Main corporate | Gaming-focused TLD, professional |
| 2 | `crystalarcade.com` | Game hosting | More memorable for players |
| 3 | `crystalcorp.io` | Tech alternative | Popular with tech/gaming |
| 4 | `crystal.games` | Premium option | Direct, but likely expensive |

### Alternative TLDs to Consider
- `.io` - Tech-focused, adult-friendly registrars available
- `.gg` - Gaming-specific, becoming industry standard
- `.games` - Descriptive, good for arcade branding
- `.xyz` - Cheap, privacy-friendly
- `.adult` / `.xxx` - Only if content requires explicit designation

### Registrar Comparison

| Registrar | Privacy | Adult-Friendly | Price (.com) | Price (.gg) | Notes |
|-----------|---------|----------------|--------------|-------------|-------|
| **Njalla** 🌟 | Excellent (owner) | ✅ Yes | €15/yr | €25/yr | Privacy-first, they own domain on your behalf |
| **Porkbun** | Free WHOIS privacy | ✅ Yes | ~$10/yr | ~$20/yr | Great value, phone support |
| **Gandi** | Free privacy | ✅ Yes | $11/yr | N/A | Long reputation, ethical stance |
| **Cloudflare** | Free privacy | ⚠️ Unclear | At-cost | At-cost | Good for DNS, not domain privacy leader |
| **Namecheap** | Free WhoisGuard | ⚠️ Mixed | ~$12/yr | ~$18/yr | Large, some adult content issues reported |

### 🌟 **Recommendation: Njalla**
- **True privacy**: Njalla owns the domain on your behalf (they're the registrant)
- **Crypto payments**: Bitcoin, Monero, etc. for additional privacy
- **No-questions policy**: Known for protecting controversial sites
- **Cost**: €15-25/year depending on TLD
- **URL**: https://njal.la/

### WHOIS Privacy Notes
- All recommended registrars offer free WHOIS privacy
- Njalla offers the strongest protection (they are the legal owner)
- For extra privacy: Pay with crypto, use privacy email (ProtonMail)

---

## Website Hosting Analysis

### ⚠️ TOS Analysis - Mainstream Platforms

#### **Vercel** - ❌ NOT RECOMMENDED
From their Acceptable Use Policy (Aug 2025):
> "Customers may not use a service for... any other **objectionable purpose**" (non-Enterprise plans)

- Vague "objectionable content" clause gives them wide discretion
- No explicit adult content prohibition, but risky
- Non-Enterprise accounts have stricter enforcement
- **Risk Level**: HIGH - Could terminate without warning

#### **Netlify** - ❌ NOT RECOMMENDED
- Standard "lawful purposes" language
- No explicit adult content policy found
- Remote storage/hosting restrictions
- **Risk Level**: MEDIUM-HIGH - Ambiguous policy

#### **GitHub Pages** - ❌ NOT RECOMMENDED
From GitHub Acceptable Use Policies:
> "We do not allow content that is **sexually obscene**"

- Explicit prohibition on sexually obscene content
- Linked to GitHub account (code hosting risk)
- **Risk Level**: VERY HIGH - Clear prohibition

#### **Cloudflare Pages** - ⚠️ PROCEED WITH CAUTION
- TOS focuses on security/abuse, not content type
- Section 2.7 (Acceptable Use) prohibits: unlawful content, viruses, phishing
- **No explicit adult content prohibition**
- Uses CDN/caching which may have separate policies
- **Risk Level**: MEDIUM - Best mainstream option IF content is legal

### ✅ Adult-Friendly Hosting Options

#### **Self-Hosted on M4 VM** - 🌟 RECOMMENDED
**Advantages:**
- Full control over content policies
- No third-party TOS restrictions
- Can run any stack (static, dynamic, game servers)
- Privacy control
- Cost-effective at scale

**Requirements:**
- Reverse proxy (nginx/Caddy) for SSL
- Cloudflare CDN (optional, for DDoS protection)
- Basic hardening (firewall, fail2ban)

**Setup:**
```
M4 VM → nginx/Caddy → Static files + API endpoints
         ↓
    Cloudflare CDN (optional, origin pull mode)
```

#### **Bunny.net CDN** - ✅ RECOMMENDED FOR CDN
- Privacy-focused, adult content allowed
- Pay-as-you-go: $0.01/GB (NA/EU), $0.03/GB (Asia)
- $1/month minimum
- Great for static assets, game files
- No explicit content restrictions in TOS

#### **Other Adult-Friendly Options**
| Provider | Type | Cost | Notes |
|----------|------|------|-------|
| **OrangeWebsite** | Shared/VPS | From $5/mo | Iceland-based, offshore |
| **FlokiNET** | VPS | From €7/mo | Iceland/Romania/Finland |
| **1984 Hosting** | VPS | From €5/mo | Iceland, privacy-focused |

---

## Website Components

### 1. Landing Page
**Purpose:** Corporate presence, brand introduction

**Requirements:**
- Clean, professional design
- Age gate before main content
- Links to arcade, subscription, support
- Legal pages (Terms, Privacy, 2257 compliance)

### 2. Game Hosting (Crystal Arcade)
**Purpose:** Host and serve games

**Requirements:**
- Static game file hosting (HTML5/WebGL/WASM)
- Game library/catalog system
- Save game sync (if applicable)
- Analytics tracking
- CDN for fast global delivery

**Technical Considerations:**
- Games likely 10-500MB each
- WebGL/WASM compatibility
- Progressive loading for large games
- Local storage/IndexedDB for saves

### 3. Account/Subscription Management
**Purpose:** User accounts, tier management

**Options:**

**A) SubscribeStar Integration (Recommended)**
- Redirect to SubscribeStar for payments
- Use SubscribeStar API for tier verification
- Keeps payment processing off your servers
- Adult-friendly payment processor

**B) Self-Hosted Auth + SubscribeStar**
- Basic auth system on your server
- Link accounts to SubscribeStar
- Query API for subscription status

**C) Full Custom (Complex)**
- Self-hosted auth + payments
- Requires PCI compliance
- Not recommended initially

### 4. Support Widget (Chatwoot)
**Purpose:** Customer support chat

**Chatwoot Options:**
| Plan | Cost | Features |
|------|------|----------|
| **Self-Hosted** | Free | Full features, your server |
| **Startup Cloud** | $19/agent/mo | 2 agents included, 300 AI credits |
| **Business Cloud** | $49/agent/mo | Advanced features, 500 AI credits |

**Recommendation:** Self-host on M4 VM
- Free
- Full control
- No content restrictions
- Already have infrastructure

**Self-Hosting Requirements:**
- Docker
- PostgreSQL
- Redis
- ~2GB RAM

### 5. Age Verification Gate
**Purpose:** Legal compliance (18+/21+ depending on jurisdiction)

**Implementation Options:**

**A) Simple Date Entry (Basic)**
- "Enter your birth date" form
- Stores verification in cookie/localStorage
- Low barrier, minimal friction
- Legally minimal but commonly accepted

**B) Checkbox Confirmation (Minimal)**
- "I confirm I am 18 or older"
- Store in localStorage
- Most common approach
- Legal minimum in most jurisdictions

**C) Third-Party Verification (Strict)**
- Services like AgeVerify, Yoti
- ID verification
- Required in some jurisdictions (e.g., UK Online Safety Bill)
- Expensive, high friction

**Recommendation:** Start with checkbox + cookie, with route-based protection. Prepare for stricter verification if regulations require it.

---

## Tech Stack Recommendations

### 🌟 Recommended Stack

```
┌─────────────────────────────────────────────────────┐
│                    FRONTEND                          │
├─────────────────────────────────────────────────────┤
│  Astro (Static Site Generator)                      │
│  - Islands architecture (partial hydration)          │
│  - 62% Core Web Vitals pass rate (best in class)    │
│  - Works with React/Vue/Svelte components           │
│  - Built-in image optimization                       │
│  - Content Collections for game catalog             │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│                    HOSTING                           │
├─────────────────────────────────────────────────────┤
│  M4 VM (Self-Hosted)                                │
│  - Caddy (auto-HTTPS, reverse proxy)                │
│  - Static files served directly                      │
│  - Chatwoot (Docker)                                │
│  - Optional: Bunny.net CDN for assets               │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│                 INTEGRATIONS                         │
├─────────────────────────────────────────────────────┤
│  SubscribeStar - Payments/Subscriptions             │
│  Chatwoot - Customer Support                        │
│  Cloudflare - DNS + DDoS protection (free tier)    │
└─────────────────────────────────────────────────────┘
```

### Static Site Generator Comparison

| Generator | Build Speed | Learning Curve | React Support | Best For |
|-----------|-------------|----------------|---------------|----------|
| **Astro** 🌟 | Fast | Medium | ✅ Yes | Content sites, optimal performance |
| Hugo | Fastest | Medium | ❌ No | Pure static, markdown blogs |
| Eleventy | Fast | Low | ⚠️ Plugin | Simple sites, flexibility |
| Next.js | Medium | Higher | ✅ Native | Apps requiring SSR |

**Recommendation:** Astro
- Best Core Web Vitals scores
- Content Collections perfect for game catalogs
- Islands architecture = fast pages with interactive components where needed
- Can use React components for complex UI (game cards, age gates)

### Authentication Approach

For SubscribeStar integration:

```javascript
// Simplified flow
1. User clicks "Subscribe" → Redirect to SubscribeStar
2. SubscribeStar handles payment
3. User returns with auth token/callback
4. Your site verifies subscription via SubscribeStar API
5. Grant access to gated content
```

**SubscribeStar API:**
- Provides subscription tier verification
- Webhook support for subscription changes
- 5% platform fee + ~5% payment processing

---

## Cost Breakdown

### Monthly Costs

| Item | Option A (Minimal) | Option B (Recommended) | Notes |
|------|-------------------|------------------------|-------|
| **Domain** | $1.25/mo ($15/yr) | $2.08/mo ($25/yr) | Njalla, .gg TLD |
| **Hosting** | $0 (M4 VM exists) | $0 | Already have infrastructure |
| **CDN** | $0 | $5-10/mo | Bunny.net for game assets |
| **SSL** | $0 | $0 | Let's Encrypt via Caddy |
| **Chatwoot** | $0 | $0 | Self-hosted |
| **Email** | $0-2/mo | $2/mo | Porkbun email or Proton |
| **DNS** | $0 | $0 | Cloudflare free tier |
| **SubscribeStar** | 5% of revenue | 5% of revenue | + ~5% payment processing |
| **TOTAL** | ~$1.25/mo | ~$7-12/mo | Plus % of revenue |

### One-Time/Setup Costs

| Item | Cost | Notes |
|------|------|-------|
| Domain registration | $15-25 | First year |
| SSL certificate | $0 | Let's Encrypt |
| Astro theme (optional) | $0-50 | Many free themes |
| Development time | Variable | DIY or contracted |

### Annual Projection

| Scenario | Year 1 Cost | Notes |
|----------|-------------|-------|
| **Minimal** | ~$40 | Domain + basic setup |
| **Recommended** | ~$120-180 | Domain + CDN + email |
| **Growth** | ~$300+ | Add more services as needed |

---

## Recommendations

### Phase 1: Foundation (Week 1-2)
1. **Register domain** via Njalla
   - Primary: `crystalarcade.gg` or `crystalcorp.gg`
   - Pay with crypto for privacy
   
2. **Set up DNS** via Cloudflare (free)
   - Point to M4 VM
   - Enable proxy for DDoS protection

3. **Configure M4 VM**
   - Install Caddy for auto-HTTPS
   - Set up static file serving
   - Docker for Chatwoot

### Phase 2: Website Development (Week 2-4)
1. **Initialize Astro project**
   ```bash
   npm create astro@latest crystal-corp
   ```

2. **Build core pages**
   - Landing page with age gate
   - Game catalog (Content Collections)
   - About/Legal pages
   - Support integration

3. **Integrate Chatwoot**
   - Self-host via Docker
   - Add widget to site

### Phase 3: Subscriptions (Week 4-6)
1. **Set up SubscribeStar** account
   - Configure tiers
   - Set up webhook endpoints

2. **Implement auth flow**
   - OAuth or redirect-based
   - Tier verification

3. **Gate premium content**
   - Subscriber-only games
   - Early access areas

### Architecture Diagram

```
                    ┌──────────────┐
                    │   Cloudflare │
                    │     (DNS)    │
                    └──────┬───────┘
                           │
                           ▼
┌──────────────────────────────────────────────────┐
│                    M4 VM                          │
├──────────────────────────────────────────────────┤
│  ┌────────────┐    ┌────────────────────────┐   │
│  │   Caddy    │───▶│   Static Files (Astro) │   │
│  │   :443     │    │   /var/www/crystal     │   │
│  └────────────┘    └────────────────────────┘   │
│        │                                         │
│        │           ┌────────────────────────┐   │
│        └──────────▶│   Chatwoot (Docker)    │   │
│                    │   :3000                 │   │
│                    └────────────────────────┘   │
└──────────────────────────────────────────────────┘
                           │
            ┌──────────────┴──────────────┐
            ▼                              ▼
    ┌──────────────┐              ┌──────────────┐
    │ SubscribeStar│              │  Bunny CDN   │
    │   (Payments) │              │   (Assets)   │
    └──────────────┘              └──────────────┘
```

---

## Risk Mitigation

### Content Policy Risks
- ✅ Self-hosting eliminates platform TOS concerns
- ✅ Njalla domain registration protects identity
- ✅ Cloudflare proxy hides origin IP
- ⚠️ Keep Cloudflare CDN use minimal (just DNS/proxy)

### Legal Compliance
- Implement age verification gate
- Maintain 2257 records if hosting user content
- Clear Terms of Service
- DMCA takedown process

### Technical Risks
- Regular backups of game files and database
- DDoS protection via Cloudflare
- Rate limiting on API endpoints
- Monitoring and alerting

---

## Next Steps

1. [ ] Confirm domain choice with stakeholders
2. [ ] Register domain via Njalla
3. [ ] Set up Cloudflare DNS
4. [ ] Configure M4 VM (Caddy + static hosting)
5. [ ] Initialize Astro project
6. [ ] Build age verification gate
7. [ ] Create landing page
8. [ ] Set up Chatwoot
9. [ ] Integrate SubscribeStar
10. [ ] Launch!

---

*Document prepared: 2026-02-10*  
*Research sources: Cloudflare TOS, Vercel TOS/AUP, GitHub AUP, Netlify AUP, Njalla, Porkbun, Bunny.net, Chatwoot, Astro.build, SubscribeStar*
