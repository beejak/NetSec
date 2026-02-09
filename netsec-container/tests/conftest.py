"""Pytest configuration and shared fixtures for NetSec-Container."""

import pytest

try:
    from fastapi.testclient import TestClient
    from netsec_container.api.main import app
    HAS_API = True
except Exception:
    HAS_API = False


@pytest.fixture
def client():
    """FastAPI TestClient for API tests. Use for /api/v1/scan, /api/v1/health, etc."""
    if not HAS_API:
        pytest.skip("API app not available (missing dependencies)")
    return TestClient(app)


@pytest.fixture
def container_scanner():
    """ContainerScanner instance for core scanner tests."""
    from netsec_container.core.scanner import ContainerScanner
    return ContainerScanner()


@pytest.fixture
def cli_runner():
    """Click CliRunner for CLI tests."""
    from click.testing import CliRunner
    return CliRunner()
