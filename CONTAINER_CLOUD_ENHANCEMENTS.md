# How to Enhance Container and Cloud Scanners

Concrete, actionable ways to improve the **current** functionality of NetSec-Container and NetSec-Cloud without scope creep.

---

## Part 1: NetSec-Container Enhancements

### 1.1 Image extraction (when Docker/Podman unavailable)

**Current state:** `ImageExtractor` uses Docker or Podman to export images, plus `extract_tar_file()` for tar input. In CI or restricted environments, Docker/Podman may be unavailable.

**Enhancements:**

1. **Tar-first path for “uploaded” scans**
   - API already has `/scan/upload` for tar files. The pipeline **already** uses the uploaded tar when provided: when `image_file` (or upload path) is set, the scanner passes it to secrets and vulnerability scanners, which use `extract_tar_file` (no Docker pull).
   - Document: “For environments without Docker, build image tar locally (`docker save` / `podman save`) and use POST /scan/upload.”

2. **Optional skopeo/crane path**
   - Add a helper that uses `skopeo copy` or `crane export` (if installed) to pull and save an image as tar, then feed that into existing tar extraction.
   - Keeps “no Docker daemon” support without reimplementing OCI.

3. **Layer walk without daemon**
   - For tar-only: walk OCI tar layers, extract to temp dir, run secrets/vuln scan on that dir. You already have layer iteration in `ImageExtractor`; ensure it’s used for upload path so secrets scanning works from tar alone.

**Priority:** High for “works in CI without Docker” story.

---

### 1.2 Fallback vulnerability path (without Trivy)

**Current state:** `BasicVulnerabilityScanner` parses package manager files (dpkg, rpm, apk, pip, npm) from extracted image. No CVE lookup yet.

**Enhancements:**

1. **Optional CVE database**
   - Use a small, offline CVE/CPE dataset (e.g. OSV, or a curated JSON by distro) keyed by package name + version.
   - In `BasicVulnerabilityScanner`, after parsing packages, look up CVEs and attach to `Vulnerability` objects. Start with one distro (e.g. Debian/Ubuntu) to keep scope small.
   - Query and result placeholders (vetted sources: NVD, CVE, CWE, OSV, CISA KEV, GitHub Advisory): see [VULNERABILITY_INTEL.md](VULNERABILITY_INTEL.md) and `vulnerability-intel/`.

2. **Clear UX when Trivy is missing**
   - If Trivy is not installed: automatically use `BasicVulnerabilityScanner` and set a flag in the report (e.g. `vulnerability_source: "basic"`). Document that “basic” has no CVE data unless CVE DB is added.

3. **Version comparison**
   - For “basic” path, if you have CVE DB with “fixed in version”, implement simple version compare (e.g. for dpkg) so you can report “affected” vs “fixed” instead of “unknown”.

**Priority:** Medium; improves adoption where Trivy isn’t allowed or is hard to install.

---

### 1.3 Secrets scanning robustness

**Current state:** Secrets scanning runs on extracted image layers; pattern-based.

**Enhancements:**

1. **Ensure extraction is used**
   - For both “image name” and “uploaded tar” flows, guarantee the same extraction path is used so secrets scanner gets a directory to scan. Add a test: upload tar with a fake secret file, assert one finding.

2. **Configurable patterns**
   - Allow a config file or env var to add custom regexes (e.g. internal secret format). Document format and example.

3. **False positive reduction**
   - Option to exclude paths (e.g. `*/test/*`, `*.test`) or add “allowed patterns” so known test fixtures don’t appear as findings.

**Priority:** Medium.

---

### 1.4 API and CLI

- **Root (/) response:** Return a small JSON (name, version, links to `/docs` and `/api/v1/health`) so API-only clients get consistent JSON; keep HTML for browser if you have a simple UI.
- **Scan response schema:** Document and stabilize the JSON schema for scan results (vulns, secrets, sbom, score) so CI can parse it reliably.
- **CLI:** Add `--format json` to scan command so scripts can consume output without parsing human-readable text.

---

## Part 2: NetSec-Cloud Enhancements

### 2.1 Deeper provider coverage (incremental)

**Current state:** AWS, Azure, GCP with storage, IAM, (optional) compute checks; compliance mapping to CIS, NIST, PCI-DSS, HIPAA.

**Enhancements (pick one or two per provider):**

1. **AWS**
   - **CloudTrail:** Check that CloudTrail is enabled and multi-region (or at least in primary region). Map to CIS/NIST.
   - **Config:** Check that AWS Config is enabled; optional: list non-compliant rules. Map to compliance.
   - **Lambda:** Optional: list functions without VPC or with broad IAM; flag public URLs if applicable.

2. **Azure**
   - **Key Vault:** List vaults; check soft-delete and purge protection; check access policies (e.g. no broad “all” access). Map to CIS/NIST.
   - **VM / App Service:** Optional: list VMs/plans; check disk encryption, HTTPS-only for App Service.

3. **GCP**
   - **Project IAM:** You have project-level IAM; add “binding with condition” checks (e.g. time-bound) and flag overly broad bindings.
   - **GKE:** Optional: list clusters; check legacy auth disabled, private cluster, etc. Map to CIS.

**Priority:** Do one “depth” check per provider (e.g. CloudTrail for AWS, Key Vault for Azure) and map to existing frameworks. Don’t add a new framework; extend mappings.

---

### 2.2 Identity and encryption validation

**Current state:** IAM/storage checks exist; encryption is partially covered (e.g. EBS encryption).

**Enhancements:**

1. **Identity**
   - **MFA:** AWS: root account MFA; Azure: conditional access / MFA for admin roles; GCP: enforce MFA for org (if API allows). Add as a “check” and map to CIS/NIST.
   - **Least privilege:** Add a “broad role” check: e.g. Owner/Contributor/Editor assigned to human users (not just service accounts). You already have some of this; document and ensure it’s in compliance mapping.

2. **Encryption**
   - **At rest:** For each provider, ensure every “storage” check includes “encryption at rest” (S3, Blob, GCS, EBS, RDS if you add it). Map to PCI-DSS/HIPAA.
   - **In transit:** Check that load balancers / app gateways enforce TLS; optional: TLS version and cipher checks. Map to same frameworks.

**Priority:** High for compliance storytelling; implement as additional checks and control IDs in existing mapping.

---

### 2.3 Compliance and API

1. **Export**
   - Add “export compliance report” (JSON/CSV) with findings + control IDs + framework so auditors can ingest it. Can be a new endpoint or a query param on existing scan/compliance response.

2. **Scan filters**
   - Allow “scan only these check types” and “only these regions” in API so large tenants can limit scope and cost.

3. **Pagination**
   - If scan result sets grow large, add pagination or “max findings per check” so responses stay bounded.

---

## Part 3: Cross-cutting

- **Observability:** Structured logging (JSON) and a few key metrics (e.g. scan duration, finding count per provider/check type) make operations and tuning easier.
- **Caching:** For cloud, cache “list” results (e.g. S3 buckets, IAM roles) for a short TTL so repeated scans don’t hammer APIs; document TTL and how to disable.
- **Rate limiting:** Respect cloud provider rate limits (e.g. AWS list throttling); add backoff and optional “slow” mode for large tenants.

---

## Summary

| Area | Top 1–2 enhancements |
|------|----------------------|
| **Container** | (1) Tar-only / upload path for image extraction so secrets and basic vuln work without Docker. (2) Optional CVE DB for BasicVulnerabilityScanner and clear “basic” vs “Trivy” in report. |
| **Cloud** | (1) One deeper check per provider (e.g. CloudTrail, Key Vault, project IAM conditions) and map to existing frameworks. (2) Explicit identity (MFA, broad roles) and encryption (at rest + in transit) checks with framework mapping. |

Implementing these in small steps will materially improve both scanners without rewriting them.
