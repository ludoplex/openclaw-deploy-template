# NetEng Agent Plan — Crystal Corp Infrastructure

**Agent:** neteng  
**Phase:** Foundation (Weeks 1-2)  
**Focus:** Infrastructure, DNS, CDN, Backups, Monitoring

---

## Scope

Deploy and configure all server infrastructure for Crystal Corp on the M4 VM, including reverse proxy, CDN integration, backup systems, and monitoring. Establish a production-ready, secure, and resilient hosting environment.

---

## Deliverables

| ID | Deliverable | Description |
|----|-------------|-------------|
| N1 | Caddy reverse proxy | HTTPS termination, auto-SSL, routing rules |
| N2 | Cloudflare DNS | DNS configuration, proxy settings, security rules |
| N3 | Bunny CDN | Asset delivery for images, audio, game files |
| N4 | Backup system | Automated daily backups to Backblaze B2 via rclone |
| N5 | Monitoring | UptimeRobot alerts, Fail2Ban security |
| N6 | llama.cpp server | Local LLM for chat support (Qwen 2.5 7B) |
| N7 | Runbook documentation | Emergency procedures for Vincent |

---

## Task Schedule

### Week 1: Core Infrastructure

| Day | Task | Hours | Output |
|-----|------|-------|--------|
| 1 | Configure Cloudflare DNS, point to M4 public IP | 2 | DNS records active |
| 1 | Set up Cloudflare security rules (rate limiting, bot protection) | 1 | Security baseline |
| 2 | Install Caddy 2.8+, configure Caddyfile for HTTPS | 3 | HTTPS working |
| 2 | Configure Caddy reverse proxy routes | 2 | Routing for /game, /api, /assets |
| 3 | Set up Bunny CDN account, create pull zone | 2 | CDN account active |
| 3 | Configure Bunny CDN origin, cache rules | 2 | Assets served via CDN |
| 4 | Install llama.cpp, compile with Metal acceleration | 3 | llama-server binary ready |
| 4 | Download Qwen 2.5 7B Q4_K_M model | 1 | Model available |
| 4 | Configure llama-server as launchd service | 2 | LLM API on :8080 |
| 5 | Set up Backblaze B2 bucket (encrypted) | 1 | Bucket created |
| 5 | Install and configure rclone with B2 remote | 2 | rclone connected |
| 5 | Create backup script (tar, encrypt, sync) | 2 | backup-now.sh working |
| 6 | Configure launchd cron for daily 3 AM backups | 1 | Automated backups |
| 6 | Set up UptimeRobot monitors (HTTPS, API) | 1 | Uptime alerts active |
| 6 | Install and configure Fail2Ban | 2 | SSH/HTTP protection |
| 7 | Create emergency runbooks (services, DNS failover) | 3 | Runbook drafts |
| 7 | Test full backup/restore cycle | 2 | Restore verified |

### Week 2: Hardening & Documentation

| Day | Task | Hours | Output |
|-----|------|-------|--------|
| 8 | Configure firewall rules (pf on macOS) | 2 | Firewall active |
| 8 | Set up SSH key-only authentication | 1 | Password auth disabled |
| 9 | Configure log rotation for Caddy, llama.cpp | 1 | Logs managed |
| 9 | Set up Oracle Cloud cold standby VM (ARM) | 3 | Failover target ready |
| 10 | Test DNS failover procedure | 2 | Failover documented |
| 10 | Create static maintenance page (GitHub Pages) | 1 | maintenance.crystalarcade.gg |
| 11 | Set up Bitwarden vault, add credentials | 2 | Credentials centralized |
| 11 | Grant Vincent emergency access (72-hour delay) | 1 | Emergency access configured |
| 12-14 | Write comprehensive runbooks | 6 | Complete documentation |

---

## Inputs Required

| Input | Source | Required By |
|-------|--------|-------------|
| Domain name (crystalarcade.gg) | sitecraft agent (Njalla) | Day 1 |
| M4 VM access | Existing infrastructure | Day 1 |
| Cloudflare account credentials | Existing or create | Day 1 |
| Vincent's Bitwarden account | Vincent | Day 11 |

---

## Outputs Produced

| Output | Location | Consumer |
|--------|----------|----------|
| Caddy configuration | /etc/caddy/Caddyfile | sitecraft, webdev |
| CDN pull zone URL | Bunny dashboard | webdev (asset URLs) |
| LLM API endpoint | localhost:8080 | ops (Chatwoot integration) |
| Backup bucket | B2: crystal-corp-backups | ops |
| Runbooks | /docs/runbooks/ | Vincent, ops |
| DNS records | Cloudflare dashboard | sitecraft |

---

## Success Criteria

| Criterion | Measurement | Target |
|-----------|-------------|--------|
| HTTPS operational | SSL Labs test | A+ rating |
| CDN latency | Bunny analytics | < 50ms global |
| Backup success | B2 console | Daily backups present |
| LLM response time | curl timing | < 3s for typical query |
| Uptime monitoring | UptimeRobot | All monitors green |
| Failover tested | Manual test | DNS switch < 10 min |

---

## Handoff to Next Phase

**To sitecraft (concurrent):**
- DNS records configured for apex and subdomains
- HTTPS working on primary domain
- Caddy ready to serve static files

**To webdev (Week 3):**
- CDN pull zone URL for asset loading
- Reverse proxy routes configured for /game/*
- Server environment documented

**To ops (Week 5):**
- LLM API endpoint for Chatwoot integration
- Backup system operational
- Monitoring handoff

---

## Risk Mitigations

| Risk | Mitigation |
|------|------------|
| M4 unavailable during setup | Have Oracle Cloud VM pre-provisioned |
| Cloudflare TOS concern | Bunny has DNS capability as backup |
| llama.cpp compilation issues | Fallback to pre-built binary |
| Backup encryption key loss | Key stored in Bitwarden with emergency access |

---

## Commands Reference

```bash
# Caddy
sudo systemctl status caddy
sudo systemctl restart caddy
caddy validate --config /etc/caddy/Caddyfile

# llama.cpp
ps aux | grep llama-server
launchctl list | grep llama

# Backup
./scripts/backup-now.sh
rclone ls b2:crystal-corp-backups

# Monitoring
fail2ban-client status
tail -f /var/log/caddy/access.log
```
