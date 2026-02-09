# MHI Automation System - Comprehensive Solutions

**Date:** 2026-02-08  
**Analyst:** Subagent (solver-sequential)  
**Purpose:** Concrete solutions for every issue identified in redundancy check and critic analysis

---

## Overview

This document provides actionable solutions for all 12 issues identified across both prior analyses. Each solution includes:
- **The Problem** (brief recap)
- **Specific Fix** (code changes, tool adoption, or removal)
- **Implementation Effort** (in hours)
- **Priority** (Critical/High/Medium)

---

# SECTION A: REDUNDANCY ISSUES

## Issue R1: Gmail/Drive UI Scraping → Should Use APIs

**Problem:** `gmail-searcher.py` and `drive-search.py` use Playwright to scrape web UIs when Google provides official APIs.

**Specific Fix:**

1. **DELETE these files entirely:**
   - `gmail-searcher.py`
   - `drive-search.py`
   - `drive-search-simple.py`
   - `onedrive-search.py`
   - `check-drive-session.py`

2. **Replace with Gmail API approach:**
```python
# NEW FILE: gmail-api-search.py
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def search_gmail(query: str, user_id: str = 'me') -> list:
    """Search Gmail using official API - reliable, fast, legal."""
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('gmail', 'v1', credentials=creds)
    
    results = service.users().messages().list(
        userId=user_id,
        q=query,
        maxResults=100
    ).execute()
    
    return results.get('messages', [])
```

3. **For Drive search, use Drive API:**
```python
# NEW FILE: drive-api-search.py
from googleapiclient.discovery import build

def search_drive(query: str) -> list:
    """Search Drive using official API."""
    service = build('drive', 'v3', credentials=creds)
    results = service.files().list(
        q=f"fullText contains '{query}'",
        pageSize=100,
        fields="files(id, name, mimeType, modifiedTime)"
    ).execute()
    return results.get('files', [])
```

4. **Alternative: Use GAM CLI (zero code):**
```bash
# Install GAM
bash <(curl -s -S -L https://gam-shortn.appspot.com/gam-install)

# Search Gmail
gam user rachelwilliams@mightyhouseinc.com show messages query "EIN OR DUNS" > results.txt

# Search Drive
gam user rachelwilliams@mightyhouseinc.com show filelist query "name contains 'EIN'" > files.txt
```

| Effort | Priority |
|--------|----------|
| 4-6 hours | **HIGH** |

---

## Issue R2: Credentials in .credentials.json → Use Bitwarden

**Problem:** Plaintext passwords stored in JSON file. Massive security risk.

**Specific Fix:**

1. **Install Bitwarden CLI:**
```bash
# Windows
choco install bitwarden-cli
# or download from https://bitwarden.com/help/cli/

bw login
bw unlock  # Get session key
```

2. **Migrate all credentials to Bitwarden:**
```bash
# For each portal in .credentials.json:
bw create item '{
  "type": 1,
  "name": "Ingram Micro Portal",
  "login": {
    "username": "user@mhi.com",
    "password": "xxx",
    "uris": [{"uri": "https://usa.ingrammicro.com"}]
  },
  "fields": [
    {"name": "entity", "value": "MHI", "type": 0}
  ]
}'
```

3. **Modify automator to fetch from Bitwarden:**
```python
# In mhi-automator.py - replace credential loading
import subprocess
import json

def get_credential(portal_name: str) -> dict:
    """Fetch credential from Bitwarden vault."""
    session = os.environ.get('BW_SESSION')
    result = subprocess.run(
        ['bw', 'get', 'item', portal_name, '--session', session],
        capture_output=True, text=True
    )
    item = json.loads(result.stdout)
    return {
        'username': item['login']['username'],
        'password': item['login']['password']
    }
```

4. **DELETE `.credentials.json` after migration:**
```bash
# Secure delete
del /P .credentials.json
# Or on Unix: shred -vfzu .credentials.json
```

5. **Add to .gitignore (defense in depth):**
```
.credentials.json
*.bwsession
BW_SESSION
```

| Effort | Priority |
|--------|----------|
| 3-4 hours | **CRITICAL** |

---

## Issue R3: Entity Profiles in JSON → Use Zoho CRM

**Problem:** `entity-profiles.json` duplicates data that belongs in Zoho CRM.

**Specific Fix:**

1. **Create custom fields in Zoho CRM:**
   - Go to: Settings → Customization → Modules → Accounts → Fields
   - Add custom fields:
     - `EIN` (Single Line)
     - `DUNS_Number` (Single Line)
     - `CAGE_Code` (Single Line)
     - `Certifications` (Multi-Select Picklist: WOSB, EDWOSB, SBA8a, HUBZone)
     - `SAM_UEI` (Single Line)

2. **Create Account records for each entity:**
   - MHI (Mighty House Inc)
   - DSAIC
   - Computer Store

3. **Fetch entity data via Zoho CRM API:**
```python
# NEW FILE: zoho-entity-fetch.py
import requests

ZOHO_BASE = "https://www.zohoapis.com/crm/v2"

def get_entity_profile(entity_name: str, access_token: str) -> dict:
    """Fetch entity profile from Zoho CRM."""
    headers = {"Authorization": f"Zoho-oauthtoken {access_token}"}
    
    # Search for account by name
    response = requests.get(
        f"{ZOHO_BASE}/Accounts/search",
        headers=headers,
        params={"criteria": f"Account_Name:equals:{entity_name}"}
    )
    
    accounts = response.json().get('data', [])
    if accounts:
        account = accounts[0]
        return {
            "legal_name": account.get("Account_Name"),
            "ein": account.get("EIN"),
            "duns": account.get("DUNS_Number"),
            "cage_code": account.get("CAGE_Code"),
            "address": {
                "street": account.get("Billing_Street"),
                "city": account.get("Billing_City"),
                "state": account.get("Billing_State"),
                "zip": account.get("Billing_Code")
            }
        }
    return None
```

4. **Migrate existing data:**
```python
# ONE-TIME MIGRATION SCRIPT
import json

# Load existing profiles
with open('entity-profiles.json') as f:
    profiles = json.load(f)

# Create in Zoho (pseudo-code)
for entity_key, data in profiles['entities'].items():
    create_zoho_account(data)
```

5. **DELETE `entity-profiles.json` after migration confirmed.**

| Effort | Priority |
|--------|----------|
| 6-8 hours | **HIGH** |

---

## Issue R4: Generic Form Fill → Bitwarden Already Does This

**Problem:** Custom form-filling code duplicates Bitwarden's built-in functionality.

**Specific Fix:**

1. **For routine logins/form fills:**
   - Use Bitwarden browser extension (free)
   - Configure identities in Bitwarden with custom fields
   - Let extension auto-fill

2. **Remove generic form fill code from `playwright-automator.py`:**
```python
# DELETE this entire method - Bitwarden handles it:
async def fill_form_with_entity(self, entity: str = "mhi", extra_data: dict = None):
    ...
```

3. **Keep ONLY portal-specific handlers for:**
   - Multi-step wizards with conditional logic
   - Forms that Bitwarden can't detect
   - Bulk registration operations

4. **Bitwarden identity setup for each entity:**
   - Create Identity in Bitwarden:
     - Company: Mighty House Inc
     - Email: rachelwilliams@mightyhouseinc.com
     - Phone: (xxx) xxx-xxxx
     - Address: full business address
   - Custom fields for EIN, DUNS, etc.

| Effort | Priority |
|--------|----------|
| 2-3 hours | **MEDIUM** |

---

# SECTION B: CRITIC ISSUES

## Issue C1: Plaintext Credential Storage → Encryption/Vault

**Problem:** `.credentials.json` stores passwords in plaintext. Any file read = full compromise.

**Specific Fix:**

*This overlaps with R2 (Bitwarden migration). Additional hardening:*

1. **If JSON must persist temporarily, encrypt it:**
```python
# Use Windows DPAPI for encryption at rest
import win32crypt
import base64

def encrypt_credential(plaintext: str) -> str:
    """Encrypt using Windows DPAPI (user-bound)."""
    encrypted = win32crypt.CryptProtectData(
        plaintext.encode('utf-8'),
        None,  # Optional description
        None,  # Optional entropy
        None,  # Reserved
        None,  # Prompt struct
        0      # Flags
    )
    return base64.b64encode(encrypted).decode('ascii')

def decrypt_credential(encrypted_b64: str) -> str:
    """Decrypt using Windows DPAPI."""
    encrypted = base64.b64decode(encrypted_b64)
    decrypted = win32crypt.CryptUnprotectData(
        encrypted, None, None, None, 0
    )
    return decrypted[1].decode('utf-8')
```

2. **For cross-platform: Use age encryption:**
```bash
# Install age
choco install age

# Generate key
age-keygen -o key.txt

# Encrypt credentials file
age -r <public-key> credentials.json > credentials.json.age

# Decrypt when needed
age -d -i key.txt credentials.json.age > credentials.json
```

3. **Best solution: Migrate to Bitwarden (see R2) and DELETE all local credential files.**

| Effort | Priority |
|--------|----------|
| 2 hours (encryption) OR 4 hours (Bitwarden) | **CRITICAL** |

---

## Issue C2: Browser State Exposure → Isolation/Protection

**Problem:** `browser-state/` contains complete session cookies for all portals. Single point of catastrophic failure.

**Specific Fix:**

1. **Encrypt browser-state directory:**
```bash
# Windows BitLocker on folder (Enterprise) or use VeraCrypt:
# Create encrypted container for browser-state

# Alternative: Use EFS (Encrypting File System)
cipher /e /s:browser-state
```

2. **Separate browser profiles by risk level:**
```python
# In playwright-automator.py - modify context creation
PROFILE_CATEGORIES = {
    "government": ["sam.gov", "sba.gov"],  # HIGH RISK - separate profile
    "distributors": ["ingrammicro.com", "synnex.com", "dandh.com"],  # MEDIUM
    "email": ["gmail.com"],  # SEPARATE - crown jewels
    "general": ["*"]  # LOW RISK
}

def get_browser_context(portal_url: str):
    """Get isolated browser context based on risk category."""
    category = categorize_portal(portal_url)
    profile_path = f"browser-state/{category}"
    return browser.new_context(storage_state=f"{profile_path}/state.json")
```

3. **Add session expiry enforcement:**
```python
import time
import json
import os

def is_session_stale(profile_path: str, max_age_hours: int = 24) -> bool:
    """Check if session should be refreshed."""
    state_file = f"{profile_path}/state.json"
    if not os.path.exists(state_file):
        return True
    
    mtime = os.path.getmtime(state_file)
    age_hours = (time.time() - mtime) / 3600
    return age_hours > max_age_hours
```

4. **Exclude browser-state from cloud sync:**
```
# Add to cloud sync exclusions (Dropbox, OneDrive, etc.)
browser-state/
*.session
```

5. **Set restrictive file permissions:**
```powershell
# Windows - restrict to current user only
icacls browser-state /inheritance:r
icacls browser-state /grant:r "%USERNAME%:F"
```

| Effort | Priority |
|--------|----------|
| 6-8 hours | **CRITICAL** |

---

## Issue C3: ToS Violations → Which Automations to Keep vs Drop

**Problem:** Automating login/scraping violates ToS for most portals. Risk of account termination or legal action.

**Specific Fix:**

### Category 1: STOP IMMEDIATELY (Legal Risk Too High)

| Portal | Action | Reason |
|--------|--------|--------|
| Gmail (UI scraping) | **DELETE** | Use Gmail API instead - legal, faster, reliable |
| SAM.gov | **DELETE** | Federal system - CFAA implications |
| Government portals | **DELETE** | All gov sites - manual only |

### Category 2: REPLACE WITH APIs (Best Practice)

| Portal | Action | Alternative |
|--------|--------|-------------|
| Gmail | Use Gmail API | OAuth-based, sanctioned access |
| Google Drive | Use Drive API | Same |
| OneDrive | Use Graph API | Microsoft's official API |
| Zoho | Continue using API | Already doing this right |

### Category 3: AUTOMATE WITH CAUTION (Accept Risk)

| Portal | Risk Level | Mitigation |
|--------|------------|------------|
| Ingram Micro | Medium | Use for initial signup only, not daily access |
| TD SYNNEX | Medium | Same |
| D&H | Medium | Same |

**Decision Framework:**
```
Is there an official API?
  YES → Use the API, delete UI automation
  NO  → Is this a government/financial system?
    YES → Manual only
    NO  → Is this a one-time or rare operation?
      YES → Proceed with caution, document risk acceptance
      NO  → Negotiate API access with vendor or go manual
```

### Implement API Access Requests:
```
1. Ingram Micro Partner API: https://partners.ingrammicro.com/api
2. TD SYNNEX API: Contact your rep for "Integration Partnership"
3. D&H API: Partner Connect program
```

| Effort | Priority |
|--------|----------|
| 4 hours (audit) + ongoing | **CRITICAL** |

---

## Issue C4: No Failure Detection → Monitoring Solutions

**Problem:** Automations fail silently. No alerts, no health checks.

**Specific Fix:**

1. **Create health check system:**
```python
# NEW FILE: health-check.py
import asyncio
import aiohttp
from datetime import datetime
import json

HEALTH_FILE = "automation/health-status.json"

async def check_portal_login(portal_name: str, login_func) -> dict:
    """Verify a portal login works."""
    try:
        start = datetime.now()
        success = await login_func()
        duration = (datetime.now() - start).total_seconds()
        
        return {
            "portal": portal_name,
            "status": "healthy" if success else "failed",
            "checked_at": datetime.now().isoformat(),
            "duration_seconds": duration
        }
    except Exception as e:
        return {
            "portal": portal_name,
            "status": "error",
            "error": str(e),
            "checked_at": datetime.now().isoformat()
        }

async def run_all_health_checks():
    """Run health checks on all critical portals."""
    results = []
    
    # Check each portal
    for portal in ["ingram_micro", "td_synnex", "dh"]:
        result = await check_portal_login(portal, lambda: check_portal(portal))
        results.append(result)
    
    # Save results
    with open(HEALTH_FILE, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Alert on failures
    failures = [r for r in results if r['status'] != 'healthy']
    if failures:
        await send_alert(failures)
    
    return results
```

2. **Add alerting via OpenClaw notifications:**
```python
async def send_alert(failures: list):
    """Send alert about failed health checks."""
    message = "🚨 Automation Health Alert:\n\n"
    for f in failures:
        message += f"❌ {f['portal']}: {f['status']}\n"
        if 'error' in f:
            message += f"   Error: {f['error']}\n"
    
    # Use OpenClaw notification system
    # Or send email/Telegram directly
    print(message)  # At minimum, log it
```

3. **Schedule daily health checks via cron:**
```
# In OpenClaw, create cron job:
0 8 * * * python automation/health-check.py
```

4. **Add to HEARTBEAT.md for periodic checks:**
```markdown
## Health Checks
- Run automation health check if >24h since last check
- Alert on any failures
```

5. **Dead man's switch for critical portals:**
```python
# Track last successful access
def record_success(portal: str):
    with open("automation/last-success.json", "r+") as f:
        data = json.load(f)
        data[portal] = datetime.now().isoformat()
        f.seek(0)
        json.dump(data, f)

# Alert if no success in X days
def check_dead_mans_switch():
    with open("automation/last-success.json") as f:
        data = json.load(f)
    
    for portal, last_success in data.items():
        last = datetime.fromisoformat(last_success)
        if (datetime.now() - last).days > 7:
            send_alert(f"No successful access to {portal} in 7+ days!")
```

| Effort | Priority |
|--------|----------|
| 8-10 hours | **HIGH** |

---

## Issue C5: Selector Fragility → Self-Healing Strategies

**Problem:** Hardcoded CSS selectors break when portals update their UI.

**Specific Fix:**

1. **Implement multi-strategy selector matching:**
```python
# NEW FILE: resilient-selectors.py
from playwright.async_api import Page

class ResilientSelector:
    """Try multiple strategies to find elements."""
    
    def __init__(self, page: Page):
        self.page = page
    
    async def find_login_field(self) -> str:
        """Find username/email field using multiple strategies."""
        strategies = [
            # Strategy 1: Common attributes
            'input[name="username"]',
            'input[name="email"]',
            'input[type="email"]',
            
            # Strategy 2: Labels
            'input[aria-label*="email" i]',
            'input[aria-label*="username" i]',
            
            # Strategy 3: Placeholder text
            'input[placeholder*="email" i]',
            'input[placeholder*="username" i]',
            
            # Strategy 4: Associated labels (Playwright's text matching)
            'label:has-text("Email") + input',
            'label:has-text("Username") + input',
            
            # Strategy 5: Form context
            'form input[type="text"]:first-of-type',
        ]
        
        for selector in strategies:
            try:
                elem = await self.page.query_selector(selector)
                if elem and await elem.is_visible():
                    return selector
            except:
                continue
        
        return None
    
    async def find_password_field(self) -> str:
        """Find password field."""
        strategies = [
            'input[type="password"]',
            'input[name="password"]',
            'input[aria-label*="password" i]',
        ]
        
        for selector in strategies:
            try:
                elem = await self.page.query_selector(selector)
                if elem and await elem.is_visible():
                    return selector
            except:
                continue
        
        return None
    
    async def find_submit_button(self) -> str:
        """Find login/submit button."""
        strategies = [
            'button[type="submit"]',
            'input[type="submit"]',
            'button:has-text("Log in")',
            'button:has-text("Login")',
            'button:has-text("Sign in")',
            'button:has-text("Submit")',
            '#loginButton',
            '#submitBtn',
            '.login-btn',
            '.submit-btn',
        ]
        
        for selector in strategies:
            try:
                elem = await self.page.query_selector(selector)
                if elem and await elem.is_visible():
                    return selector
            except:
                continue
        
        return None
```

2. **Store working selectors for each portal:**
```python
# Track which selectors work for each portal
SELECTOR_CACHE_FILE = "automation/selector-cache.json"

def cache_working_selector(portal: str, field: str, selector: str):
    """Remember what worked."""
    with open(SELECTOR_CACHE_FILE, 'r+') as f:
        cache = json.load(f)
        if portal not in cache:
            cache[portal] = {}
        cache[portal][field] = {
            "selector": selector,
            "last_worked": datetime.now().isoformat()
        }
        f.seek(0)
        json.dump(cache, f, indent=2)

def get_cached_selector(portal: str, field: str) -> str:
    """Try cached selector first."""
    with open(SELECTOR_CACHE_FILE) as f:
        cache = json.load(f)
    return cache.get(portal, {}).get(field, {}).get("selector")
```

3. **Selector validation on each run:**
```python
async def validate_and_update_selectors(portal: str, page: Page):
    """Verify cached selectors still work, update if not."""
    resilient = ResilientSelector(page)
    
    # Try cached first
    cached_username = get_cached_selector(portal, "username")
    if cached_username:
        elem = await page.query_selector(cached_username)
        if elem and await elem.is_visible():
            return cached_username  # Still works!
    
    # Cache miss or stale - find new selector
    new_selector = await resilient.find_login_field()
    if new_selector:
        cache_working_selector(portal, "username", new_selector)
        return new_selector
    
    # All strategies failed - alert
    raise SelectorNotFoundError(f"Cannot find username field on {portal}")
```

4. **Use Playwright's Aria-based selectors (more stable):**
```python
# Instead of: await page.click('#loginButton')
# Use: await page.get_by_role("button", name="Log in").click()

# Instead of: await page.fill('input[name="email"]', email)
# Use: await page.get_by_label("Email").fill(email)
```

| Effort | Priority |
|--------|----------|
| 10-12 hours | **HIGH** |

---

## Issue C6: Anti-Bot Blocking → Evasion or API Alternatives

**Problem:** Current anti-detection measures are basic and will eventually fail.

**Specific Fix:**

### Strategy 1: Prefer APIs (Best Solution)

| Portal | API Alternative |
|--------|-----------------|
| Gmail | Gmail API (OAuth) ✅ |
| Drive | Drive API ✅ |
| Distributors | Request partner API access |

### Strategy 2: Enhanced Stealth (If API Not Available)

1. **Use playwright-stealth package:**
```bash
pip install playwright-stealth
```

```python
from playwright_stealth import stealth_async

async def create_stealth_page(browser):
    context = await browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    )
    page = await context.new_page()
    await stealth_async(page)  # Apply stealth patches
    return page
```

2. **Behavioral humanization:**
```python
import random

async def human_type(page, selector: str, text: str):
    """Type like a human - variable delays between keystrokes."""
    await page.click(selector)
    for char in text:
        await page.keyboard.type(char)
        await asyncio.sleep(random.uniform(0.05, 0.15))

async def human_mouse_move(page, x: int, y: int):
    """Move mouse with human-like curves."""
    current = await page.evaluate('() => ({x: 0, y: 0})')
    steps = random.randint(10, 25)
    for i in range(steps):
        progress = i / steps
        # Add slight randomness to path
        jitter_x = random.uniform(-5, 5)
        jitter_y = random.uniform(-5, 5)
        await page.mouse.move(
            current['x'] + (x - current['x']) * progress + jitter_x,
            current['y'] + (y - current['y']) * progress + jitter_y
        )
        await asyncio.sleep(random.uniform(0.01, 0.03))
```

3. **Rotate browser fingerprints:**
```python
FINGERPRINTS = [
    {"viewport": {"width": 1920, "height": 1080}, "deviceScaleFactor": 1},
    {"viewport": {"width": 1536, "height": 864}, "deviceScaleFactor": 1.25},
    {"viewport": {"width": 1440, "height": 900}, "deviceScaleFactor": 2},
]

async def get_random_context(browser):
    fp = random.choice(FINGERPRINTS)
    return await browser.new_context(**fp)
```

### Strategy 3: Accept Limitations

**For high-value portals with aggressive bot detection:**
- Accept that automation may not be viable
- Use automation for initial setup only
- Plan for manual fallback

| Effort | Priority |
|--------|----------|
| 8-10 hours (stealth) OR 2 hours (API requests) | **HIGH** |

---

## Issue C7: No Concurrency Safety → Database vs JSON

**Problem:** JSON files can corrupt with concurrent access. No locking, no transactions.

**Specific Fix:**

1. **Migrate to SQLite (minimal change, big improvement):**
```python
# NEW FILE: database.py
import sqlite3
from contextlib import contextmanager
from datetime import datetime

DATABASE = "automation/mhi-automation.db"

def init_database():
    """Initialize SQLite database with proper schema."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Entities table (replaces entity-profiles.json)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entities (
            id INTEGER PRIMARY KEY,
            key TEXT UNIQUE NOT NULL,
            legal_name TEXT NOT NULL,
            ein TEXT,
            duns TEXT,
            cage_code TEXT,
            address_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Portal sessions (replaces parts of credentials tracking)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS portal_sessions (
            id INTEGER PRIMARY KEY,
            portal_name TEXT NOT NULL,
            entity_key TEXT,
            last_login TIMESTAMP,
            status TEXT DEFAULT 'unknown',
            FOREIGN KEY (entity_key) REFERENCES entities(key)
        )
    ''')
    
    # Audit log (new - for compliance)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            action TEXT NOT NULL,
            portal TEXT,
            entity TEXT,
            success BOOLEAN,
            details TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

@contextmanager
def get_db():
    """Get database connection with automatic commit/rollback."""
    conn = sqlite3.connect(DATABASE, timeout=30)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def log_action(action: str, portal: str = None, entity: str = None, 
               success: bool = True, details: str = None):
    """Log an automation action for audit trail."""
    with get_db() as conn:
        conn.execute(
            '''INSERT INTO audit_log (action, portal, entity, success, details)
               VALUES (?, ?, ?, ?, ?)''',
            (action, portal, entity, success, details)
        )
```

2. **Migration script from JSON to SQLite:**
```python
# ONE-TIME: migrate-to-sqlite.py
import json
from database import init_database, get_db

def migrate_entities():
    init_database()
    
    with open('entity-profiles.json') as f:
        data = json.load(f)
    
    with get_db() as conn:
        for key, entity in data.get('entities', {}).items():
            conn.execute('''
                INSERT OR REPLACE INTO entities 
                (key, legal_name, ein, duns, cage_code, address_json)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                key,
                entity.get('legal_name'),
                entity.get('ein'),
                entity.get('duns'),
                entity.get('cage_code'),
                json.dumps(entity.get('address', {}))
            ))
    
    print("Migration complete!")

if __name__ == "__main__":
    migrate_entities()
```

3. **Add file locking for any remaining JSON files:**
```python
import fcntl  # Unix
# Or for Windows:
import msvcrt

@contextmanager
def locked_json_write(filepath: str):
    """Write to JSON with file locking."""
    with open(filepath, 'r+') as f:
        # Windows locking
        msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1)
        try:
            data = json.load(f)
            yield data
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=2)
        finally:
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
```

| Effort | Priority |
|--------|----------|
| 6-8 hours | **HIGH** |

---

## Issue C8: Partial Form Submissions → Transaction Safety

**Problem:** Form fills can fail mid-way, leaving partial submissions.

**Specific Fix:**

1. **Implement form state machine:**
```python
# NEW FILE: form-state-machine.py
from enum import Enum
from dataclasses import dataclass
from typing import Optional
import json

class FormState(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    VERIFIED = "verified"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"

@dataclass
class FormSubmission:
    portal: str
    entity: str
    state: FormState
    current_step: int
    total_steps: int
    fields_filled: dict
    screenshot_path: Optional[str] = None
    error: Optional[str] = None
    
    def to_json(self) -> str:
        return json.dumps({
            "portal": self.portal,
            "entity": self.entity,
            "state": self.state.value,
            "current_step": self.current_step,
            "total_steps": self.total_steps,
            "fields_filled": self.fields_filled,
            "screenshot_path": self.screenshot_path,
            "error": self.error
        })
    
    def save_checkpoint(self):
        """Save current state to enable resume."""
        path = f"automation/checkpoints/{self.portal}_{self.entity}.json"
        with open(path, 'w') as f:
            f.write(self.to_json())
    
    @classmethod
    def load_checkpoint(cls, portal: str, entity: str) -> Optional['FormSubmission']:
        """Load saved checkpoint if exists."""
        path = f"automation/checkpoints/{portal}_{entity}.json"
        try:
            with open(path) as f:
                data = json.load(f)
                return cls(
                    portal=data['portal'],
                    entity=data['entity'],
                    state=FormState(data['state']),
                    current_step=data['current_step'],
                    total_steps=data['total_steps'],
                    fields_filled=data['fields_filled'],
                    screenshot_path=data.get('screenshot_path'),
                    error=data.get('error')
                )
        except FileNotFoundError:
            return None
```

2. **Form filling with checkpoints:**
```python
async def fill_form_with_checkpoints(page, portal: str, entity: str, 
                                      fields: list) -> FormSubmission:
    """Fill form with checkpoint/resume capability."""
    
    # Check for existing checkpoint
    submission = FormSubmission.load_checkpoint(portal, entity)
    if submission and submission.state == FormState.IN_PROGRESS:
        print(f"Resuming from step {submission.current_step}")
        start_step = submission.current_step
    else:
        submission = FormSubmission(
            portal=portal,
            entity=entity,
            state=FormState.NOT_STARTED,
            current_step=0,
            total_steps=len(fields),
            fields_filled={}
        )
        start_step = 0
    
    submission.state = FormState.IN_PROGRESS
    
    for i, field in enumerate(fields[start_step:], start=start_step):
        try:
            # Fill the field
            await fill_single_field(page, field['selector'], field['value'])
            
            # Update checkpoint
            submission.current_step = i + 1
            submission.fields_filled[field['name']] = field['value']
            submission.save_checkpoint()
            
            # Screenshot for audit
            await page.screenshot(path=f"screenshots/{portal}_{entity}_step{i}.png")
            
        except Exception as e:
            submission.state = FormState.FAILED
            submission.error = str(e)
            submission.save_checkpoint()
            raise
    
    submission.state = FormState.SUBMITTED
    submission.save_checkpoint()
    return submission
```

3. **Verification after submission:**
```python
async def verify_submission(page, portal: str, entity: str, 
                            submission: FormSubmission) -> bool:
    """Verify form was actually submitted successfully."""
    
    # Portal-specific verification
    if portal == "ingram_micro":
        # Check for success message
        success = await page.query_selector('.success-message, .confirmation')
        if success:
            submission.state = FormState.VERIFIED
            submission.save_checkpoint()
            return True
        
        # Check for error message
        error = await page.query_selector('.error-message, .alert-danger')
        if error:
            error_text = await error.inner_text()
            submission.state = FormState.FAILED
            submission.error = error_text
            submission.save_checkpoint()
            return False
    
    # Generic verification - look for confirmation
    await page.wait_for_timeout(2000)  # Wait for page update
    await page.screenshot(path=f"screenshots/{portal}_{entity}_result.png")
    
    return True  # Assume success if no error detected
```

4. **Cleanup/rollback for failed submissions:**
```python
async def cleanup_failed_submission(portal: str, entity: str):
    """Clean up after failed submission attempt."""
    checkpoint_path = f"automation/checkpoints/{portal}_{entity}.json"
    
    submission = FormSubmission.load_checkpoint(portal, entity)
    if submission:
        # Log the failure
        log_action("form_cleanup", portal, entity, False, 
                   f"Cleaned up failed submission at step {submission.current_step}")
        
        # Archive the checkpoint
        archive_path = f"automation/failed/{portal}_{entity}_{datetime.now().isoformat()}.json"
        shutil.move(checkpoint_path, archive_path)
        
        submission.state = FormState.ROLLED_BACK
```

| Effort | Priority |
|--------|----------|
| 12-15 hours | **HIGH** |

---

# IMPLEMENTATION PRIORITY MATRIX

## CRITICAL (Do This Week) - 9-15 hours

| Issue | Fix | Hours |
|-------|-----|-------|
| R2/C1 | Migrate credentials to Bitwarden | 4 |
| C3 | Stop automating Gmail/Gov sites | 2 |
| C2 | Encrypt and isolate browser-state | 4 |

## HIGH (Do This Month) - 35-45 hours

| Issue | Fix | Hours |
|-------|-----|-------|
| R1 | Replace UI scraping with APIs | 6 |
| R3 | Migrate entities to Zoho CRM | 8 |
| C4 | Implement health checks & alerts | 10 |
| C5 | Build resilient selector system | 12 |
| C6 | Request API access from distributors | 2 |
| C7 | Migrate to SQLite | 8 |

## MEDIUM (Do This Quarter) - 17-20 hours

| Issue | Fix | Hours |
|-------|-----|-------|
| R4 | Remove redundant form-fill code | 3 |
| C8 | Implement form state machine | 15 |

---

# WHAT TO DELETE

After implementing solutions, delete these files:

| File | Reason | Replace With |
|------|--------|--------------|
| `.credentials.json` | Security risk | Bitwarden |
| `gmail-searcher.py` | ToS violation, fragile | Gmail API |
| `drive-search.py` | ToS violation, fragile | Drive API |
| `drive-search-simple.py` | Same | Drive API |
| `onedrive-search.py` | ToS violation | Graph API |
| `check-drive-session.py` | Not needed | API approach |
| `entity-profiles.json` | Redundant | Zoho CRM |

---

# WHAT TO KEEP (Modified)

| File | Modifications |
|------|---------------|
| `playwright-automator.py` | Remove generic form fill, add resilient selectors |
| `mhi-automator.py` | Add health checks, checkpoints, stealth |
| `signup-templates.json` | Migrate to Notion/Airtable eventually |

---

# ESTIMATED TOTAL EFFORT

| Phase | Hours | Timeline |
|-------|-------|----------|
| Critical fixes | 9-15 | Week 1 |
| High priority | 35-45 | Weeks 2-4 |
| Medium priority | 17-20 | Month 2 |
| **TOTAL** | **61-80 hours** | 6-8 weeks |

---

# SUCCESS CRITERIA

After implementation, the system should have:

- [ ] Zero plaintext credentials in repository
- [ ] All Gmail/Drive access via official APIs
- [ ] Separate browser profiles by risk level
- [ ] Daily health checks with alerts
- [ ] SQLite database for structured data
- [ ] Audit log for all automation actions
- [ ] Resilient selector matching
- [ ] Checkpoint/resume for form submissions
- [ ] No automation of government systems
- [ ] API access requests sent to distributors

---

*Solutions document complete. Implementation should proceed in priority order.*
