#!/usr/bin/env python3
"""
MHI Web Automator
Reliable web portal login, signup, and form filling automation
Uses persistent Chrome profile with all saved sessions
"""
import os
import sys
import json
import time
import socket
import subprocess
from pathlib import Path
from datetime import datetime
from getpass import getpass

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Paths
BASE_DIR = Path(__file__).parent
PROFILES_FILE = BASE_DIR / "entity-profiles.json"
CREDENTIALS_FILE = BASE_DIR / ".credentials.json"  # gitignored
SESSIONS_DIR = BASE_DIR / "sessions"
SESSIONS_DIR.mkdir(exist_ok=True)

CHROME_USER_DATA = r"C:\Users\user\AppData\Local\Google\Chrome\User Data"
DEBUGGING_PORT = 9222

class WebAutomator:
    def __init__(self):
        self.driver = None
        self.profiles = self._load_profiles()
        self.credentials = self._load_credentials()
        
    def _load_profiles(self):
        if PROFILES_FILE.exists():
            with open(PROFILES_FILE) as f:
                return json.load(f)
        return {"entities": {}}
    
    def _load_credentials(self):
        if CREDENTIALS_FILE.exists():
            with open(CREDENTIALS_FILE) as f:
                return json.load(f)
        return {"portals": {}}
    
    def _save_credentials(self):
        with open(CREDENTIALS_FILE, 'w') as f:
            json.dump(self.credentials, f, indent=2)
        print(f"Credentials saved to {CREDENTIALS_FILE}")
    
    def add_credential(self, portal_name, username, password, url=None, notes=None):
        """Add/update portal credentials"""
        self.credentials.setdefault("portals", {})[portal_name] = {
            "username": username,
            "password": password,
            "url": url,
            "notes": notes,
            "added": datetime.now().isoformat()
        }
        self._save_credentials()
    
    def get_credential(self, portal_name):
        """Get credentials for a portal"""
        return self.credentials.get("portals", {}).get(portal_name)
    
    def _check_chrome_debugging(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', DEBUGGING_PORT))
        sock.close()
        return result == 0
    
    def _launch_chrome_debugging(self):
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        cmd = [
            chrome_path,
            f"--remote-debugging-port={DEBUGGING_PORT}",
            f"--user-data-dir={CHROME_USER_DATA}",
            "--profile-directory=Default"
        ]
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)
    
    def connect(self, headless=False):
        """Connect to Chrome (start if needed)"""
        if not self._check_chrome_debugging():
            print("Starting Chrome with debugging port...")
            os.system("taskkill /f /im chrome.exe 2>nul")
            time.sleep(2)
            self._launch_chrome_debugging()
            time.sleep(2)
        
        options = Options()
        options.add_experimental_option("debuggerAddress", f"127.0.0.1:{DEBUGGING_PORT}")
        
        self.driver = webdriver.Chrome(options=options)
        print(f"Connected to Chrome: {self.driver.title}")
        return self.driver
    
    def wait_for(self, selector, by=By.CSS_SELECTOR, timeout=10):
        """Wait for element"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, selector))
            )
        except TimeoutException:
            return None
    
    def fill_field(self, selector, value, by=By.CSS_SELECTOR, clear=True):
        """Fill a form field"""
        elem = self.wait_for(selector, by)
        if elem:
            if clear:
                elem.clear()
            elem.send_keys(value)
            return True
        return False
    
    def click(self, selector, by=By.CSS_SELECTOR):
        """Click an element"""
        elem = self.wait_for(selector, by)
        if elem:
            elem.click()
            return True
        return False
    
    def select_dropdown(self, selector, value, by=By.CSS_SELECTOR):
        """Select dropdown option"""
        elem = self.wait_for(selector, by)
        if elem:
            select = Select(elem)
            try:
                select.select_by_visible_text(value)
            except:
                select.select_by_value(value)
            return True
        return False
    
    def login_portal(self, portal_name, username=None, password=None, url=None):
        """Generic portal login"""
        cred = self.get_credential(portal_name)
        if cred:
            username = username or cred.get('username')
            password = password or cred.get('password')
            url = url or cred.get('url')
        
        if not all([username, password, url]):
            print(f"Missing credentials for {portal_name}")
            return False
        
        print(f"Logging into {portal_name}...")
        self.driver.get(url)
        time.sleep(2)
        
        # Common login field patterns
        username_selectors = [
            'input[name="username"]', 'input[name="email"]', 'input[name="user"]',
            'input[type="email"]', 'input[id*="user"]', 'input[id*="email"]',
            '#username', '#email', '#login-email'
        ]
        password_selectors = [
            'input[name="password"]', 'input[type="password"]',
            '#password', 'input[id*="pass"]'
        ]
        submit_selectors = [
            'button[type="submit"]', 'input[type="submit"]',
            'button:contains("Log")', 'button:contains("Sign")',
            '.login-button', '#login-button'
        ]
        
        # Try username fields
        for sel in username_selectors:
            if self.fill_field(sel, username):
                print(f"  Filled username with {sel}")
                break
        
        # Try password fields
        for sel in password_selectors:
            if self.fill_field(sel, password):
                print(f"  Filled password with {sel}")
                break
        
        # Try submit
        for sel in submit_selectors:
            if self.click(sel):
                print(f"  Clicked submit with {sel}")
                break
        
        time.sleep(3)
        return True
    
    def fill_supplier_application(self, entity="mhi", form_data=None):
        """Fill supplier/reseller application with entity data"""
        entity_data = self.profiles.get("entities", {}).get(entity, {})
        if not entity_data:
            print(f"Entity {entity} not found")
            return False
        
        addr = entity_data.get("address", {})
        owner = entity_data.get("contacts", {}).get("owner", {})
        
        # Common field mappings
        field_map = {
            # Company info
            'company': entity_data.get('legal_name'),
            'company_name': entity_data.get('legal_name'),
            'business_name': entity_data.get('legal_name'),
            'dba': entity_data.get('dba'),
            'legal_name': entity_data.get('legal_name'),
            
            # Address
            'address': addr.get('street'),
            'street': addr.get('street'),
            'address1': addr.get('street'),
            'city': addr.get('city'),
            'state': addr.get('state'),
            'zip': addr.get('zip'),
            'zipcode': addr.get('zip'),
            'postal': addr.get('zip'),
            'country': addr.get('country'),
            
            # Contact
            'name': owner.get('name'),
            'contact_name': owner.get('name'),
            'first_name': owner.get('name', '').split()[0] if owner.get('name') else '',
            'last_name': owner.get('name', '').split()[-1] if owner.get('name') else '',
            'email': owner.get('email'),
            'phone': owner.get('phone'),
            'title': owner.get('title'),
            
            # Business
            'website': entity_data.get('website'),
            'ein': entity_data.get('ein'),
            'tax_id': entity_data.get('ein'),
            'duns': entity_data.get('duns'),
        }
        
        # Override with form_data if provided
        if form_data:
            field_map.update(form_data)
        
        # Try to fill all fields
        filled = 0
        for field_name, value in field_map.items():
            if not value:
                continue
            selectors = [
                f'input[name*="{field_name}" i]',
                f'input[id*="{field_name}" i]',
                f'input[placeholder*="{field_name}" i]',
                f'textarea[name*="{field_name}" i]',
            ]
            for sel in selectors:
                try:
                    if self.fill_field(sel, value):
                        filled += 1
                        print(f"  Filled {field_name}: {value[:30]}...")
                        break
                except:
                    pass
        
        print(f"Filled {filled} fields")
        return filled > 0
    
    def screenshot(self, name="screenshot"):
        """Take screenshot for verification"""
        path = SESSIONS_DIR / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        self.driver.save_screenshot(str(path))
        print(f"Screenshot: {path}")
        return path


# Portal-specific handlers
class SupplierPortals:
    """Pre-configured handlers for common supplier portals"""
    
    @staticmethod
    def ingram_micro(automator):
        """Ingram Micro iMConnect login"""
        automator.driver.get("https://usa.ingrammicro.com/")
        time.sleep(2)
        # Click login, handle their specific flow
        automator.click("a[href*='login']")
        time.sleep(2)
        cred = automator.get_credential("ingram_micro")
        if cred:
            automator.fill_field("#username", cred['username'])
            automator.fill_field("#password", cred['password'])
            automator.click("button[type='submit']")
    
    @staticmethod
    def td_synnex(automator):
        """TD SYNNEX ECexpress login"""
        automator.driver.get("https://ec.synnex.com/")
        time.sleep(2)
        cred = automator.get_credential("td_synnex")
        if cred:
            automator.fill_field("input[name='username']", cred['username'])
            automator.fill_field("input[name='password']", cred['password'])
            automator.click("button[type='submit']")
    
    @staticmethod  
    def dh_distributing(automator):
        """D&H login"""
        automator.driver.get("https://www.dandh.com/")
        time.sleep(2)
        cred = automator.get_credential("dh")
        if cred:
            automator.click("a[href*='login']")
            time.sleep(1)
            automator.fill_field("#email", cred['username'])
            automator.fill_field("#password", cred['password'])
            automator.click("button[type='submit']")


def interactive_mode():
    """Interactive CLI for the automator"""
    auto = WebAutomator()
    
    print("\n" + "="*60)
    print("MHI Web Automator")
    print("="*60)
    
    while True:
        print("\nCommands:")
        print("  1. Connect to Chrome")
        print("  2. Add/update credentials")
        print("  3. Login to portal")
        print("  4. Fill supplier application")
        print("  5. Go to URL")
        print("  6. Screenshot")
        print("  7. List credentials")
        print("  0. Exit")
        
        choice = input("\n> ").strip()
        
        if choice == "1":
            auto.connect()
        elif choice == "2":
            portal = input("Portal name: ").strip()
            url = input("Login URL: ").strip()
            username = input("Username: ").strip()
            password = getpass("Password: ")
            auto.add_credential(portal, username, password, url)
        elif choice == "3":
            portal = input("Portal name: ").strip()
            auto.login_portal(portal)
        elif choice == "4":
            entity = input("Entity (mhi/dsaic/computer_store): ").strip() or "mhi"
            auto.fill_supplier_application(entity)
        elif choice == "5":
            url = input("URL: ").strip()
            auto.driver.get(url)
        elif choice == "6":
            auto.screenshot()
        elif choice == "7":
            for name, cred in auto.credentials.get("portals", {}).items():
                print(f"  {name}: {cred.get('username')} @ {cred.get('url')}")
        elif choice == "0":
            break


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Command line mode
        cmd = sys.argv[1]
        auto = WebAutomator()
        auto.connect()
        
        if cmd == "login" and len(sys.argv) > 2:
            auto.login_portal(sys.argv[2])
        elif cmd == "fill" and len(sys.argv) > 2:
            auto.driver.get(sys.argv[2])
            time.sleep(2)
            auto.fill_supplier_application()
    else:
        interactive_mode()
