# Operational Runbook

How to **deploy**, **configure**, and **operate** the NetSec Toolkit in a production-like environment. For development quick start, see each project’s README.

---

## 1. Deployment

### 1.1 NetSec-Core

```bash
cd netsec-core
pip install -e ".[dev]"   # or from wheel in production
uvicorn netsec_core.api.main:app --host 0.0.0.0 --port 8000
```

- **Docker:** Build from project Dockerfile (if present) or use a base Python image and install the package; expose port 8000.
- **Systemd:** Use a unit that runs `uvicorn netsec_core.api.main:app --host 0.0.0.0 --port 8000`; set `WorkingDirectory` to the project root.

### 1.2 NetSec-Cloud

```bash
cd netsec-cloud
pip install -e ".[dev]"
uvicorn netsec_cloud.api.main:app --host 0.0.0.0 --port 8000
```

- **Credentials:** Not stored by the API; clients pass credentials in each scan/compliance request. For automation, use a secrets manager and inject into the client.

### 1.3 NetSec-Container

```bash
cd netsec-container
pip install -e ".[dev]"
uvicorn netsec_container.api.main:app --host 0.0.0.0 --port 8000
```

- **Trivy/Syft:** Optional; if installed and on PATH, used for vuln and SBOM. Otherwise basic fallback and no SBOM.
- **Docker/Podman:** Optional for “image name” scans; for “upload” scans, only tar is needed.

---

## 2. Configuration

### 2.1 Environment variables (common)

| Variable | Product | Purpose |
|----------|----------|---------|
| `LOG_LEVEL` | All | Logging level (e.g. INFO, DEBUG) |
| `API_HOST` / `API_PORT` | Core | Bind address and port (if read by app) |

### 2.2 NetSec-Core

| Variable | Purpose |
|----------|---------|
| `LLM_PROVIDER` | openai, anthropic, ollama, etc. |
| `LLM_MODEL` | Model name |
| `LLM_API_KEY` or provider-specific key | API key for LLM |
| `LLM_BASE_URL` | Optional base URL for API |

### 2.3 NetSec-Cloud

- No server-side env for cloud credentials; they are passed per request. Optional: use env for default region or project if your app reads them.

### 2.4 NetSec-Container

| Variable | Purpose |
|----------|---------|
| `LLM_*` | Same as Core if LLM remediation is used |
| Trivy/Syft | Use system PATH; no env required by the app |

---

## 3. Health checks

| Product | Endpoint | Use |
|---------|----------|-----|
| Core | `GET /api/v1/health` | Readiness/liveness |
| Cloud | `GET /api/v1/health` | Readiness/liveness |
| Container | `GET /api/v1/health` | Readiness/liveness |

- **Expected:** 200 OK, JSON with `"status": "healthy"` (or equivalent). Use for Kubernetes readiness/liveness or load balancer health checks.

---

## 4. Logging

- **Format:** Application logs are typically stdout; structure depends on logging config (e.g. plain text or JSON).
- **Level:** Set via `LOG_LEVEL` or logging config. Use `INFO` in production; `DEBUG` for troubleshooting.
- **Sensitive data:** Avoid logging request bodies that contain credentials; the apps do not log credentials by default, but ensure middleware or proxies do not log them either.

---

## 5. Scaling

- **Stateless:** All three APIs are stateless. Run multiple instances behind a load balancer.
- **No shared state:** No database or queue required. Scale horizontally per product.

---

## 6. Troubleshooting

| Symptom | Product | Likely cause | Action |
|---------|----------|---------------|--------|
| 401 on scan | Cloud | Empty or invalid credentials in body | Check request body; validate credentials locally (e.g. aws sts get-caller-identity). |
| 503 on traffic | Core | Scapy not installed or import error | Install scapy or disable traffic routes; see docs. |
| 500 on scan | Container | Trivy missing or image pull failed | Install Trivy or use BasicVulnerabilityScanner; for “image name” scan ensure Docker/Podman and image pull works. |
| No secrets found | Container | Image not extracted | Ensure Docker/Podman available or use upload with a valid image tar. |
| Compliance check 400 | Cloud | Unsupported framework name | Use one of: cis, nist, pci_dss, hipaa (see GET /compliance/frameworks). |

### 6.1 Common failures

- **Cloud 401:** Credentials missing or wrong in POST body. Verify provider-specific CLI (aws, az, gcloud) with same creds.
- **Container 500 on POST /scan:** Image name invalid or unreachable; or Trivy crash. Try with `enable_vulnerability: false` and a small image, or use POST /scan/upload with a tar.
- **Core traffic 503:** Scapy required for traffic routes. Install or mock in tests.

---

## 7. Security operations

- **Network:** Expose only the API port; do not expose internal admin endpoints if any.
- **Credentials:** Never log or cache cloud credentials in the app; use short-lived tokens where possible.
- **Updates:** Run `pip-audit` and update dependencies; see [DEPENDENCY_AUDIT.md](DEPENDENCY_AUDIT.md).

For what we check and which frameworks we map to, see [SECURITY_AND_COMPLIANCE.md](SECURITY_AND_COMPLIANCE.md). For API details, see [API_REFERENCE.md](API_REFERENCE.md).
