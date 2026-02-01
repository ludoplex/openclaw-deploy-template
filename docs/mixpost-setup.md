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

## For Local Development (Windows)

Since MixPost needs public domain for OAuth callbacks, options:

1. **ngrok** - Tunnel localhost to public URL
2. **Cloudflare Tunnel** - Free tunnel service
3. **Deploy to VPS** - DigitalOcean/Linode/etc

### Using ngrok

```bash
# Install ngrok
choco install ngrok

# Start tunnel
ngrok http 8000

# Note the https://xxx.ngrok.io URL
# Use this as APP_DOMAIN
```

---

## Next Steps

1. Configure social providers (Twitter, Facebook, etc.)
2. Connect accounts
3. Test posting from SOP Dashboard

## Using Our Fork (mixpost-malone)

Our fork adds: Twitch, Whatnot, Discord, YouTube, TikTok

```bash
git clone https://github.com/ludoplex/mixpost-malone
# Follow standard Laravel setup
composer install
npm install && npm run build
php artisan migrate
```
