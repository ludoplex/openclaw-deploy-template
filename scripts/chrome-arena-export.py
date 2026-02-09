#!/usr/bin/env python3
"""
Arena.ai (formerly lmarena.ai) Session Exporter
Reads Chrome cookies and fetches all conversations via Supabase API
"""
import os
import sys
import json
import sqlite3
import shutil
import base64
from pathlib import Path
from datetime import datetime

try:
    import httpx
except ImportError:
    print("Installing httpx...")
    os.system(f"{sys.executable} -m pip install httpx")
    import httpx

# Windows Chrome paths
CHROME_USER_DATA = Path(os.environ.get('LOCALAPPDATA', '')) / 'Google' / 'Chrome' / 'User Data'
CHROME_DEFAULT_COOKIES = CHROME_USER_DATA / 'Default' / 'Network' / 'Cookies'
CHROME_LOCAL_STATE = CHROME_USER_DATA / 'Local State'

def get_chrome_key():
    """Get the Chrome encryption key (Windows)"""
    try:
        import win32crypt
        from Cryptodome.Cipher import AES
        
        with open(CHROME_LOCAL_STATE, 'r', encoding='utf-8') as f:
            local_state = json.load(f)
        
        encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
        encrypted_key = encrypted_key[5:]  # Remove 'DPAPI' prefix
        return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    except Exception as e:
        print(f"Warning: Could not get Chrome key: {e}")
        return None

def decrypt_cookie(encrypted_value, key):
    """Decrypt a Chrome cookie value"""
    try:
        from Cryptodome.Cipher import AES
        
        if encrypted_value[:3] == b'v10' or encrypted_value[:3] == b'v11':
            nonce = encrypted_value[3:15]
            ciphertext = encrypted_value[15:-16]
            tag = encrypted_value[-16:]
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')
    except Exception as e:
        pass
    return None

def get_arena_cookies():
    """Extract arena.ai cookies from Chrome"""
    cookies = {}
    
    # Copy cookies DB (Chrome locks it)
    temp_db = Path('temp_cookies.db')
    try:
        shutil.copy2(CHROME_DEFAULT_COOKIES, temp_db)
    except Exception as e:
        print(f"Error copying cookies: {e}")
        print("Make sure Chrome is closed or try running as admin")
        return None
    
    try:
        key = get_chrome_key()
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # Get arena.ai cookies
        cursor.execute("""
            SELECT name, encrypted_value, host_key, path 
            FROM cookies 
            WHERE host_key LIKE '%arena.ai%' OR host_key LIKE '%lmarena.ai%'
        """)
        
        for name, encrypted_value, host, path in cursor.fetchall():
            if key:
                value = decrypt_cookie(encrypted_value, key)
                if value:
                    cookies[name] = value
                    print(f"  Found cookie: {name} ({len(value)} chars)")
        
        conn.close()
    finally:
        temp_db.unlink(missing_ok=True)
    
    return cookies

def get_supabase_session(cookies):
    """Extract Supabase session from cookies"""
    # Common Supabase auth cookie patterns
    session_cookies = {k: v for k, v in cookies.items() 
                       if 'sb-' in k or 'supabase' in k or 'auth' in k.lower()}
    return session_cookies

def fetch_conversations(access_token, refresh_token=None):
    """Fetch all conversations from Arena.ai"""
    # Arena uses Supabase - need to discover the project URL
    # Common pattern: sb-{project-ref}-auth-token
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'apikey': access_token,  # Supabase also uses this
    }
    
    # Try common Arena/Supabase endpoints
    endpoints_to_try = [
        'https://auth.arena.ai/rest/v1/conversations',
        'https://auth.arena.ai/rest/v1/chats',
        'https://api.arena.ai/v1/conversations',
        'https://arena.ai/api/conversations',
        'https://arena.ai/api/chats',
    ]
    
    conversations = []
    
    with httpx.Client(timeout=30) as client:
        for endpoint in endpoints_to_try:
            try:
                print(f"Trying: {endpoint}")
                resp = client.get(endpoint, headers=headers)
                if resp.status_code == 200:
                    data = resp.json()
                    print(f"  Success! Found {len(data) if isinstance(data, list) else 'data'}")
                    conversations = data
                    break
                else:
                    print(f"  {resp.status_code}: {resp.text[:100]}")
            except Exception as e:
                print(f"  Error: {e}")
    
    return conversations

def export_from_localstorage():
    """Alternative: Export using localStorage data pasted by user"""
    print("\n" + "="*60)
    print("MANUAL EXPORT MODE")
    print("="*60)
    print("""
Run this in your Chrome console on arena.ai:

copy(JSON.stringify({
    localStorage: Object.fromEntries(
        Object.entries(localStorage).filter(([k]) => 
            k.includes('sb-') || k.includes('supabase') || k.includes('auth')
        )
    ),
    cookies: document.cookie
}))

Then paste the result here:
""")
    
    try:
        data = input("> ").strip()
        if data:
            auth_data = json.loads(data)
            print(f"\nReceived: {json.dumps(auth_data, indent=2)[:500]}...")
            
            # Extract tokens
            for key, value in auth_data.get('localStorage', {}).items():
                try:
                    parsed = json.loads(value) if isinstance(value, str) else value
                    if isinstance(parsed, dict) and 'access_token' in parsed:
                        print(f"\nFound access token in {key}")
                        return fetch_conversations(parsed['access_token'])
                except:
                    pass
    except Exception as e:
        print(f"Error: {e}")
    
    return None

def main():
    print("Arena.ai Session Exporter")
    print("="*40)
    
    # Try Chrome cookies first
    print("\n[1] Attempting to read Chrome cookies...")
    cookies = get_arena_cookies()
    
    if cookies:
        print(f"\nFound {len(cookies)} arena.ai cookies")
        
        # Look for Supabase auth
        session = get_supabase_session(cookies)
        if session:
            print(f"Found auth cookies: {list(session.keys())}")
            # Try to extract JWT from session cookies
            for name, value in session.items():
                try:
                    data = json.loads(value)
                    if 'access_token' in data:
                        print(f"\nFetching conversations with token from {name}...")
                        convos = fetch_conversations(data['access_token'])
                        if convos:
                            output = Path('arena_conversations.json')
                            with open(output, 'w') as f:
                                json.dump(convos, f, indent=2)
                            print(f"\n✅ Saved to {output}")
                            return
                except:
                    continue
    
    # Fallback to manual mode
    print("\n[2] Chrome cookie extraction didn't find auth tokens.")
    convos = export_from_localstorage()
    
    if convos:
        output = Path('arena_conversations.json')
        with open(output, 'w') as f:
            json.dump(convos, f, indent=2)
        print(f"\n✅ Saved to {output}")
    else:
        print("\n❌ Could not extract conversations")
        print("Try the Tampermonkey userscript or bookmarklet instead.")

if __name__ == '__main__':
    main()
