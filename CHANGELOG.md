# Changelog

All notable changes to the NetSec Toolkit are documented here. Format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### Added
- **Testing:** Core API tests for traffic (flows, analyze), assets discover, anomaly learn-baseline, LLM analyze-traffic. Core CLI tests for traffic, anomaly, assets, remediation get, health. Container API test for root (HTML or JSON).
- **Docs:** Mid-project evaluation ([MID_PROJECT_EVALUATION.md](MID_PROJECT_EVALUATION.md)), enterprise documentation guide ([ENTERPRISE_DOCUMENTATION.md](ENTERPRISE_DOCUMENTATION.md)), enterprise docs (API_REFERENCE, SECURITY_AND_COMPLIANCE, ARCHITECTURE, RUNBOOK), enhancement guide for Container and Cloud ([CONTAINER_CLOUD_ENHANCEMENTS.md](CONTAINER_CLOUD_ENHANCEMENTS.md)), ROADMAP_NEXT, SUPPORT_AND_SLA placeholder. Per-project READMEs link to root API_REFERENCE.
- **NetSec-Cloud:** AWS **audit** check type: `scan_audit_logging` checks CloudTrail enabled and logging; mapped to CIS 3.1/3.2, NIST DE.CM-1, PCI-DSS 10.2, HIPAA Audit Controls. Use `check_types: ["storage", "iam", "audit"]` to include.
- **Vulnerability intelligence placeholder:** [VULNERABILITY_INTEL.md](VULNERABILITY_INTEL.md) and `vulnerability-intel/` (queries.md with vetted sources NVD, CVE, CWE, OSV, CISA KEV, GitHub Advisory; results/; scanner-updates.md). All query templates reference official/industry sources. Container BasicVulnerabilityScanner and docs reference vuln-intel for future CVE DB.
- **NetSec-Container:** Image extraction with **skopeo** and **crane** when Docker/Podman unavailable (oci-archive tar then extract; crane export to tar). Optional **OSV** CVE lookup in BasicVulnerabilityScanner (Debian, Alpine, PyPI, npm); `enable_osv_lookup=True` by default.
- **NetSec-Cloud:** AWS **root account access keys** check (CIS 1.4); mapped to CIS, NIST PR.AC-4, PCI-DSS 7.1, HIPAA Access Control.
- **CI:** Lint enforced (ruff check; removed `|| true`). Optional pip-audit step per job.
- **Tests:** Cloud test_compliance: iam_root_access_keys mapping. Container: image_extractor use_skopeo/use_crane; vulnerability_basic enable_osv_lookup and _query_osv unknown ecosystem.

### Changed
- TESTING_GAPS.md updated to reflect new Core and Container test coverage.

---

## [0.2.0] – 2025-02 (prior state)

### Added
- NetSec-Cloud: AWS compute checks (EC2 IMDSv2, EBS encryption, public IP); Azure RBAC scan_iam; GCP IAM scan_iam; PCI-DSS and HIPAA compliance mapping; remediation text for findings.
- NetSec-Container: ImageExtractor (Docker/Podman + tar), BasicVulnerabilityScanner, tests for secrets, vuln, Dockerfile, scoring, image extractor.
- Root CI (`.github/workflows/ci.yml`), run_all_tests_parallel scripts, TESTING_GAPS, ROADMAP_NEXT, DEPENDENCY_AUDIT, CI_AND_BRANCH_PROTECTION.

### Changed
- Core: Extended test_api_routes (anomaly status, remediation list/get, assets inventory, anomaly detect). Cloud: test_api (compliance frameworks/controls, scan 401, compliance check 401/400, multi-scan body). Container: test_api (health, scan POST, scan/upload).

---

## [0.1.0] – Initial

### Added
- NetSec-Core: Network, DNS, SSL, traffic, anomaly, assets, remediation, LLM; API and CLI.
- NetSec-Cloud: AWS, Azure, GCP providers; storage, IAM, networking; CIS/NIST mapping; API and CLI.
- NetSec-Container: Image scanning (Trivy), secrets, Dockerfile, SBOM, risk scoring; API and CLI.
- Documentation: READMEs, testing docs, research and roadmap docs.

---

*For detailed commit history, see git log.*
