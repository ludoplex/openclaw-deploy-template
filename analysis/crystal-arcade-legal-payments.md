# Crystal Arcade: Payment & Legal Infrastructure Deep Dive

**Research Date:** February 10, 2026  
**Status:** Comprehensive Analysis Complete

---

## Table of Contents
1. [CCBill Deep Dive](#1-ccbill-deep-dive)
2. [Epoch Comparison](#2-epoch-comparison)
3. [CCBill vs Epoch: Recommendation](#3-ccbill-vs-epoch-recommendation)
4. [Crypto Payment Options](#4-crypto-payment-options)
5. [Legal Document Templates](#5-legal-document-templates)
6. [Business Structure Optimization](#6-business-structure-optimization)
7. [Master Checklist & Timeline](#7-master-checklist--timeline)

---

## 1. CCBill Deep Dive

### Company Overview
- **Founded:** 1998, Tempe, Arizona
- **Specialization:** High-risk payment processing, adult industry leader
- **PCI Level 1 Compliant:** Yes
- **24/7/365 Support:** Yes

### Application Process Step-by-Step

**Step 1: Pre-Application Preparation**
- [ ] Have website built or mockups ready
- [ ] Gather all required documents (see below)
- [ ] Ensure content compliance (no prohibited categories)
- [ ] Prepare business entity documentation

**Step 2: Submit Online Application**
- Visit: https://ccbill.com/merchants
- Click "Apply Now"
- Complete merchant application form
- Upload all required documentation

**Step 3: Review & Underwriting (5-10 Business Days)**
- CCBill reviews application
- Content compliance review
- Risk assessment
- Bank approval process

**Step 4: Account Setup**
- Receive account credentials
- Configure payment forms (FlexForms)
- Set up Postback/Webhooks
- Complete integration testing

**Step 5: Go Live**
- Final review
- Enable live transactions

### Required Documents

| Document | Description | Format |
|----------|-------------|--------|
| Government ID | Valid driver's license or passport | Scan/Photo |
| Business License | If applicable | Scan |
| Articles of Incorporation/Organization | For LLCs/Corps | Scan |
| Certificate of Good Standing | If existing LLC (some states) | Scan |
| Bank Statement | Recent, showing account details | Scan |
| Voided Check or Bank Letter | For ACH setup | Scan |
| W-9 Form | For US businesses | PDF |
| Website URL | Live or staging site | URL |
| 2257 Compliance Statement | Required for adult content | Text/URL |
| Privacy Policy | Posted on website | URL |
| Terms of Service | Posted on website | URL |

### Timeline: Application to Live

| Phase | Duration | Notes |
|-------|----------|-------|
| Application Submission | Day 1 | Online form + docs |
| Initial Review | 2-3 days | Document verification |
| Underwriting | 3-5 days | Risk assessment |
| Bank Approval | 3-7 days | High-risk registration |
| Account Setup | 1-2 days | Credentials + config |
| Integration & Testing | 3-7 days | Depends on tech stack |
| **Total Timeline** | **2-4 weeks** | Typical range |

### Fee Structure (All Fees)

#### PSP (Payment Service Provider) Model - Recommended for New Merchants

| Fee Type | Amount | Notes |
|----------|--------|-------|
| **Headline Rate** | 10.8% - 14.5%+ | Varies by risk/volume |
| Setup Fee | $0 | No setup fee |
| Monthly Fee | $0 | No monthly minimum |
| Per-Transaction Fee | Included | In percentage rate |
| Chargeback Fee | $25-35 | Per disputed transaction |
| Refund Fee | $0-1 | Varies |
| Rolling Reserve | 5-10% | Held 180 days, returned |
| Currency Conversion | ~3% | For international |
| **Annual Visa/MC High-Risk Registration** | $1,450/year | **REQUIRED** |
| - Visa Portion | $950/year | Annual |
| - Mastercard Portion | $500/year | Annual |
| Wire Transfer (Payout) | $25-30 | Per transfer |
| ACH Payout | $0-5 | Preferred method |

#### ISO Model (Own Merchant Account) - For Established Merchants

| Fee Type | Amount |
|----------|--------|
| Interchange Plus | Interchange + 0.5-1.5% + $0.10-0.30 |
| Monthly Fee | $50-200 |
| Gateway Fee | $0.05-0.10/transaction |
| PCI Compliance Fee | $99/year |

### Chargeback Handling Policies

**CCBill's Approach:**
- **Chargeback Threshold:** Must maintain below 1% ratio
- **Monitoring Program:** Automatic enrollment if >0.9%
- **Tools Provided:**
  - Ethoca/Verifi CDRN (prevention alerts)
  - RDR (Rapid Dispute Resolution) - auto-refund to prevent chargebacks
  - VScrub fraud detection
  - Web Verify user verification

**Chargeback Fees:**
- Initial chargeback: $25
- Additional fees if lost: $10-25
- Arbitration fee (if escalated): $250-500

**Best Practices:**
- Clear billing descriptors (avoid "adult" terminology)
- Strong customer service
- Easy cancellation process
- Robust age verification

---

## 2. Epoch Comparison

### Company Overview
- **Founded:** 1996, Los Angeles, California
- **Specialization:** Adult payment processing pioneer
- **PCI DSS Level 1:** Yes (first certified in 2002)
- **Support:** 24/7/365

### Application Process

**Step 1: Online Sign-Up**
- Visit: https://epoch.com/business_services/contract_initiation.html
- Complete form with business details
- **Response within 24 hours**

**Step 2: Documentation**
- Similar to CCBill requirements
- Website review
- Business verification

**Step 3: Contract & Go-Live**
- Faster approval process (reported)
- 1-2 weeks typical

### Required Documents
Same as CCBill, plus:
- Proof of business location (US or EU required)
- For EU: At least one principal must reside in EU

### Fee Structure (All Fees)

#### Tiered Volume-Based Pricing

| Weekly Volume | Processing Rate |
|---------------|-----------------|
| $0 - $5,000 | 15.00% |
| $5,001 - $7,000 | 14.75% |
| $7,001 - $9,000 | 14.50% |
| $9,001 - $12,000 | 14.25% |
| $12,001 - $15,000 | 14.00% |
| $15,001 - $20,000 | 13.75% |
| $20,001 - $25,000 | 13.50% |
| $25,001 - $35,000 | 13.25% |
| $35,001 - $45,000 | 13.00% |
| $45,001+ | Contact for custom |

#### Other Fees

| Fee Type | Amount | Notes |
|----------|--------|-------|
| Setup Fee | $0 | None |
| Monthly Fee | $0 | None |
| Transaction Fee | $0 | None (included in %) |
| Decline Fee | $0 | None |
| Maintenance Fee | $0 | None |
| Credit/Refund | $1 | Per refund |
| Chargeback | $12.50 | Per chargeback |
| **Visa/MC Registration** | $1,450 | First year |
| **Annual Renewal** | $1,450 | Each year |
| Reserve/Deposit | **$0** | **No reserve!** |

### Key Differentiator: NO RESERVE
Unlike most processors, Epoch does not hold a rolling reserve. This is a significant cash flow advantage.

---

## 3. CCBill vs Epoch: Recommendation

### Comparison Matrix

| Factor | CCBill | Epoch | Winner |
|--------|--------|-------|--------|
| **Starting Rate** | 10.8-14.5% | 15% | CCBill |
| **Volume Discounts** | Negotiable | Automatic | Epoch |
| **Rolling Reserve** | 5-10% (180 days) | **None** | **Epoch** |
| **Chargeback Fee** | $25-35 | $12.50 | Epoch |
| **Refund Fee** | $0-1 | $1 | Tie |
| **Setup Time** | 2-4 weeks | 1-2 weeks | Epoch |
| **Visa/MC Reg** | $1,450/year | $1,450/year | Tie |
| **Integration Docs** | Excellent | Good | CCBill |
| **API Quality** | Modern, RESTful | Older, functional | CCBill |
| **Support** | 24/7, Excellent | 24/7, Good | CCBill |
| **Industry Reputation** | Top Tier | Established | Tie |
| **Gaming-Specific** | Yes | Yes | Tie |

### Recommendation for Crystal Arcade

**Primary Processor:** Start with **Epoch**

**Reasons:**
1. **No Reserve:** Critical for a new gaming platform with uncertain cash flow
2. **Faster Approval:** Get to market faster
3. **Lower Chargeback Fees:** Gaming can have higher dispute rates
4. **Automatic Rate Drops:** As volume grows, rates automatically improve

**Secondary Processor:** Add **CCBill** at $15K+/month volume

**Reasons:**
1. Superior integration documentation
2. Better fraud tools
3. Geographic redundancy
4. Better conversion rates (reported)

### Dual-Processor Strategy
Consider running both processors with a failover system:
- Primary: Epoch (main volume)
- Secondary: CCBill (backup + specific geo regions)
- This provides redundancy and negotiating leverage

---

## 4. Crypto Payment Options

### Recommended: NOWPayments

**Why NOWPayments for Adult/Gaming:**
- Explicitly supports adult industry
- No KYB required for crypto-only
- 300+ cryptocurrencies
- 0.5% fee (lowest in industry)
- Fiat on-ramp coming

**Integration Complexity:** Low-Medium
- REST API available
- Webhooks for payment confirmation
- Pre-built widgets available
- ~1-2 days integration time

**Application:** https://nowpayments.io/all-solutions/adult
- Instant account creation
- No documents needed for crypto-only
- KYB required for fiat features

### Alternative: BitPay (Less Recommended)

**Considerations:**
- More compliance requirements
- May restrict adult content
- Better for mainstream businesses
- Good fiat conversion

**Integration:** https://developer.bitpay.com/docs/bitpay-integration-guide

### SpankPay/SpankChain Update

**Status:** SpankPay has pivoted - now SpankChain focuses on:
- Legislative advocacy
- Industry education
- Regulatory guidance
- No longer a payment processor

**Do NOT use for payments**

### Crypto Usage Statistics

**Industry Estimates (Adult/Gaming):**
- 2-5% of users currently pay with crypto
- Growing 15-20% annually
- Higher adoption in:
  - Privacy-conscious markets
  - Regions with banking restrictions
  - Tech-savvy gaming communities

**Recommendation:** Implement as optional, not primary

### Fiat Offramp Solutions

| Service | Notes |
|---------|-------|
| **NOWPayments** | Auto-convert to stablecoin or fiat |
| **Kraken OTC** | For larger volumes ($100K+) |
| **Coinbase Commerce** | Less adult-friendly, verify terms |
| **Exchange Direct** | Use any major exchange |

**Strategy:**
1. Receive crypto payments via NOWPayments
2. Auto-convert to USDC (stablecoin)
3. Offramp via Kraken or similar exchange
4. Transfer to business bank account

---

## 5. Legal Document Templates

### 5.1 Terms of Service (ToS) - Required Provisions for Adult Games

```markdown
## TERMS OF SERVICE - CRYSTAL ARCADE

### 1. AGE VERIFICATION & ELIGIBILITY
- You must be at least 18 years old (or 21 in some jurisdictions)
- You represent and warrant that you meet the minimum age requirement
- We reserve the right to verify your age at any time
- Misrepresentation of age is grounds for immediate termination

### 2. CONTENT DESCRIPTION
- This platform contains adult-oriented content
- Content may include [specific content types]
- Content is intended for mature audiences only

### 3. SUBSCRIPTION & BILLING
- Subscription terms: [monthly/annual/etc.]
- Auto-renewal notice: Subscriptions auto-renew unless cancelled
- Cancellation policy: [X days notice required]
- Refund policy: [Clearly state policy]
- Billing descriptor: [What appears on statement]

### 4. PROHIBITED CONDUCT
- No sharing of account credentials
- No unauthorized recording or redistribution
- No harassment of other users or creators
- Compliance with all applicable laws

### 5. INTELLECTUAL PROPERTY
- All content is copyrighted
- DMCA compliance (see separate policy)
- User-generated content licenses

### 6. LIMITATION OF LIABILITY
- Service provided "as is"
- No warranties, express or implied
- Maximum liability limited to fees paid

### 7. DISPUTE RESOLUTION
- Arbitration clause (if desired)
- Governing law: [State]
- Venue: [Location]

### 8. 18 U.S.C. § 2257 COMPLIANCE
- Records maintained pursuant to 18 U.S.C. § 2257
- Custodian of Records information

### 9. CONTACT INFORMATION
- Legal entity name
- Address (may use registered agent)
- Email for legal notices
```

### 5.2 DMCA Safe Harbor Requirements

**Required Elements for Section 512 Protection:**

#### A. Designated Agent Registration
- Register with U.S. Copyright Office: https://www.copyright.gov/dmca-512/
- Fee: $6 online filing
- Renewable every 3 years
- Must be public on website

#### B. Website Requirements

**1. DMCA Policy Page (Required Text):**

```markdown
## DMCA NOTICE AND TAKEDOWN PROCEDURE

### Notification of Infringement

If you believe that content available on Crystal Arcade infringes your 
copyright, please send a notification containing the following:

1. A physical or electronic signature of the copyright owner or authorized agent
2. Identification of the copyrighted work(s) claimed to be infringed
3. Identification of the material to be removed with sufficient information 
   to locate it (URL or description)
4. Your contact information (address, phone number, email)
5. A statement that you have a good faith belief the use is not authorized
6. A statement, under penalty of perjury, that the information is accurate 
   and you are authorized to act on behalf of the copyright owner

### Designated Agent

DMCA Designated Agent
[Company Legal Name]
[Address Line 1]
[City, State ZIP]
Email: dmca@crystalarcade.com
Phone: [Number]

### Counter-Notification

If you believe content was removed in error, you may submit a counter-notice 
containing:

1. Your physical or electronic signature
2. Identification of removed material and its former location
3. Statement under penalty of perjury that removal was due to mistake
4. Your name, address, phone number
5. Consent to jurisdiction of federal court
6. Agreement to accept service of process

### Repeat Infringer Policy

We will terminate accounts of repeat infringers in appropriate circumstances.
```

#### C. Takedown Procedure

1. Receive DMCA notice → Log in tracking system
2. Review for completeness (10-14 day deadline)
3. Remove content expeditiously
4. Notify uploader of takedown
5. Wait for counter-notice (10-14 days)
6. Restore if valid counter-notice and no lawsuit
7. Document everything

### 5.3 Age Verification Legal Standards by Jurisdiction

#### United States

| State | Requirement | Effective Date |
|-------|-------------|----------------|
| **Louisiana** | Government ID verification required | Jan 1, 2023 |
| **Utah** | Age verification law | May 2023 |
| **Arkansas** | Digital ID or commercial verification | July 2023 |
| **Virginia** | Reasonable verification required | July 2023 |
| **Mississippi** | Age verification required | July 2023 |
| **Montana** | Commercial age verification | Oct 2023 |
| **North Carolina** | Reasonable verification | Jan 2024 |
| **Texas** | Government ID verification | Sept 2023 |
| **Indiana** | Age verification | July 2024 |
| **Idaho** | Age verification | July 2024 |
| **Kansas** | Age verification | July 2024 |
| **Florida** | Age verification | Jan 2025 |
| **Tennessee** | Age verification | July 2024 |
| **Nebraska** | Age verification | Oct 2024 |

**Federal:** No federal mandate yet, but proposed legislation pending

**Compliance Options:**
1. **Age-Gate Declaration** (Weakest - not sufficient in regulated states)
2. **Credit Card Verification** (Moderate - card = 18+)
3. **Third-Party Age Verification** (Best)
   - VerifyMyAge (KJM approved, PAS 1296 certified)
   - AgeID
   - Yoti
   - CCBill's built-in verification

**Recommended Approach:**
- Use third-party verification for regulated states
- Geofence and block regulated states if verification not ready
- Credit card as baseline verification for other states

#### European Union

| Requirement | Status |
|-------------|--------|
| Age verification | Varies by country |
| GDPR compliance | Required |
| Digital Services Act | Effective Feb 2024 |

**UK:** Age Verification Guide (BBFC) - pending implementation

### 5.4 18 U.S.C. § 2257 Statement Template

**Display on every page with adult content (footer link acceptable):**

```markdown
## 18 U.S.C. § 2257 RECORD-KEEPING REQUIREMENTS COMPLIANCE STATEMENT

All models, actors, actresses and other persons that appear in any visual 
depiction of actual sexually explicit conduct appearing or otherwise contained 
in or at this website were over the age of eighteen (18) years at the time of 
the creation of such depictions.

All content and images are in full compliance with the requirements of 
18 U.S.C. § 2257 and associated regulations.

Records required pursuant to 18 U.S.C. § 2257 and 28 C.F.R. Part 75 are kept 
by the Custodian of Records at the following location:

**Custodian of Records**
[Legal Name of Custodian]
[Street Address - Must be physical address, not PO Box]
[City, State ZIP Code]

A physical copy of each performer's proof of age is kept at this location.
Records are available for inspection during normal business hours.

[Platform Name] is not a producer of any visual depictions that require the 
maintenance of records pursuant to 18 U.S.C. § 2257. As a platform that hosts 
user-generated content, we are a secondary producer under 18 U.S.C. § 2257A 
and require all uploaders to maintain their own records.
```

**Record Requirements:**
- Copy of government ID for each performer
- Real name and stage name index
- Searchable database
- Physical records kept for 5 years post last publication
- Available for federal inspection

**Note for Crystal Arcade:** If using AI-generated content exclusively:
- 2257 may not apply to purely fictional/AI characters
- Consult attorney for specific guidance
- Still recommended to have statement disclaiming real performers

---

## 6. Business Structure Optimization

### 6.1 Wyoming LLC Advantages

**Why Wyoming for Adult Business:**

| Advantage | Details |
|-----------|---------|
| **Privacy** | Members not listed publicly |
| **No State Income Tax** | 0% state income tax |
| **Asset Protection** | Strong charging order protection |
| **Low Fees** | $100 formation, $60/year annual report |
| **Minimal Requirements** | No annual meetings required |
| **Perpetual Duration** | No sunset clause |
| **Series LLC Available** | Separate liability for assets |
| **Crypto-Friendly** | Progressive crypto legislation |
| **No Franchise Tax** | Unlike Delaware |

**Formation Process:**
1. Wyoming Secretary of State: https://sos.wyo.gov/
2. Articles of Organization: $100
3. Registered Agent Required: ~$50-150/year
4. Operating Agreement: Recommended (not filed)
5. EIN from IRS: Free

**Timeline:** 1-2 business days (same-day with expedited)

**Recommended Service Providers:**
- Wyoming LLC Attorney (wyomingllcattorney.com)
- Northwest Registered Agent
- ZenBusiness
- LegalZoom

### 6.2 Banking Options for Adult Businesses

**Traditional Banks (Adult-Friendly):**

| Bank | Notes | Difficulty |
|------|-------|------------|
| **East West Bank** | Known to work with adult | Medium |
| **Bank of Nevada** | Las Vegas presence helps | Medium |
| **Metropolitan Commercial Bank** | Works with high-risk | Medium |
| **First Foundation Bank** | Case-by-case | High |
| **Community Banks** | Local relationships matter | Variable |

**Fintech/Modern Banks:**

| Platform | Adult-Friendly | Notes |
|----------|----------------|-------|
| Mercury | **No** | Explicitly excludes adult |
| Relay | **No** | Conservative policy |
| Brex | **Maybe** | Case-by-case |
| BlueVine | **No** | Excludes adult |
| **Novo** | **Maybe** | Worth trying |
| **PayPal/Venmo** | **No** | Will close accounts |
| **Stripe** | **No** | Explicitly prohibited |

**Best Strategy:**
1. Apply to 3-4 local credit unions simultaneously
2. Be upfront about business type
3. Have CCBill/Epoch processing already approved (shows legitimacy)
4. Keep personal and business accounts at different institutions
5. Consider offshore banking as backup

**Backup Options:**
- TransferWise/Wise Business (for international)
- Payoneer (receives ACH from processors)
- Mercury for non-adult subsidiary (if applicable)

### 6.3 Accounting & Bookkeeping

**Adult-Friendly Accountants:**
- Search for CPAs with entertainment/content creator experience
- Adult industry conferences often have CPA sponsors
- FSC (Free Speech Coalition) member directory

**Key Considerations:**
- Separate business finances completely
- Track income by category (subscriptions, tips, purchases)
- Document all creator payouts (1099s required)
- International tax planning if selling globally

**Software Recommendations:**
- **QuickBooks Online:** Standard, works for most
- **Xero:** Good for international
- **Wave:** Free option for starting out
- **Bench:** Outsourced bookkeeping

### 6.4 Tax Implications

**Entity Taxation:**

| Structure | Federal Tax | Self-Employment | Notes |
|-----------|-------------|-----------------|-------|
| LLC (default) | Pass-through | Yes (15.3%) | Simple |
| LLC (S-Corp elect) | Pass-through | Only on salary | Saves SE tax at higher income |
| LLC (C-Corp elect) | 21% corporate | No SE tax | Double taxation on dividends |

**S-Corp Election Strategy:**
- Consider at $80K+ net profit
- Pay yourself reasonable salary
- Remaining profits = distributions (no SE tax)
- Requires payroll processing

**Sales Tax Considerations:**
- Digital goods taxation varies by state
- Economic nexus thresholds ($100K or 200 transactions)
- Consider TaxJar or Avalara for automation
- Many states exempt digital goods

**International:**
- VAT for EU sales (consider MOSS registration)
- UK Digital Services Tax
- Canadian GST/HST

---

## 7. Master Checklist & Timeline

### Pre-Launch Checklist

#### Week 1-2: Business Formation
- [ ] Form Wyoming LLC
- [ ] Get EIN from IRS
- [ ] Open business bank account
- [ ] Set up business email domain

#### Week 2-3: Legal Documents
- [ ] Draft Terms of Service
- [ ] Draft Privacy Policy
- [ ] Draft DMCA Policy
- [ ] Create 2257 statement (if applicable)
- [ ] Register DMCA designated agent
- [ ] Age verification solution selected

#### Week 3-4: Payment Processing
- [ ] Apply to Epoch
- [ ] Pay Visa/MC registration ($1,450)
- [ ] Receive account credentials
- [ ] Apply to CCBill (secondary)
- [ ] Set up NOWPayments (crypto)

#### Week 4-5: Integration
- [ ] Integrate payment forms
- [ ] Test payment flows
- [ ] Implement webhooks/callbacks
- [ ] Set up subscription management
- [ ] Configure fraud prevention

#### Week 5-6: Compliance
- [ ] Age verification implementation
- [ ] State blocking for non-compliant states
- [ ] Content moderation system
- [ ] 2257 record-keeping system
- [ ] Creator verification process

#### Pre-Launch
- [ ] Final legal review
- [ ] Payment testing (live transactions)
- [ ] Chargeback handling procedures
- [ ] Customer support ready
- [ ] Banking reconciliation set up

### Estimated Costs Summary

| Item | One-Time | Monthly | Annual |
|------|----------|---------|--------|
| Wyoming LLC Formation | $100 | - | $60 |
| Registered Agent | - | - | $100 |
| DMCA Registration | $6 | - | - |
| Visa/MC Registration | - | - | $1,450 |
| Age Verification Service | - | $50-200 | - |
| Accounting Software | - | $30-80 | - |
| Payment Processing | - | 12-15% of revenue | - |
| **First Year Estimate** | ~$110 | ~$100-300 | $1,610 |

### Critical Links & Resources

**Payment Processors:**
- CCBill: https://ccbill.com/merchants
- Epoch: https://epoch.com/business_services
- NOWPayments: https://nowpayments.io/all-solutions/adult
- Segpay: https://segpay.com/

**Legal Resources:**
- DMCA Registration: https://www.copyright.gov/dmca-512/
- 18 USC 2257: https://www.law.cornell.edu/uscode/text/18/2257
- FSC Legal: https://www.freespeechcoalition.com/
- ASACP: https://www.asacp.org/

**Business Formation:**
- Wyoming SOS: https://sos.wyo.gov/
- IRS EIN: https://www.irs.gov/businesses/small-businesses-self-employed/apply-for-an-employer-identification-number-ein-online

**Age Verification:**
- VerifyMyAge: https://verifymyage.com/
- AgeID: https://www.ageid.com/

---

## Appendix: Document Templates (Full)

### A.1 Privacy Policy Template (GDPR + CCPA Compliant)

[See separate file: privacy-policy-template.md]

### A.2 Operating Agreement Template

[See separate file: wyoming-llc-operating-agreement.md]

### A.3 Creator Agreement Template

[See separate file: creator-agreement-template.md]

---

**Document Version:** 1.0  
**Last Updated:** February 10, 2026  
**Prepared For:** Crystal Arcade Project  
**Disclaimer:** This document is for informational purposes. Consult qualified legal and financial professionals before implementing.
