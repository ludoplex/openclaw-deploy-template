# Overnight Sprint TODO - 2026-02-11

## Phase 0: Infrastructure ⏳
- [ ] **Provision Scaleway Mac M4 Pro** (~$160/mo)
- [ ] Add SSH key
- [ ] SSH into Mac, verify access
- [ ] Install: Homebrew, Node.js, Python 3.14, cosmocc
- [ ] Clone OpenClaw and configure
- [ ] Migrate critical data from Windows C:\

## Phase 1: Supplier API Credentials 🔑
**Tools:** AppleScript + PyObjC + Playwright (on Mac)

- [ ] **Ingram Micro** (Account: 50-135152-000)
  - [ ] Log into portal via automation
  - [ ] Navigate to API/developer section
  - [ ] Obtain REST API v6 credentials
  
- [ ] **TD SYNNEX** (Account: 786379)
  - [ ] Access Digital Bridge portal
  - [ ] Get API credentials
  
- [ ] **D&H** (Account: 3270340000)
  - [ ] Access D&H portal
  - [ ] Get OAS3 REST API access
  
- [ ] **Climb** (Account: CU0043054170)
  - [ ] Check if API exists
  - [ ] Document manual process if no API

## Phase 2: Procurement App 📦
- [ ] Integrate Ingram Micro API
- [ ] Integrate TD SYNNEX API
- [ ] Integrate D&H API
- [ ] Build margin calculations
- [ ] Test live inventory sync

## Phase 3: CSV Upload Apps 📄
- [ ] **WithOdyssey** CSV exporter
  - [ ] Research WithOdyssey format requirements
  - [ ] Build export module
  
- [ ] **Amazon** CSV exporter
  - [ ] Research Amazon Seller Central format
  - [ ] Build export module

## Phase 4: Domain & Websites 🌐
- [ ] **Buy dsaicorp.com** (registrar: TBD)
- [ ] **MHI site** (mightyhouseinc.com)
  - [ ] GovCon, EDWOSB, HUBZONE focus
  - [ ] IT Solutions services
  
- [ ] **DSAIC site** (dsaicorp.com)
  - [ ] SaaS/ML/DL focus
  - [ ] IBM/Climb Channel reseller
  
- [ ] **Computer Store site** (computerstore.mightyhouseinc.com)
  - [ ] Retail + Esports/LAN
  - [ ] Training/Certification
  - [ ] Product catalog from procurement app

## Phase 5: Mixpost-Malone 📱
- [ ] Deploy Mixpost-Malone
- [ ] Connect social accounts
- [ ] Configure posting schedule

## Phase 6: Promotional Content 📣

### Events
- [ ] **Warhammer Gen 3 Hype Sealed Play** (THIS FRIDAY)
  - [ ] Create event graphics
  - [ ] Write promotional copy
  - [ ] Schedule social posts

### Services
- [ ] **Tutoring Services**
  - [ ] Create ad copy
  - [ ] Target audience: students, certification seekers
  
- [ ] **Senior Tech Literacy Workshops**
  - [ ] Create ad copy
  - [ ] Target audience: seniors, family members of seniors
  
- [ ] **DIY/Homelab Enthusiast Offerings**
  - [ ] Use supplier inventory + margins to select products
  - [ ] Create product-focused content
  - [ ] Target audience: tech hobbyists, builders

### Product Promotions
- [ ] Query procurement app for high-margin items
- [ ] Generate social media content for top products
- [ ] Schedule promotional posts

---

## Notes
- Mac M4 Pro: Scaleway fr-par or nl-ams region
- Estimated completion: Morning 2026-02-11
- Vincent contact for: domain payment approval, social account access

## Progress Log
- 01:36 MST - Created TODO list
- 01:36 MST - Starting Mac M4 Pro provisioning...
