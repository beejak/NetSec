"""Pytest configuration and shared fixtures for NetSec-Cloud."""

import pytest

# Optional: FastAPI TestClient when testing API routes
try:
    from fastapi.testclient import TestClient
    from netsec_cloud.api.main import app
    HAS_API = True
except Exception:
    HAS_API = False


def _api_client():
    if HAS_API:
        return TestClient(app)
    return None


@pytest.fixture
def client():
    """FastAPI TestClient for API tests. Use for /api/v1/cloud/* and /api/v1/health."""
    c = _api_client()
    if c is None:
        pytest.skip("API app not available (missing dependencies)")
    return c


@pytest.fixture
def scanner():
    """CloudScanner instance for provider/scanner tests (no credentials)."""
    from netsec_cloud.scanner import CloudScanner
    return CloudScanner()


@pytest.fixture
def sample_scan_request():
    """Minimal scan request payload for API tests."""
    return {
        "provider": "aws",
        "credentials": {},
        "check_types": ["storage"],
    }


@pytest.fixture
def cli_runner():
    """Click CliRunner for CLI tests."""
    from click.testing import CliRunner
    return CliRunner()
