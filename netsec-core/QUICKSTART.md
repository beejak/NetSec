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

# Try scanning commands (will show placeholder messages)
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

✅ **Week 1-2 Complete**: Foundation & API Framework
- Project structure
- FastAPI application
- CLI interface
- Testing framework
- API documentation

⏳ **Next Steps**: Week 3-4 - Core Scanning Features
- DNS Security Scanner
- SSL/TLS Monitor
- Network Scanner

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

## Next Implementation Phase

See `IMPLEMENTATION_PLANS/NETSEC_CORE_IMPLEMENTATION.md` for Week 3-4 tasks:
- DNS Security Scanner implementation
- SSL/TLS Monitor implementation
- Network Scanner implementation
