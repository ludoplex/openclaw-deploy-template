#!/usr/bin/env python3
"""
Perplexity.ai Conversation History Exporter

Exports ALL conversation history from Perplexity.ai to JSON and Markdown files.

## Authentication
Perplexity uses cookie-based authentication. You need to extract cookies from your browser:

1. Log into perplexity.ai in your browser
2. Open DevTools (F12) → Application → Cookies → https://www.perplexity.ai
3. Copy these cookies (if present):
   - __Secure-next-auth.session-token
   - __Secure-next-auth.callback-url
   - Any other session-related cookies
   
Alternatively, export all cookies using a browser extension like "Cookie-Editor" (export as JSON).

## API Endpoints (Reverse-Engineered)
- GET /rest/thread/list_recent?limit=50&offset=0 - List user's threads
- GET /rest/thread/{thread_id}?limit=100 - Get full thread with messages

## Pagination
- List endpoint: offset-based (offset parameter)
- Thread endpoint: cursor-based (next_cursor in response)

## Usage
    python perplexity-export.py --cookies cookies.json --output ./exports
    python perplexity-export.py --cookie-string "name1=value1; name2=value2" --output ./exports
"""

import argparse
import asyncio
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from dataclasses import dataclass, field

import httpx


# =============================================================================
# Configuration
# =============================================================================

BASE_URL = "https://www.perplexity.ai"
API_BASE = f"{BASE_URL}/rest"

DEFAULT_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Referer": f"{BASE_URL}/library",
    "Origin": BASE_URL,
}

# Rate limiting
RATE_LIMIT_DELAY = 0.5  # seconds between requests
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds on 429

# Pagination
LIST_PAGE_SIZE = 50
THREAD_PAGE_SIZE = 100


# =============================================================================
# Data Models
# =============================================================================

@dataclass
class ThreadListItem:
    """Minimal thread info from list endpoint"""
    uuid: str
    title: str
    updated_at: str
    url_slug: str


@dataclass
class ConversationEntry:
    """A single Q&A turn in a conversation"""
    uuid: str
    query: str
    answer: str
    model: str
    mode: str
    sources: list[dict]
    images: list[dict]
    videos: list[dict]
    created_at: str
    updated_at: str
    raw: dict = field(repr=False)


@dataclass
class Conversation:
    """Full conversation with all entries"""
    uuid: str
    title: str
    url_slug: str
    entries: list[ConversationEntry]
    raw: dict = field(repr=False)


# =============================================================================
# Cookie Handling
# =============================================================================

def load_cookies_from_json(path: str) -> dict[str, str]:
    """Load cookies from JSON file (Cookie-Editor format or simple key-value)"""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cookies = {}
    
    # Handle Cookie-Editor export format (list of objects)
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and 'name' in item and 'value' in item:
                # Filter for perplexity.ai cookies
                domain = item.get('domain', '')
                if 'perplexity' in domain or not domain:
                    cookies[item['name']] = item['value']
    # Handle simple key-value format
    elif isinstance(data, dict):
        cookies = data
    
    return cookies


def parse_cookie_string(cookie_str: str) -> dict[str, str]:
    """Parse cookie string like 'name1=value1; name2=value2'"""
    cookies = {}
    for pair in cookie_str.split(';'):
        pair = pair.strip()
        if '=' in pair:
            name, value = pair.split('=', 1)
            cookies[name.strip()] = value.strip()
    return cookies


def cookies_to_header(cookies: dict[str, str]) -> str:
    """Convert cookies dict to Cookie header value"""
    return '; '.join(f'{k}={v}' for k, v in cookies.items())


# =============================================================================
# API Client
# =============================================================================

class PerplexityClient:
    """HTTP client for Perplexity.ai API"""
    
    def __init__(self, cookies: dict[str, str]):
        self.cookies = cookies
        self.client: Optional[httpx.AsyncClient] = None
        self._request_count = 0
        
    async def __aenter__(self):
        headers = DEFAULT_HEADERS.copy()
        headers['Cookie'] = cookies_to_header(self.cookies)
        
        self.client = httpx.AsyncClient(
            headers=headers,
            timeout=30.0,
            follow_redirects=True,
        )
        return self
    
    async def __aexit__(self, *args):
        if self.client:
            await self.client.aclose()
    
    async def _request(self, method: str, url: str, **kwargs) -> dict:
        """Make an API request with retry logic"""
        if not self.client:
            raise RuntimeError("Client not initialized. Use 'async with' context.")
        
        for attempt in range(MAX_RETRIES):
            # Rate limiting
            self._request_count += 1
            if self._request_count > 1:
                await asyncio.sleep(RATE_LIMIT_DELAY)
            
            try:
                response = await self.client.request(method, url, **kwargs)
                
                if response.status_code == 429:
                    wait_time = RETRY_DELAY * (attempt + 1)
                    print(f"Rate limited (429). Waiting {wait_time}s before retry...")
                    await asyncio.sleep(wait_time)
                    continue
                
                if response.status_code == 401 or response.status_code == 403:
                    raise PermissionError(
                        f"Authentication failed ({response.status_code}). "
                        "Your cookies may be invalid or expired."
                    )
                
                response.raise_for_status()
                return response.json()
                
            except httpx.HTTPStatusError as e:
                if attempt < MAX_RETRIES - 1:
                    print(f"Request failed: {e}. Retrying...")
                    await asyncio.sleep(RETRY_DELAY)
                else:
                    raise
        
        raise RuntimeError(f"Max retries exceeded for {url}")
    
    async def list_threads(self, offset: int = 0, limit: int = LIST_PAGE_SIZE) -> tuple[list[dict], bool]:
        """
        List user's threads (conversations).
        
        Returns: (threads, has_more)
        """
        url = f"{API_BASE}/thread/list_recent"
        params = {"limit": limit, "offset": offset}
        
        data = await self._request("GET", url, params=params)
        
        # Response format varies - handle both array and object responses
        if isinstance(data, list):
            threads = data
            has_more = len(threads) >= limit
        else:
            threads = data.get('threads', data.get('entries', []))
            has_more = data.get('has_next_page', data.get('has_more', len(threads) >= limit))
        
        return threads, has_more
    
    async def get_thread(self, thread_id: str, cursor: Optional[str] = None) -> dict:
        """
        Get full thread data with all entries.
        
        Returns the thread data with entries and pagination info.
        """
        url = f"{API_BASE}/thread/{thread_id}"
        params = {"limit": THREAD_PAGE_SIZE}
        if cursor:
            params["cursor"] = cursor
        
        return await self._request("GET", url, params=params)
    
    async def get_full_thread(self, thread_id: str) -> dict:
        """Get complete thread with all pages of entries"""
        all_entries = []
        cursor = None
        base_data = None
        
        while True:
            data = await self.get_thread(thread_id, cursor)
            
            if base_data is None:
                base_data = data
            
            entries = data.get('entries', [])
            all_entries.extend(entries)
            
            if not data.get('has_next_page', False):
                break
            
            cursor = data.get('next_cursor')
            if not cursor:
                break
        
        if base_data:
            base_data['entries'] = all_entries
        
        return base_data or {'entries': all_entries}


# =============================================================================
# Data Parsing
# =============================================================================

def parse_entry(entry_data: dict) -> ConversationEntry:
    """Parse a single conversation entry from API response"""
    
    # Extract answer text from blocks
    answer = ""
    sources = []
    images = []
    videos = []
    
    blocks = entry_data.get('blocks', [])
    for block in blocks:
        intended_usage = block.get('intended_usage', '')
        
        if intended_usage == 'ask_text':
            markdown_block = block.get('markdown_block', {})
            answer = markdown_block.get('answer', '')
        
        elif intended_usage == 'sources_answer_mode':
            sources_block = block.get('sources_mode_block', {})
            rows = sources_block.get('rows', [])
            for row in rows:
                web_result = row.get('web_result', {})
                sources.append({
                    'name': web_result.get('name', ''),
                    'url': web_result.get('url', ''),
                    'snippet': web_result.get('snippet', ''),
                })
        
        elif intended_usage == 'image_answer_mode':
            image_block = block.get('image_mode_block', {})
            for item in image_block.get('media_items', []):
                images.append({
                    'name': item.get('name', ''),
                    'url': item.get('url', ''),
                    'image': item.get('image', ''),
                })
        
        elif intended_usage == 'video_answer_mode':
            video_block = block.get('video_mode_block', {})
            for item in video_block.get('media_items', []):
                videos.append({
                    'name': item.get('name', ''),
                    'url': item.get('url', ''),
                })
    
    return ConversationEntry(
        uuid=entry_data.get('uuid', ''),
        query=entry_data.get('query_str', ''),
        answer=answer,
        model=entry_data.get('display_model', entry_data.get('user_selected_model', '')),
        mode=entry_data.get('mode', ''),
        sources=sources,
        images=images,
        videos=videos,
        created_at=entry_data.get('updated_datetime', ''),
        updated_at=entry_data.get('entry_updated_datetime', ''),
        raw=entry_data,
    )


def parse_thread(thread_data: dict) -> Conversation:
    """Parse full thread data into Conversation object"""
    entries_data = thread_data.get('entries', [])
    entries = [parse_entry(e) for e in entries_data]
    
    # Get metadata from first entry
    first_entry = entries_data[0] if entries_data else {}
    
    return Conversation(
        uuid=first_entry.get('context_uuid', first_entry.get('uuid', '')),
        title=first_entry.get('thread_title', 'Untitled'),
        url_slug=first_entry.get('thread_url_slug', ''),
        entries=entries,
        raw=thread_data,
    )


# =============================================================================
# Markdown Rendering
# =============================================================================

def sanitize_filename(name: str, max_length: int = 100) -> str:
    """Create a safe filename from a string"""
    # Remove/replace unsafe characters
    safe = re.sub(r'[<>:"/\\|?*]', '_', name)
    safe = re.sub(r'\s+', ' ', safe).strip()
    
    if len(safe) > max_length:
        safe = safe[:max_length].rsplit(' ', 1)[0]
    
    return safe or 'untitled'


def render_conversation_markdown(conv: Conversation) -> str:
    """Render a conversation as markdown"""
    lines = []
    
    # YAML frontmatter
    lines.append("---")
    lines.append(f"title: \"{conv.title.replace('\"', '\\'+'\"')}\"")
    lines.append(f"uuid: {conv.uuid}")
    if conv.url_slug:
        lines.append(f"url: https://www.perplexity.ai/search/{conv.url_slug}")
    if conv.entries:
        lines.append(f"created: {conv.entries[0].created_at}")
        lines.append(f"updated: {conv.entries[-1].updated_at}")
        lines.append(f"turns: {len(conv.entries)}")
    lines.append("---")
    lines.append("")
    
    # Title
    lines.append(f"# {conv.title}")
    lines.append("")
    
    for i, entry in enumerate(conv.entries):
        if i > 0:
            lines.append("")
            lines.append("---")
            lines.append("")
        
        # Query
        lines.append(f"## Q: {entry.query}")
        lines.append("")
        
        # Model info
        if entry.model or entry.mode:
            meta = []
            if entry.model:
                meta.append(f"Model: {entry.model}")
            if entry.mode:
                meta.append(f"Mode: {entry.mode}")
            lines.append(f"> *{' | '.join(meta)}*")
            lines.append("")
        
        # Images
        if entry.images:
            lines.append("### Images")
            for img in entry.images:
                if img.get('image'):
                    lines.append(f"![{img.get('name', 'Image')}]({img['image']})")
            lines.append("")
        
        # Videos
        if entry.videos:
            lines.append("### Videos")
            for vid in entry.videos:
                lines.append(f"- [{vid.get('name', 'Video')}]({vid['url']})")
            lines.append("")
        
        # Answer
        if entry.answer:
            # Clean up the answer text
            answer = entry.answer
            # Remove pplx:// internal links
            answer = re.sub(r'\[(.*?)\]\(pplx://.*?\)', r'\1', answer)
            lines.append(answer)
            lines.append("")
        
        # Sources
        if entry.sources:
            lines.append("### Sources")
            for j, src in enumerate(entry.sources, 1):
                if src.get('url', '').startswith('http'):
                    lines.append(f"{j}. [{src.get('name', 'Source')}]({src['url']})")
                else:
                    lines.append(f"{j}. {src.get('name', 'Source')}")
                if src.get('snippet'):
                    lines.append(f"   > {src['snippet'][:200]}...")
            lines.append("")
    
    return '\n'.join(lines)


# =============================================================================
# Export Functions
# =============================================================================

async def export_all_conversations(
    client: PerplexityClient,
    output_dir: Path,
    json_only: bool = False,
    markdown_only: bool = False,
) -> tuple[int, int]:
    """
    Export all conversations from Perplexity.
    
    Returns: (success_count, error_count)
    """
    # Create output directories
    json_dir = output_dir / "json"
    md_dir = output_dir / "markdown"
    
    if not markdown_only:
        json_dir.mkdir(parents=True, exist_ok=True)
    if not json_only:
        md_dir.mkdir(parents=True, exist_ok=True)
    
    success = 0
    errors = 0
    offset = 0
    
    print("Fetching thread list...")
    
    while True:
        threads, has_more = await client.list_threads(offset=offset)
        
        if not threads:
            break
        
        print(f"Found {len(threads)} threads (offset {offset})")
        
        for thread_info in threads:
            # Extract thread ID - handle different response formats
            thread_id = (
                thread_info.get('uuid') or 
                thread_info.get('thread_uuid') or
                thread_info.get('id') or
                thread_info.get('context_uuid')
            )
            
            if not thread_id:
                print(f"  ⚠ Could not extract thread ID from: {thread_info}")
                errors += 1
                continue
            
            title = (
                thread_info.get('thread_title') or 
                thread_info.get('title') or
                thread_info.get('query_str', '')[:50] or
                'Untitled'
            )
            
            print(f"  → Exporting: {title[:50]}...")
            
            try:
                # Fetch full thread data
                thread_data = await client.get_full_thread(thread_id)
                
                if not thread_data or not thread_data.get('entries'):
                    print(f"    ⚠ No entries found for thread")
                    errors += 1
                    continue
                
                # Parse conversation
                conv = parse_thread(thread_data)
                
                # Generate filename
                date_prefix = ""
                if conv.entries:
                    try:
                        dt = datetime.fromisoformat(conv.entries[0].created_at.replace('Z', '+00:00'))
                        date_prefix = dt.strftime("%Y-%m-%d_")
                    except:
                        pass
                
                safe_title = sanitize_filename(conv.title)
                base_filename = f"{date_prefix}{safe_title}_{thread_id[:8]}"
                
                # Save JSON
                if not markdown_only:
                    json_path = json_dir / f"{base_filename}.json"
                    with open(json_path, 'w', encoding='utf-8') as f:
                        json.dump(thread_data, f, ensure_ascii=False, indent=2)
                
                # Save Markdown
                if not json_only:
                    md_content = render_conversation_markdown(conv)
                    md_path = md_dir / f"{base_filename}.md"
                    with open(md_path, 'w', encoding='utf-8') as f:
                        f.write(md_content)
                
                success += 1
                print(f"    ✓ Saved ({len(conv.entries)} turns)")
                
            except Exception as e:
                print(f"    ✗ Error: {e}")
                errors += 1
        
        if not has_more:
            break
        
        offset += len(threads)
    
    return success, errors


# =============================================================================
# Main Entry Point
# =============================================================================

async def main():
    parser = argparse.ArgumentParser(
        description="Export all Perplexity.ai conversations to JSON and Markdown",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Using cookie file (Cookie-Editor JSON export)
  python perplexity-export.py --cookies cookies.json --output ./exports
  
  # Using cookie string
  python perplexity-export.py --cookie-string "__Secure-next-auth.session-token=..." --output ./exports
  
  # JSON only
  python perplexity-export.py --cookies cookies.json --output ./exports --json-only

Cookie Extraction:
  1. Log into perplexity.ai in your browser
  2. Install "Cookie-Editor" extension
  3. Click extension icon → Export → Export as JSON
  4. Save as cookies.json
        """
    )
    
    auth_group = parser.add_mutually_exclusive_group(required=True)
    auth_group.add_argument(
        '--cookies', '-c',
        type=str,
        help='Path to cookies JSON file (Cookie-Editor format)'
    )
    auth_group.add_argument(
        '--cookie-string', '-s',
        type=str,
        help='Cookie string (e.g., "name1=value1; name2=value2")'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='./perplexity-export',
        help='Output directory (default: ./perplexity-export)'
    )
    
    format_group = parser.add_mutually_exclusive_group()
    format_group.add_argument(
        '--json-only',
        action='store_true',
        help='Export only JSON files'
    )
    format_group.add_argument(
        '--markdown-only',
        action='store_true',
        help='Export only Markdown files'
    )
    
    args = parser.parse_args()
    
    # Load cookies
    if args.cookies:
        if not os.path.exists(args.cookies):
            print(f"Error: Cookie file not found: {args.cookies}")
            sys.exit(1)
        cookies = load_cookies_from_json(args.cookies)
    else:
        cookies = parse_cookie_string(args.cookie_string)
    
    if not cookies:
        print("Error: No cookies loaded. Check your cookie file/string.")
        sys.exit(1)
    
    print(f"Loaded {len(cookies)} cookies")
    
    # Check for auth cookies
    auth_cookies = [k for k in cookies if 'session' in k.lower() or 'auth' in k.lower()]
    if not auth_cookies:
        print("Warning: No obvious auth cookies found. Authentication may fail.")
    
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Output directory: {output_dir.absolute()}")
    print()
    
    # Run export
    try:
        async with PerplexityClient(cookies) as client:
            success, errors = await export_all_conversations(
                client,
                output_dir,
                json_only=args.json_only,
                markdown_only=args.markdown_only,
            )
        
        print()
        print("=" * 50)
        print(f"Export complete!")
        print(f"  ✓ Success: {success}")
        print(f"  ✗ Errors:  {errors}")
        print(f"  Output:    {output_dir.absolute()}")
        
    except PermissionError as e:
        print(f"\n✗ {e}")
        print("\nTip: Try re-exporting your cookies from a fresh login.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
