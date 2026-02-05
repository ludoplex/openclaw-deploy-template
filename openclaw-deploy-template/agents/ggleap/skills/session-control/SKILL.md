---
name: session-control
description: ggLeap sessions. Start/stop/extend. Customer management.
---

# ggLeap Session Control

## API Base
```
https://api.ggleap.com/v1
X-API-Key: {api_key}
```

## Start Session
```bash
POST /sessions
{
  "station_id": "PC-01",
  "customer_id": "cust_123",
  "duration_minutes": 60,
  "package_id": "hourly"
}
```

## Extend Session
```bash
PATCH /sessions/{session_id}
{"add_minutes": 30}
```

## End Session
```bash
POST /sessions/{session_id}/end
{"reason": "customer_request"}
```

## Customer Lookup
```bash
GET /customers?phone=5551234567
GET /customers/{id}/balance
```

## Quick Actions
| Action | Endpoint |
|--------|----------|
| Add time | PATCH /sessions/{id} |
| Lock PC | POST /stations/{id}/lock |
| Unlock PC | POST /stations/{id}/unlock |
| Message | POST /stations/{id}/message |

## Gotchas
- station_id = physical PC name
- Session auto-ends when time expires
- Lock/unlock requires station online
