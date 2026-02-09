# Unit and Integration Testing

This document defines the **testing types** we use (unit, integration, API, CLI) and how to write and run them in the NetSec Toolkit.

---

## Test types (what they are)

| Type | What it means | Examples | Run with |
|------|----------------|----------|----------|
| **Unit** | Test one function or class in isolation. No network, no real cloud/DB. Use mocks if something talks to the outside. Fast. | Test `map_findings_to_cis()` with a list of findings; test `CloudScanner().get_summary()` with a dict. | `pytest -m unit` |
| **Integration** | Test several parts together, or code that talks to real (or mocked) external services. Slower, may need env vars or test data. | Test full scan flow with mocked boto3; test API + DB; test against a real container image. | `pytest -m integration` |
| **API** | Test HTTP endpoints (FastAPI). Usually use `TestClient` (no real server). Can be unit-like (fast) or integration-like (if they call real backends). | `client.get("/api/v1/health")`, `client.post("/api/v1/cloud/scan", json=...)`. | `pytest -m api` |
| **CLI** | Test Click commands. Invoke the CLI and check exit code and output. | `runner.invoke(cli, ["scan", "aws"])`. | `pytest -m cli` |

---

## How we mark tests

We use **pytest markers** so you can run only unit tests, or only integration, etc.

- **Unit**: `@pytest.mark.unit` — no external services, fast.
- **Integration**: `@pytest.mark.integration` — may use external services or heavier setup.
- **API**: `@pytest.mark.api` — uses the FastAPI `TestClient`.
- **CLI**: `@pytest.mark.cli` — uses the Click `CliRunner`.

A test can have more than one marker (e.g. `@pytest.mark.unit` and `@pytest.mark.api` if it’s a fast API test).

---

## Where to put tests

Each project has a `tests/` folder. You can either:

- **Option A (current)**: Put all tests in `tests/` and use **markers** to distinguish unit vs integration.
- **Option B**: Use subfolders and markers together:
  - `tests/unit/` — unit tests (and tag with `@pytest.mark.unit`).
  - `tests/integration/` — integration tests (and tag with `@pytest.mark.integration`).
  - `tests/` — API/CLI or mixed, with `@pytest.mark.api` / `@pytest.mark.cli`.

Both are valid. We use **markers** in all projects; subfolders are optional for clarity.

---

## How to run by type

From **inside** a project (e.g. `netsec-cloud`):

```bash
# Only unit tests (fast)
pytest -m unit -v

# Only integration tests
pytest -m integration -v

# Only API tests
pytest -m api -v

# Only CLI tests
pytest -m cli -v

# Everything except integration (typical for fast CI)
pytest -m "not integration" -v

# All tests
pytest -v
```

---

## Examples

### Unit test (no external calls)

```python
# tests/test_compliance.py (NetSec-Cloud)
import pytest
from netsec_cloud.compliance.mapping import map_findings_to_cis

@pytest.mark.unit
def test_map_empty_findings_to_cis():
    result = map_findings_to_cis([])
    assert result == []
```

### API test (TestClient, no real server)

```python
# tests/test_api.py (NetSec-Cloud)
import pytest

@pytest.mark.api
def test_health(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

### CLI test (invoke command, check output)

```python
# tests/test_cli.py
import pytest
from netsec_cloud.cli.main import cli

@pytest.mark.cli
def test_cli_help(cli_runner):
    result = cli_runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "scan" in result.output
```

### Integration test (marked as such; may mock or use real service)

```python
# tests/integration/test_scan_with_mock.py
import pytest
from unittest.mock import patch

@pytest.mark.integration
def test_scan_aws_with_mocked_boto():
    with patch("netsec_cloud.providers.aws.boto3") as mock_boto:
        # ... configure mock, run scan, assert
        pass
```

---

## Summary

| Goal | Command |
|------|--------|
| Run only **unit** tests | `pytest -m unit -v` |
| Run only **integration** tests | `pytest -m integration -v` |
| Run **API** tests | `pytest -m api -v` |
| Run **CLI** tests | `pytest -m cli -v` |
| Run **all except integration** (fast CI) | `pytest -m "not integration" -v` |
| Run **all** tests | `pytest -v` |

The **framework** is: pytest + markers (unit, integration, api, cli) + fixtures (client, cli_runner, scanner, etc.). Write tests, mark them, then run the layer you need.
