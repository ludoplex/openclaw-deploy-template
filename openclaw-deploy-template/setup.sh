#!/usr/bin/env bash
# setup.sh — OpenClaw Deploy Template Setup (Linux/Mac)
# Usage: chmod +x setup.sh && ./setup.sh
#
# Reads .env file and substitutes ${VAR} placeholders in openclaw.json
# with actual values. Also sets up the directory structure.

set -euo pipefail

ENV_FILE="${1:-.env}"
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"

echo ""
echo "🦞 OpenClaw Deploy Template Setup"
echo "=================================================="

# --- Check prerequisites ---
echo ""
echo "📋 Checking prerequisites..."

if ! command -v node &>/dev/null; then
    echo "  ❌ Node.js not found. Install from https://nodejs.org (v20+)"
    exit 1
fi
echo "  ✅ Node.js $(node --version)"

if ! npm list -g --depth=0 2>/dev/null | grep -q openclaw; then
    echo "  ⚠️  OpenClaw not found globally. Install with: npm install -g openclaw"
else
    echo "  ✅ OpenClaw installed"
fi

# --- Load .env ---
echo ""
echo "📄 Loading environment from $ENV_FILE..."

if [ ! -f "$ENV_FILE" ]; then
    echo "  ❌ $ENV_FILE not found. Copy .env.example to .env and fill in your values."
    exit 1
fi

declare -A ENV_VARS
while IFS= read -r line; do
    line=$(echo "$line" | xargs)  # trim
    [[ -z "$line" || "$line" == \#* ]] && continue
    key="${line%%=*}"
    value="${line#*=}"
    ENV_VARS["$key"]="$value"
done < "$ENV_FILE"

# Override OPENCLAW_HOME if set in .env
if [[ -n "${ENV_VARS[OPENCLAW_HOME]:-}" ]]; then
    OPENCLAW_HOME="${ENV_VARS[OPENCLAW_HOME]}"
fi
ENV_VARS[OPENCLAW_HOME]="$OPENCLAW_HOME"

echo "  Loaded ${#ENV_VARS[@]} variables"
echo "  OpenClaw Home: $OPENCLAW_HOME"

# --- Validate required vars ---
REQUIRED=("ANTHROPIC_API_KEY" "GATEWAY_TOKEN" "TELEGRAM_BOT_TOKEN" "TELEGRAM_ALLOWED_USER_ID")
MISSING=()
for key in "${REQUIRED[@]}"; do
    val="${ENV_VARS[$key]:-}"
    if [[ -z "$val" || "$val" == "sk-ant-..."* || "$val" == "your-"* || "$val" == "123"* ]]; then
        MISSING+=("$key")
    fi
done

if [ ${#MISSING[@]} -gt 0 ]; then
    echo ""
    echo "⚠️  Missing or placeholder values for:"
    for m in "${MISSING[@]}"; do
        echo "    - $m"
    done
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    [[ ! $REPLY =~ ^[Yy]$ ]] && exit 1
fi

# --- Create directory structure ---
echo ""
echo "📁 Creating directory structure at $OPENCLAW_HOME..."

mkdir -p "$OPENCLAW_HOME/workspace/patterns"
mkdir -p "$OPENCLAW_HOME/workspace/scripts"
mkdir -p "$OPENCLAW_HOME/workspace/hooks/workflow-enforcer"
mkdir -p "$OPENCLAW_HOME/workspace/memory"

AGENTS=(ops webdev cosmo social course pearsonvue ggleap asm
        metaquest neteng roblox cicd testcov seeker sitecraft
        skillsmith ballistics climbibm analyst)

for agent in "${AGENTS[@]}"; do
    mkdir -p "$OPENCLAW_HOME/agents/$agent/memory"
    mkdir -p "$OPENCLAW_HOME/agents/$agent/sessions"
done

# --- Copy and substitute openclaw.json ---
echo ""
echo "⚙️  Generating openclaw.json..."

CONFIG=$(cat openclaw.json)

for key in "${!ENV_VARS[@]}"; do
    val="${ENV_VARS[$key]}"
    # Escape special sed characters in value
    escaped_val=$(printf '%s\n' "$val" | sed -e 's/[\/&]/\\&/g')
    CONFIG=$(echo "$CONFIG" | sed "s|\${$key}|$escaped_val|g")
done

echo "$CONFIG" > "$OPENCLAW_HOME/openclaw.json"
echo "  ✅ Written to $OPENCLAW_HOME/openclaw.json"

# --- Copy workspace files ---
echo ""
echo "📝 Copying workspace files..."

WORKSPACE_FILES=(
    "workspace/AGENTS.md"
    "workspace/SOUL.md"
    "workspace/USER.md"
    "workspace/IDENTITY.md"
    "workspace/HEARTBEAT.md"
    "workspace/BOOTSTRAP.md"
    "workspace/MEMORY.md"
    "workspace/WORKFLOW.md"
    "workspace/TOOLS.md"
    "workspace/patterns/RECURSIVE_REASONING.md"
    "workspace/scripts/backup.ps1"
    "workspace/scripts/task-router.ps1"
    "workspace/scripts/should-use-claude.ps1"
    "workspace/hooks/workflow-enforcer/handler.js"
    "workspace/hooks/workflow-enforcer/handler.ts"
    "workspace/hooks/workflow-enforcer/HOOK.md"
)

for f in "${WORKSPACE_FILES[@]}"; do
    if [ -f "$f" ]; then
        dst="$OPENCLAW_HOME/$f"
        mkdir -p "$(dirname "$dst")"
        cp "$f" "$dst"
    fi
done
echo "  ✅ Workspace files copied"

# --- Copy agent files ---
echo ""
echo "🤖 Copying agent workspaces..."

for agent_dir in agents/*/; do
    agent_name=$(basename "$agent_dir")
    target_dir="$OPENCLAW_HOME/agents/$agent_name"
    mkdir -p "$target_dir"

    # Copy root .md files
    for md in "$agent_dir"*.md; do
        [ -f "$md" ] && cp "$md" "$target_dir/"
    done

    # Copy skills
    if [ -d "$agent_dir/skills" ]; then
        cp -r "$agent_dir/skills" "$target_dir/"
    fi

    # Copy references and templates (skillsmith)
    for sub in references templates; do
        if [ -d "$agent_dir/$sub" ]; then
            cp -r "$agent_dir/$sub" "$target_dir/"
        fi
    done
done
echo "  ✅ Agent workspaces copied"

# --- Set ANTHROPIC_API_KEY ---
echo ""
echo "🔑 Setting ANTHROPIC_API_KEY..."
if [[ -n "${ENV_VARS[ANTHROPIC_API_KEY]:-}" ]]; then
    export ANTHROPIC_API_KEY="${ENV_VARS[ANTHROPIC_API_KEY]}"
    echo "  ✅ Set for current shell"
    echo ""
    echo "  To persist, add to your shell profile:"
    echo "    echo 'export ANTHROPIC_API_KEY=\"${ENV_VARS[ANTHROPIC_API_KEY]}\"' >> ~/.bashrc"
fi

# --- Done ---
echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Export ANTHROPIC_API_KEY in your shell profile"
echo "  2. Start the gateway: openclaw gateway start"
echo "  3. Send a message to your Telegram bot"
echo ""
echo "For cloud deployment, see deploy/ directory."
