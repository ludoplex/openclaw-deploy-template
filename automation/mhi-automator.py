#!/usr/bin/env python3
"""
MHI Complete Web Automator
- Portal logins
- Program signups  
- Authorized reseller applications
- Platform registrations

Uses Playwright with persistent browser state
"""
import os
import sys
import json
import asyncio
import re
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List
from getpass import getpass

from playwright.async_api import async_playwright, Page, BrowserContext

BASE_DIR = Path(__file__).parent
PROFILES_FILE = BASE_DIR / "entity-profiles.json"
CREDENTIALS_FILE = BASE_DIR / ".credentials.json"
TEMPLATES_FILE = BASE_DIR / "signup-templates.json"
BROWSER_STATE_DIR = BASE_DIR / "browser-state"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
LOGS_DIR = BASE_DIR / "logs"

for d in [BROWSER_STATE_DIR, SCREENSHOTS_DIR, LOGS_DIR]:
    d.mkdir(exist_ok=True)


class MHIAutomator:
    """Complete web automation for MHI operations"""
    
    def __init__(self):
        self.playwright = None
        self.context = None
        self.page = None
        self.profiles = self._load_json(PROFILES_FILE, {"entities": {}})
        self.credentials = self._load_json(CREDENTIALS_FILE, {"portals": {}})
        self.templates = self._load_json(TEMPLATES_FILE, {})
        self.log_file = LOGS_DIR / f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    def _load_json(self, path, default):
        if path.exists():
            with open(path, encoding='utf-8') as f:
                return json.load(f)
        return default
    
    def _save_credentials(self):
        with open(CREDENTIALS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.credentials, f, indent=2)
    
    def log(self, message: str):
        """Log action"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        line = f"[{timestamp}] {message}"
        print(line)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(line + "\n")
    
    async def start(self, headless=False):
        """Start persistent browser"""
        self.playwright = await async_playwright().start()
        
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=str(BROWSER_STATE_DIR),
            headless=headless,
            viewport={"width": 1920, "height": 1080},
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"],
            ignore_default_args=["--enable-automation"],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36",
            locale="en-US",
            timezone_id="America/Denver",
        )
        
        self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()
        self.log(f"Browser started (headless={headless})")
        return self.page
    
    async def stop(self):
        """Close browser (state preserved)"""
        if self.context:
            await self.context.close()
        if self.playwright:
            await self.playwright.stop()
        self.log("Browser closed, state preserved")
    
    async def screenshot(self, name: str = "screenshot") -> Path:
        """Take screenshot"""
        path = SCREENSHOTS_DIR / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        await self.page.screenshot(path=str(path), full_page=True)
        self.log(f"Screenshot: {path.name}")
        return path
    
    # === CREDENTIAL MANAGEMENT ===
    
    def add_credential(self, portal: str, username: str, password: str, 
                       url: str = None, notes: str = None, entity: str = "mhi"):
        """Save portal credentials"""
        self.credentials.setdefault("portals", {})[portal] = {
            "username": username,
            "password": password,
            "url": url,
            "entity": entity,
            "notes": notes,
            "updated": datetime.now().isoformat()
        }
        self._save_credentials()
        self.log(f"Saved credentials: {portal}")
    
    def get_credential(self, portal: str) -> dict:
        return self.credentials.get("portals", {}).get(portal, {})
    
    def list_credentials(self) -> List[str]:
        return list(self.credentials.get("portals", {}).keys())
    
    # === SMART FORM DETECTION ===
    
    async def detect_form_fields(self) -> Dict[str, str]:
        """Detect all form fields on current page"""
        fields = await self.page.evaluate("""
            () => {
                const fields = {};
                const inputs = document.querySelectorAll('input, textarea, select');
                inputs.forEach(el => {
                    const name = el.name || el.id || el.placeholder || '';
                    const type = el.type || el.tagName.toLowerCase();
                    const label = el.labels?.[0]?.textContent?.trim() || '';
                    if (name || label) {
                        fields[name || label] = {
                            selector: el.name ? `[name="${el.name}"]` : 
                                     el.id ? `#${el.id}` : null,
                            type: type,
                            label: label,
                            required: el.required
                        };
                    }
                });
                return fields;
            }
        """)
        self.log(f"Detected {len(fields)} form fields")
        return fields
    
    async def fill_field_smart(self, field_name: str, value: str) -> bool:
        """Smart field filling with multiple selector strategies"""
        if not value:
            return False
            
        selectors = [
            f'input[name="{field_name}"]',
            f'input[name*="{field_name}" i]',
            f'input[id="{field_name}"]',
            f'input[id*="{field_name}" i]',
            f'input[placeholder*="{field_name}" i]',
            f'textarea[name*="{field_name}" i]',
            f'select[name*="{field_name}" i]',
            f'input[aria-label*="{field_name}" i]',
            # Label-based
            f'label:has-text("{field_name}") + input',
            f'label:has-text("{field_name}") input',
        ]
        
        for sel in selectors:
            try:
                elem = await self.page.query_selector(sel)
                if elem:
                    tag = await elem.evaluate("e => e.tagName.toLowerCase()")
                    if tag == "select":
                        await self.page.select_option(sel, label=str(value))
                    else:
                        await self.page.fill(sel, str(value), timeout=1000)
                    self.log(f"  ✓ {field_name}: {str(value)[:30]}")
                    return True
            except:
                pass
        return False
    
    # === ENTITY DATA ===
    
    def get_entity_data(self, entity: str = "mhi") -> dict:
        """Get flattened entity data for form filling"""
        ent = self.profiles.get("entities", {}).get(entity, {})
        if not ent:
            return {}
        
        addr = ent.get("address", {})
        owner = ent.get("contacts", {}).get("owner", {})
        auth_rep = ent.get("contacts", {}).get("authorized_rep", {})
        
        # Use authorized rep if available, else owner
        contact = auth_rep if auth_rep.get("name") else owner
        
        return {
            # Company
            "company": ent.get("legal_name"),
            "company_name": ent.get("legal_name"),
            "business_name": ent.get("legal_name"),
            "legal_name": ent.get("legal_name"),
            "organization": ent.get("legal_name"),
            "dba": ent.get("dba"),
            "entity_type": ent.get("entity_type"),
            
            # Address
            "address": addr.get("street"),
            "street": addr.get("street"),
            "address1": addr.get("street"),
            "address_1": addr.get("street"),
            "street_address": addr.get("street"),
            "city": addr.get("city"),
            "state": addr.get("state"),
            "province": addr.get("state"),
            "zip": addr.get("zip"),
            "zipcode": addr.get("zip"),
            "zip_code": addr.get("zip"),
            "postal": addr.get("zip"),
            "postal_code": addr.get("zip"),
            "country": addr.get("country", "United States"),
            
            # Contact
            "name": contact.get("name"),
            "full_name": contact.get("name"),
            "contact_name": contact.get("name"),
            "first_name": contact.get("name", "").split()[0] if contact.get("name") else "",
            "last_name": " ".join(contact.get("name", "").split()[1:]) if contact.get("name") else "",
            "firstname": contact.get("name", "").split()[0] if contact.get("name") else "",
            "lastname": " ".join(contact.get("name", "").split()[1:]) if contact.get("name") else "",
            "email": contact.get("email"),
            "email_address": contact.get("email"),
            "phone": contact.get("phone"),
            "telephone": contact.get("phone"),
            "phone_number": contact.get("phone"),
            "mobile": contact.get("phone"),
            "title": contact.get("title"),
            "job_title": contact.get("title"),
            "position": contact.get("title"),
            
            # Business details
            "website": ent.get("website"),
            "url": ent.get("website"),
            "web": ent.get("website"),
            "ein": ent.get("ein"),
            "tax_id": ent.get("ein"),
            "federal_tax_id": ent.get("ein"),
            "fein": ent.get("ein"),
            "duns": ent.get("duns"),
            "duns_number": ent.get("duns"),
            "cage": ent.get("cage_code"),
            "cage_code": ent.get("cage_code"),
        }
    
    async def fill_form_with_entity(self, entity: str = "mhi", extra_data: dict = None) -> int:
        """Fill current page form with entity data"""
        data = self.get_entity_data(entity)
        if extra_data:
            data.update(extra_data)
        
        self.log(f"Filling form with {entity.upper()} data...")
        
        filled = 0
        for field, value in data.items():
            if await self.fill_field_smart(field, value):
                filled += 1
        
        self.log(f"Filled {filled} fields")
        await self.screenshot(f"form_filled_{entity}")
        return filled
    
    # === LOGIN ===
    
    async def login(self, portal: str, username: str = None, password: str = None) -> bool:
        """Login to portal"""
        cred = self.get_credential(portal)
        username = username or cred.get("username")
        password = password or cred.get("password")
        url = cred.get("url")
        
        if not url:
            self.log(f"No URL configured for {portal}")
            return False
        
        self.log(f"Logging into {portal}...")
        await self.page.goto(url, wait_until="domcontentloaded")
        await asyncio.sleep(2)
        
        # Try common login patterns
        username_filled = False
        password_filled = False
        
        for sel in ['input[name="username"]', 'input[name="email"]', 'input[name="user"]',
                    'input[type="email"]', '#username', '#email', '#user', 
                    'input[name="userId"]', 'input[name="login"]']:
            try:
                await self.page.fill(sel, username, timeout=1000)
                username_filled = True
                self.log(f"  ✓ Username: {sel}")
                break
            except:
                pass
        
        for sel in ['input[name="password"]', 'input[type="password"]', '#password']:
            try:
                await self.page.fill(sel, password, timeout=1000)
                password_filled = True
                self.log(f"  ✓ Password: {sel}")
                break
            except:
                pass
        
        # Submit
        for sel in ['button[type="submit"]', 'input[type="submit"]',
                    'button:has-text("Log in")', 'button:has-text("Sign in")',
                    'button:has-text("Login")', 'button:has-text("Submit")']:
            try:
                await self.page.click(sel, timeout=1000)
                self.log(f"  ✓ Submit clicked")
                break
            except:
                pass
        
        await asyncio.sleep(3)
        await self.screenshot(f"login_{portal}")
        
        return username_filled and password_filled
    
    # === SIGNUP / APPLICATION ===
    
    async def signup(self, platform: str, entity: str = "mhi", 
                     email: str = None, password: str = None) -> bool:
        """Sign up for a new platform/program"""
        
        # Check templates for URL
        for category in ["reseller_applications", "vendor_programs", "platforms", "govcon_registrations"]:
            if platform in self.templates.get(category, {}):
                url = self.templates[category][platform].get("url")
                break
        else:
            url = None
        
        if not url:
            self.log(f"No template for {platform}, please provide URL")
            return False
        
        self.log(f"Starting signup: {platform}")
        await self.page.goto(url, wait_until="domcontentloaded")
        await asyncio.sleep(3)
        
        # Take initial screenshot
        await self.screenshot(f"signup_{platform}_start")
        
        # Detect and fill form
        await self.fill_form_with_entity(entity)
        
        # Fill email/password if creating account
        entity_data = self.get_entity_data(entity)
        if email:
            await self.fill_field_smart("email", email)
        elif entity_data.get("email"):
            await self.fill_field_smart("email", entity_data["email"])
        
        if password:
            await self.fill_field_smart("password", password)
            await self.fill_field_smart("confirm_password", password)
            await self.fill_field_smart("password_confirm", password)
        
        await self.screenshot(f"signup_{platform}_filled")
        self.log(f"Form filled for {platform} - REVIEW BEFORE SUBMITTING")
        
        return True
    
    async def apply_reseller(self, distributor: str, entity: str = "mhi") -> bool:
        """Apply for authorized reseller status"""
        template = self.templates.get("reseller_applications", {}).get(distributor)
        
        if not template:
            self.log(f"No template for distributor: {distributor}")
            self.log(f"Available: {list(self.templates.get('reseller_applications', {}).keys())}")
            return False
        
        url = template.get("url")
        self.log(f"Starting reseller application: {distributor}")
        
        await self.page.goto(url, wait_until="domcontentloaded")
        await asyncio.sleep(3)
        
        await self.fill_form_with_entity(entity)
        await self.screenshot(f"reseller_{distributor}_filled")
        
        self.log(f"Application filled - REVIEW BEFORE SUBMITTING")
        return True
    
    # === QUICK ACTIONS ===
    
    async def goto(self, url: str):
        """Navigate to URL"""
        await self.page.goto(url, wait_until="domcontentloaded")
        self.log(f"Navigated to: {url}")
    
    async def click_text(self, text: str):
        """Click element containing text"""
        await self.page.click(f"text={text}")
        self.log(f"Clicked: {text}")
    
    async def wait_for_navigation(self, timeout: int = 30000):
        """Wait for page navigation"""
        await self.page.wait_for_load_state("domcontentloaded", timeout=timeout)
    
    async def get_page_text(self) -> str:
        """Get all text from page"""
        return await self.page.evaluate("() => document.body.innerText")
    
    async def handle_captcha(self):
        """Wait for user to solve captcha"""
        self.log("⚠️  CAPTCHA detected - please solve manually")
        self.log("Press Enter when done...")
        await asyncio.get_event_loop().run_in_executor(None, input)
        self.log("Continuing...")


async def interactive():
    """Interactive CLI"""
    auto = MHIAutomator()
    
    print("\n" + "="*60)
    print("MHI Web Automator - Full Automation Suite")
    print("="*60)
    print("Capabilities: Login | Signup | Reseller Applications | Forms")
    
    await auto.start(headless=False)
    
    commands = """
Commands:
  NAVIGATION
    goto <url>           - Navigate to URL
    screenshot           - Take screenshot
    
  CREDENTIALS  
    add <portal>         - Add portal credentials
    list                 - List saved portals
    login <portal>       - Login to portal
    
  APPLICATIONS
    signup <platform>    - Start signup process
    reseller <dist>      - Apply for reseller status
    fill [entity]        - Fill current form (mhi/dsaic/computer_store)
    
  UTILITIES
    detect               - Detect form fields
    captcha              - Wait for captcha solve
    text                 - Get page text
    
  exit                   - Close browser
"""
    
    while True:
        print(commands)
        try:
            cmd = input("\n> ").strip().split()
            if not cmd:
                continue
        except (EOFError, KeyboardInterrupt):
            break
        
        action = cmd[0].lower()
        args = cmd[1:]
        
        try:
            if action == "goto" and args:
                await auto.goto(args[0])
            
            elif action == "screenshot":
                await auto.screenshot()
            
            elif action == "add" and args:
                portal = args[0]
                url = input("  Login URL: ").strip()
                username = input("  Username: ").strip()
                password = getpass("  Password: ")
                entity = input("  Entity (mhi/dsaic) [mhi]: ").strip() or "mhi"
                auto.add_credential(portal, username, password, url, entity=entity)
            
            elif action == "list":
                print("\nSaved portals:")
                for name in auto.list_credentials():
                    cred = auto.get_credential(name)
                    print(f"  {name}: {cred.get('username')} ({cred.get('entity', 'mhi')})")
            
            elif action == "login" and args:
                await auto.login(args[0])
            
            elif action == "signup" and args:
                entity = args[1] if len(args) > 1 else "mhi"
                await auto.signup(args[0], entity)
            
            elif action == "reseller" and args:
                entity = args[1] if len(args) > 1 else "mhi"
                await auto.apply_reseller(args[0], entity)
            
            elif action == "fill":
                entity = args[0] if args else "mhi"
                await auto.fill_form_with_entity(entity)
            
            elif action == "detect":
                fields = await auto.detect_form_fields()
                for name, info in fields.items():
                    print(f"  {name}: {info.get('type')} {'*' if info.get('required') else ''}")
            
            elif action == "captcha":
                await auto.handle_captcha()
            
            elif action == "text":
                text = await auto.get_page_text()
                print(text[:2000])
            
            elif action == "exit":
                break
            
            else:
                print(f"Unknown command: {action}")
                
        except Exception as e:
            print(f"Error: {e}")
    
    await auto.stop()


if __name__ == "__main__":
    asyncio.run(interactive())
