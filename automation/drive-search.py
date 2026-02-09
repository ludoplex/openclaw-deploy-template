#!/usr/bin/env python3
"""
Search Google Drive for MHI critical business documents
Uses Playwright with persistent browser state
"""
import os
import sys
import json
import asyncio
import re
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

# Paths
BASE_DIR = Path(__file__).parent
BROWSER_STATE_DIR = BASE_DIR / "browser-state"
OUTPUT_FILE = BASE_DIR / "mhi-drive-info.json"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"

BROWSER_STATE_DIR.mkdir(exist_ok=True)
SCREENSHOTS_DIR.mkdir(exist_ok=True)

# Search terms
SEARCH_TERMS = [
    '"Mighty House" EIN',
    '"Mighty House" DUNS', 
    'CAGE code',
    'Tax registration "Mighty House"',
    'Business license "Mighty House"',
    'Wyoming Secretary of State',
    'SAM.gov registration',
    'SBA certification',
    'EDWOSB',
    'HUBZone',
    'EIN',
    'DUNS',
]

# Folders to check
TARGET_FOLDERS = [
    "Critical Info",
    "Business Documents", 
    "MHI",
    "Mighty House",
    "Legal",
    "Tax",
    "Registrations",
]

async def search_google_drive(context, page, results):
    """Search Google Drive for MHI documents"""
    print("\n=== Searching Google Drive ===")
    
    try:
        # Go to Drive
        await page.goto("https://drive.google.com", wait_until="domcontentloaded")
        await asyncio.sleep(3)
        
        # Take screenshot
        await page.screenshot(path=str(SCREENSHOTS_DIR / f"drive_home_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"))
        
        # Check which account is logged in
        account_elem = await page.query_selector('[data-identifier]')
        if account_elem:
            account = await account_elem.get_attribute('data-identifier')
            print(f"Logged in as: {account}")
            results["google_drive_accounts"].append(account)
        
        # Check for profile info
        profile_btn = await page.query_selector('a[aria-label*="Google Account"]')
        if profile_btn:
            email = await profile_btn.get_attribute('aria-label')
            print(f"Account: {email}")
        
        # Search for each term
        for term in SEARCH_TERMS:
            print(f"\nSearching for: {term}")
            try:
                # Find and click search
                search_box = await page.query_selector('input[aria-label="Search in Drive"]')
                if search_box:
                    await search_box.click()
                    await search_box.fill(term)
                    await page.keyboard.press("Enter")
                    await asyncio.sleep(2)
                    
                    # Get results
                    file_items = await page.query_selector_all('[data-id]')
                    if file_items:
                        print(f"  Found {len(file_items)} results")
                        for item in file_items[:5]:  # First 5 results
                            try:
                                name = await item.get_attribute('data-tooltip') or await item.text_content()
                                if name:
                                    results["documents_found"].append({
                                        "search_term": term,
                                        "name": name[:100],
                                        "source": "Google Drive"
                                    })
                                    print(f"    - {name[:60]}")
                            except:
                                pass
                    
                    # Clear search
                    await page.goto("https://drive.google.com", wait_until="domcontentloaded")
                    await asyncio.sleep(1)
            except Exception as e:
                print(f"  Search error: {e}")
        
        # Check target folders
        print("\n--- Checking folders ---")
        for folder in TARGET_FOLDERS:
            try:
                # Search for folder
                search_box = await page.query_selector('input[aria-label="Search in Drive"]')
                if search_box:
                    await search_box.click()
                    await search_box.fill(f'type:folder "{folder}"')
                    await page.keyboard.press("Enter")
                    await asyncio.sleep(2)
                    
                    folders = await page.query_selector_all('[data-id]')
                    if folders:
                        print(f"  Found folder: {folder}")
                        results["folders_found"].append(folder)
                    
                    await page.goto("https://drive.google.com", wait_until="domcontentloaded")
                    await asyncio.sleep(1)
            except:
                pass
                
    except Exception as e:
        print(f"Drive error: {e}")
        results["errors"].append(f"Google Drive: {str(e)}")

async def search_onedrive(context, page, results):
    """Search OneDrive for MHI documents"""
    print("\n=== Searching OneDrive ===")
    
    try:
        await page.goto("https://onedrive.live.com", wait_until="domcontentloaded")
        await asyncio.sleep(3)
        
        await page.screenshot(path=str(SCREENSHOTS_DIR / f"onedrive_home_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"))
        
        # Check if logged in
        current_url = page.url
        if "login" in current_url.lower() or "signin" in current_url.lower():
            print("Not logged into OneDrive")
            results["onedrive_status"] = "not_logged_in"
            return
            
        print("OneDrive accessible")
        results["onedrive_status"] = "logged_in"
        
        # Search for MHI documents
        for term in ["Mighty House", "MHI", "EIN", "DUNS"]:
            try:
                search_box = await page.query_selector('input[type="search"]')
                if search_box:
                    await search_box.click()
                    await search_box.fill(term)
                    await page.keyboard.press("Enter")
                    await asyncio.sleep(2)
                    
                    # Get results
                    items = await page.query_selector_all('[data-automationid="row"]')
                    if items:
                        print(f"  Found {len(items)} results for: {term}")
                        for item in items[:5]:
                            name = await item.text_content()
                            if name:
                                results["documents_found"].append({
                                    "search_term": term,
                                    "name": name[:100],
                                    "source": "OneDrive"
                                })
                    
                    await page.goto("https://onedrive.live.com", wait_until="domcontentloaded")
                    await asyncio.sleep(1)
            except Exception as e:
                print(f"  OneDrive search error: {e}")
                
    except Exception as e:
        print(f"OneDrive error: {e}")
        results["errors"].append(f"OneDrive: {str(e)}")

async def main():
    """Main search function"""
    results = {
        "timestamp": datetime.now().isoformat(),
        "google_drive_accounts": [],
        "onedrive_status": "unknown",
        "documents_found": [],
        "folders_found": [],
        "extracted_info": {},
        "errors": []
    }
    
    print("="*60)
    print("MHI Document Search - Google Drive & OneDrive")
    print("="*60)
    
    playwright = await async_playwright().start()
    
    try:
        # Launch persistent context
        context = await playwright.chromium.launch_persistent_context(
            user_data_dir=str(BROWSER_STATE_DIR),
            headless=False,
            viewport={"width": 1920, "height": 1080},
            args=[
                "--disable-blink-features=AutomationControlled",
            ],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        )
        
        page = context.pages[0] if context.pages else await context.new_page()
        
        # Search Google Drive
        await search_google_drive(context, page, results)
        
        # Search OneDrive
        await search_onedrive(context, page, results)
        
        # Save results
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n\nResults saved to: {OUTPUT_FILE}")
        
        await context.close()
        
    except Exception as e:
        print(f"Error: {e}")
        results["errors"].append(str(e))
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(results, f, indent=2)
    
    await playwright.stop()
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Documents found: {len(results['documents_found'])}")
    print(f"Folders found: {results['folders_found']}")
    print(f"Errors: {len(results['errors'])}")
    
    return results

if __name__ == "__main__":
    asyncio.run(main())
