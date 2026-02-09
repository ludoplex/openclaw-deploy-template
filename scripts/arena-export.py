#!/usr/bin/env python3
"""
Arena.ai (formerly LMArena/LMSYS Chatbot Arena) Conversation Export Tool

This script extracts your conversation history from arena.ai.

Architecture:
- Arena uses Supabase for auth (auth.arena.ai) and data storage
- Conversations are stored in Supabase PostgreSQL with Row Level Security
- Auth tokens are stored in browser cookies/localStorage
- The Supabase anon key is publicly available in the frontend JS

Usage:
1. Login to arena.ai in your browser
2. Export cookies using a browser extension (EditThisCookie, etc.) to cookies.json
3. Run: python arena-export.py --cookies cookies.json --output conversations.json

Alternative method:
- Pass auth token directly: python arena-export.py --token "your-jwt-token"

Author: OpenClaw Subagent
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin

try:
    import requests
except ImportError:
    print("Error: 'requests' library required. Install with: pip install requests")
    sys.exit(1)

# Arena.ai Supabase configuration
SUPABASE_URL = "https://auth.arena.ai"
# The anon key is public and extracted from arena.ai frontend JS
# This key only allows authenticated operations with valid JWT
SUPABASE_ANON_KEY = None  # Will be fetched dynamically

# Known API endpoints
ARENA_BASE_URL = "https://arena.ai"
NEXTJS_API_URL = "https://arena.ai/nextjs-api"


class ArenaExporter:
    def __init__(self, auth_token: Optional[str] = None, cookies_file: Optional[str] = None):
        self.session = requests.Session()
        self.auth_token = auth_token
        self.supabase_url = SUPABASE_URL
        self.anon_key = None
        self.user_id = None
        
        # Set up auth
        if cookies_file:
            self._load_cookies(cookies_file)
        elif auth_token:
            self._set_auth_token(auth_token)
            
        # Fetch the public anon key
        self._fetch_anon_key()
        
    def _fetch_anon_key(self):
        """Fetch the Supabase anon key from Arena frontend."""
        try:
            # The anon key is embedded in the Next.js chunks
            # We'll try to extract it from the main page or a known endpoint
            resp = self.session.get(f"{ARENA_BASE_URL}/", timeout=30)
            
            # Look for Supabase URL pattern in the HTML/JS
            # Pattern: NEXT_PUBLIC_SUPABASE_ANON_KEY or similar
            patterns = [
                r'eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+',  # JWT pattern
                r'"apikey"\s*:\s*"([^"]+)"',
                r'anon[_-]?key["\s:]+["\']([^"\']+)["\']',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, resp.text)
                for match in matches:
                    if match.startswith('eyJ') and len(match) > 100:
                        self.anon_key = match
                        print(f"[+] Found Supabase anon key")
                        return
                        
            # Fallback: check static JS chunks
            chunk_pattern = r'static/chunks/[^"]+\.js'
            chunks = re.findall(chunk_pattern, resp.text)[:5]  # Check first 5 chunks
            
            for chunk in chunks:
                chunk_url = f"{ARENA_BASE_URL}/_next/{chunk}"
                try:
                    chunk_resp = self.session.get(chunk_url, timeout=10)
                    for pattern in patterns:
                        matches = re.findall(pattern, chunk_resp.text)
                        for match in matches:
                            if match.startswith('eyJ') and len(match) > 100:
                                self.anon_key = match
                                print(f"[+] Found Supabase anon key in chunk")
                                return
                except:
                    continue
                    
            print("[!] Could not find Supabase anon key, some features may not work")
            
        except Exception as e:
            print(f"[!] Error fetching anon key: {e}")
    
    def _load_cookies(self, cookies_file: str):
        """Load cookies from a JSON file (EditThisCookie format)."""
        try:
            with open(cookies_file, 'r') as f:
                cookies_data = json.load(f)
            
            # Handle different cookie export formats
            if isinstance(cookies_data, list):
                # EditThisCookie format
                for cookie in cookies_data:
                    name = cookie.get('name', cookie.get('Name', ''))
                    value = cookie.get('value', cookie.get('Value', ''))
                    domain = cookie.get('domain', cookie.get('Domain', ''))
                    
                    if name and value:
                        self.session.cookies.set(name, value, domain=domain.lstrip('.'))
                        
                        # Check for Supabase auth tokens
                        if 'access_token' in name or 'sb-' in name:
                            self._extract_token_from_cookie(value)
                            
            elif isinstance(cookies_data, dict):
                # Simple key-value format
                for name, value in cookies_data.items():
                    self.session.cookies.set(name, value)
                    
            print(f"[+] Loaded {len(self.session.cookies)} cookies")
            
        except Exception as e:
            print(f"[-] Error loading cookies: {e}")
            raise
    
    def _extract_token_from_cookie(self, value: str):
        """Try to extract JWT from cookie value."""
        # Supabase stores tokens as JSON in cookies
        try:
            if value.startswith('{'):
                data = json.loads(value)
                if 'access_token' in data:
                    self.auth_token = data['access_token']
                    self.user_id = data.get('user', {}).get('id')
                    print(f"[+] Found auth token, user_id: {self.user_id}")
            elif value.startswith('eyJ'):
                # Direct JWT
                self.auth_token = value
                print("[+] Found JWT auth token")
        except:
            pass
    
    def _set_auth_token(self, token: str):
        """Set the auth token directly."""
        self.auth_token = token
        # Try to decode user ID from JWT
        try:
            import base64
            payload = token.split('.')[1]
            # Add padding
            payload += '=' * (4 - len(payload) % 4)
            decoded = json.loads(base64.urlsafe_b64decode(payload))
            self.user_id = decoded.get('sub')
            print(f"[+] Decoded user_id: {self.user_id}")
        except Exception as e:
            print(f"[!] Could not decode JWT: {e}")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for Supabase API requests."""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        
        if self.anon_key:
            headers['apikey'] = self.anon_key
            
        if self.auth_token:
            headers['Authorization'] = f'Bearer {self.auth_token}'
            
        return headers
    
    def test_auth(self) -> bool:
        """Test if authentication is working."""
        try:
            # Try to get user info from Supabase
            resp = self.session.get(
                f"{self.supabase_url}/auth/v1/user",
                headers=self._get_headers(),
                timeout=30
            )
            
            if resp.status_code == 200:
                user_data = resp.json()
                self.user_id = user_data.get('id')
                print(f"[+] Authenticated as user: {self.user_id}")
                print(f"    Email: {user_data.get('email', 'N/A')}")
                return True
            else:
                print(f"[-] Auth test failed: {resp.status_code}")
                print(f"    Response: {resp.text[:200]}")
                return False
                
        except Exception as e:
            print(f"[-] Auth test error: {e}")
            return False
    
    def get_conversations_supabase(self) -> List[Dict]:
        """Fetch conversations directly from Supabase REST API."""
        if not self.user_id:
            print("[-] No user_id available, cannot fetch conversations")
            return []
        
        conversations = []
        
        try:
            # Common Supabase table names for conversations
            table_names = [
                'conversations',
                'chats', 
                'evaluations',
                'battles',
                'sessions',
                'evaluation_sessions',
            ]
            
            for table in table_names:
                try:
                    resp = self.session.get(
                        f"{self.supabase_url}/rest/v1/{table}",
                        headers=self._get_headers(),
                        params={
                            'select': '*',
                            'user_id': f'eq.{self.user_id}',
                            'order': 'created_at.desc',
                            'limit': 1000
                        },
                        timeout=30
                    )
                    
                    if resp.status_code == 200:
                        data = resp.json()
                        if data:
                            print(f"[+] Found {len(data)} records in '{table}'")
                            conversations.extend(data)
                    elif resp.status_code != 404:
                        print(f"[!] Table '{table}': {resp.status_code}")
                        
                except Exception as e:
                    continue
                    
            # Also try to get messages/turns
            message_tables = ['messages', 'turns', 'conversation_messages']
            for table in message_tables:
                try:
                    resp = self.session.get(
                        f"{self.supabase_url}/rest/v1/{table}",
                        headers=self._get_headers(),
                        params={
                            'select': '*',
                            'order': 'created_at.desc',
                            'limit': 5000
                        },
                        timeout=30
                    )
                    
                    if resp.status_code == 200:
                        data = resp.json()
                        if data:
                            print(f"[+] Found {len(data)} records in '{table}'")
                            # Attach messages to conversations
                            for conv in conversations:
                                conv_id = conv.get('id')
                                conv_messages = [m for m in data if m.get('conversation_id') == conv_id]
                                if conv_messages:
                                    conv['messages'] = conv_messages
                                    
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"[-] Error fetching from Supabase: {e}")
            
        return conversations
    
    def get_conversations_nextjs(self) -> List[Dict]:
        """Try to fetch conversations via Next.js API routes."""
        conversations = []
        
        # Common Next.js API route patterns
        api_routes = [
            '/nextjs-api/conversations',
            '/nextjs-api/user/conversations', 
            '/nextjs-api/history',
            '/nextjs-api/battles',
            '/nextjs-api/evaluations',
            '/api/conversations',
            '/api/user/history',
        ]
        
        for route in api_routes:
            try:
                url = f"{ARENA_BASE_URL}{route}"
                resp = self.session.get(
                    url,
                    headers=self._get_headers(),
                    timeout=30
                )
                
                if resp.status_code == 200:
                    data = resp.json()
                    if isinstance(data, list):
                        print(f"[+] Found {len(data)} items via {route}")
                        conversations.extend(data)
                    elif isinstance(data, dict) and 'conversations' in data:
                        items = data['conversations']
                        print(f"[+] Found {len(items)} items via {route}")
                        conversations.extend(items)
                        
            except Exception as e:
                continue
                
        return conversations
    
    def get_conversation_by_id(self, conv_id: str) -> Optional[Dict]:
        """Fetch a specific conversation by ID."""
        # Try different endpoints
        endpoints = [
            f"/nextjs-api/conversations/{conv_id}",
            f"/nextjs-api/c/{conv_id}",
            f"/api/conversations/{conv_id}",
        ]
        
        for endpoint in endpoints:
            try:
                resp = self.session.get(
                    f"{ARENA_BASE_URL}{endpoint}",
                    headers=self._get_headers(),
                    timeout=30
                )
                
                if resp.status_code == 200:
                    return resp.json()
                    
            except:
                continue
                
        # Try Supabase direct
        try:
            resp = self.session.get(
                f"{self.supabase_url}/rest/v1/conversations",
                headers=self._get_headers(),
                params={
                    'select': '*',
                    'id': f'eq.{conv_id}'
                },
                timeout=30
            )
            
            if resp.status_code == 200:
                data = resp.json()
                if data:
                    return data[0]
                    
        except:
            pass
            
        return None
    
    def export_all(self) -> Dict:
        """Export all available data."""
        export_data = {
            'exported_at': datetime.utcnow().isoformat(),
            'user_id': self.user_id,
            'source': 'arena.ai',
            'conversations': [],
            'metadata': {}
        }
        
        # Try multiple methods
        print("\n[*] Fetching conversations via Next.js API...")
        nextjs_convs = self.get_conversations_nextjs()
        
        print("\n[*] Fetching conversations via Supabase...")
        supabase_convs = self.get_conversations_supabase()
        
        # Merge and deduplicate
        all_convs = {}
        for conv in nextjs_convs + supabase_convs:
            conv_id = conv.get('id')
            if conv_id and conv_id not in all_convs:
                all_convs[conv_id] = conv
                
        export_data['conversations'] = list(all_convs.values())
        export_data['metadata'] = {
            'total_conversations': len(export_data['conversations']),
            'fetch_methods': ['nextjs_api', 'supabase_rest']
        }
        
        return export_data


def extract_from_localstorage_instructions():
    """Print instructions for extracting data from browser localStorage."""
    print("""
========================================================================
          Arena.ai Conversation Extraction Methods
========================================================================

  METHOD 1: Browser Console (Recommended)
  ----------------------------------------
  1. Go to https://arena.ai and log in with Google/email
  2. Open Developer Tools (F12 or Cmd+Option+I)
  3. Go to Application tab -> Local Storage -> auth.arena.ai
  4. Find the key like 'sb-xxxxx-auth-token'
  5. Copy the 'access_token' value from the JSON
  6. Run: python arena-export.py --token "your_access_token"

  METHOD 2: Console Script (Full Export)
  --------------------------------------
  In DevTools Console, paste:

    // Export all localStorage auth data
    const data = {};
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key.includes('supabase') || key.includes('sb-') ||
          key.includes('auth') || key.includes('arena')) {
        data[key] = localStorage.getItem(key);
      }
    }
    console.log(JSON.stringify(data));
    copy(JSON.stringify(data)); // Copies to clipboard

  Paste to 'localstorage.json' and run:
  python arena-export.py --localstorage localstorage.json

  METHOD 3: Cookie Export
  -----------------------
  1. Install browser extension like "EditThisCookie"
  2. On arena.ai, export all cookies to JSON
  3. Run: python arena-export.py --cookies cookies.json

  METHOD 4: Network Intercept (Most Reliable)
  -------------------------------------------
  1. Open DevTools -> Network tab
  2. Navigate around arena.ai to trigger API calls
  3. Find requests to auth.arena.ai or nextjs-api
  4. Copy the 'Authorization: Bearer xxx' header value
  5. Run: python arena-export.py --token "xxx"

========================================================================
""")


def main():
    parser = argparse.ArgumentParser(
        description='Export your arena.ai conversation history',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Using cookies exported from browser
  python arena-export.py --cookies cookies.json --output my_arena_history.json
  
  # Using JWT token directly
  python arena-export.py --token "eyJ..." --output my_arena_history.json
  
  # Using localStorage export
  python arena-export.py --localstorage localstorage.json --output my_arena_history.json
  
  # Show browser extraction instructions
  python arena-export.py --help-browser
"""
    )
    
    parser.add_argument('--cookies', '-c', help='Path to cookies JSON file')
    parser.add_argument('--token', '-t', help='Supabase JWT auth token')
    parser.add_argument('--localstorage', '-l', help='Path to localStorage JSON export')
    parser.add_argument('--output', '-o', default='arena_export.json', 
                       help='Output file path (default: arena_export.json)')
    parser.add_argument('--help-browser', action='store_true',
                       help='Show browser extraction instructions')
    
    args = parser.parse_args()
    
    if args.help_browser:
        extract_from_localstorage_instructions()
        return
    
    # Handle localStorage input
    token = args.token
    if args.localstorage and not token:
        try:
            with open(args.localstorage, 'r') as f:
                ls_data = json.load(f)
            
            # Look for Supabase auth data
            for key, value in ls_data.items():
                if 'auth' in key.lower() or 'token' in key.lower():
                    try:
                        parsed = json.loads(value) if isinstance(value, str) else value
                        if 'access_token' in parsed:
                            token = parsed['access_token']
                            print(f"[+] Found access_token in localStorage key: {key}")
                            break
                    except:
                        if isinstance(value, str) and value.startswith('eyJ'):
                            token = value
                            break
        except Exception as e:
            print(f"[-] Error reading localStorage file: {e}")
            sys.exit(1)
    
    if not args.cookies and not token:
        print("[-] Error: Please provide --cookies, --token, or --localstorage")
        print("    Run with --help-browser for browser extraction instructions")
        sys.exit(1)
    
    print("""
========================================================================
             Arena.ai Conversation Export Tool
========================================================================
""")
    
    # Create exporter
    exporter = ArenaExporter(
        auth_token=token,
        cookies_file=args.cookies
    )
    
    # Test authentication
    print("[*] Testing authentication...")
    if not exporter.test_auth():
        print("\n[-] Authentication failed!")
        print("    Make sure your cookies/token are fresh (try logging in again)")
        extract_from_localstorage_instructions()
        sys.exit(1)
    
    # Export data
    print("\n[*] Starting export...")
    export_data = exporter.export_all()
    
    # Write output
    output_path = Path(args.output)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"""
========================================================================
                      Export Complete!
========================================================================
  Output file: {str(output_path)}
  Total conversations: {export_data['metadata']['total_conversations']}
========================================================================
""")


if __name__ == '__main__':
    main()
