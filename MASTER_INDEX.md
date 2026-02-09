# Master Index - NetSec Toolkit Projects
## Complete Documentation Index

This document serves as the master index for all NetSec Toolkit projects and documentation.

---

## 📚 Documentation Index

### Research & Analysis
- [RESEARCH_REPORT.md](RESEARCH_REPORT.md) - Network security research findings
- [CLOUD_SECURITY_RESEARCH.md](CLOUD_SECURITY_RESEARCH.md) - Cloud security research
- [CONTAINER_SECURITY_RESEARCH.md](CONTAINER_SECURITY_RESEARCH.md) - Container security research
- [RESEARCH_REVIEW.md](RESEARCH_REVIEW.md) - Comprehensive research review
- [GAP_ANALYSIS.md](GAP_ANALYSIS.md) - Gap analysis and opportunities

### Enterprise & Operations
- [API_REFERENCE.md](API_REFERENCE.md) - API overview and OpenAPI docs
- [SECURITY_AND_COMPLIANCE.md](SECURITY_AND_COMPLIANCE.md) - What we check; CIS/NIST/PCI-DSS/HIPAA
- [ARCHITECTURE.md](ARCHITECTURE.md) - High-level architecture
- [RUNBOOK.md](RUNBOOK.md) - Deploy, config, health, logs, troubleshooting
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [ENTERPRISE_DOCUMENTATION.md](ENTERPRISE_DOCUMENTATION.md) - Enterprise doc checklist
- [MID_PROJECT_EVALUATION.md](MID_PROJECT_EVALUATION.md) - Mid-project eval (features & roadmap)
- [CONTAINER_CLOUD_ENHANCEMENTS.md](CONTAINER_CLOUD_ENHANCEMENTS.md) - How to enhance Container and Cloud scanners
- [SUPPORT_AND_SLA.md](SUPPORT_AND_SLA.md) - Support and SLA (placeholder for commercial use)
- [VULNERABILITY_INTEL.md](VULNERABILITY_INTEL.md) - Vulnerability intelligence: queries (CVE, CWE, NIST, OSV, CISA KEV, GitHub Advisory), results, scanner-update log; vetted sources only

### Standards & Compliance
- [STANDARDS_COMPLIANCE_RECOMMENDATIONS.md](STANDARDS_COMPLIANCE_RECOMMENDATIONS.md) - NIST, CIS, OWASP, MITRE, CISA, ISO recommendations
- [ENHANCED_FEATURES_ROADMAP.md](ENHANCED_FEATURES_ROADMAP.md) - Additional features based on standards

### Security Design
- [ATTACK_VECTORS_VULNERABILITIES.md](ATTACK_VECTORS_VULNERABILITIES.md) - Attack vectors and vulnerabilities
- [SECRETS_SCANNING_DESIGN.md](SECRETS_SCANNING_DESIGN.md) - Secrets scanning design
- [MITIGATION_REMEDIATION_GUIDE.md](MITIGATION_REMEDIATION_GUIDE.md) - Remediation steps for findings
- [LLM_POWERED_SCANNING.md](LLM_POWERED_SCANNING.md) - LLM integration design

### Testing & CI
- [TESTING.md](TESTING.md) - Unified testing framework
- [RUN_ALL_TESTS.md](RUN_ALL_TESTS.md) - How to run all tests
- [TEST_STATUS_CONFIRMATION.md](TEST_STATUS_CONFIRMATION.md) - Test pass and coverage summary
- [TESTING_GAPS.md](TESTING_GAPS.md) - Feature coverage and gaps
- [CI_AND_BRANCH_PROTECTION.md](CI_AND_BRANCH_PROTECTION.md) - Root CI and branch protection

### Project Planning
- [PROJECT_PROPOSAL.md](PROJECT_PROPOSAL.md) - Original project proposal
- [PROJECT_SPLIT_RECOMMENDATIONS.md](PROJECT_SPLIT_RECOMMENDATIONS.md) - Project split strategy
- [PROJECT_CONSOLIDATION.md](PROJECT_CONSOLIDATION.md) - Complete project consolidation
- [ROADMAP_NEXT.md](ROADMAP_NEXT.md) - What's next on the roadmap

### Research Agents
- [agents/](agents/) - All research agent scripts
  - Agent 1-6: Network security research
  - Agent 7-10: Cloud security research
  - Agent 11: Container security research

---

## 🚀 Projects Overview

### Project 1: NetSec-Core 🛡️
**Repository**: `netsec-core`  
**Focus**: Network Security Foundation

**Features**:
- Network scanning
- DNS security
- SSL/TLS monitoring
- Traffic analysis
- Anomaly detection

**Status**: Implemented

---

### Project 2: NetSec-Container 🐳
**Repository**: `netsec-container`  
**Focus**: Container & Kubernetes Security

**Features**:
- Image vulnerability scanning
- Secrets scanning (PRIMARY)
- Kubernetes security
- Runtime security
- Compliance checking

**Status**: Implemented

---

### Project 3: NetSec-Cloud ☁️
**Repository**: `netsec-cloud`  
**Focus**: Cloud Security, Compliance, Governance, Risk

**Features**:
- Multi-cloud CSPM
- Compliance automation
- Governance-as-code
- Risk assessment

**Status**: Implemented

---

## Quick Start

- **Run a project:** See root [README.md](README.md) (Quick Start). Each project: `pip install -e ".[dev]"`, then `uvicorn ...` and `pytest -v`.
- **Run all tests:** [RUN_ALL_TESTS.md](RUN_ALL_TESTS.md). Scripts: `run_all_tests_parallel.sh` / `.bat` / `.py`.
- **Roadmap:** [ROADMAP_NEXT.md](ROADMAP_NEXT.md). Research and standards: [RESEARCH_REVIEW.md](RESEARCH_REVIEW.md), [ENHANCED_FEATURES_ROADMAP.md](ENHANCED_FEATURES_ROADMAP.md).

---

## Repository links

Replace `your-org` with your GitHub org or user in docs (e.g. [SUPPORT_AND_SLA.md](SUPPORT_AND_SLA.md)). Per-project READMEs: [netsec-core/README.md](netsec-core/README.md), [netsec-cloud/README.md](netsec-cloud/README.md), [netsec-container/README.md](netsec-container/README.md).

---

## Current status

See [PROJECT_STATUS.md](PROJECT_STATUS.md) for per-project status. See [ROADMAP_NEXT.md](ROADMAP_NEXT.md) for what's next.
