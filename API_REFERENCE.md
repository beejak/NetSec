# API Reference

This document is the single entry for **how to call the NetSec APIs**. For interactive exploration, use each product’s **OpenAPI (Swagger) docs** when the server is running.

---

## Base URLs and versioning

| Product | Default base | API prefix | OpenAPI docs |
|---------|--------------|------------|--------------|
| **NetSec-Core** | `http://localhost:8000` | `/api/v1/` | `http://localhost:8000/api/docs` |
| **NetSec-Cloud** | `http://localhost:8000` | `/api/v1/` | `http://localhost:8000/docs` (or `/api/docs`) |
| **NetSec-Container** | `http://localhost:8000` | `/api/v1/` | `http://localhost:8000/docs` (or `/api/docs`) |

- All APIs use **JSON** request/response bodies unless noted.
- Version prefix is **`/api/v1/`**. Future versions may use `/api/v2/` etc.

---

## NetSec-Core – Main endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/` | App info (name, version, status) |
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/dns/scan` | DNS security scan |
| POST | `/api/v1/ssl/check-certificate` | SSL/TLS certificate check |
| POST | `/api/v1/scan/ports` | Port scan |
| GET | `/api/v1/anomaly/status` | Anomaly detection status |
| POST | `/api/v1/anomaly/learn-baseline` | Learn anomaly baseline |
| POST | `/api/v1/anomaly/detect` | Detect anomaly (metric + value) |
| POST | `/api/v1/assets/discover` | Discover assets (query: network) |
| POST | `/api/v1/assets/inventory` | Generate asset inventory |
| GET | `/api/v1/remediation/` | List remediation types |
| GET | `/api/v1/remediation/{finding_type}` | Get remediation for a finding type |
| POST | `/api/v1/traffic/capture` | Capture traffic (optional: scapy) |
| POST | `/api/v1/traffic/analyze` | Analyze traffic |
| GET | `/api/v1/traffic/flows` | Get traffic flows |
| POST | `/api/v1/llm/analyze-traffic` | LLM traffic analysis |
| POST | `/api/v1/llm/reduce-false-positives` | LLM false-positive reduction |
| POST | `/api/v1/llm/generate-remediation` | LLM remediation generation |

**Auth:** None by default. Add API key or bearer if you deploy behind a gateway.

**OpenAPI:** Run Core, then open `http://localhost:8000/api/docs` and `http://localhost:8000/api/openapi.json`.

---

## NetSec-Cloud – Main endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/` | App info |
| GET | `/api/v1/health` | Health check |
| GET | `/api/v1/cloud/providers` | List providers (aws, azure, gcp) |
| POST | `/api/v1/cloud/scan` | Single-provider scan (body: provider, credentials, check_types). check_types: storage, iam, networking, compute, audit (AWS only) |
| POST | `/api/v1/cloud/scan/multi` | Multi-cloud scan (body: providers list, check_types) |
| GET | `/api/v1/cloud/compliance/frameworks` | List frameworks (cis, nist, pci_dss, hipaa) |
| GET | `/api/v1/cloud/compliance/frameworks/{fw}/controls` | List controls for a framework |
| POST | `/api/v1/cloud/compliance/check` | Run scan and map to framework (query: provider, framework; body: credentials) |

**Auth:** Scan and compliance/check require **valid cloud credentials** in the request body. No separate API key unless you add one.

**OpenAPI:** Run Cloud, then open `/docs` or `/openapi.json` at the same host/port.

---

## NetSec-Container – Main endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/` | App info or HTML UI |
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/scan` | Scan image (body: image, enable_vulnerability, enable_secrets, enable_sbom) |
| POST | `/api/v1/scan/upload` | Scan uploaded image tar (multipart: file) |

**Auth:** None by default.

**OpenAPI:** Run Container, then open `/docs` or `/openapi.json` at the same host/port.

---

## Common patterns

- **Health:** All three products expose `/api/v1/health` (or equivalent). Use for readiness probes.
- **Errors:** APIs return JSON with `detail` (string or list) on 4xx/5xx. See OpenAPI schema for response shapes.
- **Rate limits:** Not enforced by default; add at reverse proxy or gateway if needed.

For full request/response schemas, use the **interactive docs** (`/api/docs` or `/docs`) or the **OpenAPI JSON** (`/api/openapi.json` or `/openapi.json`) for each product.
