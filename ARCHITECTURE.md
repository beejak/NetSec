# Architecture

High-level architecture of the NetSec Toolkit for architects and operators. For per-project details, see each project’s README and existing diagrams.

---

## 1. Overview

The toolkit is **three independent products** that can run separately or together:

```
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│   NetSec-Core   │   │  NetSec-Cloud   │   │ NetSec-Container│
│                 │   │                 │   │                 │
│ • API (FastAPI) │   │ • API (FastAPI) │   │ • API (FastAPI) │
│ • CLI (Click)   │   │ • CLI (Click)   │   │ • CLI (Click)   │
│ • Scanners      │   │ • Providers     │   │ • Scanner       │
│   (DNS, SSL,    │   │   (AWS, Azure,  │   │   (Trivy,       │
│    traffic,     │   │    GCP)         │   │    secrets,     │
│    anomaly,     │   │ • Compliance    │   │    Dockerfile,  │
│    assets)      │   │   mapping       │   │    SBOM)         │
│ • Remediation   │   │                 │   │ • Image extract │
│ • LLM (opt)     │   │                 │   │ • LLM (opt)     │
└────────┬────────┘   └────────┬────────┘   └────────┬────────┘
         │                     │                     │
         │                     │                     │
         ▼                     ▼                     ▼
   Network / DNS          Cloud APIs            Docker / tar
   SSL / targets         (boto3, azure,        (images, layers)
                          google-api)
```

- **NetSec-Core:** Network, DNS, SSL, traffic, anomaly, assets; optional LLM. No dependency on Cloud or Container.
- **NetSec-Cloud:** Multi-cloud scanning and compliance mapping. No dependency on Core or Container.
- **NetSec-Container:** Image scanning (vulns, secrets, Dockerfile, SBOM). No dependency on Core or Cloud.

---

## 2. Design principles

| Principle | How it shows up |
|-----------|------------------|
| **Minimal dependencies** | Core: optional scapy for traffic; Cloud: only official SDKs (boto3, azure-mgmt-*, google-api-python-client); Container: Trivy/Syft optional, basic fallbacks. |
| **Unified interface** | Cloud: one scanner interface, multiple providers (AWS, Azure, GCP). Same API/CLI pattern across products. |
| **Bring-your-own credentials** | Cloud: credentials in request body; Core/Container: LLM keys via env or request. No built-in secret store. |
| **Stateless API** | No server-side session store; each request carries what it needs. Safe for horizontal scaling behind a load balancer. |

---

## 3. Component roles

### 3.1 NetSec-Core

- **API:** FastAPI app; routes for health, DNS, SSL, scan, anomaly, assets, remediation, traffic, LLM.
- **CLI:** Click groups (scan, dns, ssl, traffic, anomaly, assets, remediation, health).
- **Scanners:** DNSScanner, SSLScanner, NetworkScanner, TrafficAnalyzer (optional), AnomalyDetector, AssetDiscovery.
- **Remediation:** Static guide keyed by finding type.
- **LLM:** Optional; LLMAnalyzer with configurable provider (OpenAI, Anthropic, etc.).

### 3.2 NetSec-Cloud

- **API:** FastAPI; routes for health, providers, scan, scan/multi, compliance/frameworks, compliance/check.
- **Providers:** AWS, Azure, GCP; each implements storage, IAM, networking, (optional) compute checks.
- **Compliance:** Mapping layer from findings to CIS, NIST, PCI-DSS, HIPAA control IDs; used by POST /compliance/check.

### 3.3 NetSec-Container

- **API:** FastAPI; routes for health, scan, scan/upload.
- **Scanner:** ContainerScanner orchestrates Trivy (vulns), secrets scan, Dockerfile analysis, SBOM (Syft); BasicVulnerabilityScanner when Trivy unavailable.
- **Image extraction:** ImageExtractor (Docker/Podman or tar) to get layers for secrets/vuln.
- **Scoring:** RiskScorer produces 0–100 score from findings.

---

## 4. Deployment view

- Each product runs as its own **process** (e.g. `uvicorn netsec_core.api.main:app`). No shared database.
- Typical deployment: reverse proxy (e.g. nginx) in front of one or more instances; health checks on `/api/v1/health`.
- For high availability: run multiple instances per product behind a load balancer; no sticky session required.

---

## 5. Links to existing docs

- **NetSec-Core:** [netsec-core/README.md](netsec-core/README.md), [netsec-core/QUICKSTART.md](netsec-core/QUICKSTART.md), architecture/diagrams in netsec-core if present.
- **NetSec-Cloud:** [netsec-cloud/README.md](netsec-cloud/README.md), network/architecture notes in netsec-cloud.
- **NetSec-Container:** [netsec-container/README.md](netsec-container/README.md), [netsec-container/ROADMAP.md](netsec-container/ROADMAP.md).

For API contracts, see [API_REFERENCE.md](API_REFERENCE.md). For operations, see [RUNBOOK.md](RUNBOOK.md).
