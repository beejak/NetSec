# NetSec-Core Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpcap-dev \
    tcpdump \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Install package
RUN pip install --no-cache-dir -e .

# Create non-root user for security
RUN useradd -m -u 1000 netsec && chown -R netsec:netsec /app
USER netsec

# Expose API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/api/v1/health', timeout=5)"

# Run API server
CMD ["uvicorn", "netsec_core.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
