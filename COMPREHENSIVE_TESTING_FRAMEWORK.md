# Comprehensive Testing Framework – Plan

This document defines a **comprehensive testing framework** for the NetSec Toolkit (Core, Cloud, Container). It is designed so that implementation can **run in parallel** once research and design are done—both across projects (Core / Cloud / Container in parallel) and within a project (pytest-xdist).

---

## 1. Use cases we cover

| Use case | Project(s) | Test type | How |
|----------|------------|-----------|-----|
| **API endpoints** | Core, Cloud, Container | API | FastAPI `TestClient`; `client` fixture |
| **CLI commands** | Core, Cloud, Container | CLI | Click `CliRunner`; `cli_runner` fixture |
| **Scanners / engines** | All | Unit | Direct instantiation; mocked I/O where needed |
| **Cloud providers** (AWS/Azure/GCP) | Cloud | Unit + optional integration | Mocked clients (no creds); optional moto later |
| **Compliance mapping** | Cloud | Unit | `map_findings_to_cis`, `map_findings_to_framework` |
| **Container scan** (secrets, vulns) | Container | Unit + integration | Mocked Docker/registry; optional real image in CI |
| **LLM / remediation** | Core, Container | Unit | Mocked LLM client or skip when no key |
| **Sanity / smoke** | All | Script | `sanitize_and_test.py`, `run_tests.py` |
| **Coverage** | All | Coverage | pytest-cov; optional thresholds in CI |

---

## 2. Test layers

| Layer | Purpose | Run when | Parallel |
|-------|---------|----------|----------|
| **Unit** | Fast, no external services; markers `unit` | Every commit, CI | Yes (pytest-xdist per project) |
| **API** | HTTP endpoints; marker `api` | Every commit, CI | Yes |
| **CLI** | Click commands; marker `cli` | Every commit, CI | Yes |
| **Integration** | Real/mocked external deps; marker `integration` | CI or nightly | Optional; can exclude in fast path |
| **Sanity** | Imports, lint, structure | CI, pre-push | Yes (per project in parallel) |

---

## 3. Parallel execution

### 3.1 Across projects (CI)

Run **Core**, **Cloud**, and **Container** test suites **in parallel** as separate jobs:

- **Option A**: Single repo, one workflow with a **matrix** or **multiple jobs** (e.g. `test-core`, `test-cloud`, `test-container`) so all three run at the same time.
- **Option B**: Keep per-project workflows under `netsec-core/.github`, etc.; each runs on its own path; CI still parallel by repo/path if configured.

Recommended: **one root workflow** at repo root that runs three jobs in parallel (see section 6).

### 3.2 Within a project (pytest-xdist)

For large test suites, run pytest with **pytest-xdist** to use multiple CPUs:

```bash
pytest -n auto -v
```

- Add `pytest-xdist` to each project’s `[dev]` optional deps.
- Use `-n auto` in CI or locally for parallel workers; omit for debugging.

---

## 4. Fixtures and conventions (recap + extensions)

| Fixture | Project | Purpose |
|---------|---------|---------|
| `client` | Core, Cloud, Container | FastAPI `TestClient(app)` |
| `scanner` | Cloud | `CloudScanner()` |
| `container_scanner` | Container | `ContainerScanner()` |
| `cli_runner` | Core, Cloud, Container | Click `CliRunner()` (add where missing) |
| `sample_scan_request` | Cloud | Minimal scan JSON body |

All projects:

- Use **markers**: `unit`, `api`, `cli`, `integration`.
- Use **conftest.py** for shared fixtures.
- Use **pyproject.toml** `[tool.pytest.ini_options]` for testpaths, markers, addopts.

---

## 5. Implementation phases (can run in parallel after research)

Once this plan is agreed, the following can be done **in parallel** by different people or in parallel CI jobs:

| Phase | Scope | Deliverable |
|-------|--------|-------------|
| **A. Core** | netsec-core | Add `cli_runner` fixture; tag tests with `unit`/`api`/`cli`; add pytest-xdist; ensure CI runs unit+api+cli |
| **B. Cloud** | netsec-cloud | Add `cli_runner`; tag tests; add pytest-xdist; optional moto-based AWS tests (separate job/marker) |
| **C. Container** | netsec-container | Add `cli_runner`; tag tests; add pytest-xdist; add integration tests for scan (mocked or real image) |
| **D. Root CI** | Repo root | Single workflow that runs Core, Cloud, Container test jobs in parallel; optional coverage upload |
| **E. Scripts** | Repo root | `run_all_tests_parallel.sh` / `.py` / `.bat` to run all three test suites in parallel locally |

Phases A, B, C can run in parallel; D and E depend only on the plan, not on A/B/C.

---

## 6. Root CI workflow (run all three in parallel)

Example structure for `.github/workflows/ci.yml` at **repo root**:

```yaml
name: NetSec Toolkit CI

on:
  push:
    branches: [ main, master, develop ]
  pull_request:
    branches: [ main, master, develop ]

jobs:
  test-core:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: netsec-core
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -e ".[dev]"
      - run: pytest -v -m "not integration"

  test-cloud:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: netsec-cloud
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -e ".[dev]"
      - run: pytest -v -m "not integration"

  test-container:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: netsec-container
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -e ".[dev]"
      - run: pytest -v -m "not integration"
```

No `needs:` between jobs → all three run **in parallel**.

---

## 7. Local: run all tests in parallel

Use the script at repo root:

- **Linux/macOS**: `./run_all_tests_parallel.sh`
- **Windows**: `run_all_tests_parallel.bat`
- **Python**: `python run_all_tests_parallel.py`

These run `pytest` (or `sanitize_and_test.py` + pytest) for Core, Cloud, and Container in **parallel** (subprocesses), then report pass/fail.

---

## 8. Summary

| Item | Status |
|------|--------|
| Use cases defined | Yes (API, CLI, scanners, cloud, compliance, container, LLM, sanity) |
| Test layers (unit, api, cli, integration) | Yes |
| Parallel across projects | Yes (root CI + local script) |
| Parallel within project | Yes (pytest-xdist) |
| Fixtures (client, scanner, cli_runner) | client/scanner done; cli_runner to add |
| Implementation phases | A–E; A/B/C can run in parallel once research is done |

Once research is complete, phases A–E can proceed in parallel as described above.
