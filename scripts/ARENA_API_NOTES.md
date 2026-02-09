# Arena.ai (LMArena) API Reverse Engineering Notes

## Overview

Arena.ai (formerly chat.lmsys.org / LMArena) is a platform for comparing and benchmarking AI models through blind A/B testing (battles).

## Architecture

### Frontend
- **Framework**: Next.js 14+ with React Server Components (RSC)
- **URL Structure**: 
  - Conversations: `/c/{uuid}` (UUID v7/ULID format)
  - Leaderboard: `/leaderboard`
  - Direct chat: `/` (creates new conversation)

### Authentication
- **Provider**: Supabase (hosted at `auth.arena.ai`)
- **Methods**: Google OAuth, Email/Password
- **Token Storage**: 
  - localStorage: Key like `sb-{project-id}-auth-token`
  - Cookies: HTTP-only session cookies
- **Token Format**: Standard JWT with Supabase claims

### Data Storage
- **Database**: Supabase PostgreSQL with Row Level Security (RLS)
- **API**: Supabase REST API at `https://auth.arena.ai/rest/v1/`
- **Real-time**: Supabase Realtime (websocket) for live updates

## Known API Endpoints

### Supabase REST API
```
Base: https://auth.arena.ai/rest/v1/

# Requires apikey header and Bearer token for authenticated requests
Headers:
  apikey: {supabase_anon_key}
  Authorization: Bearer {user_jwt}
  Content-Type: application/json
```

### Potential Table Names (based on code analysis)
- `conversations` - Main conversation records
- `messages` or `turns` - Individual messages in conversations
- `evaluations` - Battle/comparison evaluations
- `votes` - User voting history
- `users` - User profiles (managed by Supabase Auth)

### Next.js API Routes
```
Base: https://arena.ai/nextjs-api/

# These proxy to Supabase or other backends
# Require session cookies or Authorization header
```

## Session Structure

The Supabase auth token in localStorage contains:
```json
{
  "access_token": "eyJ...",  // JWT for API calls
  "token_type": "bearer",
  "expires_in": 3600,
  "expires_at": 1234567890,
  "refresh_token": "xxx",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "app_metadata": {...},
    "user_metadata": {...}
  }
}
```

## Conversation Data Format (Inferred)

Based on URL patterns and UI:
```json
{
  "id": "019ba997-9ff2-7779-9ca8-6c6692eb6cbf",
  "user_id": "uuid",
  "created_at": "2024-01-01T00:00:00Z",
  "mode": "battle" | "direct",
  "model_a": "gpt-4o",
  "model_b": "claude-3",
  "messages": [
    {
      "role": "user",
      "content": "...",
      "timestamp": "..."
    },
    {
      "role": "assistant_a",
      "content": "...",
      "model": "..."
    }
  ],
  "vote": "model_a" | "model_b" | "tie" | "both_bad" | null
}
```

## Extraction Approach

1. **Get Auth Token**: From browser localStorage or cookies
2. **Query Supabase**: Use REST API with RLS-filtered queries
3. **Fallback**: Try Next.js API routes if direct Supabase fails

## Security Notes

- Supabase anon key is public (visible in frontend JS)
- All data access requires valid JWT with user claims
- RLS policies restrict access to user's own data
- Rate limiting may apply

## Tools Used

- Python `requests` for HTTP
- Browser DevTools for token extraction
- Supabase PostgREST for data access

## Changes from Old Gradio Version

The old chat.lmsys.org used:
- Gradio for UI
- File-based logging (JSON files)
- In-memory state

The new arena.ai uses:
- Next.js + React
- Supabase for persistence
- Account-based history

## References

- FastChat repo: https://github.com/lm-sys/FastChat
- Supabase docs: https://supabase.com/docs
- Arena blog: https://arena.ai/blog
