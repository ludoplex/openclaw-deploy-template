# Technology Fingerprints Database

Comprehensive signatures for identifying web technologies.

## Frontend Frameworks

### React
```
Indicators:
- data-reactroot attribute
- data-reactid attribute (older)
- __REACT_DEVTOOLS_GLOBAL_HOOK__
- _reactRootContainer on DOM elements
- Script: react.production.min.js, react-dom.production.min.js
- Bundle pattern: main.[hash].chunk.js (Create React App)
```

### Vue.js
```
Indicators:
- __VUE__ global
- data-v-[hash] scoped style attributes
- v-cloak attribute (pre-render)
- Script: vue.global.prod.js, vue.runtime.esm.js
- __vue__ property on elements
```

### Angular
```
Indicators:
- ng-version attribute on root element
- _ngcontent-[hash] attributes
- ng-* attributes (AngularJS)
- Script: main.[hash].js, polyfills.[hash].js, runtime.[hash].js
- Zone.js present
```

### Svelte
```
Indicators:
- svelte-[hash] class names
- No virtual DOM overhead
- Compiled output: bundle.js, bundle.css
- __svelte_meta property
```

### Next.js
```
Indicators:
- __NEXT_DATA__ script with JSON
- /_next/static/ path
- _next/image for images
- x-nextjs-* headers
- __next element ID
```

### Nuxt.js
```
Indicators:
- __NUXT__ global with state
- /_nuxt/ static path
- nuxt-link elements
- data-n-head attributes
```

### Gatsby
```
Indicators:
- ___gatsby element ID
- gatsby-* prefixed resources
- /page-data/ paths
- __gatsby global
```

## Backend Frameworks

### Node.js / Express
```
Indicators:
- X-Powered-By: Express
- connect.sid cookie
- ETag: W/"..." weak validators
- Default 404/500 pages
```

### Django
```
Indicators:
- csrftoken cookie
- csrfmiddlewaretoken input
- /static/, /media/ paths
- __admin/ path
- CSRF token in forms
```

### Ruby on Rails
```
Indicators:
- _session_id cookie
- X-Request-Id header
- assets/application-[hash].js
- /assets/ pipeline
- authenticity_token input
- data-turbo-* attributes (Turbo)
```

### Laravel
```
Indicators:
- XSRF-TOKEN cookie
- laravel_session cookie
- X-Powered-By: PHP/X.X
- _token input
- Blade: @csrf, @method
```

### ASP.NET
```
Indicators:
- X-AspNet-Version header
- X-AspNetMvc-Version header
- ASP.NET_SessionId cookie
- __VIEWSTATE, __EVENTVALIDATION inputs
- .aspx, .ashx, .asmx extensions
- __doPostBack() function
```

### Spring (Java)
```
Indicators:
- JSESSIONID cookie
- .jsp, .do, .action extensions
- /WEB-INF/ path exposure (misconfiguration)
- X-Application-Context header
```

### Flask
```
Indicators:
- session cookie (signed)
- Werkzeug debugger (development)
- X-Powered-By: Werkzeug
```

### FastAPI
```
Indicators:
- /docs (Swagger UI)
- /redoc (ReDoc)
- /openapi.json
- application/json responses
```

## CMS Platforms

### WordPress
```
Indicators:
- /wp-content/, /wp-includes/ paths
- /wp-admin/ login
- /wp-json/ REST API
- ?p=123 post IDs
- meta generator: WordPress X.X
- /xmlrpc.php
- /wp-login.php
- Cookies: wordpress_*, wp-settings-*
```

### Drupal
```
Indicators:
- /sites/default/files/ path
- /node/123 paths
- ?q= query parameter
- meta generator: Drupal X
- /core/ path
- X-Generator: Drupal X
- Drupal.settings JS object
```

### Joomla
```
Indicators:
- /components/, /modules/, /templates/ paths
- /administrator/ backend
- ?option=com_* parameters
- meta generator: Joomla!
- /media/system/js/
```

### Ghost
```
Indicators:
- /ghost/ admin path
- meta generator: Ghost X.X
- /content/images/ path
- ghost-* classes
```

### Contentful
```
Indicators:
- cdn.contentful.com in sources
- Contentful API responses
- contentful-* in scripts
```

### Strapi
```
Indicators:
- /admin path
- /uploads/ path
- Strapi API patterns
- strapi-* identifiers
```

## E-commerce

### Shopify
```
Indicators:
- .myshopify.com domain
- cdn.shopify.com resources
- Shopify.theme JS object
- /cart.js, /products.json APIs
- shopify-* cookies
```

### WooCommerce
```
Indicators:
- /wp-content/plugins/woocommerce/
- wc-* classes
- ?add-to-cart= parameter
- woocommerce-* cookies
- /wc-api/ endpoint
```

### Magento
```
Indicators:
- /skin/, /js/mage/ paths (M1)
- /static/, /pub/ paths (M2)
- PHPSESSID + form_key
- /checkout/cart/
- Mage.Cookies JS
- mage/* RequireJS modules
```

### BigCommerce
```
Indicators:
- bigcommerce.com resources
- /cart.php path
- BigCommerce script patterns
```

## Static Site Generators

### Jekyll
```
Indicators:
- _site/ build folder
- _posts/, _layouts/, _includes/ source
- .html extensions
- meta generator: Jekyll
- Gemfile, _config.yml
```

### Hugo
```
Indicators:
- Date-based URL patterns
- /posts/, /blog/ paths
- config.toml, config.yaml
- /public/ build folder
- Static, simple HTML
```

### Eleventy (11ty)
```
Indicators:
- .eleventy.js config
- _includes/, _data/ source
- Clean HTML output
- No framework fingerprints
```

### Astro
```
Indicators:
- astro-* attributes
- /_astro/ path
- astro.config.mjs
- Islands architecture
```

## Cloud & Hosting

### Cloudflare
```
Indicators:
- cf-ray header
- __cfduid, cf_clearance cookies
- /cdn-cgi/ path
- cloudflare error pages
- CF-Cache-Status header
```

### AWS CloudFront
```
Indicators:
- .cloudfront.net domain
- x-amz-cf-* headers
- X-Cache: Hit/Miss from cloudfront
- Via: 1.1 [id].cloudfront.net
```

### Vercel
```
Indicators:
- .vercel.app domain
- x-vercel-* headers
- _vercel/ paths
- X-Vercel-Id header
```

### Netlify
```
Indicators:
- .netlify.app domain
- x-nf-* headers
- /.netlify/functions/ path
- _headers, _redirects files
```

### Heroku
```
Indicators:
- .herokuapp.com domain
- X-Request-Id pattern
- Heroku router Via header
```

### Firebase
```
Indicators:
- .firebaseapp.com, .web.app domains
- /__/firebase/ paths
- firebase.json config
- Firebase JS SDK
```

### GitHub Pages
```
Indicators:
- .github.io domain
- X-GitHub-Request-Id header
- Jekyll default builds
```

## Analytics & Tracking

### Google Analytics
```
Indicators:
- gtag.js, analytics.js scripts
- UA-XXXXXX-X (Universal Analytics)
- G-XXXXXXX (GA4)
- googletagmanager.com resources
- _ga, _gid cookies
```

### Google Tag Manager
```
Indicators:
- GTM-XXXXXX container ID
- googletagmanager.com/gtm.js
- dataLayer array
```

### Facebook Pixel
```
Indicators:
- connect.facebook.net/en_US/fbevents.js
- fbq() function
- _fbp cookie
```

### Hotjar
```
Indicators:
- static.hotjar.com scripts
- _hj* cookies
- hjid, hjsid identifiers
```

### Segment
```
Indicators:
- cdn.segment.com/analytics.js
- analytics.identify(), analytics.track()
- ajs_* cookies
```

## Security & WAF

### Cloudflare WAF
```
Indicators:
- CF challenge pages
- __cf_bm cookie
- cf_clearance cookie
- 403 with Cloudflare ray
```

### AWS WAF
```
Indicators:
- x-amzn-RequestId header
- AWS WAF block pages
```

### Akamai
```
Indicators:
- Akamai-* headers
- akamai.net resources
- AkamaiGHost Server header
```

### Imperva/Incapsula
```
Indicators:
- incap_ses_* cookies
- visid_incap_* cookies
- Incapsula incident ID
```

## Server Software

### nginx
```
Indicators:
- Server: nginx, nginx/X.X.X
- Default 50x error pages
- X-nginx-* custom headers
```

### Apache
```
Indicators:
- Server: Apache, Apache/X.X.X
- X-Powered-By: PHP/X.X
- .htaccess behavior
- Default directory listings
```

### IIS
```
Indicators:
- Server: Microsoft-IIS/X.X
- X-Powered-By: ASP.NET
- X-AspNet-Version header
- .asp, .aspx extensions
```

### LiteSpeed
```
Indicators:
- Server: LiteSpeed
- X-LiteSpeed-* headers
```

### Caddy
```
Indicators:
- Server: Caddy
- Automatic HTTPS behavior
```

## Build Tools

### Webpack
```
Indicators:
- main.[hash].js pattern
- [name].chunk.js chunks
- webpackJsonp array
- __webpack_require__ function
```

### Vite
```
Indicators:
- @vite/client module
- /@vite/ paths in dev
- vite.config.js
- Fast HMR in dev
```

### Parcel
```
Indicators:
- parcel-bundler patterns
- .parcel-cache/
```

### Rollup
```
Indicators:
- Clean ESM output
- rollup.config.js
```
