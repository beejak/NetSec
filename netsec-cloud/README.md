# NetSec-Cloud ☁️

**Cloud Security Scanner** - Lightweight, API-first multi-cloud security scanning

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## Overview

NetSec-Cloud is a lightweight cloud security scanner designed to fill the gap for API-first, multi-cloud security scanning. Unlike heavy enterprise solutions, it focuses on:

- **Lightweight**: Minimal dependencies, fast execution
- **API-First**: REST API for all operations
- **Multi-Cloud**: AWS, Azure, GCP support
- **Tight Integration**: Works seamlessly with NetSec-Core

## Features

### Cloud Security Scanning
- **Storage Security**: S3, Azure Storage, GCP Cloud Storage
- **IAM Analysis**: AWS IAM, Azure RBAC, GCP IAM
- **Networking**: Security Groups, NSGs, Firewall Rules
- **Compute**: EC2, Azure VMs, GCP Compute Engine

### Security Checks
- Public access detection
- Encryption status
- Overprivileged access
- Misconfigured resources
- Compliance violations

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/your-org/netsec-cloud.git
cd netsec-cloud

# Install
pip install -r requirements.txt
pip install -e .

# For Azure support (optional)
pip install -e ".[azure]"

# For GCP support (optional)
pip install -e ".[gcp]"
```

### Usage

#### CLI

```bash
# Scan AWS
netsec-cloud scan aws --checks storage,iam

# Scan Azure
netsec-cloud scan azure --checks storage

# Scan GCP
netsec-cloud scan gcp --checks storage,networking
```

#### API

```bash
# Start API server
uvicorn netsec_cloud.api.main:app --reload

# Scan via API
curl -X POST "http://localhost:8000/api/v1/cloud/scan" \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "aws",
    "credentials": {},
    "check_types": ["storage", "iam"]
  }'
```

## Architecture

See [ARCHITECTURE_DESIGN.md](ARCHITECTURE_DESIGN.md) for detailed architecture documentation.

### Provider Abstraction

```
CloudProvider (Base)
    ├── AWSProvider
    ├── AzureProvider
    └── GCPProvider
```

### Unified Scanner

All providers use the same interface, making it easy to scan multiple clouds with the same code.

## Credentials

### AWS
```json
{
  "access_key_id": "AKIA...",
  "secret_access_key": "...",
  "region": "us-east-1"
}
```

Or use environment variables, IAM roles, or AWS profiles.

### Azure
```json
{
  "subscription_id": "...",
  "tenant_id": "...",
  "client_id": "...",
  "client_secret": "..."
}
```

Or use Managed Identity or Azure CLI credentials.

### GCP
```json
{
  "project_id": "...",
  "service_account_file": "/path/to/key.json"
}
```

Or use Application Default Credentials.

## Security Checks

### AWS
- S3 bucket public access
- S3 encryption status
- IAM users without MFA
- Overprivileged IAM policies
- Open security groups
- And more...

### Azure
- Storage account public access
- Storage encryption
- Open NSG rules
- RBAC policies
- And more...

### GCP
- Cloud Storage public access
- Firewall rules
- IAM bindings
- And more...

## API Endpoints

- `POST /api/v1/cloud/scan` - Scan single provider
- `POST /api/v1/cloud/scan/multi` - Scan multiple providers
- `GET /api/v1/cloud/providers` - List supported providers

See API docs at `/api/docs` when server is running.

## Status

🚧 **In Development** - Phase 1 (Foundation) in progress

- ✅ Architecture designed
- ✅ AWS provider (partial)
- ✅ Azure provider (partial)
- ✅ GCP provider (partial)
- ✅ Unified scanner
- ✅ API framework
- ⏳ Complete implementations
- ⏳ CLI commands
- ⏳ Testing
- ⏳ Documentation

## Integration with NetSec-Core

NetSec-Cloud can be used independently or integrated with NetSec-Core for unified security scanning.

## Dependencies

**Minimal:**
- boto3 (AWS)
- fastapi
- pydantic
- click

**Optional:**
- azure-* (for Azure)
- google-cloud-* (for GCP)

## Documentation

- [Architecture Design](ARCHITECTURE_DESIGN.md)
- [Implementation Plan](IMPLEMENTATION_PLAN.md)
- [API Documentation](http://localhost:8000/api/docs)

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Related Projects

- [NetSec-Core](../netsec-core/) - Network Security Foundation Toolkit
