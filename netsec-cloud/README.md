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
- **IAM Analysis**: AWS IAM (MFA, overprivileged policies), **Azure RBAC** (subscription-level broad roles, SP Owner), **GCP IAM** (project Owner/Editor for users, SA Owner)
- **Networking**: Security Groups, NSGs, Firewall Rules
- **Compute**: EC2 (IMDSv2, public IP, EBS encryption); Azure/GCP compute planned

### Security Checks
- Public access detection
- Encryption status
- Overprivileged access
- Misconfigured resources
- Compliance violations

### Compliance (CIS & NIST)
- **CIS Benchmarks**: Map scan findings to CIS control IDs (storage, IAM, networking, compute).
- **NIST CSF**: Map findings to NIST subcategories (e.g. PR.AC-5, PR.DS-1).
- **POST /api/v1/cloud/compliance/check**: Run a scan and get control-level pass/fail for a framework.
- **GET /api/v1/cloud/compliance/frameworks/{framework}/controls**: List known controls for CIS or NIST.

### Compute (AWS EC2)
- **EC2**: IMDSv2 requirement, public IP exposure, EBS volume encryption.
- **scan_compute** runs EC2 and EBS checks when scanning AWS.

### Audit (AWS CloudTrail)
- **check_types** can include **`audit`** (AWS only). When present, **scan_audit_logging** runs: checks that at least one CloudTrail trail exists and that at least one has logging enabled. Mapped to CIS 3.x, NIST DE.CM-1, PCI-DSS 10.2, HIPAA Audit Controls.

## Quick Start

### Installation

```bash
# From the toolkit root, go to netsec-cloud
cd netsec-cloud

# Install
pip install -r requirements.txt
pip install -e .

# For Azure support (optional)
pip install -e ".[azure]"

# For GCP support (optional; includes IAM via google-api-python-client)
pip install -e ".[gcp]"
```

Azure RBAC scanning and GCP IAM scanning require the optional `[azure]` and `[gcp]` extras (which add `azure-mgmt-authorization` and `google-api-python-client` respectively).

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

- **API overview:** See root [API_REFERENCE.md](../API_REFERENCE.md) for endpoints and OpenAPI links.

```bash
# Start API server
uvicorn netsec_cloud.api.main:app --reload

# Scan via API
curl -X POST "http://localhost:8000/api/v1/cloud/scan" \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "aws",
    "credentials": {},
    "check_types": ["storage", "iam", "networking", "compute"]
  }'

# Compliance check (CIS or NIST)
curl -X POST "http://localhost:8000/api/v1/cloud/compliance/check" \
  -H "Content-Type: application/json" \
  -d '{"provider": "aws", "framework": "cis", "credentials": {}}'
```

## Architecture

See [ARCHITECTURE_DESIGN.md](ARCHITECTURE_DESIGN.md) for detailed architecture documentation.

## Testing

Tests use **pytest** with shared fixtures in `tests/conftest.py` (`client` for API, `scanner` for CloudScanner). Install dev deps and run:

```bash
pip install -e ".[dev]"
pytest -v
pytest -m api -v          # API tests only
pytest --cov=netsec_cloud --cov-report=term-missing   # with coverage
```

Compliance check now supports **CIS**, **NIST**, **PCI-DSS**, and **HIPAA** (finding-to-control mapping). See the repo root [TESTING.md](../TESTING.md) and [RUN_ALL_TESTS.md](../RUN_ALL_TESTS.md) for the full testing framework.

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
