# MHI Procurement Engine — Source Manifest

**Generated:** 2026-02-09  
**Source:** C:\mhi-procurement\  
**Purpose:** Foundation for D&H integration (copy ingram.c pattern)

---

## File: src/sync/ingram.c

Ingram Micro API integration — **TEMPLATE FOR D&H INTEGRATION**

### Static/Internal Functions

| Name | Signature | Line | Purpose |
|------|-----------|------|---------|
| `json_find_string` | `static const char *json_find_string(const char *json, const char *key, int *out_len)` | 50 | Find JSON string value for a key, returns pointer and length |
| `json_extract_string` | `static void json_extract_string(const char *json, const char *key, char *dst, size_t dst_size)` | 73 | Extract JSON string into buffer |
| `json_find_number` | `static double json_find_number(const char *json, const char *key)` | 85 | Find JSON number value (returns 0.0 if not found) |
| `json_find_int` | `static int json_find_int(const char *json, const char *key)` | 106 | Find JSON integer value |
| `json_find_array` | `static const char *json_find_array(const char *json, const char *key)` | 111 | Find JSON array by key, returns pointer to '[' |
| `json_array_next` | `static const char *json_array_next(const char *arr, const char **elem, int *elem_len)` | 125 | Iterate array elements, returns pointer to next element |
| `generate_correlation_id` | `static void generate_correlation_id(char *buf, size_t size)` | 152 | Generate unique correlation ID for API calls |
| `ingram_set_headers` | `static void ingram_set_headers(http_headers_t *hdrs, const char *access_token, const char *customer_number)` | 160 | Set required Ingram API headers (Auth, IM-CustomerNumber, etc.) |
| `get_http_client` | `static http_client_t *get_http_client(void)` | 202 | Lazy-init singleton HTTP client with rate limiting |
| `ensure_auth` | `static int ensure_auth(ingram_config_t *cfg)` | 247 | Auto-refresh OAuth token if expired |
| `map_ingram_product` | `static int map_ingram_product(const char *json, int json_len, mhi_product_t *product, mhi_offering_t *offering)` | 351 | Map Ingram catalog JSON to SSOT structs |

### Public API Functions

| Name | Signature | Line | Purpose |
|------|-----------|------|---------|
| `ingram_config_load` | `int ingram_config_load(ingram_config_t *cfg, const char *config_path)` | 178 | Load Ingram credentials from config file |
| `ingram_auth` | `int ingram_auth(ingram_config_t *cfg)` | 214 | OAuth2 client credentials authentication |
| `ingram_search` | `int ingram_search(ingram_config_t *cfg, const char *query, mhi_product_t *results, int max_results, int *count)` | 253 | Search Ingram product catalog |
| `ingram_get_price` | `int ingram_get_price(ingram_config_t *cfg, const char *ingram_sku, double *price, int *qty_available, char *warehouse, int warehouse_len)` | 319 | Get price and availability for single SKU |
| `ingram_sync_catalog` | `int ingram_sync_catalog(sqlite3 *db, ingram_config_t *cfg, int page_size, int max_pages)` | 412 | Full catalog sync to database with audit trail |
| `ingram_sync_pricing` | `int ingram_sync_pricing(sqlite3 *db, ingram_config_t *cfg)` | 494 | Batch pricing sync for known products (up to 25 per request) |
| `ingram_create_order` | `int ingram_create_order(ingram_config_t *cfg, const char *po_json, char *order_id, int order_id_len)` | 627 | Create purchase order via Ingram API |

---

## File: src/db/database.c

SQLite SSOT for supplier/product/pricing data

### Static/Internal Functions

| Name | Signature | Line | Purpose |
|------|-----------|------|---------|
| `safe_strncpy` | `static void safe_strncpy(char *dst, const char *src, size_t n)` | 16 | Safe string copy with null termination |
| `col_text` | `static const char *col_text(sqlite3_stmt *stmt, int col)` | 24 | Safe wrapper for sqlite3_column_text (handles NULL) |
| `null_if_empty` | `static const char *null_if_empty(const char *s)` | 29 | Return NULL for empty strings (for SQL binding) |
| `product_from_row` | `static void product_from_row(sqlite3_stmt *stmt, mhi_product_t *out)` | 68 | Populate mhi_product_t from SQLite result row |
| `offering_from_row` | `static void offering_from_row(sqlite3_stmt *stmt, mhi_offering_t *out)` | 182 | Populate mhi_offering_t from SQLite result row |
| `margin_from_row` | `static void margin_from_row(sqlite3_stmt *stmt, mhi_margin_t *out)` | 277 | Populate mhi_margin_t from SQLite result row |

### Database Lifecycle

| Name | Signature | Line | Purpose |
|------|-----------|------|---------|
| `mhi_db_open` | `mhi_result_t mhi_db_open(sqlite3 **db, const char *path)` | 33 | Open database, set WAL mode and foreign keys |
| `mhi_db_close` | `void mhi_db_close(sqlite3 *db)` | 48 | Close database connection |
| `mhi_db_init_schema` | `mhi_result_t mhi_db_init_schema(sqlite3 *db)` | 52 | Initialize schema from embedded SQL |

### Product CRUD

| Name | Signature | Line | Purpose |
|------|-----------|------|---------|
| `mhi_product_upsert` | `mhi_result_t mhi_product_upsert(sqlite3 *db, const mhi_product_t *p, int64_t *out_id)` | 80 | Insert or update product (ON CONFLICT upc) |
| `mhi_product_get` | `mhi_result_t mhi_product_get(sqlite3 *db, int64_t id, mhi_product_t *out)` | 80 | Get product by ID |
| `mhi_product_find_by_upc` | `mhi_result_t mhi_product_find_by_upc(sqlite3 *db, const char *upc, mhi_product_t *out)` | 95 | Find product by UPC |
| `mhi_product_find_by_mfr_part` | `mhi_result_t mhi_product_find_by_mfr_part(sqlite3 *db, const char *mfr_part, mhi_product_t *out)` | 109 | Find product by manufacturer part number |
| `mhi_product_search` | `mhi_result_t mhi_product_search(sqlite3 *db, const mhi_search_params_t *params, mhi_product_t *results, int max_results, int *count)` | 123 | Parameterized product search (SQL injection safe) |
| `mhi_product_delete` | `mhi_result_t mhi_product_delete(sqlite3 *db, int64_t id)` | 176 | Delete product by ID |

### Supplier Offerings

| Name | Signature | Line | Purpose |
|------|-----------|------|---------|
| `mhi_offering_upsert` | `mhi_result_t mhi_offering_upsert(sqlite3 *db, const mhi_offering_t *o, int64_t *out_id)` | 193 | Insert or update supplier offering |
| `mhi_offering_get_by_product` | `mhi_result_t mhi_offering_get_by_product(sqlite3 *db, int64_t product_id, mhi_offering_t *results, int max_results, int *count)` | 218 | Get all offerings for a product |
| `mhi_offering_get_best_price` | `mhi_result_t mhi_offering_get_best_price(sqlite3 *db, int64_t product_id, mhi_offering_t *out)` | 241 | Get best-priced in-stock offering |
| `mhi_offering_delete_stale` | `mhi_result_t mhi_offering_delete_stale(sqlite3 *db, int64_t supplier_id, int max_age_hours)` | 260 | Delete offerings not synced within max_age_hours |

### Market Prices

| Name | Signature | Line | Purpose |
|------|-----------|------|---------|
| `mhi_market_upsert` | `mhi_result_t mhi_market_upsert(sqlite3 *db, const mhi_market_price_t *mp, int64_t *out_id)` | 295 | Insert or update market price |
| `mhi_market_get_by_product` | `mhi_result_t mhi_market_get_by_product(sqlite3 *db, int64_t product_id, mhi_market_price_t *results, int max_results, int *count)` | 317 | Get market prices for a product |

### Margin Analysis

| Name | Signature | Line | Purpose |
|------|-----------|------|---------|
| `mhi_margin_get` | `mhi_result_t mhi_margin_get(sqlite3 *db, int64_t product_id, mhi_margin_t *out)` | 295 | Get margin analysis for single product |
| `mhi_margin_search` | `mhi_result_t mhi_margin_search(sqlite3 *db, const mhi_search_params_t *params, mhi_margin_t *results, int max_results, int *count)` | 313 | Search margin analysis view with filters |

### Sync Tracking

| Name | Signature | Line | Purpose |
|------|-----------|------|---------|
| `mhi_sync_start` | `mhi_result_t mhi_sync_start(sqlite3 *db, int64_t supplier_id, const char *sync_type, int64_t *log_id)` | 368 | Start sync operation, returns log ID |
| `mhi_sync_complete` | `mhi_result_t mhi_sync_complete(sqlite3 *db, int64_t log_id, int records_synced)` | 385 | Mark sync as completed with record count |
| `mhi_sync_fail` | `mhi_result_t mhi_sync_fail(sqlite3 *db, int64_t log_id, const char *error)` | 399 | Mark sync as failed with error message |

### Basket Operations

| Name | Signature | Line | Purpose |
|------|-----------|------|---------|
| `mhi_basket_add` | `mhi_result_t mhi_basket_add(sqlite3 *db, int64_t product_id, int64_t supplier_id, int quantity, double unit_cost)` | 415 | Add item to basket |
| `mhi_basket_remove` | `mhi_result_t mhi_basket_remove(sqlite3 *db, int64_t basket_item_id)` | 433 | Remove item from basket |
| `mhi_basket_clear` | `mhi_result_t mhi_basket_clear(sqlite3 *db)` | 446 | Clear all basket items |
| `mhi_basket_to_po` | `mhi_result_t mhi_basket_to_po(sqlite3 *db, int64_t supplier_id, int64_t *po_id)` | 451 | Convert basket items to purchase order |

---

## File: src/net/http.c

HTTP/HTTPS client with mbedTLS, rate limiting, and audit logging

### Credential & Memory Security

| Name | Signature | Line | Purpose |
|------|-----------|------|---------|
| `http_redact` | `const char *http_redact(const char *value)` | 44 | Redact credentials for logging (shows first/last 4 chars) |
| `http_secure_zero` | `void http_secure_zero(void *ptr, size_t len)` | 52 | Volatile memset to prevent compiler optimization |

### Static/Internal Functions

| Name | Signature | Line | Purpose |
|------|-----------|------|---------|
| `time_ms` | `static double time_ms(void)` | 59 | Get monotonic time in milliseconds |
| `default_log_fn` | `static void default_log_fn(...)` | 67 | Default audit log function (stderr) |
| `conn_close` | `static void conn_close(http_conn_t *conn)` | 141 | Close connection, free TLS resources |
| `pool_get` | `static http_conn_t *pool_get(http_client_t *client, const char *host, int port, bool is_tls)` | 181 | Get or create pooled connection |
| `pool_release` | `static void pool_release(http_conn_t *conn, bool keep_alive)` | 230 | Release connection back to pool |
| `conn_establish` | `static http_result_t conn_establish(http_client_t *client, http_conn_t *conn, const char *host, int port, bool is_tls, int timeout_ms)` | 238 | Establish TCP + optional TLS connection |
| `conn_write` | `static int conn_write(http_conn_t *conn, const void *buf, size_t len)` | 388 | Write to connection (TLS or plain) |
| `conn_read` | `static int conn_read(http_conn_t *conn, void *buf, size_t len, int timeout_ms)` | 410 | Read from connection with timeout |
| `method_str` | `static const char *method_str(http_method_t m)` | 440 | Convert method enum to string |
| `send_request` | `static http_result_t send_request(http_conn_t *conn, const http_request_t *req, const http_url_parts_t *url)` | 451 | Serialize and send HTTP request |
| `recv_response` | `static http_result_t recv_response(http_conn_t *conn, http_response_t *resp, int timeout_ms)` | 503 | Parse HTTP response (headers + body) |
| `find_rate_limiter` | `static http_rate_limiter_t *find_rate_limiter(http_client_t *client, const char *api_name)` | 697 | Find rate limiter for API |
| `audit_log` | `static void audit_log(http_client_t *client, ...)` | 706 | Write to audit log (file + callback) |
| `resp_append` | `static int resp_append(http_response_t *resp, const char *data, size_t len)` | 111 | Append data to response body buffer |

### Header Operations

| Name | Signature | Line | Purpose |
|------|-----------|------|---------|
| `http_headers_add` | `void http_headers_add(http_headers_t *hdrs, const char *name, const char *value)` | 79 | Add header to collection |
| `http_headers_set` | `void http_headers_set(http_headers_t *hdrs, const char *name, const char *value)` | 87 | Set header (update existing or add) |
| `http_headers_get` | `const char *http_headers_get(const http_headers_t *hdrs, const char *name)` | 99 | Get header value by name (case-insensitive) |
| `http_headers_clear` | `void http_headers_clear(http_headers_t *hdrs)` | 107 | Clear all headers |

### URL Operations

| Name | Signature | Line | Purpose |
|------|-----------|------|---------|
| `http_url_parse` | `int http_url_parse(const char *url, http_url_parts_t *parts)` | 113 | Parse URL into scheme/host/port/path/query |
| `http_url_encode` | `int http_url_encode(const char *src, char *dst, size_t dst_size)` | 167 | URL-encode string |

### Response Management

| Name | Signature | Line | Purpose |
|------|-----------|------|---------|
| `http_response_free` | `void http_response_free(http_response_t *resp)` | 182 | Free response body |

### Rate Limiting

| Name | Signature | Line | Purpose |
|------|-----------|------|---------|
| `http_rate_init` | `void http_rate_init(http_rate_limiter_t *rl, const char *api_name, int max_requests, int window_seconds)` | 195 | Initialize rate limiter |
| `http_rate_check` | `bool http_rate_check(const http_rate_limiter_t *rl)` | 203 | Check if request is allowed |
| `http_rate_record` | `void http_rate_record(http_rate_limiter_t *rl)` | 217 | Record a request timestamp |

### Client Lifecycle

| Name | Signature | Line | Purpose |
|------|-----------|------|---------|
| `http_client_init` | `http_result_t http_client_init(http_client_t *client)` | 649 | Initialize HTTP client with defaults |
| `http_client_destroy` | `void http_client_destroy(http_client_t *client)` | 667 | Destroy client, close connections, zero tokens |
| `http_client_set_audit_log` | `void http_client_set_audit_log(http_client_t *client, const char *path)` | 686 | Set audit log file path |
| `http_client_add_rate_limit` | `void http_client_add_rate_limit(http_client_t *client, const char *api_name, int max_requests, int window_seconds)` | 697 | Add per-API rate limiter |

### Core Request

| Name | Signature | Line | Purpose |
|------|-----------|------|---------|
| `http_request` | `http_result_t http_request(http_client_t *client, const char *api_name, const http_request_t *req, http_response_t *resp)` | 723 | Core request with retry + rate limiting + exponential backoff |

### Convenience Methods

| Name | Signature | Line | Purpose |
|------|-----------|------|---------|
| `http_get` | `http_result_t http_get(http_client_t *client, const char *api_name, const char *url, const http_headers_t *headers, http_response_t *resp)` | 825 | HTTP GET request |
| `http_post` | `http_result_t http_post(http_client_t *client, const char *api_name, const char *url, const http_headers_t *headers, const char *body, size_t body_len, http_response_t *resp)` | 835 | HTTP POST request |
| `http_put` | `http_result_t http_put(http_client_t *client, const char *api_name, const char *url, const http_headers_t *headers, const char *body, size_t body_len, http_response_t *resp)` | 848 | HTTP PUT request |
| `http_post_json` | `http_result_t http_post_json(http_client_t *client, const char *api_name, const char *url, const http_headers_t *extra_headers, const char *json_body, http_response_t *resp)` | 861 | POST with JSON content-type |
| `http_get_json` | `http_result_t http_get_json(http_client_t *client, const char *api_name, const char *url, const http_headers_t *extra_headers, http_response_t *resp)` | 870 | GET with JSON accept header |

### OAuth2

| Name | Signature | Line | Purpose |
|------|-----------|------|---------|
| `http_oauth2_client_credentials` | `http_result_t http_oauth2_client_credentials(http_client_t *client, const char *api_name, const char *token_url, const char *client_id, const char *client_secret, const char *scope, oauth2_token_t *out_token)` | 880 | Full OAuth2 client credentials flow |
| `http_oauth2_get_token` | `http_result_t http_oauth2_get_token(http_client_t *client, const char *api_name, const char *token_url, const char *client_id, const char *client_secret, const char *scope, const char **out_access_token)` | 976 | Get cached token or refresh if expired |

---

## File: src/net/config.h

Configuration management (header-only with `MHI_CONFIG_IMPLEMENTATION`)

### Types Defined

| Type | Line | Purpose |
|------|------|---------|
| `mhi_ingram_creds_t` | 40 | Ingram Micro credentials struct |
| `mhi_synnex_creds_t` | 50 | TD SYNNEX credentials struct |
| `mhi_dandh_creds_t` | 58 | D&H credentials struct |
| `mhi_bestbuy_creds_t` | 65 | Best Buy credentials struct |
| `mhi_ebay_creds_t` | 71 | eBay credentials struct |
| `mhi_icecat_creds_t` | 80 | Icecat credentials struct |
| `mhi_config_t` | 87 | Master config containing all suppliers |

### Static/Internal Functions

| Name | Signature | Line | Purpose |
|------|-----------|------|---------|
| `trim_whitespace` | `static void trim_whitespace(char *s)` | 130 | Trim leading/trailing whitespace |
| `cfg_set` | `static void cfg_set(char *dst, size_t dst_size, const char *value)` | 141 | Safe string copy for config values |
| `check_file_permissions` | `static void check_file_permissions(const char *path)` | 147 | SECURITY: Warn if config world-readable |
| `apply_env_overrides` | `static void apply_env_overrides(mhi_config_t *cfg)` | 160 | Apply MHI_* environment variables |

### Public Functions

| Name | Signature | Line | Purpose |
|------|-----------|------|---------|
| `mhi_config_load` | `int mhi_config_load(mhi_config_t *cfg, const char *path)` | 200 | Load config from file + env overrides |
| `mhi_config_free` | `void mhi_config_free(mhi_config_t *cfg)` | 320 | Free config and securely zero credentials |
| `mhi_config_has_ingram` | `bool mhi_config_has_ingram(const mhi_config_t *cfg)` | 337 | Check if Ingram credentials configured |
| `mhi_config_has_synnex` | `bool mhi_config_has_synnex(const mhi_config_t *cfg)` | 341 | Check if SYNNEX credentials configured |
| `mhi_config_has_dandh` | `bool mhi_config_has_dandh(const mhi_config_t *cfg)` | 345 | Check if D&H credentials configured |
| `mhi_config_has_bestbuy` | `bool mhi_config_has_bestbuy(const mhi_config_t *cfg)` | 349 | Check if Best Buy credentials configured |
| `mhi_config_has_ebay` | `bool mhi_config_has_ebay(const mhi_config_t *cfg)` | 353 | Check if eBay credentials configured |
| `mhi_config_has_icecat` | `bool mhi_config_has_icecat(const mhi_config_t *cfg)` | 357 | Check if Icecat credentials configured |
| `mhi_config_print` | `void mhi_config_print(const mhi_config_t *cfg)` | 362 | Print config summary (credentials redacted) |
| `mhi_config_write_template` | `int mhi_config_write_template(const char *path)` | 393 | Write template config file |

---

## File: src/ui/gui.c

CImGui + Sokol GUI (conditional on `MHI_GUI`)

### Static/Internal Functions

| Name | Signature | Line | Purpose |
|------|-----------|------|---------|
| `gui_do_search` | `static void gui_do_search(void)` | 72 | Execute product search with current filters |
| `gui_select_product` | `static void gui_select_product(int64_t product_id)` | 84 | Load product detail, margin, offerings |
| `gui_load_basket` | `static void gui_load_basket(void)` | 95 | Load basket items from database |
| `gui_load_sync_log` | `static void gui_load_sync_log(void)` | 127 | Load recent sync log entries |
| `gui_panel_search` | `static void gui_panel_search(void)` | 153 | Render search panel with results table |
| `gui_panel_detail` | `static void gui_panel_detail(void)` | 210 | Render product detail + margin analysis |
| `gui_panel_basket` | `static void gui_panel_basket(void)` | 323 | Render basket panel with items |
| `gui_panel_sync` | `static void gui_panel_sync(void)` | 381 | Render sync status panel |
| `gui_main_menu` | `static void gui_main_menu(void)` | 424 | Render main menu bar |
| `gui_init` | `static void gui_init(void)` | 456 | Sokol init callback — setup graphics + ImGui |
| `gui_frame` | `static void gui_frame(void)` | 485 | Sokol frame callback — render all panels |
| `gui_cleanup` | `static void gui_cleanup(void)` | 512 | Sokol cleanup callback |
| `gui_event` | `static void gui_event(const sapp_event *ev)` | 518 | Sokol event callback — forward to ImGui |

### Public Functions

| Name | Signature | Line | Purpose |
|------|-----------|------|---------|
| `mhi_gui_get_desc` | `sapp_desc mhi_gui_get_desc(void)` | 524 | Return Sokol app descriptor for main() |

---

## D&H Integration Template

To build `dandh.c`, copy `ingram.c` structure:

### Required Functions for dandh.c

| Function | Purpose | Ingram Equivalent |
|----------|---------|-------------------|
| `dandh_config_load` | Load D&H API key from config | `ingram_config_load` |
| `dandh_auth` | D&H uses API key (simpler than OAuth2) | `ingram_auth` |
| `dandh_set_headers` | Set D&H required headers | `ingram_set_headers` |
| `dandh_search` | Search D&H catalog | `ingram_search` |
| `dandh_get_price` | Get price/availability | `ingram_get_price` |
| `dandh_sync_catalog` | Full catalog sync | `ingram_sync_catalog` |
| `dandh_sync_pricing` | Pricing update sync | `ingram_sync_pricing` |
| `map_dandh_product` | Map D&H JSON to SSOT | `map_ingram_product` |

### D&H API Differences from Ingram

- **Auth**: API key instead of OAuth2
- **Headers**: Different required headers (check D&H docs)
- **Endpoints**: Different URL structure
- **JSON fields**: Different field names in responses
- **Supplier ID**: Use different DANDH_SUPPLIER_ID constant

### Config Keys (already in config.h)

```c
// From mhi_dandh_creds_t:
cfg->dandh.api_key        // MHI_DANDH_API_KEY
cfg->dandh.base_url       // https://api.dandh.com
cfg->dandh.account_number // 3270340000
cfg->dandh.rate_limit_rpm // 60
```

---

## What Does NOT Exist

- ❌ `synnex_*.c` — TD SYNNEX integration not implemented
- ❌ `ebay_*.c` — eBay Browse API integration not implemented
- ❌ `bestbuy_*.c` — Best Buy API integration not implemented
- ❌ `icecat_*.c` — Icecat enrichment not implemented
- ❌ `http_delete()` — HTTP DELETE convenience method not implemented
- ❌ `http_patch()` — HTTP PATCH convenience method not implemented
- ❌ `mhi_product_batch_upsert()` — Batch insert not implemented (use transaction + loop)
- ❌ `ingram_order_status()` — Order tracking not implemented
- ❌ `ingram_returns()` — RMA handling not implemented

---

*This manifest is ground truth for the MHI Procurement codebase. Verify before using any function.*
