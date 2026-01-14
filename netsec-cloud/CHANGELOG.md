# Changelog

All notable changes to NetSec-Cloud will be documented in this file.

## [0.1.0] - 2024-12-XX

### Added - Phase 1: Foundation

- **Architecture Design**
  - Provider abstraction layer
  - Unified scanner interface
  - Network architecture diagrams
  - Security architecture design

- **Base Implementation**
  - Base provider interface
  - Finding model
  - Unified scanner engine
  - Summary generation

- **AWS Provider** (Partial)
  - Authentication support
  - S3 bucket scanning (public access, encryption, versioning)
  - IAM scanning (MFA, overprivileged policies)
  - Security Groups scanning (open rules)
  - Region discovery

- **Azure Provider** (Partial)
  - Authentication support
  - Storage account scanning (public access, encryption)
  - NSG scanning (open rules)
  - Region support

- **GCP Provider** (Partial)
  - Authentication support
  - Cloud Storage scanning (public access, versioning)
  - Firewall scanning (open rules)
  - Region support

- **API Framework**
  - FastAPI application
  - Pydantic models
  - Scan endpoints
  - Health endpoint
  - Multi-cloud scan support

- **CLI Framework**
  - Click CLI interface
  - Scan command
  - Provider listing
  - Output formatting

- **Documentation**
  - Architecture design
  - Network architecture
  - Implementation plan
  - README

### Technical Details

- Python 3.10+ support
- Minimal dependencies (only official SDKs)
- boto3 for AWS
- Azure SDK (optional)
- GCP SDK (optional)
- FastAPI for API
- Click for CLI

### Known Limitations

- AWS provider: Partial implementation (S3, IAM, Security Groups)
- Azure provider: Partial implementation (Storage, NSG)
- GCP provider: Partial implementation (Storage, Firewall)
- Compute scanning: Not yet implemented
- Compliance checking: Not yet implemented
- Remediation: Not yet implemented

### Next Steps

- Complete AWS provider implementation
- Complete Azure provider implementation
- Complete GCP provider implementation
- Add compliance checking
- Add remediation system
- Integration with NetSec-Core
- Comprehensive testing
