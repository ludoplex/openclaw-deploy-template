#!/usr/bin/env python3
"""
OneDrive Document Search
Searches OneDrive for MHI critical business documents
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
BROWSER_STATE_DIR = BASE_DIR / "browser-state"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
OUTPUT_FILE = BASE_DIR / "onedrive-docs.json"

BROWSER_STATE_DIR.mkdir(exist_ok=True)
SCREENSHOTS_DIR.mkdir(exist_ok=True)

# Search terms
SEARCH_TERMS = [
    "Mighty House",
    "MHI",
    "Critical Info",
    "Business",
    "EIN",
    "DUNS",
    "CAGE",
    "Tax",
    "Certificate",
    "EDWOSB",
    "HUBZone",
    "SAM.gov",
    "W-9",
    "Insurance",
    "COI",
    "Partner",
    "Reseller",
    "Authorization"
]

# Folders to check
FOLDERS_TO_CHECK = [
    "Documents",
    "Business",
    "MHI",
    "Legal",
]


class OneDriveSearcher:
    def __init__(self):
        self.playwright = None
        self.context = None
        self.page = None
        self.results = {
            "search_date": datetime.now().isoformat(),
            "documents": [],
            "folders_checked": [],
            "search_terms_used": SEARCH_TERMS,
            "errors": []
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
        
        print(f"Browser started. State saved to: {BROWSER_STATE_DIR}")
        return self.page
    
    async def stop(self):
        """Close browser"""
        if self.context:
            await self.context.close()
        if self.playwright:
            await self.playwright.stop()
        print("Browser closed.")
    
    async def screenshot(self, name="screenshot"):
        """Take screenshot"""
        path = SCREENSHOTS_DIR / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        await self.page.screenshot(path=str(path), full_page=True)
        print(f"Screenshot: {path}")
        return path
    
    async def navigate_to_onedrive(self):
        """Navigate to OneDrive"""
        print("Navigating to OneDrive...")
        await self.page.goto("https://onedrive.live.com", wait_until="domcontentloaded")
        await asyncio.sleep(3)
        
        # Check if we need to login
        current_url = self.page.url
        print(f"Current URL: {current_url}")
        
        await self.screenshot("onedrive_initial")
        
        # Check for login needed
        if "login" in current_url.lower() or "signin" in current_url.lower():
            print("Login may be required. Please login manually if needed.")
            await asyncio.sleep(5)
        
        return True
    
    async def search_documents(self, query):
        """Search for documents using OneDrive search"""
        print(f"Searching for: {query}")
        
        try:
            # Wait for search box - OneDrive uses different selectors
            search_selectors = [
                'input[type="search"]',
                'input[aria-label*="Search" i]',
                'input[placeholder*="Search" i]',
                '[data-automationid="searchBox"] input',
                '#O365_SearchBoxContainer input',
                '#searchBox',
                '.ms-SearchBox-field',
            ]
            
            search_box = None
            for selector in search_selectors:
                try:
                    elem = await self.page.wait_for_selector(selector, timeout=3000)
                    if elem:
                        search_box = elem
                        print(f"  Found search box: {selector}")
                        break
                except:
                    pass
            
            if not search_box:
                print("  Could not find search box")
                await self.screenshot(f"search_fail_{query[:20]}")
                return []
            
            # Clear and fill search
            await search_box.click()
            await asyncio.sleep(0.5)
            await search_box.fill(query)
            await asyncio.sleep(0.5)
            
            # Press enter to search
            await self.page.keyboard.press("Enter")
            await asyncio.sleep(3)
            
            await self.screenshot(f"search_{query[:20]}")
            
            # Extract results
            results = await self.extract_search_results()
            print(f"  Found {len(results)} results for '{query}'")
            
            return results
            
        except Exception as e:
            print(f"  Search error: {e}")
            self.results["errors"].append(f"Search error for '{query}': {str(e)}")
            return []
    
    async def extract_search_results(self):
        """Extract document information from search results"""
        results = []
        
        try:
            # Wait for results to load
            await asyncio.sleep(2)
            
            # Common OneDrive file item selectors
            item_selectors = [
                '[data-automationid="row"]',
                '[role="row"]',
                '.ms-List-cell',
                '.od-ItemRow',
                '[data-list-index]',
                '.fileList-row',
            ]
            
            items = []
            for selector in item_selectors:
                try:
                    items = await self.page.query_selector_all(selector)
                    if items and len(items) > 0:
                        print(f"  Using selector: {selector}, found {len(items)} items")
                        break
                except:
                    pass
            
            for item in items[:20]:  # Limit to first 20 results
                try:
                    doc_info = await self.extract_item_info(item)
                    if doc_info and doc_info.get("filename"):
                        results.append(doc_info)
                except Exception as e:
                    print(f"    Error extracting item: {e}")
            
        except Exception as e:
            print(f"  Error extracting results: {e}")
        
        return results
    
    async def extract_item_info(self, item):
        """Extract information from a single file item"""
        try:
            # Get all text content
            text = await item.text_content()
            if not text:
                return None
            
            # Try to get filename
            filename = ""
            name_selectors = [
                '[data-automationid="name"]',
                '.ms-DetailsRow-cell[data-automationid="name"]',
                '[class*="nameCell"]',
                '.od-ItemContent-name',
                'button[class*="name" i]',
                'a[class*="name" i]',
            ]
            
            for selector in name_selectors:
                try:
                    elem = await item.query_selector(selector)
                    if elem:
                        filename = await elem.text_content()
                        if filename:
                            break
                except:
                    pass
            
            if not filename:
                # Try to extract from full text
                filename = text.split('\n')[0][:100] if text else ""
            
            # Try to get modified date
            modified = ""
            date_selectors = [
                '[data-automationid="modified"]',
                '[class*="modified" i]',
                '[class*="date" i]',
            ]
            
            for selector in date_selectors:
                try:
                    elem = await item.query_selector(selector)
                    if elem:
                        modified = await elem.text_content()
                        if modified:
                            break
                except:
                    pass
            
            # Try to get path/location
            path = ""
            path_selectors = [
                '[data-automationid="location"]',
                '[class*="location" i]',
                '[class*="path" i]',
            ]
            
            for selector in path_selectors:
                try:
                    elem = await item.query_selector(selector)
                    if elem:
                        path = await elem.text_content()
                        if path:
                            break
                except:
                    pass
            
            return {
                "filename": filename.strip() if filename else "",
                "path": path.strip() if path else "",
                "modified": modified.strip() if modified else "",
                "raw_text": text[:500] if text else ""
            }
            
        except Exception as e:
            return None
    
    async def check_folder(self, folder_name):
        """Navigate to and check a specific folder"""
        print(f"Checking folder: {folder_name}")
        
        try:
            # Go back to root first
            await self.page.goto("https://onedrive.live.com/?view=0", wait_until="domcontentloaded")
            await asyncio.sleep(2)
            
            # Look for the folder
            folder_selectors = [
                f'button:has-text("{folder_name}")',
                f'[data-automationid="name"]:has-text("{folder_name}")',
                f'[title*="{folder_name}" i]',
                f'[aria-label*="{folder_name}" i]',
            ]
            
            folder = None
            for selector in folder_selectors:
                try:
                    folder = await self.page.wait_for_selector(selector, timeout=3000)
                    if folder:
                        break
                except:
                    pass
            
            if folder:
                await folder.dblclick()
                await asyncio.sleep(2)
                await self.screenshot(f"folder_{folder_name}")
                
                # Get files in folder
                results = await self.extract_search_results()
                self.results["folders_checked"].append({
                    "folder": folder_name,
                    "files_found": len(results)
                })
                
                return results
            else:
                print(f"  Folder not found: {folder_name}")
                return []
                
        except Exception as e:
            print(f"  Error checking folder: {e}")
            return []
    
    async def run_full_search(self):
        """Run the complete search process"""
        print("\n" + "="*60)
        print("OneDrive Document Search")
        print("="*60 + "\n")
        
        await self.start(headless=False)
        
        try:
            # Navigate to OneDrive
            await self.navigate_to_onedrive()
            await asyncio.sleep(3)
            
            # Search for each term
            all_docs = []
            seen_files = set()
            
            for term in SEARCH_TERMS:
                results = await self.search_documents(term)
                for doc in results:
                    filename = doc.get("filename", "")
                    if filename and filename not in seen_files:
                        doc["search_term"] = term
                        all_docs.append(doc)
                        seen_files.add(filename)
                
                # Brief pause between searches
                await asyncio.sleep(1)
            
            # Check specific folders
            for folder in FOLDERS_TO_CHECK:
                results = await self.check_folder(folder)
                for doc in results:
                    filename = doc.get("filename", "")
                    if filename and filename not in seen_files:
                        doc["source"] = f"folder:{folder}"
                        all_docs.append(doc)
                        seen_files.add(filename)
            
            self.results["documents"] = all_docs
            self.results["total_unique_documents"] = len(all_docs)
            
            # Save results
            with open(OUTPUT_FILE, 'w') as f:
                json.dump(self.results, f, indent=2)
            
            print(f"\n{'='*60}")
            print(f"Search complete!")
            print(f"Total unique documents found: {len(all_docs)}")
            print(f"Results saved to: {OUTPUT_FILE}")
            print(f"{'='*60}\n")
            
            await self.screenshot("final_state")
            
        except Exception as e:
            print(f"Error during search: {e}")
            self.results["errors"].append(str(e))
            
            # Save partial results
            with open(OUTPUT_FILE, 'w') as f:
                json.dump(self.results, f, indent=2)
        
        finally:
            await self.stop()
        
        return self.results


if __name__ == "__main__":
    asyncio.run(OneDriveSearcher().run_full_search())
