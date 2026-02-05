#!/usr/bin/env bash
# =============================================================================
# Deploy OpenClaw to AWS ECS Fargate
# =============================================================================
# Prerequisites:
#   - AWS CLI v2 installed and configured
#   - Docker image pushed to ECR
#
# Usage:
#   export AWS_REGION=us-east-1
#   export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
#   ./deploy.sh
# =============================================================================

set -euo pipefail

# --- Configuration ---
AWS_REGION="${AWS_REGION:-us-east-1}"
AWS_ACCOUNT_ID="${AWS_ACCOUNT_ID:-$(aws sts get-caller-identity --query Account --output text)}"
CLUSTER_NAME="${ECS_CLUSTER_NAME:-openclaw-cluster}"
SERVICE_NAME="openclaw-gateway"
TASK_FAMILY="openclaw-gateway"
ECR_REPO="${ECR_REPO_NAME:-openclaw-gateway}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
ECR_URI="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:$IMAGE_TAG"

echo "🦞 Deploying OpenClaw to AWS ECS Fargate"
echo "=================================================="
echo "  Region:  $AWS_REGION"
echo "  Account: $AWS_ACCOUNT_ID"
echo "  Cluster: $CLUSTER_NAME"

# Load .env if exists
ENV_FILE="../../.env"
if [ -f "$ENV_FILE" ]; then
    set -a
    source "$ENV_FILE"
    set +a
    echo "  ✅ Loaded .env"
fi

# --- Validate ---
for var in ANTHROPIC_API_KEY GATEWAY_TOKEN TELEGRAM_BOT_TOKEN TELEGRAM_ALLOWED_USER_ID; do
    if [ -z "${!var:-}" ]; then
        echo "❌ Missing required env var: $var"
        exit 1
    fi
done

# --- Create ECR Repository ---
echo ""
echo "📦 Creating ECR repository..."
aws ecr describe-repositories --repository-names "$ECR_REPO" --region "$AWS_REGION" 2>/dev/null \
    || aws ecr create-repository --repository-name "$ECR_REPO" --region "$AWS_REGION" --output table

# --- Build and Push ---
echo ""
echo "🐳 Building and pushing Docker image..."
aws ecr get-login-password --region "$AWS_REGION" | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

docker build -t "$ECR_REPO:$IMAGE_TAG" -f ../docker/Dockerfile ../../
docker tag "$ECR_REPO:$IMAGE_TAG" "$ECR_URI"
docker push "$ECR_URI"
echo "  ✅ Pushed to $ECR_URI"

# --- Store secrets in SSM Parameter Store ---
echo ""
echo "🔑 Storing secrets in SSM Parameter Store..."
for secret in ANTHROPIC_API_KEY GATEWAY_TOKEN TELEGRAM_BOT_TOKEN; do
    aws ssm put-parameter \
        --name "/openclaw/$secret" \
        --value "${!secret}" \
        --type SecureString \
        --overwrite \
        --region "$AWS_REGION" \
        --output none
    echo "  ✅ /openclaw/$secret"
done

# Non-secret params
aws ssm put-parameter \
    --name "/openclaw/TELEGRAM_ALLOWED_USER_ID" \
    --value "$TELEGRAM_ALLOWED_USER_ID" \
    --type String \
    --overwrite \
    --region "$AWS_REGION" \
    --output none

# --- Create ECS Cluster ---
echo ""
echo "🏗️  Creating ECS cluster: $CLUSTER_NAME..."
aws ecs describe-clusters --clusters "$CLUSTER_NAME" --region "$AWS_REGION" --query 'clusters[0].status' --output text 2>/dev/null | grep -q ACTIVE \
    || aws ecs create-cluster --cluster-name "$CLUSTER_NAME" --region "$AWS_REGION" --output table

# --- Create/Update Task Definition ---
echo ""
echo "📋 Registering task definition..."

# Substitute values in task definition
TASK_DEF=$(cat task-definition.json | \
    sed "s|\${AWS_ACCOUNT_ID}|$AWS_ACCOUNT_ID|g" | \
    sed "s|\${AWS_REGION}|$AWS_REGION|g" | \
    sed "s|\${ECR_URI}|$ECR_URI|g")

echo "$TASK_DEF" > /tmp/openclaw-task-def.json
TASK_ARN=$(aws ecs register-task-definition \
    --cli-input-json file:///tmp/openclaw-task-def.json \
    --region "$AWS_REGION" \
    --query 'taskDefinition.taskDefinitionArn' \
    --output text)
echo "  ✅ $TASK_ARN"
rm /tmp/openclaw-task-def.json

# --- Get default VPC and subnets ---
echo ""
echo "🌐 Finding VPC and subnets..."
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" --query 'Vpcs[0].VpcId' --output text --region "$AWS_REGION")
SUBNETS=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --query 'Subnets[*].SubnetId' --output text --region "$AWS_REGION" | tr '\t' ',')
echo "  VPC: $VPC_ID"
echo "  Subnets: $SUBNETS"

# --- Create/Update Service ---
echo ""
echo "🚀 Deploying service..."
if aws ecs describe-services --cluster "$CLUSTER_NAME" --services "$SERVICE_NAME" --region "$AWS_REGION" --query 'services[0].status' --output text 2>/dev/null | grep -q ACTIVE; then
    aws ecs update-service \
        --cluster "$CLUSTER_NAME" \
        --service "$SERVICE_NAME" \
        --task-definition "$TASK_ARN" \
        --force-new-deployment \
        --region "$AWS_REGION" \
        --output table
    echo "  ✅ Service updated"
else
    aws ecs create-service \
        --cluster "$CLUSTER_NAME" \
        --service-name "$SERVICE_NAME" \
        --task-definition "$TASK_ARN" \
        --desired-count 1 \
        --launch-type FARGATE \
        --network-configuration "awsvpcConfiguration={subnets=[$SUBNETS],assignPublicIp=ENABLED}" \
        --region "$AWS_REGION" \
        --output table
    echo "  ✅ Service created"
fi

echo ""
echo "✅ Deployment complete!"
echo ""
echo "View logs:   aws logs tail /ecs/openclaw-gateway --follow --region $AWS_REGION"
echo "Service:     aws ecs describe-services --cluster $CLUSTER_NAME --services $SERVICE_NAME --region $AWS_REGION"
echo "Stop:        aws ecs update-service --cluster $CLUSTER_NAME --service $SERVICE_NAME --desired-count 0 --region $AWS_REGION"
