---
name: zoho-crm-crud
description: CRM CRUD ops. COQL queries. Composite API batching.
---

# Zoho CRM CRUD

## Create/Update
```bash
# Upsert (duplicate check on Email)
POST /crm/v6/Contacts/upsert
{"data":[{...}],"duplicate_check_fields":["Email"]}
```

## Read
```bash
GET /crm/v6/{Module}/{id}
GET /crm/v6/{Module}?fields=First_Name,Email&page=1&per_page=200
```

## COQL Query
```bash
POST /crm/v6/coql
{"select_query":"select First_Name,Email from Contacts where Created_Time > '2024-01-01T00:00:00+00:00' limit 100"}
```

## Composite API (batch)
```bash
POST /crm/v6/composite
{"composite_requests":[
  {"method":"GET","url":"/crm/v6/Contacts/123"},
  {"method":"POST","url":"/crm/v6/Leads","body":{...}}
]}
```

## Modules
Leads, Contacts, Accounts, Deals, Products, Quotes, Invoices, Purchase_Orders

## Gotchas
- Max 100 records per batch
- COQL: no JOINs, max 200 results
- Field API names differ from display names
