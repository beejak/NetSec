# NetSec-Cloud: Architecture Design

## Design Goals

1. **Lightweight**: Minimal dependencies, fast execution
2. **Unified**: Same interface for all cloud providers
3. **Extensible**: Easy to add new checks
4. **Integration**: Seamless with NetSec-Core
5. **Quality**: Well-tested, production-ready

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│            NetSec-Cloud System                  │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────┐  ┌──────────────┐            │
│  │   API Layer  │  │   CLI Layer  │            │
│  │  (FastAPI)   │  │   (Click)    │            │
│  └──────┬───────┘  └──────┬───────┘            │
│         │                 │                    │
│         └────────┬────────┘                    │
│                  │                             │
│         ┌────────▼────────┐                    │
│         │  Scanner Engine │                    │
│         │  (Unified)      │                    │
│         └────────┬────────┘                    │
│                  │                             │
│    ┌─────────────┼─────────────┐               │
│    │             │             │               │
│ ┌──▼──┐      ┌──▼──┐      ┌──▼──┐            │
│ │ AWS │      │Azure│      │ GCP │            │
│ │ SDK │      │ SDK │      │ SDK │            │
│ └─────┘      └─────┘      └─────┘            │
│                                                 │
│  ┌──────────────┐  ┌──────────────┐           │
│  │  Findings    │  │  Remediation │           │
│  │  Engine      │  │  System      │           │
│  └──────────────┘  └──────────────┘           │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Component Design

### 1. Provider Abstraction Layer

```python
# Unified interface for all providers
class CloudProvider(ABC):
    @abstractmethod
    def scan_storage(self, region: str) -> List[Finding]:
        pass
    
    @abstractmethod
    def scan_iam(self, region: str) -> List[Finding]:
        pass
    
    @abstractmethod
    def scan_networking(self, region: str) -> List[Finding]:
        pass

# Provider implementations
class AWSProvider(CloudProvider):
    def __init__(self, credentials):
        self.client = boto3.client(...)
    
class AzureProvider(CloudProvider):
    def __init__(self, credentials):
        self.client = AzureManagementClient(...)
    
class GCPProvider(CloudProvider):
    def __init__(self, credentials):
        self.client = google.cloud.resource_manager(...)
```

### 2. Security Check Engine

```python
# Check registry
class SecurityCheck(ABC):
    @abstractmethod
    def check(self, provider: CloudProvider) -> List[Finding]:
        pass

# Common checks
class S3PublicAccessCheck(SecurityCheck):
    def check(self, provider: CloudProvider) -> List[Finding]:
        # Check S3 buckets for public access
        pass

class IAMOverprivilegedCheck(SecurityCheck):
    def check(self, provider: CloudProvider) -> List[Finding]:
        # Check IAM policies for overprivileged access
        pass
```

### 3. Unified Scanner

```python
class CloudScanner:
    def __init__(self, provider: CloudProvider):
        self.provider = provider
        self.checks = self._load_checks()
    
    def scan(self, regions: List[str], check_types: List[str]):
        findings = []
        for region in regions:
            for check_type in check_types:
                check = self.checks[check_type]
                findings.extend(check.check(self.provider))
        return findings
```

## Data Flow

```
User Request
    │
    ▼
┌─────────────┐
│  API/CLI    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Scanner    │
│  Engine     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Provider   │
│  (AWS/Azure/GCP)│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Cloud API  │
│  Calls      │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Findings   │
│  Aggregation│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Response   │
└─────────────┘
```

## Security Checks (Planned)

### AWS Checks
- S3 bucket public access
- S3 bucket encryption
- IAM policy analysis
- Security group rules
- VPC configuration
- CloudTrail logging
- Config compliance

### Azure Checks
- Storage account security
- NSG rules
- Key Vault access
- RBAC policies
- Network security
- Activity log monitoring

### GCP Checks
- Cloud Storage security
- IAM bindings
- Firewall rules
- VPC configuration
- Cloud Asset inventory
- Security Command Center

## Credential Management

```python
# Secure credential handling
class CredentialManager:
    def get_aws_credentials(self) -> dict:
        # From environment, file, or secrets manager
        pass
    
    def get_azure_credentials(self) -> dict:
        pass
    
    def get_gcp_credentials(self) -> dict:
        pass
```

## Integration with NetSec-Core

```python
# Shared models
from netsec_core.api.models import Finding, Severity

# Shared remediation
from netsec_core.remediation.guide import RemediationGuide

# Unified API
# NetSec-Core can call NetSec-Cloud endpoints
# Or NetSec-Cloud can be a module in NetSec-Core
```

## Implementation Phases

### Phase 1: AWS Foundation
- Basic AWS SDK integration
- S3 security scanning
- IAM policy analysis
- Simple API endpoints

### Phase 2: Multi-Cloud
- Azure integration
- GCP integration
- Unified interface
- Common checks

### Phase 3: Advanced
- Compliance automation
- Governance
- Risk assessment
- Remediation

### Phase 4: Integration
- NetSec-Core integration
- LLM enhancements
- Complete testing
- Documentation

## File Structure (Planned)

```
netsec-cloud/
├── src/
│   └── netsec_cloud/
│       ├── __init__.py
│       ├── api/
│       │   ├── main.py
│       │   ├── models.py
│       │   └── routes/
│       ├── providers/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── aws.py
│       │   ├── azure.py
│       │   └── gcp.py
│       ├── checks/
│       │   ├── __init__.py
│       │   ├── storage.py
│       │   ├── iam.py
│       │   └── networking.py
│       ├── scanner.py
│       └── cli/
│           └── main.py
├── tests/
├── docs/
└── requirements.txt
```

## Dependencies Strategy

**Minimal Dependencies:**
- Only official cloud SDKs
- No heavy frameworks
- Optional dependencies for advanced features

```python
# requirements.txt
boto3>=1.28.0
azure-identity>=1.15.0
azure-mgmt-resource>=23.0.0
google-cloud-resource-manager>=1.10.0
google-cloud-storage>=2.10.0

# Optional
azure-mgmt-security>=5.0.0  # For security center
```

## Testing Strategy

- Unit tests for each provider
- Integration tests with cloud APIs (mocked)
- End-to-end tests with test accounts
- Compliance with cloud provider best practices

## Security Considerations

- Secure credential storage
- Least privilege access
- Audit logging
- Rate limiting
- Error handling (no credential leaks)

## Performance Targets

- Scan 100 resources: < 30 seconds
- Memory usage: < 200MB
- API response time: < 5 seconds
- Concurrent scans: Support 10+ parallel

## Next Steps

1. ✅ Architecture design (this document)
2. ⏳ Implement AWS provider
3. ⏳ Create unified scanner interface
4. ⏳ Add Azure support
5. ⏳ Add GCP support
6. ⏳ Integration with NetSec-Core
