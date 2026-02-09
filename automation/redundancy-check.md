# MHI Automation System - Redundancy & Alternatives Analysis

**Date:** 2026-02-08  
**Analyst:** Subagent (redundancy-checker)  
**Scope:** Full audit of automation scripts for redundancy with existing tools

---

## Executive Summary

**Verdict:** The system being built has **significant redundancy** with existing tools, but some custom components add unique value. Recommendation is a **hybrid approach**: use existing tools where they excel, build custom only for gaps.

**Estimated Build Cost Saved:** 60-80 hours of development if using existing alternatives  
**Key Recommendation:** Leverage password manager + Zoho's native features before custom building

---

## 1. Web Automation (playwright-automator.py, mhi-automator.py)

### What's Being Built
- Persistent browser sessions with anti-detection
- Generic login handler with selector detection
- Form auto-fill with entity data
- Supplier-specific handlers (Ingram Micro, TD SYNNEX, D&H)

### 🔴 REDUNDANT WITH: Password Managers

| Feature | Custom Build | Bitwarden (Free) | 1Password Business ($8/user/mo) |
|---------|--------------|------------------|--------------------------------|
| Form auto-fill | ✅ Built | ✅ Native | ✅ Native |
| Portal logins | ✅ Built | ✅ Native | ✅ Native |
| Company profiles | ✅ entity-profiles.json | ❌ No | ✅ "Item sharing" |
| Multi-entity | ✅ MHI/DSAIC/Computer Store | ⚠️ Multiple vaults | ✅ Vault per entity |
| Session persistence | ✅ Browser state | ✅ Browser extension | ✅ Browser extension |
| API access | ✅ Full control | ✅ REST API | ✅ Connect Server |

**Password Manager Alternatives:**
- **Bitwarden** (free/OSS): Excellent form fill, custom fields for EIN/DUNS, browser extension
- **1Password Business**: Team sharing, custom item types, CLI for automation
- **Keeper Business**: Form fill, identity templates, SSO integration

**What Password Managers CAN'T Do:**
- ❌ Multi-step supplier signup wizards with conditional logic
- ❌ Captcha handling (requires human anyway)
- ❌ Portal-specific navigation sequences
- ❌ Bulk operations across many portals

### ✅ UNIQUE VALUE in Custom Build
- **Supplier-specific handlers** (login_ingram_micro, login_td_synnex) - these handle quirky portal flows
- **Bulk form detection** (`detect_form_fields`) - useful for new portal onboarding
- **Screenshot auditing** - compliance/documentation trail

### 🎯 Recommendation
**Use Bitwarden** for day-to-day logins and form fill. **Keep custom Playwright** only for:
1. Initial supplier signup flows (one-time operations)
2. Bulk operations requiring scripted navigation
3. Automated testing/verification of portal access

---

## 2. Business Intelligence Gathering (gmail-searcher.py, drive-search.py)

### What's Being Built
- Search Gmail/Drive/OneDrive for EIN, DUNS, CAGE, certs
- Extract business documents from cloud storage
- Build master inventory of accounts/assets

### 🔴 REDUNDANT WITH: Native Platform Features

| Feature | Custom Script | Gmail/Drive Native | Google Workspace Admin |
|---------|---------------|-------------------|------------------------|
| Email search | ✅ Playwright UI scraping | ✅ Gmail search operators | ✅ Admin search |
| Drive search | ✅ Playwright UI scraping | ✅ Drive search | ✅ Drive audit logs |
| Export results | ✅ JSON output | ✅ Takeout export | ✅ Reports API |
| Cross-account | ✅ Account switching | ❌ Single account | ✅ Domain-wide |

**Google Workspace Has:**
- **Gmail API** - direct programmatic search (no UI scraping needed)
- **Drive API** - search files with `q` parameter, get metadata
- **Google Takeout** - bulk export all data
- **Admin Console Reports** - audit all user activity

**Microsoft 365 Has:**
- **Microsoft Graph API** - search OneDrive, mail, everything
- **Content Search** - compliance center bulk search
- **eDiscovery** - legal hold and export

### 🔴 MAJOR ISSUE: You're Screen-Scraping Instead of Using APIs

The gmail-searcher.py and drive-search.py are **UI automation** when you should be using **APIs**:

```python
# CURRENT (UI scraping - fragile, slow)
await self.page.goto(f"https://mail.google.com/mail/u/0/#search/{query}")
rows = await self.page.query_selector_all('tr.zA')

# BETTER (Gmail API - fast, reliable)
service = build('gmail', 'v1', credentials=creds)
results = service.users().messages().list(userId='me', q=query).execute()
```

### ✅ Open Source Alternatives

| Tool | Purpose | URL |
|------|---------|-----|
| **GYB (Got Your Back)** | Gmail backup/search | github.com/GAM-team/got-your-back |
| **GAM (Google Apps Manager)** | Full Google Workspace CLI | github.com/GAM-team/GAM |
| **rclone** | Sync/search cloud storage | rclone.org |
| **Thunderbird + ImportExportTools** | Email archive/search | |

### 🎯 Recommendation

**DELETE** gmail-searcher.py and drive-search.py. Replace with:

1. **For one-time document gathering:** Use Google Takeout + local grep/search
2. **For ongoing monitoring:** Set up Gmail API with OAuth
3. **For Drive search:** Use `rclone` or Google Drive API

**Sample replacement using GAM:**
```bash
# Search all Gmail for EIN documents
gam user rachelwilliams@mightyhouseinc.com show messages query "EIN OR DUNS" > email_results.txt

# List all Drive files matching criteria
gam user rachelwilliams@mightyhouseinc.com show filelist query "name contains 'EIN'" > drive_results.txt
```

---

## 3. Entity Profiles (entity-profiles.json)

### What's Being Built
- JSON store of company data (legal name, EIN, DUNS, address, contacts)
- Multi-entity support (MHI, DSAIC, Computer Store)

### 🔴 REDUNDANT WITH: Zoho CRM + Other CRMs

**You already have Zoho!** Per `zoho-entity-audit.json`:
- Zoho CRM (rate limited but configured)
- Zoho Books
- Zoho Inventory
- Zoho Desk

**Zoho CRM Can Store:**
- ✅ Company records with all business fields
- ✅ Custom fields (EIN, DUNS, CAGE, certifications)
- ✅ Contact associations
- ✅ Address management
- ✅ API access for automation

### Why Duplicate in JSON?
The current `entity-profiles.json` duplicates what should live in CRM:
- Legal name → Account Name
- EIN/DUNS/CAGE → Custom Fields
- Address → Billing/Shipping Address
- Contacts → Associated Contacts

### 🎯 Recommendation

**Migrate entity-profiles.json INTO Zoho CRM:**

1. Create custom fields in Zoho CRM: EIN, DUNS, CAGE_Code, Certifications (multi-select)
2. Create Account records for each entity
3. Link Contacts to Accounts
4. Use Zoho CRM API to fetch data for automation scripts

**Benefits:**
- Single source of truth
- Zoho handles updates, history, audit trail
- Other team members can access/update
- Zoho integrations for form fill (Zoho Forms)

---

## 4. Signup Templates (signup-templates.json)

### What's Being Built
- URL database for reseller applications
- Field mappings per portal
- Requirements documentation

### 🟡 PARTIALLY REDUNDANT

**Not exactly replicated elsewhere, but consider:**

| Alternative | What It Does |
|-------------|--------------|
| **Notion/Airtable** | Same data, better UI, collaboration |
| **Zoho Creator** | Low-code database, can trigger automation |
| **Bitwarden Notes** | Store signup URLs with credentials |

### ✅ UNIQUE VALUE

- Having field mappings programmatically is useful
- Requirements documentation is good reference
- Templates enable batch operations

### 🎯 Recommendation

**Keep but migrate to Airtable or Notion:**
- Better UI for managing portal catalog
- Filter/sort/search capabilities
- Can export to JSON for automation if needed
- Team can update without editing code

---

## 5. LLM Export Scripts (zoho-entity-audit.json context)

### From Context
The system appears to be doing Zoho API calls to audit entity presence.

### 🔴 ZOHO HAS NATIVE EXPORT

- **Zoho CRM:** Export to CSV/XLS from any module
- **Zoho Books:** Export financial data, contacts
- **Zoho Inventory:** Export items, warehouses
- **Zoho Analytics:** Cross-app reporting

### 🎯 Recommendation

**For auditing entity presence:**
- Use Zoho CRM's "Account" module list view
- Create saved filters for each entity
- Use Zoho Analytics for cross-app dashboards

**For data extraction:**
- Use Zoho's Data Backup feature
- Or Zoho CRM's native API (which you already have OAuth for)

---

## 6. Social Media Account Discovery

### Files Found
- `social-media-accounts.json` (not examined but exists)

### Existing Tools

| Tool | Price | What It Does |
|------|-------|--------------|
| **Namechk** | Free | Check username availability across platforms |
| **KnowEm** | Free-$65 | Brand monitoring, registration |
| **Hootsuite** | $99/mo | Manage multiple social accounts |
| **Brand24** | $99/mo | Social mention monitoring |
| **PhantomBuster** | $69/mo | Scrape social profiles |

### 🎯 Recommendation

**Manual inventory** is probably sufficient for 3 entities. If needed:
- Use Namechk for initial discovery
- Store results in simple spreadsheet or CRM custom fields

---

## Cost-Benefit Summary

### What to STOP Building (Use Existing Tools)

| Component | Hours to Build | Alternative | Annual Cost |
|-----------|---------------|-------------|-------------|
| Email search scripts | 20+ hrs | Gmail API + GAM | $0 |
| Drive search scripts | 15+ hrs | rclone + Drive API | $0 |
| Entity profiles | 10+ hrs | Zoho CRM | Already paying |
| Generic form fill | 20+ hrs | Bitwarden | $0 (free tier) |
| Signup templates DB | 10+ hrs | Notion/Airtable | $0-10/mo |

**Total Development Hours Saved: 75+ hours**

### What to KEEP Building

| Component | Justification |
|-----------|---------------|
| Supplier-specific handlers | Portal quirks need custom handling |
| Playwright infrastructure | Base for future automation |
| Anti-detection patterns | Useful for any web automation |
| Screenshot audit trail | Compliance documentation |

---

## Recommended Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     DATA LAYER                               │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐   │
│  │   Zoho CRM    │  │  Bitwarden    │  │ Notion/Airtable│   │
│  │ (Entities,    │  │ (Credentials, │  │ (Portal URLs,  │   │
│  │  Contacts)    │  │  Login info)  │  │  Templates)    │   │
│  └───────────────┘  └───────────────┘  └───────────────┘   │
│           │                │                  │              │
│           └────────────────┼──────────────────┘              │
│                            ▼                                 │
│              ┌─────────────────────────┐                    │
│              │  mhi-automator.py       │                    │
│              │  (Playwright - custom   │                    │
│              │   flows only)           │                    │
│              └─────────────────────────┘                    │
│                            │                                 │
│           ┌────────────────┼────────────────┐               │
│           ▼                ▼                ▼               │
│  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐     │
│  │ Ingram Micro  │ │  TD SYNNEX    │ │   D&H         │     │
│  │   Signup      │ │   Signup      │ │   Signup      │     │
│  └───────────────┘ └───────────────┘ └───────────────┘     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                  DOCUMENT DISCOVERY                          │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐   │
│  │  Gmail API    │  │   GAM CLI     │  │   rclone      │   │
│  │  (OAuth)      │  │  (Workspace)  │  │  (Drive sync) │   │
│  └───────────────┘  └───────────────┘  └───────────────┘   │
│           │                │                  │              │
│           └────────────────┼──────────────────┘              │
│                            ▼                                 │
│              ┌─────────────────────────┐                    │
│              │  Local Search/Index     │                    │
│              │  (grep, ripgrep, etc)   │                    │
│              └─────────────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Action Items

### Immediate (This Week)
1. [ ] **Install Bitwarden** and migrate credentials from `.credentials.json`
2. [ ] **Create Zoho CRM custom fields** for EIN, DUNS, CAGE
3. [ ] **Delete** gmail-searcher.py, drive-search.py (replace with API-based tools)
4. [ ] **Install GAM** for Google Workspace management

### Short Term (This Month)
5. [ ] Migrate entity-profiles.json data to Zoho CRM Account records
6. [ ] Move signup-templates.json to Notion/Airtable for easier management
7. [ ] Simplify mhi-automator.py to only handle custom portal flows
8. [ ] Set up Gmail API OAuth for any future email automation

### Long Term
9. [ ] Consider Zoho Forms for external data collection
10. [ ] Evaluate Zoho Flow for workflow automation between apps
11. [ ] Build Zoho CRM integration to pull entity data directly

---

## Files to Delete/Archive

| File | Recommendation | Reason |
|------|---------------|--------|
| `gmail-searcher.py` | DELETE | UI scraping when API exists |
| `drive-search.py` | DELETE | UI scraping when API exists |
| `drive-search-simple.py` | DELETE | Same issue |
| `onedrive-search.py` | DELETE | Use Graph API or manual |
| `check-drive-session.py` | DELETE | Not needed with API approach |
| `entity-profiles.json` | MIGRATE | Move to Zoho CRM |
| `playwright-automator.py` | KEEP | Generic utilities useful |
| `mhi-automator.py` | KEEP | Custom portal flows |
| `signup-templates.json` | MIGRATE | Move to Notion/Airtable |

---

## Conclusion

You're building a comprehensive system, but ~70% of it duplicates existing tools. The unique value is in portal-specific automation that handles quirky multi-step flows.

**Recommended approach:**
1. **Data storage:** Use Zoho CRM (already have it)
2. **Credentials:** Use Bitwarden (free, battle-tested)
3. **Email/Drive search:** Use APIs, not UI scraping
4. **Custom automation:** Keep Playwright for supplier-specific flows only

This reduces maintenance burden, improves reliability, and lets you focus development time on the genuinely unique parts of the system.
