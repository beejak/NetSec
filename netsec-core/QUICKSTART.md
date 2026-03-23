# NetSec-Core Quick Start Guide

## Installation

```bash
# Navigate to netsec-core directory
cd netsec-core

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

## Running the API Server

```bash
# Option 1: Using uvicorn directly
uvicorn netsec_core.api.main:app --reload

# Option 2: Using the run script
python run_api.py
```

The API will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/api/docs
- Health: http://localhost:8000/api/v1/health

## Using the CLI

```bash
# Check CLI is installed
netsec-core --help

# Check API health
netsec-core health

# Run tests (unit + API; exclude integration for speed)
pip install -e ".[dev]"
pytest -v -m "not integration"

# Try scanning commands
netsec-core scan ports example.com
netsec-core dns scan example.com
netsec-core ssl check example.com
```

## Running Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=netsec_core --cov-report=html

# Run specific test
pytest tests/test_api_health.py
```

## Project Status

✅ **Fully Implemented** — all core features in production:
- DNS Security Scanner (tunneling detection, spoofing detection, pattern analysis)
- SSL/TLS Monitor (certificate expiry, weak ciphers, chain validation)
- Network Scanner (TCP/UDP port scanning, service detection)
- Traffic Analyzer (flow capture, protocol analysis)
- Anomaly Detector (baseline learning, statistical detection)
- Asset Discovery (CIDR/range scanning, inventory generation)
- LLM Integration (traffic analysis, remediation suggestions, finding explanation)
- Remediation Guide (CIS/NIST-mapped guidance)

See [USAGE_GUIDE.md](USAGE_GUIDE.md) for detailed feature documentation.

## Development Workflow

1. Make changes to code
2. Run tests: `pytest`
3. Format code: `black src/ tests/`
4. Lint code: `ruff check src/ tests/`
5. Type check: `mypy src/`

## API Testing

```python
# Test health endpoint
import httpx
response = httpx.get("http://localhost:8000/api/v1/health")
print(response.json())
```
