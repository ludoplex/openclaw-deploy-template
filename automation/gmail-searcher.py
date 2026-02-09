#!/usr/bin/env python3
"""
Gmail Search Script for MHI Business Info
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

BASE_DIR = Path(__file__).parent
BROWSER_STATE_DIR = BASE_DIR / "browser-state"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
OUTPUT_FILE = BASE_DIR / "gmail-search-results.json"

BROWSER_STATE_DIR.mkdir(exist_ok=True)
SCREENSHOTS_DIR.mkdir(exist_ok=True)

# Gmail accounts to search
GMAIL_ACCOUNTS = [
    "theanderproject@gmail.com",
    "racheljeannewilliams@gmail.com",
    "mightyhouseinc@gmail.com"
]

# Search queries organized by category
SEARCH_QUERIES = {
    "BUSINESS_INFO": [
        '"EIN" OR "tax id" OR "federal id"',
        '"DUNS" OR "D-U-N-S"',
        '"CAGE code"',
        '"SAM.gov" OR "SAM registration"',
        '"Wyoming Secretary of State"',
    ],
    "PORTALS_PLATFORMS": [
        '"welcome to" (portal OR partner OR reseller)',
        '"account created" OR "registration confirmed"',
        '"partner portal" OR "dealer portal"',
        'from:ingram OR from:synnex OR from:dandh OR from:climb',
        'from:dell OR from:hp OR from:lenovo OR from:microsoft OR from:cisco',
    ],
    "PARTNER_ASSETS": [
        '"letter of authorization" OR "LoA"',
        '"authorized reseller"',
        '"marketing materials" OR "partner assets"',
        '"deal registration"',
        'has:attachment filename:pdf',
    ]
}

class GmailSearcher:
    def __init__(self):
        self.playwright = None
        self.context = None
        self.page = None
        self.results = {
            "search_date": datetime.now().isoformat(),
            "accounts": {}
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
        
        print(f"Browser started with persistent state")
        return self
    
    async def stop(self):
        """Close browser (state is auto-saved)"""
        if self.context:
            await self.context.close()
        if self.playwright:
            await self.playwright.stop()
        print("Browser closed. State preserved.")
    
    async def screenshot(self, name):
        """Take screenshot"""
        path = SCREENSHOTS_DIR / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        await self.page.screenshot(path=str(path), full_page=False)
        print(f"  Screenshot: {path.name}")
        return str(path)
    
    async def check_gmail_login(self):
        """Check if we're logged into Gmail"""
        await self.page.goto("https://mail.google.com")
        await asyncio.sleep(3)
        
        # Check for login prompt
        if "accounts.google.com" in self.page.url:
            return None
        
        # Try to get current account email
        try:
            # Click on account switcher to see current account
            account_btn = await self.page.query_selector('a[aria-label*="Google Account"]')
            if account_btn:
                label = await account_btn.get_attribute('aria-label')
                # Extract email from label
                email_match = re.search(r'[\w\.-]+@[\w\.-]+', label)
                if email_match:
                    return email_match.group()
        except:
            pass
        
        return "unknown@gmail.com"
    
    async def switch_account(self, target_email):
        """Switch to a different Gmail account"""
        await self.page.goto("https://mail.google.com")
        await asyncio.sleep(2)
        
        # Click account switcher
        try:
            switcher = await self.page.query_selector('a[aria-label*="Google Account"]')
            if switcher:
                await switcher.click()
                await asyncio.sleep(1)
                
                # Look for the target account
                account_link = await self.page.query_selector(f'a[aria-label*="{target_email}"]')
                if account_link:
                    await account_link.click()
                    await asyncio.sleep(3)
                    return True
        except Exception as e:
            print(f"  Error switching accounts: {e}")
        
        return False
    
    async def perform_search(self, query):
        """Perform a Gmail search and extract results"""
        results = []
        
        # URL encode the query
        import urllib.parse
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://mail.google.com/mail/u/0/#search/{encoded_query}"
        
        await self.page.goto(search_url)
        await asyncio.sleep(3)
        
        # Wait for emails to load
        try:
            await self.page.wait_for_selector('tr.zA', timeout=10000)
        except:
            print(f"    No results or timeout")
            return results
        
        # Get email rows
        rows = await self.page.query_selector_all('tr.zA')
        
        for i, row in enumerate(rows[:15]):  # Limit to first 15 results per query
            try:
                email_data = {}
                
                # Get sender
                sender_elem = await row.query_selector('span.bA4 span[email]')
                if sender_elem:
                    email_data['from'] = await sender_elem.get_attribute('email')
                    email_data['from_name'] = await sender_elem.text_content()
                else:
                    sender_elem = await row.query_selector('.yP, .zF')
                    if sender_elem:
                        email_data['from'] = await sender_elem.text_content()
                
                # Get subject
                subject_elem = await row.query_selector('.bog span, .y2')
                if subject_elem:
                    email_data['subject'] = await subject_elem.text_content()
                
                # Get date
                date_elem = await row.query_selector('.xW.xY span')
                if date_elem:
                    email_data['date'] = await date_elem.get_attribute('title')
                    if not email_data['date']:
                        email_data['date'] = await date_elem.text_content()
                
                # Get snippet
                snippet_elem = await row.query_selector('.y2')
                if snippet_elem:
                    email_data['snippet'] = await snippet_elem.text_content()
                
                # Check for attachments
                attach_elem = await row.query_selector('.yf.xY img[src*="attach"]')
                email_data['has_attachment'] = attach_elem is not None
                
                # Get attachment names if we click into email (skip for now for speed)
                email_data['attachments'] = []
                
                if email_data.get('subject') or email_data.get('from'):
                    email_data['search_query'] = query
                    results.append(email_data)
                    
            except Exception as e:
                print(f"    Error parsing row: {e}")
        
        return results
    
    async def search_account(self, email):
        """Search all queries for a specific account"""
        print(f"\n{'='*60}")
        print(f"Searching: {email}")
        print('='*60)
        
        account_results = {
            "email": email,
            "search_time": datetime.now().isoformat(),
            "categories": {}
        }
        
        for category, queries in SEARCH_QUERIES.items():
            print(f"\n  Category: {category}")
            account_results["categories"][category] = []
            
            for query in queries:
                print(f"    Query: {query[:50]}...")
                
                try:
                    results = await self.perform_search(query)
                    if results:
                        print(f"    Found {len(results)} emails")
                        for r in results:
                            r['category'] = category
                            account_results["categories"][category].append(r)
                    else:
                        print(f"    No results")
                except Exception as e:
                    print(f"    Error: {e}")
                
                await asyncio.sleep(1)  # Rate limiting
        
        return account_results
    
    async def run_all_searches(self):
        """Run searches for all accounts"""
        print("\n" + "="*60)
        print("Gmail Search for MHI Business Info")
        print("="*60)
        
        # First, go to Gmail and check login status
        current_account = await self.check_gmail_login()
        
        if current_account is None:
            print("\n⚠️  NOT LOGGED INTO GMAIL!")
            print("Please log in to at least one Gmail account first.")
            print("Opening Gmail login page...")
            await self.page.goto("https://accounts.google.com/signin/v2/identifier?service=mail")
            await self.screenshot("gmail_login_needed")
            return
        
        print(f"\nCurrently logged in as: {current_account}")
        await self.screenshot("gmail_current_state")
        
        # Search the current account
        results = await self.search_account(current_account)
        self.results["accounts"][current_account] = results
        
        # Try to switch to other accounts
        for target_email in GMAIL_ACCOUNTS:
            if target_email == current_account:
                continue
            
            print(f"\n\nAttempting to switch to: {target_email}")
            
            # Try to switch accounts
            if await self.switch_account(target_email):
                print(f"  Switched to {target_email}")
                results = await self.search_account(target_email)
                self.results["accounts"][target_email] = results
            else:
                print(f"  ⚠️ Could not switch to {target_email}")
                print(f"  You may need to add this account to the browser profile")
                self.results["accounts"][target_email] = {
                    "email": target_email,
                    "error": "Could not access this account - not logged in",
                    "search_time": datetime.now().isoformat()
                }
        
        # Save results
        self.save_results()
        
        print("\n" + "="*60)
        print("SEARCH COMPLETE")
        print("="*60)
        self.print_summary()
    
    def save_results(self):
        """Save results to JSON file"""
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to: {OUTPUT_FILE}")
    
    def print_summary(self):
        """Print a summary of findings"""
        print("\n📊 SUMMARY OF FINDINGS")
        print("-" * 40)
        
        for email, account_data in self.results.get("accounts", {}).items():
            print(f"\n📧 {email}")
            
            if "error" in account_data:
                print(f"   ❌ {account_data['error']}")
                continue
            
            categories = account_data.get("categories", {})
            total = 0
            
            for category, emails in categories.items():
                count = len(emails)
                total += count
                if count > 0:
                    print(f"   • {category}: {count} emails")
                    for e in emails[:3]:
                        subj = e.get('subject', 'No subject')[:50]
                        print(f"     - {subj}")
                    if count > 3:
                        print(f"     ... and {count - 3} more")
            
            print(f"   Total: {total} relevant emails")


async def main():
    searcher = GmailSearcher()
    
    try:
        await searcher.start(headless=False)  # Visible for debugging
        await searcher.run_all_searches()
    finally:
        await searcher.stop()


if __name__ == "__main__":
    asyncio.run(main())
