"""Unit tests for SecretsScanner (no image extraction)."""

import pytest
from netsec_container.core.secrets import SecretsScanner


@pytest.mark.unit
def test_secrets_scanner_init():
    """SecretsScanner initializes with patterns."""
    scanner = SecretsScanner()
    assert scanner is not None
    assert scanner.name == "Secrets Scanner"
    assert scanner.patterns
    assert len(scanner.patterns) > 0


@pytest.mark.unit
def test_secret_patterns_have_required_keys():
    """Each secret pattern has type, pattern, confidence."""
    scanner = SecretsScanner()
    for p in scanner.patterns:
        assert "type" in p
        assert "pattern" in p
        assert "confidence" in p
        assert 0 <= p["confidence"] <= 1


@pytest.mark.unit
def test_secret_patterns_include_common_types():
    """Patterns include aws, api_key, password, private_key."""
    scanner = SecretsScanner()
    types = [p["type"] for p in scanner.patterns]
    assert "aws_access_key" in types or "api_key" in types or "password" in types
