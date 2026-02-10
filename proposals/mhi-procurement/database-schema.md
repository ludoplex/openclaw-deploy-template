# MHI Procurement Database Schema

SQLite single-file database for multi-entity procurement.

## ERD (Text-Based)

```
┌─────────────┐       ┌──────────────────────┐
│  entities   │───<──┤  supplier_credentials │
└─────────────┘       └──────────────────────┘
      │                        │
      │                        │
      ▼                        ▼
┌─────────────┐       ┌──────────────────────┐
│   quotes    │───>───┤      suppliers       │
└─────────────┘       └──────────────────────┘
      │                        │
      ▼                        ▼
┌─────────────┐       ┌──────────────────────┐
│ quote_items │───>───┤   product_cache      │
└─────────────┘       └──────────────────────┘
      │
      ▼
┌─────────────┐       ┌──────────────────────┐
│   orders    │───>───┤     order_items      │
└─────────────┘       └──────────────────────┘
```

**Relationships:**
- Entity 1:N Supplier Credentials
- Entity 1:N Quotes
- Entity 1:N Orders
- Quote 1:N Quote Items
- Order 1:N Order Items
- Product Cache is supplier-specific, denormalized for speed

---

## CREATE TABLE Statements

```sql
-- Enable foreign keys (SQLite default is OFF)
PRAGMA foreign_keys = ON;

-- Business entities (MHI, DSAIC, Computer Store)
CREATE TABLE entities (
    id              INTEGER PRIMARY KEY,
    code            TEXT NOT NULL UNIQUE,  -- 'MHI', 'DSAIC', 'CS'
    name            TEXT NOT NULL,
    tax_id          TEXT,
    default_ship_to TEXT,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);

-- Supplier definitions
CREATE TABLE suppliers (
    id              INTEGER PRIMARY KEY,
    code            TEXT NOT NULL UNIQUE,  -- 'INGRAM', 'SYNNEX', 'DH', 'CLIMB'
    name            TEXT NOT NULL,
    api_base_url    TEXT,
    active          INTEGER DEFAULT 1
);

-- Credentials per entity/supplier combo
CREATE TABLE supplier_credentials (
    id              INTEGER PRIMARY KEY,
    entity_id       INTEGER NOT NULL REFERENCES entities(id),
    supplier_id     INTEGER NOT NULL REFERENCES suppliers(id),
    account_number  TEXT,
    username        TEXT,
    password_enc    TEXT,  -- encrypted, never plaintext
    api_key_enc     TEXT,  -- encrypted
    extra_json      TEXT,  -- any supplier-specific fields
    active          INTEGER DEFAULT 1,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now')),
    UNIQUE(entity_id, supplier_id)
);

-- Cached product data from suppliers (denormalized for search speed)
CREATE TABLE product_cache (
    id              INTEGER PRIMARY KEY,
    supplier_id     INTEGER NOT NULL REFERENCES suppliers(id),
    sku             TEXT NOT NULL,         -- supplier's SKU
    mfr_part        TEXT,                  -- manufacturer part number
    upc             TEXT,
    description     TEXT,
    manufacturer    TEXT,
    category        TEXT,
    price           REAL,                  -- current price (entity-specific pricing handled at query time)
    msrp            REAL,
    qty_available   INTEGER,
    weight_lbs      REAL,
    image_url       TEXT,
    raw_json        TEXT,                  -- full API response for reference
    fetched_at      TEXT DEFAULT (datetime('now')),
    UNIQUE(supplier_id, sku)
);

-- Quotes (saved comparisons/carts)
CREATE TABLE quotes (
    id              INTEGER PRIMARY KEY,
    entity_id       INTEGER NOT NULL REFERENCES entities(id),
    quote_number    TEXT UNIQUE,           -- user-friendly ID: 'Q-2024-0001'
    name            TEXT,                  -- 'Dell Laptops for IT Dept'
    status          TEXT DEFAULT 'draft',  -- draft, sent, accepted, expired
    notes           TEXT,
    created_by      TEXT,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now')),
    expires_at      TEXT
);

-- Line items in a quote
CREATE TABLE quote_items (
    id              INTEGER PRIMARY KEY,
    quote_id        INTEGER NOT NULL REFERENCES quotes(id) ON DELETE CASCADE,
    supplier_id     INTEGER NOT NULL REFERENCES suppliers(id),
    sku             TEXT NOT NULL,
    mfr_part        TEXT,
    description     TEXT NOT NULL,
    quantity        INTEGER NOT NULL DEFAULT 1,
    unit_price      REAL NOT NULL,
    extended_price  REAL GENERATED ALWAYS AS (quantity * unit_price) STORED,
    notes           TEXT,
    created_at      TEXT DEFAULT (datetime('now'))
);

-- Orders placed with suppliers
CREATE TABLE orders (
    id              INTEGER PRIMARY KEY,
    entity_id       INTEGER NOT NULL REFERENCES entities(id),
    supplier_id     INTEGER NOT NULL REFERENCES suppliers(id),
    quote_id        INTEGER REFERENCES quotes(id),  -- optional, if from quote
    order_number    TEXT UNIQUE,           -- our internal: 'PO-2024-0001'
    supplier_order  TEXT,                  -- supplier's order/confirmation #
    status          TEXT DEFAULT 'pending', -- pending, submitted, confirmed, shipped, delivered, cancelled
    ship_to_name    TEXT,
    ship_to_address TEXT,
    ship_method     TEXT,
    subtotal        REAL,
    tax             REAL,
    shipping        REAL,
    total           REAL,
    notes           TEXT,
    ordered_by      TEXT,
    ordered_at      TEXT,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);

-- Line items in an order
CREATE TABLE order_items (
    id              INTEGER PRIMARY KEY,
    order_id        INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    sku             TEXT NOT NULL,
    mfr_part        TEXT,
    description     TEXT NOT NULL,
    quantity        INTEGER NOT NULL,
    unit_price      REAL NOT NULL,
    extended_price  REAL GENERATED ALWAYS AS (quantity * unit_price) STORED,
    tracking_number TEXT,
    ship_date       TEXT,
    notes           TEXT
);

-- Simple search log for analytics (optional, lightweight)
CREATE TABLE search_log (
    id              INTEGER PRIMARY KEY,
    entity_id       INTEGER REFERENCES entities(id),
    query           TEXT NOT NULL,
    result_count    INTEGER,
    searched_at     TEXT DEFAULT (datetime('now'))
);
```

---

## Key Indexes

```sql
-- Product search (the hot path)
CREATE INDEX idx_product_cache_mfr_part ON product_cache(mfr_part);
CREATE INDEX idx_product_cache_upc ON product_cache(upc);
CREATE INDEX idx_product_cache_description ON product_cache(description);
CREATE INDEX idx_product_cache_supplier_sku ON product_cache(supplier_id, sku);

-- FTS for product search (optional but recommended)
CREATE VIRTUAL TABLE product_fts USING fts5(
    description, 
    manufacturer, 
    mfr_part,
    content='product_cache',
    content_rowid='id'
);

-- Quotes/Orders by entity
CREATE INDEX idx_quotes_entity ON quotes(entity_id, status);
CREATE INDEX idx_orders_entity ON orders(entity_id, status);
CREATE INDEX idx_orders_supplier ON orders(supplier_id, status);

-- Order tracking
CREATE INDEX idx_orders_supplier_order ON orders(supplier_order);
CREATE INDEX idx_order_items_tracking ON order_items(tracking_number);

-- Credentials lookup
CREATE INDEX idx_creds_entity ON supplier_credentials(entity_id);
```

---

## Design Rationale

| Decision | Why |
|----------|-----|
| **SQLite** | Single file, zero config, works everywhere (Cosmopolitan), handles this scale easily |
| **Denormalized product_cache** | Search speed > normalization purity; products are fetched fresh from APIs anyway |
| **Generated columns for extended_price** | Auto-calculated, can't get out of sync |
| **ISO 8601 TEXT dates** | SQLite doesn't have real datetime; TEXT with `datetime()` is portable and sortable |
| **Encrypted credential fields** | Just column placeholders; actual encryption handled in app layer |
| **Separate quotes vs orders** | Different lifecycles; quotes are comparisons, orders are commitments |
| **FTS5 for search** | Native SQLite full-text search, fast, no external dependencies |
| **Soft entity isolation** | All tables have entity_id FK; multi-tenant via row-level filtering |
| **No user table** | Assume auth handled externally (SSO, etc.); just store usernames as text |

---

## Seed Data

```sql
-- Suppliers
INSERT INTO suppliers (code, name) VALUES 
    ('INGRAM', 'Ingram Micro'),
    ('SYNNEX', 'TD SYNNEX'),
    ('DH', 'D&H Distributing'),
    ('CLIMB', 'Climb Channel Solutions');

-- Entities
INSERT INTO entities (code, name) VALUES 
    ('MHI', 'MHI'),
    ('DSAIC', 'DSAIC'),
    ('CS', 'Computer Store');
```

---

## File Size Estimates

| Data | Rows | Est. Size |
|------|------|-----------|
| Entities | 3-10 | <1 KB |
| Suppliers | 4-8 | <1 KB |
| Credentials | ~20 | <5 KB |
| Product cache | 100K | ~50 MB |
| Quotes | 1000/yr | ~500 KB/yr |
| Orders | 500/yr | ~300 KB/yr |

**Total: <100 MB** for years of operation. SQLite handles this trivially.
