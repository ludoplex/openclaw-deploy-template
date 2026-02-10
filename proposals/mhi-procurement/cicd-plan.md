# MHI Procurement App — CI/CD Pipeline Plan

**Date:** 2026-02-09  
**Status:** PLANNING  
**Context:** TypeScript full-stack app with multi-distributor API integrations (Ingram, TD SYNNEX, D&H, Climb) and multi-entity support (MHI, DSAIC, Computer Store)

---

## Executive Summary

This document outlines the CI/CD pipeline architecture for the MHI Procurement application. The design prioritizes:

1. **Safe credential management** — 12+ API credential sets (4 distributors × 3 entities)
2. **Phased testing** — Mock APIs in CI, live validation in staging
3. **Multi-entity isolation** — Prevent credential cross-contamination
4. **Rate limit awareness** — Avoid hitting distributor API limits during CI

---

## 1. GitHub Actions Workflow Structure

### Repository Layout

```
.github/
├── workflows/
│   ├── ci.yml                 # Main CI pipeline (PRs + main)
│   ├── deploy-staging.yml     # Deploy to staging
│   ├── deploy-prod.yml        # Deploy to production
│   ├── nightly.yml            # Nightly integration tests
│   └── credential-rotation.yml # Scheduled credential validation
├── actions/
│   └── setup-test-env/        # Composite action for test environment
└── CODEOWNERS
```

### Workflow Triggers

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `ci.yml` | Push to any branch, PRs | Build, lint, unit tests |
| `deploy-staging.yml` | Push to `main` | Auto-deploy to staging |
| `deploy-prod.yml` | GitHub Release / Manual | Production deployment |
| `nightly.yml` | `cron: 0 6 * * *` (6 AM UTC) | Live API integration tests |
| `credential-rotation.yml` | `cron: 0 0 1 * *` (Monthly) | Validate all credentials |

---

## 2. Main CI Pipeline (`ci.yml`)

```yaml
name: CI

on:
  push:
    branches: ['**']
  pull_request:
    branches: [main, develop]

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

env:
  NODE_VERSION: '20'
  PNPM_VERSION: '9'

jobs:
  # ─────────────────────────────────────────────────────────
  # Stage 1: Quick Checks (< 2 min)
  # ─────────────────────────────────────────────────────────
  lint:
    name: Lint & Format
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: pnpm/action-setup@v3
        with:
          version: ${{ env.PNPM_VERSION }}
      
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'pnpm'
      
      - run: pnpm install --frozen-lockfile
      
      - name: TypeScript Check
        run: pnpm tsc --noEmit
      
      - name: ESLint
        run: pnpm lint
      
      - name: Prettier Check
        run: pnpm format:check

  # ─────────────────────────────────────────────────────────
  # Stage 2: Build
  # ─────────────────────────────────────────────────────────
  build:
    name: Build
    runs-on: ubuntu-latest
    needs: [lint]
    steps:
      - uses: actions/checkout@v4
      
      - uses: pnpm/action-setup@v3
        with:
          version: ${{ env.PNPM_VERSION }}
      
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'pnpm'
      
      - run: pnpm install --frozen-lockfile
      
      - name: Build Application
        run: pnpm build
        env:
          # Build-time only (no secrets)
          NEXT_PUBLIC_APP_VERSION: ${{ github.sha }}
      
      - name: Upload Build Artifacts
        uses: actions/upload-artifact@v4
        with:
          name: build-output
          path: |
            .next/
            dist/
          retention-days: 7

  # ─────────────────────────────────────────────────────────
  # Stage 3: Unit Tests (Parallel by domain)
  # ─────────────────────────────────────────────────────────
  test-unit:
    name: Unit Tests
    runs-on: ubuntu-latest
    needs: [lint]
    strategy:
      fail-fast: false
      matrix:
        shard: [1, 2, 3]
    steps:
      - uses: actions/checkout@v4
      
      - uses: pnpm/action-setup@v3
        with:
          version: ${{ env.PNPM_VERSION }}
      
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'pnpm'
      
      - run: pnpm install --frozen-lockfile
      
      - name: Run Unit Tests (Shard ${{ matrix.shard }}/3)
        run: pnpm test:unit --shard=${{ matrix.shard }}/3
        env:
          CI: true
      
      - name: Upload Coverage
        uses: codecov/codecov-action@v4
        if: matrix.shard == 1
        with:
          token: ${{ secrets.CODECOV_TOKEN }}

  # ─────────────────────────────────────────────────────────
  # Stage 4: Integration Tests (Mock APIs)
  # ─────────────────────────────────────────────────────────
  test-integration:
    name: Integration Tests (Mocked)
    runs-on: ubuntu-latest
    needs: [build]
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: procurement_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    steps:
      - uses: actions/checkout@v4
      
      - uses: pnpm/action-setup@v3
        with:
          version: ${{ env.PNPM_VERSION }}
      
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'pnpm'
      
      - run: pnpm install --frozen-lockfile
      
      - name: Run Migrations
        run: pnpm db:migrate
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/procurement_test
      
      - name: Run Integration Tests
        run: pnpm test:integration
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/procurement_test
          # Mock API mode - no real credentials
          API_MODE: mock
          MOCK_API_DELAY_MS: 50

  # ─────────────────────────────────────────────────────────
  # Stage 5: E2E Tests (Mock APIs)
  # ─────────────────────────────────────────────────────────
  test-e2e:
    name: E2E Tests
    runs-on: ubuntu-latest
    needs: [build]
    steps:
      - uses: actions/checkout@v4
      
      - uses: pnpm/action-setup@v3
        with:
          version: ${{ env.PNPM_VERSION }}
      
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'pnpm'
      
      - run: pnpm install --frozen-lockfile
      
      - name: Install Playwright
        run: pnpm exec playwright install --with-deps chromium
      
      - name: Download Build Artifacts
        uses: actions/download-artifact@v4
        with:
          name: build-output
      
      - name: Run E2E Tests
        run: pnpm test:e2e
        env:
          API_MODE: mock
          BASE_URL: http://localhost:3000
      
      - name: Upload Test Results
        uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/

  # ─────────────────────────────────────────────────────────
  # Gate: All Tests Pass
  # ─────────────────────────────────────────────────────────
  ci-pass:
    name: CI Pass
    runs-on: ubuntu-latest
    needs: [build, test-unit, test-integration, test-e2e]
    if: always()
    steps:
      - name: Check Results
        run: |
          if [[ "${{ needs.build.result }}" != "success" ]] ||
             [[ "${{ needs.test-unit.result }}" != "success" ]] ||
             [[ "${{ needs.test-integration.result }}" != "success" ]] ||
             [[ "${{ needs.test-e2e.result }}" != "success" ]]; then
            echo "One or more jobs failed"
            exit 1
          fi
          echo "All CI checks passed!"
```

---

## 3. Build and Lint Stages

### Tooling Recommendations

| Tool | Purpose | Config File |
|------|---------|-------------|
| **TypeScript** | Type checking | `tsconfig.json` |
| **ESLint** | Code linting | `eslint.config.js` (flat config) |
| **Prettier** | Code formatting | `.prettierrc` |
| **Vitest** | Unit/integration tests | `vitest.config.ts` |
| **Playwright** | E2E tests | `playwright.config.ts` |

### `package.json` Scripts

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "test": "vitest",
    "test:unit": "vitest run --project unit",
    "test:integration": "vitest run --project integration",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "db:migrate": "prisma migrate deploy",
    "db:push": "prisma db push",
    "typecheck": "tsc --noEmit"
  }
}
```

### Lint Rules for Procurement Domain

```js
// eslint.config.js additions
export default [
  // ... base config
  {
    rules: {
      // Enforce explicit return types for API client methods
      '@typescript-eslint/explicit-function-return-type': ['error', {
        allowExpressions: true,
        allowedNames: ['getServerSideProps', 'getStaticProps']
      }],
      
      // Prevent accidental credential logging
      'no-console': ['error', { allow: ['warn', 'error'] }],
      
      // Enforce error handling on API calls
      '@typescript-eslint/no-floating-promises': 'error',
    }
  }
];
```

---

## 4. Test Stages

### Test Pyramid

```
                    ┌─────────┐
                    │   E2E   │  ← 5-10 critical user flows
                    │ (< 20)  │
                   ┌┴─────────┴┐
                   │Integration│  ← API clients, database
                   │  (50-100) │
                  ┌┴───────────┴┐
                  │  Unit Tests │  ← Business logic, utils
                  │  (200-500)  │
                  └─────────────┘
```

### Unit Tests

**What to test:**
- Price calculation logic
- Margin computation
- Tax calculations (entity-specific)
- Data normalization (SKU mapping across distributors)
- Validation schemas
- Utility functions

**Example structure:**
```
src/
├── lib/
│   ├── pricing/
│   │   ├── calculate-margin.ts
│   │   └── calculate-margin.test.ts    # Unit test
│   ├── distributors/
│   │   ├── ingram/
│   │   │   ├── client.ts
│   │   │   └── client.test.ts          # Integration test (mocked)
│   │   └── normalize.ts
│   │   └── normalize.test.ts           # Unit test
```

### Integration Tests

**What to test:**
- Distributor API client logic (with mocked HTTP responses)
- Database operations
- Multi-entity credential loading
- Caching behavior
- Error handling and retries

**Mock API Strategy:**

```typescript
// src/lib/distributors/ingram/client.test.ts
import { IngramClient } from './client';
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';

const server = setupServer(
  http.post('https://api.ingrammicro.com/*/catalog/priceandavailability', () => {
    return HttpResponse.json({
      productDetails: [{
        ingramPartNumber: 'ABC123',
        vendorPartNumber: 'MFG-ABC123',
        vendorName: 'ACME Corp',
        productDescription: 'Widget Pro',
        availability: {
          available: true,
          quantityAvailable: 150
        },
        pricing: {
          retailPrice: 199.99,
          customerPrice: 149.99
        }
      }]
    });
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

test('fetches price and availability', async () => {
  const client = new IngramClient({ 
    clientId: 'test',
    clientSecret: 'test',
    sandbox: true 
  });
  
  const result = await client.getPriceAndAvailability(['ABC123']);
  expect(result[0].pricing.customerPrice).toBe(149.99);
});
```

### E2E Tests

**What to test:**
- Complete quote workflow (search → add → calculate → save)
- Entity switching
- Authentication flow
- Export functionality (PDF, CSV)
- Error states and recovery

**Playwright Config:**

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 2 : undefined,
  reporter: process.env.CI ? 'github' : 'html',
  
  use: {
    baseURL: process.env.BASE_URL ?? 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    // Mobile for responsive testing
    { name: 'mobile', use: { ...devices['iPhone 14'] } },
  ],
  
  webServer: {
    command: 'pnpm start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    env: {
      API_MODE: 'mock',
    },
  },
});
```

---

## 5. Secrets Management

### Credential Inventory

| Entity | Distributor | Secret Name Pattern | Rotation |
|--------|-------------|---------------------|----------|
| MHI | Ingram Micro | `INGRAM_MHI_CLIENT_ID/SECRET` | 90 days |
| MHI | TD SYNNEX | `SYNNEX_MHI_API_KEY` | 90 days |
| MHI | D&H | `DANDH_MHI_USERNAME/PASSWORD` | 90 days |
| MHI | Climb | `CLIMB_MHI_*` (if API exists) | N/A |
| DSAIC | Ingram Micro | `INGRAM_DSAIC_CLIENT_ID/SECRET` | 90 days |
| DSAIC | TD SYNNEX | `SYNNEX_DSAIC_API_KEY` | 90 days |
| DSAIC | D&H | `DANDH_DSAIC_USERNAME/PASSWORD` | 90 days |
| Computer Store | Ingram Micro | `INGRAM_COMPSTORE_CLIENT_ID/SECRET` | 90 days |
| Computer Store | TD SYNNEX | `SYNNEX_COMPSTORE_API_KEY` | 90 days |
| Computer Store | D&H | `DANDH_COMPSTORE_USERNAME/PASSWORD` | 90 days |

### GitHub Secrets Organization

```yaml
# Use GitHub Environments for isolation
environments:
  staging:
    secrets:
      # Staging uses sandbox/test credentials
      INGRAM_MHI_CLIENT_ID: (sandbox)
      INGRAM_MHI_CLIENT_SECRET: (sandbox)
      # ... etc
      
  production:
    secrets:
      # Production uses real credentials
      INGRAM_MHI_CLIENT_ID: (prod)
      INGRAM_MHI_CLIENT_SECRET: (prod)
      # ... etc
    protection_rules:
      - required_reviewers: 1
      - wait_timer: 5  # 5-minute delay before deploy
```

### Runtime Credential Loading

```typescript
// src/lib/config/credentials.ts
import { z } from 'zod';

const EntityCredentialsSchema = z.object({
  ingram: z.object({
    clientId: z.string(),
    clientSecret: z.string(),
    sandbox: z.boolean().default(false),
  }).optional(),
  synnex: z.object({
    apiKey: z.string(),
  }).optional(),
  dandh: z.object({
    username: z.string(),
    password: z.string(),
  }).optional(),
  climb: z.object({
    // Manual entry - no API
  }).optional(),
});

const CredentialsConfigSchema = z.object({
  mhi: EntityCredentialsSchema,
  dsaic: EntityCredentialsSchema,
  computerStore: EntityCredentialsSchema,
});

export type CredentialsConfig = z.infer<typeof CredentialsConfigSchema>;

export function loadCredentials(): CredentialsConfig {
  const raw = {
    mhi: {
      ingram: {
        clientId: process.env.INGRAM_MHI_CLIENT_ID!,
        clientSecret: process.env.INGRAM_MHI_CLIENT_SECRET!,
        sandbox: process.env.NODE_ENV !== 'production',
      },
      synnex: {
        apiKey: process.env.SYNNEX_MHI_API_KEY!,
      },
      dandh: {
        username: process.env.DANDH_MHI_USERNAME!,
        password: process.env.DANDH_MHI_PASSWORD!,
      },
    },
    // ... dsaic, computerStore
  };
  
  return CredentialsConfigSchema.parse(raw);
}
```

### Credential Rotation Workflow

```yaml
# .github/workflows/credential-rotation.yml
name: Credential Validation

on:
  schedule:
    - cron: '0 0 1 * *'  # Monthly on the 1st
  workflow_dispatch:

jobs:
  validate-credentials:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      
      - name: Validate Ingram Credentials (All Entities)
        run: |
          for entity in MHI DSAIC COMPSTORE; do
            echo "Validating Ingram credentials for $entity..."
            # Test OAuth token generation
            response=$(curl -s -o /dev/null -w "%{http_code}" \
              -X POST "https://api.ingrammicro.com/oauth/oauth20/token" \
              -H "Content-Type: application/x-www-form-urlencoded" \
              -d "grant_type=client_credentials" \
              -d "client_id=${{ secrets[format('INGRAM_{0}_CLIENT_ID', entity)] }}" \
              -d "client_secret=${{ secrets[format('INGRAM_{0}_CLIENT_SECRET', entity)] }}")
            
            if [[ "$response" != "200" ]]; then
              echo "::error::Ingram credentials for $entity failed (HTTP $response)"
              exit 1
            fi
          done
      
      # Similar validation for SYNNEX, D&H...
      
      - name: Alert on Expiring Credentials
        if: failure()
        uses: slackapi/slack-github-action@v1
        with:
          channel-id: 'C123ALERT'
          slack-message: '⚠️ Credential validation failed! Review API credentials.'
        env:
          SLACK_BOT_TOKEN: ${{ secrets.SLACK_BOT_TOKEN }}
```

### Never in CI Logs

```typescript
// src/lib/logging/sanitize.ts
const SENSITIVE_PATTERNS = [
  /client_secret[:=]["']?[\w-]+/gi,
  /api_key[:=]["']?[\w-]+/gi,
  /password[:=]["']?[\w-]+/gi,
  /bearer\s+[\w-]+/gi,
];

export function sanitizeLog(message: string): string {
  let sanitized = message;
  for (const pattern of SENSITIVE_PATTERNS) {
    sanitized = sanitized.replace(pattern, '[REDACTED]');
  }
  return sanitized;
}
```

---

## 6. Deployment Strategy

### Recommended Hosting

| Option | Pros | Cons | Cost |
|--------|------|------|------|
| **Vercel** | Zero-config Next.js, preview deploys | Vendor lock-in, serverless limits | $20-50/mo |
| **Railway** | Simple, supports any Node app | Newer platform | $20-50/mo |
| **Fly.io** | Global edge, Docker-based | More setup | $15-40/mo |
| **Self-hosted (VPS)** | Full control, cost-effective | Maintenance burden | $10-30/mo |

**Recommendation:** **Vercel** for fastest deployment, or **Railway** for flexibility.

### Vercel Deployment Flow

```yaml
# .github/workflows/deploy-staging.yml
name: Deploy Staging

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: ${{ steps.deploy.outputs.url }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to Vercel
        id: deploy
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prebuilt'
          working-directory: ./
      
      - name: Run Smoke Tests
        run: |
          curl --fail ${{ steps.deploy.outputs.url }}/api/health
```

### Production Deployment

```yaml
# .github/workflows/deploy-prod.yml
name: Deploy Production

on:
  release:
    types: [published]
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to deploy'
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://procurement.mhi-example.com
    
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.inputs.version || github.ref }}
      
      - name: Deploy to Vercel (Production)
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod --prebuilt'
          alias-domains: procurement.mhi-example.com
      
      - name: Post-Deploy Validation
        run: |
          # Verify critical endpoints
          curl --fail https://procurement.mhi-example.com/api/health
          curl --fail https://procurement.mhi-example.com/api/distributors/status
```

---

## 7. Environment Management

### Environment Matrix

| Environment | Purpose | Data | API Mode | Credentials |
|-------------|---------|------|----------|-------------|
| **Local** | Development | SQLite/local | Mock | None (optional real for testing) |
| **CI** | Automated tests | In-memory/ephemeral | Mock | None |
| **Preview** | PR previews | Staging DB (read-only) | Mock | None |
| **Staging** | Pre-prod validation | Staging DB | Sandbox APIs | Sandbox/test credentials |
| **Production** | Live users | Production DB | Live APIs | Production credentials |

### Environment Variable Management

```typescript
// src/lib/env.ts
import { z } from 'zod';

const envSchema = z.object({
  // App
  NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),
  APP_ENV: z.enum(['local', 'ci', 'preview', 'staging', 'production']).default('local'),
  
  // Database
  DATABASE_URL: z.string().url(),
  
  // API Mode
  API_MODE: z.enum(['mock', 'sandbox', 'live']).default('mock'),
  
  // Rate limiting
  RATE_LIMIT_ENABLED: z.coerce.boolean().default(true),
  RATE_LIMIT_MAX_PER_MINUTE: z.coerce.number().default(100),
  
  // Feature flags
  FEATURE_SYNNEX_ENABLED: z.coerce.boolean().default(false),
  FEATURE_DANDH_ENABLED: z.coerce.boolean().default(false),
  FEATURE_ORDERING_ENABLED: z.coerce.boolean().default(false),
});

export const env = envSchema.parse(process.env);
```

### `.env` File Templates

```bash
# .env.local (development - committed as .env.example)
NODE_ENV=development
APP_ENV=local
DATABASE_URL=file:./dev.db
API_MODE=mock

# Optional: real API testing in development
# INGRAM_MHI_CLIENT_ID=your-sandbox-id
# INGRAM_MHI_CLIENT_SECRET=your-sandbox-secret
```

```bash
# .env.staging (managed in hosting platform)
NODE_ENV=production
APP_ENV=staging
DATABASE_URL=postgresql://...
API_MODE=sandbox

# Sandbox credentials (from GitHub Secrets → Vercel)
INGRAM_MHI_CLIENT_ID=sandbox-xxx
INGRAM_MHI_CLIENT_SECRET=sandbox-yyy
```

---

## 8. Rate Limit Handling in CI

### The Problem

Distributor APIs have rate limits:
- Ingram Micro: ~100 req/min (estimated)
- TD SYNNEX: Unknown
- D&H: Unknown

Running full integration tests against real APIs could:
1. Hit rate limits, causing flaky tests
2. Consume API quota unnecessarily
3. Generate noise in distributor logs

### Solution: Mock-First Testing

```
┌──────────────────────────────────────────────────────────────┐
│                     CI Pipeline (Always)                     │
│                                                              │
│  Unit Tests → Integration (Mocked) → E2E (Mocked) → Build   │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│               Nightly Pipeline (Once per day)                │
│                                                              │
│  Live API Tests (Sandbox) → Rate Limited → Alert on Failure │
└──────────────────────────────────────────────────────────────┘
```

### Nightly Live API Tests

```yaml
# .github/workflows/nightly.yml
name: Nightly Integration Tests

on:
  schedule:
    - cron: '0 6 * * *'  # 6 AM UTC (midnight MST)
  workflow_dispatch:

jobs:
  live-api-tests:
    runs-on: ubuntu-latest
    environment: staging
    
    strategy:
      fail-fast: false
      matrix:
        distributor: [ingram, synnex, dandh]
        entity: [mhi, dsaic, compstore]
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: pnpm/action-setup@v3
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
      
      - run: pnpm install --frozen-lockfile
      
      - name: Run Live API Tests (${{ matrix.distributor }} / ${{ matrix.entity }})
        run: pnpm test:live --distributor=${{ matrix.distributor }} --entity=${{ matrix.entity }}
        env:
          API_MODE: sandbox
          # Dynamic credential loading based on entity
          CURRENT_ENTITY: ${{ matrix.entity }}
          # Rate limiting for live tests
          RATE_LIMIT_DELAY_MS: 500
        timeout-minutes: 10
      
      - name: Notify on Failure
        if: failure()
        uses: slackapi/slack-github-action@v1
        with:
          channel-id: 'C123ALERTS'
          slack-message: |
            ⚠️ Nightly API test failed
            Distributor: ${{ matrix.distributor }}
            Entity: ${{ matrix.entity }}
            Run: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
```

### Rate Limit Middleware for Tests

```typescript
// src/lib/testing/rate-limiter.ts
import pLimit from 'p-limit';

const delayMs = parseInt(process.env.RATE_LIMIT_DELAY_MS ?? '0', 10);
const maxConcurrent = parseInt(process.env.RATE_LIMIT_CONCURRENT ?? '1', 10);

const limit = pLimit(maxConcurrent);

export async function rateLimitedApiCall<T>(fn: () => Promise<T>): Promise<T> {
  return limit(async () => {
    if (delayMs > 0) {
      await new Promise(resolve => setTimeout(resolve, delayMs));
    }
    return fn();
  });
}
```

---

## 9. Mock vs Live API Testing

### Testing Matrix

| Test Type | API Mode | When | Purpose |
|-----------|----------|------|---------|
| Unit | None | Every commit | Business logic |
| Integration | **Mock** | Every commit | API client code paths |
| E2E | **Mock** | Every commit | User workflows |
| Contract | **Mock** | Every commit | API schema validation |
| Smoke | **Sandbox** | After deploy | Deployment validation |
| Nightly | **Sandbox** | Daily | Real API compatibility |
| Pre-release | **Sandbox** | Before prod deploy | Final validation |

### Mock API Implementation

```typescript
// src/lib/testing/mocks/ingram.ts
import { http, HttpResponse } from 'msw';
import { ingramProducts } from './fixtures/ingram-products';

export const ingramHandlers = [
  // OAuth Token
  http.post('https://api.ingrammicro.com/oauth/oauth20/token', () => {
    return HttpResponse.json({
      access_token: 'mock_token_12345',
      token_type: 'Bearer',
      expires_in: 3600,
    });
  }),
  
  // Price and Availability
  http.post('https://api.ingrammicro.com/*/catalog/priceandavailability', async ({ request }) => {
    const body = await request.json() as { products: { ingramPartNumber: string }[] };
    const partNumbers = body.products.map(p => p.ingramPartNumber);
    
    const results = partNumbers.map(pn => {
      const product = ingramProducts[pn];
      if (!product) {
        return {
          ingramPartNumber: pn,
          error: { code: 'NOT_FOUND', message: 'Product not found' }
        };
      }
      return product;
    });
    
    return HttpResponse.json({ productDetails: results });
  }),
  
  // Product Search
  http.get('https://api.ingrammicro.com/*/catalog', ({ request }) => {
    const url = new URL(request.url);
    const keyword = url.searchParams.get('keyword') ?? '';
    
    const results = Object.values(ingramProducts)
      .filter(p => p.productDescription.toLowerCase().includes(keyword.toLowerCase()))
      .slice(0, 25);
    
    return HttpResponse.json({
      catalog: results,
      recordsFound: results.length,
    });
  }),
  
  // Simulate rate limiting
  http.all('https://api.ingrammicro.com/*', () => {
    // Random 429 for chaos testing (disabled by default)
    if (process.env.MOCK_CHAOS === 'true' && Math.random() < 0.1) {
      return HttpResponse.json(
        { error: 'Rate limit exceeded' },
        { status: 429, headers: { 'Retry-After': '60' } }
      );
    }
    return;  // Pass through to other handlers
  }),
];
```

### Contract Testing

```typescript
// src/lib/distributors/ingram/contract.test.ts
import { describe, test, expect } from 'vitest';
import { z } from 'zod';

// Schema based on Ingram's OpenAPI spec
const PriceAvailabilityResponseSchema = z.object({
  productDetails: z.array(z.object({
    ingramPartNumber: z.string(),
    vendorPartNumber: z.string().optional(),
    vendorName: z.string().optional(),
    productDescription: z.string(),
    availability: z.object({
      available: z.boolean(),
      quantityAvailable: z.number(),
    }).optional(),
    pricing: z.object({
      retailPrice: z.number(),
      customerPrice: z.number(),
    }).optional(),
  })),
});

describe('Ingram API Contract', () => {
  test('price and availability response matches schema', async () => {
    const response = await fetch('mock://ingram/catalog/priceandavailability', {
      method: 'POST',
      body: JSON.stringify({ products: [{ ingramPartNumber: 'ABC123' }] }),
    });
    
    const data = await response.json();
    const result = PriceAvailabilityResponseSchema.safeParse(data);
    
    expect(result.success).toBe(true);
  });
});
```

---

## 10. Multi-Entity Configuration Management

### Configuration Structure

```typescript
// src/lib/config/entities.ts
export interface EntityConfig {
  id: 'mhi' | 'dsaic' | 'computerStore';
  displayName: string;
  taxExempt: boolean;
  defaultMarginPercent: number;
  enabledDistributors: ('ingram' | 'synnex' | 'dandh' | 'climb')[];
  preferredDistributor?: 'ingram' | 'synnex' | 'dandh';
}

export const entities: Record<string, EntityConfig> = {
  mhi: {
    id: 'mhi',
    displayName: 'MHI',
    taxExempt: true,  // GovCon
    defaultMarginPercent: 15,
    enabledDistributors: ['ingram', 'synnex', 'dandh'],
    preferredDistributor: 'ingram',
  },
  dsaic: {
    id: 'dsaic',
    displayName: 'DSAIC',
    taxExempt: true,  // GovCon
    defaultMarginPercent: 18,
    enabledDistributors: ['ingram', 'synnex', 'dandh', 'climb'],
  },
  computerStore: {
    id: 'computerStore',
    displayName: 'The Computer Store',
    taxExempt: false,
    defaultMarginPercent: 20,
    enabledDistributors: ['ingram', 'dandh'],
  },
};
```

### Entity Context in Application

```typescript
// src/lib/context/entity.ts
import { createContext, useContext } from 'react';
import type { EntityConfig } from '../config/entities';

export const EntityContext = createContext<EntityConfig | null>(null);

export function useEntity(): EntityConfig {
  const entity = useContext(EntityContext);
  if (!entity) {
    throw new Error('useEntity must be used within EntityProvider');
  }
  return entity;
}
```

### Entity-Specific API Client Factory

```typescript
// src/lib/distributors/factory.ts
import { IngramClient } from './ingram/client';
import { SynnexClient } from './synnex/client';
import { DandHClient } from './dandh/client';
import type { EntityConfig } from '../config/entities';
import { loadCredentials } from '../config/credentials';

export interface DistributorClient {
  getPriceAndAvailability(partNumbers: string[]): Promise<PriceResult[]>;
  searchProducts(query: string): Promise<Product[]>;
}

export function createDistributorClient(
  distributor: 'ingram' | 'synnex' | 'dandh',
  entity: EntityConfig
): DistributorClient {
  const credentials = loadCredentials();
  const entityCreds = credentials[entity.id];
  
  switch (distributor) {
    case 'ingram':
      if (!entityCreds.ingram) throw new Error(`No Ingram credentials for ${entity.id}`);
      return new IngramClient(entityCreds.ingram);
    
    case 'synnex':
      if (!entityCreds.synnex) throw new Error(`No SYNNEX credentials for ${entity.id}`);
      return new SynnexClient(entityCreds.synnex);
    
    case 'dandh':
      if (!entityCreds.dandh) throw new Error(`No D&H credentials for ${entity.id}`);
      return new DandHClient(entityCreds.dandh);
    
    default:
      throw new Error(`Unknown distributor: ${distributor}`);
  }
}
```

---

## 11. Recommended CI/CD Tooling

| Category | Tool | Purpose |
|----------|------|---------|
| **CI** | GitHub Actions | Workflows, automation |
| **Testing** | Vitest | Unit/integration tests |
| **E2E** | Playwright | Browser automation |
| **API Mocking** | MSW (Mock Service Worker) | HTTP-level mocking |
| **Coverage** | Codecov | Coverage tracking |
| **Secrets** | GitHub Secrets + Environments | Credential storage |
| **Hosting** | Vercel or Railway | Deployment |
| **Monitoring** | Sentry | Error tracking |
| **Alerts** | Slack/Discord webhook | CI notifications |

---

## 12. Implementation Phases

### Phase A: Foundation (Week 1)

- [ ] Set up repository structure
- [ ] Configure TypeScript, ESLint, Prettier
- [ ] Create `ci.yml` workflow with lint + build
- [ ] Set up Vitest with basic unit tests
- [ ] Create mock fixtures for Ingram API

### Phase B: Testing Infrastructure (Week 2)

- [ ] Implement MSW handlers for all distributors
- [ ] Add integration test suite
- [ ] Set up Playwright with basic E2E tests
- [ ] Configure code coverage reporting

### Phase C: Deployment (Week 3)

- [ ] Connect to Vercel/Railway
- [ ] Configure staging environment
- [ ] Set up production environment with protection rules
- [ ] Add smoke test job after deployments

### Phase D: Credentials & Monitoring (Week 4)

- [ ] Migrate all credentials to GitHub Secrets
- [ ] Implement credential validation workflow
- [ ] Set up nightly live API tests
- [ ] Configure Slack/Discord notifications
- [ ] Add Sentry for error monitoring

---

## Appendix: Quick Reference

### GitHub Secrets to Create

```
# Per-entity credentials (Staging + Production environments)
INGRAM_MHI_CLIENT_ID
INGRAM_MHI_CLIENT_SECRET
INGRAM_DSAIC_CLIENT_ID
INGRAM_DSAIC_CLIENT_SECRET
INGRAM_COMPSTORE_CLIENT_ID
INGRAM_COMPSTORE_CLIENT_SECRET
SYNNEX_MHI_API_KEY
SYNNEX_DSAIC_API_KEY
SYNNEX_COMPSTORE_API_KEY
DANDH_MHI_USERNAME
DANDH_MHI_PASSWORD
DANDH_DSAIC_USERNAME
DANDH_DSAIC_PASSWORD
DANDH_COMPSTORE_USERNAME
DANDH_COMPSTORE_PASSWORD

# Deployment
VERCEL_TOKEN
VERCEL_ORG_ID
VERCEL_PROJECT_ID

# Notifications
SLACK_BOT_TOKEN

# Optional
CODECOV_TOKEN
```

### Key Commands

```bash
# Development
pnpm dev              # Start dev server
pnpm test             # Run all tests
pnpm test:unit        # Unit tests only
pnpm test:integration # Integration tests (mocked)
pnpm test:e2e         # E2E tests (mocked)

# CI simulation
pnpm lint && pnpm typecheck && pnpm build && pnpm test

# Database
pnpm db:push          # Push schema to dev DB
pnpm db:migrate       # Run migrations
```

---

*Document prepared for MHI Procurement App CI/CD planning. Review and adapt based on actual framework choice (Next.js vs SvelteKit) and hosting decisions.*
