# MixPost Self-Hosted Setup

## Quick Start (Docker)

### Prerequisites
- Docker & Docker Compose
- Public domain/subdomain
- SSL email for Let's Encrypt

### 1. Create docker-compose.yml

```yaml
services:
  traefik:
    image: "traefik"
    restart: unless-stopped
    command:
      - "--api=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.mytlschallenge.acme.tlschallenge=true"
      - "--certificatesresolvers.mytlschallenge.acme.email=${SSL_EMAIL}"
      - "--certificatesresolvers.mytlschallenge.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - traefik_data:/letsencrypt
      - /var/run/docker.sock:/var/run/docker.sock:ro

  mixpost:
    image: inovector/mixpost:latest
    env_file:
      - .env
    labels:
      - traefik.enable=true
      - traefik.http.routers.mixpost.rule=Host(`${APP_DOMAIN}`)
      - traefik.http.routers.mixpost.tls=true
      - traefik.http.routers.mixpost.tls.certresolver=mytlschallenge
    volumes:
      - storage:/var/www/html/storage/app
      - logs:/var/www/html/storage/logs
    depends_on:
      - mysql
      - redis
    restart: unless-stopped

  mysql:
    image: 'mysql/mysql-server:8.0'
    environment:
      MYSQL_DATABASE: ${DB_DATABASE}
      MYSQL_USER: ${DB_USERNAME}
      MYSQL_PASSWORD: ${DB_PASSWORD}
    volumes:
      - 'mysql:/var/lib/mysql'
    restart: unless-stopped

  redis:
    image: 'redis:latest'
    command: redis-server --appendonly yes
    volumes:
      - 'redis:/data'
    restart: unless-stopped

volumes:
  traefik_data:
  mysql:
  redis:
  storage:
  logs:
```

### 2. Create .env file

```env
APP_NAME=Mixpost
APP_KEY=  # Generate at https://mixpost.app/tools/encryption-key-generator
APP_DEBUG=false
APP_DOMAIN=mixpost.yourdomain.com
APP_URL=https://${APP_DOMAIN}

DB_DATABASE=mixpost_db
DB_USERNAME=mixpost_user
DB_PASSWORD=your_secure_password

SSL_EMAIL=your@email.com
```

### 3. Start

```bash
docker compose up -d
docker compose logs -f  # Watch logs
```

### 4. Login

- URL: https://your-domain.com
- Email: admin@example.com
- Password: changeme

**Change password immediately!**

---

## Deployment Options

### 1. Railway (Easiest) ⭐
One-click Laravel deployment with managed databases.

```bash
# Install Railway CLI
npm i -g @railway/cli

# From mixpost-malone directory
railway login
railway init
railway up

# Add MySQL + Redis from Railway dashboard
# Set APP_URL to Railway domain
```

**Pros:** Zero config, GitHub auto-deploy, free tier
**Cost:** ~$5/month for small instance

### 2. Fly.io (Global PoPs)
Edge deployment with multiple regions.

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# From mixpost-malone directory
fly launch  # Auto-detects Laravel
fly deploy

# Add Postgres + Redis
fly postgres create
fly redis create
```

**Pros:** Global edge, great latency, free allowance
**Cost:** ~$5-10/month

### 3. Render
Simple Docker deployment.

```yaml
# render.yaml
services:
  - type: web
    name: mixpost
    env: docker
    dockerfilePath: ./Dockerfile
    envVars:
      - key: APP_KEY
        generateValue: true
databases:
  - name: mixpost-db
    databaseName: mixpost
```

**Pros:** Easy setup, managed SSL
**Cost:** ~$7/month

### 4. Self-Hosted Docker
Full control on any VPS (DigitalOcean, Linode, Hetzner).

See Docker Compose setup above.

**Pros:** Full control, cheapest at scale
**Cost:** $5-20/month VPS

### 5. Local Development (Windows)

For testing OAuth flows locally:

```bash
# Option A: ngrok tunnel
choco install ngrok
ngrok http 8000
# Use https://xxx.ngrok.io as APP_DOMAIN

# Option B: Cloudflare Tunnel (free)
cloudflared tunnel --url http://localhost:8000
```

---

## Next Steps

1. Configure social providers (Twitter, Facebook, etc.)
2. Connect accounts
3. Test posting from SOP Dashboard

---

## Puter.js for AI Features

Puter.js provides free browser-based AI (Claude, GPT, Gemini) with user-pays model.

**Use for:** Content generation UI, image analysis, frontend AI features.

```html
<script src="https://js.puter.com/v2/"></script>
<script>
// Generate social post with AI
puter.ai.chat('Write a tweet about our new product launch', {
  model: 'claude-sonnet-4'
}).then(puter.print);
</script>
```

**Not for:** Backend hosting (use Railway/Fly.io for MixPost itself)

---

## Using Our Fork (mixpost-malone)

Our fork adds: Twitch, Whatnot, Discord, YouTube, TikTok

```bash
git clone https://github.com/ludoplex/mixpost-malone
# Follow standard Laravel setup
composer install
npm install && npm run build
php artisan migrate
```
