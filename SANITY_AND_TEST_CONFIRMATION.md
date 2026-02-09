# Sanity and Test Confirmation

This document confirms what sanity checks and tests exist across the NetSec Toolkit and that they have been run successfully.

---

## 1. What “sanity” covers

### NetSec-Cloud (`netsec-cloud/`)

| Check | Script / Command | What it does |
|-------|------------------|---------------|
| **Sanity script** | `python sanitize_and_test.py` | (1) Critical imports (scanner, providers, compliance, API), (2) Ruff lint on `src/` and `tests/`, (3) `run_tests.py`, (4) Pytest |
| **Verification** | `python run_tests.py` | Imports (including `netsec_cloud.compliance.mapping`), API routes (including `/api/v1/cloud/compliance/check`), provider/scanner structure, file layout |
| **Unit tests** | `python -m pytest tests/` | `test_providers.py`, `test_scanner.py`, `test_compliance.py` |

**Confirmed:** All of the above have been run; **exit code 0** for `sanitize_and_test.py` and for `pytest tests/`.

### NetSec-Core (`netsec-core/`)

| Check | Script / Command | What it does |
|-------|------------------|---------------|
| **Sanity script** | `python sanitize_and_test.py` | (1) Critical imports (API, DNS/SSL/network scanners, LLM, test_logger), (2) Ruff lint, (3) Verification script, (4) Pytest |
| **Verification** | `python run_tests.py` | Imports, API routes, CLI, scanner init, config/logging, file structure |
| **Unit tests** | `python -m pytest tests/` | Full test suite under `tests/` |

**Confirmed:** Sanity script and pytest have been run; **exit code 0** for both.

### NetSec-Container (`netsec-container/`)

| Check | Script / Command | What it does |
|-------|------------------|---------------|
| **Sanity script** | `python sanitize_and_test.py` | Imports, lint, verification, pytest |
| **Unit tests** | `python -m pytest tests/` | `test_imports.py`, `test_scanner.py` |

**Confirmed:** Sanity and pytest have been run; **exit code 0** for both.

---

## 2. Test suites (what “all sorts of tests” means)

- **Imports:** All critical modules (including new ones like `netsec_cloud.compliance.mapping`) are import-checked by the sanity/verification scripts.
- **Structure:** API routes, CLI, providers, scanner, and file layout are verified.
- **Unit tests (pytest):** Provider init, scanner, compliance mapping, AWS compute/Azure RBAC/GCP IAM return types, CIS/NIST mapping, etc.
- **Linting:** Ruff is run on `src/` and `tests/` as part of sanity (where the script is used).

No tests were skipped or disabled for the runs above; all executed with **exit code 0**.

---

## 3. How to re-run locally

From the repo root:

```bash
# NetSec-Cloud
cd netsec-cloud && pip install -e . && python sanitize_and_test.py && python -m pytest tests/ -v

# NetSec-Core
cd netsec-core && pip install -e . && python sanitize_and_test.py && python -m pytest tests/ -v

# NetSec-Container
cd netsec-container && pip install -e . && python sanitize_and_test.py && python -m pytest tests/ -v
```

Optional: in `netsec-cloud`, run `python run_sanity_report.py` to write a short sanity + pytest report to `sanity_report.txt`.

---

## 4. Summary

| Project         | Sanity run (exit 0) | Pytest run (exit 0) | Notes |
|----------------|---------------------|---------------------|--------|
| **NetSec-Cloud**   | Yes                 | Yes                 | Compliance and new IAM/RBAC code included in sanity imports and route checks. |
| **NetSec-Core**    | Yes                 | Yes                 | Full sanity and pytest. |
| **NetSec-Container** | Yes               | Yes                 | Imports, scanner, tests. |

**Conclusion:** Sanity has been done and all executed tests have cleared (exit code 0). You can re-run the commands in section 3 anytime to reproduce.

---

## 5. Testing framework

A **unified testing framework** is in place across all projects:

- **Shared fixtures**: `conftest.py` in each project provides `client` (FastAPI TestClient), and project-specific fixtures (e.g. `scanner` in Cloud, `container_scanner` in Container).
- **Pytest config**: Markers (`unit`, `integration`, `api`) and test paths are defined in each project’s `pyproject.toml` under `[tool.pytest.ini_options]`.
- **Dev deps**: pytest, pytest-cov, pytest-mock (Cloud), httpx (Core, Cloud) are in each project’s `[dev]` optional dependencies.

See **[TESTING.md](TESTING.md)** for how to run tests, use fixtures, and add new tests. See **[TESTING_FRAMEWORK_RESEARCH.md](TESTING_FRAMEWORK_RESEARCH.md)** for research and design choices.
