#!/usr/bin/env python3
"""
ChatGPT Conversation Exporter

Exports all conversations from ChatGPT to JSON and/or Markdown format.
Uses the unofficial ChatGPT backend API (same endpoints as the web interface).

AUTHENTICATION:
---------------
You need to provide an access token. Get it from:
1. Go to https://chatgpt.com (or https://chat.openai.com)
2. Open DevTools (F12) → Network tab
3. Refresh the page
4. Find a request to "session" or any backend-api request
5. Copy the Authorization header value (the part after "Bearer ")

Alternatively, visit: https://chatgpt.com/api/auth/session
and copy the "accessToken" value from the JSON response.

API STRUCTURE (Documented):
---------------------------
Base URL: https://chatgpt.com/backend-api

Endpoints:
  GET /conversations?offset={offset}&limit={limit}
      - Lists conversations with pagination
      - Returns: { items: [...], total: int, limit: int, offset: int }

  GET /conversation/{id}
      - Fetches full conversation with message tree
      - Returns: { title, create_time, update_time, mapping: {...}, current_node }

  GET /api/auth/session
      - Returns session info including accessToken
      - Response: { accessToken, user: {...}, expires }

  GET /files/{id}/download
      - Downloads file assets (images, etc.)
      - Returns: { status, download_url, file_name }

  GET /accounts/check/v4-2023-04-27
      - Returns account info for team/workspace accounts

Authentication:
  - Bearer token in Authorization header
  - Same token in X-Authorization header (for CORS)
  - For team accounts: Chatgpt-Account-Id header

Message Structure:
  - mapping: dict of { node_id: ConversationNode }
  - ConversationNode: { id, parent, children, message }
  - message: { author: {role}, content: {content_type, parts}, create_time, ... }
  - author.role: "system" | "user" | "assistant" | "tool"
  - content_type: "text" | "code" | "multimodal_text" | "execution_output" | etc.

Usage:
------
  python chatgpt-export.py --token "YOUR_ACCESS_TOKEN" --output ./export
  python chatgpt-export.py --token-file ~/.chatgpt-token --format both
  python chatgpt-export.py --help

Requirements:
-------------
  pip install httpx rich

Author: OpenClaw Subagent
Date: 2026-02-08
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

try:
    import httpx
except ImportError:
    print("Error: httpx is required. Install with: pip install httpx")
    sys.exit(1)

try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Note: Install 'rich' for better output: pip install rich")


# =============================================================================
# Configuration
# =============================================================================

BASE_URLS = {
    "chatgpt.com": "https://chatgpt.com",
    "chat.openai.com": "https://chat.openai.com",
}

DEFAULT_BASE_URL = "https://chatgpt.com"
API_PATH = "/backend-api"
SESSION_PATH = "/api/auth/session"

# Model slug to friendly name mapping
MODEL_MAPPING = {
    "text-davinci-002-render-sha": "GPT-3.5",
    "text-davinci-002-render-paid": "GPT-3.5",
    "text-davinci-002-browse": "GPT-3.5 (Browse)",
    "gpt-4": "GPT-4",
    "gpt-4-browsing": "GPT-4 (Browse)",
    "gpt-4o": "GPT-4o",
    "gpt-4o-mini": "GPT-4o Mini",
    "o1-preview": "o1-preview",
    "o1-mini": "o1-mini",
}


# =============================================================================
# Console Output Helpers
# =============================================================================

if RICH_AVAILABLE:
    console = Console()
    
    def info(msg: str):
        console.print(f"[blue]ℹ[/blue] {msg}")
    
    def success(msg: str):
        console.print(f"[green]✓[/green] {msg}")
    
    def warning(msg: str):
        console.print(f"[yellow]⚠[/yellow] {msg}")
    
    def error(msg: str):
        console.print(f"[red]✗[/red] {msg}")
else:
    def info(msg: str):
        print(f"[INFO] {msg}")
    
    def success(msg: str):
        print(f"[OK] {msg}")
    
    def warning(msg: str):
        print(f"[WARN] {msg}")
    
    def error(msg: str):
        print(f"[ERROR] {msg}")


# =============================================================================
# ChatGPT API Client
# =============================================================================

class ChatGPTClient:
    """
    Client for ChatGPT's unofficial backend API.
    
    The API uses:
    - Bearer token authentication (from session)
    - JSON responses
    - Pagination for conversation lists
    - Tree-structured message history
    """
    
    def __init__(
        self,
        access_token: str,
        base_url: str = DEFAULT_BASE_URL,
        account_id: Optional[str] = None,
        timeout: float = 60.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_url = f"{self.base_url}{API_PATH}"
        self.access_token = access_token
        self.account_id = account_id
        self.timeout = timeout
        
        # Build headers
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }
        
        if account_id:
            self.headers["Chatgpt-Account-Id"] = account_id
        
        self._client: Optional[httpx.AsyncClient] = None
    
    async def __aenter__(self):
        self._client = httpx.AsyncClient(
            headers=self.headers,
            timeout=self.timeout,
            follow_redirects=True,
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()
    
    async def _get(self, endpoint: str, params: Optional[dict] = None) -> dict:
        """Make GET request to API endpoint."""
        url = f"{self.api_url}{endpoint}"
        response = await self._client.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    async def get_conversations(
        self,
        offset: int = 0,
        limit: int = 100,
    ) -> dict:
        """
        List conversations with pagination.
        
        GET /backend-api/conversations?offset={offset}&limit={limit}
        
        Returns:
            {
                "items": [{"id": str, "title": str, "create_time": float}, ...],
                "total": int,
                "limit": int,
                "offset": int,
                "has_missing_conversations": bool
            }
        """
        return await self._get("/conversations", {"offset": offset, "limit": limit})
    
    async def get_all_conversations(
        self,
        max_conversations: int = 10000,
        batch_size: int = 100,
        progress_callback: Optional[callable] = None,
    ) -> list[dict]:
        """
        Fetch all conversations with pagination.
        
        Args:
            max_conversations: Maximum number of conversations to fetch
            batch_size: Number of conversations per API call
            progress_callback: Optional callback(fetched, total) for progress
        
        Returns:
            List of conversation metadata dicts
        """
        all_conversations = []
        offset = 0
        total = None
        
        while True:
            result = await self.get_conversations(offset=offset, limit=batch_size)
            items = result.get("items", [])
            
            if not items:
                break
            
            all_conversations.extend(items)
            
            # Update total if available
            if total is None and result.get("total"):
                total = result["total"]
            
            # Progress callback
            if progress_callback:
                progress_callback(len(all_conversations), total or len(all_conversations))
            
            # Check if we've got everything
            if len(items) < batch_size:
                break
            
            if len(all_conversations) >= max_conversations:
                break
            
            if total and offset + batch_size >= total:
                break
            
            offset += batch_size
        
        return all_conversations[:max_conversations]
    
    async def get_conversation(self, conversation_id: str) -> dict:
        """
        Fetch full conversation with message tree.
        
        GET /backend-api/conversation/{id}
        
        Returns:
            {
                "title": str,
                "create_time": float,
                "update_time": float,
                "mapping": {node_id: ConversationNode, ...},
                "current_node": str,
                "is_archived": bool,
                "moderation_results": []
            }
        """
        return await self._get(f"/conversation/{conversation_id}")
    
    async def download_file(self, file_id: str) -> Optional[dict]:
        """
        Get download URL for a file asset.
        
        GET /backend-api/files/{id}/download
        
        Returns:
            {
                "status": "success",
                "download_url": str,
                "file_name": str,
                "creation_time": str
            }
        """
        try:
            return await self._get(f"/files/{file_id}/download")
        except httpx.HTTPStatusError:
            return None


# =============================================================================
# Conversation Processing
# =============================================================================

def extract_messages_from_tree(
    mapping: dict[str, dict],
    current_node: str,
) -> list[dict]:
    """
    Extract ordered list of messages from the conversation tree.
    
    The mapping is a dict of node_id -> ConversationNode where each node has:
    - id: str
    - parent: Optional[str]
    - children: list[str]
    - message: Optional[MessageDict]
    
    We traverse from current_node back to root, collecting messages.
    """
    messages = []
    node_id = current_node
    
    while node_id:
        node = mapping.get(node_id)
        if not node:
            break
        
        message = node.get("message")
        if message:
            author_role = message.get("author", {}).get("role", "unknown")
            content = message.get("content", {})
            content_type = content.get("content_type", "text")
            
            # Skip system messages and context messages
            if author_role == "system":
                node_id = node.get("parent")
                continue
            
            if content_type in ("user_editable_context", "model_editable_context"):
                node_id = node.get("parent")
                continue
            
            # Extract text content
            text = ""
            if content_type == "text":
                parts = content.get("parts", [])
                text = "\n".join(str(p) for p in parts if isinstance(p, str))
            elif content_type == "code":
                text = content.get("text", "")
            elif content_type == "execution_output":
                text = content.get("text", "")
            elif content_type == "multimodal_text":
                parts = content.get("parts", [])
                text_parts = [str(p) for p in parts if isinstance(p, str)]
                text = "\n".join(text_parts)
                # Note: Image assets would need separate handling
            elif content_type == "tether_quote":
                text = f"[Quote from {content.get('title', 'source')}]\n{content.get('text', '')}"
            elif content_type == "tether_browsing_display":
                text = content.get("result", "") or content.get("summary", "")
            
            messages.insert(0, {
                "role": author_role,
                "content": text,
                "content_type": content_type,
                "create_time": message.get("create_time"),
                "id": message.get("id"),
                "metadata": message.get("metadata", {}),
            })
        
        node_id = node.get("parent")
    
    return messages


def get_model_from_conversation(mapping: dict[str, dict]) -> tuple[str, str]:
    """Extract model slug and friendly name from conversation."""
    for node in mapping.values():
        message = node.get("message", {})
        metadata = message.get("metadata", {})
        model_slug = metadata.get("model_slug")
        if model_slug:
            friendly_name = MODEL_MAPPING.get(model_slug, model_slug)
            return model_slug, friendly_name
    return "", "Unknown"


def format_timestamp(ts: Optional[float]) -> str:
    """Format Unix timestamp to readable string."""
    if not ts:
        return ""
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


# =============================================================================
# Export Functions
# =============================================================================

def conversation_to_markdown(
    conversation_data: dict,
    include_metadata: bool = True,
) -> str:
    """Convert conversation to Markdown format."""
    title = conversation_data.get("title", "Untitled Conversation")
    create_time = conversation_data.get("create_time")
    update_time = conversation_data.get("update_time")
    mapping = conversation_data.get("mapping", {})
    current_node = conversation_data.get("current_node", "")
    
    messages = extract_messages_from_tree(mapping, current_node)
    model_slug, model_name = get_model_from_conversation(mapping)
    
    lines = []
    
    # YAML frontmatter
    if include_metadata:
        lines.append("---")
        lines.append(f"title: {json.dumps(title)}")
        lines.append(f"model: {model_name}")
        if create_time:
            lines.append(f"created: {format_timestamp(create_time)}")
        if update_time:
            lines.append(f"updated: {format_timestamp(update_time)}")
        lines.append(f"source: ChatGPT")
        lines.append("---")
        lines.append("")
    
    # Title
    lines.append(f"# {title}")
    lines.append("")
    
    # Messages
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        
        if role == "user":
            lines.append("## User")
        elif role == "assistant":
            lines.append("## Assistant")
        elif role == "tool":
            tool_name = msg.get("metadata", {}).get("name", "Tool")
            lines.append(f"## Tool ({tool_name})")
        else:
            lines.append(f"## {role.title()}")
        
        lines.append("")
        lines.append(content)
        lines.append("")
    
    return "\n".join(lines)


def sanitize_filename(name: str, max_length: int = 100) -> str:
    """Sanitize string for use as filename."""
    # Remove or replace problematic characters
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    name = re.sub(r'\s+', ' ', name).strip()
    name = name[:max_length]
    return name or "untitled"


async def export_conversations(
    client: ChatGPTClient,
    output_dir: Path,
    export_format: str = "both",  # "json", "markdown", or "both"
    max_conversations: Optional[int] = None,
    include_metadata: bool = True,
) -> dict:
    """
    Export all conversations to files.
    
    Args:
        client: ChatGPTClient instance
        output_dir: Directory to save exports
        export_format: "json", "markdown", or "both"
        max_conversations: Limit number of conversations (None = all)
        include_metadata: Include YAML frontmatter in Markdown
    
    Returns:
        Summary dict with counts and any errors
    """
    output_dir = Path(output_dir)
    json_dir = output_dir / "json"
    md_dir = output_dir / "markdown"
    
    # Create directories
    output_dir.mkdir(parents=True, exist_ok=True)
    if export_format in ("json", "both"):
        json_dir.mkdir(exist_ok=True)
    if export_format in ("markdown", "both"):
        md_dir.mkdir(exist_ok=True)
    
    # Fetch conversation list
    info("Fetching conversation list...")
    
    if RICH_AVAILABLE:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
        ) as progress:
            list_task = progress.add_task("Listing conversations...", total=None)
            
            def update_progress(fetched, total):
                progress.update(list_task, completed=fetched, total=total)
            
            conversations = await client.get_all_conversations(
                max_conversations=max_conversations or 10000,
                progress_callback=update_progress,
            )
    else:
        conversations = await client.get_all_conversations(
            max_conversations=max_conversations or 10000,
        )
    
    total_count = len(conversations)
    success(f"Found {total_count} conversations")
    
    if not conversations:
        warning("No conversations found to export")
        return {"total": 0, "exported": 0, "errors": []}
    
    # Export each conversation
    exported = 0
    errors = []
    all_conversations_data = []
    
    info("Exporting conversations...")
    
    if RICH_AVAILABLE:
        progress_ctx = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TextColumn("[cyan]{task.fields[current]}"),
            console=console,
        )
    else:
        progress_ctx = None
    
    async def export_one(conv_meta: dict, task_id=None):
        nonlocal exported
        conv_id = conv_meta["id"]
        title = conv_meta.get("title", "Untitled")
        
        try:
            # Fetch full conversation
            conv_data = await client.get_conversation(conv_id)
            conv_data["id"] = conv_id  # Ensure ID is included
            all_conversations_data.append(conv_data)
            
            # Generate filename
            create_time = conv_data.get("create_time")
            date_prefix = ""
            if create_time:
                date_prefix = datetime.fromtimestamp(create_time).strftime("%Y-%m-%d_")
            
            safe_title = sanitize_filename(title)
            filename_base = f"{date_prefix}{safe_title}_{conv_id[:8]}"
            
            # Export JSON
            if export_format in ("json", "both"):
                json_path = json_dir / f"{filename_base}.json"
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(conv_data, f, indent=2, ensure_ascii=False)
            
            # Export Markdown
            if export_format in ("markdown", "both"):
                md_content = conversation_to_markdown(conv_data, include_metadata)
                md_path = md_dir / f"{filename_base}.md"
                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(md_content)
            
            exported += 1
            
            if progress_ctx and task_id is not None:
                progress_ctx.update(task_id, advance=1, current=f"[{exported}/{total_count}] {title[:40]}")
            
        except Exception as e:
            error_msg = f"Failed to export '{title}' ({conv_id}): {e}"
            errors.append(error_msg)
            if not RICH_AVAILABLE:
                error(error_msg)
    
    if RICH_AVAILABLE:
        with progress_ctx:
            task = progress_ctx.add_task(
                "Exporting...",
                total=total_count,
                current=""
            )
            for conv_meta in conversations:
                await export_one(conv_meta, task)
    else:
        for i, conv_meta in enumerate(conversations):
            print(f"  [{i+1}/{total_count}] {conv_meta.get('title', 'Untitled')[:50]}")
            await export_one(conv_meta)
    
    # Save combined JSON
    combined_path = output_dir / "all_conversations.json"
    with open(combined_path, "w", encoding="utf-8") as f:
        json.dump({
            "export_time": datetime.now().isoformat(),
            "total_conversations": len(all_conversations_data),
            "conversations": all_conversations_data,
        }, f, indent=2, ensure_ascii=False)
    
    success(f"Exported {exported}/{total_count} conversations to {output_dir}")
    
    if errors:
        warning(f"{len(errors)} errors occurred during export")
        error_log_path = output_dir / "export_errors.log"
        with open(error_log_path, "w", encoding="utf-8") as f:
            f.write("\n".join(errors))
        info(f"Error log saved to {error_log_path}")
    
    return {
        "total": total_count,
        "exported": exported,
        "errors": errors,
        "output_dir": str(output_dir),
    }


# =============================================================================
# CLI
# =============================================================================

def parse_args():
    parser = argparse.ArgumentParser(
        description="Export ChatGPT conversations to JSON and/or Markdown",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --token "eyJhbG..." --output ./export
  %(prog)s --token-file ~/.chatgpt-token --format markdown
  %(prog)s --token "$TOKEN" --format both --max 100

How to get your access token:
  1. Go to https://chatgpt.com
  2. Open DevTools (F12) -> Console
  3. Run: await fetch('/api/auth/session').then(r=>r.json()).then(d=>console.log(d.accessToken))
  4. Copy the token string
        """
    )
    
    # Token options (mutually exclusive)
    token_group = parser.add_mutually_exclusive_group(required=True)
    token_group.add_argument(
        "--token", "-t",
        help="ChatGPT access token (JWT)"
    )
    token_group.add_argument(
        "--token-file", "-f",
        help="File containing access token"
    )
    
    # Output options
    parser.add_argument(
        "--output", "-o",
        default="./chatgpt-export",
        help="Output directory (default: ./chatgpt-export)"
    )
    parser.add_argument(
        "--format",
        choices=["json", "markdown", "both"],
        default="both",
        help="Export format (default: both)"
    )
    
    # Limits
    parser.add_argument(
        "--max", "-m",
        type=int,
        default=None,
        help="Maximum number of conversations to export"
    )
    
    # Advanced options
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"Base URL (default: {DEFAULT_BASE_URL})"
    )
    parser.add_argument(
        "--account-id",
        help="Team/workspace account ID (for team accounts)"
    )
    parser.add_argument(
        "--no-metadata",
        action="store_true",
        help="Omit YAML frontmatter in Markdown files"
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=60.0,
        help="Request timeout in seconds (default: 60)"
    )
    
    return parser.parse_args()


async def main():
    args = parse_args()
    
    # Get access token
    if args.token:
        access_token = args.token
    else:
        token_path = Path(args.token_file).expanduser()
        if not token_path.exists():
            error(f"Token file not found: {token_path}")
            sys.exit(1)
        access_token = token_path.read_text().strip()
    
    if not access_token:
        error("Access token is empty")
        sys.exit(1)
    
    # Validate token format (should be JWT)
    if not access_token.startswith("eyJ"):
        warning("Token doesn't look like a JWT (should start with 'eyJ')")
    
    info(f"Using base URL: {args.base_url}")
    info(f"Output directory: {args.output}")
    info(f"Format: {args.format}")
    
    # Create client and export
    try:
        async with ChatGPTClient(
            access_token=access_token,
            base_url=args.base_url,
            account_id=args.account_id,
            timeout=args.timeout,
        ) as client:
            result = await export_conversations(
                client=client,
                output_dir=Path(args.output),
                export_format=args.format,
                max_conversations=args.max,
                include_metadata=not args.no_metadata,
            )
        
        # Print summary
        if RICH_AVAILABLE:
            table = Table(title="Export Summary")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            table.add_row("Total Conversations", str(result["total"]))
            table.add_row("Successfully Exported", str(result["exported"]))
            table.add_row("Errors", str(len(result["errors"])))
            table.add_row("Output Directory", result["output_dir"])
            console.print(table)
        else:
            print("\n=== Export Summary ===")
            print(f"Total: {result['total']}")
            print(f"Exported: {result['exported']}")
            print(f"Errors: {len(result['errors'])}")
            print(f"Output: {result['output_dir']}")
        
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            error("Authentication failed. Your token may be expired.")
            error("Get a new token from: https://chatgpt.com/api/auth/session")
        elif e.response.status_code == 403:
            error("Access forbidden. Check your token and account permissions.")
        else:
            error(f"HTTP error: {e.response.status_code} - {e.response.text}")
        sys.exit(1)
    except httpx.RequestError as e:
        error(f"Request failed: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        warning("\nExport interrupted by user")
        sys.exit(130)


if __name__ == "__main__":
    asyncio.run(main())
