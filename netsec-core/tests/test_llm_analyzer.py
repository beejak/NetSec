"""Unit tests for LLMAnalyzer (mocked LLM calls)."""

from unittest.mock import patch, MagicMock
import pytest
from netsec_core.llm.analyzer import LLMAnalyzer


@pytest.mark.unit
def test_llm_analyzer_init():
    """LLMAnalyzer initializes with provider and model."""
    analyzer = LLMAnalyzer(provider="openai", model="gpt-3.5-turbo")
    assert analyzer.provider == "openai"
    assert analyzer.model == "gpt-3.5-turbo"
    assert analyzer._client is None


@pytest.mark.unit
def test_analyze_traffic_returns_analysis_and_timestamp():
    """analyze_traffic returns dict with analysis and timestamp when LLM succeeds."""
    analyzer = LLMAnalyzer(provider="openai", model="gpt-3.5-turbo")
    traffic_summary = {"packets": 100, "flows": 5}
    with patch.object(analyzer, "_call_llm", return_value="Security review: No critical issues."):
        result = analyzer.analyze_traffic(traffic_summary)
    assert "analysis" in result
    assert result["analysis"] == "Security review: No critical issues."
    assert "timestamp" in result


@pytest.mark.unit
def test_analyze_traffic_returns_error_on_failure():
    """analyze_traffic returns error and fallback when _call_llm raises."""
    analyzer = LLMAnalyzer(provider="openai", model="gpt-3.5-turbo")
    with patch.object(analyzer, "_call_llm", side_effect=Exception("API error")):
        result = analyzer.analyze_traffic({"packets": 10})
    assert "error" in result
    assert "API error" in result["error"]
    assert "fallback" in result


@pytest.mark.unit
def test_generate_remediation_returns_finding_id_and_remediation():
    """generate_remediation returns finding_id, remediation, generated_by when LLM succeeds."""
    analyzer = LLMAnalyzer(provider="openai", model="gpt-3.5-turbo")
    finding = {"finding_id": "test-1", "type": "xss", "severity": "high", "description": "Reflected XSS"}
    with patch.object(analyzer, "_call_llm", return_value="1. Sanitize input. 2. Use CSP."):
        result = analyzer.generate_remediation(finding)
    assert result["finding_id"] == "test-1"
    assert "remediation" in result
    assert result["remediation"] == "1. Sanitize input. 2. Use CSP."
    assert result["generated_by"] == "llm"
    assert "timestamp" in result


@pytest.mark.unit
def test_explain_finding_returns_string():
    """explain_finding returns string explanation when LLM succeeds."""
    analyzer = LLMAnalyzer(provider="openai", model="gpt-3.5-turbo")
    finding = {"type": "sql_injection", "severity": "critical", "description": "SQLi in login"}
    with patch.object(analyzer, "_call_llm", return_value="An attacker can inject SQL commands."):
        result = analyzer.explain_finding(finding)
    assert isinstance(result, str)
    assert "inject" in result
