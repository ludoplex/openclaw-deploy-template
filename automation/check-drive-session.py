#!/usr/bin/env python3
"""
Check if Google Drive session is active in browser-state-drive
"""
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

BASE_DIR = Path(__file__).parent
BROWSER_STATE = BASE_DIR / "browser-state-drive"

async def main():
    print("Checking Google Drive sessions...")
    
    playwright = await async_playwright().start()
    
    try:
        context = await playwright.chromium.launch_persistent_context(
            user_data_dir=str(BROWSER_STATE),
            headless=True,  # Run headless for quick check
            viewport={"width": 1920, "height": 1080},
        )
        
        page = context.pages[0] if context.pages else await context.new_page()
        
        # Go to Drive
        await page.goto("https://drive.google.com/drive/my-drive", wait_until="domcontentloaded")
        await asyncio.sleep(3)
        
        url = page.url
        print(f"Current URL: {url}")
        
        # Check if redirected to login
        if "accounts.google.com" in url or "signin" in url.lower():
            print("STATUS: Not logged in - redirected to login page")
            result = {"logged_in": False, "account": None}
        else:
            print("STATUS: Logged in!")
            # Try to get account info
            account = None
            try:
                account_elem = await page.query_selector('[data-email]')
                if account_elem:
                    account = await account_elem.get_attribute('data-email')
                else:
                    account_elem = await page.query_selector('a[aria-label*="@"]')
                    if account_elem:
                        label = await account_elem.get_attribute('aria-label')
                        if label:
                            import re
                            match = re.search(r'[\w\.-]+@[\w\.-]+', label)
                            if match:
                                account = match.group()
            except:
                pass
            
            print(f"Account: {account or 'Unknown'}")
            result = {"logged_in": True, "account": account, "url": url}
        
        await context.close()
        
        # Output as JSON for parsing
        print("\n---JSON---")
        print(json.dumps(result))
        
    except Exception as e:
        print(f"Error: {e}")
        print("\n---JSON---")
        print(json.dumps({"logged_in": False, "error": str(e)}))
    
    await playwright.stop()

if __name__ == "__main__":
    asyncio.run(main())
