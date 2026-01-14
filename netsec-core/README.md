# NetSec-Core 🛡️

[![CI](https://github.com/your-org/netsec-core/workflows/CI/badge.svg)](https://github.com/your-org/netsec-core/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**Network Security Foundation Toolkit** - A comprehensive network security toolkit providing network scanning, DNS security analysis, SSL/TLS monitoring, traffic analysis, and anomaly detection.

## Features

- **Network Scanning** - Port scanning, service detection, OS fingerprinting
- **DNS Security** - DNS tunneling detection, spoofing detection, query pattern analysis
- **SSL/TLS Monitoring** - Certificate expiration tracking, weak cipher detection, chain validation
- **Traffic Analysis** - Packet capture, protocol analysis, flow visualization
- **Anomaly Detection** - Statistical anomaly detection, real-time baseline learning

## Installation

### Prerequisites

- Python 3.10 or higher
- pip

### Quick Install

```bash
# Clone the repository
git clone https://github.com/your-org/netsec-core.git
cd netsec-core

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

### Docker Install

```bash
# Build Docker image
docker build -t netsec-core:latest .

# Run with Docker Compose
docker-compose up -d
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment options.

## Quick Start

### Using the CLI

```bash
# Check API health
netsec-core health

# Scan ports
netsec-core scan ports example.com

# Scan DNS security
netsec-core dns scan example.com

# Check SSL/TLS certificate
netsec-core ssl check example.com
```

### Using the API

Start the API server:

```bash
uvicorn netsec_core.api.main:app --reload
```

The API will be available at `http://localhost:8000`

- API Documentation: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc
- Health Check: http://localhost:8000/api/v1/health

### Example API Usage

```python
import httpx

# Health check
response = httpx.get("http://localhost:8000/api/v1/health")
print(response.json())

# Scan ports (when implemented)
response = httpx.post(
    "http://localhost:8000/api/v1/scan/ports",
    json={"target": "example.com", "ports": [80, 443]}
)
print(response.json())
```

## Project Structure

```
netsec-core/
├── src/
│   └── netsec_core/
│       ├── __init__.py
│       ├── api/              # FastAPI application
│       │   ├── main.py       # FastAPI app
│       │   ├── models.py     # Pydantic models
│       │   └── routes/       # API routes
│       └── cli/              # CLI interface
│           ├── main.py       # CLI entry point
│           └── commands/     # CLI commands
├── tests/                    # Test suite
├── docs/                     # Documentation
├── examples/                 # Usage examples
├── requirements.txt          # Dependencies
├── setup.py                  # Package setup
└── pyproject.toml            # Modern Python config
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=netsec_core --cov-report=html

# Run specific test file
pytest tests/test_api_health.py
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type checking
mypy src/
```

## Implementation Status

### ✅ Week 1-2: Foundation & API Framework (Complete)
- [x] Project structure
- [x] FastAPI application
- [x] API routes structure
- [x] Health check endpoint
- [x] API models (Pydantic)
- [x] Error handling
- [x] CLI interface (Click)
- [x] Testing framework (pytest)

### ✅ Week 3-4: Core Scanning Features (Complete)
- [x] DNS Security Scanner
  - [x] DNS query resolution
  - [x] DNS tunneling detection
  - [x] DNS spoofing detection
  - [x] Query pattern analysis
  - [x] Malicious domain indicators
- [x] SSL/TLS Monitor
  - [x] Certificate checking
  - [x] Expiration tracking
  - [x] Weak cipher detection
  - [x] Certificate chain validation
- [x] Network Scanner
  - [x] Port scanning (TCP/UDP)
  - [x] Service detection
  - [x] Banner grabbing

### ✅ Week 5-6: Advanced Features (Complete)
- [x] Traffic Analyzer
  - [x] Packet capture with scapy
  - [x] Protocol analysis (HTTP, DNS, TCP, UDP)
  - [x] Flow analysis
  - [x] Traffic statistics
- [x] Anomaly Detector
  - [x] Baseline learning
  - [x] Statistical anomaly detection (z-score)
  - [x] Pattern-based anomaly detection
  - [x] Real-time anomaly detection
- [x] Asset Discovery
  - [x] Network asset discovery
  - [x] Service identification
  - [x] Asset inventory generation

### ✅ Week 7-8: Integration & Enhancement (Complete)
- [x] LLM enhancements
  - [x] LLM analyzer framework
  - [x] Traffic analysis with LLM
  - [x] False positive reduction
  - [x] Remediation generation
  - [x] Natural language explanations
- [x] Remediation system
  - [x] Remediation database
  - [x] Remediation lookup
  - [x] Customized remediation guidance
  - [x] API and CLI integration
- [x] Documentation
  - [x] Comprehensive README
  - [x] Testing guide
  - [x] Quick start guide
  - [x] Changelog
- [x] Performance optimizations
  - [x] Concurrent scanning
  - [x] Efficient data structures

## API Endpoints

### Health
- `GET /api/v1/health` - Health check

### Network Scanner ✅
- `POST /api/v1/scan/ports` - Scan ports (Implemented)
- `POST /api/v1/scan/services` - Scan services (Implemented)
- `GET /api/v1/scan/results/{scan_id}` - Get scan results (Requires storage)

### DNS Security ✅
- `POST /api/v1/dns/scan` - Scan DNS security (Implemented)
- `GET /api/v1/dns/monitor` - Monitor DNS queries (Basic implementation)
- `POST /api/v1/dns/detect-tunneling` - Detect DNS tunneling (Implemented)
- `GET /api/v1/dns/anomalies` - Get DNS anomalies (Implemented)

### SSL/TLS ✅
- `POST /api/v1/ssl/check-certificate` - Check certificate (Implemented)
- `GET /api/v1/ssl/certificates` - List certificates (Basic implementation)
- `POST /api/v1/ssl/detect-weak-ciphers` - Detect weak ciphers (Implemented)
- `GET /api/v1/ssl/expiring-soon` - Get expiring certificates (Implemented)

### Traffic Analysis ✅
- `POST /api/v1/traffic/capture` - Capture traffic (Implemented)
- `GET /api/v1/traffic/stream` - Stream traffic (WebSocket - Requires implementation)
- `POST /api/v1/traffic/analyze` - Analyze traffic (Implemented)
- `GET /api/v1/traffic/flows` - Get network flows (Implemented)

### Anomaly Detection ✅
- `POST /api/v1/anomaly/learn-baseline` - Learn baseline (Implemented)
- `POST /api/v1/anomaly/detect` - Detect anomalies (Implemented)
- `GET /api/v1/anomaly/status` - Get anomaly status (Implemented)

### Asset Discovery ✅
- `POST /api/v1/assets/discover` - Discover assets (Implemented)
- `POST /api/v1/assets/inventory` - Generate inventory (Implemented)

### LLM Analysis ✅
- `POST /api/v1/llm/analyze-traffic` - Analyze traffic with LLM (Implemented)
- `POST /api/v1/llm/reduce-false-positives` - Reduce false positives (Implemented)
- `POST /api/v1/llm/generate-remediation` - Generate remediation (Implemented)
- `POST /api/v1/llm/explain-finding` - Explain finding (Implemented)

### Remediation ✅
- `GET /api/v1/remediation/{finding_type}` - Get remediation (Implemented)
- `POST /api/v1/remediation/` - Get remediation for finding (Implemented)
- `GET /api/v1/remediation/` - List all remediations (Implemented)
- `GET /api/v1/remediation/search/{keyword}` - Search remediations (Implemented)

## Deployment

NetSec-Core can be deployed in multiple ways:

- **Local Development**: See [QUICKSTART.md](QUICKSTART.md)
- **Docker**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Production**: See [DEPLOYMENT.md](DEPLOYMENT.md) for systemd, Kubernetes, and more

### Quick Docker Deployment

```bash
# Using Docker Compose
docker-compose up -d

# Or using Docker directly
docker run -d -p 8000:8000 netsec-core:latest
```

## Configuration

NetSec-Core can be configured via environment variables:

```bash
# API Configuration
export API_HOST=0.0.0.0
export API_PORT=8000

# LLM Configuration (Optional)
export OPENAI_API_KEY=your-key-here
# or
export ANTHROPIC_API_KEY=your-key-here

# Logging
export LOG_LEVEL=INFO
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for full configuration options.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

- 🐛 [Report a Bug](https://github.com/your-org/netsec-core/issues/new?template=bug_report.md)
- 💡 [Request a Feature](https://github.com/your-org/netsec-core/issues/new?template=feature_request.md)
- 📖 [View Documentation](HELP.md)
- 🧪 [Run Tests](TESTING_GUIDE.md)

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Links

- 📖 [Complete Help Guide](HELP.md)
- 🚀 [Quick Start](QUICKSTART.md)
- 🐳 [Deployment Guide](DEPLOYMENT.md)
- 🧪 [Testing Guide](TESTING_GUIDE.md)
- 🤝 [Contributing](CONTRIBUTING.md)
- 📝 [Changelog](CHANGELOG.md)

---

**Made with ❤️ for the security community**

## Acknowledgments

This project is part of the NetSec Toolkit suite, designed to fill gaps in the network security tool landscape.

## Roadmap

See [IMPLEMENTATION_PLANS/NETSEC_CORE_IMPLEMENTATION.md](../IMPLEMENTATION_PLANS/NETSEC_CORE_IMPLEMENTATION.md) for detailed implementation roadmap.
