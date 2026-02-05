---
name: dns-cloudflare
description: Cloudflare DNS API. Record CRUD. Proxy settings.
---

# Cloudflare DNS

## Auth
```bash
# Headers (use API token, not global key)
Authorization: Bearer $CF_API_TOKEN
Content-Type: application/json
```

## List Records
```bash
GET /zones/{zone_id}/dns_records?type=A&name=example.com
```

## Create Record
```bash
POST /zones/{zone_id}/dns_records
{"type":"A","name":"@","content":"1.2.3.4","ttl":1,"proxied":true}
```

## Update Record
```bash
PATCH /zones/{zone_id}/dns_records/{id}
{"content":"5.6.7.8"}
```

## Delete Record
```bash
DELETE /zones/{zone_id}/dns_records/{id}
```

## Common Records
| Type | Name | Content | Proxied |
|------|------|---------|---------|
| A | @ | IP | true |
| CNAME | www | @ | true |
| MX | @ | mail.provider.com | false |
| TXT | @ | "v=spf1 ..." | false |

## Gotchas
- `ttl:1` = auto (Cloudflare decides)
- MX/TXT cannot be proxied
- Zone ID: Dashboard → Overview → API section
