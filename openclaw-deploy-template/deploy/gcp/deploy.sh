#!/usr/bin/env bash
# =============================================================================
# Deploy OpenClaw to Google Cloud Run
# =============================================================================
# Prerequisites:
#   - gcloud CLI installed and authenticated
#   - Docker installed (for local build) or use Cloud Build
#
# Usage:
#   export GCP_PROJECT_ID=my-project
#   ./deploy.sh
# =============================================================================

set -euo pipefail

# --- Configuration ---
PROJECT_ID="${GCP_PROJECT_ID:-$(gcloud config get-value project 2>/dev/null)}"
REGION="${GCP_REGION:-us-central1}"
SERVICE_NAME="openclaw-gateway"
IMAGE_NAME="gcr.io/$PROJECT_ID/openclaw-gateway"
IMAGE_TAG="${IMAGE_TAG:-latest}"

echo "🦞 Deploying OpenClaw to Google Cloud Run"
echo "=================================================="
echo "  Project: $PROJECT_ID"
echo "  Region:  $REGION"

# Load .env if exists
ENV_FILE="../../.env"
if [ -f "$ENV_FILE" ]; then
    set -a
    source "$ENV_FILE"
    set +a
    echo "  ✅ Loaded .env"
fi

# --- Validate ---
if [ -z "$PROJECT_ID" ]; then
    echo "❌ GCP_PROJECT_ID not set. Run: gcloud config set project <your-project>"
    exit 1
fi

for var in ANTHROPIC_API_KEY GATEWAY_TOKEN TELEGRAM_BOT_TOKEN TELEGRAM_ALLOWED_USER_ID; do
    if [ -z "${!var:-}" ]; then
        echo "❌ Missing required env var: $var"
        exit 1
    fi
done

# --- Enable APIs ---
echo ""
echo "📡 Enabling required APIs..."
gcloud services enable \
    run.googleapis.com \
    secretmanager.googleapis.com \
    artifactregistry.googleapis.com \
    --project "$PROJECT_ID" \
    --quiet

# --- Store secrets in Secret Manager ---
echo ""
echo "🔑 Storing secrets in Secret Manager..."

for secret_name in ANTHROPIC_API_KEY GATEWAY_TOKEN TELEGRAM_BOT_TOKEN; do
    secret_value="${!secret_name}"
    # Create or update secret
    if gcloud secrets describe "openclaw-$secret_name" --project "$PROJECT_ID" &>/dev/null; then
        echo "$secret_value" | gcloud secrets versions add "openclaw-$secret_name" \
            --data-file=- --project "$PROJECT_ID" --quiet
    else
        echo "$secret_value" | gcloud secrets create "openclaw-$secret_name" \
            --data-file=- --project "$PROJECT_ID" --quiet
    fi
    echo "  ✅ openclaw-$secret_name"
done

# --- Build and push image ---
echo ""
echo "🐳 Building image with Cloud Build..."
gcloud builds submit ../../ \
    --tag "$IMAGE_NAME:$IMAGE_TAG" \
    --project "$PROJECT_ID" \
    --quiet

echo "  ✅ Image pushed to $IMAGE_NAME:$IMAGE_TAG"

# --- Deploy to Cloud Run ---
echo ""
echo "🚀 Deploying to Cloud Run..."

gcloud run deploy "$SERVICE_NAME" \
    --image "$IMAGE_NAME:$IMAGE_TAG" \
    --platform managed \
    --region "$REGION" \
    --project "$PROJECT_ID" \
    --port 18790 \
    --memory 1Gi \
    --cpu 1 \
    --min-instances 1 \
    --max-instances 1 \
    --no-allow-unauthenticated \
    --set-secrets="ANTHROPIC_API_KEY=openclaw-ANTHROPIC_API_KEY:latest,GATEWAY_TOKEN=openclaw-GATEWAY_TOKEN:latest,TELEGRAM_BOT_TOKEN=openclaw-TELEGRAM_BOT_TOKEN:latest" \
    --set-env-vars="TELEGRAM_ALLOWED_USER_ID=$TELEGRAM_ALLOWED_USER_ID,OPENCLAW_HOME=/home/openclaw/.openclaw,NODE_ENV=production,ELEVENLABS_API_KEY=${ELEVENLABS_API_KEY:-},ELEVENLABS_VOICE_ID=${ELEVENLABS_VOICE_ID:-}" \
    --quiet

# --- Get URL ---
echo ""
SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" \
    --region "$REGION" \
    --project "$PROJECT_ID" \
    --format 'value(status.url)')

echo "✅ Deployment complete!"
echo ""
echo "Service URL: $SERVICE_URL"
echo ""
echo "View logs:   gcloud run services logs read $SERVICE_NAME --region $REGION --project $PROJECT_ID"
echo "Delete:      gcloud run services delete $SERVICE_NAME --region $REGION --project $PROJECT_ID"
