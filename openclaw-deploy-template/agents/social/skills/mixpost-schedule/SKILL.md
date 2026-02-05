---
name: mixpost-schedule
description: Mixpost API. Post creation. Queue scheduling.
---

# Mixpost Schedule

## API Base
```
https://your-mixpost.com/api/v1
Authorization: Bearer {token}
```

## Create Post
```bash
POST /posts
{
  "body": "Post content #hashtag",
  "media": [{"id": "media_123"}],
  "accounts": ["acc_1", "acc_2"],
  "scheduled_at": "2024-01-15T10:00:00Z"
}
```

## Queue Management
```bash
# List scheduled
GET /posts?status=scheduled

# Reschedule
PATCH /posts/{id}
{"scheduled_at": "2024-01-16T14:00:00Z"}

# Delete from queue
DELETE /posts/{id}
```

## Upload Media
```bash
POST /media
Content-Type: multipart/form-data
file: @image.jpg
```

## Gotchas
- scheduled_at in UTC
- Max 4 images or 1 video per post
- accounts[] = connected social account IDs
- Draft posts: omit scheduled_at
