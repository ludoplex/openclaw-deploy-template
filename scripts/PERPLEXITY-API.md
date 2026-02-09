# Perplexity.ai Internal API Documentation

**Reverse-engineered: 2026-02-08**

This document describes the internal (undocumented) API endpoints used by Perplexity.ai's web interface for conversation history. These endpoints are **not part of their public API** and may change without notice.

## Authentication

Perplexity uses **cookie-based authentication** via NextAuth.js.

### Key Cookies

| Cookie Name | Purpose |
|-------------|---------|
| `__Secure-next-auth.session-token` | Primary session token (JWT) |
| `__Secure-next-auth.callback-url` | Callback URL after auth |
| `__Secure-next-auth.csrf-token` | CSRF protection token |

### How to Extract Cookies

1. Log into [perplexity.ai](https://perplexity.ai) in your browser
2. Open DevTools (F12)
3. Go to: Application → Cookies → https://www.perplexity.ai
4. Copy all session-related cookies

**Recommended**: Use the "Cookie-Editor" browser extension:
- Install from [Chrome Web Store](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) or [Firefox Add-ons](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/)
- Click extension icon → Export → Export as JSON
- Use the exported JSON file with the export script

## API Endpoints

### Base URL
```
https://www.perplexity.ai/rest
```

### Required Headers
```http
Accept: application/json, text/plain, */*
Accept-Language: en-US,en;q=0.9
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
Referer: https://www.perplexity.ai/library
Origin: https://www.perplexity.ai
Cookie: <your session cookies>
```

---

## Endpoints

### 1. List Threads (Conversation List)

**Endpoint:** `GET /rest/thread/list_recent`

**Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `limit` | int | 50 | Number of threads to return |
| `offset` | int | 0 | Pagination offset |

**Response:**
```json
{
  "threads": [
    {
      "uuid": "abc123-...",
      "thread_uuid": "abc123-...",
      "thread_title": "How to make sourdough bread",
      "query_str": "How do I make sourdough bread?",
      "updated_datetime": "2026-02-08T10:30:00Z",
      "thread_url_slug": "how-to-make-sourdough-bread-abc123",
      "display_model": "claude-3.5-sonnet",
      "mode": "concise",
      ...
    }
  ],
  "has_next_page": true
}
```

**Notes:**
- Response format may be a simple array `[...]` instead of `{"threads": [...]}`
- Pagination is offset-based

---

### 2. Get Thread (Full Conversation)

**Endpoint:** `GET /rest/thread/{thread_id}`

**Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `limit` | int | 100 | Max entries per page |
| `cursor` | string | null | Pagination cursor (from previous response) |

**Response:**
```json
{
  "status": "ok",
  "entries": [
    {
      "uuid": "entry-uuid-123",
      "context_uuid": "thread-uuid-abc",
      "thread_title": "How to make sourdough bread",
      "query_str": "How do I make sourdough bread?",
      "display_model": "claude-3.5-sonnet",
      "mode": "concise",
      "updated_datetime": "2026-02-08T10:30:00Z",
      "entry_updated_datetime": "2026-02-08T10:30:05Z",
      "thread_url_slug": "how-to-make-sourdough-bread-abc123",
      "blocks": [...],
      "sources": {...},
      ...
    }
  ],
  "has_next_page": false,
  "next_cursor": null
}
```

---

## Data Structures

### Entry Blocks

Each entry contains a `blocks` array with different content types:

#### Ask Text Block (Answer)
```json
{
  "intended_usage": "ask_text",
  "markdown_block": {
    "progress": "completed",
    "chunks": ["...", "..."],
    "answer": "Full markdown answer text..."
  }
}
```

#### Sources Block
```json
{
  "intended_usage": "sources_answer_mode",
  "sources_mode_block": {
    "answer_mode_type": "sources",
    "progress": "completed",
    "result_count": 5,
    "rows": [
      {
        "web_result": {
          "name": "Source Title",
          "url": "https://example.com/article",
          "snippet": "Preview text..."
        },
        "citation": 1
      }
    ]
  }
}
```

#### Image Block
```json
{
  "intended_usage": "image_answer_mode",
  "image_mode_block": {
    "answer_mode_type": "image",
    "media_items": [
      {
        "name": "Image description",
        "url": "https://source.com/page",
        "image": "https://cdn.example.com/image.jpg",
        "image_width": 800,
        "image_height": 600
      }
    ]
  }
}
```

#### Video Block
```json
{
  "intended_usage": "video_answer_mode",
  "video_mode_block": {
    "answer_mode_type": "video",
    "media_items": [
      {
        "name": "Video title",
        "url": "https://youtube.com/watch?v=..."
      }
    ]
  }
}
```

#### Pro Search Steps Block
```json
{
  "intended_usage": "plan",
  "plan_block": {
    "progress": "completed",
    "goals": [
      {
        "id": "goal-1",
        "description": "Find information about X",
        "final": true,
        "todo_task_status": "completed"
      }
    ],
    "steps": [...]
  }
}
```

---

## Rate Limits

- **Built-in export**: Rate limited (triggers 429 errors with frequent use)
- **API requests**: Approximately 1 request/second recommended
- **429 response**: Wait 60+ seconds before retry

---

## Other Endpoints (Observed)

These additional endpoints were observed but not fully documented:

| Endpoint | Description |
|----------|-------------|
| `GET /rest/user/settings` | User preferences/settings |
| `GET /rest/collections` | User's collection/folders |
| `POST /rest/thread/{id}/bookmark` | Bookmark a thread |
| `DELETE /rest/thread/{id}` | Delete a thread |
| `GET /rest/search_focus` | Available search focus modes |

---

## Usage Example

```python
import httpx

cookies = {
    "__Secure-next-auth.session-token": "your-token-here"
}

headers = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 ...",
    "Cookie": "; ".join(f"{k}={v}" for k, v in cookies.items())
}

# List threads
async with httpx.AsyncClient(headers=headers) as client:
    resp = await client.get(
        "https://www.perplexity.ai/rest/thread/list_recent",
        params={"limit": 50, "offset": 0}
    )
    threads = resp.json()
    
    # Get full thread
    thread_id = threads[0]["uuid"]
    resp = await client.get(
        f"https://www.perplexity.ai/rest/thread/{thread_id}",
        params={"limit": 100}
    )
    full_thread = resp.json()
```

---

## Disclaimer

This documentation is based on reverse engineering and may be incomplete or outdated. Use at your own risk. Perplexity may block or rate-limit automated access.

For official API access, see: https://docs.perplexity.ai/
