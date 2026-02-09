#!/usr/bin/env python3
"""
Selenium LLM Exporter - Attaches to Running Chrome
No need to close Chrome - connects via debugging port
"""
import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

OUTPUT_DIR = Path(r"C:\Users\user\.openclaw\workspace\llm-exports")
OUTPUT_DIR.mkdir(exist_ok=True)

DEBUGGING_PORT = 9222

def check_chrome_debugging():
    """Check if Chrome is running with debugging port"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', DEBUGGING_PORT))
    sock.close()
    return result == 0

def launch_chrome_with_debugging():
    """Launch Chrome with remote debugging enabled"""
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    user_data = r"C:\Users\user\AppData\Local\Google\Chrome\User Data"
    
    cmd = [
        chrome_path,
        f"--remote-debugging-port={DEBUGGING_PORT}",
        f"--user-data-dir={user_data}",
        "--profile-directory=Default"
    ]
    
    print(f"Launching Chrome with debugging on port {DEBUGGING_PORT}...")
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3)

def attach_to_chrome():
    """Attach Selenium to existing Chrome"""
    options = Options()
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{DEBUGGING_PORT}")
    
    driver = webdriver.Chrome(options=options)
    return driver

def scroll_to_load_all(driver, max_scrolls=20):
    """Scroll to load lazy-loaded content"""
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    for _ in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def export_arena_all(driver):
    """Export ALL Arena.ai conversations"""
    print("\n" + "="*50)
    print("[Arena.ai] Exporting ALL conversations...")
    print("="*50)
    
    conversations = []
    
    # Go to Arena and get sidebar
    driver.get("https://arena.ai/")
    time.sleep(3)
    
    # Scroll sidebar to load all conversations
    try:
        # Find and scroll sidebar
        sidebar = driver.execute_script("""
            return document.querySelector('[class*="sidebar"]') || 
                   document.querySelector('nav') ||
                   document.querySelector('[class*="history"]');
        """)
        if sidebar:
            for _ in range(30):  # Scroll many times to load all
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", sidebar)
                time.sleep(0.5)
    except:
        pass
    
    # Get all conversation URLs
    conv_links = driver.execute_script("""
        const links = document.querySelectorAll('a[href*="/c/"]');
        return [...new Set([...links].map(a => a.href).filter(h => h.includes('/c/')))];
    """)
    
    print(f"Found {len(conv_links)} unique conversations")
    
    for i, url in enumerate(conv_links):
        try:
            print(f"  [{i+1}/{len(conv_links)}] {url.split('/c/')[-1][:30]}...")
            driver.get(url)
            time.sleep(2)
            
            # Scroll to load full conversation
            scroll_to_load_all(driver, max_scrolls=10)
            
            content = driver.execute_script("return document.body.innerText")
            title = driver.title
            
            conversations.append({
                'id': url.split('/c/')[-1].split('?')[0],
                'url': url,
                'title': title,
                'content': content,
                'extracted_at': datetime.now().isoformat()
            })
        except Exception as e:
            print(f"    Error: {e}")
    
    return conversations

def export_perplexity_all(driver):
    """Export ALL Perplexity threads"""
    print("\n" + "="*50)
    print("[Perplexity] Exporting ALL conversations...")
    print("="*50)
    
    conversations = []
    
    driver.get("https://www.perplexity.ai/library")
    time.sleep(3)
    
    # Scroll to load all threads
    scroll_to_load_all(driver, max_scrolls=50)
    
    # Get all thread URLs
    thread_links = driver.execute_script("""
        const links = document.querySelectorAll('a[href*="/search/"]');
        return [...new Set([...links].map(a => a.href))];
    """)
    
    print(f"Found {len(thread_links)} threads")
    
    for i, url in enumerate(thread_links):
        try:
            print(f"  [{i+1}/{len(thread_links)}] {url.split('/')[-1][:40]}...")
            driver.get(url)
            time.sleep(2)
            scroll_to_load_all(driver, max_scrolls=5)
            
            content = driver.execute_script("return document.body.innerText")
            
            conversations.append({
                'id': url.split('/')[-1].split('?')[0],
                'url': url,
                'content': content,
                'extracted_at': datetime.now().isoformat()
            })
        except Exception as e:
            print(f"    Error: {e}")
    
    return conversations

def export_chatgpt_all(driver):
    """Export ALL ChatGPT conversations"""
    print("\n" + "="*50)
    print("[ChatGPT] Exporting ALL conversations...")
    print("="*50)
    
    conversations = []
    
    driver.get("https://chatgpt.com/")
    time.sleep(3)
    
    # Scroll sidebar
    for _ in range(30):
        try:
            driver.execute_script("""
                const sidebar = document.querySelector('nav');
                if (sidebar) sidebar.scrollTop = sidebar.scrollHeight;
            """)
            time.sleep(0.5)
        except:
            break
    
    conv_links = driver.execute_script("""
        const links = document.querySelectorAll('a[href*="/c/"]');
        return [...new Set([...links].map(a => a.href))];
    """)
    
    print(f"Found {len(conv_links)} conversations")
    
    for i, url in enumerate(conv_links):
        try:
            if not url.startswith('http'):
                url = f"https://chatgpt.com{url}"
            print(f"  [{i+1}/{len(conv_links)}] {url.split('/c/')[-1][:30]}...")
            driver.get(url)
            time.sleep(2)
            scroll_to_load_all(driver, max_scrolls=10)
            
            content = driver.execute_script("return document.body.innerText")
            
            conversations.append({
                'id': url.split('/c/')[-1].split('?')[0],
                'url': url,
                'content': content,
                'extracted_at': datetime.now().isoformat()
            })
        except Exception as e:
            print(f"    Error: {e}")
    
    return conversations

def export_claude_all(driver):
    """Export ALL Claude.ai conversations"""
    print("\n" + "="*50)
    print("[Claude.ai] Exporting ALL conversations...")
    print("="*50)
    
    conversations = []
    
    driver.get("https://claude.ai/recents")
    time.sleep(3)
    
    # Scroll to load all
    scroll_to_load_all(driver, max_scrolls=30)
    
    conv_links = driver.execute_script("""
        const links = document.querySelectorAll('a[href*="/chat/"]');
        return [...new Set([...links].map(a => a.href))];
    """)
    
    print(f"Found {len(conv_links)} conversations")
    
    for i, url in enumerate(conv_links):
        try:
            if not url.startswith('http'):
                url = f"https://claude.ai{url}"
            print(f"  [{i+1}/{len(conv_links)}] {url.split('/chat/')[-1][:30]}...")
            driver.get(url)
            time.sleep(2)
            scroll_to_load_all(driver, max_scrolls=10)
            
            content = driver.execute_script("return document.body.innerText")
            
            conversations.append({
                'id': url.split('/chat/')[-1].split('?')[0],
                'url': url,
                'content': content,
                'extracted_at': datetime.now().isoformat()
            })
        except Exception as e:
            print(f"    Error: {e}")
    
    return conversations

def main():
    print("="*60)
    print("Selenium LLM Exporter - Attach to Chrome")
    print("="*60)
    
    # Check if Chrome has debugging enabled
    if not check_chrome_debugging():
        print(f"\n⚠️  Chrome not running with debugging port {DEBUGGING_PORT}")
        print("\nClose Chrome and relaunch with:")
        print(f'  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port={DEBUGGING_PORT}')
        
        response = input("\nOr type 'launch' to do it automatically: ").strip().lower()
        if response == 'launch':
            # Kill existing Chrome
            os.system("taskkill /f /im chrome.exe 2>nul")
            time.sleep(2)
            launch_chrome_with_debugging()
        else:
            print("Exiting.")
            return
    
    print(f"\n✅ Connecting to Chrome on port {DEBUGGING_PORT}...")
    driver = attach_to_chrome()
    print(f"   Connected! Current page: {driver.title}")
    
    all_exports = {}
    
    try:
        all_exports['arena'] = export_arena_all(driver)
        all_exports['perplexity'] = export_perplexity_all(driver)
        all_exports['chatgpt'] = export_chatgpt_all(driver)
        all_exports['claude'] = export_claude_all(driver)
        
        # Save
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # JSON
        json_file = OUTPUT_DIR / f"all_llm_exports_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(all_exports, f, indent=2, ensure_ascii=False)
        
        # Markdown per platform
        for platform, convos in all_exports.items():
            if convos:
                md_file = OUTPUT_DIR / f"{platform}_export_{timestamp}.md"
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(f"# {platform.title()} Export\n")
                    f.write(f"Exported: {datetime.now().isoformat()}\n")
                    f.write(f"Total: {len(convos)} conversations\n\n")
                    for conv in convos:
                        f.write(f"## {conv.get('title', conv.get('id', 'Unknown'))}\n")
                        f.write(f"**URL:** {conv.get('url', 'N/A')}\n\n")
                        f.write("```\n")
                        f.write(conv.get('content', '')[:50000])
                        f.write("\n```\n\n---\n\n")
        
        print("\n" + "="*60)
        print("EXPORT COMPLETE")
        print("="*60)
        total = sum(len(c) for c in all_exports.values())
        print(f"Total: {total} conversations")
        for platform, convos in all_exports.items():
            print(f"  {platform}: {len(convos)}")
        print(f"\nSaved to: {OUTPUT_DIR}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Don't quit - leave Chrome running
    print("\n(Chrome left running - you can continue using it)")

if __name__ == '__main__':
    main()
