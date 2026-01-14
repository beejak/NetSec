# Multi-stage Dockerfile for NetSec-Container
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements if they exist
COPY requirements.txt* ./
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir --user -r requirements.txt; fi

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Install Docker CLI for container scanning
RUN apt-get update && apt-get install -y \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY src/ ./src/
COPY setup.py pyproject.toml* ./

# Install application
RUN pip install --no-cache-dir -e .

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Expose API port
EXPOSE 8002

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8002/api/v1/health')" || exit 1

# Run API server
CMD ["uvicorn", "netsec_container.api.main:app", "--host", "0.0.0.0", "--port", "8002"]
