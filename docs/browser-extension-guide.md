# OpenClaw Browser Extension Guide

## Overview

The OpenClaw Browser Relay extension allows Claude to interact with your browser tabs through the Chrome DevTools Protocol (CDP). This enables web automation, page inspection, and content extraction.

## Installation

1. Open Chrome and navigate to `chrome://extensions`
2. Enable "Developer mode" (toggle in top-right)
3. Click "Load unpacked" and select the extension directory
4. The OpenClaw icon should appear in your toolbar

## Usage

### Attaching a Tab

1. Navigate to the page you want Claude to access
2. Click the OpenClaw toolbar icon
3. The badge should show **ON** when attached
4. Claude can now interact with that tab

### Basic Commands

Once attached, ask Claude to:
- "Take a snapshot of this page"
- "Click the login button"
- "Fill in the search field"
- "Navigate to [URL]"

## Known Limitations

### Cross-Origin Navigation Disconnects

**Issue:** When you navigate to a different domain (cross-origin), Chrome silently disconnects the debugger session. The extension badge may still show "ON" but the connection is stale.

**Example:**
1. Attach tab on `example.com` ✅
2. Click link to `google.com` ❌ Connection lost
3. Badge still shows ON but commands fail

**Workaround:** Re-attach the tab after cross-origin navigation by clicking the toolbar icon again.

**Technical Details:**
- Chrome's Debugger API disconnects on cross-origin navigations as a security measure
- The extension uses `webNavigation` listeners to detect this, but reconnection requires user action
- Same-origin navigations (staying within the same domain) work fine

### Recommended Patterns

1. **Single-domain sessions:** Keep automation within one domain when possible
2. **Re-attach after jumps:** Click the toolbar icon after navigating to a new domain
3. **Use `navigate` action:** Instead of clicking links, ask Claude to use the navigate action directly - this maintains control better

### Multiple Tabs

- Only one tab can be attached at a time per profile
- Switching tabs requires re-attaching
- The `chrome` profile is for your existing Chrome; `openclaw` profile is for isolated browser

## Troubleshooting

### "Connection lost" errors

1. Check if you navigated to a different domain
2. Click the toolbar icon to re-attach
3. Verify badge shows ON

### Tab not responding

1. Refresh the page
2. Re-attach via toolbar icon
3. Try a different tab

### Badge shows ON but commands fail

This is the stale connection issue. Re-attach the tab.

## Profiles

| Profile | Description |
|---------|-------------|
| `chrome` | Your existing Chrome browser (requires extension) |
| `openclaw` | Isolated browser managed by OpenClaw |

When using the extension relay, always use `profile="chrome"`.

---

*Last updated: 2026-02-03*
