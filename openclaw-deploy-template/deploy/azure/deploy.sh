#!/usr/bin/env bash
# =============================================================================
# Deploy OpenClaw to Azure Container Instances
# =============================================================================
# Prerequisites:
#   - Azure CLI (az) installed and logged in
#   - Docker image pushed to a container registry (ACR or Docker Hub)
#
# Usage:
#   export AZURE_SUBSCRIPTION_ID=...
#   export AZURE_RESOURCE_GROUP=openclaw-rg
#   ./deploy.sh
# =============================================================================

set -euo pipefail

# --- Configuration ---
RESOURCE_GROUP="${AZURE_RESOURCE_GROUP:-openclaw-rg}"
LOCATION="${AZURE_LOCATION:-eastus}"
CONTAINER_NAME="openclaw-gateway"
IMAGE="${DOCKER_IMAGE:-openclaw-gateway:latest}"
ACR_NAME="${AZURE_ACR_NAME:-}"
CPU="1"
MEMORY="1"

echo "🦞 Deploying OpenClaw to Azure Container Instances"
echo "=================================================="

# --- Validate ---
if ! command -v az &>/dev/null; then
    echo "❌ Azure CLI not found. Install from https://aka.ms/install-azure-cli"
    exit 1
fi

# Load .env if exists
ENV_FILE="../../.env"
if [ -f "$ENV_FILE" ]; then
    set -a
    source "$ENV_FILE"
    set +a
    echo "  ✅ Loaded .env"
fi

# Required env vars
for var in ANTHROPIC_API_KEY GATEWAY_TOKEN TELEGRAM_BOT_TOKEN TELEGRAM_ALLOWED_USER_ID; do
    if [ -z "${!var:-}" ]; then
        echo "❌ Missing required env var: $var"
        exit 1
    fi
done

# --- Create Resource Group ---
echo ""
echo "📁 Creating resource group: $RESOURCE_GROUP in $LOCATION..."
az group create --name "$RESOURCE_GROUP" --location "$LOCATION" --output none

# --- Build and push (if ACR) ---
if [ -n "$ACR_NAME" ]; then
    echo ""
    echo "🐳 Building and pushing to ACR: $ACR_NAME..."
    az acr build --registry "$ACR_NAME" --image "$IMAGE" ../../
    IMAGE="$ACR_NAME.azurecr.io/$IMAGE"
fi

# --- Deploy Container Instance ---
echo ""
echo "🚀 Deploying container instance..."

az container create \
    --resource-group "$RESOURCE_GROUP" \
    --name "$CONTAINER_NAME" \
    --image "$IMAGE" \
    --cpu "$CPU" \
    --memory "$MEMORY" \
    --ports 18790 \
    --restart-policy Always \
    --environment-variables \
        ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" \
        GATEWAY_TOKEN="$GATEWAY_TOKEN" \
        TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN" \
        TELEGRAM_ALLOWED_USER_ID="$TELEGRAM_ALLOWED_USER_ID" \
        ELEVENLABS_API_KEY="${ELEVENLABS_API_KEY:-}" \
        ELEVENLABS_VOICE_ID="${ELEVENLABS_VOICE_ID:-}" \
        OPENCLAW_HOME="/home/openclaw/.openclaw" \
        NODE_ENV="production" \
    --output table

# --- Get status ---
echo ""
echo "📊 Container status:"
az container show \
    --resource-group "$RESOURCE_GROUP" \
    --name "$CONTAINER_NAME" \
    --query "{Status:instanceView.state, IP:ipAddress.ip, FQDN:ipAddress.fqdn}" \
    --output table

echo ""
echo "✅ Deployment complete!"
echo ""
echo "View logs: az container logs -g $RESOURCE_GROUP -n $CONTAINER_NAME --follow"
echo "Delete:    az container delete -g $RESOURCE_GROUP -n $CONTAINER_NAME -y"
