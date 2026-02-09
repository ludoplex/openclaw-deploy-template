#!/usr/bin/env python3
"""
Simple Google Drive search script - uses separate browser profile
"""
import os
import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

# Paths
BASE_DIR = Path(__file__).parent
BROWSER_STATE_DIR = BASE_DIR / "browser-state-drive"  # Separate profile
OUTPUT_FILE = BASE_DIR / "mhi-drive-info.json"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"

BROWSER_STATE_DIR.mkdir(exist_ok=True)
SCREENSHOTS_DIR.mkdir(exist_ok=True)

async def main():
    results = {
        "timestamp": datetime.now().isoformat(),
        "google_accounts": [],
        "onedrive_status": "unknown",
        "documents_found": [],
        "folders_found": [],
        "errors": [],
        "notes": []
    }
    
    print("="*60)
    print("MHI Document Search")
    print("="*60)
    print(f"Output: {OUTPUT_FILE}")
    print(f"Browser state: {BROWSER_STATE_DIR}")
    print()
    
    try:
        playwright = await async_playwright().start()
        
        context = await playwright.chromium.launch_persistent_context(
            user_data_dir=str(BROWSER_STATE_DIR),
            headless=False,
            viewport={"width": 1400, "height": 900},
            args=["--disable-blink-features=AutomationControlled", "--no-first-run"],
        )
        
        page = context.pages[0] if context.pages else await context.new_page()
        print("Browser launched")
        
        # Try Google Drive
        print("\n--- Google Drive ---")
        await page.goto("https://drive.google.com", wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(3)
        
        ss_path = SCREENSHOTS_DIR / f"drive_{datetime.now().strftime('%H%M%S')}.png"
        await page.screenshot(path=str(ss_path))
        print(f"Screenshot: {ss_path}")
        
        # Check current URL
        url = page.url
        print(f"URL: {url}")
        
        if "accounts.google.com" in url or "login" in url.lower():
            print("NOT LOGGED IN - Need to login to Google first")
            results["notes"].append("Google Drive requires login")
            # Keep browser open for manual login
            print("\nKeeping browser open - please login manually if needed")
            results["errors"].append("Not logged into Google - manual login required")
        else:
            print("Google Drive accessible")
            
            # Try to identify account
            try:
                account_btn = await page.query_selector('a[href*="SignOutOptions"]')
                if account_btn:
                    aria = await account_btn.get_attribute('aria-label')
                    if aria:
                        print(f"Account: {aria}")
                        results["google_accounts"].append(aria)
            except:
                pass
            
            # Search for key terms
            search_terms = [
                "EIN",
                "DUNS", 
                "Mighty House",
                "CAGE code",
                "SAM.gov",
                "EDWOSB",
            ]
            
            for term in search_terms:
                print(f"\nSearching: {term}")
                try:
                    # Click in search area
                    search = await page.query_selector('[aria-label="Search in Drive"]')
                    if search:
                        await search.click()
                        await asyncio.sleep(0.5)
                        await search.fill(term)
                        await page.keyboard.press("Enter")
                        await asyncio.sleep(2)
                        
                        # Count results
                        items = await page.query_selector_all('[data-id]')
                        print(f"  Found: {len(items)} items")
                        
                        for item in items[:3]:
                            try:
                                tooltip = await item.get_attribute('data-tooltip')
                                if tooltip:
                                    results["documents_found"].append({
                                        "term": term,
                                        "name": tooltip,
                                        "source": "Google Drive"
                                    })
                                    print(f"    - {tooltip[:50]}")
                            except:
                                pass
                        
                        # Go back to Drive home
                        await page.goto("https://drive.google.com", wait_until="domcontentloaded", timeout=20000)
                        await asyncio.sleep(1)
                except Exception as e:
                    print(f"  Error: {e}")
        
        # Save results
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n\nSaved: {OUTPUT_FILE}")
        
        # Close
        await context.close()
        await playwright.stop()
        
    except Exception as e:
        print(f"ERROR: {e}")
        results["errors"].append(str(e))
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(results, f, indent=2)
    
    print("\n" + "="*60)
    print(f"Documents found: {len(results['documents_found'])}")
    print(f"Errors: {len(results['errors'])}")
    print("="*60)
    
    return results

if __name__ == "__main__":
    asyncio.run(main())
