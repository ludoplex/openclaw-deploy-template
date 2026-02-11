# Support Stack Source Manifest

**Generated:** 2026-02-10  
**Components:** Vapi.ai, Chatwoot  
**Purpose:** Voice AI + Multi-channel Support Integration

---

## 1. VAPI.AI — Voice AI Platform

### Overview
Vapi is an orchestration layer for voice AI, managing three core modules: transcriber (STT), model (LLM), and voice (TTS). It handles real-time streaming, latency optimization, and conversation flow.

### Base URLs
```
REST API:    https://api.vapi.ai
WebSocket:   wss://api.vapi.ai  (for real-time)
Dashboard:   https://dashboard.vapi.ai
```

### Authentication
```http
Authorization: Bearer <VAPI_API_KEY>
```
- API keys generated in Vapi Dashboard → Settings → API Keys
- Keys are organization-scoped

---

### 1.1 REST API Endpoints

#### Assistants
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/assistant` | List all assistants |
| POST | `/assistant` | Create assistant |
| GET | `/assistant/{id}` | Get assistant by ID |
| PATCH | `/assistant/{id}` | Update assistant |
| DELETE | `/assistant/{id}` | Delete assistant |

**Create Assistant Request:**
```json
{
  "name": "Support Assistant",
  "model": {
    "provider": "anthropic",
    "model": "claude-3-opus-20240229",
    "messages": [
      {"role": "system", "content": "You are a helpful support agent..."}
    ],
    "temperature": 0.7,
    "maxTokens": 1500
  },
  "transcriber": {
    "provider": "assembly-ai",
    "language": "en"
  },
  "voice": {
    "provider": "azure",
    "voiceId": "andrew"
  },
  "firstMessage": "Hello! How can I help you today?",
  "serverUrl": "https://your-webhook.com/vapi",
  "serverMessages": ["end-of-call-report", "tool-calls", "status-update"]
}
```

**Response Schema (Assistant Object):**
```json
{
  "id": "assistant-1234abcd",
  "orgId": "org-5678efgh",
  "createdAt": "2024-01-15T09:30:00Z",
  "updatedAt": "2024-01-15T09:30:00Z",
  "name": "string",
  "transcriber": { /* TranscriberConfig */ },
  "model": { /* ModelConfig */ },
  "voice": { /* VoiceConfig */ },
  "firstMessage": "string",
  "serverUrl": "string",
  "serverMessages": ["string"],
  "maxDurationSeconds": 600,
  "endCallPhrases": ["goodbye", "bye"],
  "metadata": {}
}
```

#### Calls
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/call` | List all calls |
| POST | `/call` | Create outbound call |
| GET | `/call/{id}` | Get call by ID |
| DELETE | `/call/{id}` | End/delete call |

**Create Outbound Call:**
```json
{
  "assistantId": "assistant-1234",
  "phoneNumberId": "phone-5678",
  "customer": {
    "number": "+14155551234",
    "name": "John Doe"
  },
  "assistantOverrides": {
    "firstMessage": "Hi John, this is a follow-up call..."
  }
}
```

**Call Response Schema:**
```json
{
  "id": "call-uuid",
  "type": "outboundPhoneCall",
  "status": "queued|ringing|in-progress|ended",
  "endedReason": "hangup|error|timeout",
  "startedAt": "2024-01-15T09:30:00Z",
  "endedAt": "2024-01-15T09:35:00Z",
  "cost": 0.15,
  "costBreakdown": {
    "transport": 0.02,
    "stt": 0.03,
    "llm": 0.08,
    "tts": 0.02,
    "vapi": 0.00
  },
  "artifact": {
    "transcript": "string",
    "recordingUrl": "https://...",
    "messages": []
  }
}
```

#### Phone Numbers
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/phone-number` | List phone numbers |
| POST | `/phone-number` | Buy/import number |
| GET | `/phone-number/{id}` | Get number details |
| PATCH | `/phone-number/{id}` | Update number config |
| DELETE | `/phone-number/{id}` | Release number |

**Phone Number Object:**
```json
{
  "id": "phone-uuid",
  "provider": "twilio|vonage|byo-phone-number",
  "number": "+14155551234",
  "assistantId": "assistant-uuid",
  "squadId": "squad-uuid",
  "serverUrl": "https://webhook.example.com/vapi",
  "status": "active|inactive"
}
```

#### Tools (Function Calling)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tool` | List tools |
| POST | `/tool` | Create tool |
| GET | `/tool/{id}` | Get tool |
| PATCH | `/tool/{id}` | Update tool |
| DELETE | `/tool/{id}` | Delete tool |

**Tool Definition:**
```json
{
  "type": "apiRequest",
  "name": "lookupOrder",
  "description": "Look up customer order status",
  "method": "GET",
  "url": "https://api.example.com/orders/{{orderId}}",
  "headers": {
    "Authorization": "Bearer {{apiKey}}"
  },
  "body": {
    "type": "object",
    "properties": {
      "orderId": {"type": "string"}
    },
    "required": ["orderId"]
  }
}
```

---

### 1.2 WebSocket API (Real-time)

**Connection:**
```javascript
const ws = new WebSocket('wss://api.vapi.ai/ws');
ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'auth',
    token: 'your-api-key'
  }));
};
```

**Supported message types:**
- `start` — Start a call
- `stop` — End a call  
- `say` — Inject speech
- `control` — Call control commands

---

### 1.3 Server URL (Webhooks)

Configure `serverUrl` on assistants/phone numbers. All webhooks are POST with:

```json
{
  "message": {
    "type": "<event-type>",
    "call": { /* Call Object */ },
    /* event-specific fields */
  }
}
```

#### Webhook Event Types

| Event Type | Response Required | Description |
|------------|-------------------|-------------|
| `assistant-request` | ✅ Yes (7.5s timeout) | Provide assistant for inbound call |
| `tool-calls` | ✅ Yes | Execute function calls |
| `transfer-destination-request` | ✅ Yes | Provide transfer destination |
| `knowledge-base-request` | ✅ Yes | Custom knowledge base query |
| `status-update` | ❌ No | Call status changed |
| `end-of-call-report` | ❌ No | Call completed with artifacts |
| `conversation-update` | ❌ No | Transcript updated |
| `transcript` | ❌ No | Partial/final transcript |
| `hang` | ❌ No | Assistant failed to respond |
| `speech-update` | ❌ No | Speech started/stopped |

#### assistant-request Response
```json
// Option 1: Existing assistant
{ "assistantId": "assistant-uuid" }

// Option 2: Transient assistant
{
  "assistant": {
    "firstMessage": "Hello!",
    "model": { "provider": "openai", "model": "gpt-4o" }
  }
}

// Option 3: Direct transfer (skip AI)
{
  "destination": {
    "type": "number",
    "number": "+14155551234"
  }
}

// Option 4: Error message to caller
{ "error": "Sorry, the system is unavailable." }
```

#### tool-calls Payload & Response
```json
// Incoming
{
  "message": {
    "type": "tool-calls",
    "call": {},
    "toolCallList": [
      {
        "id": "call-abc123",
        "name": "lookupOrder", 
        "parameters": { "orderId": "12345" }
      }
    ]
  }
}

// Response
{
  "results": [
    {
      "name": "lookupOrder",
      "toolCallId": "call-abc123",
      "result": "{\"status\": \"shipped\", \"trackingNumber\": \"1Z999\"}"
    }
  ]
}
```

#### end-of-call-report Payload
```json
{
  "message": {
    "type": "end-of-call-report",
    "endedReason": "hangup|error|timeout|assistant-ended",
    "call": { /* full call object */ },
    "artifact": {
      "transcript": "Full conversation transcript...",
      "recordingUrl": "https://storage.vapi.ai/recordings/...",
      "stereoRecordingUrl": "https://...",
      "messages": [
        {"role": "assistant", "message": "Hello!", "time": 0.5},
        {"role": "user", "message": "Hi there", "time": 2.1}
      ]
    },
    "analysis": {
      "summary": "Customer called about order status...",
      "structuredData": { /* custom schema data */ }
    }
  }
}
```

---

### 1.4 Model Providers Supported

| Provider | Models |
|----------|--------|
| OpenAI | gpt-4o, gpt-4-turbo, gpt-3.5-turbo |
| Anthropic | claude-3-opus, claude-3-sonnet, claude-3-haiku |
| Google | gemini-pro, gemini-1.5-pro |
| Groq | llama-3, mixtral |
| Custom | Your own LLM via server URL |

### 1.5 Voice Providers Supported

| Provider | Notable Voices |
|----------|----------------|
| ElevenLabs | Custom cloned voices |
| Azure | andrew, jenny, aria |
| PlayHT | Various |
| Deepgram | Aura voices |
| LMNT | Low-latency voices |

### 1.6 Transcriber Providers

| Provider | Features |
|----------|----------|
| Deepgram | Fast, streaming |
| AssemblyAI | Multi-language, speaker diarization |
| Gladia | Multi-language |

---

### 1.7 Python SDK Example

```python
# pip install vapi-python
from vapi import Vapi

client = Vapi(api_key="your-api-key")

# Create assistant
assistant = client.assistants.create(
    name="Support Bot",
    model={
        "provider": "anthropic",
        "model": "claude-3-sonnet-20240229",
        "messages": [{"role": "system", "content": "You help customers..."}]
    },
    voice={"provider": "elevenlabs", "voiceId": "21m00Tcm4TlvDq8ikWAM"},
    first_message="Hi, how can I help?"
)

# Create outbound call
call = client.calls.create(
    assistant_id=assistant.id,
    phone_number_id="phone-123",
    customer={"number": "+14155551234"}
)

# List calls
calls = client.calls.list()
```

---

## 2. CHATWOOT — Multi-Channel Support Platform

### Overview
Open-source customer engagement platform supporting web chat, email, WhatsApp, Facebook, Twitter, Telegram, and API channels. Self-hostable with Docker/Kubernetes.

### Base URLs
```
Cloud:       https://app.chatwoot.com
Self-hosted: https://your-domain.com
API Base:    {base}/api/v1
```

### Authentication
```http
api_access_token: <USER_ACCESS_TOKEN>
```
- Generate from Profile Settings → Access Token
- Platform APIs use different tokens from Super Admin Console

---

### 2.1 Self-Hosting Requirements

#### Minimum Requirements
- CPU: 2 cores
- RAM: 4GB
- Storage: 20GB SSD
- OS: Ubuntu 20.04+

#### Production Recommended
- CPU: 4+ cores
- RAM: 8GB+
- Storage: 50GB+ SSD
- PostgreSQL 12+
- Redis 6+
- Nginx reverse proxy

#### Docker Deployment
```bash
# Download configs
wget -O .env https://raw.githubusercontent.com/chatwoot/chatwoot/develop/.env.example
wget -O docker-compose.yaml https://raw.githubusercontent.com/chatwoot/chatwoot/develop/docker-compose.production.yaml

# Configure .env with your settings
nano .env

# Initialize database
docker compose run --rm rails bundle exec rails db:chatwoot_prepare

# Start services
docker compose up -d
```

**docker-compose.yaml services:**
- `rails` — Main app (port 3000)
- `sidekiq` — Background jobs
- `postgres` — Database
- `redis` — Cache/queues

---

### 2.2 Application APIs

#### Conversations
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/accounts/{account_id}/conversations` | List conversations |
| POST | `/accounts/{account_id}/conversations` | Create conversation |
| GET | `/accounts/{account_id}/conversations/{id}` | Get conversation |
| POST | `/accounts/{account_id}/conversations/{id}/toggle_status` | Toggle status |
| POST | `/accounts/{account_id}/conversations/{id}/assignments` | Assign agent |

**Create Conversation:**
```bash
curl -X POST "https://app.chatwoot.com/api/v1/accounts/{account_id}/conversations" \
  -H "api_access_token: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "inbox_id": 1,
    "contact_id": 1,
    "status": "open",
    "assignee_id": 1,
    "message": {
      "content": "Hello, how can I help you?"
    }
  }'
```

**Conversation Response:**
```json
{
  "id": 1,
  "account_id": 1,
  "inbox_id": 1,
  "status": "open",
  "muted": false,
  "can_reply": true,
  "timestamp": 1619098200,
  "contact_last_seen_at": 1619098200,
  "agent_last_seen_at": 1619098200,
  "unread_count": 0,
  "additional_attributes": {},
  "custom_attributes": {},
  "meta": {
    "sender": { /* contact */ },
    "assignee": { /* agent */ }
  },
  "messages": []
}
```

#### Messages
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/accounts/{id}/conversations/{conv_id}/messages` | Get messages |
| POST | `/accounts/{id}/conversations/{conv_id}/messages` | Send message |
| DELETE | `/accounts/{id}/conversations/{conv_id}/messages/{msg_id}` | Delete message |

**Send Message:**
```json
{
  "content": "Your order has been shipped!",
  "message_type": "outgoing",
  "private": false,
  "content_type": "text",
  "content_attributes": {}
}
```

**Message Types:**
- `incoming` — From customer
- `outgoing` — From agent/bot
- `activity` — System events
- `template` — WhatsApp templates

**Content Types:**
- `text` — Plain text
- `input_select` — Quick replies
- `cards` — Rich cards
- `article` — Help article
- `input_email` — Email collector
- `input_csat` — CSAT survey

#### Contacts
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/accounts/{id}/contacts` | List contacts |
| POST | `/accounts/{id}/contacts` | Create contact |
| GET | `/accounts/{id}/contacts/{contact_id}` | Get contact |
| PUT | `/accounts/{id}/contacts/{contact_id}` | Update contact |
| DELETE | `/accounts/{id}/contacts/{contact_id}` | Delete contact |
| GET | `/accounts/{id}/contacts/search` | Search contacts |

**Contact Object:**
```json
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "phone_number": "+14155551234",
  "availability_status": "online",
  "identifier": "external-id-123",
  "custom_attributes": {
    "plan": "premium",
    "company": "Acme Inc"
  },
  "additional_attributes": {
    "city": "San Francisco",
    "country": "USA"
  },
  "contact_inboxes": [
    {
      "source_id": "web-widget-session-id",
      "inbox": {
        "id": 1,
        "name": "Website",
        "channel_type": "Channel::WebWidget"
      }
    }
  ]
}
```

#### Inboxes
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/accounts/{id}/inboxes` | List inboxes |
| POST | `/accounts/{id}/inboxes` | Create inbox |
| GET | `/accounts/{id}/inboxes/{inbox_id}` | Get inbox |
| PATCH | `/accounts/{id}/inboxes/{inbox_id}` | Update inbox |
| DELETE | `/accounts/{id}/inboxes/{inbox_id}` | Delete inbox |

**Inbox Types (channel_type):**
- `Channel::WebWidget` — Website chat widget
- `Channel::Api` — API/bot channel
- `Channel::Email` — Email inbox
- `Channel::FacebookPage` — Facebook Messenger
- `Channel::TwitterProfile` — Twitter DMs
- `Channel::TelegramBot` — Telegram
- `Channel::Whatsapp` — WhatsApp Business
- `Channel::Line` — LINE
- `Channel::Sms` — SMS/Twilio

**Create API Inbox (for bot integration):**
```bash
curl -X POST "https://app.chatwoot.com/api/v1/accounts/{account_id}/inboxes" \
  -H "api_access_token: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AI Bot Channel",
    "channel": {
      "type": "api",
      "webhook_url": "https://your-server.com/chatwoot-webhook"
    }
  }'
```

#### Agents
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/accounts/{id}/agents` | List agents |
| POST | `/accounts/{id}/agents` | Add agent |
| PATCH | `/accounts/{id}/agents/{agent_id}` | Update agent |
| DELETE | `/accounts/{id}/agents/{agent_id}` | Remove agent |

---

### 2.3 Webhooks

Configure at: Settings → Integrations → Webhooks

**Webhook Payload Structure:**
```json
{
  "event": "event_type",
  "id": "unique-event-id",
  "account": { /* account object */ },
  "inbox": { /* inbox object */ },
  "conversation": { /* conversation object */ },
  "message": { /* message object if applicable */ },
  "sender": { /* sender object */ }
}
```

**Webhook Events:**
| Event | Trigger |
|-------|---------|
| `conversation_created` | New conversation started |
| `conversation_status_changed` | Status changed (open/resolved/pending) |
| `conversation_updated` | Conversation metadata updated |
| `message_created` | New message in conversation |
| `message_updated` | Message edited |
| `webwidget_triggered` | Website visitor event |

**message_created Webhook:**
```json
{
  "event": "message_created",
  "id": "1234",
  "account": {
    "id": 1,
    "name": "Acme Support"
  },
  "inbox": {
    "id": 1,
    "name": "Website Chat"
  },
  "conversation": {
    "id": 100,
    "status": "open"
  },
  "message": {
    "id": 500,
    "content": "I need help with my order",
    "message_type": "incoming",
    "content_type": "text",
    "created_at": 1619098200,
    "sender": {
      "id": 50,
      "name": "John Doe",
      "type": "contact"
    }
  }
}
```

---

### 2.4 Agent Bot API (For Qwen Integration)

Agent Bots can automatically handle conversations before human handoff.

**Create Agent Bot:**
```bash
curl -X POST "https://app.chatwoot.com/api/v1/accounts/{account_id}/agent_bots" \
  -H "api_access_token: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Qwen Support Bot",
    "description": "AI-powered first responder",
    "outgoing_url": "https://your-server.com/bot-webhook"
  }'
```

**Assign Bot to Inbox:**
```bash
curl -X POST "https://app.chatwoot.com/api/v1/accounts/{id}/inboxes/{inbox_id}/set_agent_bot" \
  -H "api_access_token: <token>" \
  -d '{ "agent_bot": bot_id }'
```

**Bot Webhook Receives:**
```json
{
  "event": "message_created",
  "message": {
    "id": 1,
    "content": "Hello, I need help",
    "message_type": "incoming"
  },
  "conversation": {
    "id": 100,
    "meta": {
      "sender": {
        "id": 50,
        "name": "Customer Name"
      }
    }
  }
}
```

**Bot Response (Send Message Back):**
```bash
curl -X POST "https://app.chatwoot.com/api/v1/accounts/{id}/conversations/{conv_id}/messages" \
  -H "api_access_token: <bot-access-token>" \
  -d '{
    "content": "Hi! I'\''m an AI assistant. How can I help?",
    "message_type": "outgoing"
  }'
```

**Handoff to Human:**
```bash
# Toggle bot handoff (removes bot, opens to human agents)
curl -X POST "https://app.chatwoot.com/api/v1/accounts/{id}/conversations/{conv_id}/toggle_status" \
  -H "api_access_token: <token>" \
  -d '{ "status": "open" }'
```

---

### 2.5 Client APIs (For Custom Chat Widgets)

Used when building custom chat interfaces instead of the default widget.

**Base URL:** `/public/api/v1/inboxes/{inbox_identifier}`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/contacts` | Create contact |
| POST | `/contacts/{id}/conversations` | Create conversation |
| GET | `/contacts/{id}/conversations/{conv_id}/messages` | Get messages |
| POST | `/contacts/{id}/conversations/{conv_id}/messages` | Send message |

**Create Contact:**
```bash
curl -X POST "https://app.chatwoot.com/public/api/v1/inboxes/{inbox_identifier}/contacts" \
  -H "Content-Type: application/json" \
  -d '{
    "identifier": "user-external-id",
    "identifier_hash": "hmac-hash-for-verification",
    "name": "John Doe",
    "email": "john@example.com",
    "phone_number": "+14155551234"
  }'
```

**Response includes `contact_identifier` for subsequent requests.**

---

### 2.6 Platform APIs (Self-hosted Admin)

Available only on self-hosted installations via Super Admin Console.

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/platform/api/v1/users` | Create user |
| GET | `/platform/api/v1/users/{id}` | Get user |
| PATCH | `/platform/api/v1/users/{id}` | Update user |
| DELETE | `/platform/api/v1/users/{id}` | Delete user |
| POST | `/platform/api/v1/accounts` | Create account |
| POST | `/platform/api/v1/account_users` | Add user to account |

---

### 2.7 Channel Connectors

#### Web Widget Setup
```html
<script>
  (function(d,t) {
    var BASE_URL="https://your-chatwoot.com";
    var g=d.createElement(t),s=d.getElementsByTagName(t)[0];
    g.src=BASE_URL+"/packs/js/sdk.js";
    g.defer = true;
    g.async = true;
    s.parentNode.insertBefore(g,s);
    g.onload=function(){
      window.chatwootSDK.run({
        websiteToken: 'YOUR_WEBSITE_TOKEN',
        baseUrl: BASE_URL
      })
    }
  })(document,"script");
</script>
```

#### WhatsApp (via 360dialog/Twilio)
Configure in Settings → Inboxes → Add WhatsApp

#### Email Channel
Set SMTP/IMAP in environment variables:
```bash
MAILER_SENDER_EMAIL=support@example.com
SMTP_ADDRESS=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=user
SMTP_PASSWORD=pass
IMAP_ADDRESS=imap.example.com
```

---

## 3. INTEGRATION PATTERN: Vapi ↔ Chatwoot

### Voice-to-Chat Handoff Flow

```
[Phone Call] → Vapi → [end-of-call-report webhook]
                            ↓
              Your Server → Create Chatwoot Contact
                            ↓
                          Create Conversation with transcript
                            ↓
                          Human agent follows up via chat/email
```

### Example Integration Code

```python
from flask import Flask, request
import requests

app = Flask(__name__)

CHATWOOT_URL = "https://app.chatwoot.com"
CHATWOOT_TOKEN = "your-api-token"
ACCOUNT_ID = 1
INBOX_ID = 1  # API inbox for bot/integration

@app.route("/vapi-webhook", methods=["POST"])
def vapi_webhook():
    data = request.json
    message = data.get("message", {})
    
    if message.get("type") == "end-of-call-report":
        call = message.get("call", {})
        artifact = message.get("artifact", {})
        customer = call.get("customer", {})
        
        # Create or find contact
        contact = create_or_find_contact(
            phone=customer.get("number"),
            name=customer.get("name")
        )
        
        # Create conversation with transcript
        transcript = artifact.get("transcript", "")
        summary = message.get("analysis", {}).get("summary", "")
        
        create_conversation(
            contact_id=contact["id"],
            message=f"📞 Voice Call Summary\n\n{summary}\n\n---\n\nFull Transcript:\n{transcript}"
        )
    
    return {"status": "ok"}

def create_or_find_contact(phone, name):
    # Search for existing contact
    resp = requests.get(
        f"{CHATWOOT_URL}/api/v1/accounts/{ACCOUNT_ID}/contacts/search",
        headers={"api_access_token": CHATWOOT_TOKEN},
        params={"q": phone}
    )
    contacts = resp.json().get("payload", [])
    
    if contacts:
        return contacts[0]
    
    # Create new contact
    resp = requests.post(
        f"{CHATWOOT_URL}/api/v1/accounts/{ACCOUNT_ID}/contacts",
        headers={"api_access_token": CHATWOOT_TOKEN},
        json={
            "name": name or "Unknown Caller",
            "phone_number": phone
        }
    )
    return resp.json()["payload"]["contact"]

def create_conversation(contact_id, message):
    resp = requests.post(
        f"{CHATWOOT_URL}/api/v1/accounts/{ACCOUNT_ID}/conversations",
        headers={"api_access_token": CHATWOOT_TOKEN},
        json={
            "inbox_id": INBOX_ID,
            "contact_id": contact_id,
            "status": "open",
            "message": {"content": message}
        }
    )
    return resp.json()
```

---

## 4. QUICK REFERENCE

### Vapi API Quick Reference
```bash
# List assistants
curl -H "Authorization: Bearer $VAPI_KEY" https://api.vapi.ai/assistant

# Create call
curl -X POST https://api.vapi.ai/call \
  -H "Authorization: Bearer $VAPI_KEY" \
  -H "Content-Type: application/json" \
  -d '{"assistantId": "xxx", "phoneNumberId": "yyy", "customer": {"number": "+1..."}}'

# Get call details
curl -H "Authorization: Bearer $VAPI_KEY" https://api.vapi.ai/call/{call_id}
```

### Chatwoot API Quick Reference
```bash
# List conversations
curl -H "api_access_token: $CW_TOKEN" \
  https://app.chatwoot.com/api/v1/accounts/1/conversations

# Send message
curl -X POST https://app.chatwoot.com/api/v1/accounts/1/conversations/100/messages \
  -H "api_access_token: $CW_TOKEN" \
  -d '{"content": "Hello!", "message_type": "outgoing"}'

# Create contact
curl -X POST https://app.chatwoot.com/api/v1/accounts/1/contacts \
  -H "api_access_token: $CW_TOKEN" \
  -d '{"name": "John", "email": "john@example.com"}'
```

---

## 5. RESOURCES

### Vapi
- **Docs:** https://docs.vapi.ai
- **API Reference:** https://docs.vapi.ai/api-reference
- **Dashboard:** https://dashboard.vapi.ai
- **Python SDK:** `pip install vapi-python`
- **Status:** https://status.vapi.ai

### Chatwoot
- **Docs:** https://developers.chatwoot.com
- **GitHub:** https://github.com/chatwoot/chatwoot
- **API Postman:** https://www.postman.com/chatwoot/workspace/chatwoot-apis
- **Docker Hub:** https://hub.docker.com/r/chatwoot/chatwoot
- **Discord:** https://discord.gg/cJXdrwS
