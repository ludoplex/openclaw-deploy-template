#!/usr/bin/env python3
"""
Selenium LLM Session Exporter
Uses existing Chrome profile to access authenticated sessions
Exports from: Arena.ai, Perplexity, ChatGPT, Claude.ai, Grok
"""
import os
import sys
import json
import time
import re
from pathlib import Path
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Output directory
OUTPUT_DIR = Path(r"C:\Users\user\.openclaw\workspace\llm-exports")
OUTPUT_DIR.mkdir(exist_ok=True)

# Chrome profile path
CHROME_USER_DATA = r"C:\Users\user\AppData\Local\Google\Chrome\User Data"

def create_driver(headless=False):
    """Create Chrome driver with user profile"""
    options = Options()
    
    # Use existing Chrome profile for auth
    options.add_argument(f"--user-data-dir={CHROME_USER_DATA}")
    options.add_argument("--profile-directory=Default")
    
    # Other options
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    if headless:
        options.add_argument("--headless=new")
    
    # Use webdriver-manager to get chromedriver
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())
    except:
        service = Service()
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def wait_and_find(driver, selector, by=By.CSS_SELECTOR, timeout=10):
    """Wait for element and return it"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, selector))
        )
        return element
    except TimeoutException:
        return None

def extract_text_content(driver):
    """Extract all text content from page"""
    return driver.execute_script("return document.body.innerText")

def export_arena(driver):
    """Export Arena.ai conversations"""
    print("\n[Arena.ai] Starting export...")
    conversations = []
    
    # Go to Arena homepage to check if logged in
    driver.get("https://arena.ai/")
    time.sleep(3)
    
    # Check for login state
    page_source = driver.page_source
    if "Login" in page_source and "Sign up" in page_source:
        print("  Not logged in to Arena.ai")
        return []
    
    # Get localStorage for auth info
    local_storage = driver.execute_script("""
        return Object.fromEntries(Object.entries(localStorage));
    """)
    
    # Try to find conversation list - check sidebar or history
    # Arena stores conversations in the sidebar
    try:
        # Look for conversation links in sidebar
        conv_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/c/']")
        print(f"  Found {len(conv_links)} conversation links")
        
        conv_urls = list(set([link.get_attribute('href') for link in conv_links if '/c/' in str(link.get_attribute('href'))]))
        print(f"  Unique conversations: {len(conv_urls)}")
        
        for url in conv_urls[:50]:  # Limit to 50 for now
            try:
                driver.get(url)
                time.sleep(2)
                
                content = extract_text_content(driver)
                conv_id = url.split('/c/')[-1].split('?')[0]
                
                conversations.append({
                    'id': conv_id,
                    'url': url,
                    'content': content,
                    'extracted_at': datetime.now().isoformat()
                })
                print(f"  Extracted: {conv_id[:20]}...")
            except Exception as e:
                print(f"  Error on {url}: {e}")
    except Exception as e:
        print(f"  Error finding conversations: {e}")
    
    return conversations

def export_perplexity(driver):
    """Export Perplexity conversations"""
    print("\n[Perplexity] Starting export...")
    conversations = []
    
    # Go to library
    driver.get("https://www.perplexity.ai/library")
    time.sleep(3)
    
    try:
        # Find thread links
        thread_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/search/']")
        urls = list(set([link.get_attribute('href') for link in thread_links]))
        print(f"  Found {len(urls)} threads")
        
        for url in urls[:50]:
            try:
                driver.get(url)
                time.sleep(2)
                
                content = extract_text_content(driver)
                thread_id = url.split('/')[-1].split('?')[0]
                
                conversations.append({
                    'id': thread_id,
                    'url': url,
                    'content': content,
                    'extracted_at': datetime.now().isoformat()
                })
                print(f"  Extracted: {thread_id[:30]}...")
            except Exception as e:
                print(f"  Error: {e}")
    except Exception as e:
        print(f"  Error: {e}")
    
    return conversations

def export_chatgpt(driver):
    """Export ChatGPT conversations"""
    print("\n[ChatGPT] Starting export...")
    conversations = []
    
    driver.get("https://chatgpt.com/")
    time.sleep(3)
    
    try:
        # Find conversation links in sidebar
        conv_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/c/']")
        urls = list(set([link.get_attribute('href') for link in conv_links]))
        print(f"  Found {len(urls)} conversations")
        
        for url in urls[:50]:
            try:
                if not url.startswith('http'):
                    url = f"https://chatgpt.com{url}"
                driver.get(url)
                time.sleep(2)
                
                content = extract_text_content(driver)
                conv_id = url.split('/c/')[-1].split('?')[0]
                
                conversations.append({
                    'id': conv_id,
                    'url': url,
                    'content': content,
                    'extracted_at': datetime.now().isoformat()
                })
                print(f"  Extracted: {conv_id[:20]}...")
            except Exception as e:
                print(f"  Error: {e}")
    except Exception as e:
        print(f"  Error: {e}")
    
    return conversations

def export_claude(driver):
    """Export Claude.ai conversations"""
    print("\n[Claude.ai] Starting export...")
    conversations = []
    
    driver.get("https://claude.ai/")
    time.sleep(3)
    
    try:
        # Find conversation links
        conv_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/chat/']")
        urls = list(set([link.get_attribute('href') for link in conv_links]))
        print(f"  Found {len(urls)} conversations")
        
        for url in urls[:50]:
            try:
                if not url.startswith('http'):
                    url = f"https://claude.ai{url}"
                driver.get(url)
                time.sleep(2)
                
                content = extract_text_content(driver)
                conv_id = url.split('/chat/')[-1].split('?')[0]
                
                conversations.append({
                    'id': conv_id,
                    'url': url,
                    'content': content,
                    'extracted_at': datetime.now().isoformat()
                })
                print(f"  Extracted: {conv_id[:20]}...")
            except Exception as e:
                print(f"  Error: {e}")
    except Exception as e:
        print(f"  Error: {e}")
    
    return conversations

def export_grok(driver):
    """Export Grok (X.com) conversations"""
    print("\n[Grok] Starting export...")
    conversations = []
    
    driver.get("https://x.com/i/grok")
    time.sleep(3)
    
    try:
        content = extract_text_content(driver)
        # Grok doesn't have easy conversation history navigation
        # Just grab current page
        conversations.append({
            'id': 'grok-session',
            'url': 'https://x.com/i/grok',
            'content': content,
            'extracted_at': datetime.now().isoformat()
        })
        print(f"  Extracted current session")
    except Exception as e:
        print(f"  Error: {e}")
    
    return conversations

def main():
    print("="*60)
    print("Selenium LLM Session Exporter")
    print("="*60)
    print(f"Output: {OUTPUT_DIR}")
    print("\n⚠️  Close Chrome before running this script!")
    print("   (Selenium needs exclusive access to the profile)")
    
    input("\nPress Enter when Chrome is closed...")
    
    driver = None
    all_exports = {}
    
    try:
        print("\nStarting Chrome with your profile...")
        driver = create_driver(headless=False)  # Use headless=True for background
        
        # Export from each platform
        all_exports['arena'] = export_arena(driver)
        all_exports['perplexity'] = export_perplexity(driver)
        all_exports['chatgpt'] = export_chatgpt(driver)
        all_exports['claude'] = export_claude(driver)
        all_exports['grok'] = export_grok(driver)
        
        # Save combined export
        output_file = OUTPUT_DIR / f"all_llm_exports_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_exports, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*60}")
        print("EXPORT COMPLETE")
        print(f"{'='*60}")
        for platform, convos in all_exports.items():
            print(f"  {platform}: {len(convos)} conversations")
        print(f"\nSaved to: {output_file}")
        
        # Also save individual markdown files
        for platform, convos in all_exports.items():
            if convos:
                md_file = OUTPUT_DIR / f"{platform}_export.md"
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(f"# {platform.title()} Export\n")
                    f.write(f"Exported: {datetime.now().isoformat()}\n\n")
                    for conv in convos:
                        f.write(f"## {conv.get('id', 'Unknown')}\n")
                        f.write(f"URL: {conv.get('url', 'N/A')}\n\n")
                        f.write(conv.get('content', '')[:10000])  # Limit length
                        f.write("\n\n---\n\n")
                print(f"  Also saved: {md_file}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    main()
