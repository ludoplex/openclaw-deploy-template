---
name: zoho-sync
description: Cross-module sync CRM↔Books↔Inventory. Webhook triggers.
---

# Zoho Sync

## CRM → Books (Contact/Vendor)
```bash
# Create Books contact from CRM
POST /books/v3/contacts?organization_id={org}
{"contact_name":"...","contact_type":"customer","crm_contact_id":"{crm_id}"}
```

## CRM → Inventory (Item sync)
```bash
POST /inventory/v1/items?organization_id={org}
{"name":"...","rate":100,"product_id":"{crm_product_id}"}
```

## Webhook Setup
```bash
POST /crm/v6/actions/watch
{"watch":[{"channel_id":"1","events":["Contacts.create"],"notify_url":"https://..."}]}
```

## Sync Patterns
| Source | Target | Link Field |
|--------|--------|------------|
| CRM Contact | Books Contact | crm_contact_id |
| CRM Product | Inventory Item | product_id |
| Books Invoice | CRM Deal | cf_deal_id (custom) |

## Gotchas
- Webhooks expire 24hr, re-register daily
- Use composite API to avoid rate limits
- Books/Inventory share org_id, CRM may differ
