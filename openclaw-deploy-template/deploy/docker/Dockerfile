# =============================================================================
# OpenClaw Multi-Agent Gateway — Docker Image
# =============================================================================
# Build:  docker build -t openclaw-gateway .
# Run:    docker run --env-file .env openclaw-gateway
# =============================================================================

FROM node:24-slim AS base

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install OpenClaw globally
RUN npm install -g openclaw@latest

# Create non-root user
RUN groupadd -r openclaw && useradd -r -g openclaw -m -d /home/openclaw openclaw

# Set up OpenClaw home
ENV OPENCLAW_HOME=/home/openclaw/.openclaw
RUN mkdir -p $OPENCLAW_HOME

# Copy configuration
COPY openclaw.json $OPENCLAW_HOME/openclaw.json

# Copy workspace files
COPY workspace/ $OPENCLAW_HOME/workspace/

# Copy agent workspaces
COPY agents/ $OPENCLAW_HOME/agents/

# Create required directories
RUN mkdir -p $OPENCLAW_HOME/workspace/memory \
    && for agent in ops webdev cosmo social course pearsonvue ggleap asm \
       metaquest neteng roblox cicd testcov seeker sitecraft skillsmith \
       ballistics climbibm analyst; do \
       mkdir -p $OPENCLAW_HOME/agents/$agent/memory \
       $OPENCLAW_HOME/agents/$agent/sessions; \
    done

# Fix ownership
RUN chown -R openclaw:openclaw /home/openclaw

# Switch to non-root user
USER openclaw
WORKDIR /home/openclaw

# Gateway port
EXPOSE 18790

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:18790/health || exit 1

# Start the gateway
CMD ["openclaw", "gateway", "start", "--foreground"]
