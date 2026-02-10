# MHI Procurement App — Test Coverage Plan

**Version:** 1.0  
**Date:** 2026-02-09  
**Application:** Multi-Supplier Procurement & Quoting System  

---

## 1. Executive Summary

This document outlines the comprehensive test strategy for the MHI Procurement web application. The system handles real-time price comparison across four distributors (Ingram, SYNNEX, D&H, Climb), supports three business entities (MHI, DSAIC, Computer Store), and generates quotes with calculated margins.

**Testing Pyramid Target:**
- Unit Tests: 70% coverage (fast, isolated)
- Integration Tests: 20% coverage (API contracts, service interactions)
- E2E Tests: 10% coverage (critical user workflows)

---

## 2. Unit Tests

### 2.1 Margin Calculation Functions

```typescript
// test/unit/margin.test.ts
describe('MarginCalculator', () => {
  describe('calculateMargin()', () => {
    it('calculates percentage margin correctly')
    it('calculates dollar margin correctly')
    it('handles zero cost (division by zero)')
    it('applies entity-specific margin rules')
    it('applies tiered margin based on quantity')
    it('respects minimum margin thresholds')
    it('caps maximum margin per entity policy')
  })
  
  describe('calculateSellPrice()', () => {
    it('applies target margin to cost')
    it('rounds to configured decimal places')
    it('applies entity-specific pricing rules')
  })
})
```

**Test Cases:**

| Function | Input | Expected Output | Notes |
|----------|-------|-----------------|-------|
| `calculateMargin(100, 120)` | cost=100, sell=120 | 20% | Standard margin |
| `calculateMargin(0, 50)` | cost=0, sell=50 | `Infinity` or error | Edge case |
| `calculateMargin(100, 100)` | cost=100, sell=100 | 0% | Zero margin |
| `calculateMargin(100, 80)` | cost=100, sell=80 | -20% | Negative margin |

### 2.2 Price Comparison Utilities

```typescript
// test/unit/price-comparison.test.ts
describe('PriceComparisonService', () => {
  describe('findLowestPrice()', () => {
    it('returns lowest price from multiple distributors')
    it('handles single distributor response')
    it('handles empty responses array')
    it('breaks ties with distributor priority')
    it('excludes out-of-stock items from comparison')
    it('handles null/undefined prices gracefully')
  })
  
  describe('normalizeDistributorResponse()', () => {
    it('normalizes Ingram response format')
    it('normalizes SYNNEX response format')
    it('normalizes D&H response format')
    it('normalizes Climb response format')
  })
  
  describe('compareAvailability()', () => {
    it('aggregates stock across all distributors')
    it('calculates lead times correctly')
    it('prioritizes in-stock over drop-ship')
  })
})
```

### 2.3 Quote Generation Utilities

```typescript
// test/unit/quote.test.ts
describe('QuoteBuilder', () => {
  describe('generateQuoteNumber()', () => {
    it('generates unique quote numbers')
    it('includes entity prefix (MHI-, DSA-, CS-)')
    it('includes sequential counter')
    it('includes date component')
  })
  
  describe('calculateQuoteTotals()', () => {
    it('sums line items correctly')
    it('applies quantity discounts')
    it('calculates tax by entity tax rules')
    it('handles multi-currency (if applicable)')
  })
  
  describe('validateQuote()', () => {
    it('rejects quotes with negative margins below threshold')
    it('requires customer information')
    it('validates line item quantities > 0')
  })
})
```

### 2.4 Entity & Credential Utilities

```typescript
// test/unit/entity.test.ts
describe('EntityService', () => {
  describe('getEntityConfig()', () => {
    it('returns MHI configuration')
    it('returns DSAIC configuration')
    it('returns Computer Store configuration')
    it('throws for unknown entity')
  })
  
  describe('getDistributorCredentials()', () => {
    it('returns entity-specific Ingram credentials')
    it('returns entity-specific SYNNEX credentials')
    it('returns entity-specific D&H credentials')
    it('returns entity-specific Climb credentials')
    it('masks sensitive credential data in logs')
  })
})
```

### 2.5 Data Transformation & Validation

```typescript
// test/unit/transformers.test.ts
describe('DataTransformers', () => {
  describe('parsePartNumber()', () => {
    it('normalizes part numbers (uppercase, trim)')
    it('handles manufacturer prefixes')
    it('validates part number format')
  })
  
  describe('formatCurrency()', () => {
    it('formats USD correctly')
    it('handles negative values')
    it('respects locale settings')
  })
})
```

---

## 3. Integration Tests

### 3.1 Distributor API Mocking Strategy

Use **MSW (Mock Service Worker)** or **nock** for HTTP mocking:

```typescript
// test/integration/setup.ts
import { setupServer } from 'msw/node'
import { ingramHandlers } from './mocks/ingram'
import { synnexHandlers } from './mocks/synnex'
import { dhHandlers } from './mocks/dh'
import { climbHandlers } from './mocks/climb'

export const server = setupServer(
  ...ingramHandlers,
  ...synnexHandlers,
  ...dhHandlers,
  ...climbHandlers
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

### 3.2 Ingram Micro API Integration

```typescript
// test/integration/ingram.test.ts
describe('IngramAPIClient', () => {
  describe('authenticate()', () => {
    it('obtains OAuth token successfully')
    it('handles invalid credentials')
    it('refreshes expired tokens')
  })
  
  describe('searchProducts()', () => {
    it('returns product details for valid SKU')
    it('handles product not found')
    it('paginates large result sets')
  })
  
  describe('getPriceAndAvailability()', () => {
    it('returns real-time pricing')
    it('includes branch-level availability')
    it('handles partial responses')
  })
  
  describe('Rate Limiting', () => {
    it('respects X-RateLimit-Remaining header')
    it('implements exponential backoff on 429')
    it('queues requests when approaching limit')
  })
})
```

### 3.3 SYNNEX API Integration

```typescript
// test/integration/synnex.test.ts
describe('SYNNEXAPIClient', () => {
  describe('authenticate()', () => {
    it('authenticates via XML/SOAP endpoint')
    it('handles session expiration')
  })
  
  describe('priceCheck()', () => {
    it('returns pricing for valid MFR part')
    it('handles discontinued products')
    it('returns warehouse availability')
  })
  
  describe('Error Handling', () => {
    it('parses SOAP fault responses')
    it('retries on transient errors')
    it('handles timeout gracefully')
  })
})
```

### 3.4 D&H API Integration

```typescript
// test/integration/dh.test.ts
describe('DHAPIClient', () => {
  describe('lookupProduct()', () => {
    it('returns product by D&H item number')
    it('returns product by UPC')
    it('returns product by MFR part number')
  })
  
  describe('checkInventory()', () => {
    it('returns multi-warehouse availability')
    it('includes ETA for backordered items')
  })
})
```

### 3.5 Climb API Integration

```typescript
// test/integration/climb.test.ts
describe('ClimbAPIClient', () => {
  describe('productSearch()', () => {
    it('returns pricing for software licenses')
    it('handles subscription vs perpetual pricing')
  })
  
  describe('licensing()', () => {
    it('validates license eligibility')
    it('returns volume discount tiers')
  })
})
```

### 3.6 Multi-Entity Credential Tests

```typescript
// test/integration/multi-entity.test.ts
describe('Multi-Entity API Access', () => {
  describe('Credential Isolation', () => {
    it('MHI uses MHI-specific Ingram account')
    it('DSAIC uses DSAIC-specific Ingram account')
    it('Computer Store uses CS-specific Ingram account')
    it('credentials do not leak between entities')
  })
  
  describe('Concurrent Entity Requests', () => {
    it('handles parallel requests from different entities')
    it('maintains credential context per request')
  })
})
```

### 3.7 Database Integration (if applicable)

```typescript
// test/integration/database.test.ts
describe('QuoteRepository', () => {
  it('persists quote to database')
  it('retrieves quote by ID')
  it('updates quote status')
  it('soft-deletes expired quotes')
})
```

---

## 4. End-to-End Tests

### 4.1 E2E Framework

Use **Playwright** for browser automation:

```typescript
// playwright.config.ts
export default defineConfig({
  testDir: './test/e2e',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure'
  },
  projects: [
    { name: 'chromium', use: { browserName: 'chromium' } },
    { name: 'firefox', use: { browserName: 'firefox' } }
  ]
})
```

### 4.2 Full Quote Workflow

```typescript
// test/e2e/quote-workflow.spec.ts
describe('Quote Generation Workflow', () => {
  test('complete quote creation flow', async ({ page }) => {
    // 1. Login as MHI user
    await page.goto('/login')
    await page.fill('[data-testid="email"]', 'user@mhi.com')
    await page.fill('[data-testid="password"]', 'testpass')
    await page.click('[data-testid="login-btn"]')
    
    // 2. Search for product
    await page.fill('[data-testid="product-search"]', 'HP EliteBook 850')
    await page.click('[data-testid="search-btn"]')
    
    // 3. Wait for distributor price comparison
    await page.waitForSelector('[data-testid="price-comparison-table"]')
    
    // 4. Select best price
    await page.click('[data-testid="select-lowest-price"]')
    
    // 5. Set margin and add to quote
    await page.fill('[data-testid="margin-input"]', '15')
    await page.click('[data-testid="add-to-quote"]')
    
    // 6. Complete quote
    await page.click('[data-testid="finalize-quote"]')
    await page.fill('[data-testid="customer-name"]', 'Test Customer')
    await page.click('[data-testid="generate-quote"]')
    
    // 7. Verify quote generated
    await expect(page.locator('[data-testid="quote-number"]')).toBeVisible()
  })
  
  test('handles distributor API failure gracefully', async ({ page }) => {
    // Mock Ingram to fail
    await page.route('**/api/ingram/**', route => 
      route.fulfill({ status: 503 })
    )
    
    await page.goto('/search')
    await page.fill('[data-testid="product-search"]', 'Dell Latitude')
    await page.click('[data-testid="search-btn"]')
    
    // Should show results from other distributors
    await expect(page.locator('[data-testid="ingram-error"]')).toContainText('Unavailable')
    await expect(page.locator('[data-testid="synnex-price"]')).toBeVisible()
  })
})
```

### 4.3 Multi-Entity Switching

```typescript
// test/e2e/entity-switching.spec.ts
describe('Entity Context Switching', () => {
  test('user can switch between entities', async ({ page }) => {
    await loginAs(page, 'multi-entity-user@test.com')
    
    // Start in MHI context
    await expect(page.locator('[data-testid="entity-badge"]')).toContainText('MHI')
    
    // Switch to DSAIC
    await page.click('[data-testid="entity-selector"]')
    await page.click('[data-testid="entity-dsaic"]')
    
    // Verify context change
    await expect(page.locator('[data-testid="entity-badge"]')).toContainText('DSAIC')
    
    // Verify pricing reflects DSAIC contracts
    await page.fill('[data-testid="product-search"]', 'Cisco Switch')
    await page.click('[data-testid="search-btn"]')
    
    // DSAIC may have different contract pricing
    await expect(page.locator('[data-testid="contract-pricing"]')).toBeVisible()
  })
})
```

### 4.4 Critical Path Tests

| Test | Priority | Description |
|------|----------|-------------|
| Login → Search → Quote | P0 | Core happy path |
| Price comparison accuracy | P0 | Lowest price selected correctly |
| Margin calculation display | P0 | Sell price reflects margin |
| Quote PDF generation | P1 | PDF renders correctly |
| Entity switching | P1 | Credentials update on switch |
| Bulk product search | P2 | CSV upload for multiple SKUs |

---

## 5. Test Data Strategy

### 5.1 Mock Distributor Responses

Create realistic mock responses for each distributor:

```
test/
  fixtures/
    ingram/
      product-hp-elitebook.json
      product-not-found.json
      price-availability-multi.json
      auth-token.json
      rate-limit-exceeded.json
    synnex/
      price-check-response.xml
      soap-fault.xml
    dh/
      inventory-lookup.json
      product-detail.json
    climb/
      software-pricing.json
      license-validation.json
```

### 5.2 Sample Mock Response (Ingram)

```json
// test/fixtures/ingram/product-hp-elitebook.json
{
  "responseCode": "SUCCESS",
  "products": [
    {
      "ingramPartNumber": "ABC123",
      "vendorPartNumber": "5Y3T1UT#ABA",
      "description": "HP EliteBook 850 G8 15.6\" Notebook",
      "vendorName": "HP INC",
      "upcCode": "195697674563",
      "pricing": {
        "customerPrice": 1249.99,
        "retailPrice": 1499.99,
        "specialPriceFlag": false
      },
      "availability": {
        "totalAvailability": 47,
        "warehouseDetails": [
          { "warehouseId": "10", "quantityAvailable": 25, "location": "Mira Loma, CA" },
          { "warehouseId": "40", "quantityAvailable": 22, "location": "Jonestown, PA" }
        ]
      }
    }
  ]
}
```

### 5.3 Mock Response (SYNNEX SOAP)

```xml
<!-- test/fixtures/synnex/price-check-response.xml -->
<soap:Envelope>
  <soap:Body>
    <PriceCheckResponse>
      <Product>
        <SKU>4829371</SKU>
        <MfgPN>5Y3T1UT#ABA</MfgPN>
        <Price>1262.45</Price>
        <QtyAvailable>18</QtyAvailable>
        <Warehouse>Greenville, SC</Warehouse>
      </Product>
    </PriceCheckResponse>
  </soap:Body>
</soap:Envelope>
```

### 5.4 Test Data Factories

```typescript
// test/factories/quote.factory.ts
import { faker } from '@faker-js/faker'

export const createMockQuote = (overrides = {}) => ({
  id: faker.string.uuid(),
  quoteNumber: `MHI-${faker.number.int({ min: 10000, max: 99999 })}`,
  customer: {
    name: faker.company.name(),
    email: faker.internet.email(),
    phone: faker.phone.number()
  },
  lineItems: [createMockLineItem()],
  totals: {
    subtotal: 0,
    tax: 0,
    total: 0
  },
  createdAt: faker.date.recent(),
  expiresAt: faker.date.future(),
  ...overrides
})

export const createMockLineItem = (overrides = {}) => ({
  id: faker.string.uuid(),
  partNumber: faker.string.alphanumeric(10).toUpperCase(),
  description: faker.commerce.productName(),
  quantity: faker.number.int({ min: 1, max: 10 }),
  cost: parseFloat(faker.commerce.price({ min: 100, max: 2000 })),
  sellPrice: 0, // calculated
  margin: 15,
  distributor: faker.helpers.arrayElement(['Ingram', 'SYNNEX', 'D&H', 'Climb']),
  ...overrides
})
```

### 5.5 Seed Data Script

```typescript
// scripts/seed-test-data.ts
async function seedTestData() {
  // Create test users for each entity
  await createUser({ email: 'mhi-user@test.com', entity: 'MHI' })
  await createUser({ email: 'dsaic-user@test.com', entity: 'DSAIC' })
  await createUser({ email: 'cs-user@test.com', entity: 'ComputerStore' })
  await createUser({ email: 'multi-user@test.com', entities: ['MHI', 'DSAIC', 'ComputerStore'] })
  
  // Create sample quotes for testing retrieval
  await createQuote({ entity: 'MHI', status: 'draft' })
  await createQuote({ entity: 'MHI', status: 'sent' })
  await createQuote({ entity: 'DSAIC', status: 'accepted' })
}
```

---

## 6. Error Handling Tests

### 6.1 API Failure Scenarios

```typescript
// test/integration/error-handling.test.ts
describe('Distributor API Error Handling', () => {
  describe('Network Failures', () => {
    it('handles connection timeout', async () => {
      server.use(
        rest.get('/api/ingram/*', (req, res, ctx) => 
          res(ctx.delay('infinite'))
        )
      )
      
      const result = await priceService.fetchPrices('ABC123')
      expect(result.ingram.error).toBe('TIMEOUT')
      expect(result.synnex.price).toBeDefined() // Others still work
    })
    
    it('handles connection refused', async () => {
      server.use(
        rest.get('/api/ingram/*', (req, res) => 
          res.networkError('Connection refused')
        )
      )
      
      const result = await priceService.fetchPrices('ABC123')
      expect(result.ingram.error).toBe('NETWORK_ERROR')
    })
  })
  
  describe('HTTP Errors', () => {
    it('handles 401 Unauthorized - triggers re-auth', async () => {
      const authSpy = jest.spyOn(ingramClient, 'authenticate')
      
      server.use(
        rest.get('/api/ingram/prices', (req, res, ctx) => 
          res.once(ctx.status(401))
        )
      )
      
      await priceService.fetchPrices('ABC123')
      expect(authSpy).toHaveBeenCalledTimes(2) // Initial + retry
    })
    
    it('handles 403 Forbidden - no retry', async () => {
      server.use(
        rest.get('/api/ingram/prices', (req, res, ctx) => 
          res(ctx.status(403), ctx.json({ error: 'Access denied' }))
        )
      )
      
      await expect(priceService.fetchPrices('ABC123'))
        .rejects.toThrow('ACCESS_DENIED')
    })
    
    it('handles 500 Server Error - retries with backoff', async () => {
      let attempts = 0
      server.use(
        rest.get('/api/ingram/prices', (req, res, ctx) => {
          attempts++
          if (attempts < 3) return res(ctx.status(500))
          return res(ctx.json({ price: 100 }))
        })
      )
      
      const result = await priceService.fetchPrices('ABC123')
      expect(attempts).toBe(3)
      expect(result.ingram.price).toBe(100)
    })
    
    it('handles 503 Service Unavailable', async () => {
      server.use(
        rest.get('/api/ingram/prices', (req, res, ctx) => 
          res(ctx.status(503))
        )
      )
      
      const result = await priceService.fetchPrices('ABC123')
      expect(result.ingram.error).toBe('SERVICE_UNAVAILABLE')
    })
  })
  
  describe('Invalid Response Handling', () => {
    it('handles malformed JSON', async () => {
      server.use(
        rest.get('/api/ingram/prices', (req, res, ctx) => 
          res(ctx.body('not json'))
        )
      )
      
      const result = await priceService.fetchPrices('ABC123')
      expect(result.ingram.error).toBe('PARSE_ERROR')
    })
    
    it('handles missing required fields', async () => {
      server.use(
        rest.get('/api/ingram/prices', (req, res, ctx) => 
          res(ctx.json({ unexpected: 'format' }))
        )
      )
      
      const result = await priceService.fetchPrices('ABC123')
      expect(result.ingram.error).toBe('INVALID_RESPONSE')
    })
  })
})
```

### 6.2 Rate Limit Testing

```typescript
// test/integration/rate-limits.test.ts
describe('Rate Limit Handling', () => {
  describe('Ingram Rate Limits', () => {
    it('respects rate limit headers', async () => {
      server.use(
        rest.get('/api/ingram/prices', (req, res, ctx) => 
          res(
            ctx.set('X-RateLimit-Remaining', '5'),
            ctx.set('X-RateLimit-Reset', String(Date.now() + 60000)),
            ctx.json({ price: 100 })
          )
        )
      )
      
      await priceService.fetchPrices('ABC123')
      expect(rateLimiter.getRemaining('ingram')).toBe(5)
    })
    
    it('queues requests when approaching limit', async () => {
      rateLimiter.setRemaining('ingram', 1)
      
      const promise1 = priceService.fetchPrices('ABC123')
      const promise2 = priceService.fetchPrices('DEF456')
      
      // Second request should be queued
      expect(rateLimiter.getQueueLength('ingram')).toBe(1)
      
      await Promise.all([promise1, promise2])
    })
    
    it('handles 429 with Retry-After', async () => {
      server.use(
        rest.get('/api/ingram/prices', (req, res, ctx) => 
          res.once(
            ctx.status(429),
            ctx.set('Retry-After', '2')
          )
        )
      )
      
      const start = Date.now()
      await priceService.fetchPrices('ABC123')
      const elapsed = Date.now() - start
      
      expect(elapsed).toBeGreaterThanOrEqual(2000)
    })
  })
  
  describe('Concurrent Request Limits', () => {
    it('limits concurrent requests per distributor', async () => {
      const concurrentLimit = 5
      const requests = Array(10).fill(null).map((_, i) => 
        priceService.fetchPrices(`PART${i}`)
      )
      
      // Check that max 5 are in-flight at once
      expect(requestTracker.getInFlight('ingram')).toBeLessThanOrEqual(5)
      
      await Promise.all(requests)
    })
  })
})
```

---

## 7. CI/CD Integration

### 7.1 GitHub Actions Workflow

```yaml
# .github/workflows/test.yml
name: Test Suite

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - run: npm ci
      - run: npm run test:unit -- --coverage
      
      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage/lcov.info
          flags: unit

  integration-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - run: npm ci
      - run: npm run test:integration
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/test
      
      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage/lcov.info
          flags: integration

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - run: npm ci
      - run: npx playwright install --with-deps
      
      - name: Start application
        run: npm run build && npm run start &
        env:
          NODE_ENV: test
      
      - name: Wait for app
        run: npx wait-on http://localhost:3000
      
      - run: npm run test:e2e
      
      - name: Upload Playwright report
        uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/

  coverage-gate:
    needs: [unit-tests, integration-tests]
    runs-on: ubuntu-latest
    steps:
      - name: Check coverage threshold
        run: |
          # Enforce minimum 80% coverage
          if [ "$COVERAGE" -lt 80 ]; then
            echo "Coverage $COVERAGE% is below 80% threshold"
            exit 1
          fi
```

### 7.2 Test Scripts (package.json)

```json
{
  "scripts": {
    "test": "npm run test:unit && npm run test:integration",
    "test:unit": "vitest run --config vitest.unit.config.ts",
    "test:integration": "vitest run --config vitest.integration.config.ts",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:coverage": "vitest run --coverage",
    "test:watch": "vitest watch"
  }
}
```

### 7.3 Vitest Configuration

```typescript
// vitest.unit.config.ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    include: ['test/unit/**/*.test.ts'],
    environment: 'node',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov', 'html'],
      thresholds: {
        statements: 80,
        branches: 75,
        functions: 80,
        lines: 80
      }
    }
  }
})
```

```typescript
// vitest.integration.config.ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    include: ['test/integration/**/*.test.ts'],
    environment: 'node',
    setupFiles: ['./test/integration/setup.ts'],
    testTimeout: 30000,
    hookTimeout: 30000
  }
})
```

### 7.4 Pre-commit Hooks

```json
// .husky/pre-commit
npm run test:unit -- --run
npm run lint
```

---

## 8. Coverage Goals & Metrics

### 8.1 Coverage Targets by Area

| Area | Target | Critical Files |
|------|--------|----------------|
| Margin Calculations | 100% | `src/lib/margin.ts` |
| Price Comparison | 95% | `src/services/price-comparison.ts` |
| API Clients | 90% | `src/clients/*.ts` |
| Quote Generation | 90% | `src/services/quote.ts` |
| Entity Management | 85% | `src/services/entity.ts` |
| UI Components | 70% | `src/components/*.tsx` |
| Utility Functions | 80% | `src/utils/*.ts` |

### 8.2 Quality Gates

- **PR Merge Requirements:**
  - All tests passing
  - No decrease in coverage %
  - No new critical/high security vulnerabilities
  - E2E critical path tests green

- **Release Requirements:**
  - Full test suite passing
  - Overall coverage ≥ 80%
  - All P0 E2E tests passing
  - Performance benchmarks within threshold

---

## 9. Test Environment Setup

### 9.1 Local Development

```bash
# Install dependencies
npm install

# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run E2E tests with UI
npm run test:e2e:ui
```

### 9.2 Environment Variables (Test)

```bash
# .env.test
NODE_ENV=test
DATABASE_URL=postgres://localhost:5432/procurement_test

# Mock API endpoints (optional - MSW handles most mocking)
INGRAM_API_URL=http://localhost:3001/mock/ingram
SYNNEX_API_URL=http://localhost:3001/mock/synnex

# Disable external calls
ENABLE_EXTERNAL_APIS=false
```

### 9.3 Docker Test Environment

```yaml
# docker-compose.test.yml
version: '3.8'
services:
  test-db:
    image: postgres:15
    environment:
      POSTGRES_DB: procurement_test
      POSTGRES_PASSWORD: test
    ports:
      - "5433:5432"
  
  test-runner:
    build:
      context: .
      dockerfile: Dockerfile.test
    depends_on:
      - test-db
    environment:
      DATABASE_URL: postgres://postgres:test@test-db:5432/procurement_test
    volumes:
      - ./coverage:/app/coverage
```

---

## 10. Appendix

### A. Test Naming Conventions

```
describe('[Module/Component Name]', () => {
  describe('[method/feature]', () => {
    it('[should/does] [expected behavior] [when/given condition]')
  })
})

Examples:
- "calculates margin correctly when cost is zero"
- "returns lowest price given multiple distributor responses"
- "retries request when receiving 503 status"
```

### B. Mock Data Locations

```
test/
├── fixtures/           # Static mock responses
│   ├── ingram/
│   ├── synnex/
│   ├── dh/
│   └── climb/
├── factories/          # Dynamic test data generators
├── mocks/              # MSW handlers
└── helpers/            # Shared test utilities
```

### C. Key Testing Libraries

| Library | Purpose | Version |
|---------|---------|---------|
| Vitest | Unit/Integration test runner | ^1.0 |
| Playwright | E2E browser automation | ^1.40 |
| MSW | API mocking | ^2.0 |
| @faker-js/faker | Test data generation | ^8.0 |
| @testing-library/react | Component testing | ^14.0 |

---

## Approval

| Role | Name | Date |
|------|------|------|
| Author | | 2026-02-09 |
| Tech Lead | | |
| QA Lead | | |
