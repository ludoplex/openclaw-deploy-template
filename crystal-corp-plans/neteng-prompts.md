# NetEng Agent Stage Prompts — Crystal Corp

Ready-to-paste prompts for each infrastructure stage. Each prompt is self-contained with all necessary context.

---

## Stage 1: Cloudflare DNS Setup (Day 1)

```
Configure Cloudflare DNS for Crystal Corp's Crystal Arcade game site.

**Domain:** crystalarcade.gg (registered via Njalla, nameservers pointed to Cloudflare)

**Target Server:** M4 VM at [PUBLIC_IP_HERE]

**DNS Records to Create:**
1. A record: @ → [PUBLIC_IP] (proxied)
2. A record: www → [PUBLIC_IP] (proxied)
3. CNAME: cdn → bunny CDN (DNS only, not proxied)
4. A record: api → [PUBLIC_IP] (proxied)

**Security Settings:**
1. Enable "Always Use HTTPS"
2. Set SSL/TLS to "Full (strict)"
3. Enable "Automatic HTTPS Rewrites"
4. Create rate limiting rule: 100 requests/minute per IP to /api/*
5. Enable Bot Fight Mode
6. Add firewall rule: Block requests from Tor exit nodes (optional)

**Page Rules (if needed):**
1. cdn.crystalarcade.gg/* — Cache Level: Standard, Edge TTL: 1 month

Verify DNS propagation and confirm the domain resolves correctly. Output the final DNS configuration summary.
```

---

## Stage 2: Caddy Installation & Configuration (Day 2)

```
Install and configure Caddy 2.8+ as the reverse proxy for Crystal Arcade on macOS (M4 VM).

**Requirements:**
- Auto-HTTPS via Let's Encrypt
- Reverse proxy routes for multiple services
- Access logging
- Security headers

**Installation:**
1. Install via Homebrew: brew install caddy
2. Create systemd-like launchd plist for auto-start

**Caddyfile Configuration:**
Create /etc/caddy/Caddyfile with:

```caddyfile
crystalarcade.gg {
    # Security headers
    header {
        X-Content-Type-Options nosniff
        X-Frame-Options DENY
        Referrer-Policy strict-origin-when-cross-origin
        -Server
    }
    
    # API routes (LLM, webhooks)
    handle /api/* {
        reverse_proxy localhost:3000
    }
    
    # LLM endpoint (internal)
    handle /llm/* {
        reverse_proxy localhost:8080
    }
    
    # Static site (Astro)
    handle {
        root * /var/www/crystalarcade
        file_server
        try_files {path} /index.html
    }
    
    # Logging
    log {
        output file /var/log/caddy/access.log
        format json
    }
}

www.crystalarcade.gg {
    redir https://crystalarcade.gg{uri} permanent
}
```

**Post-install:**
1. Validate config: caddy validate --config /etc/caddy/Caddyfile
2. Start Caddy: sudo caddy start
3. Verify HTTPS: curl -I https://crystalarcade.gg
4. Check SSL rating at ssllabs.com

Output the complete Caddyfile and verification results.
```

---

## Stage 3: Bunny CDN Setup (Day 3)

```
Set up Bunny.net CDN for serving Crystal Arcade game assets (images, audio, game files).

**Account Setup:**
1. Create Bunny.net account (if not exists)
2. Verify adult content is permitted (Bunny is adult-friendly)

**Pull Zone Configuration:**
- Zone Name: crystalarcade-assets
- Origin URL: https://crystalarcade.gg/assets
- Enable: Edge caching, Gzip compression, Brotli
- Cache TTL: 30 days for images, 7 days for JS/CSS
- Enable: Origin Shield (choose US West or closest to M4)

**Custom Hostname:**
- Add cdn.crystalarcade.gg as custom hostname
- Point CNAME in Cloudflare to [pullzone].b-cdn.net (DNS only, not proxied)

**Cache Rules:**
1. *.jpg, *.png, *.webp → 30 days
2. *.mp3, *.ogg → 30 days  
3. *.js, *.css → 7 days
4. *.json → 1 day (game data may update)

**Security:**
1. Enable Bunny Token Authentication for premium content
2. Set up hotlink protection (allow only crystalarcade.gg)
3. Enable basic DDoS protection

**Testing:**
1. Upload test image to origin
2. Verify delivery via cdn.crystalarcade.gg/test.jpg
3. Check response headers for cache hit

Output the pull zone URL, configuration summary, and test results.
```

---

## Stage 4: llama.cpp LLM Server Setup (Day 4)

```
Install and configure llama.cpp with Qwen 2.5 7B for local LLM inference on M4 Mac (Apple Silicon).

**Purpose:** Provide OpenAI-compatible API for Chatwoot chat support integration.

**Installation:**
1. Clone and build llama.cpp with Metal support:
   ```bash
   git clone https://github.com/ggerganov/llama.cpp
   cd llama.cpp
   make LLAMA_METAL=1
   ```

2. Download model:
   - Model: Qwen2.5-7B-Instruct-Q4_K_M.gguf
   - Source: HuggingFace (TheBloke or official Qwen)
   - Size: ~4.5GB

**Server Configuration:**
Run llama-server with:
```bash
./llama-server \
  --model ./models/qwen2.5-7b-instruct-q4_k_m.gguf \
  --host 127.0.0.1 \
  --port 8080 \
  --ctx-size 4096 \
  --n-gpu-layers 99 \
  --threads 8 \
  --parallel 2
```

**launchd Service:**
Create ~/Library/LaunchAgents/com.crystalcorp.llama.plist:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.crystalcorp.llama</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/llama.cpp/llama-server</string>
        <string>--model</string>
        <string>/path/to/models/qwen2.5-7b-instruct-q4_k_m.gguf</string>
        <string>--host</string>
        <string>127.0.0.1</string>
        <string>--port</string>
        <string>8080</string>
        <string>--ctx-size</string>
        <string>4096</string>
        <string>--n-gpu-layers</string>
        <string>99</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/llama-server.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/llama-server.err</string>
</dict>
</plist>
```

**Testing:**
```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5-7b",
    "messages": [{"role": "user", "content": "Hello, how can you help me?"}]
  }'
```

Output: Server running confirmation, response time metrics, launchd status.
```

---

## Stage 5: Backup System Setup (Day 5-6)

```
Configure automated encrypted backups to Backblaze B2 for Crystal Arcade.

**Backblaze B2 Setup:**
1. Create B2 bucket: crystal-corp-backups
2. Set bucket to private
3. Enable Object Lock (optional, for ransomware protection)
4. Create application key with read/write access to this bucket only

**rclone Configuration:**
```bash
brew install rclone

rclone config
# Create remote named "b2"
# Type: b2
# Account ID: [B2_ACCOUNT_ID]
# Application Key: [B2_APP_KEY]
```

**Backup Script (scripts/backup-now.sh):**
```bash
#!/bin/bash
set -e

BACKUP_DIR="/tmp/crystal-backup"
DATE=$(date +%Y%m%d-%H%M%S)
ENCRYPTION_KEY="[SECURE_KEY_FROM_BITWARDEN]"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup website files
tar -czf $BACKUP_DIR/website-$DATE.tar.gz /var/www/crystalarcade

# Backup configurations
tar -czf $BACKUP_DIR/configs-$DATE.tar.gz \
  /etc/caddy \
  ~/Library/LaunchAgents/com.crystalcorp.* \
  ~/.config/rclone

# Backup Listmonk data (if exists)
if [ -d "/var/lib/listmonk" ]; then
  tar -czf $BACKUP_DIR/listmonk-$DATE.tar.gz /var/lib/listmonk
fi

# Encrypt backups
for file in $BACKUP_DIR/*.tar.gz; do
  openssl enc -aes-256-cbc -salt -pbkdf2 -in "$file" -out "$file.enc" -pass pass:"$ENCRYPTION_KEY"
  rm "$file"
done

# Sync to B2
rclone sync $BACKUP_DIR b2:crystal-corp-backups --transfers 4

# Cleanup
rm -rf $BACKUP_DIR

# Keep only last 30 days of backups on B2
rclone delete b2:crystal-corp-backups --min-age 30d

echo "Backup completed: $DATE"
```

**launchd Cron (daily 3 AM):**
Create ~/Library/LaunchAgents/com.crystalcorp.backup.plist for daily execution.

**Verification:**
1. Run manual backup
2. List B2 contents: rclone ls b2:crystal-corp-backups
3. Test restore to /tmp/restore-test
4. Verify file integrity

Output: Backup script, launchd plist, successful test restore confirmation.
```

---

## Stage 6: Monitoring & Security (Day 6)

```
Set up monitoring and security for Crystal Arcade infrastructure.

**UptimeRobot Configuration:**
1. Create account at uptimerobot.com (free tier)
2. Add monitors:
   - HTTPS monitor: https://crystalarcade.gg (5-min interval)
   - Keyword monitor: https://crystalarcade.gg - check for "Crystal Arcade"
   - Port monitor: [M4_IP]:443 (HTTPS port)
3. Configure alerts:
   - Email to: [admin email]
   - Telegram webhook (optional)
4. Create status page (optional): status.crystalarcade.gg

**Fail2Ban Setup (or macOS equivalent):**
On macOS, use pf (packet filter) with custom scripts:

1. Create /etc/pf.anchors/crystal-block:
```
# Block list anchor
```

2. Create ban script for failed SSH attempts:
```bash
#!/bin/bash
# /usr/local/bin/ban-ip.sh
IP=$1
echo "block drop from $IP to any" >> /etc/pf.anchors/crystal-block
pfctl -f /etc/pf.conf
```

3. Monitor auth.log for failed attempts

**Alternative: Use Little Snitch or Lulu for GUI-based blocking**

**SSH Hardening:**
1. Disable password authentication in /etc/ssh/sshd_config:
   ```
   PasswordAuthentication no
   PubkeyAuthentication yes
   PermitRootLogin no
   ```
2. Restart SSH: sudo launchctl kickstart -k system/com.openssh.sshd

**Firewall (pf):**
Edit /etc/pf.conf:
```
# Default deny incoming
block in all
pass out all

# Allow established connections
pass in quick on lo0 all
pass in quick proto tcp from any to any port {22, 80, 443} keep state
```

Output: UptimeRobot dashboard screenshot, pf rules, SSH config changes.
```

---

## Stage 7: Oracle Cloud Failover Setup (Day 9)

```
Set up Oracle Cloud ARM VM as cold standby for disaster recovery.

**Oracle Cloud Setup:**
1. Create Oracle Cloud account (Always Free tier)
2. Create ARM-based VM:
   - Shape: VM.Standard.A1.Flex (4 OCPU, 24GB RAM - free tier)
   - OS: Ubuntu 22.04 LTS
   - Storage: 100GB boot volume
3. Note public IP for DNS failover

**Minimal Configuration (cold standby):**
1. Install Caddy: apt install caddy
2. Install rclone: apt install rclone
3. Configure rclone with B2 credentials
4. Create restore script:

```bash
#!/bin/bash
# /root/restore-from-backup.sh
set -e

ENCRYPTION_KEY="[KEY_FROM_BITWARDEN]"
RESTORE_DIR="/tmp/restore"

mkdir -p $RESTORE_DIR

# Get latest backup
LATEST=$(rclone ls b2:crystal-corp-backups | grep website | tail -1 | awk '{print $2}')
rclone copy b2:crystal-corp-backups/$LATEST $RESTORE_DIR

# Decrypt
openssl enc -aes-256-cbc -d -pbkdf2 -in $RESTORE_DIR/$LATEST -out $RESTORE_DIR/website.tar.gz -pass pass:"$ENCRYPTION_KEY"

# Extract
tar -xzf $RESTORE_DIR/website.tar.gz -C /var/www/

# Start Caddy
systemctl start caddy

echo "Restore complete. Update DNS to point to this server."
```

**DNS Failover Procedure:**
Document in runbook:
1. Log into Cloudflare
2. Update A record for @ from [M4_IP] to [ORACLE_IP]
3. Reduce TTL to 1 minute during incident
4. Run restore script on Oracle VM
5. Verify site is accessible

**Testing:**
1. Run restore script on Oracle VM
2. Access via Oracle IP directly (hosts file override)
3. Verify basic functionality

Output: Oracle VM IP, restore script, failover procedure documented.
```

---

## Stage 8: Runbook Documentation (Day 12-14)

```
Create comprehensive runbooks for Vincent's emergency use.

**Runbook Structure:**
Create in /docs/runbooks/:

**00-EMERGENCY-START-HERE.md:**
- Quick decision tree for common issues
- Who to contact, when to escalate
- Critical credentials location (Bitwarden)

**01-check-status.md:**
- How to verify site is up
- UptimeRobot dashboard URL
- Manual curl commands

**02-restart-services.md:**
- SSH connection instructions
- Caddy restart: sudo systemctl restart caddy
- LLM restart: launchctl kickstart -k ~/Library/LaunchAgents/com.crystalcorp.llama
- Full reboot procedure

**03-dns-failover.md:**
- Step-by-step Cloudflare login
- Screenshot of where to change A record
- Oracle VM IP and credentials
- Restore script location and usage

**04-process-refund.md:**
- SubscribeStar login procedure
- Finding subscriber
- Processing refund
- Template response to customer

**05-post-maintenance-notice.md:**
- Discord posting instructions
- Twitter posting instructions
- Template messages for common scenarios

**Format Requirements:**
- Each runbook standalone (no cross-references)
- Include screenshots where helpful
- Assume Vincent has zero technical knowledge
- Include "If this doesn't work, call [emergency freelancer]"

Output: All runbook files with complete, tested procedures.
```

---

## Verification Checklist

After completing all stages, verify:

```
[ ] DNS resolves crystalarcade.gg to M4 IP
[ ] HTTPS works with valid certificate (A+ SSL Labs)
[ ] Caddy serves test page correctly
[ ] cdn.crystalarcade.gg serves assets via Bunny
[ ] llama-server responds on localhost:8080
[ ] Backup script runs successfully
[ ] B2 bucket contains encrypted backup
[ ] UptimeRobot shows all monitors green
[ ] SSH key-only authentication works
[ ] Oracle VM can restore from backup
[ ] All runbooks reviewed and tested
[ ] Vincent has Bitwarden emergency access
```
