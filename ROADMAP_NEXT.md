# What's Next on the Roadmap

This document summarizes the **next priorities** across the NetSec Toolkit, based on [ENHANCED_FEATURES_ROADMAP.md](ENHANCED_FEATURES_ROADMAP.md), [PROJECT_STATUS.md](PROJECT_STATUS.md), [TESTING_GAPS.md](TESTING_GAPS.md), and [netsec-container/ROADMAP.md](netsec-container/ROADMAP.md).

---

## 1. Testing (short term)

| Area | Next |
|------|------|
| **Core** | Add API tests for traffic routes, assets/discover, LLM (mock); CLI tests for traffic, anomaly, assets, remediation, health; unit tests for TrafficAnalyzer (scapy), LLMAnalyzer (mock). |
| **Cloud** | IAM wildcard check extended to all customer-managed policies (not just name filter); S3 encryption and IAM wildcard provider tests added. |
| **Container** | Root HTML content test and CLI smoke for scan/serve added. |

See **[TESTING_GAPS.md](TESTING_GAPS.md)** for the full gap list.

---

## 2. NetSec-Core

| Priority | Item | Source |
|----------|------|--------|
| High | **Log analysis** – Security log collection/parsing, event detection, anomaly in logs (CIS 8, NIST SI-4). | ENHANCED_FEATURES_ROADMAP |
| Medium | **Data exfiltration detection** – Large transfers, unusual patterns, encrypted tunnel detection (MITRE ATT&CK). | ENHANCED_FEATURES_ROADMAP |
| Medium | **DoS detection** – Traffic spikes, connection floods, availability monitoring. | ENHANCED_FEATURES_ROADMAP |
| Lower | **Injection pattern detection** – SQL/command/XSS injection patterns (OWASP A03). | ENHANCED_FEATURES_ROADMAP |

---

## 3. NetSec-Cloud

| Priority | Item | Source |
|----------|------|--------|
| High | **Deeper provider coverage** – AWS (CloudTrail, Config, Lambda); Azure (Key Vault, VM/App Service); GCP (project IAM bindings, GKE, Compute). | PROJECT_STATUS, gaps |
| High | **Identity / encryption validation** – IAM policy validation, MFA validation; encryption at rest/transit, key management (CISA, ISO 27001). | ENHANCED_FEATURES_ROADMAP |
| Medium | **Account management auditing** – Account lifecycle, privileged/inactive accounts (CIS 5). | ENHANCED_FEATURES_ROADMAP |
| Medium | **Backup validation** – Backup config, frequency, encryption (CIS 11). | ENHANCED_FEATURES_ROADMAP |
| Lower | **Third-party risk** – Vendor/integration assessment (CIS 15). | ENHANCED_FEATURES_ROADMAP |

---

## 4. NetSec-Container

| Priority | Item | Source |
|----------|------|--------|
| High | **Image extraction** – Reliable extraction for secrets scanning (Docker/Podman + tar; layer walk). | netsec-container/ROADMAP |
| High | **Fallback vulnerability path** – BasicVulnerabilityScanner + optional CVE DB when Trivy unavailable. | netsec-container/ROADMAP |
| High | **Web UI** – Finish drag-and-drop upload and live results. | netsec-container/ROADMAP |
| Medium | **Image signature verification** – Content Trust, signing (NIST SP 800-190, OWASP C8). | ENHANCED_FEATURES_ROADMAP |
| Medium | **SBOM** – SPDX/CycloneDX, license detection (CISA supply chain). | ENHANCED_FEATURES_ROADMAP |
| Planned | **Runtime security** – Runtime monitoring, privilege escalation, container escape (Falco-style). | netsec-container/ROADMAP |
| Planned | **Kubernetes** – Manifest scanning, network policies, cluster assessment (kube-bench style). | netsec-container/ROADMAP |

---

## 5. Cross-cutting

| Area | Next |
|------|------|
| **CI** | Lint enforced (removed `\|\| true` from ruff check); optional coverage upload and thresholds. |
| **Docs** | Refresh per-project HELP/QUICKSTART; replace any remaining placeholders. |
| **Dependencies** | Run `pip-audit` per project; add audit step to CI; see [DEPENDENCY_AUDIT.md](DEPENDENCY_AUDIT.md). |
| **Vulnerability intel** | Use [VULNERABILITY_INTEL.md](VULNERABILITY_INTEL.md) and `vulnerability-intel/` (queries, results, scanner-update log) to feed CVE DB or scanner updates; all sources vetted (NVD, CVE, CWE, OSV, CISA KEV, GitHub Advisory). |

---

## Suggested order

1. **Close testing gaps** (Core traffic/assets/LLM tests, Cloud multi-scan, Container HTML/CLI) for stability. *(Done: API/CLI smoke, multi-scan response shape, root HTML/CLI scan/serve smoke, S3 encryption provider test; CI lint enforced.)*
2. **NetSec-Container**: Image extraction and fallback vuln path so container scanning is usable without Trivy. *(Done: skopeo/crane when no Docker; optional OSV CVE lookup in BasicVulnerabilityScanner.)*
3. **NetSec-Cloud**: Deeper provider coverage and identity/encryption validation for compliance. *(Done: S3 default encryption check + CIS/NIST mapping; root access keys, CloudTrail. Next: more identity/encryption checks.)*
4. **NetSec-Core**: Log analysis and data exfiltration/DoS detection for detection value. *(Defer until use case.)*
5. **Container**: Runtime/K8s and image signing/SBOM as Phase 2.

Full detail: **[ENHANCED_FEATURES_ROADMAP.md](ENHANCED_FEATURES_ROADMAP.md)**, **[netsec-container/ROADMAP.md](netsec-container/ROADMAP.md)**.
