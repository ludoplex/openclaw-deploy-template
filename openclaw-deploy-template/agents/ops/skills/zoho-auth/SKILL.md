---
name: zoho-auth
description: Zoho OAuth2 tokens. Refresh flow. Multi-org routing.
---

# Zoho Auth

## Token Refresh
```bash
curl -X POST "https://accounts.zoho.com/oauth/v2/token" \
  -d "refresh_token=$REFRESH&client_id=$ID&client_secret=$SECRET&grant_type=refresh_token"
```

## Multi-Org Headers
```
X-com-zoho-subscriptions-organizationid: {org_id}
Authorization: Zoho-oauthtoken {access_token}
```

## Domains
| Region | Auth | API |
|--------|------|-----|
| US | accounts.zoho.com | www.zohoapis.com |
| EU | accounts.zoho.eu | www.zohoapis.eu |
| IN | accounts.zoho.in | www.zohoapis.in |

## Gotchas
- Tokens expire 1hr, refresh tokens last 90 days inactive
- Scope required per module: `ZohoCRM.modules.ALL`
- Rate: 500 req/day/user (Free), 25k (Pro)
