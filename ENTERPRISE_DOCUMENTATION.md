# Enterprise-Class Documentation: What You Need

This document is an **unbiased view** of the documentation required to make the NetSec Toolkit **enterprise-class**: what exists, what’s missing, and what to add.

---

## 1. Documentation Checklist (Enterprise Bar)

| Document | Purpose | Status | Action |
|----------|---------|--------|--------|
| **README (root + per project)** | First impression; install & quick start | ✅ Done | Keep updated; link to other docs. |
| **API reference** | Contract for integrators; OpenAPI/Swagger | ⚠️ Partial | Expose `/docs`; add **API_REFERENCE.md** (overview + link to OpenAPI). |
| **Security & compliance** | What we check; which frameworks we map to | ⚠️ Partial | Add **SECURITY_AND_COMPLIANCE.md** (one place for all three products). |
| **Architecture** | How components fit; design decisions | ⚠️ Partial | Add **ARCHITECTURE.md** (high-level + links to existing diagrams). |
| **Operational runbook** | Deploy, configure, scale, logs, alerts | ❌ Missing | Add **RUNBOOK.md** (deploy, env vars, health, logs, troubleshooting). |
| **Changelog / release notes** | What changed; version history | ❌ Missing | Add **CHANGELOG.md**; use for every release. |
| **Support & SLA** | How to get help; SLA if commercial | ⚠️ Placeholder | Optional until you have paying customers. |
| **Testing** | How to run tests; what’s covered | ✅ Done | TESTING.md, TESTING_GAPS.md—keep current. |
| **Contributing** | How to contribute | ✅ Done | CONTRIBUTING.md—keep. |

---

## 2. What to Add (Concrete)

### 2.1 API reference (API_REFERENCE.md)

- **Purpose:** Single entry for “how do I call the APIs?”
- **Contents:**
  - Base URLs and versioning (e.g. `/api/v1/`).
  - Link to **interactive docs**: Core/Cloud/Container `/docs` (OpenAPI).
  - Short table: product → main endpoints (health, scan, compliance, etc.).
  - Auth (if any): API key, bearer, etc.
- **Where:** Root `API_REFERENCE.md`; each project can add “See also root API_REFERENCE.md” in its README.

### 2.2 Security & compliance (SECURITY_AND_COMPLIANCE.md)

- **Purpose:** One place for “what do we check?” and “what frameworks do we support?”
- **Contents:**
  - **NetSec-Core:** Network/DNS/SSL/traffic/anomaly/assets; no PII logging; optional LLM (bring-your-own-key).
  - **NetSec-Cloud:** Checks per provider (storage, IAM, compute, etc.); frameworks: CIS, NIST, PCI-DSS, HIPAA; how findings map to controls.
  - **NetSec-Container:** Image vulns, secrets, Dockerfile, SBOM; no runtime/K8s in MVP.
  - **Data handling:** What we do/don’t store; where scans run (on-prem vs cloud).
- **Where:** Root `SECURITY_AND_COMPLIANCE.md`.

### 2.3 Architecture (ARCHITECTURE.md)

- **Purpose:** High-level picture for architects and ops.
- **Contents:**
  - Diagram or list: Core / Cloud / Container; API, CLI, scanners, compliance.
  - Design principles (e.g. minimal deps, provider abstraction).
  - Links to existing diagrams (e.g. in netsec-core, netsec-cloud).
- **Where:** Root `ARCHITECTURE.md`.

### 2.4 Operational runbook (RUNBOOK.md)

- **Purpose:** “How do I run this in production?”
- **Contents:**
  - **Deployment:** Docker, systemd, or cloud (e.g. ECS, App Service)—one paragraph per option.
  - **Configuration:** Env vars (e.g. cloud creds, LLM keys, log level); config files if any.
  - **Health:** Health endpoints; what “healthy” means.
  - **Logging:** Log format, level, where they go.
  - **Scaling:** Stateless; horizontal scaling note.
  - **Troubleshooting:** Common failures (e.g. 401 cloud, Trivy missing, scapy missing) and fixes.
- **Where:** Root `RUNBOOK.md`; per-project README can link to it.

### 2.5 Changelog (CHANGELOG.md)

- **Purpose:** Version history and release notes.
- **Contents:**
  - Format: [Keep a Changelog](https://keepachangelog.com/) (Added / Changed / Fixed / Removed).
  - One section per version (e.g. 0.2.0, 0.1.0); date and high-level changes.
- **Where:** Root `CHANGELOG.md`. Tag releases in git; refer to CHANGELOG in release notes.

---

## 3. Where This Puts You

- **Today:** You have READMEs, testing docs, roadmap, and design docs. You’re **good for open source and early adopters**.
- **After adding the five above:** You have a **clear, single place** for API, security/compliance, architecture, operations, and changes. That is the **minimum for “enterprise-class” documentation**.
- **Later (if commercial):** Add support process, SLA, and formal security whitepaper as needed.

---

## 4. Order of Work

1. **CHANGELOG.md** – Quick win; start with current state and last few changes.
2. **API_REFERENCE.md** – Point to `/docs` and list main endpoints.
3. **SECURITY_AND_COMPLIANCE.md** – Collate what each product checks and which frameworks.
4. **ARCHITECTURE.md** – One-page overview + links to existing content.
5. **RUNBOOK.md** – Deploy, config, health, logs, troubleshooting.

Once these exist and are linked from the root README, the repo is in a **strong position** for enterprise evaluation.
