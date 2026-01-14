# NetSec-Core 🛡️

[![CI](https://github.com/your-org/netsec-core/workflows/CI/badge.svg)](https://github.com/your-org/netsec-core/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**Network Security Foundation Toolkit** - A comprehensive network security toolkit providing network scanning, DNS security analysis, SSL/TLS monitoring, traffic analysis, and anomaly detection.

## ✨ Features

- 🔍 **Network Scanning** - Port scanning, service detection, OS fingerprinting
- 🌐 **DNS Security** - DNS tunneling detection, spoofing detection, query pattern analysis
- 🔒 **SSL/TLS Monitoring** - Certificate expiration tracking, weak cipher detection, chain validation
- 📊 **Traffic Analysis** - Packet capture, protocol analysis, flow visualization
- 🚨 **Anomaly Detection** - Statistical anomaly detection, real-time baseline learning
- 🏗️ **Asset Discovery** - Network asset identification and inventory
- 🤖 **LLM Integration** - AI-powered analysis and remediation
- 📋 **Remediation System** - Comprehensive security guidance

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/your-org/netsec-core.git
cd netsec-core

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install
pip install -r requirements.txt
pip install -e .
```

### Docker

```bash
docker-compose up -d
```

### Usage

```bash
# CLI
netsec-core dns scan example.com
netsec-core ssl check example.com
netsec-core scan ports 127.0.0.1

# API
curl http://localhost:8000/api/v1/health
```

## 📚 Documentation

- [README](README.md) - Complete documentation
- [Quick Start](QUICKSTART.md) - Get started quickly
- [Deployment Guide](DEPLOYMENT.md) - Production deployment
- [Testing Guide](TESTING_GUIDE.md) - Testing instructions
- [Help Guide](HELP.md) - Complete command reference
- [Contributing](CONTRIBUTING.md) - Contribution guidelines

## 🛠️ API

Interactive API documentation available at `/api/docs` when server is running.

**Base URL:** `http://localhost:8000`

**Key Endpoints:**
- `GET /api/v1/health` - Health check
- `POST /api/v1/dns/scan` - DNS security scan
- `POST /api/v1/ssl/check-certificate` - SSL/TLS check
- `POST /api/v1/scan/ports` - Port scanning
- `GET /api/v1/remediation/{finding_type}` - Get remediation

## 🧪 Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=netsec_core --cov-report=html

# Quick test
python test_quick.py
```

## 📦 Requirements

- Python 3.10+
- See [requirements.txt](requirements.txt) for dependencies

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built as part of the NetSec Toolkit suite to fill gaps in the network security tool landscape.

## 🔗 Links

- [Documentation](README.md)
- [Issue Tracker](https://github.com/your-org/netsec-core/issues)
- [Changelog](CHANGELOG.md)

---

**Made with ❤️ for the security community**
