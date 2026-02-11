# CRYSTAL CORP MASTER OPERATIONAL BLUEPRINT

**Version:** 1.0  
**Generated:** 2026-02-10  
**Status:** APPROVED FOR EXECUTION  
**Classification:** Internal — Mighty House Inc.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Final Tech Stack](#2-final-tech-stack)
3. [Architecture Diagram](#3-architecture-diagram)
4. [Implementation Roadmap](#4-implementation-roadmap)
5. [Budget](#5-budget)
6. [Revenue Model](#6-revenue-model)
7. [Risk Register](#7-risk-register)
8. [Operational Procedures](#8-operational-procedures)
9. [Escalation Matrix](#9-escalation-matrix)
10. [Success Criteria](#10-success-criteria)

---

## 1. Executive Summary

### What Is Crystal Corp?

Crystal Corp is an adult-oriented digital entertainment venture operating under Mighty House Inc., launching with its flagship product **Crystal Arcade** — a browser-based skill-based puzzle game featuring AI-generated pin-up artwork in a Gals Panic/Qix revival format.

### The Business Model

| Element | Description |
|---------|-------------|
| **Product** | Retro arcade puzzle game (Qix/Gals Panic style) with AI-generated pin-up image reveals |
| **Target Audience** | Adult (18+) gaming enthusiasts in NSFW gaming communities |
| **Monetization** | Subscription-first ($9.99/mo) with credit packs and direct purchases |
| **Distribution** | Web-only (self-hosted, no app stores) |
| **Legal Position** | Adult-positioned from day one with specialized payment processors |

### Why This Works

1. **Skill-based gameplay** avoids gambling/loot box regulations
2. **AI image generation** is 100x cheaper than LLM chat companions (~$0.001/image vs $0.10/chat exchange)
3. **Adult niche creates a moat** — mainstream competitors can't enter, specialized payment processors reduce freeze risk
4. **Pre-generated content libraries** eliminate real-time API costs
5. **Web-only distribution** bypasses app store gatekeepers

### Success Metrics

| Metric | 30-Day | 60-Day | 90-Day |
|--------|--------|--------|--------|
| **Monthly Revenue** | $500 | $1,200 | $2,000 |
| **Paying Subscribers** | 50 | 120 | 200+ |
| **Discord Community** | 200 | 500 | 1,000 |
| **Content Library** | 200 images | 400 images | 600 images |
| **Churn Rate** | <40% | <35% | <30% |

### Probability Assessment

Based on comprehensive market validation:

| Scenario | Probability | Revenue at Day 90 |
|----------|-------------|-------------------|
| **Best Case** | 25% | $2,500-3,000/mo |
| **Expected Case** | 50% | $1,000-2,000/mo |
| **Worst Case** | 25% | <$500/mo (pivot required) |

**Overall Go/No-Go:** ✅ **CONDITIONAL GO** — Viable if execution is strong and Vincent provides emergency escalation support.

---

## 2. Final Tech Stack

### 2.1 Component Summary

| Layer | Component | Version | Why Chosen |
|-------|-----------|---------|------------|
| **Domain** | Njalla | N/A | Maximum privacy — they own domain on your behalf |
| **DNS/CDN** | Cloudflare (free tier) | N/A | DDoS protection, fast DNS |
| **Asset CDN** | Bunny.net | N/A | Adult-friendly, $0.01/GB, great performance |
| **Web Server** | Caddy | 2.8+ | Auto-HTTPS, simple config, reverse proxy |
| **Static Site** | Astro | 4.x | Best Core Web Vitals, Content Collections for game catalog |
| **Game Engine** | Phaser 3 | 3.90+ | Full game framework, built-in touch, Graphics API for polygon masking |
| **Support (Chat)** | Chatwoot Cloud | N/A | $19/mo initially, migrate to self-hosted at scale |
| **Support (Voice)** | Vapi.ai | N/A | Voice AI platform with API LLM (latency-critical) |
| **LLM (Chat)** | Qwen 2.5 7B (Q4_K_M) | GGUF | Local, free, good enough for chat support |
| **LLM (Voice)** | Claude Haiku / Groq | API | Low latency required for voice |
| **LLM Server** | llama.cpp | Latest | OpenAI-compatible API, Metal acceleration |
| **Payments** | SubscribeStar.Adult (primary) | N/A | No upfront fees, adult-specialized |
| **Payments Backup** | CCBill (pre-approved) | N/A | Industry standard backup |
| **Crypto Backup** | NOWPayments | N/A | Emergency rail, 0.5% fees |
| **Email List** | Listmonk (self-hosted) | N/A | Free, independent of platforms |
| **Monitoring** | UptimeRobot + Fail2Ban | N/A | Free, essential security |
| **Backups** | Backblaze B2 + rclone | N/A | $0.005/GB, encrypted off-site |
| **Image Generation** | Stable Diffusion XL + LoRA | N/A | Local or RunPod, ~$0.001-0.02/image |

### 2.2 Dropped Components

| Component | Reason Dropped |
|-----------|----------------|
| **Squid Cache** | Playwright's built-in route blocking handles resource filtering — Squid adds complexity without benefit |
| **Self-hosted Chatwoot (MVP)** | Cloud version faster to deploy, migrate to self-hosted at 500+ users |
| **Local LLM for Voice** | Latency requirements (< 1 second) incompatible with local inference |

### 2.3 Version Specifications

```yaml
# Core Infrastructure
caddy: "2.8+"
astro: "^4.0.0"
phaser: "^3.90.0"
llama-cpp: "latest (build from source for Metal)"

# Python Dependencies
playwright: "^1.49.0"
pyobjc-framework-quartz: "^12.1"
llama-cpp-python: "latest (Metal wheel)"

# Image Generation
stable-diffusion: "SDXL / Illustrious / Pony v6"
lora-training: "kohya-ss latest"

# Node.js
node: "20.x LTS"
npm: "10.x"
```

---

## 3. Architecture Diagram

### 3.1 System Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CRYSTAL CORP INFRASTRUCTURE                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   INTERNET                                                                   │
│      │                                                                       │
│      ▼                                                                       │
│  ┌──────────────┐     ┌──────────────┐                                      │
│  │  Cloudflare  │────▶│   Bunny.net  │ (game assets, images)                │
│  │  (DNS/Proxy) │     │    (CDN)     │                                      │
│  └──────┬───────┘     └──────────────┘                                      │
│         │                                                                    │
│         ▼                                                                    │
│  ┌─────────────────────────────────────────────────────────────────┐        │
│  │                        M4 VM (Self-Hosted)                       │        │
│  │  ┌─────────────────────────────────────────────────────────┐    │        │
│  │  │                     CADDY (:443)                         │    │        │
│  │  │                   (Reverse Proxy)                        │    │        │
│  │  └─────────────────────┬───────────────────────────────────┘    │        │
│  │                        │                                         │        │
│  │          ┌─────────────┼─────────────┬─────────────┐            │        │
│  │          ▼             ▼             ▼             ▼            │        │
│  │   ┌───────────┐  ┌───────────┐  ┌─────────┐  ┌──────────┐      │        │
│  │   │  Astro    │  │  Phaser   │  │ Listmonk│  │ llama.cpp│      │        │
│  │   │  Website  │  │   Game    │  │ (Email) │  │  (:8080) │      │        │
│  │   └───────────┘  └───────────┘  └─────────┘  └──────────┘      │        │
│  │                                                                  │        │
│  └─────────────────────────────────────────────────────────────────┘        │
│                                                                              │
│   EXTERNAL SERVICES                                                          │
│   ┌────────────────┐  ┌────────────────┐  ┌────────────────┐                │
│   │ Chatwoot Cloud │  │    Vapi.ai     │  │ SubscribeStar  │                │
│   │  (Chat Support)│  │ (Voice Support)│  │   (Payments)   │                │
│   └───────┬────────┘  └───────┬────────┘  └───────┬────────┘                │
│           │                   │                   │                          │
│           └───────────────────┴───────────────────┘                          │
│                          │                                                   │
│                          ▼                                                   │
│                    WEBHOOKS TO M4                                            │
│                                                                              │
│   BACKUP / DR                                                                │
│   ┌────────────────┐  ┌────────────────┐  ┌────────────────┐                │
│   │  Backblaze B2  │  │  Oracle Cloud  │  │ CCBill (Backup)│                │
│   │  (Daily Backup)│  │ (Cold Standby) │  │   (Dormant)    │                │
│   └────────────────┘  └────────────────┘  └────────────────┘                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Request Flow

```
User Request: crystalarcade.gg/game/level-1
                    │
                    ▼
            Cloudflare (DNS)
                    │
                    ▼
            Caddy (:443) ─────► SSL termination
                    │
                    ▼
         ┌──────────┴──────────┐
         │                     │
    /game/*               /assets/*
         │                     │
         ▼                     ▼
    Phaser Game          Bunny CDN
    (local files)        (images, audio)
```

### 3.3 Support Flow

```
                    ┌─────────────────┐
                    │   Customer      │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
        Voice Call                      Chat Widget
              │                             │
              ▼                             ▼
        ┌──────────┐                 ┌──────────────┐
        │ Vapi.ai  │                 │Chatwoot Cloud│
        │  Phone   │                 │   Widget     │
        └────┬─────┘                 └──────┬───────┘
             │                              │
             │ webhook                      │ webhook
             ▼                              ▼
        ┌──────────────────────────────────────────┐
        │              M4 VM Webhook Server         │
        │  ┌─────────────────────────────────────┐ │
        │  │  Voice: Claude Haiku API (latency)  │ │
        │  │  Chat: Local Qwen 2.5 7B            │ │
        │  └─────────────────────────────────────┘ │
        └──────────────────────────────────────────┘
                             │
                             ▼
                    Response to User
```

### 3.4 Backup & Recovery Flow

```
M4 VM Daily Backup (3 AM):
┌───────────────────┐
│   Backup Script   │
│  (launchd cron)   │
└─────────┬─────────┘
          │
          ├──► tar + encrypt (/website)
          ├──► tar + encrypt (/configs)
          ├──► tar + encrypt (/chatwoot-data)
          │
          ▼
┌─────────────────┐
│   rclone sync   │
│   to B2 bucket  │
└─────────────────┘

RECOVERY (if M4 dies):
┌───────────┐    ┌───────────────┐    ┌──────────────┐
│ Vincent   │───▶│ DNS → Oracle  │───▶│ Restore from │
│ triggers  │    │ Cloud VM      │    │ B2 backups   │
└───────────┘    └───────────────┘    └──────────────┘
```

---

## 4. Implementation Roadmap

### 4.1 Phase Overview

| Phase | Weeks | Focus | Deliverable |
|-------|-------|-------|-------------|
| **Foundation** | 1-2 | Infrastructure + Legal | Server running, legal docs, domain |
| **Game MVP** | 3-4 | Core gameplay + 100 images | Playable demo |
| **Launch Prep** | 5-6 | Payments, marketing, beta | Beta users, payments working |
| **Launch** | 7-8 | Public launch, first revenue | Monetization live |
| **Growth** | 9-12 | Scale content, optimize | 200+ subscribers |

### 4.2 Week-by-Week Breakdown

#### WEEK 1: Foundation (Infrastructure)

| Day | Task | Owner | Deliverable |
|-----|------|-------|-------------|
| 1 | Register domain via Njalla (crystalarcade.gg or similar) | Peridot | Domain active |
| 1 | Configure Cloudflare DNS | Peridot | DNS pointing to M4 |
| 2 | Install Caddy, configure HTTPS | Peridot | HTTPS working |
| 2 | Set up Bunny CDN account | Peridot | CDN ready |
| 3 | Initialize Astro project | Peridot | Basic site live |
| 4 | Install llama.cpp, download Qwen 2.5 7B | Peridot | LLM running |
| 5 | Set up Backblaze B2, configure rclone | Peridot | Backups running |
| 6 | Install UptimeRobot, Fail2Ban | Peridot | Monitoring active |
| 7 | Document all configurations | Peridot | Runbook draft |

**Week 1 Milestone:** ✅ Infrastructure operational, basic site live at domain

#### WEEK 2: Foundation (Legal + Business)

| Day | Task | Owner | Deliverable |
|-----|------|-------|-------------|
| 8 | Apply for SubscribeStar.Adult account | Peridot | Application submitted |
| 8 | Apply for CCBill account (backup) | Peridot | Application submitted |
| 9 | Purchase ToS template (TermsFeed) | Peridot | ToS draft |
| 9 | Purchase Privacy Policy template | Peridot | Policy draft |
| 10 | Create age verification gate | Peridot | Gate implemented |
| 11 | Register DMCA designated agent | Peridot | $6 registration |
| 12 | Create 2257 compliance statement | Peridot | Statement ready |
| 13 | Set up Bitwarden, add Vincent emergency access | Peridot | Credentials shared |
| 14 | Write 00-EMERGENCY-START-HERE.md | Peridot | Runbook for Vincent |

**Week 2 Milestone:** ✅ Legal framework complete, payment applications submitted

#### WEEK 3: Game Development (Core Mechanics)

| Day | Task | Owner | Deliverable |
|-----|------|-------|-------------|
| 15-16 | Set up Phaser 3 project structure | Peridot | Project scaffold |
| 17-18 | Implement player movement system | Peridot | Player controls |
| 19 | Implement boundary detection | Peridot | Edge movement |
| 20 | Implement line drawing + polygon claiming | Peridot | Area capture |
| 21 | Test core loop on mobile | Peridot | Touch controls working |

**Week 3 Milestone:** ✅ Core Qix gameplay loop functional

#### WEEK 4: Game Development (Polish + Content)

| Day | Task | Owner | Deliverable |
|-----|------|-------|-------------|
| 22 | Implement image masking reveal system | Peridot | Progressive reveal |
| 23 | Add enemy (basic Qix) | Peridot | Single enemy |
| 24 | Add percentage tracking + win condition | Peridot | Level completion |
| 25-26 | Train first character LoRAs (3-5 characters) | Peridot | LoRAs ready |
| 27-28 | Generate first 100 images | Peridot | Initial library |

**Week 4 Milestone:** ✅ Playable game with 100 images

#### WEEK 5: Launch Preparation (Payments + Marketing)

| Day | Task | Owner | Deliverable |
|-----|------|-------|-------------|
| 29 | SubscribeStar approval received | — | Account active |
| 30 | Integrate SubscribeStar payment flow | Peridot | Payments working |
| 31 | Create Discord server | Peridot | Community home |
| 32 | Create F95zone developer account | Peridot | Account ready |
| 33 | Create Twitter/X NSFW account | Peridot | @CrystalArcade |
| 34 | Write launch announcement posts | Peridot | Content ready |
| 35 | Create email list via Listmonk | Peridot | Capture ready |

**Week 5 Milestone:** ✅ Payments integrated, marketing channels established

#### WEEK 6: Launch Preparation (Beta)

| Day | Task | Owner | Deliverable |
|-----|------|-------|-------------|
| 36 | Create F95zone game thread | Peridot | Thread live |
| 37 | Post first Twitter content | Peridot | Initial following |
| 38 | Invite beta testers (Discord, Reddit) | Peridot | 50-100 beta users |
| 39-40 | Collect feedback, fix critical bugs | Peridot | Polish pass |
| 41 | Set up Chatwoot Cloud account | Peridot | Support ready |
| 42 | Configure Vapi voice support | Peridot | Voice ready |

**Week 6 Milestone:** ✅ Beta complete, 50-100 users tested

#### WEEK 7: Public Launch

| Day | Task | Owner | Deliverable |
|-----|------|-------|-------------|
| 43 | Final polish, last bug fixes | Peridot | Release candidate |
| 44 | Update all legal pages, verify age gate | Peridot | Compliance check |
| 45 | **LAUNCH DAY** | Peridot | 🚀 LIVE |
| 46 | All-hands marketing push | Peridot | Maximum exposure |
| 47-49 | Monitor, respond to feedback, hotfix | Peridot | Stability |

**Week 7 Milestone:** ✅ PUBLIC LAUNCH — First revenue

#### WEEK 8: Post-Launch Stabilization

| Day | Task | Owner | Deliverable |
|-----|------|-------|-------------|
| 50-52 | Address critical feedback | Peridot | v1.1 patch |
| 53-54 | Generate 50 more images | Peridot | Content expansion |
| 55-56 | Analyze metrics, adjust pricing/content | Peridot | Data-driven decisions |

**Week 8 Milestone:** ✅ Stable operation, initial metrics analyzed

#### WEEKS 9-12: Growth Phase

| Week | Focus | Target |
|------|-------|--------|
| 9 | Content expansion (100 more images) | 300 total images |
| 10 | Marketing optimization | 100 subscribers |
| 11 | New characters (5 more) | 400 total images |
| 12 | Community events, Discord growth | 200 subscribers, 1000 Discord |

**Day 90 Milestone:** ✅ $2,000/month revenue target

---

## 5. Budget

### 5.1 Startup Costs (One-Time)

| Item | Cost | Notes |
|------|------|-------|
| Domain (Njalla, first year) | $25 | .gg TLD |
| ToS Template | $50 | TermsFeed |
| Privacy Policy Template | $30 | TermsFeed |
| DMCA Registration | $6 | Copyright Office |
| External SSD (local backup) | $60 | 1TB minimum |
| LoRA Training (cloud) | $50-100 | 5-7 characters |
| Initial Image Generation | $50-100 | 200 images on RunPod |
| **TOTAL STARTUP** | **$271-371** | |

### 5.2 Monthly Operating Costs

#### MVP Phase (0-100 users)

| Item | Low | High | Notes |
|------|-----|------|-------|
| Domain (amortized) | $2 | $2 | Annual ÷ 12 |
| Bunny CDN | $5 | $15 | Scales with traffic |
| Chatwoot Cloud | $19 | $19 | 1 agent |
| Voice API (Vapi + Claude) | $15 | $40 | Scales with calls |
| Backup Storage (B2) | $1 | $5 | 50GB encrypted |
| **Infrastructure Total** | $42 | $81 | |
| Contingency (20%) | $8 | $16 | Unexpected costs |
| **TOTAL MVP MONTHLY** | **$50** | **$97** | |

#### Growth Phase (100-500 users)

| Item | Low | High | Notes |
|------|-----|------|-------|
| Domain (amortized) | $2 | $2 | |
| Bunny CDN | $20 | $40 | More traffic |
| Chatwoot Cloud | $38 | $38 | 2 agents |
| Voice API | $40 | $100 | More calls |
| Backup Storage | $5 | $10 | More data |
| Ongoing Image Generation | $30 | $60 | New content |
| **Infrastructure Total** | $135 | $250 | |
| Contingency (20%) | $27 | $50 | |
| **TOTAL GROWTH MONTHLY** | **$162** | **$300** | |

### 5.3 Payment Processor Costs

| Processor | Rate | On $2K Revenue | On $5K Revenue |
|-----------|------|----------------|----------------|
| SubscribeStar.Adult | ~10% | $200 | $500 |
| CCBill (if needed) | ~14% | $280 | $700 |
| NOWPayments (crypto) | 0.5% | $10 | $25 |

### 5.4 Break-Even Analysis

| Monthly Cost | Revenue Required | Subscribers at $9.99 |
|--------------|------------------|----------------------|
| $100 (MVP) | $111 (after 10% fees) | 12 |
| $200 (Growth) | $222 | 23 |
| $300 (Scale) | $333 | 34 |

**Target $2K/month:**
- Gross: $2,222 (after fees)
- Subscribers needed: ~223 at $9.99/month

### 5.5 First Year Budget Summary

| Category | Amount | Notes |
|----------|--------|-------|
| Startup Costs | $350 | One-time |
| Operating (12 months avg $150) | $1,800 | Scales up |
| Payment Fees (on $15K revenue) | $1,500 | Estimate 10% |
| Contingency | $350 | 10% buffer |
| **TOTAL FIRST YEAR** | **$4,000** | Before revenue |

**Remaining from $1K Budget:** ~$650 after startup costs — covers 6-10 months of MVP operation.

---

## 6. Revenue Model

### 6.1 Revenue Streams

| Stream | Pricing | Model | Priority |
|--------|---------|-------|----------|
| **Subscription** | $9.99/month | Recurring | Primary |
| **Annual Subscription** | $79.99/year | Recurring (33% discount) | Secondary |
| **Credit Packs** | $4.99/50 plays | One-time | Casual users |
| **Character Packs** | $2.99-4.99 | One-time | Direct purchase |
| **Tips/Donations** | Variable | One-time | Community |

### 6.2 Subscription Tiers

```
FREE TIER (Lead Generation)
├── 3-4 showcase characters
├── Softcore content only
├── Limited plays (5/day)
├── Low-res gallery
└── Age-verified only

BASIC ($9.99/month)
├── All free tier content
├── 8-10 additional characters
├── Soft explicit content
├── Unlimited plays
├── Medium-res downloads
├── Ad-free experience
└── Discord role: Subscriber

PREMIUM ($19.99/month)
├── All basic tier content
├── All characters (18-20)
├── Full explicit content
├── High-res downloads
├── Early access (1 week)
├── Monthly exclusive sets
├── Request priority queue
└── Discord role: Premium

COLLECTOR ($39.99/month) — Future Phase
├── All premium content
├── 4K resolution
├── Behind-the-scenes
├── Character development input
├── Exclusive LoRAs
├── Custom request credits
└── Discord role: Collector
```

### 6.3 Revenue Projections

| Timeline | Subscribers | Avg Revenue/Sub | Monthly Revenue |
|----------|-------------|-----------------|-----------------|
| Day 30 | 50 | $9 net | $450 |
| Day 60 | 120 | $10 net | $1,200 |
| Day 90 | 200 | $10 net | $2,000 |
| Month 6 | 400 | $11 net | $4,400 |
| Month 12 | 800 | $12 net | $9,600 |

### 6.4 Conversion Funnel Targets

```
Visitors → Free Sign-ups → Paying Users → Retained Users
   │            │              │              │
   ▼            ▼              ▼              ▼
  100%         15%            8%            60%
  
Example at 1,000 monthly visitors:
├── 150 create free accounts
├── 12 become paying subscribers
├── 7 retained month-over-month
└── LTV: ~$60-80 per subscriber (6-8 month retention)
```

### 6.5 Key Revenue Metrics to Track

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Conversion (visitor → paid) | 5-8% | <3% |
| Monthly Churn | <30% | >40% |
| Average Revenue Per User | $10+ | <$8 |
| Customer Acquisition Cost | <$5 | >$10 |
| Lifetime Value | >$60 | <$40 |

---

## 7. Risk Register

### 7.1 Top 10 Risks with Mitigations

| # | Risk | Probability | Impact | Mitigation |
|---|------|-------------|--------|------------|
| **1** | **M4 VM Hardware Failure** | Medium | 🔴 Critical | Daily B2 backups, Oracle Cloud cold standby, static failover page |
| **2** | **SubscribeStar Account Termination** | Low | 🔴 Critical | CCBill pre-approved, NOWPayments crypto backup, independent email list |
| **3** | **Peridot Unavailable 72+ Hours** | Low | 🔴 Critical | Vincent runbooks, Bitwarden emergency access, documented procedures |
| **4** | **Payment Processor Freeze** | Low | 🔴 Critical | Dual-processor strategy, crypto rail, low chargeback rate |
| **5** | **Legal Challenge (jurisdiction)** | Low | 🟡 High | Wyoming LLC, registered agent, legal templates, escalation path |
| **6** | **Content Copied/Stolen** | High | 🟡 Medium | Watermarking, DMCA procedures, first-mover advantage, community moat |
| **7** | **Scaling Faster Than Infrastructure** | Medium | 🟡 Medium | Clear upgrade triggers, Oracle failover ready, CDN caching |
| **8** | **Voice API Latency Issues** | Medium | 🟡 Medium | Use Claude Haiku/Groq, fallback to chat-only |
| **9** | **Cloudflare TOS Concern** | Low | 🟡 Medium | Bunny DNS backup, self-hosted origin if needed |
| **10** | **Low User Traction** | Medium | 🟡 Medium | Pivot to image pack model, B2B licensing, merge with platform |

### 7.2 Risk Response Playbooks

#### Risk 1: M4 VM Failure

```
DETECTION: UptimeRobot alert OR manual check fails

IMMEDIATE (0-1 hour):
1. Vincent receives alert
2. Vincent follows 05-dns-failover.md runbook
3. Update DNS to static maintenance page (GitHub Pages)
4. Post status on Twitter/Discord

RECOVERY (1-24 hours):
1. Spin up Oracle Cloud ARM VM
2. Restore from B2 backup
3. Verify functionality
4. Update DNS to Oracle VM
5. Order replacement hardware if needed

POST-MORTEM:
1. Document failure cause
2. Improve detection
3. Update runbooks
```

#### Risk 2: SubscribeStar Termination

```
DETECTION: Account suspension notice OR payment failures

IMMEDIATE (0-4 hours):
1. Activate CCBill (pre-approved, dormant)
2. Email all subscribers: "Payment method changing"
3. Update website payment integration
4. Post on Discord/Twitter

MIGRATION (24-72 hours):
1. All subscribers manually re-subscribe on CCBill
2. Offer 1-month free for transition friction
3. Update all documentation
4. Consider crypto for resistant users

PREVENTION:
- Maintain low chargeback rate (<1%)
- Respond quickly to SubscribeStar inquiries
- Keep CCBill account warm (test transaction monthly)
```

#### Risk 3: Peridot Unavailable

```
IF PERIDOT UNAVAILABLE > 24 HOURS:

Vincent's Capability:
✅ Restart services (runbook 02)
✅ Process refunds (runbook 04)
✅ Post maintenance notices
✅ Contact emergency freelancer

Vincent CANNOT:
❌ Fix code bugs
❌ Generate new content
❌ Complex troubleshooting

ESCALATION:
1. If issue > Vincent's capability: Hire freelancer
2. Toptal/Upwork: "macOS DevOps emergency"
3. Budget: $100-300 per incident
4. Pre-identified contact: [TBD by Peridot]
```

### 7.3 Business Continuity

| Scenario | Survival Time | Actions Required |
|----------|---------------|------------------|
| M4 down, backup works | 4-24 hours | Failover to Oracle |
| M4 destroyed, no backup | 1-2 weeks | Rebuild from scratch |
| SubscribeStar terminates | 24-72 hours | CCBill activation |
| Peridot unavailable 1 week | 1 week | Auto-pilot + Vincent |
| Peridot unavailable 1 month | Variable | Hire replacement or wind down |
| Legal challenge | Weeks-months | Lawyer engagement |

---

## 8. Operational Procedures

### 8.1 Daily Tasks for Peridot

| Time | Task | Duration | Tool |
|------|------|----------|------|
| Morning | Check UptimeRobot dashboard | 2 min | Browser |
| Morning | Review Chatwoot tickets | 10-30 min | Chatwoot |
| Morning | Check SubscribeStar dashboard | 5 min | Browser |
| Morning | Review Vapi call summaries | 5 min | Vapi |
| Afternoon | Respond to Discord | 15-30 min | Discord |
| Evening | Post Twitter content | 10 min | Twitter |
| Evening | Check error logs (Caddy, llama.cpp) | 5 min | SSH |

**Total Daily Time:** 45-90 minutes

### 8.2 Weekly Tasks

| Day | Task | Duration | Notes |
|-----|------|----------|-------|
| Monday | Review weekly metrics | 30 min | Revenue, users, churn |
| Tuesday | F95zone thread update | 30 min | Progress, changelog |
| Wednesday | Generate new images (batch) | 2-4 hours | 20-30 images |
| Thursday | Content planning | 30 min | Next week's schedule |
| Friday | Community engagement | 1 hour | Discord event, poll |
| Saturday | Backup verification | 15 min | Test restore |
| Sunday | Week review, update docs | 30 min | Runbook updates |

**Total Weekly Time:** 6-8 hours additional

### 8.3 Monthly Tasks

| Task | Duration | Week |
|------|----------|------|
| macOS security updates | 1-2 hours | Week 1 |
| llama.cpp/dependency updates | 1 hour | Week 1 |
| Financial review | 30 min | Week 1 |
| Content audit (quality check) | 1 hour | Week 2 |
| New character development | 4-6 hours | Week 2-3 |
| Marketing campaign analysis | 30 min | Week 3 |
| Runbook review with Vincent | 30 min | Week 4 |
| Quarterly fire drill (Vincent test) | 1 hour | Month 3, 6, 9, 12 |

**Total Monthly Time:** 10-15 hours additional

### 8.4 Standard Operating Procedures (SOPs)

#### SOP-001: Processing a Refund

```
1. Receive refund request (Chatwoot/email)
2. Verify: User is actual subscriber
3. Check: Refund within policy (7 days, first-time)
4. Process via SubscribeStar:
   - Dashboard → Subscribers → Find user
   - Actions → Refund
5. Respond to user: Confirmation email
6. Log: Refund reason in tracking sheet
7. If pattern: Investigate root cause
```

#### SOP-002: Deploying a Content Update

```
1. Generate new images locally or via RunPod
2. Quality check: Reject artifacts, check consistency
3. Process: Upscale, watermark, export tiers
4. Upload to Bunny CDN: /assets/images/characters/{name}/
5. Update game data: /data/characters.json
6. Test locally: Images load correctly
7. Deploy: git push (Astro rebuilds)
8. Verify: Check live site
9. Announce: Discord + Twitter
10. Update F95zone thread
```

#### SOP-003: Responding to DMCA Notice

```
1. Receive notice (email/registered agent)
2. Log: Create ticket in tracking system
3. Evaluate: Is claim valid?
   - If our content: Impossible (AI-generated, we own)
   - If third-party claim on our work: Counter-notice
   - If user somehow uploaded infringing content: Remove
4. Remove content if required (within 24 hours)
5. Notify affected user
6. File counter-notice if frivolous
7. Document everything
8. If pattern: Consult lawyer
```

### 8.5 Automation Opportunities

| Task | Current | Automated Solution | Priority |
|------|---------|-------------------|----------|
| Backup | Manual script | launchd cron | Week 1 ✅ |
| Uptime alerts | Manual check | UptimeRobot | Week 1 ✅ |
| Image watermarking | Manual | Batch script | Week 4 |
| Twitter posting | Manual | Buffer/Hootsuite | Week 5 |
| Metrics dashboard | Manual spreadsheet | Grafana | Month 2 |

---

## 9. Escalation Matrix

### 9.1 Decision Authority

| Decision Type | Peridot | Vincent | External |
|---------------|---------|---------|----------|
| **Routine Operations** | ✅ Full authority | — | — |
| **Content Changes** | ✅ Full authority | — | — |
| **Pricing Changes** | ⚠️ Under $5 | ✅ Over $5 | — |
| **Refunds** | ✅ Under $50 | ✅ Over $50 | — |
| **New Features** | ✅ Planned | ⚠️ Unplanned major | — |
| **Legal Responses** | ⚠️ Template only | ✅ Custom | ✅ Lawyer |
| **Terminating Users** | ✅ TOS violations | ⚠️ Edge cases | — |
| **Infrastructure Changes** | ✅ Routine | ⚠️ Major (DNS, etc.) | — |
| **Hiring/Contractors** | — | ✅ Approve | — |
| **Major Pivots** | — | ✅ Decide | — |

### 9.2 Escalation Triggers

| Situation | Action | Who |
|-----------|--------|-----|
| Site down > 1 hour | Investigate, failover if needed | Peridot → Vincent |
| Chargeback rate > 0.5% | Review practices, adjust | Peridot |
| Chargeback rate > 1% | URGENT: Risk of processor termination | Peridot → Vincent |
| Legal notice received | Log, follow template, escalate if complex | Peridot → Vincent |
| Angry customer threatening lawsuit | Do not engage, escalate | Peridot → Vincent |
| Security breach suspected | Isolate, investigate, notify | Peridot → Vincent |
| Revenue drop > 20% month-over-month | Analyze, report | Peridot → Vincent |
| Peridot unavailable > 24 hours | Vincent takes over basic ops | Vincent |
| Peridot unavailable > 72 hours | Vincent hires emergency help | Vincent + Freelancer |

### 9.3 Contact Methods

| Priority | Method | Response Time |
|----------|--------|---------------|
| 🔴 Critical | Phone call to Vincent | Immediate |
| 🟡 Urgent | Telegram to Vincent | < 4 hours |
| 🟢 Normal | Email to Vincent | < 24 hours |
| ⚪ Informational | Weekly summary | Weekly |

### 9.4 Vincent's Emergency Capabilities

After completing runbook training, Vincent can:

| Task | Capability Level |
|------|------------------|
| Check if site is up | ✅ Full |
| Restart services (Caddy, llama.cpp) | ✅ With runbook |
| Failover DNS to backup | ⚠️ With explicit runbook |
| Process simple refunds | ✅ Full |
| Post maintenance notices | ✅ Full |
| Hire emergency freelancer | ✅ Full |
| Respond to legal notices | ⚠️ Template only |
| Fix code bugs | ❌ Cannot |
| Generate new content | ❌ Cannot |
| Complex troubleshooting | ❌ Cannot |

---

## 10. Success Criteria

### 10.1 Day 30 Checkpoint

| Category | Metric | Target | Minimum | Red Flag |
|----------|--------|--------|---------|----------|
| **Revenue** | MRR | $500 | $300 | < $150 |
| **Subscribers** | Paying users | 50 | 30 | < 15 |
| **Content** | Total images | 200 | 150 | < 100 |
| **Community** | Discord members | 200 | 100 | < 50 |
| **Marketing** | F95zone thread views | 5,000 | 2,000 | < 500 |
| **Operations** | Uptime | 99% | 95% | < 90% |
| **Support** | Avg response time | < 4 hours | < 12 hours | > 24 hours |

**Day 30 Go/No-Go Decision:**
- **GREEN:** All targets met → Continue as planned
- **YELLOW:** Minimum met, targets missed → Analyze and adjust
- **RED:** Below minimum → Emergency pivot discussion

### 10.2 Day 60 Checkpoint

| Category | Metric | Target | Minimum | Red Flag |
|----------|--------|--------|---------|----------|
| **Revenue** | MRR | $1,200 | $800 | < $500 |
| **Subscribers** | Paying users | 120 | 80 | < 50 |
| **Retention** | Month 1 → 2 churn | < 35% | < 45% | > 50% |
| **Content** | Total images | 400 | 300 | < 200 |
| **Community** | Discord members | 500 | 300 | < 150 |
| **Marketing** | Twitter followers | 500 | 300 | < 100 |
| **Operations** | Support satisfaction | > 80% | > 60% | < 50% |

**Day 60 Go/No-Go Decision:**
- **GREEN:** Growing toward $2K → Double down on marketing
- **YELLOW:** Growth stalled → Pivot content/pricing strategy
- **RED:** Declining or < minimum → Consider exit options

### 10.3 Day 90 Checkpoint (Final Target)

| Category | Metric | Target | Acceptable | Pivot Required |
|----------|--------|--------|------------|----------------|
| **Revenue** | MRR | $2,000 | $1,500 | < $1,000 |
| **Subscribers** | Paying users | 200 | 150 | < 100 |
| **Retention** | 90-day LTV | > $25 | > $20 | < $15 |
| **Content** | Total images | 600 | 500 | < 400 |
| **Community** | Discord members | 1,000 | 700 | < 400 |
| **Operations** | Uptime | 99.5% | 99% | < 98% |
| **Profitability** | Net margin | > 50% | > 30% | < 10% |

**Day 90 Outcomes:**

| Result | Next Steps |
|--------|------------|
| **🟢 Target Met ($2K MRR)** | Continue scaling, add premium tier, hire part-time support |
| **🟡 Acceptable ($1.5K MRR)** | Optimize conversion, add content, extend runway |
| **🟠 Below Target ($1-1.5K MRR)** | Analyze bottlenecks, consider pivot, reduce costs |
| **🔴 Pivot Required (< $1K MRR)** | Exit options: sell assets, content subscription only, merge with platform |

### 10.4 Exit Ramps (If Pivot Required)

| Option | Effort | Potential Return | Timeline |
|--------|--------|------------------|----------|
| **Sell Image Library** | Low | $500-2,000 | 2 weeks |
| **License Game Engine** | Medium | $200-500/license | 4 weeks |
| **Pure Subscription (no game)** | Medium | $500-1,500/mo | 4 weeks |
| **Merge with Platform** | High | Revenue share | 8 weeks |
| **Graceful Shutdown** | Low | $0 | 1 week |

---

## Appendices

### Appendix A: Character Launch Lineup (18 Characters)

**Free Tier (4 Characters)**

| Name | Archetype | Style | Niche Served |
|------|-----------|-------|--------------|
| Luna | Mysterious Stranger | Gothic anime | Alt/punk |
| Mika | Bubbly Idol | Bright anime | Mass appeal |
| Diana | Confident Temptress | Semi-realistic | Mature (28) |
| Jade | Athletic Tomboy | Stylized | Muscular women |

**Premium Flagship (3 Characters)**

| Name | Archetype | Style | Unique Angle |
|------|-----------|-------|--------------|
| Scarlett | Dominant Queen | Dark semi-real | Elegant BDSM-lite |
| Valentina | Mature Sophisticate | Painted | MILF (35) |
| Zara | Monster Girl | Fantasy anime | Demon queen |

**Premium Secondary (5 Characters)**

| Name | Archetype | Style |
|------|-----------|-------|
| Yuki | Shy Ingenue | Soft anime |
| Raven | Gothic Princess | Dark stylized |
| Nova | Sci-Fi Synthetic | Cyberpunk |
| Ivy | Nature Spirit | Fantasy |
| Carmen | Fiery Latina | Warm semi-real |

**Premium Tertiary (6 Characters)**

| Name | Archetype | Style |
|------|-----------|-------|
| Faye | Fairy/Elf | Ethereal |
| Storm | Punk Rebel | Gritty |
| Cleo | Egyptian Queen | Exotic |
| Rose | Classic Beauty | Vintage |
| Ember | Fire Elemental | Dramatic |
| Crystal | Ice Queen | Cool tones |

### Appendix B: Legal Compliance Checklist

- [ ] Wyoming LLC formed
- [ ] EIN obtained
- [ ] Registered agent service active
- [ ] Terms of Service published
- [ ] Privacy Policy published (GDPR/CCPA compliant)
- [ ] Age verification gate implemented
- [ ] DMCA designated agent registered ($6)
- [ ] 2257 compliance statement (if explicit content)
- [ ] Cookie consent banner
- [ ] SubscribeStar.Adult approved
- [ ] CCBill pre-approved (backup)
- [ ] Billing descriptor configured (discrete)

### Appendix C: Credential Locations

All credentials stored in Bitwarden vault "Crystal Corp Operations"

| Service | Credential Type | Emergency Access |
|---------|-----------------|------------------|
| Njalla | Login + 2FA | Vincent (72-hour delay) |
| Cloudflare | Login + 2FA | Vincent (72-hour delay) |
| Bunny CDN | Login + API key | Vincent (72-hour delay) |
| SubscribeStar | Login + 2FA | Vincent (72-hour delay) |
| CCBill | Login + 2FA | Vincent (72-hour delay) |
| M4 VM SSH | Key + passphrase | Vincent (secure file) |
| Discord | Login + 2FA | Peridot only |
| Twitter | Login + 2FA | Peridot only |
| Chatwoot | Login | Vincent (72-hour delay) |
| Vapi | API key | Vincent (72-hour delay) |
| Backblaze B2 | API key | Vincent (72-hour delay) |

### Appendix D: Quick Reference Commands

```bash
# Check service status
systemctl status caddy
ps aux | grep llama-server

# Restart services
sudo systemctl restart caddy
pkill -f llama-server && nohup llama-server ... &

# Check logs
tail -f /var/log/caddy/access.log
tail -f /tmp/llm-server.log

# Manual backup
./scripts/backup-now.sh

# Check disk space
df -h

# Check memory
top -l 1 | head -n 10
```

### Appendix E: Key URLs

| Service | URL |
|---------|-----|
| Production Site | https://crystalarcade.gg |
| SubscribeStar | https://subscribestar.adult/crystal-arcade |
| Discord | https://discord.gg/[invite-code] |
| F95zone Thread | https://f95zone.to/threads/crystal-arcade.[id] |
| Twitter | https://twitter.com/CrystalArcade |
| Chatwoot Dashboard | https://app.chatwoot.com |
| Vapi Dashboard | https://dashboard.vapi.ai |
| UptimeRobot | https://uptimerobot.com |

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-10 | Project Manager Agent | Initial comprehensive blueprint |

**Review Schedule:**
- Weekly: Peridot reviews operational sections
- Monthly: Vincent reviews risk/escalation sections
- Quarterly: Full document review and update

**Approval:**
- [ ] Vincent (Business Owner)
- [ ] Peridot (Operator)

---

*This document is the single source of truth for Crystal Corp operations. When in doubt, consult this blueprint.*
