# NetSec Toolkit: Project Status

Current status of the three projects. For what's next, see [ROADMAP_NEXT.md](ROADMAP_NEXT.md).

---

## NetSec-Core – Complete

**Status:** Implemented and maintained.

- **Features:** Network scanning, DNS security, SSL/TLS monitoring, traffic analysis, anomaly detection, asset discovery, LLM integration, remediation.
- **API/CLI:** 30+ endpoints, 20+ CLI commands. OpenAPI at `/api/docs`.
- **Tests:** Unit, API, CLI (including traffic, anomaly, assets, remediation, health). Integration tests available.
- **Docs:** README, QUICKSTART, USAGE_GUIDE, HELP, ARCHITECTURE.

---

## NetSec-Cloud – Implemented

**Status:** Multi-cloud scanning and compliance in place.

- **Features:** AWS, Azure, GCP providers; storage, IAM, networking, compute (AWS EC2), audit (AWS CloudTrail); root account access keys check. Compliance mapping: CIS, NIST, PCI-DSS, HIPAA.
- **API/CLI:** Scan (single/multi), compliance frameworks and check. Lint enforced in CI; optional pip-audit.
- **Tests:** API, CLI, scanner, providers, compliance mapping.
- **Docs:** README, QUICKSTART, ARCHITECTURE_DESIGN.

---

## NetSec-Container – Implemented

**Status:** Image scanning, secrets, fallback vuln path, optional OSV CVE lookup.

- **Features:** Image extraction (Docker, Podman, skopeo, crane, tar upload); vulnerability scanning (Trivy or BasicVulnerabilityScanner with optional OSV); secrets, Dockerfile, SBOM, risk scoring.
- **API/CLI:** Scan, scan/upload. Lint enforced in CI; optional pip-audit.
- **Tests:** API, CLI, scanner, secrets, vulnerability_basic, dockerfile, scoring, image_extractor.
- **Docs:** README, ROADMAP.

---

## Summary

| Project   | Status      | Next (see ROADMAP_NEXT)        |
|-----------|-------------|---------------------------------|
| Core      | Complete    | Optional unit tests; defer log/exfil |
| Cloud     | Implemented | More identity/encryption checks |
| Container | Implemented | Runtime/K8s, SBOM (Phase 2)    |
