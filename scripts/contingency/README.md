# OpenClaw Crash Recovery Contingency Plan

## Overview
If OpenClaw (Peridot) crashes, Claude Code Desktop can be prompted to restore it.

## Components

### 1. Monitor Script
`monitor-openclaw.ps1` - Checks if OpenClaw gateway is running

### 2. Recovery Script  
`restart-openclaw.ps1` - Restarts the OpenClaw gateway

### 3. Claude Code Prompt Template
`recovery-prompt.md` - Paste this into Claude Code to trigger recovery

## How It Works

1. **Detection:** Monitor script checks gateway health every 5 minutes
2. **Alert:** If gateway down, creates `OPENCLAW_DOWN.flag` file
3. **Recovery:** User opens Claude Code, pastes recovery prompt
4. **Restoration:** Claude Code runs restart script

## Manual Recovery

If you notice Peridot is unresponsive:

1. Open Claude Code Desktop
2. Paste contents of `recovery-prompt.md`
3. Claude Code will restart the gateway

## Paths

- OpenClaw binary: `/home/user/.openclaw/openclaw-2026.2.2/openclaw`
- Gateway config: `/home/user/.openclaw/openclaw.json`
- Claude Code: `C:\Users\user\AppData\Local\AnthropicClaude\app-1.1.2512\claude.exe`
