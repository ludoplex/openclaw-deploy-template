# MHI Procurement Web Application — Architecture & Development Plan

**Version:** 1.0  
**Date:** 2026-02-09  
**Status:** Implementation Ready

---

## Executive Summary

Build a **TypeScript web application** for MHI, DSAIC, and Computer Store that provides:
- Multi-supplier price comparison (Ingram Micro, TD SYNNEX, D&H, Climb)
- Best deals / highest margin discovery
- Complete UI with all supplier features exposed
- Multi-entity support (switch between MHI/DSAIC/Computer Store)

This web application **complements** the existing C-based desktop tool (`mhi-procurement.com`) and can share the same SQLite database or operate independently.

---

## 1. Technology Stack Decision

### Chosen Stack: **Next.js 15 + TypeScript + SQLite/Postgres**

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Framework** | Next.js 15 (App Router) | React 19, Server Components, Server Actions, excellent DX |
| **Language** | TypeScript 5.x | Full type safety, matches requirement |
| **Database** | SQLite (dev) → Postgres (prod) | Compatible with existing C app, Postgres for scale |
| **ORM** | Drizzle ORM | Type-safe, lightweight, excellent SQLite/Postgres support |
| **API Layer** | Server Actions + tRPC (optional) | Modern, type-safe, minimal boilerplate |
| **UI Components** | shadcn/ui + Tailwind CSS | Beautiful, accessible, copy-paste components |
| **Auth** | NextAuth.js v5 | Multi-entity support, session management |
| **State** | Zustand | Lightweight, TypeScript-friendly |
| **Testing** | Vitest + Playwright | Fast unit tests, E2E coverage |

### Why Next.js over SvelteKit?

| Factor | Next.js | SvelteKit |
|--------|---------|-----------|
| Ecosystem | Massive (shadcn, Auth.js, etc.) | Growing but smaller |
| TypeScript | First-class | First-class |
| React knowledge | Common in enterprise | Less common |
| Component libraries | Abundant | Limited |
| Hiring | Easier | Harder |

**Verdict:** Next.js for faster development and larger ecosystem.

---

## 2. Project Structure

```
C:\mhi-procurement-web\
├── src/
│   ├── app/                      # Next.js App Router
│   │   ├── (auth)/               # Auth routes (login, etc.)
│   │   ├── (dashboard)/          # Main app routes
│   │   │   ├── products/         # Product catalog
│   │   │   ├── compare/          # Price comparison
│   │   │   ├── margins/          # Margin analysis
│   │   │   ├── basket/           # Shopping basket
│   │   │   ├── orders/           # Purchase orders
│   │   │   ├── sync/             # Supplier sync status
│   │   │   └── settings/         # Entity & supplier settings
│   │   ├── api/                  # API routes (webhooks, etc.)
│   │   ├── layout.tsx
│   │   └── page.tsx
│   │
│   ├── components/
│   │   ├── ui/                   # shadcn/ui components
│   │   ├── products/             # Product-specific components
│   │   ├── suppliers/            # Supplier-specific components
│   │   ├── comparison/           # Price comparison views
│   │   └── layout/               # Header, sidebar, etc.
│   │
│   ├── lib/
│   │   ├── db/
│   │   │   ├── schema.ts         # Drizzle schema
│   │   │   ├── index.ts          # DB connection
│   │   │   └── queries/          # Query functions
│   │   ├── suppliers/
│   │   │   ├── ingram/           # Ingram Micro API client
│   │   │   ├── synnex/           # TD SYNNEX client
│   │   │   ├── dandh/            # D&H client
│   │   │   └── climb/            # Climb (manual entry)
│   │   ├── auth/                 # Auth config
│   │   └── utils/                # Utilities
│   │
│   ├── actions/                  # Server Actions
│   │   ├── products.ts
│   │   ├── suppliers.ts
│   │   ├── basket.ts
│   │   └── sync.ts
│   │
│   └── types/                    # TypeScript types
│       ├── product.ts
│       ├── supplier.ts
│       └── api.ts
│
├── drizzle/
│   ├── migrations/               # DB migrations
│   └── seed.ts                   # Seed data
│
├── public/
│   └── ...
│
├── tests/
│   ├── unit/
│   └── e2e/
│
├── drizzle.config.ts
├── next.config.ts
├── tailwind.config.ts
├── tsconfig.json
└── package.json
```

---

## 3. Database Schema (Drizzle ORM)

Matches existing C app schema for compatibility:

```typescript
// src/lib/db/schema.ts
import { sqliteTable, text, integer, real, index, uniqueIndex } from 'drizzle-orm/sqlite-core';

// Core product table (SSOT)
export const products = sqliteTable('products', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  upc: text('upc').unique(),
  ean: text('ean'),
  mfrPart: text('mfr_part').notNull(),
  manufacturer: text('manufacturer').notNull(),
  name: text('name').notNull(),
  category: text('category'),
  subcategory: text('subcategory'),
  description: text('description'),
  specsJson: text('specs_json'),
  msrp: real('msrp'),
  weightLbs: real('weight_lbs'),
  imageUrl: text('image_url'),
  icecatId: integer('icecat_id'),
  createdAt: text('created_at').default(sql`(datetime('now'))`),
  updatedAt: text('updated_at').default(sql`(datetime('now'))`),
}, (table) => ({
  upcIdx: index('idx_products_upc').on(table.upc),
  mfrPartIdx: index('idx_products_mfr_part').on(table.mfrPart),
  manufacturerIdx: index('idx_products_manufacturer').on(table.manufacturer),
}));

// Suppliers
export const suppliers = sqliteTable('suppliers', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  code: text('code').unique().notNull(),
  name: text('name').notNull(),
  apiType: text('api_type'),
  apiBase: text('api_base'),
  accountNum: text('account_num'),
  contact: text('contact'),
  notes: text('notes'),
  enabled: integer('enabled').default(1),
});

// Supplier offerings (prices, stock)
export const supplierOfferings = sqliteTable('supplier_offerings', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  productId: integer('product_id').notNull().references(() => products.id, { onDelete: 'cascade' }),
  supplierId: integer('supplier_id').notNull().references(() => suppliers.id, { onDelete: 'cascade' }),
  supplierSku: text('supplier_sku'),
  supplierPart: text('supplier_part'),
  cost: real('cost').notNull(),
  qtyAvailable: integer('qty_available').default(0),
  warehouse: text('warehouse'),
  leadTimeDays: integer('lead_time_days'),
  minOrderQty: integer('min_order_qty').default(1),
  promoPrice: real('promo_price'),
  promoExpires: text('promo_expires'),
  lastSyncedAt: text('last_synced_at').default(sql`(datetime('now'))`),
}, (table) => ({
  productIdx: index('idx_offerings_product').on(table.productId),
  supplierIdx: index('idx_offerings_supplier').on(table.supplierId),
  costIdx: index('idx_offerings_cost').on(table.cost),
  uniqueOffering: uniqueIndex('idx_unique_offering').on(table.productId, table.supplierId, table.warehouse),
}));

// Market prices (Best Buy, eBay, etc.)
export const marketPrices = sqliteTable('market_prices', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  productId: integer('product_id').notNull().references(() => products.id, { onDelete: 'cascade' }),
  source: text('source').notNull(),
  marketPrice: real('market_price').notNull(),
  url: text('url'),
  condition: text('condition').default('new'),
  seller: text('seller'),
  lastCheckedAt: text('last_checked_at').default(sql`(datetime('now'))`),
});

// Basket items
export const basketItems = sqliteTable('basket_items', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  entityId: text('entity_id').notNull(), // MHI, DSAIC, or ComputerStore
  productId: integer('product_id').notNull().references(() => products.id),
  supplierId: integer('supplier_id').notNull().references(() => suppliers.id),
  quantity: integer('quantity').notNull().default(1),
  unitCost: real('unit_cost').notNull(),
  targetSell: real('target_sell'),
  notes: text('notes'),
  addedAt: text('added_at').default(sql`(datetime('now'))`),
});

// Purchase orders
export const purchaseOrders = sqliteTable('purchase_orders', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  entityId: text('entity_id').notNull(),
  supplierId: integer('supplier_id').notNull().references(() => suppliers.id),
  poNumber: text('po_number').unique(),
  status: text('status').default('draft'),
  totalCost: real('total_cost'),
  submittedAt: text('submitted_at'),
  receivedAt: text('received_at'),
  notes: text('notes'),
  createdAt: text('created_at').default(sql`(datetime('now'))`),
});

// PO line items
export const poLineItems = sqliteTable('po_line_items', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  poId: integer('po_id').notNull().references(() => purchaseOrders.id, { onDelete: 'cascade' }),
  productId: integer('product_id').notNull().references(() => products.id),
  quantity: integer('quantity').notNull(),
  unitCost: real('unit_cost').notNull(),
  supplierSku: text('supplier_sku'),
});

// Entities (MHI, DSAIC, Computer Store)
export const entities = sqliteTable('entities', {
  id: text('id').primaryKey(), // 'mhi', 'dsaic', 'computer-store'
  name: text('name').notNull(),
  accountNumbers: text('account_numbers'), // JSON: { ingram: "...", synnex: "..." }
  settings: text('settings'), // JSON for entity-specific settings
  createdAt: text('created_at').default(sql`(datetime('now'))`),
});

// Sync log
export const syncLog = sqliteTable('sync_log', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  supplierId: integer('supplier_id').references(() => suppliers.id),
  source: text('source').notNull(),
  syncType: text('sync_type').notNull(),
  status: text('status').notNull(),
  recordsSynced: integer('records_synced').default(0),
  errorMsg: text('error_msg'),
  startedAt: text('started_at').default(sql`(datetime('now'))`),
  completedAt: text('completed_at'),
});
```

---

## 4. Ingram Micro API Integration Plan

### API Overview

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/oauth/oauth30/token` | POST | OAuth2 token (client credentials) |
| `/resellers/v6/catalog` | GET | Product search |
| `/resellers/v6/catalog/priceandavailability` | POST | Real-time P&A |
| `/resellers/v6/catalog/{sku}` | GET | Product details |
| `/resellers/v6/orders` | POST | Create order |
| `/resellers/v6/orders/{orderNumber}` | GET | Order status |

### Implementation

```typescript
// src/lib/suppliers/ingram/client.ts
import { z } from 'zod';

const INGRAM_API_BASE = 'https://api.ingrammicro.com';
const INGRAM_CUSTOMER_NUMBER = process.env.INGRAM_CUSTOMER_NUMBER!;
const INGRAM_SENDER_ID = 'MHI-Procurement-Web';

// Token cache
let cachedToken: { accessToken: string; expiresAt: number } | null = null;

export class IngramMicroClient {
  private clientId: string;
  private clientSecret: string;
  private customerNumber: string;

  constructor(config: {
    clientId: string;
    clientSecret: string;
    customerNumber: string;
  }) {
    this.clientId = config.clientId;
    this.clientSecret = config.clientSecret;
    this.customerNumber = config.customerNumber;
  }

  // OAuth2 Client Credentials
  async getAccessToken(): Promise<string> {
    const now = Date.now();
    if (cachedToken && cachedToken.expiresAt > now + 60000) {
      return cachedToken.accessToken;
    }

    const response = await fetch(`${INGRAM_API_BASE}/oauth/oauth30/token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        grant_type: 'client_credentials',
        client_id: this.clientId,
        client_secret: this.clientSecret,
      }),
    });

    if (!response.ok) {
      throw new Error(`OAuth failed: ${response.status}`);
    }

    const data = await response.json();
    cachedToken = {
      accessToken: data.access_token,
      expiresAt: now + (data.expires_in * 1000),
    };

    return cachedToken.accessToken;
  }

  // Standard headers for all API calls
  private async getHeaders(): Promise<HeadersInit> {
    const token = await this.getAccessToken();
    return {
      'Authorization': `Bearer ${token}`,
      'IM-CustomerNumber': this.customerNumber,
      'IM-SenderID': INGRAM_SENDER_ID,
      'IM-CorrelationID': `web-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };
  }

  // Search products
  async searchCatalog(query: string, options?: {
    pageNumber?: number;
    pageSize?: number;
  }): Promise<IngramCatalogResponse> {
    const params = new URLSearchParams({
      keyword: query,
      pageNumber: String(options?.pageNumber ?? 1),
      pageSize: String(options?.pageSize ?? 25),
    });

    const response = await fetch(
      `${INGRAM_API_BASE}/resellers/v6/catalog?${params}`,
      { headers: await this.getHeaders() }
    );

    if (!response.ok) {
      throw new Error(`Catalog search failed: ${response.status}`);
    }

    return response.json();
  }

  // Get price and availability
  async getPriceAndAvailability(skus: string[]): Promise<IngramPriceResponse> {
    const response = await fetch(
      `${INGRAM_API_BASE}/resellers/v6/catalog/priceandavailability`,
      {
        method: 'POST',
        headers: await this.getHeaders(),
        body: JSON.stringify({
          showAvailableDiscounts: true,
          showReserveInventoryDetails: true,
          specialBidNumber: '',
          products: skus.map(sku => ({
            ingramPartNumber: sku,
          })),
        }),
      }
    );

    if (!response.ok) {
      throw new Error(`P&A lookup failed: ${response.status}`);
    }

    return response.json();
  }

  // Create order
  async createOrder(order: IngramOrderRequest): Promise<IngramOrderResponse> {
    const response = await fetch(
      `${INGRAM_API_BASE}/resellers/v6/orders`,
      {
        method: 'POST',
        headers: await this.getHeaders(),
        body: JSON.stringify(order),
      }
    );

    if (!response.ok) {
      throw new Error(`Order creation failed: ${response.status}`);
    }

    return response.json();
  }
}

// Type definitions
export interface IngramCatalogResponse {
  recordsFound: number;
  pageSize: number;
  pageNumber: number;
  catalog: IngramProduct[];
}

export interface IngramProduct {
  ingramPartNumber: string;
  vendorPartNumber: string;
  vendorNumber: string;
  vendorName: string;
  description: string;
  upcCode: string;
  productCategory: string;
  productSubcategory: string;
  customerPrice: number;
  msrp: number;
  availability: {
    available: boolean;
    totalAvailability: number;
    availabilityByWarehouse: {
      warehouseId: string;
      quantityAvailable: number;
    }[];
  };
}

export interface IngramPriceResponse {
  productDetailResponse: {
    ingramPartNumber: string;
    vendorPartNumber: string;
    customerPrice: number;
    retailPrice: number;
    availability: {
      available: boolean;
      totalAvailability: number;
    };
  }[];
}
```

### Sync Service

```typescript
// src/lib/suppliers/ingram/sync.ts
import { db } from '@/lib/db';
import { products, supplierOfferings, syncLog } from '@/lib/db/schema';
import { IngramMicroClient } from './client';
import { eq } from 'drizzle-orm';

export async function syncIngramCatalog(options?: {
  searchTerms?: string[];
  fullSync?: boolean;
}) {
  const client = new IngramMicroClient({
    clientId: process.env.INGRAM_CLIENT_ID!,
    clientSecret: process.env.INGRAM_CLIENT_SECRET!,
    customerNumber: process.env.INGRAM_CUSTOMER_NUMBER!,
  });

  // Log sync start
  const [logEntry] = await db.insert(syncLog).values({
    supplierId: 1, // Ingram
    source: 'ingram',
    syncType: 'catalog',
    status: 'started',
  }).returning();

  try {
    const terms = options?.searchTerms ?? ['laptop', 'desktop', 'gpu', 'monitor'];
    let totalSynced = 0;

    for (const term of terms) {
      let page = 1;
      let hasMore = true;

      while (hasMore) {
        const response = await client.searchCatalog(term, {
          pageNumber: page,
          pageSize: 50,
        });

        for (const item of response.catalog) {
          // Upsert product
          await db.insert(products).values({
            upc: item.upcCode || null,
            mfrPart: item.vendorPartNumber,
            manufacturer: item.vendorName,
            name: item.description,
            category: item.productCategory,
            subcategory: item.productSubcategory,
            msrp: item.msrp,
          }).onConflictDoUpdate({
            target: products.upc,
            set: {
              name: item.description,
              msrp: item.msrp,
              updatedAt: new Date().toISOString(),
            },
          });

          // Get product ID
          const [product] = await db.select()
            .from(products)
            .where(eq(products.upc, item.upcCode))
            .limit(1);

          if (product) {
            // Upsert offering
            for (const wh of item.availability.availabilityByWarehouse) {
              await db.insert(supplierOfferings).values({
                productId: product.id,
                supplierId: 1, // Ingram
                supplierSku: item.ingramPartNumber,
                supplierPart: item.vendorPartNumber,
                cost: item.customerPrice,
                qtyAvailable: wh.quantityAvailable,
                warehouse: wh.warehouseId,
              }).onConflictDoUpdate({
                target: [supplierOfferings.productId, supplierOfferings.supplierId, supplierOfferings.warehouse],
                set: {
                  cost: item.customerPrice,
                  qtyAvailable: wh.quantityAvailable,
                  lastSyncedAt: new Date().toISOString(),
                },
              });
            }
          }

          totalSynced++;
        }

        hasMore = response.catalog.length === 50;
        page++;

        // Rate limiting: 60 req/min
        await new Promise(r => setTimeout(r, 1100));
      }
    }

    // Update sync log
    await db.update(syncLog)
      .set({
        status: 'completed',
        recordsSynced: totalSynced,
        completedAt: new Date().toISOString(),
      })
      .where(eq(syncLog.id, logEntry.id));

    return { success: true, synced: totalSynced };

  } catch (error) {
    await db.update(syncLog)
      .set({
        status: 'failed',
        errorMsg: error instanceof Error ? error.message : 'Unknown error',
        completedAt: new Date().toISOString(),
      })
      .where(eq(syncLog.id, logEntry.id));

    throw error;
  }
}
```

---

## 5. UI Components & Wireframes

### Main Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ [Logo] MHI Procurement    [🔍 Search...]  [Entity: MHI ▼]  [👤] │
├────────────┬────────────────────────────────────────────────────┤
│            │                                                    │
│ 📦 Products│  [Main Content Area]                              │
│ 📊 Compare │                                                    │
│ 📈 Margins │  - Product Grid / Table                           │
│ 🛒 Basket  │  - Price Comparison Cards                         │
│ 📋 Orders  │  - Margin Analysis Dashboard                      │
│ 🔄 Sync    │                                                    │
│ ⚙️ Settings│                                                    │
│            │                                                    │
├────────────┴────────────────────────────────────────────────────┤
│ Basket: 12 items | Total: $4,532.00 | Best Margin: 23.4%        │
└─────────────────────────────────────────────────────────────────┘
```

### Price Comparison View

```tsx
// src/components/comparison/PriceComparisonCard.tsx
interface PriceComparisonCardProps {
  product: Product;
  offerings: SupplierOffering[];
  marketPrices: MarketPrice[];
}

export function PriceComparisonCard({ product, offerings, marketPrices }: PriceComparisonCardProps) {
  const bestOffering = offerings.reduce((best, curr) => 
    curr.cost < best.cost ? curr : best
  );
  
  const bestMarket = marketPrices.length > 0
    ? Math.min(...marketPrices.map(m => m.marketPrice))
    : null;
  
  const margin = bestMarket 
    ? ((bestMarket - bestOffering.cost) / bestMarket * 100).toFixed(1)
    : null;

  return (
    <Card>
      <CardHeader>
        <div className="flex justify-between">
          <div>
            <CardTitle>{product.name}</CardTitle>
            <CardDescription>{product.manufacturer} | {product.mfrPart}</CardDescription>
          </div>
          {margin && (
            <Badge variant={Number(margin) > 20 ? "success" : "secondary"}>
              {margin}% margin
            </Badge>
          )}
        </div>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Supplier</TableHead>
              <TableHead>Cost</TableHead>
              <TableHead>Stock</TableHead>
              <TableHead>Warehouse</TableHead>
              <TableHead></TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {offerings.map((offering) => (
              <TableRow key={offering.id}>
                <TableCell>
                  <div className="flex items-center gap-2">
                    {offering.supplierId === bestOffering.supplierId && (
                      <Badge variant="outline" className="bg-green-50">Best</Badge>
                    )}
                    {offering.supplier.name}
                  </div>
                </TableCell>
                <TableCell className="font-mono">
                  ${offering.cost.toFixed(2)}
                  {offering.promoPrice && (
                    <span className="text-red-500 ml-2">
                      Promo: ${offering.promoPrice.toFixed(2)}
                    </span>
                  )}
                </TableCell>
                <TableCell>{offering.qtyAvailable}</TableCell>
                <TableCell>{offering.warehouse}</TableCell>
                <TableCell>
                  <Button size="sm" onClick={() => addToBasket(offering)}>
                    Add
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        
        {marketPrices.length > 0 && (
          <div className="mt-4 pt-4 border-t">
            <h4 className="font-semibold mb-2">Market Prices</h4>
            <div className="flex gap-4">
              {marketPrices.map((mp) => (
                <div key={mp.id} className="text-sm">
                  <span className="text-muted-foreground">{mp.source}:</span>
                  <span className="font-mono ml-1">${mp.marketPrice.toFixed(2)}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
```

### Margin Analysis Dashboard

```tsx
// src/components/margins/MarginDashboard.tsx
export function MarginDashboard() {
  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-4 gap-4">
        <StatCard 
          title="Products Tracked" 
          value="2,847" 
          trend="+124 this week" 
        />
        <StatCard 
          title="Avg MSRP Margin" 
          value="18.4%" 
          trend="+0.8% vs last month" 
        />
        <StatCard 
          title="Best Opportunity" 
          value="$1,247" 
          subtitle="RTX 4090 FE" 
        />
        <StatCard 
          title="Supplier Spread" 
          value="$89 avg" 
          subtitle="Between best/worst" 
        />
      </div>
      
      {/* Top Margin Products */}
      <Card>
        <CardHeader>
          <CardTitle>Highest Margin Opportunities</CardTitle>
          <CardDescription>Products with best profit potential</CardDescription>
        </CardHeader>
        <CardContent>
          <DataTable 
            columns={marginColumns}
            data={topMarginProducts}
            sorting={[{ id: 'marketMargin', desc: true }]}
          />
        </CardContent>
      </Card>
      
      {/* Margin Distribution Chart */}
      <Card>
        <CardHeader>
          <CardTitle>Margin Distribution by Category</CardTitle>
        </CardHeader>
        <CardContent>
          <BarChart data={marginByCategory} />
        </CardContent>
      </Card>
    </div>
  );
}
```

### Entity Switcher

```tsx
// src/components/layout/EntitySwitcher.tsx
const entities = [
  { id: 'mhi', name: 'Mighty House Inc', accounts: { ingram: '50-135152-000' } },
  { id: 'dsaic', name: 'DSAIC', accounts: { ingram: '50-XXXXX-XXX' } },
  { id: 'computer-store', name: 'Computer Store', accounts: { ingram: '50-YYYYY-YYY' } },
];

export function EntitySwitcher() {
  const [current, setCurrent] = useEntityStore((s) => [s.current, s.setCurrent]);
  
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" className="w-[200px] justify-between">
          {entities.find(e => e.id === current)?.name ?? 'Select Entity'}
          <ChevronsUpDown className="ml-2 h-4 w-4" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent>
        {entities.map((entity) => (
          <DropdownMenuItem 
            key={entity.id}
            onClick={() => setCurrent(entity.id)}
          >
            <Check className={cn(
              "mr-2 h-4 w-4",
              current === entity.id ? "opacity-100" : "opacity-0"
            )} />
            {entity.name}
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
```

---

## 6. Implementation Phases

### Phase 1: Foundation (Week 1)
- [x] Architecture document (this file)
- [ ] Project scaffolding with Next.js 15
- [ ] Database schema with Drizzle ORM
- [ ] Basic auth setup (NextAuth.js)
- [ ] Entity switching mechanism
- [ ] shadcn/ui component library setup

### Phase 2: Core Features (Week 2-3)
- [ ] Product catalog view (table + grid)
- [ ] Search functionality
- [ ] Ingram Micro API integration
  - [ ] OAuth2 client
  - [ ] Catalog search
  - [ ] Price & availability
- [ ] Basic price comparison view

### Phase 3: Supplier Expansion (Week 4)
- [ ] TD SYNNEX integration (if API access available)
- [ ] D&H integration (if API access available)
- [ ] Climb manual entry interface
- [ ] Unified offering view

### Phase 4: Advanced Features (Week 5-6)
- [ ] Margin analysis dashboard
- [ ] Shopping basket
- [ ] Purchase order creation
- [ ] Order tracking
- [ ] Sync status dashboard
- [ ] Market price integration (Best Buy, eBay)

### Phase 5: Polish (Week 7)
- [ ] Testing (Vitest + Playwright)
- [ ] Performance optimization
- [ ] Documentation
- [ ] Deployment (Vercel or self-hosted)

---

## 7. Environment Variables

```env
# Database
DATABASE_URL="file:./procurement.db"
# Or for Postgres:
# DATABASE_URL="postgresql://user:pass@localhost:5432/procurement"

# Auth
NEXTAUTH_URL="http://localhost:3000"
NEXTAUTH_SECRET="your-secret-key"

# Ingram Micro
INGRAM_CLIENT_ID="your-client-id"
INGRAM_CLIENT_SECRET="your-client-secret"
INGRAM_CUSTOMER_NUMBER="50-135152-000"
INGRAM_API_BASE="https://api.ingrammicro.com"
# Use sandbox for dev:
# INGRAM_API_BASE="https://api.ingrammicro.com/sandbox"

# TD SYNNEX (when available)
SYNNEX_API_KEY=""
SYNNEX_ACCOUNT=""

# D&H (when available)
DANDH_API_KEY=""
DANDH_ACCOUNT=""
```

---

## 8. Commands Reference

```bash
# Development
npm run dev              # Start dev server
npm run db:push          # Push schema to DB
npm run db:studio        # Open Drizzle Studio
npm run db:seed          # Seed initial data

# Testing
npm run test             # Run unit tests
npm run test:e2e         # Run E2E tests
npm run test:coverage    # Coverage report

# Production
npm run build            # Build for production
npm run start            # Start production server

# Sync
npm run sync:ingram      # Sync Ingram catalog
npm run sync:all         # Sync all suppliers
```

---

## 9. Next Steps

1. **Create the project** at `C:\mhi-procurement-web\`
2. **Scaffold Next.js 15** with TypeScript
3. **Set up Drizzle ORM** with SQLite (dev) / Postgres (prod)
4. **Install shadcn/ui** components
5. **Implement Ingram Micro client** first (best documented)
6. **Build price comparison UI**

---

## Appendix A: Existing C App Compatibility

The web app can **share the same SQLite database** as the C desktop app:

```
C:\mhi-procurement\procurement.db  ← Same file
```

Both can read/write to it. WAL mode enables concurrent access.

For production, migrate to Postgres and both apps connect to the same DB.

---

## Appendix B: Supplier API Documentation

| Supplier | Docs | Notes |
|----------|------|-------|
| Ingram Micro | [developer.ingrammicro.com](https://developer.ingrammicro.com/) | Best documented, OpenAPI specs on GitHub |
| TD SYNNEX | Partner portal only | Digital Bridge + StreamOne Ion |
| D&H | Partner portal only | REST OAS3 |
| Climb | N/A | No API — manual entry or portal scraping |

---

*Document generated: 2026-02-09*  
*Project: MHI Procurement Web*  
*Author: WebDev Agent*
