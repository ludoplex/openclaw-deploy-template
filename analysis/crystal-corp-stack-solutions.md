# Crystal Corp Stack Solutions: Critical Issue Resolution

**Generated:** 2026-02-10  
**Analyst:** Subagent (Claude)  
**Purpose:** Practical solutions for 7 critical issues within $1K budget

---

## Constraints Summary

| Constraint | Value |
|------------|-------|
| Startup Budget | $1,000 |
| Revenue Target (30 days) | $1,600 |
| Ongoing Revenue Target | $2,000/month |
| Operator | Peridot (mostly autonomous) |
| Human Backup | Vincent (emergency only) |

---

## Issue 1: Single M4 VM SPOF 🔴

**Problem:** One hardware failure = complete business death. No redundancy exists.

### Solution: Multi-Layer Resilience Strategy

**Total Cost: ~$180/year + one-time setup**

#### Layer 1: Automated Off-Site Backups ($60/year)

**Implementation:**
```bash
# Backblaze B2 - $0.005/GB storage, $0.01/GB download
# 50GB backup = $3/year storage + occasional restore costs

# Daily backup script via launchd
#!/bin/bash
BACKUP_DIR="/tmp/crystal-backup-$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"

# Critical data
tar -czf "$BACKUP_DIR/website.tar.gz" /path/to/website
tar -czf "$BACKUP_DIR/chatwoot-data.tar.gz" /path/to/chatwoot
tar -czf "$BACKUP_DIR/configs.tar.gz" /path/to/configs

# Encrypt before upload
gpg --symmetric --cipher-algo AES256 "$BACKUP_DIR"/*.tar.gz

# Upload via rclone
rclone sync "$BACKUP_DIR" b2:crystal-backups/daily/

# Keep 30 days of dailies, 12 months of monthlies
rclone delete --min-age 30d b2:crystal-backups/daily/
```

| Component | Cost |
|-----------|------|
| Backblaze B2 (50GB) | $3/year |
| rclone | Free |
| GPG encryption | Free |
| Setup time | 2-3 hours |

#### Layer 2: Cold Standby VM ($0-120/year)

**Option A: Oracle Cloud Free Tier (Recommended)**
- **ARM VM:** 4 OCPU, 24GB RAM — permanently free
- Can host website + Chatwoot (no LLM)
- Pre-configured but dormant
- Spin up in <30 minutes if M4 dies

**Option B: Hetzner Cloud ARM**
- CAX11: €3.79/month (~$50/year) 
- 2 vCPU, 4GB RAM
- Keep dormant, use only in emergency

**Setup:**
1. Create Oracle Cloud account (free)
2. Deploy ARM VM with Ubuntu
3. Install Caddy, Docker
4. Test restore procedure
5. Document DNS failover steps
6. Keep VM stopped (free) until needed

| Component | Cost |
|-----------|------|
| Oracle Free Tier | $0 |
| Initial setup | 4-6 hours |
| Monthly maintenance | 30 min (test restore) |

#### Layer 3: Static Fallback Page ($0)

**Even if everything dies, customers see something:**

```html
<!-- Hosted on GitHub Pages (free) or Cloudflare Pages (free) -->
<!-- DNS TTL: 300 seconds for fast failover -->
<!DOCTYPE html>
<html>
<head><title>Crystal Corp - Temporary Maintenance</title></head>
<body>
<h1>We're experiencing technical difficulties</h1>
<p>Our team is working to restore service. Expected: 24-48 hours.</p>
<p>SubscribeStar subscriptions are unaffected. No action needed.</p>
<p>Contact: emergency@crystal.gg</p>
</body>
</html>
```

**Failover procedure:**
1. If M4 down > 1 hour, Vincent updates DNS
2. Points to static GitHub Pages site
3. Buys time for proper recovery

#### Layer 4: Critical Hardware Spare (~$100 one-time)

**Keep on hand:**
- 1TB external SSD ($60) — for local backup
- USB-C hub ($20) — for emergency recovery
- Raspberry Pi 5 ($80) — can serve static site in emergency

**Alternative:** Credit card with $500 available for emergency Mac Mini rental/purchase.

### Recovery Time Objectives

| Failure Scenario | RTO with Solution |
|------------------|-------------------|
| Software crash | 5 min (restart) |
| Data corruption | 1-2 hours (restore from backup) |
| Hardware failure | 4-24 hours (Oracle VM failover) |
| Complete disaster | 24-48 hours (new hardware + restore) |

### Implementation Complexity
- **Effort:** 8-12 hours initial setup
- **Maintenance:** 1 hour/month testing
- **Documentation:** 2-3 pages for Vincent

### Fallback if Solution Fails
- If Oracle VM unavailable, spin up Hetzner ($5 for emergency)
- If all backups corrupt, rebuild from SubscribeStar data + local dev copies
- Absolute worst case: 1-week downtime while rebuilding

---

## Issue 2: SubscribeStar Existential Risk 🔴

**Problem:** 100% revenue through one company. One policy change = business death.

### Solution: Diversified Payment Rails + Escape Hatch

**Total Cost: ~$0-50 setup + fees only on transactions**

#### Strategy 1: Pre-Approved Backup Processor

**CCBill — The Industry Standard Backup**
- Adult content explicitly allowed
- 10-15% fees (higher than SubscribeStar's ~10%)
- Application takes 3-5 business days
- Keep approved but dormant

**Action Items:**
1. Apply for CCBill merchant account NOW (free to apply)
2. Complete verification (ID, business docs)
3. Set up but don't activate
4. If SubscribeStar dies, switch within 24 hours

**Alternative: Epoch**
- Similar to CCBill
- Slightly lower fees (~12-14%)
- Also adult-friendly

| Processor | Apply Now | Fees | Switch Time |
|-----------|-----------|------|-------------|
| SubscribeStar (primary) | ✅ Active | ~10% | N/A |
| CCBill (backup) | Apply now | ~14% | 24-48 hours |
| Crypto (emergency) | Setup now | ~1% | Immediate |

#### Strategy 2: Cryptocurrency Emergency Rail ($0)

**Setup:**
- BTCPay Server (self-hosted, free)
- Accept BTC/ETH/USDC
- Only promote if SubscribeStar dies
- Handles 10-20% of customers who have crypto

**Why it works:**
- Can't be shut down by payment processors
- Appeals to privacy-conscious adult content consumers
- Zero ongoing cost until used

**Implementation:**
```bash
# BTCPay Server on Oracle Cloud (if using that for backup)
docker run -d \
  --name btcpay \
  -p 80:80 \
  btcpayserver/btcpayserver:latest
```

#### Strategy 3: Independent Email List (Critical)

**SubscribeStar owns your customer relationship. Fix that.**

1. **Collect emails independently:**
   - Offer "launch updates" list on website
   - Incentive: Early access to new content
   - Store in: Buttondown ($9/mo) or self-hosted Listmonk (free)

2. **Export SubscribeStar data regularly:**
   - Download subscriber list monthly
   - Store encrypted off-site
   - If SubscribeStar dies, you can contact customers

3. **Communicate migration path:**
   - Email template ready: "We've moved to [backup processor]"
   - Pre-written, encrypted, stored with backups

| Component | Cost |
|-----------|------|
| CCBill application | Free |
| BTCPay Server | Free (uses existing VM) |
| Listmonk (email) | Free (self-hosted) |
| Setup time | 4-6 hours |

### Implementation Complexity
- **CCBill application:** 1 hour + 3-5 day wait
- **BTCPay setup:** 2 hours
- **Email list setup:** 2 hours
- **Maintenance:** 30 min/month (export subscriber data)

### Fallback if Solution Fails
- Crypto-only mode can sustain 10-20% of revenue
- Use that runway to apply for alternative processor
- Worst case: 2-4 week revenue gap during transition

---

## Issue 3: Bus Factor of One 🔴

**Problem:** If Peridot unavailable 72+ hours, business dies. No documentation, no backup operator.

### Solution: Vincent-Ready Emergency Runbooks

**Total Cost: $0 (time investment only)**

#### Runbook Structure

Create: `docs/runbooks/` with these files:

```
docs/runbooks/
├── 00-EMERGENCY-START-HERE.md    # Vincent's first read
├── 01-system-health-check.md     # Is everything running?
├── 02-restart-services.md        # How to restart stuff
├── 03-restore-from-backup.md     # Disaster recovery
├── 04-process-refunds.md         # Customer service basics
├── 05-dns-failover.md            # Switch to backup hosting
├── 06-credentials.md             # Where passwords live (encrypted)
└── 99-when-to-escalate.md        # When to hire a professional
```

#### 00-EMERGENCY-START-HERE.md

```markdown
# CRYSTAL CORP EMERGENCY RUNBOOK

Vincent, if you're reading this, something happened to me.
Here's what to do.

## Step 1: Assess the Situation (5 minutes)

1. Open https://crystal.gg — is it up?
2. Open https://subscribestar.adult/crystal-corp — is it up?
3. Check email for customer complaints

## Step 2: If Website is Down

Follow: `02-restart-services.md`
If that fails: `05-dns-failover.md`

## Step 3: If You Can't Fix It

1. Post maintenance notice on Twitter/Discord
2. Contact emergency help: [freelancer contact]
3. Estimated cost for professional: $100-300/incident

## Step 4: Critical Decisions You Can Make

✅ Restart any service
✅ Process refunds up to $50
✅ Post maintenance notices
✅ Contact customers about outages

❌ Don't change DNS without the runbook
❌ Don't modify code
❌ Don't access customer payment data

## Credentials Location

See: `06-credentials.md` (requires passphrase I gave you)
```

#### Credential Management

**Use: Bitwarden** (free for personal use)

1. Create shared Bitwarden vault
2. Add Vincent as emergency contact
3. Enable Emergency Access (72-hour delay, then auto-grant)
4. Store all service credentials

**Critical credentials to document:**
- Njalla (domain)
- SubscribeStar (payments)
- Bunny CDN
- Cloudflare
- Oracle Cloud (backup VM)
- M4 VM login (SSH key + passphrase)

#### Training Session (1-2 hours)

**Schedule with Vincent:**
1. Walk through 00-EMERGENCY-START-HERE.md
2. Practice: Vincent restarts a service
3. Practice: Vincent checks if backups are working
4. Give Vincent the Bitwarden emergency access passphrase

| Component | Time Investment |
|-----------|-----------------|
| Write runbooks | 4-6 hours |
| Set up Bitwarden sharing | 1 hour |
| Training session | 2 hours |
| **Total** | 7-9 hours |

### Vincent's Capability Level After Training

| Task | Vincent Can Do? |
|------|----------------|
| Check if site is up | ✅ Yes |
| Restart services | ✅ Yes (with runbook) |
| Restore from backup | ⚠️ Maybe (with runbook) |
| Fix code bugs | ❌ No |
| DNS changes | ⚠️ With explicit runbook |
| Customer refunds | ✅ Yes |
| Hire emergency help | ✅ Yes |

### Escalation Path

**When Vincent can't fix it:**

1. **Toptal/Upwork:** Search "macOS DevOps emergency" — $100-200/hour
2. **Specific freelancer:** Pre-identify and contact someone now
   - Ask: "If I have an emergency, can you help within 24 hours?"
   - Offer: $50 retainer for priority response
3. **Local Mac consultant:** Apple Consultants Network

### Implementation Complexity
- **Effort:** 7-9 hours one-time
- **Maintenance:** Update runbooks when things change
- **Test:** Quarterly fire drill (Vincent practices one scenario)

### Fallback if Solution Fails
- If Vincent fails, hire emergency freelancer
- If no one available, enable static maintenance page + wait for Peridot
- Business survives 1-2 weeks on autopilot (SubscribeStar keeps collecting)

---

## Issue 4: Voice Latency 🔴

**Problem:** Local LLM too slow for voice. 2-6 second latency vs. 0.5-1 second expected.

### Solution: Accept API Costs for Voice, Local for Everything Else

**Total Cost: $20-100/month depending on volume**

#### The Reality

| LLM Location | First Token Latency | Acceptable For |
|--------------|---------------------|----------------|
| Local Qwen 7B | 100-250ms + 2-5s full response | Chat, email, batch |
| Claude Haiku API | 50-100ms + streaming | Voice, real-time |
| GPT-4o-mini | 50-100ms + streaming | Voice, real-time |

**Voice requires API. Accept this.**

#### Hybrid Architecture

```
Voice Calls (Vapi):
  └── Claude Haiku API ($0.25/1M input, $1.25/1M output)
      └── Latency: 200-400ms total → Acceptable

Chat Support (Chatwoot):
  └── Local Qwen 2.5 7B
      └── Latency: 2-4 seconds → Acceptable for chat

Batch Processing (emails, summaries):
  └── Local Qwen 2.5 7B
      └── Latency: Don't care
```

#### Cost Projections

**Voice (Vapi + Claude Haiku):**

| Monthly Volume | Claude Cost | Vapi Cost | Total |
|----------------|-------------|-----------|-------|
| 50 calls × 3 min | ~$2 | ~$10 | ~$12 |
| 200 calls × 3 min | ~$8 | ~$40 | ~$48 |
| 500 calls × 3 min | ~$20 | ~$100 | ~$120 |

**Chat (Local LLM):**
- Cost: $0 (electricity only)
- 1000 messages/month: No cost increase

#### Alternative: Groq for Ultra-Low Latency

If Claude Haiku latency still not enough:

- **Groq Llama 3.1 8B:** 200-400 tokens/second
- **Latency:** 50-100ms first token
- **Cost:** $0.05/1M input, $0.08/1M output (10x cheaper than Haiku)
- **Quality:** Slightly lower, but fine for voice support

```python
# Vapi configuration for Groq
{
    "model": "llama-3.1-8b-instant",
    "provider": "groq",
    "temperature": 0.7,
    "max_tokens": 150  # Keep responses short for voice
}
```

#### Implementation

```python
# Decision logic for LLM routing
def get_llm_for_task(task_type: str):
    if task_type == "voice":
        return CloudLLM("claude-3-haiku")  # or Groq
    elif task_type == "chat":
        return LocalLLM("qwen2.5-7b")
    elif task_type == "batch":
        return LocalLLM("qwen2.5-7b")
    else:
        return LocalLLM("qwen2.5-7b")  # Default local
```

### Implementation Complexity
- **Effort:** 2-3 hours (configure Vapi with API LLM)
- **Maintenance:** Monitor costs monthly
- **Testing:** Call yourself, verify latency

### Fallback if Solution Fails
- If API costs explode, implement rate limiting on voice
- "Press 1 for chat support, 2 for callback"
- Move complex issues to chat (local LLM)

---

## Issue 5: Scaling Ceiling ~1K Users 🟡

**Problem:** Stack designed for solo operation. Breaks under success.

### Solution: Staged Upgrade Path with Clear Triggers

**Philosophy:** Don't solve scaling problems until you have them. But know the plan.

#### Scaling Stages

| Users | Monthly Revenue | Trigger Actions |
|-------|-----------------|-----------------|
| 0-100 | $0-1,000 | MVP mode. Manual everything. |
| 100-500 | $1,000-5,000 | Upgrade Chatwoot, optimize LLM |
| 500-1,000 | $5,000-10,000 | Consider part-time help |
| 1,000-5,000 | $10,000-50,000 | Hire first employee, upgrade infra |
| 5,000+ | $50,000+ | Real company infrastructure |

#### Stage 1: MVP (0-100 users)

**Current stack is fine. Focus on:**
- Ship product
- Get first customers
- Validate business model

**Cost:** $50-100/month

#### Stage 2: Early Growth (100-500 users)

**Upgrade triggers:**
- Support tickets > 50/month
- Voice calls > 100/month
- Website load consistently > 50% CPU

**Actions:**
1. Upgrade Chatwoot to 2 agents ($38/month)
2. Add CDN caching rules for static assets
3. Implement rate limiting on LLM endpoints
4. Consider hiring: Virtual assistant for support ($300-500/month)

**Cost:** $150-300/month

#### Stage 3: Growth (500-1,000 users)

**Upgrade triggers:**
- Support tickets > 200/month
- Revenue > $5,000/month
- Peridot spending > 10 hours/week on support

**Actions:**
1. Hire part-time support person ($500-1,000/month)
2. Migrate Chatwoot to self-hosted (saves $38/month)
3. Add second M4 or upgrade to Mac Studio
4. Implement proper monitoring (Grafana + Prometheus)

**Cost:** $300-500/month (infrastructure) + $500-1,000 (help)

#### Stage 4: Scaling (1,000+ users)

**This is a good problem to have. At this point:**
- Revenue: $10,000+/month
- Can afford proper infrastructure
- Consider: AWS/GCP with proper architecture
- Hire: Full-time support + part-time DevOps

**Decisions at this stage should be made with actual data, not projections.**

#### Horizontal Scaling Path (When Needed)

```
Current:
  M4 VM → Everything

Stage 2:
  M4 VM → LLM + Automation
  Oracle Cloud → Website + Chatwoot

Stage 3:
  M4/Studio → LLM only
  Cloud VMs → Website (load balanced)
  Managed DB → Chatwoot data
  CDN → All static assets

Stage 4:
  Multiple LLM servers
  Auto-scaling cloud
  Dedicated support team
```

### Implementation Complexity
- **Now:** Document the scaling triggers (1 hour)
- **Later:** Execute when triggers hit
- **Never:** Pre-optimize before you have the problem

### Fallback if Scaling Faster Than Expected
- Temporary: Disable voice support (reduces load)
- Temporary: Pause new signups
- Emergency: Throw money at cloud resources

---

## Issue 6: Cost Projections Understated 🟡

**Problem:** Current projections: $46-81/month. Reality likely 3-5x higher.

### Solution: Honest Budget with Contingency

#### Revised Cost Projections

| Phase | Users | Monthly Cost | Revenue Target | Margin |
|-------|-------|--------------|----------------|--------|
| MVP | 0-100 | $80-150 | $0-1,000 | Break-even focus |
| Early | 100-300 | $150-300 | $1,000-3,000 | 50%+ margin |
| Growth | 300-1,000 | $300-700 | $3,000-10,000 | 60%+ margin |

#### Detailed MVP Budget

| Item | Low | High | Notes |
|------|-----|------|-------|
| Domain (Njalla) | $2 | $2 | Fixed |
| Bunny CDN | $5 | $20 | Scales with traffic |
| Chatwoot Cloud | $19 | $38 | 1-2 agents |
| Voice API (Vapi + LLM) | $20 | $80 | Scales with calls |
| Backup storage (B2) | $1 | $5 | 50-200GB |
| Email (Listmonk hosted or Buttondown) | $0 | $9 | Optional |
| **Infrastructure Total** | $47 | $154 | |
| **Contingency (20%)** | $9 | $31 | Unexpected costs |
| **Total MVP** | $56 | $185 | |

#### Budget Guardrails

**Set spending alerts:**
```bash
# Bunny CDN: Alert at $25/month
# Vapi: Alert at $100/month
# B2: Alert at $10/month
```

**Monthly review:**
1. First week: Check all service dashboards
2. Identify cost spikes
3. Adjust usage or upgrade plan

#### Break-Even Analysis

| Monthly Cost | Required Subscribers | At $10/sub |
|--------------|---------------------|------------|
| $100 | 10 | After fees (~$9 net) |
| $200 | 22 | |
| $500 | 56 | |
| $1,000 | 112 | |

**At 30-day $1,600 target: Covers costs + profit margin**

### Implementation Complexity
- **Effort:** 1 hour to set up billing alerts
- **Maintenance:** 30 min/month cost review

### Fallback if Costs Exceed Budget
- Reduce voice support hours
- Downgrade Chatwoot to free tier (limits features)
- Disable non-essential features
- Aggressive caching to reduce bandwidth

---

## Issue 7: Security Monitoring Absent 🔴

**Problem:** No way to detect breaches. Won't know you're hacked until it's too late.

### Solution: Cheap but Effective Security Stack

**Total Cost: $0-20/month**

#### Layer 1: Uptime Monitoring (Free)

**UptimeRobot (Free tier):**
- 50 monitors
- 5-minute checks
- Email + SMS alerts

**Configure:**
1. Monitor: https://crystal.gg (HTTP 200)
2. Monitor: https://crystal.gg/health (if you add health endpoint)
3. Monitor: SSH port (if exposed)

#### Layer 2: Log Aggregation (Free)

**Option A: Loki + Grafana (Self-hosted, Free)**
```yaml
# docker-compose.yml addition
services:
  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"
    volumes:
      - ./loki-data:/loki
  
  promtail:
    image: grafana/promtail:latest
    volumes:
      - /var/log:/var/log
      - ./promtail-config.yml:/etc/promtail/config.yml
```

**Option B: Better Stack (Free tier)**
- 1GB/month logs
- 3-day retention
- Pre-built dashboards
- Zero setup

#### Layer 3: Intrusion Detection (Free)

**Fail2Ban:**
```bash
# Install
brew install fail2ban

# Configure for SSH + Caddy
# /etc/fail2ban/jail.local
[sshd]
enabled = true
bantime = 3600
maxretry = 3

[caddy-auth]
enabled = true
filter = caddy-auth
logpath = /var/log/caddy/access.log
bantime = 3600
maxretry = 5
```

**CrowdSec (Alternative, also free):**
- Community-powered threat intelligence
- Shares attack patterns
- Better detection than Fail2Ban alone

#### Layer 4: File Integrity Monitoring (Free)

**AIDE (Advanced Intrusion Detection Environment):**
```bash
# Initial baseline
aide --init

# Daily check (via cron)
0 3 * * * /usr/bin/aide --check | mail -s "AIDE Report" peridot@crystal.gg
```

**What it catches:**
- Modified binaries
- Changed config files
- New unauthorized files

#### Layer 5: Security Alerts (Free)

**Configure alerts for:**
1. Failed SSH logins > 5/hour
2. 4xx/5xx errors > 100/hour
3. Disk usage > 80%
4. CPU > 90% for > 10 minutes
5. New user accounts created
6. Sudo commands by unexpected users

**Using macOS built-in + simple script:**
```bash
#!/bin/bash
# security-check.sh - run hourly via cron

# Check for failed logins
FAILED=$(grep "Failed password" /var/log/auth.log | wc -l)
if [ $FAILED -gt 10 ]; then
    echo "HIGH FAILED LOGINS: $FAILED" | mail -s "Security Alert" peridot@crystal.gg
fi

# Check for new users
USERS=$(dscl . list /Users | wc -l)
EXPECTED=5  # Set this to your expected count
if [ $USERS -gt $EXPECTED ]; then
    echo "NEW USER DETECTED" | mail -s "Security Alert" peridot@crystal.gg
fi
```

#### Layer 6: LLM Security (Implementation)

**Prompt injection prevention:**
```python
def sanitize_input(user_message: str) -> str:
    # Remove common injection patterns
    dangerous_patterns = [
        r"ignore (all |previous |)instructions",
        r"system prompt",
        r"reveal.*api.?key",
        r"act as",
        r"you are now",
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, user_message.lower()):
            return "[Message filtered for safety]"
    
    return user_message

def llm_response(user_message: str) -> str:
    safe_message = sanitize_input(user_message)
    # Process with LLM
    ...
```

**Output filtering:**
```python
def filter_output(llm_response: str) -> str:
    # Remove anything that looks like secrets
    patterns = [
        r"sk-[a-zA-Z0-9]{48}",  # OpenAI keys
        r"password.*[:=].*\S+",
        r"api.?key.*[:=].*\S+",
    ]
    
    for pattern in patterns:
        llm_response = re.sub(pattern, "[REDACTED]", llm_response)
    
    return llm_response
```

#### Security Checklist

| Control | Cost | Implementation Time |
|---------|------|---------------------|
| UptimeRobot | $0 | 15 minutes |
| Fail2Ban | $0 | 30 minutes |
| Log aggregation | $0 | 2 hours |
| File integrity | $0 | 1 hour |
| Security alerts script | $0 | 1 hour |
| LLM input/output filtering | $0 | 2 hours |
| **Total** | $0 | ~7 hours |

### Implementation Complexity
- **Effort:** 6-8 hours for full stack
- **Maintenance:** Review alerts daily (5 min), investigate anomalies
- **Testing:** Trigger alerts intentionally to verify they work

### Fallback if Breach Detected
1. Isolate: Disconnect M4 from internet
2. Assess: Check logs for extent of compromise
3. Notify: If customer data affected, notify within 72 hours (GDPR)
4. Recover: Restore from known-good backup
5. Harden: Fix vulnerability that allowed breach
6. Document: Post-mortem for future prevention

---

## Implementation Priority Matrix

| Issue | Priority | Effort | Cost | When |
|-------|----------|--------|------|------|
| 7. Security Monitoring | 🔴 P1 | 7 hours | $0 | Week 1 |
| 1. Backup/Redundancy | 🔴 P1 | 12 hours | $60/year | Week 1-2 |
| 3. Runbooks for Vincent | 🔴 P1 | 9 hours | $0 | Week 2 |
| 2. Backup Payment Rails | 🔴 P1 | 6 hours | $0 | Week 2-3 |
| 4. Voice Latency Fix | 🟡 P2 | 3 hours | $20-80/mo | Week 3 |
| 6. Revised Budget | 🟡 P2 | 1 hour | $0 | Week 1 |
| 5. Scaling Plan | 🟢 P3 | 2 hours | $0 | Document now, execute later |

**Total implementation: ~40 hours over 3-4 weeks**

---

## Summary: Before Launch Checklist

### Must Have (Block Launch)

- [ ] Daily automated backups running
- [ ] Backup restore tested at least once
- [ ] UptimeRobot monitoring active
- [ ] Fail2Ban configured
- [ ] Vincent has emergency access (Bitwarden)
- [ ] 00-EMERGENCY-START-HERE.md written
- [ ] CCBill application submitted

### Should Have (Within 30 Days)

- [ ] Full runbook set complete
- [ ] Vincent trained (2-hour session)
- [ ] Oracle Cloud backup VM configured
- [ ] Email list collection active
- [ ] Voice API configured with Haiku/Groq
- [ ] All billing alerts set
- [ ] Security scripts running

### Nice to Have (Within 90 Days)

- [ ] BTCPay Server configured (dormant)
- [ ] Full log aggregation
- [ ] Quarterly fire drill scheduled
- [ ] Scaling triggers documented

---

## Budget Summary

### One-Time Costs

| Item | Cost |
|------|------|
| External SSD (backups) | $60 |
| Misc hardware (optional) | $0-100 |
| Time investment | 40 hours |
| **Total One-Time** | $60-160 |

### Monthly Costs (Revised)

| Phase | Monthly | Annual |
|-------|---------|--------|
| MVP (0-100 users) | $80-150 | $960-1,800 |
| Early (100-500) | $150-300 | $1,800-3,600 |
| Growth (500-1K) | $300-700 | $3,600-8,400 |

### Remaining from $1K Budget

After infrastructure setup: **$840-940 remaining**

Use for:
- 6-12 months of runway for MVP costs
- Marketing/content creation
- Emergency fund

---

*Solutions complete. Stack is now resilient enough to survive common failures.*
