"""Test that all modules can be imported."""

import pytest


def test_package_import():
    """Test that main package can be imported."""
    import netsec_container
    assert hasattr(netsec_container, '__version__')
    assert netsec_container.__version__ == "0.1.0"


def test_scanner_import():
    """Test that scanner can be imported."""
    from netsec_container.core.scanner import ContainerScanner
    assert ContainerScanner is not None


def test_results_import():
    """Test that results can be imported."""
    from netsec_container.core.results import ScanResults
    assert ScanResults is not None


def test_vulnerability_import():
    """Test that vulnerability scanner can be imported."""
    from netsec_container.core.vulnerability import VulnerabilityScanner
    assert VulnerabilityScanner is not None


def test_secrets_import():
    """Test that secrets scanner can be imported."""
    from netsec_container.core.secrets import SecretsScanner
    assert SecretsScanner is not None


def test_sbom_import():
    """Test that SBOM generator can be imported."""
    from netsec_container.core.sbom import SBOMGenerator
    assert SBOMGenerator is not None


def test_dockerfile_import():
    """Test that Dockerfile analyzer can be imported."""
    from netsec_container.core.dockerfile import DockerfileAnalyzer
    assert DockerfileAnalyzer is not None


def test_scoring_import():
    """Test that scoring system can be imported."""
    from netsec_container.core.scoring import RiskScorer
    assert RiskScorer is not None


def test_llm_import():
    """Test that LLM analyzer can be imported."""
    from netsec_container.llm.analyzer import LLMAnalyzer
    assert LLMAnalyzer is not None


def test_api_import():
    """Test that API can be imported."""
    from netsec_container.api.main import app
    assert app is not None


def test_cli_import():
    """Test that CLI can be imported."""
    from netsec_container.cli.main import cli
    assert cli is not None
