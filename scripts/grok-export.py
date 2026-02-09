#!/usr/bin/env python3
"""
Grok Conversation Exporter for X.com

Exports Grok conversation history from X.com using the internal API.

Authentication requires:
- Bearer token (from X.com request headers)
- X-CSRF-Token (from X.com request headers)  
- Session cookies (from browser)

Usage:
    python grok-export.py --cookies "auth_token=xxx; ct0=yyy; ..." --csrf-token "your-csrf-token"
    
Or set environment variables:
    X_COOKIES="auth_token=xxx; ct0=yyy; ..."
    X_CSRF_TOKEN="your-csrf-token"
    X_BEARER_TOKEN="AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D..."
"""

import httpx
import json
import os
import argparse
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, asdict
import asyncio


# Known API endpoints
class GrokAPI:
    """X.com Grok API endpoints"""
    
    # GraphQL endpoints
    GRAPHQL_BASE = "https://x.com/i/api/graphql"
    
    # Known GraphQL query IDs (these may change over time)
    QUERY_IDS = {
        "CreateGrokConversation": "vvC5uy7pWWHXS2aDi1FZeA",  # or "6cmfJY3d7EPWuCSXWrkOFg"
        "GrokConversationItemByRestId": None,  # To be discovered
        "GrokConversationListSlice": None,  # To be discovered
    }
    
    # REST endpoints
    ADD_RESPONSE = "https://grok.x.com/2/grok/add_response.json"
    ADD_RESPONSE_ALT = "https://api.x.com/2/grok/add_response.json"
    UPLOAD_ATTACHMENT = "https://x.com/i/api/2/grok/attachment.json"
    
    # Grok history endpoints (discovered patterns)
    GROK_HISTORY = "https://x.com/i/api/2/grok/history.json"
    GROK_CONVERSATIONS = "https://x.com/i/api/2/grok/conversations.json"
    
    # Default bearer token (public, used by web client)
    DEFAULT_BEARER = "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"


@dataclass
class GrokMessage:
    """Represents a single Grok message"""
    sender: str  # "user" or "grok"
    message: str
    timestamp: Optional[str] = None
    feedback_labels: Optional[List[dict]] = None
    follow_up_suggestions: Optional[List[dict]] = None
    web_results: Optional[List[dict]] = None
    cited_web_results: Optional[List[dict]] = None
    tools_used: Optional[dict] = None
    

@dataclass
class GrokConversation:
    """Represents a Grok conversation"""
    conversation_id: str
    title: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    messages: Optional[List[GrokMessage]] = None


class RateLimiter:
    """Simple rate limiter to avoid hitting API limits"""
    
    def __init__(self, requests_per_minute: int = 30):
        self.requests_per_minute = requests_per_minute
        self.min_interval = 60.0 / requests_per_minute
        self.last_request = 0
        
    async def wait(self):
        """Wait if necessary to respect rate limits"""
        now = time.time()
        elapsed = now - self.last_request
        if elapsed < self.min_interval:
            await asyncio.sleep(self.min_interval - elapsed)
        self.last_request = time.time()


class GrokExporter:
    """
    Exports Grok conversations from X.com
    """
    
    def __init__(
        self,
        cookies: str,
        csrf_token: str,
        bearer_token: Optional[str] = None,
        requests_per_minute: int = 30,
    ):
        self.cookies = cookies
        self.csrf_token = csrf_token
        self.bearer_token = bearer_token or GrokAPI.DEFAULT_BEARER
        self.client_uuid = uuid.uuid4().hex
        self.rate_limiter = RateLimiter(requests_per_minute)
        
        # Build headers
        self.headers = self._build_headers()
        
        # HTTP client
        self.client = httpx.AsyncClient(
            headers=self.headers,
            timeout=30.0,
            follow_redirects=True,
        )
        
    def _build_headers(self) -> Dict[str, str]:
        """Build request headers matching X.com web client"""
        return {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "authorization": f"Bearer {self.bearer_token}",
            "content-type": "application/json",
            "cookie": self.cookies,
            "origin": "https://x.com",
            "referer": "https://x.com/i/grok",
            "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "x-client-uuid": self.client_uuid,
            "x-csrf-token": self.csrf_token,
            "x-twitter-active-user": "yes",
            "x-twitter-auth-type": "OAuth2Session",
            "x-twitter-client-language": "en",
        }
        
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
        
    async def _request(
        self,
        method: str,
        url: str,
        **kwargs
    ) -> httpx.Response:
        """Make a rate-limited request"""
        await self.rate_limiter.wait()
        
        response = await self.client.request(method, url, **kwargs)
        
        # Handle rate limiting
        if response.status_code == 429:
            retry_after = int(response.headers.get("retry-after", 60))
            print(f"Rate limited. Waiting {retry_after} seconds...")
            await asyncio.sleep(retry_after)
            return await self._request(method, url, **kwargs)
            
        return response
    
    async def discover_endpoints(self) -> Dict[str, str]:
        """
        Attempt to discover Grok API endpoints by probing known patterns.
        Returns a dict of discovered endpoints.
        """
        discovered = {}
        
        # Try common endpoint patterns
        patterns = [
            ("history", "https://x.com/i/api/2/grok/history.json"),
            ("history_alt", "https://api.x.com/2/grok/history.json"),
            ("conversations", "https://x.com/i/api/2/grok/conversations.json"),
            ("conversations_alt", "https://grok.x.com/2/grok/conversations.json"),
            ("list", "https://x.com/i/api/2/grok/conversation/list.json"),
        ]
        
        for name, url in patterns:
            try:
                response = await self._request("GET", url)
                if response.status_code == 200:
                    discovered[name] = url
                    print(f"✓ Found endpoint: {name} -> {url}")
                elif response.status_code != 404:
                    print(f"? Endpoint {name} returned {response.status_code}")
            except Exception as e:
                print(f"✗ Failed to probe {name}: {e}")
                
        # Try GraphQL endpoints
        graphql_patterns = [
            ("GrokConversations", "GrokConversations"),
            ("GrokConversationHistory", "GrokConversationHistory"),
            ("GrokConversationListSlice", "GrokConversationListSlice"),
            ("GrokConversationByRestId", "GrokConversationByRestId"),
            ("GrokConversationItemByRestId", "GrokConversationItemByRestId"),
        ]
        
        for name, query_name in graphql_patterns:
            # Try to find the query ID by making a request
            # This is speculative - real query IDs would need to be extracted from X.com's JS
            for possible_id in ["abc123", "xyz789"]:  # Placeholder - would need real IDs
                url = f"{GrokAPI.GRAPHQL_BASE}/{possible_id}/{query_name}"
                try:
                    response = await self._request(
                        "GET", 
                        url,
                        params={"variables": "{}"}
                    )
                    if response.status_code == 200:
                        discovered[f"graphql_{name}"] = url
                        print(f"✓ Found GraphQL endpoint: {name}")
                        break
                except:
                    pass
                    
        return discovered
        
    async def get_conversations_list(self) -> List[GrokConversation]:
        """
        Fetch list of Grok conversations.
        
        Note: This endpoint structure is based on reverse engineering.
        The actual endpoint may differ.
        """
        conversations = []
        
        # Try REST API first
        endpoints_to_try = [
            GrokAPI.GROK_CONVERSATIONS,
            GrokAPI.GROK_HISTORY,
            "https://x.com/i/api/2/grok/conversation/list.json",
            "https://grok.x.com/2/grok/conversations.json",
        ]
        
        for endpoint in endpoints_to_try:
            try:
                response = await self._request("GET", endpoint)
                if response.status_code == 200:
                    data = response.json()
                    print(f"Successfully fetched from: {endpoint}")
                    
                    # Parse response - structure depends on endpoint
                    if isinstance(data, list):
                        for item in data:
                            conv = GrokConversation(
                                conversation_id=item.get("conversationId") or item.get("id", ""),
                                title=item.get("title"),
                                created_at=item.get("createdAt") or item.get("created_at"),
                                updated_at=item.get("updatedAt") or item.get("updated_at"),
                            )
                            conversations.append(conv)
                    elif isinstance(data, dict):
                        items = data.get("conversations") or data.get("data") or data.get("items") or []
                        for item in items:
                            conv = GrokConversation(
                                conversation_id=item.get("conversationId") or item.get("id", ""),
                                title=item.get("title"),
                                created_at=item.get("createdAt") or item.get("created_at"),
                                updated_at=item.get("updatedAt") or item.get("updated_at"),
                            )
                            conversations.append(conv)
                            
                    if conversations:
                        return conversations
                        
            except Exception as e:
                print(f"Failed to fetch from {endpoint}: {e}")
                continue
                
        # Try GraphQL approach
        print("Attempting GraphQL approach...")
        
        # Try to create a conversation to verify authentication works
        try:
            response = await self.create_conversation()
            if response:
                print("Authentication verified - can create conversations")
                print("Note: Conversation listing endpoint not found in public documentation")
                print("Please check browser DevTools while browsing x.com/i/grok for the correct endpoint")
        except Exception as e:
            print(f"Authentication check failed: {e}")
            
        return conversations
        
    async def create_conversation(self) -> Optional[str]:
        """Create a new Grok conversation and return the conversation ID"""
        query_id = GrokAPI.QUERY_IDS["CreateGrokConversation"]
        url = f"{GrokAPI.GRAPHQL_BASE}/{query_id}/CreateGrokConversation"
        
        payload = {
            "variables": {},
            "queryId": query_id,
        }
        
        response = await self._request("POST", url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            try:
                conversation_id = data["data"]["create_grok_conversation"]["conversation_id"]
                return conversation_id
            except (KeyError, TypeError) as e:
                print(f"Failed to parse conversation ID: {e}")
                print(f"Response: {data}")
                return None
        else:
            print(f"Failed to create conversation: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    async def get_conversation_messages(
        self, 
        conversation_id: str
    ) -> List[GrokMessage]:
        """
        Fetch messages for a specific conversation.
        
        Note: This may require discovering the correct endpoint.
        """
        messages = []
        
        # Try various endpoint patterns
        endpoints = [
            f"https://x.com/i/api/2/grok/conversation/{conversation_id}.json",
            f"https://grok.x.com/2/grok/conversation/{conversation_id}.json",
            f"https://api.x.com/2/grok/conversation/{conversation_id}/messages.json",
        ]
        
        for endpoint in endpoints:
            try:
                response = await self._request("GET", endpoint)
                if response.status_code == 200:
                    data = response.json()
                    
                    # Parse messages from response
                    msg_list = data if isinstance(data, list) else data.get("messages", [])
                    
                    for msg in msg_list:
                        message = GrokMessage(
                            sender="user" if msg.get("sender") == 1 else "grok",
                            message=msg.get("message", ""),
                            timestamp=msg.get("timestamp") or msg.get("created_at"),
                            feedback_labels=msg.get("feedbackLabels"),
                            follow_up_suggestions=msg.get("followUpSuggestions"),
                            web_results=msg.get("webResults"),
                            cited_web_results=msg.get("citedWebResults"),
                            tools_used=msg.get("toolsUsed"),
                        )
                        messages.append(message)
                        
                    if messages:
                        return messages
                        
            except Exception as e:
                continue
                
        return messages
        
    async def export_all(self, output_dir: str = "grok_export") -> Dict[str, Any]:
        """
        Export all Grok conversations to files.
        
        Returns a summary of the export.
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        summary = {
            "exported_at": datetime.now().isoformat(),
            "conversations_found": 0,
            "messages_exported": 0,
            "files": [],
        }
        
        print("Fetching conversations list...")
        conversations = await self.get_conversations_list()
        
        if not conversations:
            print("\nNo conversations found via API.")
            print("\n--- Manual Export Instructions ---")
            print("1. Open Chrome DevTools (F12) on x.com/i/grok")
            print("2. Go to Network tab and filter by 'XHR'")
            print("3. Browse your Grok conversations")
            print("4. Look for requests to endpoints containing 'grok' or 'conversation'")
            print("5. Copy the request details and update this script")
            print("\nAlternatively, check GROK_HISTORY_ENDPOINT environment variable")
            return summary
            
        summary["conversations_found"] = len(conversations)
        print(f"Found {len(conversations)} conversations")
        
        for i, conv in enumerate(conversations, 1):
            print(f"\nExporting conversation {i}/{len(conversations)}: {conv.conversation_id}")
            
            # Fetch messages
            messages = await self.get_conversation_messages(conv.conversation_id)
            conv.messages = messages
            summary["messages_exported"] += len(messages)
            
            # Save to file
            filename = f"conversation_{conv.conversation_id}.json"
            filepath = output_path / filename
            
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(asdict(conv), f, indent=2, ensure_ascii=False)
                
            summary["files"].append(str(filepath))
            print(f"  Saved {len(messages)} messages to {filename}")
            
        # Save summary
        summary_path = output_path / "export_summary.json"
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
            
        print(f"\n✓ Export complete! Files saved to: {output_path}")
        print(f"  Conversations: {summary['conversations_found']}")
        print(f"  Messages: {summary['messages_exported']}")
        
        return summary


def parse_cookies_from_file(filepath: str) -> str:
    """Parse cookies from a Netscape cookies.txt file or JSON"""
    with open(filepath, "r") as f:
        content = f.read().strip()
        
    # Try JSON format first
    try:
        cookies = json.loads(content)
        if isinstance(cookies, list):
            # Cookie list format
            return "; ".join(f"{c['name']}={c['value']}" for c in cookies)
        elif isinstance(cookies, dict):
            # Simple dict format
            return "; ".join(f"{k}={v}" for k, v in cookies.items())
    except json.JSONDecodeError:
        pass
        
    # Try Netscape format
    cookie_pairs = []
    for line in content.split("\n"):
        if line.startswith("#") or not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) >= 7:
            cookie_pairs.append(f"{parts[5]}={parts[6]}")
            
    if cookie_pairs:
        return "; ".join(cookie_pairs)
        
    # Return as-is (might already be in the right format)
    return content


async def main():
    parser = argparse.ArgumentParser(
        description="Export Grok conversations from X.com",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Using command line arguments:
  python grok-export.py --cookies "auth_token=xxx; ct0=yyy" --csrf-token "abc123"
  
  # Using environment variables:
  export X_COOKIES="auth_token=xxx; ct0=yyy"
  export X_CSRF_TOKEN="abc123"
  python grok-export.py
  
  # Using a cookies file:
  python grok-export.py --cookies-file cookies.json --csrf-token "abc123"
  
  # Discover endpoints (useful for debugging):
  python grok-export.py --discover --cookies "..." --csrf-token "..."
  
How to get credentials:
  1. Log into x.com in your browser
  2. Open DevTools (F12) -> Network tab
  3. Go to x.com/i/grok and start a conversation
  4. Find any request to x.com and copy:
     - Cookie header value -> --cookies
     - x-csrf-token header value -> --csrf-token
        """,
    )
    
    parser.add_argument(
        "--cookies",
        help="Cookie string from browser (or set X_COOKIES env var)",
        default=os.environ.get("X_COOKIES", ""),
    )
    parser.add_argument(
        "--cookies-file",
        help="Path to cookies file (JSON or Netscape format)",
    )
    parser.add_argument(
        "--csrf-token",
        help="X-CSRF-Token from browser (or set X_CSRF_TOKEN env var)",
        default=os.environ.get("X_CSRF_TOKEN", ""),
    )
    parser.add_argument(
        "--bearer-token",
        help="Bearer token (optional, uses default if not set)",
        default=os.environ.get("X_BEARER_TOKEN", ""),
    )
    parser.add_argument(
        "--output",
        help="Output directory for exported conversations",
        default="grok_export",
    )
    parser.add_argument(
        "--rate-limit",
        help="Requests per minute (default: 30)",
        type=int,
        default=30,
    )
    parser.add_argument(
        "--discover",
        help="Discover available API endpoints",
        action="store_true",
    )
    
    args = parser.parse_args()
    
    # Get cookies
    cookies = args.cookies
    if args.cookies_file:
        cookies = parse_cookies_from_file(args.cookies_file)
        
    if not cookies:
        print("Error: No cookies provided. Use --cookies or set X_COOKIES environment variable.")
        print("Run with --help for instructions on how to get credentials.")
        return 1
        
    if not args.csrf_token:
        # Try to extract from cookies (ct0 cookie is the CSRF token)
        import re
        match = re.search(r'ct0=([^;]+)', cookies)
        if match:
            args.csrf_token = match.group(1)
            print(f"Extracted CSRF token from cookies: {args.csrf_token[:20]}...")
        else:
            print("Error: No CSRF token provided. Use --csrf-token or set X_CSRF_TOKEN environment variable.")
            return 1
    
    print("Initializing Grok Exporter...")
    print(f"  Rate limit: {args.rate_limit} requests/minute")
    
    exporter = GrokExporter(
        cookies=cookies,
        csrf_token=args.csrf_token,
        bearer_token=args.bearer_token or None,
        requests_per_minute=args.rate_limit,
    )
    
    try:
        if args.discover:
            print("\nDiscovering API endpoints...")
            endpoints = await exporter.discover_endpoints()
            print(f"\nDiscovered {len(endpoints)} endpoints:")
            for name, url in endpoints.items():
                print(f"  {name}: {url}")
        else:
            await exporter.export_all(args.output)
            
    finally:
        await exporter.close()
        
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
