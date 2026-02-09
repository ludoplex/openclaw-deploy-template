# DEPLOYMENT.md - Cloud VM Deployment Guide

**Purpose:** Ensure all local resources are available when deploying agents to cloud VMs.

---

## 📦 What Gets Deployed

### 1. Git-Tracked Workspace (Auto-deployed)
Everything in `~/.openclaw/workspace/` syncs via git:
- `AGENTS.md`, `SOUL.md`, `USER.md`, `IDENTITY.md`
- `MEMORY.md`, `HEARTBEAT.md`, `DEVICE_TOOLS.md`
- `automation/` - entity profiles, templates, scripts
- `skills/` - ported Claude.ai skills
- `scripts/` - utility scripts
- `docs/` - OpenClaw documentation

### 2. Local Resources (Need Manual Sync)

| Resource | Local Path | Size | Priority |
|----------|-----------|------|----------|
| Zoho API System | `C:\zoho-console-api-module-system\` | ~50MB | HIGH |
| rclone config | `%APPDATA%\rclone\rclone.conf` | <1KB | HIGH (has OneDrive tokens) |
| llamafile binary | `workspace\bin\llamafile.exe` | ~2MB | MEDIUM |
| Qwen model | `workspace\models\qwen2.5-7b-instruct-q3_k_m.gguf` | ~3.5GB | LOW (re-download) |
| Agent workspaces | `~/.openclaw/agents/*/` | varies | HIGH |

### 3. Credentials & Tokens (Sensitive)

| Credential | Location | Notes |
|------------|----------|-------|
| Zoho OAuth tokens | `zoho-console-api-module-system/config/accounts.json` | Refresh tokens for boss/mine |
| rclone OneDrive | `%APPDATA%\rclone\rclone.conf` | Rachel's OneDrive access |
| OpenClaw config | `~/.openclaw/config.yaml` | API keys, channel configs |

---

## 🚀 Deployment Steps

### Option A: Full Clone (Recommended)

```bash
# On cloud VM after base OpenClaw install:

# 1. Clone workspace
git clone https://github.com/ludoplex/openclaw-workspace.git ~/.openclaw/workspace

# 2. Copy Zoho API system (from local backup or separate repo)
git clone https://github.com/ludoplex/zoho-console-api.git ~/zoho-console-api-module-system

# 3. Restore rclone config (from secure vault)
mkdir -p ~/.config/rclone
# Copy rclone.conf from 1Password/Bitwarden

# 4. Restore OpenClaw config
# Copy config.yaml from secure vault

# 5. Install dependencies
pip install -r ~/.openclaw/workspace/requirements.txt
```

### Option B: Sync Script

Run from local machine to push to cloud:
```powershell
# See scripts/sync-to-cloud.ps1
```

---

## 📁 Files to Add to Private Repo

These should be in the private deployment template:

```
openclaw-workspace/
├── AGENTS.md
├── SOUL.md
├── USER.md
├── IDENTITY.md
├── MEMORY.md
├── HEARTBEAT.md
├── DEVICE_TOOLS.md
├── DEPLOYMENT.md (this file)
├── automation/
│   ├── entity-profiles.json
│   ├── signup-templates.json
│   ├── mhi-critical-info.json
│   └── ...
├── skills/
│   ├── operational-substrate/
│   ├── advanced-search/
│   └── ...
├── scripts/
│   └── ...
├── memory/
│   └── *.md (daily logs)
└── .gitignore
```

---

## 🔐 Secrets Management

**DO NOT commit to git:**
- `config/accounts.json` (Zoho tokens)
- `rclone.conf` (OneDrive tokens)
- `config.yaml` (API keys)
- Any `.env` files

**Use instead:**
- 1Password/Bitwarden CLI for secrets
- GitHub Secrets for CI/CD
- Environment variables in cloud VM

---

## 🔄 Keeping In Sync

### From Local → Cloud
```powershell
cd ~/.openclaw/workspace
git add -A
git commit -m "Sync local changes"
git push origin master
```

### On Cloud VM
```bash
cd ~/.openclaw/workspace
git pull origin master
```

### Automated (via cron job on VM)
```bash
# Every hour, pull latest
0 * * * * cd ~/.openclaw/workspace && git pull origin master
```

---

## ✅ Verification Checklist

After deploying to cloud VM, verify:

- [ ] `openclaw status` shows healthy
- [ ] All agents listed: `openclaw agents list`
- [ ] Zoho API works: `python zoho-console-api-module-system/test_auth.py`
- [ ] rclone works: `rclone lsd onedrive:`
- [ ] Skills loaded: check `<available_skills>` in agent response
- [ ] Memory files present: `ls ~/.openclaw/workspace/memory/`
- [ ] Entity profiles loaded: `cat automation/entity-profiles.json`

---

*Last updated: 2026-02-08*
