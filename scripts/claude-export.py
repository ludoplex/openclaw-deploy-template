#!/usr/bin/env python3
"""
Claude.ai Conversation Exporter

Exports all conversations from your Claude.ai account using the web interface's
internal API endpoints.

REVERSE-ENGINEERED API ENDPOINTS:
================================
1. List all conversations:
   GET https://claude.ai/api/organizations/{orgId}/chat_conversations
   
2. Get single conversation (full content):
   GET https://claude.ai/api/organizations/{orgId}/chat_conversations/{conversationId}?tree=True&rendering_mode=messages&render_all_tools=true

3. List project conversations:
   GET https://claude.ai/api/organizations/{orgId}/projects/{projectId}/conversations_v2?limit={limit}&offset={offset}

AUTHENTICATION:
===============
- Uses browser session cookies
- Key cookies: 'sessionKey', '__cf_bm', 'lastActiveOrg'
- Organization ID extracted from 'lastActiveOrg' cookie

USAGE:
======
1. Log into claude.ai in your browser
2. Open DevTools (F12) → Application → Cookies → claude.ai
3. Copy the cookie string (or individual cookies)
4. Run this script with the cookies

Examples:
  python claude-export.py --cookie "sessionKey=sk-ant-xxx; __cf_bm=xxx"
  python claude-export.py --cookie-file cookies.txt
  python claude-export.py --cookie "..." --format markdown --output ./exports
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import quote

try:
    import requests
except ImportError:
    print("Error: 'requests' library required. Install with: pip install requests")
    sys.exit(1)


class ClaudeExporter:
    """Export conversations from Claude.ai web interface."""
    
    BASE_URL = "https://claude.ai"
    
    # Model display names for pretty output
    MODEL_NAMES = {
        'claude-3-sonnet-20240229': 'Claude 3 Sonnet',
        'claude-3-opus-20240229': 'Claude 3 Opus',
        'claude-3-haiku-20240307': 'Claude 3 Haiku',
        'claude-3-5-sonnet-20240620': 'Claude 3.5 Sonnet',
        'claude-3-5-haiku-20241022': 'Claude 3.5 Haiku',
        'claude-3-5-sonnet-20241022': 'Claude 3.6 Sonnet',
        'claude-3-7-sonnet-20250219': 'Claude 3.7 Sonnet',
        'claude-sonnet-4-20250514': 'Claude Sonnet 4',
        'claude-opus-4-20250514': 'Claude Opus 4',
        'claude-opus-4-1-20250805': 'Claude Opus 4.1',
        'claude-sonnet-4-5-20250929': 'Claude Sonnet 4.5',
        'claude-haiku-4-5-20251001': 'Claude Haiku 4.5',
        'claude-opus-4-5-20251015': 'Claude Opus 4.5',
        'claude-opus-4-6-20260115': 'Claude Opus 4.6',
    }
    
    def __init__(self, cookie_string: str, org_id: Optional[str] = None):
        """
        Initialize the exporter with session cookies.
        
        Args:
            cookie_string: Cookie string from browser (sessionKey=xxx; ...)
            org_id: Optional organization ID (auto-detected from cookies if not provided)
        """
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Parse and set cookies
        self._set_cookies(cookie_string)
        
        # Get organization ID
        self.org_id = org_id or self._extract_org_id(cookie_string)
        if not self.org_id:
            raise ValueError(
                "Could not detect organization ID. Please provide it with --org-id.\n"
                "Find it in: DevTools → Application → Cookies → lastActiveOrg"
            )
        
        print(f"✓ Organization ID: {self.org_id}")
    
    def _set_cookies(self, cookie_string: str):
        """Parse cookie string and add to session."""
        # Handle different cookie formats
        cookie_string = cookie_string.strip()
        
        # Parse "name=value; name2=value2" format
        for part in cookie_string.split(';'):
            part = part.strip()
            if '=' in part:
                name, value = part.split('=', 1)
                self.session.cookies.set(name.strip(), value.strip(), domain='claude.ai')
    
    def _extract_org_id(self, cookie_string: str) -> Optional[str]:
        """Extract organization ID from cookies."""
        # Look for lastActiveOrg cookie
        match = re.search(r'lastActiveOrg=([a-f0-9-]{36})', cookie_string)
        if match:
            return match.group(1)
        
        # Check session cookies
        org_id = self.session.cookies.get('lastActiveOrg')
        if org_id and re.match(r'^[a-f0-9-]{36}$', org_id):
            return org_id
        
        return None
    
    def _api_request(self, endpoint: str, params: dict = None, retries: int = 3) -> dict:
        """Make an API request with retry logic."""
        url = f"{self.BASE_URL}/api/{endpoint}"
        
        for attempt in range(retries):
            try:
                response = self.session.get(url, params=params, timeout=30)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    raise PermissionError("Authentication failed. Check your cookies.")
                elif response.status_code == 403:
                    raise PermissionError("Access denied. You may not have permission.")
                elif response.status_code == 429:
                    # Rate limited
                    wait_time = min(2 ** attempt * 2, 30)
                    print(f"  Rate limited. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    response.raise_for_status()
                    
            except requests.RequestException as e:
                if attempt == retries - 1:
                    raise
                time.sleep(1 * (attempt + 1))
        
        raise RuntimeError(f"Failed after {retries} attempts")
    
    def list_conversations(self) -> list:
        """
        List all conversations.
        
        API: GET /api/organizations/{orgId}/chat_conversations
        """
        print("Fetching conversation list...")
        endpoint = f"organizations/{self.org_id}/chat_conversations"
        conversations = self._api_request(endpoint)
        print(f"✓ Found {len(conversations)} conversations")
        return conversations
    
    def get_conversation(self, conversation_id: str) -> dict:
        """
        Get full conversation content.
        
        API: GET /api/organizations/{orgId}/chat_conversations/{conversationId}
             ?tree=True&rendering_mode=messages&render_all_tools=true
        """
        endpoint = f"organizations/{self.org_id}/chat_conversations/{conversation_id}"
        params = {
            'tree': 'True',
            'rendering_mode': 'messages',
            'render_all_tools': 'true'
        }
        return self._api_request(endpoint, params)
    
    def list_projects(self) -> list:
        """
        List all projects.
        
        API: GET /api/organizations/{orgId}/projects
        """
        try:
            endpoint = f"organizations/{self.org_id}/projects"
            return self._api_request(endpoint)
        except Exception as e:
            print(f"  Could not list projects: {e}")
            return []
    
    def list_project_conversations(self, project_id: str, limit: int = 1000) -> list:
        """
        List conversations in a project.
        
        API: GET /api/organizations/{orgId}/projects/{projectId}/conversations_v2
        """
        endpoint = f"organizations/{self.org_id}/projects/{project_id}/conversations_v2"
        params = {'limit': limit, 'offset': 0}
        result = self._api_request(endpoint, params)
        
        # Handle different response formats
        if isinstance(result, dict) and 'data' in result:
            return result['data']
        return result if isinstance(result, list) else []
    
    def _get_current_branch(self, data: dict) -> list:
        """Reconstruct the current branch from the message tree."""
        if 'chat_messages' not in data or 'current_leaf_message_uuid' not in data:
            return data.get('chat_messages', [])
        
        # Create message map
        message_map = {msg['uuid']: msg for msg in data['chat_messages']}
        
        # Trace from leaf to root
        branch = []
        current_uuid = data.get('current_leaf_message_uuid')
        
        while current_uuid and current_uuid in message_map:
            message = message_map[current_uuid]
            branch.insert(0, message)
            current_uuid = message.get('parent_message_uuid')
        
        return branch
    
    def convert_to_markdown(self, data: dict, include_metadata: bool = True) -> str:
        """Convert conversation to Markdown format."""
        lines = []
        
        name = data.get('name', 'Untitled Conversation')
        lines.append(f"# {name}\n")
        
        if include_metadata:
            created = data.get('created_at', '')
            updated = data.get('updated_at', '')
            model = data.get('model', 'Unknown')
            model_name = self.MODEL_NAMES.get(model, model)
            
            lines.append(f"**Created:** {created}")
            lines.append(f"**Updated:** {updated}")
            lines.append(f"**Model:** {model_name}\n")
            lines.append("---\n")
        
        # Get current branch messages
        messages = self._get_current_branch(data)
        
        for message in messages:
            sender = message.get('sender', 'unknown')
            sender_label = '**You**' if sender == 'human' else '**Claude**'
            lines.append(f"{sender_label}:\n")
            
            # Extract text content
            content = message.get('content', [])
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict):
                        # Handle thinking blocks
                        if item.get('type') == 'thinking' and item.get('thinking'):
                            thinking = item['thinking']
                            if 'truncated' not in thinking:
                                lines.append(f"*Thinking:*\n```\n{thinking}\n```\n")
                        # Handle text
                        elif item.get('text'):
                            lines.append(f"{item['text']}\n")
                        # Handle tool use
                        elif item.get('type') == 'tool_use':
                            tool_input = item.get('input', {})
                            lines.append(f"*Tool Use:*\n```json\n{json.dumps(tool_input, indent=2)}\n```\n")
            elif message.get('text'):
                lines.append(f"{message['text']}\n")
            
            # Handle attachments
            attachments = message.get('attachments', [])
            if attachments:
                lines.append("\n**Attachments:**")
                for att in attachments:
                    name = att.get('file_name', 'Attachment')
                    file_type = att.get('file_type', 'file')
                    lines.append(f"- {name} ({file_type})")
                lines.append("")
            
            if include_metadata and message.get('created_at'):
                lines.append(f"*{message['created_at']}*\n")
            
            lines.append("---\n")
        
        return '\n'.join(lines)
    
    def sanitize_filename(self, name: str) -> str:
        """Create a safe filename from conversation name."""
        if not name:
            return 'untitled_conversation'
        
        # Remove/replace invalid characters
        safe = re.sub(r'[<>:"/\\|?*]', '_', name)
        safe = re.sub(r'\s+', '_', safe)
        safe = re.sub(r'_+', '_', safe)
        safe = safe.strip('_')
        
        return safe[:100] if safe else 'untitled_conversation'
    
    def export_all(self, output_dir: str, format: str = 'both', 
                   include_projects: bool = True, delay: float = 0.5):
        """
        Export all conversations.
        
        Args:
            output_dir: Directory to save exports
            format: 'json', 'markdown', or 'both'
            include_projects: Also export project conversations
            delay: Delay between API calls (seconds)
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        if format in ('json', 'both'):
            (output_path / 'json').mkdir(exist_ok=True)
        if format in ('markdown', 'both'):
            (output_path / 'markdown').mkdir(exist_ok=True)
        
        # Get all conversations
        conversations = self.list_conversations()
        
        # Track stats
        total = len(conversations)
        success = 0
        failed = 0
        failed_names = []
        
        print(f"\nExporting {total} conversations...")
        
        for i, conv in enumerate(conversations, 1):
            conv_id = conv.get('uuid')
            conv_name = conv.get('name', 'Untitled')
            
            print(f"  [{i}/{total}] {conv_name[:50]}...")
            
            try:
                # Fetch full conversation
                full_conv = self.get_conversation(conv_id)
                
                # Generate filename
                safe_name = self.sanitize_filename(conv_name)
                filename = f"{safe_name}_{conv_id[:8]}"
                
                # Export JSON
                if format in ('json', 'both'):
                    json_path = output_path / 'json' / f"{filename}.json"
                    with open(json_path, 'w', encoding='utf-8') as f:
                        json.dump(full_conv, f, indent=2, ensure_ascii=False)
                
                # Export Markdown
                if format in ('markdown', 'both'):
                    md_content = self.convert_to_markdown(full_conv)
                    md_path = output_path / 'markdown' / f"{filename}.md"
                    with open(md_path, 'w', encoding='utf-8') as f:
                        f.write(md_content)
                
                success += 1
                
            except Exception as e:
                print(f"    ✗ Error: {e}")
                failed += 1
                failed_names.append(conv_name)
            
            # Rate limiting
            if i < total:
                time.sleep(delay)
        
        # Export projects if requested
        if include_projects:
            print("\nChecking for projects...")
            projects = self.list_projects()
            
            if projects:
                projects_path = output_path / 'projects'
                projects_path.mkdir(exist_ok=True)
                
                for project in projects:
                    project_id = project.get('uuid')
                    project_name = project.get('name', 'Untitled Project')
                    
                    print(f"\nProject: {project_name}")
                    
                    project_convs = self.list_project_conversations(project_id)
                    if not project_convs:
                        print("  No conversations in this project")
                        continue
                    
                    # Create project directory
                    safe_project = self.sanitize_filename(project_name)
                    project_dir = projects_path / safe_project
                    project_dir.mkdir(exist_ok=True)
                    
                    for conv in project_convs:
                        conv_id = conv.get('uuid')
                        conv_name = conv.get('name', 'Untitled')
                        
                        try:
                            full_conv = self.get_conversation(conv_id)
                            safe_name = self.sanitize_filename(conv_name)
                            filename = f"{safe_name}_{conv_id[:8]}"
                            
                            if format in ('json', 'both'):
                                with open(project_dir / f"{filename}.json", 'w', encoding='utf-8') as f:
                                    json.dump(full_conv, f, indent=2, ensure_ascii=False)
                            
                            if format in ('markdown', 'both'):
                                md_content = self.convert_to_markdown(full_conv)
                                with open(project_dir / f"{filename}.md", 'w', encoding='utf-8') as f:
                                    f.write(md_content)
                            
                            success += 1
                            
                        except Exception as e:
                            print(f"    ✗ {conv_name}: {e}")
                            failed += 1
                        
                        time.sleep(delay)
        
        # Create summary
        summary = {
            'export_date': datetime.now().isoformat(),
            'organization_id': self.org_id,
            'total_conversations': total,
            'successful_exports': success,
            'failed_exports': failed,
            'failed_conversations': failed_names,
            'format': format
        }
        
        with open(output_path / 'export_summary.json', 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        # Print summary
        print(f"\n{'='*50}")
        print(f"Export Complete!")
        print(f"{'='*50}")
        print(f"  Successful: {success}")
        print(f"  Failed: {failed}")
        print(f"  Output: {output_path.absolute()}")
        
        if failed_names:
            print(f"\nFailed conversations:")
            for name in failed_names[:10]:
                print(f"  - {name}")
            if len(failed_names) > 10:
                print(f"  ... and {len(failed_names) - 10} more")


def main():
    parser = argparse.ArgumentParser(
        description='Export Claude.ai conversations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --cookie "sessionKey=sk-ant-xxx; lastActiveOrg=xxx"
  %(prog)s --cookie-file cookies.txt --format markdown
  %(prog)s --cookie "..." --output ./my-exports --format both

How to get cookies:
  1. Log into claude.ai
  2. Open DevTools (F12) -> Application -> Cookies -> claude.ai
  3. Copy the cookie values (at minimum: sessionKey, lastActiveOrg)
"""
    )
    
    cookie_group = parser.add_mutually_exclusive_group(required=True)
    cookie_group.add_argument(
        '--cookie', '-c',
        help='Cookie string (e.g., "sessionKey=xxx; lastActiveOrg=xxx")'
    )
    cookie_group.add_argument(
        '--cookie-file', '-f',
        help='File containing cookie string'
    )
    
    parser.add_argument(
        '--org-id', '-o',
        help='Organization ID (auto-detected from cookies if not provided)'
    )
    parser.add_argument(
        '--output', '-d',
        default='./claude-exports',
        help='Output directory (default: ./claude-exports)'
    )
    parser.add_argument(
        '--format', '-t',
        choices=['json', 'markdown', 'both'],
        default='both',
        help='Export format (default: both)'
    )
    parser.add_argument(
        '--no-projects',
        action='store_true',
        help='Skip exporting project conversations'
    )
    parser.add_argument(
        '--delay',
        type=float,
        default=0.5,
        help='Delay between API calls in seconds (default: 0.5)'
    )
    parser.add_argument(
        '--list-only',
        action='store_true',
        help='Only list conversations, do not export'
    )
    
    args = parser.parse_args()
    
    # Get cookie string
    if args.cookie_file:
        with open(args.cookie_file, 'r') as f:
            cookie_string = f.read().strip()
    else:
        cookie_string = args.cookie
    
    try:
        exporter = ClaudeExporter(cookie_string, args.org_id)
        
        if args.list_only:
            # Just list conversations
            conversations = exporter.list_conversations()
            print(f"\nConversations ({len(conversations)}):")
            for conv in conversations:
                name = conv.get('name', 'Untitled')
                model = conv.get('model', 'Unknown')
                created = conv.get('created_at', '')[:10]
                print(f"  [{created}] {name} ({model})")
        else:
            # Full export
            exporter.export_all(
                output_dir=args.output,
                format=args.format,
                include_projects=not args.no_projects,
                delay=args.delay
            )
            
    except PermissionError as e:
        print(f"\n✗ Authentication Error: {e}")
        print("\nMake sure you're logged into claude.ai and copied the cookies correctly.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
