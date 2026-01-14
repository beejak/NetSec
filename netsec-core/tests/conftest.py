"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient

from netsec_core.api.main import app


@pytest.fixture
def client():
    """Create test client for FastAPI app."""
    return TestClient(app)


@pytest.fixture
def api_base_url():
    """Base URL for API testing."""
    return "http://localhost:8000"
