# NetSec Toolkit – Testing Framework

This document describes the **unified testing framework** used across NetSec-Core, NetSec-Cloud, and NetSec-Container.

- **Unit vs integration (what they are, how to run them)**: see **[UNIT_AND_INTEGRATION_TESTING.md](UNIT_AND_INTEGRATION_TESTING.md)**.
- **Feature coverage and gaps**: see **[TESTING_GAPS.md](TESTING_GAPS.md)**.
- **Plan (use cases, parallel execution)**: see **[COMPREHENSIVE_TESTING_FRAMEWORK.md](COMPREHENSIVE_TESTING_FRAMEWORK.md)**.

---

## Overview

- **Runner**: [pytest](https://pytest.org/)
- **Shared fixtures**: Defined in each project’s `tests/conftest.py` (e.g. `client` for API, `scanner` for Cloud).
- **Configuration**: Pytest options and markers in each project’s `pyproject.toml` under `[tool.pytest.ini_options]`.
- **Optional plugins**: pytest-cov (coverage), pytest-asyncio (async), pytest-mock (mocking).

For research and design choices, see **[TESTING_FRAMEWORK_RESEARCH.md](TESTING_FRAMEWORK_RESEARCH.md)**.

---

## Quick commands

From the **repository root**:

```bash
# Run one project
cd netsec-core && pip install -e ".[dev]" && pytest -v
cd netsec-cloud && pip install -e ".[dev]" && pytest -v
cd netsec-container && pip install -e ".[dev]" && pytest -v

# Run all three in parallel (after research/implementation)
python run_all_tests_parallel.py   # or ./run_all_tests_parallel.sh
```

With coverage (example for Core):

```bash
cd netsec-core && pytest --cov=netsec_core --cov-report=term-missing --cov-report=html
```

---

## Test structure per project

| Project            | tests/              | conftest.py fixtures     | Notes                          |
|--------------------|---------------------|---------------------------|--------------------------------|
| **netsec-core**    | test_*.py, integration/ | `client`, `api_base_url`, test logging | TestResultLogger hooks in conftest |
| **netsec-cloud**   | test_*.py           | `client`, `scanner`, `sample_scan_request` | API + scanner tests            |
| **netsec-container** | test_*.py         | `client`, `container_scanner` | API + scanner tests            |

---

## Fixtures

### NetSec-Core (`netsec-core/tests/conftest.py`)

- **client**: `TestClient(app)` for FastAPI.
- **api_base_url**: Base URL string for API tests.
- **cli_runner**: `CliRunner()` for Click CLI tests.
- Test result logging is wired via `pytest_runtest_makereport`.

### NetSec-Cloud (`netsec-cloud/tests/conftest.py`)

- **client**: `TestClient(app)` for `/api/v1/cloud/*` and `/api/v1/health`.
- **scanner**: `CloudScanner()` instance (no credentials).
- **sample_scan_request**: Minimal JSON body for scan API tests.
- **cli_runner**: `CliRunner()` for Click CLI tests.

### NetSec-Container (`netsec-container/tests/conftest.py`)

- **client**: `TestClient(app)` for `/api/v1/scan`, `/api/v1/health`, etc.
- **container_scanner**: `ContainerScanner()` instance.
- **cli_runner**: `CliRunner()` for Click CLI tests.

---

## Pytest markers

All projects register these markers (in `pyproject.toml`):

- **unit**: Fast tests, no external services. Run with: `pytest -m unit`
- **integration**: May use external services or heavier setup. Run with: `pytest -m integration`
- **api**: Tests that use the FastAPI TestClient. Run with: `pytest -m api`
- **cli**: Tests that use the Click CliRunner. Run with: `pytest -m cli`

Exclude integration in CI for speed:

```bash
pytest -m "not integration" -v
```

---

## Writing new tests

1. **Location**: Add `test_<module>.py` under the project’s `tests/` directory.
2. **Naming**: Use `test_<name>` for test functions; pytest discovers them automatically.
3. **Fixtures**: Request fixtures by name in the function signature, e.g. `def test_health(client):`.
4. **API tests**: Use the `client` fixture and assert on `response.status_code` and `response.json()`.
5. **Markers**: Add `@pytest.mark.unit` or `@pytest.mark.api` as needed.

Example (NetSec-Cloud):

```python
import pytest

@pytest.mark.api
def test_health(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

---

## Sanity and verification scripts

In addition to pytest, each project has:

- **sanitize_and_test.py**: Imports, lint (ruff), verification script, then pytest.
- **run_tests.py** (Core, Cloud): Structural checks (imports, API routes, file layout).

Run sanity before pushing:

```bash
cd netsec-cloud && python sanitize_and_test.py
```

See **[SANITY_AND_TEST_CONFIRMATION.md](SANITY_AND_TEST_CONFIRMATION.md)** and **[RUN_ALL_TESTS.md](RUN_ALL_TESTS.md)** for full details.

---

## Coverage

- **NetSec-Core**: Coverage is enabled by default in `addopts` (term + HTML report). Disable with `pytest -p no:cov` for a faster run.
- **NetSec-Cloud / NetSec-Container**: Run coverage explicitly:
  - `pytest --cov=netsec_cloud --cov-report=term-missing`
  - `pytest --cov=netsec_container --cov-report=term-missing`

---

## CI

GitHub Actions (or other CI) should:

1. Install the project with dev extras: `pip install -e ".[dev]"`.
2. Run pytest: `pytest -v` (or `pytest -m "not integration"` for speed).
3. Optionally run `sanitize_and_test.py` and/or coverage and fail on thresholds.

See each project’s `.github/workflows/ci.yml` for the current pipeline.
