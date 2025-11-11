# ==========================================================
# Dockerfile - FastAPI Application (Production Ready)
# Base image: Python 3.9 Slim
# ==========================================================

# Environment Image
FROM python:3.9-slim AS base

LABEL maintainer="user"
LABEL project="FastAPI Service"
LABEL description="Container for FastAPI application running on Uvicorn."

# Environment Configuration
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    DEBIAN_FRONTEND=noninteractive \
    TZ=Etc/UTC

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency files first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# (Optional) Ensure folders exist
RUN mkdir -p /app/storage /app/utils

# Expose port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD curl -f http://localhost:8000/health || exit 1

# Default command
CMD ["uvicorn", "server:app", "--host"]()
