#!/usr/bin/env python3
"""
MHI Playwright Automator
Most reliable web automation for portals, signups, and form filling
Uses persistent browser context (saves cookies/state between sessions)
"""
import os
import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime
from getpass import getpass

from playwright.async_api import async_playwright, Page, BrowserContext

# Paths
BASE_DIR = Path(__file__).parent
PROFILES_FILE = BASE_DIR / "entity-profiles.json"
CREDENTIALS_FILE = BASE_DIR / ".credentials.json"
BROWSER_STATE_DIR = BASE_DIR / "browser-state"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"

BROWSER_STATE_DIR.mkdir(exist_ok=True)
SCREENSHOTS_DIR.mkdir(exist_ok=True)

class PlaywrightAutomator:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.profiles = self._load_json(PROFILES_FILE, {"entities": {}})
        self.credentials = self._load_json(CREDENTIALS_FILE, {"portals": {}})
    
    def _load_json(self, path, default):
        if path.exists():
            with open(path) as f:
                return json.load(f)
        return default
    
    def _save_credentials(self):
        with open(CREDENTIALS_FILE, 'w') as f:
            json.dump(self.credentials, f, indent=2)
    
    async def start(self, headless=False):
        """Start browser with persistent context"""
        self.playwright = await async_playwright().start()
        
        # Use persistent context - saves ALL state between sessions
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=str(BROWSER_STATE_DIR),
            headless=headless,
            viewport={"width": 1920, "height": 1080},
            # Anti-detection
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
            ],
            ignore_default_args=["--enable-automation"],
            # Realistic browser
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            locale="en-US",
            timezone_id="America/Denver",
        )
        
        # Use existing page or create new
        if self.context.pages:
            self.page = self.context.pages[0]
        else:
            self.page = await self.context.new_page()
        
        print(f"Browser started. State saved to: {BROWSER_STATE_DIR}")
        return self.page
    
    async def stop(self):
        """Close browser (state is auto-saved)"""
        if self.context:
            await self.context.close()
        if self.playwright:
            await self.playwright.stop()
        print("Browser closed. State preserved for next session.")
    
    async def goto(self, url: str, wait_until="domcontentloaded"):
        """Navigate to URL"""
        await self.page.goto(url, wait_until=wait_until)
        print(f"Navigated to: {url}")
    
    async def fill(self, selector: str, value: str, timeout=5000):
        """Fill a form field (auto-waits)"""
        try:
            await self.page.fill(selector, value, timeout=timeout)
            return True
        except Exception as e:
            print(f"  Could not fill {selector}: {e}")
            return False
    
    async def click(self, selector: str, timeout=5000):
        """Click element (auto-waits)"""
        try:
            await self.page.click(selector, timeout=timeout)
            return True
        except Exception as e:
            print(f"  Could not click {selector}: {e}")
            return False
    
    async def type_slow(self, selector: str, value: str, delay=50):
        """Type slowly like a human"""
        await self.page.type(selector, value, delay=delay)
    
    async def wait_for(self, selector: str, timeout=10000):
        """Wait for element"""
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            return True
        except:
            return False
    
    async def screenshot(self, name="screenshot"):
        """Take screenshot"""
        path = SCREENSHOTS_DIR / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        await self.page.screenshot(path=str(path), full_page=True)
        print(f"Screenshot: {path}")
        return path
    
    async def get_text(self, selector: str) -> str:
        """Get text content of element"""
        elem = await self.page.query_selector(selector)
        if elem:
            return await elem.text_content()
        return ""
    
    async def is_logged_in(self, indicators: list) -> bool:
        """Check if logged in by looking for indicators"""
        for selector in indicators:
            if await self.page.query_selector(selector):
                return True
        return False
    
    # === CREDENTIAL MANAGEMENT ===
    
    def add_credential(self, portal: str, username: str, password: str, url: str = None, notes: str = None):
        """Store portal credentials"""
        self.credentials.setdefault("portals", {})[portal] = {
            "username": username,
            "password": password,
            "url": url,
            "notes": notes,
            "updated": datetime.now().isoformat()
        }
        self._save_credentials()
        print(f"Saved credentials for {portal}")
    
    def get_credential(self, portal: str) -> dict:
        """Get credentials for portal"""
        return self.credentials.get("portals", {}).get(portal, {})
    
    # === GENERIC LOGIN ===
    
    async def login(self, portal: str, username: str = None, password: str = None, url: str = None):
        """Generic login with auto-detection of form fields"""
        cred = self.get_credential(portal)
        username = username or cred.get("username")
        password = password or cred.get("password")
        url = url or cred.get("url")
        
        if not url:
            print(f"No URL for {portal}")
            return False
        
        print(f"Logging into {portal}...")
        await self.goto(url)
        await asyncio.sleep(2)
        
        # Common username/email selectors
        username_selectors = [
            'input[name="username"]', 'input[name="email"]', 'input[name="user"]',
            'input[name="userId"]', 'input[name="login"]',
            'input[type="email"]', 'input[id*="user" i]', 'input[id*="email" i]',
            'input[id*="login" i]', 'input[placeholder*="email" i]',
            'input[placeholder*="user" i]', '#username', '#email', '#user',
        ]
        
        password_selectors = [
            'input[name="password"]', 'input[name="pass"]', 'input[type="password"]',
            'input[id*="pass" i]', '#password',
        ]
        
        submit_selectors = [
            'button[type="submit"]', 'input[type="submit"]',
            'button:has-text("Log in")', 'button:has-text("Login")',
            'button:has-text("Sign in")', 'button:has-text("Submit")',
            'button:has-text("Continue")', '[class*="login" i] button',
            '[class*="submit" i]',
        ]
        
        # Fill username
        filled_user = False
        for sel in username_selectors:
            try:
                if await self.fill(sel, username, timeout=1000):
                    print(f"  ✓ Username: {sel}")
                    filled_user = True
                    break
            except:
                pass
        
        # Fill password
        filled_pass = False
        for sel in password_selectors:
            try:
                if await self.fill(sel, password, timeout=1000):
                    print(f"  ✓ Password: {sel}")
                    filled_pass = True
                    break
            except:
                pass
        
        if not filled_user or not filled_pass:
            print("  ⚠ Could not find all login fields")
            await self.screenshot(f"{portal}_login_failed")
            return False
        
        # Click submit
        for sel in submit_selectors:
            try:
                if await self.click(sel, timeout=1000):
                    print(f"  ✓ Submit: {sel}")
                    break
            except:
                pass
        
        await asyncio.sleep(3)
        await self.screenshot(f"{portal}_after_login")
        return True
    
    # === FORM FILLING ===
    
    async def fill_entity_form(self, entity: str = "mhi", extra_data: dict = None):
        """Fill form with entity data"""
        ent = self.profiles.get("entities", {}).get(entity, {})
        if not ent:
            print(f"Entity {entity} not found")
            return 0
        
        addr = ent.get("address", {})
        owner = ent.get("contacts", {}).get("owner", {})
        
        # Field mappings
        data = {
            # Company
            "company": ent.get("legal_name"),
            "company_name": ent.get("legal_name"),
            "business": ent.get("legal_name"),
            "organization": ent.get("legal_name"),
            "legal_name": ent.get("legal_name"),
            "dba": ent.get("dba"),
            
            # Address  
            "address": addr.get("street"),
            "street": addr.get("street"),
            "address1": addr.get("street"),
            "address_1": addr.get("street"),
            "city": addr.get("city"),
            "state": addr.get("state"),
            "province": addr.get("state"),
            "zip": addr.get("zip"),
            "zipcode": addr.get("zip"),
            "postal": addr.get("zip"),
            "postal_code": addr.get("zip"),
            "country": addr.get("country", "United States"),
            
            # Contact
            "name": owner.get("name"),
            "contact": owner.get("name"),
            "full_name": owner.get("name"),
            "first_name": owner.get("name", "").split()[0] if owner.get("name") else "",
            "last_name": " ".join(owner.get("name", "").split()[1:]) if owner.get("name") else "",
            "email": owner.get("email"),
            "phone": owner.get("phone"),
            "telephone": owner.get("phone"),
            "title": owner.get("title"),
            "job_title": owner.get("title"),
            
            # Business
            "website": ent.get("website"),
            "url": ent.get("website"),
            "ein": ent.get("ein"),
            "tax_id": ent.get("ein"),
            "federal_tax_id": ent.get("ein"),
            "duns": ent.get("duns"),
            "duns_number": ent.get("duns"),
        }
        
        if extra_data:
            data.update(extra_data)
        
        filled = 0
        for field, value in data.items():
            if not value:
                continue
            
            # Try various selector patterns
            selectors = [
                f'input[name="{field}"]',
                f'input[name*="{field}" i]',
                f'input[id="{field}"]',
                f'input[id*="{field}" i]',
                f'input[placeholder*="{field}" i]',
                f'textarea[name*="{field}" i]',
                f'select[name*="{field}" i]',
            ]
            
            for sel in selectors:
                try:
                    elem = await self.page.query_selector(sel)
                    if elem:
                        tag = await elem.evaluate("e => e.tagName.toLowerCase()")
                        if tag == "select":
                            await self.page.select_option(sel, label=str(value))
                        else:
                            await self.fill(sel, str(value), timeout=500)
                        print(f"  ✓ {field}: {str(value)[:30]}")
                        filled += 1
                        break
                except:
                    pass
        
        print(f"Filled {filled} fields")
        await self.screenshot("form_filled")
        return filled
    
    # === SUPPLIER-SPECIFIC HANDLERS ===
    
    async def login_ingram_micro(self):
        """Ingram Micro specific login"""
        cred = self.get_credential("ingram_micro")
        await self.goto("https://usa.ingrammicro.com/cep/app/login")
        await asyncio.sleep(2)
        
        await self.fill('input[name="username"]', cred.get("username", ""))
        await self.fill('input[name="password"]', cred.get("password", ""))
        await self.click('button[type="submit"]')
        await asyncio.sleep(3)
        
        return await self.is_logged_in(['[class*="account"]', '[class*="logout"]'])
    
    async def login_td_synnex(self):
        """TD SYNNEX ECexpress login"""
        cred = self.get_credential("td_synnex")
        await self.goto("https://ec.synnex.com/ecx/login.html")
        await asyncio.sleep(2)
        
        await self.fill('#userid', cred.get("username", ""))
        await self.fill('#password', cred.get("password", ""))
        await self.click('#loginButton')
        await asyncio.sleep(3)
        
        return await self.is_logged_in(['#logoutLink', '.welcome-user'])
    
    async def login_dh(self):
        """D&H Distributing login"""
        cred = self.get_credential("dh")
        await self.goto("https://www.dandh.com/v4/dhlogin")
        await asyncio.sleep(2)
        
        await self.fill('input[name="email"]', cred.get("username", ""))
        await self.fill('input[name="password"]', cred.get("password", ""))
        await self.click('button[type="submit"]')
        await asyncio.sleep(3)
        
        return await self.is_logged_in(['[class*="logout"]', '[class*="account"]'])


async def interactive():
    """Interactive CLI"""
    auto = PlaywrightAutomator()
    
    print("\n" + "="*60)
    print("MHI Playwright Automator (Persistent Browser)")
    print("="*60)
    
    await auto.start(headless=False)
    
    while True:
        print("\nCommands:")
        print("  1. Go to URL")
        print("  2. Login to portal")
        print("  3. Add credentials")
        print("  4. Fill form with entity data")
        print("  5. Screenshot")
        print("  6. List saved portals")
        print("  7. Login Ingram Micro")
        print("  8. Login TD SYNNEX")
        print("  9. Login D&H")
        print("  0. Exit")
        
        try:
            choice = input("\n> ").strip()
        except EOFError:
            break
        
        if choice == "1":
            url = input("URL: ").strip()
            await auto.goto(url)
        elif choice == "2":
            portal = input("Portal name: ").strip()
            await auto.login(portal)
        elif choice == "3":
            portal = input("Portal name: ").strip()
            url = input("Login URL: ").strip()
            username = input("Username: ").strip()
            password = getpass("Password: ")
            auto.add_credential(portal, username, password, url)
        elif choice == "4":
            entity = input("Entity (mhi/dsaic/computer_store) [mhi]: ").strip() or "mhi"
            await auto.fill_entity_form(entity)
        elif choice == "5":
            await auto.screenshot()
        elif choice == "6":
            for name, cred in auto.credentials.get("portals", {}).items():
                print(f"  {name}: {cred.get('username')} @ {cred.get('url', 'N/A')[:50]}")
        elif choice == "7":
            await auto.login_ingram_micro()
        elif choice == "8":
            await auto.login_td_synnex()
        elif choice == "9":
            await auto.login_dh()
        elif choice == "0":
            break
    
    await auto.stop()


async def cli_command(args):
    """Command line interface"""
    auto = PlaywrightAutomator()
    await auto.start(headless="--headless" in args)
    
    if "login" in args:
        idx = args.index("login")
        if idx + 1 < len(args):
            portal = args[idx + 1]
            success = await auto.login(portal)
            print(f"Login {'succeeded' if success else 'failed'}")
    
    elif "fill" in args:
        idx = args.index("fill")
        if idx + 1 < len(args):
            url = args[idx + 1]
            await auto.goto(url)
            await asyncio.sleep(2)
            entity = args[idx + 2] if idx + 2 < len(args) else "mhi"
            await auto.fill_entity_form(entity)
    
    elif "goto" in args:
        idx = args.index("goto")
        if idx + 1 < len(args):
            await auto.goto(args[idx + 1])
            await asyncio.sleep(5)
            await auto.screenshot()
    
    await auto.stop()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        asyncio.run(cli_command(sys.argv[1:]))
    else:
        asyncio.run(interactive())
