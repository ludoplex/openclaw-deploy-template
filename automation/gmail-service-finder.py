#!/usr/bin/env python3
"""
Gmail Service Account Finder
Searches Gmail for social media and service account registrations
Uses persistent browser state from playwright-automator
"""
import os
import sys
import json
import asyncio
import re
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = Path(__file__).parent
BROWSER_STATE_DIR = BASE_DIR / "browser-state"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
OUTPUT_FILE = BASE_DIR / "gmail-service-accounts.json"

BROWSER_STATE_DIR.mkdir(exist_ok=True)
SCREENSHOTS_DIR.mkdir(exist_ok=True)

# Gmail accounts to search (primary first)
GMAIL_ACCOUNTS = [
    "mightyhouseinc@gmail.com",
    "theanderproject@gmail.com", 
    "racheljeannewilliams@gmail.com"
]

# Search queries for finding service accounts
SEARCH_QUERIES = [
    ("Facebook", "from:facebook OR from:fb.com OR from:facebookmail.com"),
    ("Twitter/X", "from:twitter OR from:x.com OR from:postmaster.twitter.com"),
    ("LinkedIn", "from:linkedin OR from:linkedin.com"),
    ("Instagram", "from:instagram OR from:mail.instagram.com"),
    ("YouTube", "from:youtube OR from:accounts.youtube.com"),
    ("Google Business", "from:google subject:business OR from:business.google.com"),
    ("TikTok", "from:tiktok OR from:tiktok.com"),
    ("Welcome/Verify/Confirm", '"welcome" OR "verify your" OR "confirm your" OR "verification code"'),
    ("Account Created", '"account created" OR "registration complete" OR "successfully registered" OR "sign up"'),
    ("Domain Registrars", "from:godaddy OR from:namecheap OR from:cloudflare"),
    ("Payment/Financial", "from:stripe OR from:paypal OR from:square"),
    ("Amazon Seller", "from:amazon subject:seller OR from:sellercentral"),
    ("eBay", "from:ebay"),
    # Additional service discovery
    ("GitHub", "from:github OR from:noreply.github.com"),
    ("Apple", "from:apple OR from:id.apple.com"),
    ("Microsoft", "from:microsoft OR from:account.microsoft.com"),
    ("Dropbox", "from:dropbox OR from:dropboxmail.com"),
    ("Slack", "from:slack OR from:slackbot"),
    ("Discord", "from:discord OR from:discordapp.com"),
    ("Zoom", "from:zoom OR from:zoom.us"),
    ("AWS", "from:aws OR from:amazonaws.com"),
    ("Shopify", "from:shopify"),
    ("QuickBooks", "from:quickbooks OR from:intuit"),
    ("Adobe", "from:adobe"),
    ("Canva", "from:canva"),
    ("Mailchimp", "from:mailchimp"),
    ("HubSpot", "from:hubspot"),
]


class ServiceAccountFinder:
    def __init__(self):
        self.playwright = None
        self.context = None
        self.page = None
        self.results = {
            "search_date": datetime.now().isoformat(),
            "accounts": {},
            "services_found": []
        }
    
    async def start(self, headless=False):
        """Start browser with persistent context"""
        self.playwright = await async_playwright().start()
        
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=str(BROWSER_STATE_DIR),
            headless=headless,
            viewport={"width": 1920, "height": 1080},
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
            ],
            ignore_default_args=["--enable-automation"],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            locale="en-US",
            timezone_id="America/Denver",
        )
        
        if self.context.pages:
            self.page = self.context.pages[0]
        else:
            self.page = await self.context.new_page()
        
        print(f"Browser started with persistent state from: {BROWSER_STATE_DIR}")
        return self
    
    async def stop(self):
        if self.context:
            await self.context.close()
        if self.playwright:
            await self.playwright.stop()
        print("Browser closed. State preserved.")
    
    async def screenshot(self, name):
        path = SCREENSHOTS_DIR / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        await self.page.screenshot(path=str(path), full_page=False)
        print(f"  [Screenshot] {path.name}")
        return str(path)
    
    async def check_gmail_login(self):
        """Check if logged into Gmail and return current account"""
        await self.page.goto("https://mail.google.com")
        await asyncio.sleep(4)
        
        if "accounts.google.com" in self.page.url:
            return None
        
        try:
            account_btn = await self.page.query_selector('a[aria-label*="Google Account"]')
            if account_btn:
                label = await account_btn.get_attribute('aria-label')
                email_match = re.search(r'[\w\.-]+@[\w\.-]+', label)
                if email_match:
                    return email_match.group()
        except:
            pass
        
        return "unknown@gmail.com"
    
    async def switch_account(self, target_email):
        """Switch to a different Gmail account using account index"""
        # Gmail uses /mail/u/0/, /mail/u/1/, etc. for different accounts
        for i in range(5):  # Try first 5 account slots
            url = f"https://mail.google.com/mail/u/{i}/"
            await self.page.goto(url)
            await asyncio.sleep(3)
            
            if "accounts.google.com" in self.page.url:
                continue
            
            current = await self.check_gmail_login()
            if current and target_email.lower() in current.lower():
                return True
        
        return False
    
    async def perform_search(self, service_name, query):
        """Perform Gmail search and extract email details"""
        results = []
        
        import urllib.parse
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://mail.google.com/mail/u/0/#search/{encoded_query}"
        
        await self.page.goto(search_url)
        await asyncio.sleep(3)
        
        try:
            await self.page.wait_for_selector('tr.zA', timeout=8000)
        except:
            return results
        
        rows = await self.page.query_selector_all('tr.zA')
        
        for row in rows[:20]:  # First 20 per query
            try:
                email_data = {
                    "service": service_name,
                    "query": query
                }
                
                # Sender
                sender_elem = await row.query_selector('span.bA4 span[email]')
                if sender_elem:
                    email_data['from_email'] = await sender_elem.get_attribute('email')
                    email_data['from_name'] = await sender_elem.text_content()
                else:
                    sender_elem = await row.query_selector('.yP, .zF')
                    if sender_elem:
                        email_data['from_email'] = await sender_elem.text_content()
                
                # Subject
                subject_elem = await row.query_selector('.bog span')
                if not subject_elem:
                    subject_elem = await row.query_selector('.y6 span')
                if subject_elem:
                    email_data['subject'] = await subject_elem.text_content()
                
                # Date
                date_elem = await row.query_selector('.xW.xY span')
                if date_elem:
                    email_data['date'] = await date_elem.get_attribute('title')
                    if not email_data['date']:
                        email_data['date'] = await date_elem.text_content()
                
                # Snippet
                snippet_elem = await row.query_selector('.y2')
                if snippet_elem:
                    email_data['snippet'] = (await snippet_elem.text_content())[:200]
                
                # Determine if this is a signup/welcome email
                subject_lower = email_data.get('subject', '').lower()
                snippet_lower = email_data.get('snippet', '').lower()
                
                signup_keywords = ['welcome', 'verify', 'confirm', 'account', 'registration', 
                                   'sign up', 'signup', 'activate', 'new account', 'get started']
                
                email_data['is_signup'] = any(kw in subject_lower or kw in snippet_lower for kw in signup_keywords)
                
                # Extract potential URLs from snippet
                urls = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', email_data.get('snippet', ''))
                email_data['urls_found'] = urls[:3]
                
                if email_data.get('subject') or email_data.get('from_email'):
                    results.append(email_data)
                    
            except Exception as e:
                pass
        
        return results
    
    async def search_account(self, email):
        """Search all queries for a specific account"""
        print(f"\n{'='*60}")
        print(f"[>] Searching: {email}")
        print('='*60)
        
        account_results = {
            "email": email,
            "search_time": datetime.now().isoformat(),
            "services": {}
        }
        
        for service_name, query in SEARCH_QUERIES:
            print(f"  [{service_name}]...", end=" ")
            
            try:
                results = await self.perform_search(service_name, query)
                if results:
                    print(f"[+] {len(results)} emails")
                    account_results["services"][service_name] = results
                    
                    # Add unique services to global list
                    for r in results:
                        if r.get('is_signup'):
                            service_entry = {
                                "service_name": service_name,
                                "email_used": email,
                                "date": r.get('date'),
                                "subject": r.get('subject'),
                                "from": r.get('from_email'),
                                "urls": r.get('urls_found', [])
                            }
                            # Check if not already in list
                            key = f"{service_name}|{email}"
                            existing = [s for s in self.results["services_found"] 
                                       if f"{s['service_name']}|{s['email_used']}" == key]
                            if not existing:
                                self.results["services_found"].append(service_entry)
                else:
                    print("[-] none")
            except Exception as e:
                print(f"[X] error: {e}")
            
            await asyncio.sleep(0.5)  # Rate limiting
        
        return account_results
    
    async def run_all_searches(self):
        """Run searches for all accounts"""
        print("\n" + "="*60)
        print("[*] GMAIL SERVICE ACCOUNT FINDER")
        print("="*60)
        
        current_account = await self.check_gmail_login()
        
        if current_account is None:
            print("\n[!] NOT LOGGED INTO GMAIL!")
            print("Please log in to at least one Gmail account first.")
            print("Use the playwright-automator.py to login, or log in manually.")
            await self.screenshot("gmail_login_needed")
            
            # Return partial results showing what's needed
            self.results["error"] = "Not logged into Gmail"
            self.results["action_required"] = "Log in to Gmail using playwright-automator.py or manually"
            self.save_results()
            return
        
        print(f"\n[+] Currently logged in as: {current_account}")
        await self.screenshot("gmail_logged_in")
        
        # Search the current account
        results = await self.search_account(current_account)
        self.results["accounts"][current_account] = results
        
        # Try to switch to other accounts
        for target_email in GMAIL_ACCOUNTS:
            if target_email.lower() == current_account.lower():
                continue
            
            print(f"\n[~] Attempting to switch to: {target_email}")
            
            if await self.switch_account(target_email):
                print(f"  [+] Switched successfully")
                results = await self.search_account(target_email)
                self.results["accounts"][target_email] = results
            else:
                print(f"  [!] Could not access - not logged in")
                self.results["accounts"][target_email] = {
                    "email": target_email,
                    "error": "Account not accessible - needs login",
                    "search_time": datetime.now().isoformat()
                }
        
        self.save_results()
        self.print_summary()
    
    def save_results(self):
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"\n[SAVED] Results saved to: {OUTPUT_FILE}")
    
    def print_summary(self):
        print("\n" + "="*60)
        print("[*] SUMMARY OF SERVICE ACCOUNTS FOUND")
        print("="*60)
        
        services_by_type = {}
        for svc in self.results.get("services_found", []):
            name = svc["service_name"]
            if name not in services_by_type:
                services_by_type[name] = []
            services_by_type[name].append(svc)
        
        if services_by_type:
            for service, entries in sorted(services_by_type.items()):
                print(f"\n  [{service}]:")
                for e in entries:
                    print(f"   - {e['email_used']} ({e.get('date', 'unknown date')})")
        else:
            print("\nNo confirmed signup/welcome emails found yet.")
            print("This may mean:")
            print("  - Accounts exist but welcome emails were deleted")
            print("  - Need to log into the Gmail accounts first")
        
        print("\n" + "="*60)


async def main():
    finder = ServiceAccountFinder()
    
    try:
        await finder.start(headless=False)  # Visible browser
        await finder.run_all_searches()
    finally:
        await finder.stop()


if __name__ == "__main__":
    asyncio.run(main())
