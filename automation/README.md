# MHI Web Automator

Reliable web automation for portal logins, supplier signups, and form filling.

## Setup

```powershell
pip install selenium webdriver-manager
```

## Usage

### Interactive Mode
```powershell
python automation/web-automator.py
```

### Command Line
```powershell
# Login to a saved portal
python automation/web-automator.py login ingram_micro

# Fill supplier application form (navigate to form first)
python automation/web-automator.py fill https://example.com/apply
```

## Adding Credentials

1. Run interactive mode
2. Choose "2. Add/update credentials"
3. Enter portal name, URL, username, password

Credentials are stored in `.credentials.json` (gitignored, never committed).

## Entity Profiles

Edit `entity-profiles.json` to add:
- EIN/Tax ID
- DUNS number  
- CAGE code
- Phone numbers
- Additional contacts

## Supported Portals

Pre-configured handlers exist for:
- Ingram Micro (iMConnect)
- TD SYNNEX (ECexpress)
- D&H Distributing

Add more in the `SupplierPortals` class.

## How It Works

1. Connects to Chrome via remote debugging port (9222)
2. Uses your existing Chrome profile with all saved sessions
3. Auto-fills forms using entity profile data
4. Handles common login patterns automatically

## Security

- Credentials stored locally only (`.credentials.json`)
- Never committed to git
- Uses your existing browser sessions
- No passwords sent to external services

## For OpenClaw/Peridot

I can use this system to:
- Log into portals on your behalf
- Fill out supplier applications
- Sign up for new platforms
- Manage authorized seller applications

Just tell me what portal and which entity (MHI, DSAIC, or Computer Store).
