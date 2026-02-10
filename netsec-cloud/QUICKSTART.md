# NetSec-Cloud Quick Start Guide

## Installation

```bash
# From the toolkit root, go to netsec-cloud
cd netsec-cloud

# Install core dependencies
pip install -r requirements.txt

# Install package
pip install -e .

# For Azure support (optional)
pip install -e ".[azure]"

# For GCP support (optional)
pip install -e ".[gcp]"
```

## Quick Start

### 1. Configure Credentials

#### AWS
```bash
# Option 1: Environment variables
export AWS_ACCESS_KEY_ID=your-key
export AWS_SECRET_ACCESS_KEY=your-secret

# Option 2: AWS CLI profile
aws configure

# Option 3: IAM role (if running on EC2)
```

#### Azure
```bash
# Option 1: Azure CLI
az login

# Option 2: Service principal
export AZURE_CLIENT_ID=...
export AZURE_CLIENT_SECRET=...
export AZURE_TENANT_ID=...
```

#### GCP
```bash
# Option 1: Application Default Credentials
gcloud auth application-default login

# Option 2: Service account key file
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
```

### 2. Run CLI Scan

```bash
# Scan AWS
netsec-cloud scan aws --checks storage,iam

# Scan Azure
netsec-cloud scan azure --checks storage

# Scan GCP
netsec-cloud scan gcp --checks storage,networking
```

### 3. Use API

```bash
# Start API server
uvicorn netsec_cloud.api.main:app --reload

# Scan via API
curl -X POST "http://localhost:8000/api/v1/cloud/scan" \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "aws",
    "credentials": {},
    "check_types": ["storage"]
  }'
```

## Examples

See [examples/basic_scan.py](examples/basic_scan.py) for code examples.

## Multi-cloud scan (API)

```bash
# POST /api/v1/cloud/scan/multi with providers and optional check_types
curl -X POST "http://localhost:8000/api/v1/cloud/scan/multi" \
  -H "Content-Type: application/json" \
  -d '{"providers": ["aws", "azure"], "check_types": ["storage", "iam"]}'
# Response: scan_id, results (per provider), summary, timestamp
```

## Documentation

- [README](README.md) - Overview
- [Architecture Design](ARCHITECTURE_DESIGN.md) - Architecture details
- [Network Architecture](NETWORK_ARCHITECTURE.md) - Network diagrams
- [Implementation Plan](IMPLEMENTATION_PLAN.md) - Development roadmap

## Status

Multi-cloud scan API, storage/IAM checks (including S3 encryption), and compliance mapping (CIS, NIST, PCI-DSS, HIPAA) are in place. CI enforces lint; tests cover API, providers, and compliance.
