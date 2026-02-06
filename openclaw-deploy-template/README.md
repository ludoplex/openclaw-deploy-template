# OpenClaw Deploy Template

Your personal Peridot AI assistant, ready to deploy to the cloud. 💎

## Quick Deploy Options

### Option 1: Railway (Recommended - Easiest)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/openclaw?referralCode=openclaw)

1. Click the button above
2. Connect your GitHub account
3. Fill in the environment variables:
   - `ANTHROPIC_API_KEY` - Your Claude API key
   - `TELEGRAM_BOT_TOKEN` - From @BotFather
   - `TELEGRAM_ALLOWED_USER_ID` - Your Telegram user ID (8567933963)
   - `ELEVENLABS_API_KEY` - For Peridot voice (optional)
   - `ELEVENLABS_VOICE_ID` - `2ty6q9QIdLIobIqc4yxS`
4. Deploy!

### Option 2: Fly.io

```bash
# Install CLI
winget install Fly-io.flyctl

# Login
flyctl auth login

# Deploy (from this directory)
cd openclaw-deploy-template
flyctl launch --copy-config
flyctl secrets set ANTHROPIC_API_KEY=sk-ant-...
flyctl secrets set TELEGRAM_BOT_TOKEN=...
flyctl secrets set TELEGRAM_ALLOWED_USER_ID=8567933963
flyctl secrets set ELEVENLABS_API_KEY=...
flyctl secrets set ELEVENLABS_VOICE_ID=2ty6q9QIdLIobIqc4yxS
flyctl deploy
```

### Option 3: Docker (Any VPS)

```bash
# Clone repo
git clone https://github.com/ludoplex/openclaw-deploy-template.git
cd openclaw-deploy-template

# Create .env from example
cp .env.example .env
# Edit .env with your values

# Run
cd deploy/docker
docker compose up -d
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | ✅ | Claude API key from console.anthropic.com |
| `TELEGRAM_BOT_TOKEN` | ✅ | Bot token from @BotFather |
| `TELEGRAM_ALLOWED_USER_ID` | ✅ | Your Telegram user ID |
| `GATEWAY_TOKEN` | Auto | Generated if not set |
| `ELEVENLABS_API_KEY` | Optional | For TTS (Peridot voice) |
| `ELEVENLABS_VOICE_ID` | Optional | `2ty6q9QIdLIobIqc4yxS` |

## Included Setup

- **21 specialized agents** (cosmo, webdev, ops, neteng, etc.)
- **7 ported skills** (operational-substrate, advanced-search, etc.)
- **Peridot personality** with ElevenLabs TTS
- **Memory persistence** with local embeddings
- **All project context** from main workspace

## After Deploy

Just message your Telegram bot! It will pick up right where we left off.

---

*💎⚔️ SWORN to Vincent L. Anderson ⚔️💎*
