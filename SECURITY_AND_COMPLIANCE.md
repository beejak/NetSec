# Security and Compliance

This document describes **what the NetSec Toolkit checks** and **which compliance frameworks** it maps to. Use it for security reviews and compliance discussions.

---

## 1. NetSec-Core

### What we check

| Area | Checks | Notes |
|------|--------|--------|
| **Network** | Port scan, service detection | Target and ports configurable |
| **DNS** | Tunneling, spoofing, pattern analysis | Optional checks |
| **SSL/TLS** | Certificate validity, expiration, ciphers, chain | Hostname and port configurable |
| **Traffic** | Capture and analysis (optional) | Requires scapy; may be disabled in restricted environments |
| **Anomaly** | Baseline learning, metric-based detection | In-memory; no PII stored |
| **Assets** | Network discovery, inventory generation | Uses network scan results |
| **Remediation** | Static guidance per finding type | No external calls |
| **LLM** | Optional analysis, false-positive reduction, remediation generation | Bring-your-own API key; no data sent unless configured |

### Data handling

- **No PII logging:** Scanned targets (hostnames, IPs) may appear in logs; no user credentials stored.
- **LLM:** If enabled, traffic summaries or finding text may be sent to the configured LLM provider (OpenAI, Anthropic, etc.). Keys and endpoints are user-configured.
- **On-prem:** Core can run entirely on-premises; no telemetry to third parties by default.

### Compliance mapping (Core)

- Core does **not** emit framework-specific control IDs. It produces **findings** that can be consumed by Cloud or external tools. Remediation types align with common controls (e.g. weak cipher → TLS hardening).

---

## 2. NetSec-Cloud

### What we check

| Provider | Areas | Examples |
|----------|--------|----------|
| **AWS** | Storage, IAM, networking, compute, audit | S3 public access, EBS encryption, EC2 IMDSv2, public IP; CloudTrail enabled and logging (when check_types includes `audit`) |
| **Azure** | Storage, IAM (RBAC), NSG | Blob public access, subscription-level broad roles, NSG rules |
| **GCP** | Storage, IAM, firewall | GCS public access, project-level Owner/Editor for users, firewall rules |

- **Storage:** Public access, encryption (where supported), bucket/container listing.
- **IAM:** Broad roles (Owner, Contributor, Editor, User Access Admin) for users and service principals.
- **Networking:** Public exposure, overly permissive rules.
- **Compute (AWS):** EC2 IMDSv2, EBS encryption, public IP.

### Compliance frameworks supported

| Framework | Name | Use |
|-----------|------|-----|
| **cis** | CIS Benchmarks | Map findings to CIS control IDs |
| **nist** | NIST | Map findings to NIST control IDs |
| **pci_dss** | PCI-DSS | Map findings to PCI-DSS requirements |
| **hipaa** | HIPAA | Map findings to HIPAA-relevant controls |

- **API:** `GET /api/v1/cloud/compliance/frameworks` lists frameworks; `GET .../frameworks/{fw}/controls` lists controls; `POST .../compliance/check` runs a scan and maps results to the chosen framework.
- **Remediation:** Findings include remediation text where applicable.

### Data handling

- **Credentials:** Supplied in request body; not persisted by the API. Credentials are used only to call cloud provider APIs.
- **Scan results:** Returned in the response; persistence is the caller’s responsibility (e.g. logging, SIEM).
- **On-prem / self-hosted:** Cloud API can run in your environment; no telemetry to third parties by default.

---

## 3. NetSec-Container

### What we check

| Area | Checks | Notes |
|------|--------|--------|
| **Vulnerabilities** | Image layers, OS and app packages | Trivy when available; basic fallback (package list) when not |
| **Secrets** | Pattern-based scan in image layers | Requires extracted image (Docker/Podman or uploaded tar) |
| **Dockerfile** | Best practices | Dockerfile analysis |
| **SBOM** | Software bill of materials | Syft when available |
| **Risk score** | 0–100 score from findings | Combined severity and count |
| **LLM** | Optional remediation generation | Bring-your-own API key |

### Data handling

- **Images:** Processed locally or via uploaded tar; not sent to third parties except if LLM is configured and you send finding text.
- **Secrets:** Detected locally; no automatic reporting to external systems.

### Compliance mapping (Container)

- Container produces **findings** (vulns, secrets, Dockerfile issues). It does not currently emit framework-specific control IDs; findings can be fed into Cloud or external compliance tooling.

---

## 4. Summary table

| Product | Security checks | Compliance frameworks | Data location |
|---------|-----------------|------------------------|---------------|
| **Core** | Network, DNS, SSL, traffic, anomaly, assets | N/A (findings only) | On-prem / your control |
| **Cloud** | AWS/Azure/GCP storage, IAM, networking, compute | CIS, NIST, PCI-DSS, HIPAA | On-prem / your control |
| **Container** | Image vulns, secrets, Dockerfile, SBOM | N/A (findings only) | On-prem / your control |

For **exact** control IDs and mapping logic, see NetSec-Cloud source: `netsec_cloud/compliance/mapping.py` and API routes under `compliance/`.
