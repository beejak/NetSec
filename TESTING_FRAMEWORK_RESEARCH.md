# Testing Framework Research – NetSec Toolkit

This document summarizes research on testing frameworks and libraries for the NetSec Toolkit (Core, Cloud, Container) and what has been implemented.

---

## 1. Goals

- **Unified approach**: Same testing style and tooling across Core, Cloud, and Container.
- **Cover use cases**: Unit tests (scanners, providers, compliance), API tests (FastAPI), CLI tests (Click), integration-style tests (with mocks where needed).
- **CI-friendly**: Fast, deterministic, no flaky tests; optional coverage and markers.
- **Maintainable**: Shared fixtures, clear structure, documentation.

---

## 2. Framework and Library Options

### 2.1 Test Runner: pytest

**Choice: pytest** (already in use across all three projects.)

- **Why**: De facto standard for Python; rich plugin ecosystem; fixtures, parametrization, markers; good FastAPI and Click support.
- **Alternatives considered**: `unittest` (less expressive, no shared fixtures by default); `nose2` (smaller ecosystem).
- **Verdict**: Keep pytest as the single test runner.

### 2.2 Coverage: pytest-cov

**Choice: pytest-cov** (coverage plugin for pytest.)

- **Why**: Integrates with pytest; produces terminal and HTML reports; CI can fail on coverage thresholds.
- **Usage**: `pytest --cov=netsec_core --cov-report=term-missing --cov-report=html` (or equivalent per project).
- **Verdict**: Add to all projects as part of the dev/testing stack; optional in default `pytest` run so local runs stay fast.

### 2.3 Async: pytest-asyncio

**Choice: pytest-asyncio** (for async tests.)

- **Why**: NetSec-Core and others may have async endpoints or helpers; FastAPI is async; asyncio mode must be configured.
- **Usage**: `@pytest.mark.asyncio` on async tests; `asyncio_mode = "auto"` or `"strict"` in config.
- **Verdict**: Already in Core/Container dev deps; ensure config is set so async tests run without boilerplate.

### 2.4 Mocking: unittest.mock / pytest-mock

**Choice: `unittest.mock` (stdlib) + optional `pytest-mock`.**

- **Why**: Mocking cloud SDKs (boto3, Azure, GCP) and network calls avoids real credentials and external services; pytest-mock adds `mocker` fixture and integrates with pytest.
- **Usage**: `from unittest.mock import patch, MagicMock` or `def test_foo(mocker): mocker.patch(...)`.
- **Verdict**: Use stdlib mock everywhere; add `pytest-mock` to dev deps for projects that benefit from `mocker` (e.g. Cloud).

### 2.5 API Testing: FastAPI TestClient

**Choice: FastAPI’s `TestClient`** (wraps Starlette/httpx.)

- **Why**: Official pattern; synchronous test code; no need to run a server; supports all HTTP methods and JSON.
- **Usage**: `from fastapi.testclient import TestClient; client = TestClient(app); response = client.get("/api/v1/health")`.
- **Verdict**: Use TestClient in shared fixture (`client` in `conftest.py`) for Core, Cloud, and Container API tests.

### 2.6 CLI Testing: Click CliRunner

**Choice: Click’s `CliRunner`.**

- **Why**: Official way to test Click apps; captures exit code and output; supports `isolated_filesystem()` for file operations.
- **Usage**: `from click.testing import CliRunner; runner = CliRunner(); result = runner.invoke(cli, ["scan", "aws"])`.
- **Verdict**: Add a `cli_runner` fixture in conftest where CLI is used (Core, Cloud, Container) for consistent CLI tests.

### 2.7 Property-Based / Fuzz: Hypothesis

**Not adopted for now.**

- **Why**: Hypothesis is powerful for finding edge cases but adds complexity and runtime; current tests are mostly structure and behavior checks.
- **Verdict**: Optional later for specific modules (e.g. parsers, validators); not part of the baseline framework.

### 2.8 Multi-Environment: tox / nox

**Not adopted for now.**

- **Why**: tox/nox are useful for matrix testing (e.g. multiple Python versions). CI can do that via a matrix job instead.
- **Verdict**: Rely on CI (e.g. GitHub Actions) for multi-version testing; keep local workflow as single-venv pytest.

### 2.9 Cloud SDK Mocking: moto (AWS), etc.

**Not adopted as a default.**

- **Why**: moto is great for AWS but adds weight and version coupling; current tests avoid real credentials by testing “no creds” or mocked clients.
- **Verdict**: Prefer `unittest.mock` to patch boto3/Azure/GCP clients in unit tests; consider moto later for integration-style AWS tests if needed.

---

## 3. What Was Implemented

### 3.1 Shared Test Infrastructure

| Project           | conftest.py                         | Pytest config (pyproject.toml)     |
|------------------|--------------------------------------|-------------------------------------|
| **NetSec-Core**  | Yes: `client`, `api_base_url`, test logging hook | Yes: testpaths, addopts (cov optional) |
| **NetSec-Cloud** | Added: `client`, `scanner` fixtures  | Added: testpaths, markers, addopts  |
| **NetSec-Container** | Added: `client` fixture          | Added: testpaths, markers, addopts |

### 3.2 Fixtures

- **client**: FastAPI `TestClient(app)` for API tests (Core, Cloud, Container).
- **scanner** (Cloud): `CloudScanner()` instance for provider/scanner tests.
- **cli_runner** (where added): Click `CliRunner()` for CLI tests.

### 3.3 Pytest Markers (optional)

- `unit`: Fast, no network/external deps.
- `integration`: May hit real services or heavier setup (use sparingly in CI).
- `api`: Tests that use TestClient.

Markers are registered so `pytest -m unit` works; CI can run `pytest -m "not integration"` for speed.

### 3.4 Dev Dependencies

- **Core**: pytest, pytest-cov, pytest-asyncio, httpx (already present).
- **Cloud**: Added pytest-cov, pytest-mock, httpx to dev deps.
- **Container**: Already has pytest, pytest-cov, pytest-asyncio; ensured pytest config is consistent.

### 3.5 Documentation

- **TESTING.md** (repo root): How to run tests, structure, fixtures, markers, coverage.
- **RUN_ALL_TESTS.md**: Updated with framework and new commands.
- **SANITY_AND_TEST_CONFIRMATION.md**: Updated to reference testing framework.
- **Project READMEs**: Testing sections point to TESTING.md and project-specific commands.

---

## 4. Is This Helpful?

**Yes.** Summary of benefits:

1. **Consistency**: Same runner (pytest), same patterns (conftest, TestClient, markers) across Core, Cloud, and Container.
2. **Less duplication**: Shared fixtures (e.g. `client`) avoid repeating TestClient setup in every test file.
3. **Easier onboarding**: New tests follow the same structure; TESTING.md explains how and where to add tests.
4. **CI-ready**: Markers and coverage options support fast default runs and optional coverage/HTML reports.
5. **Scalable**: Easy to add more fixtures (e.g. mock cloud clients), more markers, or Hypothesis later without changing the overall framework.

---

## 5. How to Run Tests (after implementation)

From repo root:

```bash
# NetSec-Core (with optional coverage)
cd netsec-core && pip install -e ".[dev]" && pytest -v

# NetSec-Cloud
cd netsec-cloud && pip install -e ".[dev]" && pytest -v

# NetSec-Container
cd netsec-container && pip install -e ".[dev]" && pytest -v
```

With coverage (per project):

```bash
pytest --cov=netsec_<project> --cov-report=term-missing --cov-report=html
```

Unit-only (if markers are used):

```bash
pytest -m unit -v
```

---

## 6. References

- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/) – TestClient
- [Click Testing](https://click.palletsprojects.com/en/stable/testing/) – CliRunner
- [pytest Fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)
- [pytest Parametrize](https://docs.pytest.org/how-to/parametrize.html)
- [pytest-cov](https://pytest-cov.readthedocs.io/) – Coverage plugin
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/) – Async tests
