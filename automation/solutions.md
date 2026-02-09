# MHI Automation System - Comprehensive Solutions Guide

> **Purpose**: Anticipate and solve every potential issue before it becomes a problem.
> **Last Updated**: 2026-02-08

---

## Table of Contents
1. [Security Hardening](#1-security-hardening)
2. [Reliability Improvements](#2-reliability-improvements)
3. [Monitoring & Alerting](#3-monitoring--alerting)
4. [Scalability Solutions](#4-scalability-solutions)
5. [Maintenance Reduction](#5-maintenance-reduction)
6. [Fallback Strategies](#6-fallback-strategies)
7. [Compliance Solutions](#7-compliance-solutions)
8. [Implementation Priority Matrix](#8-implementation-priority-matrix)

---

## 1. Security Hardening

### Problem: Plaintext Credentials in JSON
**Current State**: `.credentials.json` stores passwords in plaintext.

**Solution A: Windows Credential Manager (Recommended for Windows)**
```python
import keyring

class SecureCredentialStore:
    """Use OS-level credential storage"""
    SERVICE_NAME = "MHI_Automation"
    
    def store_credential(self, portal: str, username: str, password: str):
        keyring.set_password(self.SERVICE_NAME, f"{portal}_user", username)
        keyring.set_password(self.SERVICE_NAME, f"{portal}_pass", password)
    
    def get_credential(self, portal: str) -> tuple:
        username = keyring.get_password(self.SERVICE_NAME, f"{portal}_user")
        password = keyring.get_password(self.SERVICE_NAME, f"{portal}_pass")
        return username, password
    
    def delete_credential(self, portal: str):
        keyring.delete_password(self.SERVICE_NAME, f"{portal}_user")
        keyring.delete_password(self.SERVICE_NAME, f"{portal}_pass")
```

**Solution B: Encrypted JSON with User-Provided Master Password**
```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class EncryptedCredentialStore:
    def __init__(self, master_password: str, salt_file: Path = Path(".salt")):
        # Load or generate salt
        if salt_file.exists():
            salt = salt_file.read_bytes()
        else:
            salt = os.urandom(16)
            salt_file.write_bytes(salt)
        
        # Derive key from master password
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        self.cipher = Fernet(key)
    
    def encrypt(self, plaintext: str) -> str:
        return self.cipher.encrypt(plaintext.encode()).decode()
    
    def decrypt(self, ciphertext: str) -> str:
        return self.cipher.decrypt(ciphertext.encode()).decode()
```

**Solution C: HashiCorp Vault Integration (Enterprise-Grade)**
```python
import hvac

class VaultCredentialStore:
    def __init__(self, vault_addr: str, token: str):
        self.client = hvac.Client(url=vault_addr, token=token)
    
    def store_credential(self, portal: str, username: str, password: str):
        self.client.secrets.kv.v2.create_or_update_secret(
            path=f"mhi/portals/{portal}",
            secret={"username": username, "password": password}
        )
    
    def get_credential(self, portal: str) -> dict:
        secret = self.client.secrets.kv.v2.read_secret_version(
            path=f"mhi/portals/{portal}"
        )
        return secret['data']['data']
```

### Problem: Browser State Contains Sensitive Sessions
**Current State**: `browser-state/` directory has active cookies and session tokens.

**Solutions**:

1. **Filesystem Encryption**: Use Windows EFS or BitLocker on the automation directory
   ```powershell
   # Enable EFS on folder
   cipher /e /s:C:\Users\user\.openclaw\workspace\automation\browser-state
   ```

2. **Session Isolation**: Create separate browser profiles per portal risk level
   ```python
   BROWSER_STATE_DIRS = {
       "low_risk": BASE_DIR / "browser-state-low",    # Public portals
       "medium_risk": BASE_DIR / "browser-state-med",  # Supplier portals
       "high_risk": BASE_DIR / "browser-state-high",   # Financial, govcon
   }
   ```

3. **Auto-Logout on Exit**: Force logout when closing sessions
   ```python
   async def stop(self, logout_all=True):
       if logout_all:
           for portal in self.active_sessions:
               await self.logout(portal)
       await self.context.close()
   ```

4. **Session Timeout Enforcement**:
   ```python
   SESSION_MAX_AGE = timedelta(hours=8)
   
   def check_session_freshness(self, portal: str) -> bool:
       session_file = BROWSER_STATE_DIR / "session_times.json"
       times = json.load(open(session_file)) if session_file.exists() else {}
       last_used = datetime.fromisoformat(times.get(portal, "1970-01-01"))
       return datetime.now() - last_used < SESSION_MAX_AGE
   ```

### Problem: API Key Rotation
**Solution**: Implement key rotation tracking and reminders

```python
class APIKeyManager:
    KEY_FILE = BASE_DIR / ".api_keys.json"
    ROTATION_DAYS = 90
    
    def add_key(self, service: str, key: str, created: datetime = None):
        keys = self._load_keys()
        keys[service] = {
            "key": self.encrypt(key),  # Use encryption from above
            "created": (created or datetime.now()).isoformat(),
            "expires_warning": (datetime.now() + timedelta(days=self.ROTATION_DAYS - 14)).isoformat()
        }
        self._save_keys(keys)
    
    def check_expiring_keys(self) -> List[str]:
        """Return list of keys needing rotation soon"""
        keys = self._load_keys()
        expiring = []
        for service, info in keys.items():
            created = datetime.fromisoformat(info["created"])
            if datetime.now() - created > timedelta(days=self.ROTATION_DAYS - 14):
                expiring.append(service)
        return expiring
    
    def rotate_key(self, service: str, new_key: str):
        """Rotate key with audit trail"""
        keys = self._load_keys()
        old_created = keys.get(service, {}).get("created")
        
        # Archive old key info (not the key itself)
        self.log_rotation(service, old_created, datetime.now())
        
        # Store new key
        self.add_key(service, new_key)
```

---

## 2. Reliability Improvements

### Problem: Portal UI Changes Break Selectors
**Solution: Multi-Strategy Selector System with Self-Healing**

```python
class ResilientSelector:
    """Try multiple selector strategies, learn which work"""
    
    def __init__(self, page, selector_db: Path = BASE_DIR / "selector_cache.json"):
        self.page = page
        self.selector_db = selector_db
        self.cache = self._load_cache()
    
    async def find_element(self, intent: str, portal: str, hints: List[str] = None) -> ElementHandle:
        """
        Find element by intent (e.g., 'username_field', 'submit_button')
        Uses cached selectors first, falls back to discovery
        """
        # 1. Try cached selector
        cached = self.cache.get(portal, {}).get(intent)
        if cached:
            elem = await self.page.query_selector(cached)
            if elem:
                return elem
        
        # 2. Try common patterns
        patterns = SELECTOR_PATTERNS.get(intent, [])
        for sel in patterns:
            elem = await self.page.query_selector(sel)
            if elem:
                self._cache_selector(portal, intent, sel)
                return elem
        
        # 3. Try AI-based discovery (use aria labels, text content)
        elem = await self._discover_by_context(intent, hints)
        if elem:
            discovered_sel = await self._extract_best_selector(elem)
            self._cache_selector(portal, intent, discovered_sel)
            return elem
        
        return None
    
    async def _discover_by_context(self, intent: str, hints: List[str]) -> ElementHandle:
        """Use page context to find elements"""
        # Intent-based discovery
        discovery_strategies = {
            "username_field": [
                "input[type='email']",
                "input[type='text']:near(:text('email'))",
                "input[type='text']:near(:text('user'))",
                "input:near(label:text-matches('email|user', 'i'))",
            ],
            "password_field": [
                "input[type='password']",
                "input:near(label:text-matches('password', 'i'))",
            ],
            "submit_button": [
                "button[type='submit']",
                "input[type='submit']",
                "button:has-text('Log in')",
                "button:has-text('Sign in')",
                "button:has-text('Submit')",
                "*[role='button']:has-text('Log')",
            ],
        }
        
        for sel in discovery_strategies.get(intent, []):
            try:
                elem = await self.page.query_selector(sel)
                if elem:
                    return elem
            except:
                pass
        return None

# Selector patterns by intent
SELECTOR_PATTERNS = {
    "username_field": [
        'input[name="username"]', 'input[name="email"]', 'input[name="user"]',
        'input[name="userId"]', 'input[name="login"]', 'input[name="identifier"]',
        'input[type="email"]', 'input[id*="user" i]', 'input[id*="email" i]',
        'input[autocomplete="username"]', 'input[autocomplete="email"]',
        '#username', '#email', '#user', '#login',
    ],
    "password_field": [
        'input[type="password"]', 'input[name="password"]', 'input[name="pass"]',
        'input[autocomplete="current-password"]', '#password',
    ],
    "submit_button": [
        'button[type="submit"]', 'input[type="submit"]',
        'button:has-text("Log in")', 'button:has-text("Login")',
        'button:has-text("Sign in")', 'button:has-text("Submit")',
        'button:has-text("Continue")', 'button[class*="login" i]',
        '*[class*="submit" i]', 'button[data-testid*="login"]',
    ],
    "company_name": [
        'input[name="company"]', 'input[name="companyName"]',
        'input[name*="company" i]', 'input[id*="company" i]',
        'input[name="organization"]', 'input[name="business"]',
        'input:near(label:text-matches("company|business|organization", "i"))',
    ],
}
```

### Problem: Login Failures
**Solution: Robust Retry with Exponential Backoff**

```python
class RetryableLogin:
    MAX_RETRIES = 3
    BASE_DELAY = 2  # seconds
    
    async def login_with_retry(self, portal: str, username: str, password: str) -> LoginResult:
        last_error = None
        
        for attempt in range(self.MAX_RETRIES):
            try:
                # Exponential backoff
                if attempt > 0:
                    delay = self.BASE_DELAY * (2 ** attempt) + random.uniform(0, 1)
                    self.log(f"Retry {attempt + 1}/{self.MAX_RETRIES} in {delay:.1f}s...")
                    await asyncio.sleep(delay)
                
                # Clear any stale state
                await self.page.reload()
                await asyncio.sleep(1)
                
                # Attempt login
                result = await self._do_login(portal, username, password)
                
                if result.success:
                    return result
                
                # Analyze failure
                if result.error_type == "invalid_credentials":
                    # Don't retry bad credentials
                    return result
                elif result.error_type == "captcha":
                    # Signal for human intervention
                    return LoginResult(
                        success=False, 
                        error_type="captcha_required",
                        message="CAPTCHA detected - manual intervention needed"
                    )
                elif result.error_type == "rate_limited":
                    # Wait longer
                    await asyncio.sleep(60)
                    
            except PlaywrightTimeoutError as e:
                last_error = e
                self.log(f"Timeout on attempt {attempt + 1}")
            except Exception as e:
                last_error = e
                self.log(f"Error on attempt {attempt + 1}: {e}")
        
        return LoginResult(
            success=False,
            error_type="max_retries_exceeded",
            message=f"Failed after {self.MAX_RETRIES} attempts: {last_error}"
        )
    
    async def _do_login(self, portal: str, username: str, password: str) -> LoginResult:
        """Actual login logic with error detection"""
        cred = self.get_credential(portal)
        url = cred.get("url")
        
        await self.page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(2)
        
        # Check for immediate issues
        page_text = await self.page.evaluate("() => document.body.innerText")
        
        if any(x in page_text.lower() for x in ["rate limit", "too many requests", "try again later"]):
            return LoginResult(success=False, error_type="rate_limited")
        
        if any(x in page_text.lower() for x in ["captcha", "verify you're human", "robot check"]):
            return LoginResult(success=False, error_type="captcha")
        
        # ... fill credentials and submit ...
        
        # Check result
        await asyncio.sleep(3)
        new_text = await self.page.evaluate("() => document.body.innerText")
        
        if any(x in new_text.lower() for x in ["invalid", "incorrect", "wrong password", "failed"]):
            return LoginResult(success=False, error_type="invalid_credentials")
        
        if await self._check_login_success():
            return LoginResult(success=True)
        
        return LoginResult(success=False, error_type="unknown")

@dataclass
class LoginResult:
    success: bool
    error_type: str = None
    message: str = None
    session_valid_until: datetime = None
```

### Problem: CAPTCHA Blocking
**Solutions (in order of preference)**:

1. **Prevention First**: Reduce CAPTCHA triggers
   ```python
   class AntiDetectionBrowser:
       """Configure browser to minimize automation detection"""
       
       STEALTH_ARGS = [
           "--disable-blink-features=AutomationControlled",
           "--no-sandbox",
           "--disable-web-security",
           "--disable-features=IsolateOrigins,site-per-process",
       ]
       
       async def start_stealth(self):
           self.context = await self.playwright.chromium.launch_persistent_context(
               user_data_dir=str(BROWSER_STATE_DIR),
               headless=False,  # Headless more likely to trigger
               args=self.STEALTH_ARGS,
               ignore_default_args=["--enable-automation"],
               
               # Realistic fingerprint
               viewport={"width": 1920, "height": 1080},
               user_agent=self._get_realistic_ua(),
               locale="en-US",
               timezone_id="America/Denver",
               geolocation={"latitude": 42.0, "longitude": -104.8},  # Wyoming
               permissions=["geolocation"],
               
               # Human-like behavior
               has_touch=False,
               java_script_enabled=True,
               accept_downloads=True,
           )
           
           # Inject stealth scripts
           await self._inject_stealth_scripts()
       
       async def _inject_stealth_scripts(self):
           """Override automation detection properties"""
           await self.page.add_init_script("""
               // Override webdriver property
               Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
               
               // Override plugins (headless usually has none)
               Object.defineProperty(navigator, 'plugins', {
                   get: () => [1, 2, 3, 4, 5]
               });
               
               // Override languages
               Object.defineProperty(navigator, 'languages', {
                   get: () => ['en-US', 'en']
               });
               
               // Chrome object
               window.chrome = { runtime: {} };
               
               // Permissions
               const originalQuery = window.navigator.permissions.query;
               window.navigator.permissions.query = (parameters) => (
                   parameters.name === 'notifications' ?
                       Promise.resolve({ state: Notification.permission }) :
                       originalQuery(parameters)
               );
           """)
       
       def _get_realistic_ua(self) -> str:
           """Rotate between recent, common user agents"""
           agents = [
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
           ]
           return random.choice(agents)
   ```

2. **Human-like Interactions**:
   ```python
   async def human_type(self, selector: str, text: str):
       """Type like a human with variable delays"""
       elem = await self.page.query_selector(selector)
       await elem.click()
       await asyncio.sleep(random.uniform(0.1, 0.3))
       
       for char in text:
           await self.page.keyboard.type(char)
           # Variable delay between keystrokes (50-150ms)
           await asyncio.sleep(random.uniform(0.05, 0.15))
   
   async def human_move_and_click(self, selector: str):
       """Move mouse naturally before clicking"""
       elem = await self.page.query_selector(selector)
       box = await elem.bounding_box()
       
       # Get current mouse position (or center of viewport)
       current_x, current_y = 960, 540
       target_x = box['x'] + box['width'] / 2 + random.uniform(-5, 5)
       target_y = box['y'] + box['height'] / 2 + random.uniform(-5, 5)
       
       # Bezier curve movement (more human-like than linear)
       steps = random.randint(20, 40)
       for i in range(steps):
           t = i / steps
           # Simple ease-out
           progress = 1 - (1 - t) ** 2
           x = current_x + (target_x - current_x) * progress
           y = current_y + (target_y - current_y) * progress
           await self.page.mouse.move(x, y)
           await asyncio.sleep(random.uniform(0.01, 0.03))
       
       await asyncio.sleep(random.uniform(0.1, 0.2))
       await self.page.mouse.click(target_x, target_y)
   ```

3. **CAPTCHA Service Integration** (for high-value portals):
   ```python
   class CaptchaSolver:
       """Integration with CAPTCHA solving services"""
       
       def __init__(self, api_key: str, service: str = "2captcha"):
           self.api_key = api_key
           self.service = service
       
       async def solve_recaptcha(self, site_key: str, page_url: str) -> str:
           """Use 2captcha or similar service"""
           if self.service == "2captcha":
               # Submit
               submit_url = (
                   f"http://2captcha.com/in.php?"
                   f"key={self.api_key}&method=userrecaptcha"
                   f"&googlekey={site_key}&pageurl={page_url}"
               )
               async with aiohttp.ClientSession() as session:
                   async with session.get(submit_url) as resp:
                       text = await resp.text()
                       if not text.startswith("OK|"):
                           raise CaptchaError(f"Submit failed: {text}")
                       captcha_id = text.split("|")[1]
               
               # Poll for result
               for _ in range(60):  # Wait up to 2 minutes
                   await asyncio.sleep(2)
                   result_url = f"http://2captcha.com/res.php?key={self.api_key}&action=get&id={captcha_id}"
                   async with aiohttp.ClientSession() as session:
                       async with session.get(result_url) as resp:
                           text = await resp.text()
                           if text == "CAPCHA_NOT_READY":
                               continue
                           if text.startswith("OK|"):
                               return text.split("|")[1]
                           raise CaptchaError(f"Solve failed: {text}")
               
               raise CaptchaError("Timeout waiting for solution")
       
       async def inject_solution(self, page, token: str):
           """Inject solved token into page"""
           await page.evaluate(f"""
               document.getElementById('g-recaptcha-response').innerHTML = '{token}';
           """)
   ```

4. **Human Fallback Queue**:
   ```python
   class CaptchaQueue:
       """Queue CAPTCHAs for human solving"""
       QUEUE_FILE = BASE_DIR / "captcha_queue.json"
       
       def queue_captcha(self, portal: str, screenshot_path: Path, callback_data: dict):
           """Add CAPTCHA to human queue"""
           queue = self._load_queue()
           queue.append({
               "id": str(uuid.uuid4()),
               "portal": portal,
               "screenshot": str(screenshot_path),
               "callback": callback_data,
               "queued_at": datetime.now().isoformat(),
               "status": "pending"
           })
           self._save_queue(queue)
           
           # Notify (telegram, email, etc.)
           self.notify_human(f"CAPTCHA needed for {portal}")
       
       def notify_human(self, message: str):
           """Send notification"""
           # Integration with OpenClaw notification system
           pass
   ```

---

## 3. Monitoring & Alerting

### Problem: Detecting Broken Logins Automatically

**Solution: Health Check System**

```python
class PortalHealthMonitor:
    """Continuous monitoring of portal login health"""
    
    HEALTH_FILE = BASE_DIR / "portal_health.json"
    
    async def check_portal(self, portal: str) -> HealthStatus:
        """Check if login still works"""
        auto = MHIAutomator()
        await auto.start(headless=True)
        
        try:
            result = await auto.login_with_retry(portal)
            
            status = HealthStatus(
                portal=portal,
                checked_at=datetime.now(),
                login_success=result.success,
                error_type=result.error_type,
                response_time_ms=result.response_time,
            )
            
            # Check for post-login indicators
            if result.success:
                status.session_valid = await auto._verify_session_active()
                status.can_navigate = await auto._check_navigation()
            
        except Exception as e:
            status = HealthStatus(
                portal=portal,
                checked_at=datetime.now(),
                login_success=False,
                error_type="exception",
                error_message=str(e)
            )
        finally:
            await auto.stop()
        
        self._save_health(status)
        return status
    
    async def run_all_checks(self) -> List[HealthStatus]:
        """Check all portals and alert on failures"""
        results = []
        for portal in self.get_all_portals():
            status = await self.check_portal(portal)
            results.append(status)
            
            if not status.login_success:
                await self.send_alert(status)
            
            # Rate limit between checks
            await asyncio.sleep(30)
        
        return results
    
    async def send_alert(self, status: HealthStatus):
        """Send alert via configured channels"""
        message = f"""
⚠️ Portal Login Failed: {status.portal}
Error: {status.error_type}
Details: {status.error_message or 'N/A'}
Time: {status.checked_at.strftime('%Y-%m-%d %H:%M')}

Action required: Check credentials or UI changes.
        """
        
        # Send via available channels
        if TELEGRAM_BOT_TOKEN:
            await self._telegram_alert(message)
        if ALERT_EMAIL:
            await self._email_alert(message)
        if SLACK_WEBHOOK:
            await self._slack_alert(message)
    
    def get_health_dashboard(self) -> dict:
        """Generate health summary"""
        health = self._load_all_health()
        return {
            "total_portals": len(health),
            "healthy": sum(1 for h in health.values() if h["login_success"]),
            "failing": [p for p, h in health.items() if not h["login_success"]],
            "last_check": max(h["checked_at"] for h in health.values()) if health else None,
            "average_response_ms": statistics.mean(
                h["response_time_ms"] for h in health.values() if h.get("response_time_ms")
            ) if health else 0
        }

@dataclass
class HealthStatus:
    portal: str
    checked_at: datetime
    login_success: bool
    error_type: str = None
    error_message: str = None
    response_time_ms: float = None
    session_valid: bool = None
    can_navigate: bool = None
```

### Problem: Session Expiry Detection

```python
class SessionMonitor:
    """Detect and handle session expiration"""
    
    SESSION_FILE = BASE_DIR / "session_state.json"
    
    async def check_session_valid(self, portal: str) -> bool:
        """Verify session is still active"""
        # Try to access a protected page
        cred = self.get_credential(portal)
        check_url = cred.get("session_check_url") or cred.get("url")
        
        await self.page.goto(check_url, wait_until="domcontentloaded")
        await asyncio.sleep(2)
        
        # Check for login redirect or session expired indicators
        current_url = self.page.url
        page_text = await self.page.evaluate("() => document.body.innerText.toLowerCase()")
        
        session_expired_indicators = [
            "login" in current_url.lower() and "dashboard" not in current_url.lower(),
            "session expired" in page_text,
            "please log in" in page_text,
            "session timeout" in page_text,
            "sign in" in page_text and self._is_login_page(),
        ]
        
        return not any(session_expired_indicators)
    
    async def refresh_session_if_needed(self, portal: str) -> bool:
        """Refresh session if expired"""
        if await self.check_session_valid(portal):
            self._update_session_time(portal)
            return True
        
        # Session expired, re-login
        self.log(f"Session expired for {portal}, re-authenticating...")
        result = await self.login_with_retry(portal)
        
        if result.success:
            self._update_session_time(portal)
            return True
        
        return False
    
    def _update_session_time(self, portal: str):
        """Track session refresh times"""
        sessions = self._load_sessions()
        sessions[portal] = {
            "last_verified": datetime.now().isoformat(),
            "refresh_count": sessions.get(portal, {}).get("refresh_count", 0) + 1
        }
        self._save_sessions(sessions)
```

### Problem: Failed Form Submission Alerts

```python
class FormSubmissionMonitor:
    """Track and alert on form submission issues"""
    
    async def submit_with_verification(self, form_name: str, submit_selector: str) -> SubmitResult:
        """Submit form and verify success"""
        # Capture state before submit
        before_url = self.page.url
        before_text = await self.page.evaluate("() => document.body.innerText")
        
        # Submit
        await self.page.click(submit_selector)
        await asyncio.sleep(3)
        
        # Analyze result
        after_url = self.page.url
        after_text = await self.page.evaluate("() => document.body.innerText.toLowerCase()")
        
        # Check for success indicators
        success_indicators = [
            "thank you" in after_text,
            "submitted" in after_text,
            "success" in after_text,
            "confirmation" in after_text,
            "received" in after_text,
            after_url != before_url and "confirm" in after_url.lower(),
        ]
        
        # Check for error indicators
        error_indicators = [
            "error" in after_text,
            "failed" in after_text,
            "invalid" in after_text,
            "required field" in after_text,
            "please correct" in after_text,
        ]
        
        if any(success_indicators) and not any(error_indicators):
            return SubmitResult(success=True, form=form_name)
        
        # Capture details for debugging
        screenshot = await self.screenshot(f"submit_failed_{form_name}")
        
        result = SubmitResult(
            success=False,
            form=form_name,
            error_text=self._extract_errors(after_text),
            screenshot=screenshot
        )
        
        await self.alert_form_failure(result)
        return result
    
    def _extract_errors(self, page_text: str) -> List[str]:
        """Extract error messages from page"""
        # Look for common error patterns
        error_patterns = [
            r"error:?\s*(.+?)(?:\.|$)",
            r"please\s+(.+?)(?:\.|$)",
            r"invalid\s+(.+?)(?:\.|$)",
            r"required:?\s*(.+?)(?:\.|$)",
        ]
        
        errors = []
        for pattern in error_patterns:
            matches = re.findall(pattern, page_text, re.IGNORECASE)
            errors.extend(matches)
        
        return errors[:5]  # Limit to top 5
```

---

## 4. Scalability Solutions

### Problem: JSON vs Database for Account Inventory

**Current State**: JSON files work for small scale but become problematic.

**Solution: SQLite with JSON Fallback**

```python
from sqlalchemy import create_engine, Column, String, DateTime, JSON
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class PortalCredential(Base):
    __tablename__ = "credentials"
    
    id = Column(String, primary_key=True)
    portal = Column(String, index=True)
    entity = Column(String, index=True)
    username = Column(String)
    password_encrypted = Column(String)
    url = Column(String)
    extra_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime)
    status = Column(String, default="active")

class Entity(Base):
    __tablename__ = "entities"
    
    id = Column(String, primary_key=True)
    name = Column(String)
    legal_name = Column(String)
    entity_type = Column(String)
    address = Column(JSON)
    contacts = Column(JSON)
    certifications = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_log"
    
    id = Column(String, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    action = Column(String, index=True)  # login, signup, form_fill, etc.
    portal = Column(String, index=True)
    entity = Column(String, index=True)
    success = Column(String)
    details = Column(JSON)
    error = Column(String)

class DatabaseManager:
    def __init__(self, db_path: Path = BASE_DIR / "mhi_automation.db"):
        self.engine = create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def migrate_from_json(self):
        """One-time migration from JSON files"""
        # Migrate credentials
        creds_file = BASE_DIR / ".credentials.json"
        if creds_file.exists():
            creds = json.load(open(creds_file))
            for portal, data in creds.get("portals", {}).items():
                self.session.merge(PortalCredential(
                    id=f"{data.get('entity', 'mhi')}_{portal}",
                    portal=portal,
                    entity=data.get("entity", "mhi"),
                    username=data.get("username"),
                    password_encrypted=self.encrypt(data.get("password", "")),
                    url=data.get("url"),
                    extra_data={"notes": data.get("notes")},
                    updated_at=datetime.fromisoformat(data.get("updated", datetime.now().isoformat()))
                ))
        
        # Migrate entities
        profiles_file = BASE_DIR / "entity-profiles.json"
        if profiles_file.exists():
            profiles = json.load(open(profiles_file))
            for entity_id, data in profiles.get("entities", {}).items():
                self.session.merge(Entity(
                    id=entity_id,
                    name=data.get("dba") or data.get("legal_name"),
                    legal_name=data.get("legal_name"),
                    entity_type=data.get("entity_type"),
                    address=data.get("address"),
                    contacts=data.get("contacts"),
                    certifications=data.get("certifications", [])
                ))
        
        self.session.commit()
    
    def log_action(self, action: str, portal: str, entity: str, success: bool, details: dict = None, error: str = None):
        """Log all automation actions"""
        self.session.add(AuditLog(
            id=str(uuid.uuid4()),
            action=action,
            portal=portal,
            entity=entity,
            success="yes" if success else "no",
            details=details,
            error=error
        ))
        self.session.commit()
```

### Problem: Agent Orchestration

**Solution: Task Queue with Priorities**

```python
import asyncio
from dataclasses import dataclass, field
from typing import Callable, Any
from enum import Enum
import heapq

class Priority(Enum):
    CRITICAL = 1  # Expiring certifications, urgent logins
    HIGH = 2      # New signups, time-sensitive
    NORMAL = 3    # Regular form fills
    LOW = 4       # Health checks, cleanup

@dataclass(order=True)
class AutomationTask:
    priority: int
    task_id: str = field(compare=False)
    task_type: str = field(compare=False)
    portal: str = field(compare=False)
    entity: str = field(compare=False)
    params: dict = field(compare=False, default_factory=dict)
    created_at: datetime = field(compare=False, default_factory=datetime.now)
    scheduled_for: datetime = field(compare=False, default=None)

class TaskOrchestrator:
    def __init__(self, max_concurrent: int = 3):
        self.queue = []  # Priority queue
        self.running = {}  # Currently executing tasks
        self.max_concurrent = max_concurrent
        self.results = {}
        self.lock = asyncio.Lock()
    
    async def add_task(self, task: AutomationTask):
        """Add task to queue"""
        async with self.lock:
            heapq.heappush(self.queue, task)
    
    async def run_worker(self):
        """Process tasks from queue"""
        while True:
            async with self.lock:
                if not self.queue or len(self.running) >= self.max_concurrent:
                    await asyncio.sleep(1)
                    continue
                
                # Get highest priority task
                task = heapq.heappop(self.queue)
                
                # Check if scheduled for later
                if task.scheduled_for and task.scheduled_for > datetime.now():
                    heapq.heappush(self.queue, task)
                    await asyncio.sleep(1)
                    continue
                
                self.running[task.task_id] = task
            
            # Execute task
            try:
                result = await self._execute_task(task)
                self.results[task.task_id] = {"status": "completed", "result": result}
            except Exception as e:
                self.results[task.task_id] = {"status": "failed", "error": str(e)}
                # Retry logic
                if task.params.get("retries", 0) < 3:
                    task.params["retries"] = task.params.get("retries", 0) + 1
                    task.scheduled_for = datetime.now() + timedelta(minutes=5)
                    await self.add_task(task)
            finally:
                async with self.lock:
                    del self.running[task.task_id]
    
    async def _execute_task(self, task: AutomationTask):
        """Execute a single task"""
        auto = MHIAutomator()
        await auto.start(headless=True)
        
        try:
            if task.task_type == "login":
                return await auto.login(task.portal)
            elif task.task_type == "signup":
                return await auto.signup(task.portal, task.entity)
            elif task.task_type == "health_check":
                return await auto.check_session_valid(task.portal)
            elif task.task_type == "form_fill":
                await auto.goto(task.params.get("url"))
                return await auto.fill_form_with_entity(task.entity)
        finally:
            await auto.stop()
    
    def get_status(self) -> dict:
        """Get orchestrator status"""
        return {
            "queued": len(self.queue),
            "running": len(self.running),
            "completed": sum(1 for r in self.results.values() if r["status"] == "completed"),
            "failed": sum(1 for r in self.results.values() if r["status"] == "failed"),
        }
```

### Problem: Resource Management for Parallel Agents

```python
class BrowserPool:
    """Manage pool of browser instances"""
    
    def __init__(self, max_browsers: int = 3):
        self.max_browsers = max_browsers
        self.available = asyncio.Queue()
        self.all_contexts = []
        self.playwright = None
    
    async def initialize(self):
        """Pre-warm browser pool"""
        self.playwright = await async_playwright().start()
        
        for i in range(self.max_browsers):
            context = await self._create_context(f"browser-pool-{i}")
            self.all_contexts.append(context)
            await self.available.put(context)
    
    async def _create_context(self, state_dir: str) -> BrowserContext:
        """Create a new browser context"""
        state_path = BASE_DIR / "browser-pools" / state_dir
        state_path.mkdir(parents=True, exist_ok=True)
        
        return await self.playwright.chromium.launch_persistent_context(
            user_data_dir=str(state_path),
            headless=True,
            viewport={"width": 1920, "height": 1080},
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"],
            ignore_default_args=["--enable-automation"],
        )
    
    async def acquire(self, timeout: float = 30) -> BrowserContext:
        """Get a browser from pool"""
        try:
            return await asyncio.wait_for(self.available.get(), timeout=timeout)
        except asyncio.TimeoutError:
            raise ResourceExhausted("No browsers available")
    
    async def release(self, context: BrowserContext):
        """Return browser to pool"""
        # Clear pages except main
        pages = context.pages
        for page in pages[1:]:
            await page.close()
        
        await self.available.put(context)
    
    async def shutdown(self):
        """Clean shutdown of all browsers"""
        for context in self.all_contexts:
            await context.close()
        await self.playwright.stop()
```

---

## 5. Maintenance Reduction

### Problem: Generic Selectors That Survive UI Changes

**Solution: Semantic Selector Library**

```python
class SemanticSelectors:
    """Use semantic, role-based selectors instead of fragile CSS"""
    
    @staticmethod
    def get_form_field(field_type: str, label_text: str = None) -> List[str]:
        """
        Generate resilient selectors for form fields.
        Returns list of selectors to try in order.
        """
        selectors = []
        
        if field_type == "text":
            # Role-based (most resilient)
            selectors.append(f'[role="textbox"]')
            if label_text:
                selectors.append(f'input:near(:text("{label_text}"))')
                selectors.append(f'label:has-text("{label_text}") input')
            # Semantic HTML
            selectors.append('input[type="text"]')
            
        elif field_type == "email":
            selectors.extend([
                'input[type="email"]',
                'input[autocomplete="email"]',
                'input:near(:text("email"))',
            ])
            
        elif field_type == "password":
            selectors.extend([
                'input[type="password"]',
                'input[autocomplete="current-password"]',
                'input[autocomplete="new-password"]',
            ])
            
        elif field_type == "submit":
            selectors.extend([
                'button[type="submit"]',
                'input[type="submit"]',
                '[role="button"]:has-text("Submit")',
                '[role="button"]:has-text("Log in")',
                '[role="button"]:has-text("Sign in")',
                'button:visible:has-text("Submit")',
            ])
            
        elif field_type == "dropdown":
            selectors.extend([
                f'select:near(:text("{label_text}"))' if label_text else 'select',
                '[role="listbox"]',
                '[role="combobox"]',
            ])
        
        return selectors
    
    @staticmethod
    def get_navigation(nav_type: str) -> List[str]:
        """Get navigation selectors"""
        patterns = {
            "logout": [
                '[role="button"]:has-text("Log out")',
                '[role="menuitem"]:has-text("Log out")',
                'a:has-text("Logout")',
                'a:has-text("Sign out")',
                '[aria-label*="logout" i]',
            ],
            "dashboard": [
                'a:has-text("Dashboard")',
                '[role="link"]:has-text("Home")',
                '[aria-label*="dashboard" i]',
            ],
            "account": [
                'a:has-text("Account")',
                'a:has-text("Profile")',
                '[role="menuitem"]:has-text("Account")',
            ],
        }
        return patterns.get(nav_type, [])
```

### Problem: Self-Documenting Portal Handlers

**Solution: Decorator-Based Registration with Metadata**

```python
from functools import wraps
from typing import Dict, List, Optional

# Registry for all portal handlers
PORTAL_REGISTRY: Dict[str, dict] = {}

def portal_handler(
    name: str,
    url: str,
    entity: str = "mhi",
    requires: List[str] = None,
    notes: str = None,
    last_verified: str = None,
):
    """
    Decorator to register and document portal handlers.
    
    Example:
        @portal_handler(
            name="ingram_micro",
            url="https://usa.ingrammicro.com/cep/app/login",
            entity="mhi",
            requires=["username", "password"],
            notes="Uses SSO, may need 2FA",
            last_verified="2024-01-15"
        )
        async def login_ingram_micro(self):
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            return await func(self, *args, **kwargs)
        
        # Register handler
        PORTAL_REGISTRY[name] = {
            "name": name,
            "url": url,
            "entity": entity,
            "requires": requires or ["username", "password"],
            "notes": notes,
            "last_verified": last_verified,
            "handler": func.__name__,
            "module": func.__module__,
        }
        
        return wrapper
    return decorator


def generate_portal_docs() -> str:
    """Generate markdown documentation from registry"""
    doc = "# Portal Handler Documentation\n\n"
    doc += f"*Auto-generated on {datetime.now().strftime('%Y-%m-%d')}*\n\n"
    
    # Group by entity
    by_entity = {}
    for name, info in PORTAL_REGISTRY.items():
        entity = info["entity"]
        by_entity.setdefault(entity, []).append(info)
    
    for entity, portals in by_entity.items():
        doc += f"## {entity.upper()}\n\n"
        
        for portal in portals:
            doc += f"### {portal['name']}\n"
            doc += f"- **URL**: {portal['url']}\n"
            doc += f"- **Requires**: {', '.join(portal['requires'])}\n"
            if portal['notes']:
                doc += f"- **Notes**: {portal['notes']}\n"
            if portal['last_verified']:
                doc += f"- **Last Verified**: {portal['last_verified']}\n"
            doc += "\n"
    
    return doc


# Example usage in automator
class DocumentedAutomator(MHIAutomator):
    
    @portal_handler(
        name="ingram_micro",
        url="https://usa.ingrammicro.com/cep/app/login",
        entity="mhi",
        requires=["username", "password"],
        notes="iMConnect portal. May redirect to SSO. Session lasts ~8 hours.",
        last_verified="2024-01-15"
    )
    async def login_ingram_micro(self):
        cred = self.get_credential("ingram_micro")
        await self.page.goto("https://usa.ingrammicro.com/cep/app/login")
        # ... login logic ...
    
    @portal_handler(
        name="td_synnex",
        url="https://ec.synnex.com/ecx/login.html",
        entity="mhi",
        requires=["username", "password"],
        notes="ECexpress portal. Classic HTML form.",
        last_verified="2024-01-15"
    )
    async def login_td_synnex(self):
        # ... login logic ...
        pass
```

### Problem: Automated Testing for Login Flows

**Solution: pytest-Based Login Tests**

```python
# tests/test_logins.py
import pytest
import asyncio
from automation.mhi_automator import MHIAutomator

class TestLoginFlows:
    """Automated tests for all login flows"""
    
    @pytest.fixture
    def automator(self):
        auto = MHIAutomator()
        yield auto
    
    @pytest.fixture
    async def browser(self, automator):
        await automator.start(headless=True)
        yield automator
        await automator.stop()
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("portal", [
        "ingram_micro",
        "td_synnex",
        "dh",
    ])
    async def test_login_flow(self, browser, portal):
        """Test that login completes without errors"""
        # Skip if no credentials
        cred = browser.get_credential(portal)
        if not cred.get("username"):
            pytest.skip(f"No credentials for {portal}")
        
        result = await browser.login(portal)
        
        assert result.success or result.error_type == "captcha_required", \
            f"Login failed: {result.error_type} - {result.message}"
    
    @pytest.mark.asyncio
    async def test_form_detection(self, browser):
        """Test that form field detection works"""
        # Use a known test form
        await browser.goto("https://httpbin.org/forms/post")
        
        fields = await browser.detect_form_fields()
        
        assert len(fields) > 0
        assert any("custname" in f.lower() for f in fields)
    
    @pytest.mark.asyncio
    async def test_entity_data_loads(self, browser):
        """Test entity data is complete"""
        data = browser.get_entity_data("mhi")
        
        assert data.get("company")
        assert data.get("address")
        assert data.get("city")
        assert data.get("email")
    
    @pytest.mark.asyncio
    async def test_selector_fallback(self, browser):
        """Test selector fallback mechanism"""
        # Navigate to a real login page
        await browser.goto("https://github.com/login")
        
        # Should find username field using fallback selectors
        found = await browser.fill_field_smart("username", "test@test.com")
        
        # GitHub might have different field names, but our smart fill should adapt
        # This tests the resilience of the selector system


# Run tests
# pytest tests/test_logins.py -v --tb=short
```

---

## 6. Fallback Strategies

### Problem: Playwright Fails → Selenium Fallback

**Solution: Dual-Engine Automator**

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DualEngineAutomator:
    """Fallback between Playwright and Selenium"""
    
    def __init__(self):
        self.primary_engine = "playwright"
        self.playwright_auto = None
        self.selenium_driver = None
    
    async def start(self, headless=False):
        """Start with primary engine, prepare fallback"""
        try:
            self.playwright_auto = MHIAutomator()
            await self.playwright_auto.start(headless=headless)
            self.active_engine = "playwright"
        except Exception as e:
            print(f"Playwright failed: {e}, falling back to Selenium")
            self._start_selenium(headless)
            self.active_engine = "selenium"
    
    def _start_selenium(self, headless=False):
        """Initialize Selenium as fallback"""
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        
        # Anti-detection
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Use existing profile
        user_data = str(BASE_DIR / "browser-state-selenium")
        options.add_argument(f"--user-data-dir={user_data}")
        
        self.selenium_driver = webdriver.Chrome(options=options)
        
        # Execute CDP command to hide webdriver
        self.selenium_driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"}
        )
    
    async def login(self, portal: str, username: str = None, password: str = None):
        """Login using active engine"""
        if self.active_engine == "playwright":
            try:
                return await self.playwright_auto.login(portal, username, password)
            except Exception as e:
                print(f"Playwright login failed: {e}, trying Selenium")
                if not self.selenium_driver:
                    self._start_selenium()
                return self._selenium_login(portal, username, password)
        else:
            return self._selenium_login(portal, username, password)
    
    def _selenium_login(self, portal: str, username: str = None, password: str = None):
        """Selenium-based login"""
        cred = self.get_credential(portal)
        username = username or cred.get("username")
        password = password or cred.get("password")
        url = cred.get("url")
        
        self.selenium_driver.get(url)
        time.sleep(2)
        
        # Find and fill username
        username_selectors = [
            (By.NAME, "username"), (By.NAME, "email"), (By.NAME, "user"),
            (By.ID, "username"), (By.ID, "email"),
            (By.CSS_SELECTOR, "input[type='email']"),
        ]
        
        for by, value in username_selectors:
            try:
                elem = WebDriverWait(self.selenium_driver, 2).until(
                    EC.presence_of_element_located((by, value))
                )
                elem.clear()
                elem.send_keys(username)
                break
            except:
                continue
        
        # Similar for password and submit...
        
        return True
    
    async def stop(self):
        if self.playwright_auto:
            await self.playwright_auto.stop()
        if self.selenium_driver:
            self.selenium_driver.quit()
```

### Problem: Automation Blocked → Manual Workflow

**Solution: Graceful Degradation with Manual Queue**

```python
class ManualWorkflowQueue:
    """Queue tasks for manual completion when automation fails"""
    
    QUEUE_FILE = BASE_DIR / "manual_queue.json"
    
    def queue_for_manual(self, task: AutomationTask, reason: str, instructions: str = None):
        """Add task to manual queue with context"""
        queue = self._load_queue()
        
        manual_item = {
            "id": task.task_id,
            "task_type": task.task_type,
            "portal": task.portal,
            "entity": task.entity,
            "reason": reason,
            "instructions": instructions or self._generate_instructions(task),
            "queued_at": datetime.now().isoformat(),
            "status": "pending",
            "attempted_automation": True,
            "screenshots": self._get_related_screenshots(task),
        }
        
        queue.append(manual_item)
        self._save_queue(queue)
        
        # Notify
        self.send_notification(
            title=f"Manual Action Required: {task.portal}",
            body=f"""
Automation failed for: {task.task_type} on {task.portal}
Reason: {reason}

Instructions:
{instructions or 'See manual_queue.json for details'}

Entity: {task.entity}
            """
        )
    
    def _generate_instructions(self, task: AutomationTask) -> str:
        """Generate human-readable instructions"""
        templates = {
            "login": f"""
1. Open browser and go to: {task.params.get('url', 'N/A')}
2. Log in with credentials for: {task.portal}
3. Verify login successful (dashboard visible)
4. Mark task complete in manual_queue.json
            """,
            "signup": f"""
1. Open browser and go to signup page
2. Fill form with {task.entity.upper()} entity data
3. Complete any CAPTCHAs
4. Submit and verify confirmation
5. Save any account numbers/credentials
            """,
            "form_fill": f"""
1. Navigate to: {task.params.get('url', 'N/A')}
2. Fill form using {task.entity.upper()} data from entity-profiles.json
3. Review all fields before submission
4. Screenshot confirmation
            """,
        }
        return templates.get(task.task_type, "Complete the task manually")
    
    def get_pending_tasks(self) -> List[dict]:
        """Get all pending manual tasks"""
        queue = self._load_queue()
        return [t for t in queue if t["status"] == "pending"]
    
    def mark_complete(self, task_id: str, notes: str = None):
        """Mark manual task as complete"""
        queue = self._load_queue()
        for task in queue:
            if task["id"] == task_id:
                task["status"] = "completed"
                task["completed_at"] = datetime.now().isoformat()
                task["completion_notes"] = notes
                break
        self._save_queue(queue)
    
    def generate_todo_list(self) -> str:
        """Generate human-readable TODO list"""
        pending = self.get_pending_tasks()
        if not pending:
            return "No pending manual tasks ✓"
        
        output = "# Manual Tasks TODO\n\n"
        for task in pending:
            output += f"""
## {task['portal']} - {task['task_type']}
- **Queued**: {task['queued_at']}
- **Reason**: {task['reason']}
- **Entity**: {task['entity']}

{task['instructions']}

---
"""
        return output
```

### Problem: Data Backup Strategies

**Solution: Multi-Layer Backup System**

```python
class BackupManager:
    """Automated backup of critical automation data"""
    
    BACKUP_DIR = BASE_DIR / "backups"
    CRITICAL_FILES = [
        ".credentials.json",
        "entity-profiles.json",
        "signup-templates.json",
        "mhi_automation.db",
        "selector_cache.json",
    ]
    
    def __init__(self):
        self.BACKUP_DIR.mkdir(exist_ok=True)
    
    def create_backup(self, reason: str = "scheduled") -> Path:
        """Create timestamped backup"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}_{reason}"
        backup_path = self.BACKUP_DIR / backup_name
        backup_path.mkdir()
        
        # Copy critical files
        for file in self.CRITICAL_FILES:
            src = BASE_DIR / file
            if src.exists():
                dst = backup_path / file
                if src.is_file():
                    shutil.copy2(src, dst)
                else:
                    shutil.copytree(src, dst)
        
        # Create backup metadata
        metadata = {
            "created_at": datetime.now().isoformat(),
            "reason": reason,
            "files": [f for f in self.CRITICAL_FILES if (BASE_DIR / f).exists()],
            "size_bytes": sum(
                f.stat().st_size for f in backup_path.rglob("*") if f.is_file()
            ),
        }
        
        with open(backup_path / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        
        # Create compressed archive
        archive = shutil.make_archive(str(backup_path), "zip", backup_path)
        shutil.rmtree(backup_path)  # Remove uncompressed version
        
        self._cleanup_old_backups()
        
        return Path(archive)
    
    def _cleanup_old_backups(self, keep_count: int = 10):
        """Remove old backups, keep most recent"""
        backups = sorted(self.BACKUP_DIR.glob("backup_*.zip"), reverse=True)
        for old_backup in backups[keep_count:]:
            old_backup.unlink()
    
    def restore_backup(self, backup_file: Path, dry_run: bool = True):
        """Restore from backup"""
        import zipfile
        
        if dry_run:
            print("DRY RUN - Would restore the following files:")
            with zipfile.ZipFile(backup_file) as zf:
                for name in zf.namelist():
                    print(f"  {name}")
            return
        
        # Create restore point first
        self.create_backup(reason="pre_restore")
        
        # Extract backup
        with zipfile.ZipFile(backup_file) as zf:
            for name in zf.namelist():
                if name == "metadata.json":
                    continue
                zf.extract(name, BASE_DIR)
        
        print(f"Restored from: {backup_file}")
    
    def schedule_backup(self, interval_hours: int = 24):
        """Schedule periodic backups"""
        async def backup_loop():
            while True:
                self.create_backup(reason="scheduled")
                await asyncio.sleep(interval_hours * 3600)
        
        asyncio.create_task(backup_loop())
    
    def backup_to_cloud(self, backup_path: Path, provider: str = "onedrive"):
        """Upload backup to cloud storage"""
        if provider == "onedrive":
            # Use OneDrive API or simply copy to synced folder
            onedrive_path = Path.home() / "OneDrive" / "Backups" / "MHI_Automation"
            onedrive_path.mkdir(parents=True, exist_ok=True)
            shutil.copy2(backup_path, onedrive_path / backup_path.name)
        elif provider == "google_drive":
            # Use Google Drive API
            pass
```

---

## 7. Compliance Solutions

### Problem: Secure Credential Handling Patterns

**Solution: Defense in Depth**

```python
class SecureCredentialPipeline:
    """
    Secure credential handling following best practices:
    1. Never log credentials
    2. Encrypt at rest
    3. Minimize time in memory
    4. Audit all access
    """
    
    def __init__(self, db: DatabaseManager, audit: AuditLogger):
        self.db = db
        self.audit = audit
        self._decrypted_cache = {}  # Short-lived cache
        self._cache_timeout = 60  # seconds
    
    def get_credential(self, portal: str, purpose: str) -> SecureString:
        """
        Get credential with full audit trail.
        Returns SecureString that auto-clears.
        """
        # Log access attempt
        self.audit.log_access(
            resource=f"credential:{portal}",
            purpose=purpose,
            accessor=self._get_caller_info()
        )
        
        # Check cache
        if portal in self._decrypted_cache:
            cached = self._decrypted_cache[portal]
            if datetime.now() - cached["time"] < timedelta(seconds=self._cache_timeout):
                return cached["cred"]
        
        # Fetch and decrypt
        encrypted = self.db.get_credential_encrypted(portal)
        if not encrypted:
            raise CredentialNotFound(portal)
        
        decrypted = self._decrypt(encrypted)
        secure_cred = SecureString(decrypted)
        
        # Cache briefly
        self._decrypted_cache[portal] = {
            "cred": secure_cred,
            "time": datetime.now()
        }
        
        # Schedule cache clear
        asyncio.get_event_loop().call_later(
            self._cache_timeout,
            lambda: self._clear_cache_entry(portal)
        )
        
        return secure_cred
    
    def _clear_cache_entry(self, portal: str):
        if portal in self._decrypted_cache:
            self._decrypted_cache[portal]["cred"].clear()
            del self._decrypted_cache[portal]


class SecureString:
    """String that can be securely cleared from memory"""
    
    def __init__(self, value: str):
        self._value = bytearray(value.encode())
        self._cleared = False
    
    def get(self) -> str:
        if self._cleared:
            raise ValueError("SecureString has been cleared")
        return self._value.decode()
    
    def clear(self):
        """Overwrite memory before releasing"""
        for i in range(len(self._value)):
            self._value[i] = 0
        self._cleared = True
    
    def __del__(self):
        self.clear()
    
    def __str__(self):
        return "[REDACTED]"
    
    def __repr__(self):
        return "SecureString([REDACTED])"
```

### Problem: Audit Logging for Automated Actions

**Solution: Comprehensive Audit Trail**

```python
class AuditLogger:
    """
    Complete audit logging for compliance.
    Logs: Who, What, When, Where, Why, Outcome
    """
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.session_id = str(uuid.uuid4())
        self.start_time = datetime.now()
    
    def log_action(
        self,
        action: str,
        portal: str = None,
        entity: str = None,
        success: bool = None,
        details: dict = None,
        sensitive_fields: List[str] = None,
    ):
        """Log automation action with sanitization"""
        
        # Sanitize sensitive data
        sanitized_details = self._sanitize(details, sensitive_fields or [])
        
        entry = {
            "id": str(uuid.uuid4()),
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "portal": portal,
            "entity": entity,
            "success": success,
            "details": sanitized_details,
            "machine": socket.gethostname(),
            "user": os.getenv("USERNAME") or os.getenv("USER"),
        }
        
        self.db.insert_audit_log(entry)
        
        # Also log to file for redundancy
        self._log_to_file(entry)
    
    def _sanitize(self, data: dict, sensitive_fields: List[str]) -> dict:
        """Remove or mask sensitive data"""
        if not data:
            return data
        
        sanitized = {}
        for key, value in data.items():
            if key.lower() in ["password", "secret", "token", "api_key"]:
                sanitized[key] = "[REDACTED]"
            elif key in sensitive_fields:
                sanitized[key] = "[REDACTED]"
            elif isinstance(value, dict):
                sanitized[key] = self._sanitize(value, sensitive_fields)
            else:
                sanitized[key] = value
        
        return sanitized
    
    def _log_to_file(self, entry: dict):
        """Append to audit log file"""
        log_file = BASE_DIR / "logs" / f"audit_{datetime.now().strftime('%Y%m')}.jsonl"
        log_file.parent.mkdir(exist_ok=True)
        
        with open(log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
    
    def generate_audit_report(
        self,
        start_date: datetime,
        end_date: datetime,
        portal: str = None,
        entity: str = None,
    ) -> dict:
        """Generate audit report for compliance review"""
        logs = self.db.query_audit_logs(
            start_date=start_date,
            end_date=end_date,
            portal=portal,
            entity=entity,
        )
        
        return {
            "report_generated": datetime.now().isoformat(),
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
            },
            "summary": {
                "total_actions": len(logs),
                "successful": sum(1 for l in logs if l["success"]),
                "failed": sum(1 for l in logs if not l["success"]),
                "by_portal": self._group_by(logs, "portal"),
                "by_entity": self._group_by(logs, "entity"),
                "by_action": self._group_by(logs, "action"),
            },
            "details": logs,
        }
```

### Problem: Data Retention Policies

**Solution: Automated Data Lifecycle Management**

```python
class DataRetentionManager:
    """
    Manage data lifecycle per retention policies.
    
    Default policies:
    - Audit logs: 7 years (legal requirement)
    - Session data: 30 days
    - Screenshots: 90 days
    - Backups: 1 year
    """
    
    RETENTION_POLICIES = {
        "audit_logs": timedelta(days=7 * 365),
        "session_data": timedelta(days=30),
        "screenshots": timedelta(days=90),
        "backups": timedelta(days=365),
        "temp_files": timedelta(days=1),
    }
    
    def __init__(self, db: DatabaseManager, audit: AuditLogger):
        self.db = db
        self.audit = audit
    
    def apply_retention_policies(self, dry_run: bool = True):
        """Apply all retention policies"""
        results = {
            "audit_logs": self._clean_audit_logs(dry_run),
            "screenshots": self._clean_screenshots(dry_run),
            "backups": self._clean_backups(dry_run),
            "browser_state": self._clean_browser_state(dry_run),
        }
        
        if not dry_run:
            self.audit.log_action(
                action="data_retention_cleanup",
                details=results
            )
        
        return results
    
    def _clean_screenshots(self, dry_run: bool) -> dict:
        """Clean old screenshots"""
        cutoff = datetime.now() - self.RETENTION_POLICIES["screenshots"]
        to_delete = []
        
        for screenshot in SCREENSHOTS_DIR.glob("*.png"):
            mtime = datetime.fromtimestamp(screenshot.stat().st_mtime)
            if mtime < cutoff:
                to_delete.append(screenshot)
        
        if not dry_run:
            for f in to_delete:
                f.unlink()
        
        return {
            "policy": "90 days",
            "found": len(to_delete),
            "deleted": 0 if dry_run else len(to_delete)
        }
    
    def _clean_browser_state(self, dry_run: bool) -> dict:
        """Clean old session cookies (while preserving active ones)"""
        # Be careful here - only clean obviously stale data
        cutoff = datetime.now() - self.RETENTION_POLICIES["session_data"]
        
        # Check session validity before cleaning
        stale_sessions = []
        session_file = BROWSER_STATE_DIR / "session_times.json"
        
        if session_file.exists():
            sessions = json.load(open(session_file))
            for portal, last_used in sessions.items():
                if datetime.fromisoformat(last_used) < cutoff:
                    stale_sessions.append(portal)
        
        return {
            "policy": "30 days",
            "stale_sessions": stale_sessions,
            "note": "Manual review recommended before cleanup"
        }
    
    def export_for_legal(
        self,
        entity: str,
        start_date: datetime,
        end_date: datetime,
        output_path: Path,
    ):
        """Export data for legal/compliance requests"""
        # Gather all relevant data
        export_data = {
            "export_date": datetime.now().isoformat(),
            "entity": entity,
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
            },
            "audit_logs": self.db.query_audit_logs(
                start_date=start_date,
                end_date=end_date,
                entity=entity,
            ),
            "entity_profile": self._get_entity_profile(entity),
        }
        
        # Create encrypted export
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w") as f:
            json.dump(export_data, f, indent=2, default=str)
        
        self.audit.log_action(
            action="legal_data_export",
            entity=entity,
            details={
                "output_path": str(output_path),
                "record_count": len(export_data["audit_logs"]),
            }
        )
        
        return output_path
```

---

## 8. Implementation Priority Matrix

### Critical (Do First)
| Issue | Solution | Effort | Impact |
|-------|----------|--------|--------|
| Plaintext credentials | Windows Credential Manager | Low | High |
| Login failure recovery | Retry with backoff | Low | High |
| No monitoring | Health check system | Medium | High |

### High Priority
| Issue | Solution | Effort | Impact |
|-------|----------|--------|--------|
| Audit logging | AuditLogger class | Medium | High |
| Selector brittleness | ResilientSelector | Medium | High |
| Backup strategy | BackupManager | Low | Medium |

### Medium Priority
| Issue | Solution | Effort | Impact |
|-------|----------|--------|--------|
| Database migration | SQLite + SQLAlchemy | Medium | Medium |
| CAPTCHA handling | Prevention + service integration | High | Medium |
| Task orchestration | TaskOrchestrator | High | Medium |

### Lower Priority (Nice to Have)
| Issue | Solution | Effort | Impact |
|-------|----------|--------|--------|
| Selenium fallback | DualEngineAutomator | High | Low |
| Vault integration | HashiCorp Vault | High | Low |
| Browser pool | BrowserPool | Medium | Low |

---

## Quick Reference: Common Responses to Critics

| Criticism | Response |
|-----------|----------|
| "Credentials stored insecurely" | Use Windows Credential Manager (keyring library) - zero code in files |
| "What if portal changes?" | Multi-strategy selectors with caching + automatic fallback |
| "Automation will get blocked" | Human-like behavior, stealth mode, CAPTCHA queue for manual fallback |
| "No audit trail" | Every action logged with timestamp, entity, portal, outcome |
| "Data loss risk" | Automated backups (local + cloud) with retention policies |
| "Single point of failure" | Playwright → Selenium fallback, automation → manual queue |
| "Can't scale" | SQLite database, task queue, browser pool for parallelism |
| "Compliance concerns" | Full audit logs, data retention, secure credential handling |
| "Hard to maintain" | Self-documenting handlers, automated tests, semantic selectors |
| "Session expires" | Automatic detection and re-authentication |

---

## Files to Create

Based on this document, the following files should be added to the automation system:

1. `secure_credentials.py` - Credential encryption and storage
2. `resilient_selectors.py` - Self-healing selector system
3. `health_monitor.py` - Portal health checking
4. `task_orchestrator.py` - Task queue and scheduling
5. `audit_logger.py` - Compliance audit logging
6. `backup_manager.py` - Automated backups
7. `database.py` - SQLite models and migrations
8. `tests/test_logins.py` - Automated login testing

---

*This document should be reviewed and updated quarterly or whenever significant changes occur.*
