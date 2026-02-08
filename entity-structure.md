# MHI Entity Structure & SOPs

## Three Distinct Entities

### 1. Mighty House Inc. (MHI) — Parent Company
**Type:** EDWOSB (Economically Disadvantaged Woman-Owned Small Business)  
**Status:** HUBZONE certified  
**Focus:** Federal government contracting, IT Solutions  
**Address:** 977 Gilchrist St, Wheatland WY 82201  
**Domain:** mightyhouseinc.com (exists)

**GovCon Advantages:**
- EDWOSB sole-source up to $7M
- HUBZONE preference in federal contracts
- 8(a) potential pathway

**Owns:**
- Computer Store retail locations
- DSAIC (SaaS subsidiary)

---

### 2. Computer Store — Retail Brand
**Full Name:** Computer Store [City] Tech, Gaming and Learning Hub  
**Flagship:** Wheatland, WY (Store #001)  
**Phone:** (307) 331-1040  
**Domain:** computerstore.mightyhouseinc.com (planned subdomain)

**Service Lines (48 SOPs):**

| Section | Focus | SOPs |
|---------|-------|------|
| Section 1 | Customer-Facing/Front Desk | 8 |
| Section 2 | Repair Bench Procedures | 14 |
| Section 3 | Phone Activations/ISP | 5 |
| Section 4 | Gaming Center/Events | 6 |
| Section 5 | Learning Center/PearsonVUE | 5 |
| Section 6 | Trade-Ins/Sales | 3 |
| Section 7 | Commissions/Payroll | 4 |
| Section 8 | Risk Management/Legal | 8 |

**Revenue Streams:**
- Tech repair ($49-$179/service)
- Phone activations (carrier commissions)
- Gaming center (hourly/day pass)
- VR experiences
- Learning/tutoring ($25-$40/session)
- PearsonVUE testing (coming soon)
- Trade-ins and refurbished sales

**Expansion Plan 2025-2028 (School Choice States):**
- Wyoming: Wheatland ✓, Cheyenne, Casper, Gillette
- Colorado: Colorado Springs
- Arizona: Mesa, Gilbert
- Oklahoma: Tulsa
- Idaho: Boise, Meridian

**Operating Hours:**
- Mon-Thu: 10am-6pm
- Fri: 10am-7pm
- Sat: 10am-5pm
- Sun: Closed

---

### 3. DSAIC — SaaS/ML Entity
**Full Name:** Data Science Applications, Inc.  
**Type:** SaaS/ML products + IBM/Climb Channel reseller  
**Domain:** TBD (explicitly NOT .ai)  
**Independence:** Separate brand, MHI-backed financially

**SOPs (5 defined):**
- `dsaic_product_launch.yaml` — Product launch pipeline
- `dsaic_customer_onboarding.yaml` — New customer setup
- `dsaic_support_escalation.yaml` — Support tiers
- `dsaic_churn_prevention.yaml` — Retention workflows
- `dsaic_beta_program.yaml` — Beta user management

**Products (In Development):**
- Apeswarm (IDP/RAG platform)
- AI Governance tools

**Channel Partnerships:**
- IBM/Climb (account CU0043054170)

---

## Key Distinctions

| Aspect | MHI | Computer Store | DSAIC |
|--------|-----|----------------|-------|
| **Type** | Holding/GovCon | Retail/Service | SaaS |
| **Revenue** | Contracts | Walk-in + Local | Subscriptions |
| **Market** | Federal/DoD | Local consumers | Enterprise/Dev |
| **Location** | HQ only | Physical stores | 100% Remote |
| **Brand** | B2G formal | B2C friendly | B2B technical |

---

## Path to File: `C:\Users\user\.openclaw\workspace\sops\`
- `/mighty-house-inc/` — Master SOPs (48 total)
- `/computer-store/` — Store-specific automation triggers
- `/dsaic/` — SaaS workflow SOPs
- `/cross-entity/` — Shared procedures
- `/schema/` — SOP schema definitions
