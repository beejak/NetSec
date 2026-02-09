# NetSec Toolkit

A suite of three security projects: **NetSec-Core** (network security), **NetSec-Cloud** (multi-cloud security & compliance), and **NetSec-Container** (container & image security). Built on research across 11 specialized agents and designed to fill gaps in the network and cloud security tool landscape.

---

## Overview

| Project | Description | Status |
|--------|-------------|--------|
| **[NetSec-Core](netsec-core/)** | Network scanning, DNS security, SSL/TLS monitoring, traffic analysis, anomaly detection, LLM integration | Implemented |
| **[NetSec-Cloud](netsec-cloud/)** | Multi-cloud (AWS, Azure, GCP) scanning, CIS/NIST compliance mapping, storage/IAM/networking/compute checks | Implemented |
| **[NetSec-Container](netsec-container/)** | Container image scanning, secrets detection, vulnerability scanning, SBOM, LLM remediation | In progress |

---

## Quick Start

### Run one project

```bash
# NetSec-Core (network security)
cd netsec-core
pip install -e ".[dev]"
uvicorn netsec_core.api.main:app --reload    # API at http://localhost:8000
pytest -v                                     # tests

# NetSec-Cloud (cloud security)
cd netsec-cloud
pip install -e ".[dev]"
uvicorn netsec_cloud.api.main:app --reload    # API at http://localhost:8000
pytest -v                                     # tests

# NetSec-Container (container security)
cd netsec-container
pip install -e ".[dev]"
uvicorn netsec_container.api.main:app --reload
pytest -v
```

### Run all tests

See **[RUN_ALL_TESTS.md](RUN_ALL_TESTS.md)** and **[TEST_STATUS_CONFIRMATION.md](TEST_STATUS_CONFIRMATION.md)**. Per project:

```bash
cd netsec-core    && pip install -e ".[dev]" && pytest -v -m "not integration"
cd netsec-cloud   && pip install -e ".[dev]" && pytest -v
cd netsec-container && pip install -e ".[dev]" && pytest -v
```

Or use `run_all_tests_parallel.sh` / `.bat` / `.py` at repo root.

---

## Documentation

### Enterprise & operations
- **[API_REFERENCE.md](API_REFERENCE.md)** – API overview and OpenAPI docs links
- **[SECURITY_AND_COMPLIANCE.md](SECURITY_AND_COMPLIANCE.md)** – What we check; CIS/NIST/PCI-DSS/HIPAA
- **[ARCHITECTURE.md](ARCHITECTURE.md)** – High-level architecture and design
- **[RUNBOOK.md](RUNBOOK.md)** – Deploy, config, health, logs, troubleshooting
- **[CHANGELOG.md](CHANGELOG.md)** – Version history and release notes
- **[ENTERPRISE_DOCUMENTATION.md](ENTERPRISE_DOCUMENTATION.md)** – Enterprise doc checklist and actions
- **[SUPPORT_AND_SLA.md](SUPPORT_AND_SLA.md)** – Support and SLA (placeholder for commercial use)
- **[MID_PROJECT_EVALUATION.md](MID_PROJECT_EVALUATION.md)** – Unbiased mid-project eval (features & roadmap)
- **[CONTAINER_CLOUD_ENHANCEMENTS.md](CONTAINER_CLOUD_ENHANCEMENTS.md)** – How to enhance Container and Cloud scanners
- **[VULNERABILITY_INTEL.md](VULNERABILITY_INTEL.md)** – Vulnerability intelligence: queries (CVE, CWE, NIST, OSV, CISA KEV, GitHub Advisory), results, scanner-update log

### Getting started
- **[TESTING.md](TESTING.md)** – Unified testing framework (pytest, fixtures, markers)
- **[UNIT_AND_INTEGRATION_TESTING.md](UNIT_AND_INTEGRATION_TESTING.md)** – Unit vs integration tests: what they are, how to run them
- **[TESTING_GAPS.md](TESTING_GAPS.md)** – Feature coverage and testing gaps
- **[COMPREHENSIVE_TESTING_FRAMEWORK.md](COMPREHENSIVE_TESTING_FRAMEWORK.md)** – Use cases, parallel execution, implementation phases
- **[CI_AND_BRANCH_PROTECTION.md](CI_AND_BRANCH_PROTECTION.md)** – Root CI and branch protection
- **[DEPENDENCY_AUDIT.md](DEPENDENCY_AUDIT.md)** – pip-audit and dependency checks
- **[ROADMAP_NEXT.md](ROADMAP_NEXT.md)** – What’s next on the roadmap (testing, Core/Cloud/Container priorities)
- **[RUN_ALL_TESTS.md](RUN_ALL_TESTS.md)** – How to run all tests and sanity
- **[SANITY_AND_TEST_CONFIRMATION.md](SANITY_AND_TEST_CONFIRMATION.md)** – What sanity covers and how to re-run
- **[MASTER_INDEX.md](MASTER_INDEX.md)** – Full documentation index
- **[RESEARCH_REVIEW.md](RESEARCH_REVIEW.md)** – Research summary
- **[PROJECT_CONSOLIDATION.md](PROJECT_CONSOLIDATION.md)** – Project breakdown

### Research & design
- [RESEARCH_REPORT.md](RESEARCH_REPORT.md) – Network security research
- [CLOUD_SECURITY_RESEARCH.md](CLOUD_SECURITY_RESEARCH.md) – Cloud security research
- [GAP_ANALYSIS.md](GAP_ANALYSIS.md) – Gap analysis
- [ATTACK_VECTORS_VULNERABILITIES.md](ATTACK_VECTORS_VULNERABILITIES.md) – Attack vectors
- [SECRETS_SCANNING_DESIGN.md](SECRETS_SCANNING_DESIGN.md) – Secrets scanning design
- [MITIGATION_REMEDIATION_GUIDE.md](MITIGATION_REMEDIATION_GUIDE.md) – Remediation guide
- [LLM_POWERED_SCANNING.md](LLM_POWERED_SCANNING.md) – LLM integration
- [STANDARDS_COMPLIANCE_RECOMMENDATIONS.md](STANDARDS_COMPLIANCE_RECOMMENDATIONS.md) – NIST, CIS, OWASP
- [ENHANCED_FEATURES_ROADMAP.md](ENHANCED_FEATURES_ROADMAP.md) – Roadmap

### Project docs
- **[netsec-core/README.md](netsec-core/README.md)** – Core install, API, CLI, testing
- **[netsec-cloud/README.md](netsec-cloud/README.md)** – Cloud install, scan, compliance, testing
- **[netsec-container/README.md](netsec-container/README.md)** – Container install, scan, testing

---

## Project structure

```
Netsec-Toolkit/
├── netsec-core/          # Network security (DNS, SSL, scanning, traffic, LLM)
├── netsec-cloud/         # Multi-cloud security & compliance (AWS, Azure, GCP)
├── netsec-container/     # Container & image security (secrets, vulns, SBOM)
├── agents/               # Research agents (11 agents)
├── scripts/              # Init scripts (init_core.sh, init_cloud.sh, init_container.sh)
├── TESTING.md            # Testing framework
├── RUN_ALL_TESTS.md      # Run all tests guide
└── *.md                  # Research and planning docs
```

---

## Technology stack

| Layer | Stack |
|-------|--------|
| **Common** | Python 3.10+, FastAPI, Click, Pydantic, pytest |
| **NetSec-Core** | scapy, dnspython, cryptography, optional LLM (OpenAI, Anthropic, Ollama, etc.) |
| **NetSec-Cloud** | boto3, azure-mgmt-*, google-cloud-* (optional extras) |
| **NetSec-Container** | docker, kubernetes, pyyaml, trufflehog, detect-secrets, reportlab |

---

## Contributing

Contributions are welcome. See each project’s README and [PROJECT_CONSOLIDATION.md](PROJECT_CONSOLIDATION.md) for details. When cloning or linking, replace `your-org` in [SUPPORT_AND_SLA.md](SUPPORT_AND_SLA.md) and [MASTER_INDEX.md](MASTER_INDEX.md) with your GitHub org or repo path.

---

## Dependency audit

Run `pip install pip-audit && pip-audit` from each project after installing to check for known vulnerabilities. See [DEPENDENCY_AUDIT.md](DEPENDENCY_AUDIT.md).

## License

MIT. See [netsec-core/LICENSE](netsec-core/LICENSE) and [netsec-cloud/LICENSE](netsec-cloud/LICENSE).
