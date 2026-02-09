# ChatGPT Unofficial Backend API Documentation

This document describes the unofficial ChatGPT backend API used by the web interface.
Reverse-engineered from browser network traffic and open-source projects.

## Base URLs

| Domain | API Base |
|--------|----------|
| chatgpt.com | `https://chatgpt.com/backend-api` |
| chat.openai.com | `https://chat.openai.com/backend-api` |

## Authentication

### Obtaining Access Token

1. **Via Session Endpoint:**
   ```
   GET /api/auth/session
   ```
   Response:
   ```json
   {
     "accessToken": "eyJhbGciOiJSUzI1NiIsInR5cCI...",
     "user": {
       "id": "user-xxxx",
       "name": "John Doe",
       "email": "john@example.com",
       "image": "https://...",
       "picture": "https://...",
       "mfa": false
     },
     "expires": "2024-03-01T12:00:00.000Z",
     "authProvider": "auth0"
   }
   ```

2. **Via Browser Console:**
   ```javascript
   await fetch('/api/auth/session').then(r=>r.json()).then(d=>console.log(d.accessToken))
   ```

3. **Via DevTools Network Tab:**
   - Open DevTools (F12) → Network
   - Filter by "backend-api" or "auth"
   - Find `Authorization: Bearer <token>` header

### Request Headers

```http
Authorization: Bearer <access_token>
X-Authorization: Bearer <access_token>
Content-Type: application/json
```

For team/workspace accounts, add:
```http
Chatgpt-Account-Id: <account_id>
```

The account ID comes from the `_account` cookie.

---

## API Endpoints

### List Conversations

```
GET /backend-api/conversations?offset={offset}&limit={limit}
```

**Parameters:**
- `offset` (int): Pagination offset (default: 0)
- `limit` (int): Number of results (default: 20, max: 100)

**Response:**
```json
{
  "items": [
    {
      "id": "abc123-def456-...",
      "title": "Conversation Title",
      "create_time": 1704067200.123456
    }
  ],
  "total": 150,
  "limit": 20,
  "offset": 0,
  "has_missing_conversations": false
}
```

---

### Get Conversation Details

```
GET /backend-api/conversation/{conversation_id}
```

**Response:**
```json
{
  "title": "Conversation Title",
  "create_time": 1704067200.123456,
  "update_time": 1704153600.789012,
  "current_node": "node-uuid-123",
  "is_archived": false,
  "moderation_results": [],
  "mapping": {
    "node-uuid-root": {
      "id": "node-uuid-root",
      "parent": null,
      "children": ["node-uuid-1"]
    },
    "node-uuid-1": {
      "id": "node-uuid-1",
      "parent": "node-uuid-root",
      "children": ["node-uuid-2"],
      "message": {
        "id": "msg-uuid-1",
        "author": { "role": "user" },
        "content": {
          "content_type": "text",
          "parts": ["Hello, how are you?"]
        },
        "create_time": 1704067200.123456,
        "status": "finished_successfully",
        "weight": 1
      }
    },
    "node-uuid-2": {
      "id": "node-uuid-2",
      "parent": "node-uuid-1",
      "children": [],
      "message": {
        "id": "msg-uuid-2",
        "author": { "role": "assistant" },
        "content": {
          "content_type": "text",
          "parts": ["I'm doing well, thank you!"]
        },
        "create_time": 1704067205.654321,
        "status": "finished_successfully",
        "weight": 1,
        "metadata": {
          "model_slug": "gpt-4o",
          "finish_details": { "type": "stop" }
        }
      }
    }
  }
}
```

---

### Modify Conversation

```
PATCH /backend-api/conversation/{conversation_id}
```

**Archive conversation:**
```json
{ "is_archived": true }
```

**Delete conversation (hide):**
```json
{ "is_visible": false }
```

**Rename conversation:**
```json
{ "title": "New Title" }
```

---

### Download File Asset

```
GET /backend-api/files/{file_id}/download
```

Used for images and other attachments referenced as `file-service://file-id`.

**Response:**
```json
{
  "status": "success",
  "download_url": "https://files.oaiusercontent.com/...",
  "file_name": "image.png",
  "creation_time": "2024-01-01T12:00:00Z"
}
```

---

### Account Info

```
GET /backend-api/accounts/check/v4-2023-04-27
```

Returns account/subscription info for team workspace handling.

---

## Data Structures

### Message Node

```typescript
interface ConversationNode {
  id: string;
  parent?: string;
  children: string[];
  message?: {
    id: string;
    author: {
      role: "system" | "user" | "assistant" | "tool";
      name?: string;  // e.g., "browser", "python"
    };
    content: MessageContent;
    create_time?: number;
    update_time?: number;
    status: string;
    weight: number;
    metadata?: {
      model_slug?: string;
      finish_details?: { type: "stop" | "interrupted" };
      citations?: Citation[];
      is_visually_hidden_from_conversation?: boolean;
    };
    recipient: string;  // "all", "browser", "python", etc.
    end_turn?: boolean;
  };
}
```

### Content Types

| Type | Description |
|------|-------------|
| `text` | Regular text message with `parts: string[]` |
| `code` | Code block with `language` and `text` |
| `execution_output` | Code execution result |
| `multimodal_text` | Text with images/audio |
| `tether_quote` | Web browsing quote |
| `tether_browsing_display` | Browsing results |
| `user_editable_context` | Custom instructions |
| `model_editable_context` | Model memory |
| `thoughts` | Reasoning/thinking (hidden in UI) |

### Multimodal Image Asset

```typescript
interface MultiModalInputImage {
  content_type: "image_asset_pointer";
  asset_pointer: string;  // "file-service://file-id"
  width: number;
  height: number;
  size_bytes: number;
  metadata?: {
    dalle?: {
      gen_id: string;
      prompt: string;
      seed: number;
    };
  };
}
```

---

## Model Slugs

| Slug | Model |
|------|-------|
| `text-davinci-002-render-sha` | GPT-3.5 (Free) |
| `text-davinci-002-render-paid` | GPT-3.5 (Plus) |
| `gpt-4` | GPT-4 |
| `gpt-4-browsing` | GPT-4 with Browse |
| `gpt-4o` | GPT-4o |
| `gpt-4o-mini` | GPT-4o Mini |
| `o1-preview` | o1-preview |
| `o1-mini` | o1-mini |

---

## Rate Limits

Based on observed behavior:
- **Conversations list:** ~100 requests/minute
- **Individual conversations:** ~50-100 requests/minute
- **Free accounts:** More restrictive limits

Implement exponential backoff for 429 responses.

---

## References

- [acheong08/ChatGPT](https://github.com/acheong08/ChatGPT) - Python reverse-engineered API
- [pionxzh/chatgpt-exporter](https://github.com/pionxzh/chatgpt-exporter) - Browser userscript
- [mohamed-chs/convoviz](https://github.com/mohamed-chs/convoviz) - Export to Markdown

---

*Document generated: 2026-02-08*
*Note: This is an unofficial API that may change without notice.*
