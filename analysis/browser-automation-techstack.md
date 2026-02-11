# Browser Automation & AutoGUI Tech Stack for Maximum Speed

**Target:** Mac M4 VM | Pre-LLM autonomous web operation | Speed-critical

---

## Executive Summary

**Recommended Stack:**
- **Primary:** Playwright (Python) with CDP protocol
- **GUI Fallback:** PyObjC/Quartz (native macOS) 
- **Anti-Detection:** playwright-stealth + custom fingerprinting
- **Parallelization:** asyncio + browser contexts (not full instances)

**Expected Performance:** 50-200 actions/second for simple operations, 5-20 page loads/second with optimizations.

---

## 1. Browser Automation Framework Comparison

### Selenium vs Playwright vs Puppeteer

| Aspect | Selenium | Playwright | Puppeteer |
|--------|----------|------------|-----------|
| **Speed** | Slowest (HTTP-based WebDriver) | Fastest (CDP/native) | Fast (CDP) |
| **Protocol** | W3C WebDriver (HTTP) | CDP + custom protocols | Chrome DevTools Protocol |
| **Auto-wait** | Manual | Built-in smart waits | Manual/semi-auto |
| **Parallel** | Needs Grid setup | Native contexts | Manual management |
| **Browser Support** | All (via drivers) | Chromium, Firefox, WebKit | Chromium only |
| **macOS M4** | Good (ARM drivers exist) | Excellent (native ARM) | Good |
| **Memory/instance** | ~150-300MB | ~80-150MB per context | ~100-200MB |

### Benchmark Data (Typical Operations)

```
Operation                    Selenium    Playwright    Puppeteer
─────────────────────────────────────────────────────────────────
Page load (cached)           200-400ms   80-150ms      100-180ms
Element click                50-100ms    10-30ms       15-40ms
Text input (100 chars)       100-200ms   20-50ms       30-60ms
Screenshot                   100-300ms   30-80ms       40-100ms
DOM query (1000 elements)    50-150ms    10-30ms       15-40ms
Navigation                   300-800ms   100-300ms     150-400ms
```

### Winner: Playwright

**Why Playwright for Mac M4:**
1. Native ARM64 binaries (no Rosetta overhead)
2. Single API for Chromium/Firefox/WebKit
3. Built-in parallelization via browser contexts
4. Smart auto-waiting eliminates flaky timing code
5. Request interception is trivial
6. Persistent contexts for session management

---

## 2. Headless vs Headed Performance

### Performance Difference

```
Mode          Overhead    Memory    Detection Risk    Use Case
────────────────────────────────────────────────────────────────
Headless      Baseline    Lower     Higher           Scraping, CI/CD
Headed        +10-20%     +50MB     Lower            Anti-detect sites
New Headless  +5%         +20MB     Medium           Best balance
```

### Playwright's "New Headless" Mode

```python
browser = await playwright.chromium.launch(
    headless=True,
    args=['--headless=new']  # Chrome 112+ new headless
)
```

**Recommendation:** Use `--headless=new` by default. Switch to headed only for sites with aggressive bot detection (major social platforms, banking).

---

## 3. Speed Optimizations

### 3.1 Request Interception (CRITICAL)

Block unnecessary resources for 2-5x speedup:

```python
async def route_handler(route):
    if route.request.resource_type in ['image', 'media', 'font', 'stylesheet']:
        await route.abort()
    else:
        await route.continue_()

await page.route('**/*', route_handler)

# Or more aggressive - block by URL pattern
await page.route('**/*.{png,jpg,jpeg,gif,svg,woff,woff2,ttf,css}', 
                 lambda r: r.abort())
await page.route('**/analytics*', lambda r: r.abort())
await page.route('**/tracking*', lambda r: r.abort())
await page.route('**/ads*', lambda r: r.abort())
```

### 3.2 Browser Launch Optimizations

```python
browser = await playwright.chromium.launch(
    headless=True,
    args=[
        '--disable-gpu',
        '--disable-dev-shm-usage',
        '--disable-setuid-sandbox',
        '--no-sandbox',
        '--disable-accelerated-2d-canvas',
        '--disable-gl-drawing-for-tests',
        '--disable-extensions',
        '--disable-plugins',
        '--disable-background-networking',
        '--disable-background-timer-throttling',
        '--disable-backgrounding-occluded-windows',
        '--disable-breakpad',
        '--disable-component-extensions-with-background-pages',
        '--disable-component-update',
        '--disable-default-apps',
        '--disable-features=TranslateUI',
        '--disable-hang-monitor',
        '--disable-ipc-flooding-protection',
        '--disable-popup-blocking',
        '--disable-prompt-on-repost',
        '--disable-renderer-backgrounding',
        '--disable-sync',
        '--metrics-recording-only',
        '--no-first-run',
        '--safebrowsing-disable-auto-update',
    ]
)
```

### 3.3 Context Reuse (Not Browser Reuse)

```python
# FAST: Reuse browser, create lightweight contexts
browser = await playwright.chromium.launch()

# Each "session" is a context (shares browser process)
async def fast_session():
    context = await browser.new_context()
    page = await context.new_page()
    # ... do work ...
    await context.close()  # Fast cleanup

# Contexts share: browser process, compiled JS cache
# Contexts isolate: cookies, storage, permissions
```

### 3.4 Parallel Execution Pattern

```python
import asyncio
from playwright.async_api import async_playwright

async def worker(browser, task_queue, results):
    context = await browser.new_context()
    page = await context.new_page()
    
    while True:
        try:
            url = await asyncio.wait_for(task_queue.get(), timeout=1.0)
        except asyncio.TimeoutError:
            break
        
        try:
            await page.goto(url, wait_until='domcontentloaded')
            # Extract data...
            results.append({'url': url, 'status': 'ok'})
        except Exception as e:
            results.append({'url': url, 'error': str(e)})
        
        task_queue.task_done()
    
    await context.close()

async def parallel_scrape(urls, num_workers=10):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        task_queue = asyncio.Queue()
        for url in urls:
            await task_queue.put(url)
        
        results = []
        workers = [
            asyncio.create_task(worker(browser, task_queue, results))
            for _ in range(num_workers)
        ]
        
        await asyncio.gather(*workers)
        await browser.close()
        
        return results
```

### 3.5 Wait Strategy Optimization

```python
# SLOW: Fixed waits
await page.wait_for_timeout(2000)  # Never do this

# MEDIUM: Wait for selector
await page.wait_for_selector('#content')

# FAST: Wait for network idle (only when needed)
await page.goto(url, wait_until='domcontentloaded')  # Faster than 'load'

# FASTEST: Wait for specific condition
await page.wait_for_function('window.dataLoaded === true')
```

---

## 4. Anti-Detection Techniques

### 4.1 playwright-stealth

```bash
pip install playwright-stealth
```

```python
from playwright_stealth import stealth_async

browser = await playwright.chromium.launch(headless=True)
context = await browser.new_context(
    viewport={'width': 1920, 'height': 1080},
    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ...',
    locale='en-US',
    timezone_id='America/New_York',
)
page = await context.new_page()
await stealth_async(page)
```

### 4.2 Manual Stealth Patches

```python
# Override navigator properties
await page.add_init_script("""
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
    Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
    
    // Chrome-specific
    window.chrome = { runtime: {} };
    
    // Permissions
    const originalQuery = window.navigator.permissions.query;
    window.navigator.permissions.query = (parameters) => (
        parameters.name === 'notifications' ?
        Promise.resolve({ state: Notification.permission }) :
        originalQuery(parameters)
    );
""")
```

### 4.3 Fingerprint Randomization

```python
import random

def random_viewport():
    viewports = [
        {'width': 1920, 'height': 1080},
        {'width': 1366, 'height': 768},
        {'width': 1536, 'height': 864},
        {'width': 1440, 'height': 900},
    ]
    return random.choice(viewports)

def random_user_agent():
    # Use up-to-date Chrome/Safari UAs for Mac
    agents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    ]
    return random.choice(agents)

context = await browser.new_context(
    viewport=random_viewport(),
    user_agent=random_user_agent(),
    locale='en-US',
    timezone_id='America/Denver',
    geolocation={'latitude': 39.7392, 'longitude': -104.9903},
    permissions=['geolocation'],
)
```

---

## 5. GUI Automation (PyAutoGUI Alternatives)

### Comparison for macOS

| Library | Speed | Native macOS | Reliability | Use Case |
|---------|-------|--------------|-------------|----------|
| PyAutoGUI | Slow (100ms+) | Via Quartz | Good | Cross-platform |
| PyObjC/Quartz | Fast (1-5ms) | Native | Excellent | macOS-specific |
| cliclick | Very Fast | Native CLI | Good | Simple clicks |
| Hammerspoon | Fast | Lua scripting | Excellent | Complex automation |

### 5.1 PyObjC + Quartz (Recommended for macOS)

```python
from Quartz import (
    CGEventCreateMouseEvent, CGEventPost, kCGEventMouseMoved,
    kCGEventLeftMouseDown, kCGEventLeftMouseUp, kCGHIDEventTap,
    CGEventCreateKeyboardEvent, CGEventSetFlags
)
from AppKit import NSScreen, NSWorkspace
import time

def click(x, y):
    """Native macOS click - ~1-5ms"""
    move = CGEventCreateMouseEvent(None, kCGEventMouseMoved, (x, y), 0)
    down = CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, (x, y), 0)
    up = CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, (x, y), 0)
    
    CGEventPost(kCGHIDEventTap, move)
    CGEventPost(kCGHIDEventTap, down)
    CGEventPost(kCGHIDEventTap, up)

def type_text(text):
    """Type text via keyboard events"""
    for char in text:
        # Get key code for character
        event_down = CGEventCreateKeyboardEvent(None, ord(char), True)
        event_up = CGEventCreateKeyboardEvent(None, ord(char), False)
        CGEventPost(kCGHIDEventTap, event_down)
        CGEventPost(kCGHIDEventTap, event_up)
        time.sleep(0.001)  # 1ms between keystrokes
```

### 5.2 Image Recognition for Element Finding

```python
import cv2
import numpy as np
from PIL import ImageGrab

def find_template(template_path, threshold=0.8):
    """Find image template on screen - ~20-50ms"""
    screenshot = np.array(ImageGrab.grab())
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
    
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    
    locations = np.where(result >= threshold)
    if locations[0].size > 0:
        # Return center of first match
        y, x = locations[0][0], locations[1][0]
        h, w = template.shape
        return (x + w // 2, y + h // 2)
    return None

def click_image(template_path):
    """Find and click an image template"""
    coords = find_template(template_path)
    if coords:
        click(*coords)
        return True
    return False
```

### 5.3 Speed Comparison

```
Operation                PyAutoGUI    Quartz      cliclick
──────────────────────────────────────────────────────────
Mouse move              50-100ms     1-2ms       1-2ms
Click                   100-150ms    2-5ms       2-5ms
Type (per char)         10-30ms      1-2ms       1-2ms
Screenshot              100-200ms    20-50ms     N/A
```

---

## 6. Hybrid Approach: Browser + GUI

### When to Use Each

| Scenario | Use Browser Automation | Use GUI Automation |
|----------|------------------------|-------------------|
| Standard web forms | ✅ | ❌ |
| File upload dialogs | ❌ (native dialog) | ✅ |
| CAPTCHA solving | ❌ | ✅ (with solving service) |
| Flash/native plugins | ❌ | ✅ |
| Shadow DOM issues | Try first | Fallback |
| Authentication popups | ❌ | ✅ |
| PDF/download dialogs | Context handling | Fallback |

### Coordination Pattern

```python
class HybridAutomation:
    def __init__(self):
        self.browser = None
        self.page = None
    
    async def setup(self):
        p = await async_playwright().start()
        self.browser = await p.chromium.launch(headless=False)  # Headed for GUI fallback
        self.page = await self.browser.new_page()
    
    async def click_with_fallback(self, selector, timeout=5000):
        """Try browser click, fallback to GUI"""
        try:
            await self.page.click(selector, timeout=timeout)
            return True
        except:
            # Fallback to GUI
            element = await self.page.query_selector(selector)
            if element:
                box = await element.bounding_box()
                if box:
                    # Get browser window position (platform specific)
                    click(box['x'] + box['width']/2, box['y'] + box['height']/2)
                    return True
        return False
    
    async def handle_file_dialog(self, file_path):
        """Handle native file dialogs via GUI"""
        async with self.page.expect_file_chooser() as fc_info:
            await self.page.click('#upload-button')
        file_chooser = await fc_info.value
        await file_chooser.set_files(file_path)
```

---

## 7. Session Persistence & Auth Management

### 7.1 Persistent Browser Context

```python
# Save and restore complete browser state
storage_state_path = 'auth_state.json'

# First run: authenticate and save
context = await browser.new_context()
page = await context.new_page()
await page.goto('https://example.com/login')
# ... perform login ...
await context.storage_state(path=storage_state_path)

# Subsequent runs: restore state
context = await browser.new_context(storage_state=storage_state_path)
# Already logged in!
```

### 7.2 Cookie Management

```python
import json

async def save_cookies(context, path):
    cookies = await context.cookies()
    with open(path, 'w') as f:
        json.dump(cookies, f)

async def load_cookies(context, path):
    with open(path) as f:
        cookies = json.load(f)
    await context.add_cookies(cookies)

# For localStorage/sessionStorage
async def save_storage(page, path):
    storage = await page.evaluate("""() => {
        return {
            localStorage: {...localStorage},
            sessionStorage: {...sessionStorage}
        }
    }""")
    with open(path, 'w') as f:
        json.dump(storage, f)
```

### 7.3 Session Health Monitoring

```python
async def check_session_valid(page, login_indicator_selector):
    """Check if still logged in"""
    try:
        await page.wait_for_selector(login_indicator_selector, timeout=5000)
        return True
    except:
        return False

async def ensure_logged_in(context, login_func):
    """Wrapper to ensure valid session"""
    page = await context.new_page()
    if not await check_session_valid(page, '#user-profile'):
        await login_func(page)
        await context.storage_state(path='auth_state.json')
    return page
```

---

## 8. Error Recovery & Resilience

### 8.1 Retry Pattern

```python
import asyncio
from functools import wraps

def retry(max_attempts=3, delay=1.0, backoff=2.0):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_attempts - 1:
                        await asyncio.sleep(delay * (backoff ** attempt))
            raise last_error
        return wrapper
    return decorator

@retry(max_attempts=3)
async def resilient_navigate(page, url):
    await page.goto(url, timeout=30000)
```

### 8.2 Context Recovery

```python
class ResilientBrowser:
    def __init__(self):
        self.browser = None
        self.context = None
        
    async def get_context(self):
        """Get or recreate context if crashed"""
        if self.context is None or not self.context.pages:
            if self.browser:
                try:
                    await self.browser.close()
                except:
                    pass
            
            p = await async_playwright().start()
            self.browser = await p.chromium.launch()
            self.context = await self.browser.new_context(
                storage_state='auth_state.json' if os.path.exists('auth_state.json') else None
            )
        return self.context
```

---

## 9. Proxy & CAPTCHA Handling

### 9.1 Proxy Rotation

```python
import itertools

class ProxyRotator:
    def __init__(self, proxies):
        self.proxies = itertools.cycle(proxies)
        self.current = None
    
    def next(self):
        self.current = next(self.proxies)
        return self.current
    
    def get_playwright_config(self):
        if not self.current:
            return {}
        # Format: http://user:pass@host:port
        return {'proxy': {'server': self.current}}

# Usage
proxies = ['http://proxy1:8080', 'http://proxy2:8080']
rotator = ProxyRotator(proxies)

context = await browser.new_context(**rotator.get_playwright_config())
```

### 9.2 CAPTCHA Handling (2Captcha Integration)

```python
import aiohttp

class CaptchaSolver:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'http://2captcha.com'
    
    async def solve_recaptcha(self, site_key, page_url):
        async with aiohttp.ClientSession() as session:
            # Submit
            async with session.post(f'{self.base_url}/in.php', data={
                'key': self.api_key,
                'method': 'userrecaptcha',
                'googlekey': site_key,
                'pageurl': page_url,
                'json': 1
            }) as resp:
                result = await resp.json()
                task_id = result['request']
            
            # Poll for result (typically 20-60 seconds)
            for _ in range(60):
                await asyncio.sleep(5)
                async with session.get(f'{self.base_url}/res.php', params={
                    'key': self.api_key,
                    'action': 'get',
                    'id': task_id,
                    'json': 1
                }) as resp:
                    result = await resp.json()
                    if result['status'] == 1:
                        return result['request']
            
            raise Exception('CAPTCHA solving timeout')

# Usage in Playwright
async def submit_with_captcha(page, solver):
    site_key = await page.get_attribute('.g-recaptcha', 'data-sitekey')
    token = await solver.solve_recaptcha(site_key, page.url)
    
    await page.evaluate(f"""
        document.getElementById('g-recaptcha-response').value = '{token}';
    """)
    await page.click('#submit')
```

---

## 10. Platform-Specific Workflows

### 10.1 Twitter/X Automation

```python
class TwitterAutomation:
    def __init__(self, context):
        self.context = context
        
    async def post_tweet(self, text, media_paths=None):
        page = await self.context.new_page()
        await page.goto('https://twitter.com/compose/tweet')
        
        # Wait for composer
        await page.wait_for_selector('[data-testid="tweetTextarea_0"]')
        await page.fill('[data-testid="tweetTextarea_0"]', text)
        
        if media_paths:
            for path in media_paths:
                file_input = await page.query_selector('input[type="file"]')
                await file_input.set_input_files(path)
                await page.wait_for_selector('[data-testid="attachments"]')
        
        await page.click('[data-testid="tweetButton"]')
        await page.wait_for_url('**/status/**')
        
        return page.url
```

### 10.2 Reddit Automation

```python
class RedditAutomation:
    def __init__(self, context):
        self.context = context
    
    async def submit_post(self, subreddit, title, body=None, url=None):
        page = await self.context.new_page()
        await page.goto(f'https://www.reddit.com/r/{subreddit}/submit')
        
        if url:
            await page.click('button:has-text("Link")')
            await page.fill('[placeholder*="Url"]', url)
        else:
            await page.click('button:has-text("Text")')
            if body:
                await page.fill('[placeholder*="Text"]', body)
        
        await page.fill('[placeholder*="Title"]', title)
        await page.click('button:has-text("Post")')
```

### 10.3 Generic Form Filling

```python
async def fill_form(page, form_data: dict):
    """
    form_data = {
        '#name': 'John Doe',
        '#email': 'john@example.com',
        'select#country': 'US',  # Select elements
        'input[type="checkbox"]#terms': True,  # Checkboxes
    }
    """
    for selector, value in form_data.items():
        element = await page.query_selector(selector)
        if not element:
            continue
            
        tag = await element.get_attribute('tagName')
        input_type = await element.get_attribute('type')
        
        if tag.lower() == 'select':
            await page.select_option(selector, value)
        elif input_type == 'checkbox':
            if value:
                await element.check()
            else:
                await element.uncheck()
        elif input_type == 'radio':
            await element.check()
        else:
            await page.fill(selector, str(value))
```

---

## 11. Realistic Performance Expectations

### Actions Per Second by Category

```
Category                    Actions/sec    Notes
────────────────────────────────────────────────────
DOM queries                 100-500        In-memory, fast
Clicks/inputs               20-50          Includes render
Page navigations            2-5            With caching
Full page loads (new)       0.5-2          Depends on site
Parallel contexts           5-10x          Linear scaling
API requests (direct)       50-200         Bypass browser
```

### Bottleneck Analysis

1. **Network latency** - Usually the biggest factor
2. **JavaScript execution** - Heavy SPAs are slow
3. **Rendering** - Headed mode adds overhead
4. **Resource loading** - Block unnecessary assets!
5. **Anti-bot delays** - Some sites rate-limit heavily

### Optimization Priority

1. Block images/CSS/fonts → 3-5x speedup
2. Use domcontentloaded instead of load → 2x
3. Parallel contexts → linear scaling
4. Cache static pages → eliminates network
5. Direct API calls when possible → 10-50x

---

## 12. Recommended Tech Stack Summary

### Core Stack

```bash
# Python 3.11+ (faster async)
pip install playwright playwright-stealth aiohttp

# macOS GUI automation
pip install pyobjc-framework-Quartz pyobjc-framework-AppKit

# Image processing (for GUI fallback)
pip install opencv-python pillow numpy

# Install browsers
playwright install chromium
```

### Project Structure

```
automation/
├── core/
│   ├── browser.py      # Playwright wrapper with optimizations
│   ├── gui.py          # Quartz-based GUI automation
│   ├── hybrid.py       # Browser + GUI coordination
│   └── session.py      # Auth/cookie management
├── workflows/
│   ├── twitter.py
│   ├── reddit.py
│   └── forms.py
├── utils/
│   ├── proxy.py        # Proxy rotation
│   ├── captcha.py      # 2captcha integration
│   └── retry.py        # Error recovery
├── data/
│   ├── auth_states/    # Saved login sessions
│   ├── cookies/        # Cookie jars
│   └── screenshots/    # Debug captures
└── config.yaml
```

### Key Configuration

```yaml
# config.yaml
browser:
  headless: true
  viewport: {width: 1920, height: 1080}
  block_resources: [image, media, font, stylesheet]
  
parallelization:
  max_contexts: 10
  requests_per_second: 5  # Rate limiting
  
anti_detection:
  use_stealth: true
  randomize_fingerprint: true
  human_delays: {min_ms: 50, max_ms: 200}
  
captcha:
  service: 2captcha
  api_key: ${CAPTCHA_API_KEY}
  
proxies:
  enabled: false
  rotation: round_robin
  list: []
```

---

## 13. Mac M4 Specific Notes

### ARM64 Optimizations

1. **Native Playwright binaries** - Uses ARM64 Chromium, no Rosetta
2. **Metal acceleration** - Enable GPU in headed mode for speed
3. **Unified memory** - Browser contexts share memory efficiently
4. **Power efficiency** - Headless uses ~30% less power

### VM Considerations

1. **Display server** - Headless works without display
2. **Accessibility permissions** - Required for GUI automation:
   ```bash
   # Grant accessibility access to Terminal/Python
   # System Settings → Privacy & Security → Accessibility
   ```
3. **Screen recording** - Needed for screenshots of other apps

### Recommended VM Config

```
CPU: 4+ cores (for parallel browsers)
RAM: 8GB+ (each context ~150MB)
Storage: SSD (for fast browser launch)
Display: Virtual display or headless
```

---

## 14. Quick Start Template

```python
#!/usr/bin/env python3
"""Fast browser automation template for Mac M4"""

import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

async def main():
    async with async_playwright() as p:
        # Optimized browser launch
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--disable-gpu',
                '--disable-dev-shm-usage',
                '--disable-extensions',
                '--disable-background-networking',
                '--disable-sync',
                '--no-first-run',
            ]
        )
        
        # Create context with anti-detection
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            locale='en-US',
            timezone_id='America/Denver',
        )
        
        page = await context.new_page()
        await stealth_async(page)
        
        # Block heavy resources
        await page.route('**/*.{png,jpg,gif,svg,woff,woff2,css}', lambda r: r.abort())
        
        # Your automation here
        await page.goto('https://example.com', wait_until='domcontentloaded')
        
        # Save session for reuse
        await context.storage_state(path='session.json')
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
```

---

## Summary

| Component | Recommendation | Speed Impact |
|-----------|---------------|--------------|
| Framework | Playwright | 2-3x vs Selenium |
| Mode | Headless (new) | 10-20% vs headed |
| Parallelization | Contexts (not browsers) | 5-10x scaling |
| Resource blocking | Images/CSS/fonts | 3-5x speedup |
| GUI fallback | PyObjC/Quartz | 50x vs PyAutoGUI |
| Anti-detection | playwright-stealth | Varies |
| CAPTCHA | 2captcha/anticaptcha | External dependency |

**Expected throughput:** 5-20 page operations/second with optimizations, scaling linearly with parallel contexts up to ~50 concurrent.
