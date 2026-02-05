# Headless Browser Infrastructure Setup

**Date:** 2026-02-04  
**Agent:** neteng (subagent)  
**Status:** ✅ Operational

---

## Summary

Two headless browser options are now available for agent use:

1. **Playwright + Chromium** (standalone, recommended) — fully working
2. **OpenClaw managed browser** (Brave via CDP) — config added, requires gateway restart

---

## A. OpenClaw Managed Browser Configuration

### What was done
Added `browser.profiles.openclaw.headless = true` to `openclaw.json`:

```json
"browser": {
  "profiles": {
    "openclaw": {
      "headless": true
    }
  }
}
```

### Current state
- Brave is installed at: `C:\Users\user\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe`
- CDP endpoint: `http://127.0.0.1:18801` (when running)
- User data: `C:\Users\user\.openclaw\browser\openclaw\user-data`
- **Note:** The managed Brave browser was not running at test time (CDP unreachable). The gateway may need a restart to pick up the headless config. The `openclaw` CLI is not in the agent's PATH, so the gateway must be restarted by the user or the main agent.

### To apply
```
openclaw gateway restart
```

### Agents with browser tool access
These agents have `browser` in their `alsoAllow` list:
- `seeker` (Argus)
- `sitecraft` (Mason)
- `climbibm` (Channel Partner)
- `analyst` (Strategist)

---

## B. Playwright (Standalone Headless Chromium)

### Installation
| Component | Version | Location |
|-----------|---------|----------|
| Playwright | latest (npm) | Global + local in `workspace/bin` and `agents/neteng` |
| Chromium Headless Shell | 145.0.7632.6 | `%LOCALAPPDATA%\ms-playwright\chromium_headless_shell-1208` |
| Node.js | v24.11.1 | System PATH |

### Test results
All tests passed:
- ✅ Launch headless Chromium
- ✅ Navigate to `example.com` — title: "Example Domain"
- ✅ Extract page content (H1 text, full body text)
- ✅ Take screenshots (PNG, 10KB)
- ✅ Navigate to `httpbin.org/headers` — parsed JSON response
- ✅ User-Agent: `HeadlessChrome/145.0.7632.6`

### Browse utility
A reusable utility is available at:
```
C:\Users\user\.openclaw\workspace\bin\browse.mjs
```

**Usage:**
```bash
# Print page title + URL
node browse.mjs https://example.com

# Full text content
node browse.mjs https://example.com --text

# Screenshot
node browse.mjs https://example.com --screenshot output.png

# Wait for dynamic content (ms)
node browse.mjs https://spa-app.com --text --wait 3000
```

### Using Playwright in agent scripts
```javascript
import { chromium } from 'playwright';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
await page.goto('https://example.com');
const title = await page.title();
const text = await page.locator('body').innerText();
await page.screenshot({ path: 'screenshot.png' });
await browser.close();
```

**Important:** The script directory needs a `package.json` with `"type": "module"` and `playwright` as a dependency. Directories already set up:
- `C:\Users\user\.openclaw\workspace\bin\` 
- `C:\Users\user\.openclaw\agents\neteng\`

### Connecting to existing CDP browser
If the OpenClaw managed browser is running:
```javascript
import { chromium } from 'playwright';
const browser = await chromium.connectOverCDP('http://127.0.0.1:18801');
// Use browser as normal...
```

Test script: `C:\Users\user\.openclaw\agents\neteng\cdp-connect-test.mjs`

---

## C. Test Results Summary

| Test | Result | Notes |
|------|--------|-------|
| Playwright launch headless | ✅ Pass | Chromium 145 |
| Page navigation | ✅ Pass | example.com, httpbin.org |
| Text extraction | ✅ Pass | Title, H1, full body |
| Screenshots | ✅ Pass | PNG output |
| browse.mjs utility | ✅ Pass | CLI tool for any agent |
| CDP connect (port 18801) | ❌ Fail | Managed browser not running |
| OpenClaw headless config | ⚠️ Pending | Config added, needs gateway restart |

---

## D. Recommendations

1. **Use Playwright for most agent tasks** — it's self-contained, doesn't depend on the gateway browser lifecycle, and works reliably
2. **Restart the gateway** to activate headless mode for the managed Brave browser (for agents that use the built-in `browser` tool)
3. **Add `browser` to more agents' `alsoAllow`** if they need web automation beyond `web_fetch`
4. **Consider adding playwright to `neteng`'s tool profile** for CDP-based automation tasks

---

## Files Created

| File | Purpose |
|------|---------|
| `workspace/bin/browse.mjs` | Reusable headless browse utility |
| `workspace/bin/package.json` | Node.js project config (ESM) |
| `agents/neteng/playwright-test.mjs` | Full Playwright test script |
| `agents/neteng/cdp-connect-test.mjs` | CDP connection test script |
| `agents/neteng/playwright-test-screenshot.png` | Test screenshot output |
| `workspace/docs/headless-browser-setup.md` | This document |
