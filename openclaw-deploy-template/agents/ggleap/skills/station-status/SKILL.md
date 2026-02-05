---
name: station-status
description: Real-time PC status. Availability. Health monitoring.
---

# ggLeap Station Status

## List All Stations
```bash
GET /stations
# Returns: id, name, status, current_session, specs
```

## Single Station
```bash
GET /stations/{id}
GET /stations/{id}/health  # CPU, RAM, network
```

## Status Values
| Status | Meaning |
|--------|---------|
| available | Ready for customer |
| in_use | Active session |
| reserved | Upcoming booking |
| maintenance | Admin disabled |
| offline | Not responding |

## Availability Query
```bash
GET /stations?status=available&zone=vip
```

## Health Thresholds
```json
{
  "cpu_warn": 80,
  "ram_warn": 85,
  "disk_warn": 90,
  "network_latency_warn": 50
}
```

## Gotchas
- Status updates every 30s
- offline after 2min no heartbeat
- Health data requires ggLeap agent v3+
