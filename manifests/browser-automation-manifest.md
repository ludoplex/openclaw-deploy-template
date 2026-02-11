# Browser Automation Stack - Source Manifest
## Mac M4 (Apple Silicon ARM64)

**Generated:** 2026-02-10
**Methodology:** SOURCE_MANIFEST - Actual API enumeration, not summaries

---

# 1. AppleScript + Safari Automation

## Version Info
- **AppleScript:** 2.8+ (macOS Sonoma/Sequoia)
- **Safari:** 17.x / 18.x
- **Scripting Dictionary:** Safari.sdef

## Installation
```bash
# AppleScript is built into macOS - no installation required
# Verify osascript availability:
osascript -e 'return "AppleScript works"'

# Enable Safari automation (one-time):
# Safari → Settings → Advanced → "Show features for web developers"
# Safari → Develop → "Allow JavaScript from Apple Events"
```

## Safari AppleScript Dictionary Commands

### Application-Level Commands

```applescript
-- Application properties
tell application "Safari"
    name                           -- string (read-only): app name
    frontmost                      -- boolean: is frontmost app
    version                        -- string (read-only): version number
    
    -- Window management
    windows                        -- list of window objects
    front window                   -- window: frontmost window
    
    -- Document management  
    documents                      -- list of document objects
    front document                 -- document: frontmost document
end tell
```

### Window Class Commands

```applescript
tell application "Safari"
    tell window 1
        -- Properties
        name                       -- string: window title
        index                      -- integer: window index
        bounds                     -- rectangle: {x, y, width, height}
        closeable                  -- boolean
        miniaturizable             -- boolean
        miniaturized               -- boolean
        resizable                  -- boolean
        visible                    -- boolean
        zoomable                   -- boolean
        zoomed                     -- boolean
        
        -- Tab management
        tabs                       -- list of tab objects
        current tab                -- tab: active tab
        
        -- Commands
        close                      -- close window
    end tell
end tell
```

### Tab Class Commands

```applescript
tell application "Safari"
    tell front window
        tell current tab
            -- Properties (read/write)
            URL                    -- string: current URL
            
            -- Properties (read-only)
            name                   -- string: page title
            source                 -- string: HTML source
            text                   -- string: visible text content
            
            -- Commands
            do JavaScript "..."    -- execute JS, returns result
            email contents         -- create email with content
            search the web for "..." -- search selected text
        end tell
        
        -- Tab manipulation
        make new tab with properties {URL:"https://..."}
        close tab 2
        set current tab to tab 3
    end tell
end tell
```

### Document Class Commands

```applescript
tell application "Safari"
    tell document 1
        -- Properties
        name                       -- string: document title
        URL                        -- string: document URL
        source                     -- string: HTML source
        text                       -- string: visible text
        
        -- Commands
        do JavaScript "..."        -- execute JavaScript
    end tell
end tell
```

## JavaScript Bridge: `do JavaScript`

### Signature
```applescript
do JavaScript <text>
    -- text: JavaScript code to execute
    -- Returns: result of JS expression (coerced to AppleScript type)
```

### Examples

```applescript
tell application "Safari"
    tell document 1
        -- Get page title
        set pageTitle to do JavaScript "document.title"
        
        -- Click element
        do JavaScript "document.querySelector('#submit-btn').click()"
        
        -- Fill form field
        do JavaScript "document.getElementById('email').value = 'test@example.com'"
        
        -- Scroll to element
        do JavaScript "document.querySelector('.target').scrollIntoView()"
        
        -- Get element text
        set content to do JavaScript "document.body.innerText"
        
        -- Wait for element (polling)
        do JavaScript "
            (function waitFor() {
                return new Promise(resolve => {
                    const check = setInterval(() => {
                        if (document.querySelector('.loaded')) {
                            clearInterval(check);
                            resolve(true);
                        }
                    }, 100);
                });
            })()
        "
        
        -- Return JSON data
        set jsonData to do JavaScript "JSON.stringify({a:1, b:2})"
        
        -- Execute async and get result
        do JavaScript "
            (async () => {
                const response = await fetch('/api/data');
                return await response.text();
            })()
        "
    end tell
end tell
```

### Type Coercion Rules
| JavaScript Type | AppleScript Type |
|-----------------|------------------|
| string          | text             |
| number          | real/integer     |
| boolean         | boolean          |
| null/undefined  | missing value    |
| Array           | list             |
| Object          | (JSON string)    |
| Promise         | resolved value   |

## Complete Automation Example

```applescript
#!/usr/bin/osascript

on run
    tell application "Safari"
        activate
        
        -- Open new window with URL
        make new document with properties {URL:"https://example.com"}
        delay 2 -- wait for load
        
        tell front document
            -- Wait for page load
            repeat until (do JavaScript "document.readyState") is "complete"
                delay 0.5
            end repeat
            
            -- Interact with page
            set pageTitle to do JavaScript "document.title"
            do JavaScript "document.querySelector('input[name=q]').value = 'test'"
            do JavaScript "document.querySelector('form').submit()"
            
            delay 2
            
            -- Get results
            set resultText to do JavaScript "document.body.innerText"
        end tell
        
        return resultText
    end tell
end run
```

## Limitations & Gotchas

### Security Restrictions
1. **JavaScript from Apple Events must be enabled** in Safari Develop menu
2. **Automation permissions required** (System Settings → Privacy & Security → Automation)
3. **Sandbox restrictions** on file:// URLs in newer macOS versions
4. **Cross-origin limitations** still apply within JavaScript

### Technical Limitations
1. **No headless mode** - Safari window must exist (can be minimized)
2. **Single-threaded** - AppleScript blocks during `do JavaScript`
3. **No DevTools access** - Cannot inspect network, console programmatically
4. **No screenshot API** - Must use separate screencapture command
5. **No cookie manipulation** - No direct cookie read/write
6. **Limited error handling** - JS errors may not propagate cleanly
7. **Timing sensitivity** - Need explicit delays or polling for dynamic content
8. **Promise handling** - Async JS requires wrapper for result capture

### Performance Characteristics
- **Latency:** ~50-200ms per AppleScript command
- **JavaScript execution:** Near-native speed within page
- **Memory:** Shared with Safari process
- **Parallelism:** None (sequential only)

### Common Errors
```applescript
-- Error: "Safari got an error: Can't get document 1"
-- Cause: No document/window open

-- Error: "Execution was interrupted"
-- Cause: JavaScript error or infinite loop

-- Error: "Not authorized to send Apple events"
-- Cause: Automation permission not granted
```

---

# 2. Playwright (Python)

## Version Info
- **playwright:** 1.49.x (current stable as of 2026-02)
- **Python:** 3.8+ required, 3.11+ recommended
- **WebKit:** Playwright-patched WebKit (not Safari branded)

## Installation (Mac M4)

```bash
# Install with pip
pip install playwright

# Install browser binaries (includes WebKit for Safari-like testing)
playwright install

# Or install only WebKit
playwright install webkit

# Install with system dependencies
playwright install --with-deps webkit

# Verify installation
python -c "from playwright.sync_api import sync_playwright; print('OK')"
```

## WebKit/Safari Support on macOS ARM64

### Status: ✅ Fully Supported

```python
# WebKit works natively on Apple Silicon
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.webkit.launch()  # Native ARM64 WebKit
    page = browser.new_page()
    page.goto("https://example.com")
    browser.close()
```

### Important Notes
- Uses **Playwright's WebKit build**, NOT system Safari
- WebKit matches Safari rendering but lacks Safari-specific features
- No Safari extensions support
- No iCloud/Keychain integration
- Media codec support differs from branded Safari

## Core API Reference

### Playwright Entry Points

```python
# Sync API
from playwright.sync_api import sync_playwright, Playwright

def run(playwright: Playwright):
    browser = playwright.webkit.launch()
    # ...

with sync_playwright() as playwright:
    run(playwright)

# Async API
from playwright.async_api import async_playwright, Playwright
import asyncio

async def run(playwright: Playwright):
    browser = await playwright.webkit.launch()
    # ...

asyncio.run(main())
```

### Browser Launch

```python
browser = playwright.webkit.launch(
    headless=True,                    # bool: headless mode (default: True)
    channel=None,                     # str: browser channel (not for webkit)
    executable_path=None,             # str|Path: custom browser path
    args=[],                          # List[str]: additional browser args
    ignore_default_args=[],           # List[str]: args to exclude
    proxy={                           # Dict: proxy settings
        "server": "http://proxy:3128",
        "bypass": "*.example.com",
        "username": "user",
        "password": "pass"
    },
    downloads_path=None,              # str|Path: download directory
    slow_mo=0,                        # float: slow down operations (ms)
    timeout=30000,                    # float: launch timeout (ms)
    env={},                           # Dict: environment variables
    devtools=False,                   # bool: open devtools (chromium only)
)

# Returns: Browser instance
```

### BrowserContext

```python
context = browser.new_context(
    # Viewport
    viewport={"width": 1280, "height": 720},  # Dict|None
    no_viewport=False,                         # bool: disable viewport
    
    # Device emulation
    user_agent="...",                          # str: custom UA
    device_scale_factor=1,                     # float: device pixel ratio
    is_mobile=False,                           # bool: mobile mode
    has_touch=False,                           # bool: touch support
    
    # Locale & timezone
    locale="en-US",                            # str: locale
    timezone_id="America/Denver",              # str: timezone
    
    # Geolocation
    geolocation={"latitude": 0, "longitude": 0},  # Dict
    permissions=["geolocation"],               # List[str]
    
    # Authentication
    http_credentials={"username": "", "password": ""},  # Dict
    
    # Proxy (overrides browser-level)
    proxy={"server": "http://proxy:3128"},     # Dict
    
    # Recording
    record_video_dir="videos/",                # str|Path
    record_video_size={"width": 1280, "height": 720},
    record_har_path="trace.har",               # str|Path
    record_har_content="omit",                 # "omit"|"embed"|"attach"
    
    # Storage
    storage_state="state.json",                # str|Path|Dict
    
    # Behavior
    ignore_https_errors=False,                 # bool
    java_script_enabled=True,                  # bool
    bypass_csp=False,                          # bool
    offline=False,                             # bool
    color_scheme="light",                      # "light"|"dark"|"no-preference"
    service_workers="allow",                   # "allow"|"block"
)

# Context methods
context.add_cookies([{"name": "", "value": "", "url": ""}])
context.clear_cookies()
context.cookies(urls=None)  # List[Dict]
context.add_init_script(script="...", path=None)
context.expose_binding(name, callback, handle=False)
context.expose_function(name, callback)
context.grant_permissions(permissions, origin=None)
context.route(url, handler)
context.unroute(url, handler=None)
context.set_default_timeout(timeout)
context.set_default_navigation_timeout(timeout)
context.storage_state(path=None)  # Dict
context.close()
```

### Page Class - Core Methods

```python
page = context.new_page()

# Navigation
page.goto(url, timeout=30000, wait_until="load")
    # wait_until: "load"|"domcontentloaded"|"networkidle"|"commit"
    # Returns: Response|None
page.go_back(timeout=30000, wait_until="load")
page.go_forward(timeout=30000, wait_until="load")
page.reload(timeout=30000, wait_until="load")

# Content
page.content()  # str: full HTML
page.title()    # str: page title
page.url        # str: current URL

# Waiting
page.wait_for_load_state(state="load", timeout=30000)
    # state: "load"|"domcontentloaded"|"networkidle"
page.wait_for_url(url, timeout=30000, wait_until="load")
page.wait_for_timeout(timeout)  # ms
page.wait_for_function(expression, arg=None, timeout=30000, polling="raf")
page.wait_for_selector(selector, timeout=30000, state="visible")
    # state: "attached"|"detached"|"visible"|"hidden"

# JavaScript
page.evaluate(expression, arg=None)  # Any: result
page.evaluate_handle(expression, arg=None)  # JSHandle
page.add_init_script(script=None, path=None)
page.add_script_tag(url=None, path=None, content=None, type=None)
page.add_style_tag(url=None, path=None, content=None)

# Screenshots & PDF
page.screenshot(
    path=None,              # str|Path
    type="png",             # "png"|"jpeg"
    quality=None,           # int: jpeg quality 0-100
    full_page=False,        # bool: capture full scrollable page
    clip=None,              # Dict: {x, y, width, height}
    omit_background=False,  # bool: transparent background
    timeout=30000,
)
page.pdf(
    path=None,
    scale=1,
    display_header_footer=False,
    header_template="",
    footer_template="",
    print_background=False,
    landscape=False,
    page_ranges="",
    format="Letter",        # "Letter"|"Legal"|"Tabloid"|"A4"|etc
    width=None,
    height=None,
    margin=None,            # Dict: {top, right, bottom, left}
)

# Network
page.route(url, handler)
    # handler(route): route.fulfill(), route.continue_(), route.abort()
page.unroute(url, handler=None)
page.set_extra_http_headers(headers)

# Events
page.on("request", lambda request: ...)
page.on("response", lambda response: ...)
page.on("console", lambda msg: ...)
page.on("dialog", lambda dialog: dialog.accept())
page.on("download", lambda download: ...)
page.on("filechooser", lambda chooser: ...)
page.on("pageerror", lambda error: ...)
page.on("popup", lambda popup: ...)
page.on("load", lambda: ...)
page.on("domcontentloaded", lambda: ...)

# Frames
page.frames              # List[Frame]
page.main_frame         # Frame
page.frame(name=None, url=None)  # Frame|None

# Dialogs
page.on("dialog", lambda d: d.accept())
page.on("dialog", lambda d: d.dismiss())

# Close
page.close(run_before_unload=False)
```

### Locator Class - Element Selection

```python
# Creating locators
page.locator(selector)              # CSS or XPath
page.get_by_role(role, **kwargs)    # ARIA role
page.get_by_text(text, exact=False) # Text content
page.get_by_label(text, exact=False) # Label text
page.get_by_placeholder(text, exact=False)
page.get_by_alt_text(text, exact=False)
page.get_by_title(text, exact=False)
page.get_by_test_id(test_id)        # data-testid attribute

# Role-based selection
page.get_by_role(
    role,                   # str: "button"|"link"|"textbox"|"checkbox"|etc
    name=None,             # str|Pattern: accessible name
    exact=False,           # bool: exact match
    checked=None,          # bool: checked state
    disabled=None,         # bool: disabled state
    expanded=None,         # bool: expanded state
    include_hidden=False,  # bool: include hidden elements
    level=None,            # int: heading level
    pressed=None,          # bool: pressed state
    selected=None,         # bool: selected state
)

# Locator methods
locator.click(
    button="left",          # "left"|"right"|"middle"
    click_count=1,
    delay=0,                # ms between mousedown/mouseup
    force=False,            # skip actionability checks
    modifiers=[],           # ["Alt"|"Control"|"Meta"|"Shift"]
    position=None,          # {x, y} relative to element
    timeout=30000,
    trial=False,            # only check actionability
)
locator.dblclick(**kwargs)   # Same options as click
locator.hover(**kwargs)
locator.tap(**kwargs)        # Touch tap

locator.fill(value, force=False, timeout=30000)
locator.type(text, delay=0, timeout=30000)  # Deprecated
locator.press(key, delay=0, timeout=30000)
locator.press_sequentially(text, delay=0, timeout=30000)
locator.clear(force=False, timeout=30000)
locator.select_option(value=None, index=None, label=None)
locator.set_input_files(files, timeout=30000)

locator.check(force=False, position=None, timeout=30000)
locator.uncheck(**kwargs)
locator.set_checked(checked, **kwargs)

locator.focus(timeout=30000)
locator.blur(timeout=30000)
locator.scroll_into_view_if_needed(timeout=30000)

locator.drag_to(target, force=False, timeout=30000)

# Getting info
locator.count()                      # int
locator.all()                        # List[Locator]
locator.first                        # Locator
locator.last                         # Locator
locator.nth(index)                   # Locator

locator.inner_text(timeout=30000)    # str
locator.inner_html(timeout=30000)    # str
locator.text_content(timeout=30000)  # str|None
locator.input_value(timeout=30000)   # str
locator.get_attribute(name, timeout=30000)  # str|None
locator.bounding_box(timeout=30000)  # Dict|None

locator.is_checked(timeout=30000)    # bool
locator.is_disabled(timeout=30000)   # bool
locator.is_editable(timeout=30000)   # bool
locator.is_enabled(timeout=30000)    # bool
locator.is_hidden(timeout=30000)     # bool
locator.is_visible(timeout=30000)    # bool

locator.screenshot(path=None, timeout=30000, **kwargs)
locator.evaluate(expression, arg=None, timeout=30000)

# Filtering/chaining
locator.filter(has_text=None, has=None)
locator.and_(locator)
locator.or_(locator)
locator.locator(selector)            # Nested selector
```

### Keyboard & Mouse

```python
# Keyboard
page.keyboard.down(key)
page.keyboard.up(key)
page.keyboard.press(key, delay=0)
page.keyboard.type(text, delay=0)
page.keyboard.insert_text(text)

# Key names: "Enter", "Tab", "Escape", "ArrowDown", "F1", "a", etc.

# Mouse
page.mouse.move(x, y, steps=1)
page.mouse.down(button="left", click_count=1)
page.mouse.up(button="left", click_count=1)
page.mouse.click(x, y, button="left", click_count=1, delay=0)
page.mouse.dblclick(x, y, button="left", delay=0)
page.mouse.wheel(delta_x, delta_y)
```

### Route/Network Interception

```python
def handle_route(route):
    # Fulfill with mock response
    route.fulfill(
        status=200,
        headers={"Content-Type": "application/json"},
        body='{"data": "mocked"}',
        path=None,           # file path
        response=None,       # Response object to clone
    )
    
    # Or continue with modifications
    route.continue_(
        url=None,
        method=None,
        headers=None,
        post_data=None,
    )
    
    # Or abort
    route.abort(error_code="failed")
        # error_codes: "aborted"|"accessdenied"|"addressunreachable"|
        #              "blockedbyclient"|"blockedbyresponse"|"connectionaborted"|
        #              "connectionclosed"|"connectionfailed"|"connectionrefused"|
        #              "connectionreset"|"failed"|"timedout"

# Route by URL pattern
page.route("**/*.{png,jpg,jpeg}", lambda r: r.abort())
page.route("**/api/*", handle_route)
page.route(re.compile(r"\.css$"), lambda r: r.abort())
```

## Async Patterns for Parallel Contexts

```python
import asyncio
from playwright.async_api import async_playwright

async def scrape_page(context, url):
    """Scrape a single page in its own context/page"""
    page = await context.new_page()
    try:
        await page.goto(url)
        title = await page.title()
        return {"url": url, "title": title}
    finally:
        await page.close()

async def run_parallel():
    async with async_playwright() as p:
        browser = await p.webkit.launch()
        
        # Option 1: Multiple pages in one context
        context = await browser.new_context()
        urls = ["https://example.com", "https://example.org", "https://example.net"]
        
        tasks = [scrape_page(context, url) for url in urls]
        results = await asyncio.gather(*tasks)
        
        await context.close()
        
        # Option 2: Multiple contexts (more isolated)
        async def isolated_scrape(browser, url):
            context = await browser.new_context()
            page = await context.new_page()
            try:
                await page.goto(url)
                return await page.title()
            finally:
                await context.close()
        
        tasks = [isolated_scrape(browser, url) for url in urls]
        results = await asyncio.gather(*tasks)
        
        await browser.close()

asyncio.run(run_parallel())
```

### Semaphore for Concurrency Control

```python
import asyncio
from playwright.async_api import async_playwright

async def bounded_scrape(sem, browser, url):
    async with sem:  # Limit concurrent operations
        context = await browser.new_context()
        page = await context.new_page()
        try:
            await page.goto(url, timeout=30000)
            return await page.content()
        except Exception as e:
            return f"Error: {e}"
        finally:
            await context.close()

async def main():
    sem = asyncio.Semaphore(5)  # Max 5 concurrent contexts
    
    async with async_playwright() as p:
        browser = await p.webkit.launch()
        urls = [f"https://example.com/page/{i}" for i in range(100)]
        
        tasks = [bounded_scrape(sem, browser, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        await browser.close()
    
    return results

asyncio.run(main())
```

## Stealth/Anti-Detection: playwright-stealth

### Version: 2.0.1 (2026-01)

```bash
pip install playwright-stealth
```

### API

```python
from playwright_stealth import Stealth, ALL_EVASIONS_DISABLED_KWARGS

# Recommended: Apply to all pages automatically
from playwright.async_api import async_playwright

async def main():
    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()  # Stealth applied automatically
        # ...

# Manual application to context
stealth = Stealth(
    # Navigator evasions
    navigator_webdriver=True,           # Hide webdriver flag
    navigator_plugins=True,             # Mock plugins array
    navigator_languages_override=("en-US", "en"),  # Override languages
    navigator_platform=True,            # Normalize platform string
    navigator_vendor=True,              # Set navigator.vendor
    navigator_hardware_concurrency=True, # Mock CPU cores
    
    # WebGL evasions
    webgl_vendor=True,                  # Mock WebGL vendor
    webgl_renderer=True,                # Mock WebGL renderer
    
    # Chrome-specific
    chrome_runtime=True,                # Add chrome.runtime
    chrome_app=True,                    # Add chrome.app
    chrome_csi=True,                    # Add chrome.csi
    chrome_load_times=True,             # Add chrome.loadTimes
    
    # Other
    iframe_content_window=True,         # Fix iframe detection
    media_codecs=True,                  # Mock media capabilities
    permissions=True,                   # Mock permissions API
    
    # Mode
    init_scripts_only=False,            # Only inject init scripts
)

# Apply to context
async with async_playwright() as p:
    browser = await p.chromium.launch()
    context = await browser.new_context()
    await stealth.apply_stealth_async(context)
    page = await context.new_page()

# Sync version
stealth.apply_stealth_sync(context)

# Disable all evasions, enable specific ones
no_evasions = Stealth(**ALL_EVASIONS_DISABLED_KWARGS)
single_evasion = Stealth(
    **ALL_EVASIONS_DISABLED_KWARGS,
    navigator_webdriver=True
)
```

### Limitations of Stealth
- **Not a guarantee** - Advanced bot detection will still detect automation
- **Chromium-focused** - Most evasions target Chromium, limited WebKit support
- **Detection arms race** - Evasions may break as detection improves
- **No fingerprint randomization** - Static values, not randomized per session

## Playwright Limitations

### WebKit-Specific
1. No Safari branded browser support
2. Media codecs differ from Safari
3. No Safari extensions
4. Limited DevTools Protocol compared to Chromium
5. Some CSS features may differ from Safari

### General Limitations
1. Cannot bypass sophisticated bot detection
2. No built-in proxy rotation
3. Memory usage scales with contexts
4. Cannot access browser DevTools UI programmatically
5. Limited support for browser extensions

### Performance Characteristics
- **Context creation:** ~100-300ms
- **Page creation:** ~50-150ms
- **Navigation:** Network dependent + ~100ms overhead
- **Screenshot:** ~50-200ms depending on size
- **Memory per context:** ~50-200MB depending on content

---

# 3. Squid Cache Proxy

## Version Info
- **Squid:** 7.4 (current Homebrew stable, 2026-02)
- **Platform:** macOS ARM64 (Apple Silicon native)
- **License:** GPL-2.0-or-later

## Installation (Mac M4)

```bash
# Install via Homebrew
brew install squid

# Verify installation
squid -v

# Configuration file location
# /opt/homebrew/etc/squid.conf (Apple Silicon)
# /usr/local/etc/squid.conf (Intel)

# Service management
brew services start squid
brew services stop squid
brew services restart squid

# Manual start (foreground for debugging)
squid -N -d1

# Check configuration syntax
squid -k parse

# Reconfigure running squid
squid -k reconfigure
```

## Core Configuration Directives

### HTTP Port & Proxy Settings

```squid
# Basic HTTP proxy port
http_port 3128

# Transparent proxy (requires network config)
http_port 3129 intercept

# SSL bump port (for HTTPS interception)
http_port 3130 ssl-bump \
    cert=/opt/homebrew/etc/squid/squid.pem \
    key=/opt/homebrew/etc/squid/squid.key \
    generate-host-certificates=on \
    dynamic_cert_mem_cache_size=4MB
```

### ACL (Access Control Lists)

```squid
# ACL Syntax: acl <name> <type> <value> [<value>...]

# By source IP
acl localnet src 10.0.0.0/8
acl localnet src 172.16.0.0/12
acl localnet src 192.168.0.0/16
acl localhost src 127.0.0.1/32

# By destination domain
acl blocked_domains dstdomain .facebook.com .twitter.com
acl allowed_domains dstdomain .example.com

# By URL regex
acl images urlpath_regex -i \.(jpg|jpeg|png|gif|webp|svg|ico)$
acl stylesheets urlpath_regex -i \.css$
acl fonts urlpath_regex -i \.(woff|woff2|ttf|eot|otf)$
acl scripts urlpath_regex -i \.js$

# By MIME type (response)
acl image_mime rep_mime_type image/

# By port
acl SSL_ports port 443
acl Safe_ports port 80 443 1025-65535

# By method
acl CONNECT method CONNECT
acl GET method GET

# By time
acl business_hours time MTWHF 09:00-17:00

# By browser/user-agent
acl mobile_ua browser -i (iPhone|Android|Mobile)

# By request header
acl has_auth req_header Authorization .

# By file size (response)
acl large_files rep_header Content-Length >10485760  # >10MB
```

### Access Control (http_access)

```squid
# http_access allow|deny <acl> [<acl>...]
# Rules are processed in order, first match wins

# Basic safe access
http_access deny !Safe_ports
http_access deny CONNECT !SSL_ports

# Allow local network
http_access allow localnet
http_access allow localhost

# Block specific domains
http_access deny blocked_domains

# Deny all others (should be last)
http_access deny all
```

## Blocking Images/CSS/Fonts Configuration

### Method 1: Deny Requests (No Download)

```squid
# Define ACLs for resource types
acl images urlpath_regex -i \.(jpg|jpeg|png|gif|webp|svg|ico|bmp|tiff?)$
acl stylesheets urlpath_regex -i \.css(\?.*)?$
acl fonts urlpath_regex -i \.(woff2?|ttf|eot|otf)(\?.*)?$
acl scripts urlpath_regex -i \.js(\?.*)?$

# Block by URL pattern
http_access deny images
http_access deny stylesheets
http_access deny fonts

# Alternative: Block by MIME type (requires response, less efficient)
acl image_content rep_mime_type ^image/
acl css_content rep_mime_type text/css
acl font_content rep_mime_type ^font/
acl font_content2 rep_mime_type application/font
acl font_content3 rep_mime_type application/x-font

# Note: http_reply_access works on responses
http_reply_access deny image_content
```

### Method 2: Replace with Minimal Response

```squid
# Use deny_info to return custom error/empty response
deny_info TCP_RESET images
deny_info TCP_RESET stylesheets
deny_info TCP_RESET fonts

# Or redirect to empty content
acl images urlpath_regex -i \.(jpg|jpeg|png|gif|webp)$
deny_info 204:/dev/null images
http_access deny images
```

### Method 3: URL Rewriter (Advanced)

```squid
# External rewriter program
url_rewrite_program /opt/homebrew/etc/squid/blocker.py
url_rewrite_children 5 startup=1 idle=1 concurrency=0
url_rewrite_access deny localhost  # Don't rewrite local requests
url_rewrite_access allow all

# blocker.py example:
#!/usr/bin/env python3
import sys
import re

BLOCK_PATTERNS = [
    r'\.(jpg|jpeg|png|gif|webp|svg|ico)(\?.*)?$',
    r'\.css(\?.*)?$',
    r'\.(woff2?|ttf|eot|otf)(\?.*)?$',
]

for line in sys.stdin:
    url = line.strip().split()[0]
    if any(re.search(p, url, re.I) for p in BLOCK_PATTERNS):
        # Return 1x1 transparent pixel or empty
        print("OK status=302 url=data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7")
    else:
        print("OK")
    sys.stdout.flush()
```

### Complete Lightweight Browsing Config

```squid
# /opt/homebrew/etc/squid.conf

# Basic settings
http_port 3128
access_log daemon:/opt/homebrew/var/logs/squid/access.log squid

# Cache settings (optional, can be disabled for pure proxy)
cache_dir ufs /opt/homebrew/var/cache/squid 100 16 256
maximum_object_size 10 MB

# ACLs for blocking
acl localnet src 127.0.0.0/8
acl localnet src 10.0.0.0/8
acl localnet src 192.168.0.0/16

acl SSL_ports port 443
acl Safe_ports port 80
acl Safe_ports port 443
acl CONNECT method CONNECT

# Resource blocking ACLs
acl images urlpath_regex -i \.(jpg|jpeg|png|gif|webp|svg|ico|bmp)(\?.*)?$
acl stylesheets urlpath_regex -i \.css(\?.*)?$
acl fonts urlpath_regex -i \.(woff2?|ttf|eot|otf)(\?.*)?$

# Access rules
http_access deny !Safe_ports
http_access deny CONNECT !SSL_ports

# Block resources (comment out lines you don't want blocked)
http_access deny images
http_access deny stylesheets
http_access deny fonts

# Allow local
http_access allow localnet
http_access allow localhost
http_access deny all

# Performance tuning
workers 2
memory_cache_mode always
cache_mem 256 MB
```

## HTTPS Interception Setup

### Generate SSL Certificate

```bash
# Create directory
mkdir -p /opt/homebrew/etc/squid/ssl

# Generate CA certificate (one time)
openssl req -new -newkey rsa:2048 -days 3650 -nodes -x509 \
    -subj "/CN=Squid Proxy CA/O=Local/C=US" \
    -keyout /opt/homebrew/etc/squid/ssl/squid-ca.key \
    -out /opt/homebrew/etc/squid/ssl/squid-ca.crt

# Create PEM bundle
cat /opt/homebrew/etc/squid/ssl/squid-ca.crt \
    /opt/homebrew/etc/squid/ssl/squid-ca.key \
    > /opt/homebrew/etc/squid/ssl/squid-ca.pem

# Initialize SSL database
/opt/homebrew/opt/squid/libexec/security_file_certgen -c -s \
    /opt/homebrew/var/cache/squid/ssl_db -M 4MB

# Set permissions
chmod 700 /opt/homebrew/etc/squid/ssl
chmod 600 /opt/homebrew/etc/squid/ssl/*

# IMPORTANT: Add CA cert to system/browser trust store
# System: Keychain Access → System → Import squid-ca.crt → Trust
```

### HTTPS Bump Configuration

```squid
# SSL Bump ports
http_port 3128 ssl-bump \
    cert=/opt/homebrew/etc/squid/ssl/squid-ca.pem \
    generate-host-certificates=on \
    dynamic_cert_mem_cache_size=16MB

# SSL certificate generator
sslcrtd_program /opt/homebrew/opt/squid/libexec/security_file_certgen \
    -s /opt/homebrew/var/cache/squid/ssl_db \
    -M 16MB
sslcrtd_children 5 startup=1 idle=1

# SSL bump mode
acl step1 at_step SslBump1
acl step2 at_step SslBump2
acl step3 at_step SslBump3

# Sites to NOT bump (banking, etc.)
acl nobump dstdomain .bank.com .paypal.com

# Bump decision
ssl_bump peek step1 all
ssl_bump splice nobump
ssl_bump bump all

# or simpler: bump everything
# ssl_bump server-first all

# TLS options
tls_outgoing_options options=NO_SSLv3,NO_TLSv1,NO_TLSv1_1
```

## Integration with Playwright

### Proxy Configuration

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Browser-level proxy (all contexts)
    browser = p.chromium.launch(
        proxy={
            "server": "http://127.0.0.1:3128",
            # If using authentication:
            # "username": "user",
            # "password": "pass",
        }
    )
    
    # OR context-level proxy
    browser = p.chromium.launch()
    context = browser.new_context(
        proxy={"server": "http://127.0.0.1:3128"},
        ignore_https_errors=True,  # Required if using SSL bump with self-signed CA
    )
    
    page = context.new_page()
    page.goto("https://example.com")
    
    browser.close()
```

### Async with Squid Proxy

```python
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.webkit.launch(
            proxy={"server": "http://127.0.0.1:3128"}
        )
        context = await browser.new_context(
            ignore_https_errors=True  # For HTTPS interception
        )
        page = await context.new_page()
        
        # Resources matching Squid ACLs will be blocked
        # Only HTML and essential content loads
        await page.goto("https://example.com")
        
        await browser.close()

asyncio.run(main())
```

### Complete Example: Lightweight Scraping

```python
"""
Playwright + Squid: Block images/CSS/fonts for fast scraping
"""
import asyncio
from playwright.async_api import async_playwright

SQUID_PROXY = "http://127.0.0.1:3128"

async def lightweight_scrape(url: str) -> dict:
    async with async_playwright() as p:
        browser = await p.webkit.launch(
            proxy={"server": SQUID_PROXY}
        )
        context = await browser.new_context(
            ignore_https_errors=True,
            # Disable JS if not needed for further speedup
            # java_script_enabled=False,
        )
        
        page = await context.new_page()
        
        try:
            response = await page.goto(url, wait_until="domcontentloaded")
            
            return {
                "url": page.url,
                "status": response.status if response else None,
                "title": await page.title(),
                "text": await page.locator("body").inner_text(),
            }
        finally:
            await browser.close()

# Usage
result = asyncio.run(lightweight_scrape("https://example.com"))
print(result)
```

## Squid Limitations

1. **HTTPS interception requires CA trust** - Clients must trust proxy CA
2. **No HTTP/2 to origin** - Squid speaks HTTP/1.1 to servers
3. **Certificate pinning breaks** - Apps with pinned certs fail through bump
4. **Memory usage** - SSL contexts consume significant memory
5. **Single machine** - Not designed for distributed caching
6. **Configuration complexity** - Many interacting directives

## Performance Characteristics

- **Request latency:** ~1-5ms added per request
- **Cache HIT:** Sub-millisecond
- **SSL bump overhead:** ~20-50ms first request (cert generation)
- **Memory:** ~50-200MB base + SSL certs + cache
- **Concurrent connections:** Thousands (depends on worker config)

---

# Summary: Integration Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Mac M4 Browser Automation                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐     ┌──────────────┐     ┌──────────────────┐ │
│  │ AppleScript │     │  Playwright  │     │   Squid Proxy    │ │
│  │  + Safari   │     │   (Python)   │     │   (Homebrew)     │ │
│  └──────┬──────┘     └──────┬───────┘     └────────┬─────────┘ │
│         │                   │                      │           │
│         │                   │    ┌─────────────────┘           │
│         │                   │    │                             │
│         ▼                   ▼    ▼                             │
│  ┌──────────────┐    ┌─────────────────┐                       │
│  │    Safari    │    │     WebKit      │                       │
│  │  (Branded)   │    │  (Playwright)   │◄─────Proxy────────┐   │
│  └──────────────┘    └─────────────────┘                   │   │
│         │                   │                              │   │
│         │                   │                    ┌─────────┴─┐ │
│         ▼                   ▼                    │   Squid   │ │
│  ┌──────────────────────────────────────────┐   │  Filters: │ │
│  │              Target Website              │   │  - Images │ │
│  └──────────────────────────────────────────┘   │  - CSS    │ │
│                                                  │  - Fonts  │ │
│                                                  └───────────┘ │
└─────────────────────────────────────────────────────────────────┘

Use Cases:
- AppleScript + Safari: iCloud integration, extension support, branded Safari
- Playwright + WebKit: Headless automation, parallel contexts, CI/CD
- Squid Proxy: Bandwidth optimization, content filtering, caching
```

---

# Version Summary

| Component | Version | Install Command |
|-----------|---------|-----------------|
| AppleScript | 2.8+ | (built-in) |
| Safari | 17-18 | (built-in) |
| Playwright | 1.49.x | `pip install playwright` |
| playwright-stealth | 2.0.1 | `pip install playwright-stealth` |
| Squid | 7.4 | `brew install squid` |
| Python | 3.11+ | `brew install python@3.11` |

---

*Manifest generated following SOURCE_MANIFEST methodology: Actual API enumeration with signatures, version numbers, and working code examples.*
