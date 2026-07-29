# Builder stage
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev --no-install-project

# Final runtime stage
FROM python:3.13-slim-bookworm

WORKDIR /app

# Runtime environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

# Install only runtime dependencies
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    git \
    curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Run as non-root user for security
RUN groupadd -r botgroup && useradd -r -g botgroup botuser && \
    mkdir -p /app/downloads /app/cache && \
    chown -R botuser:botgroup /app

# Copy virtual environment from builder
COPY --from=builder --chown=botuser:botgroup /app/.venv /app/.venv

# Copy the rest of the application
COPY --chown=botuser:botgroup . .

USER botuser

# Healthcheck to verify the bot's web service is alive
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

CMD ["bash", "start"]

