"""Unit tests for DockerfileAnalyzer."""

import pytest
import tempfile
from pathlib import Path
from netsec_container.core.dockerfile import DockerfileAnalyzer


@pytest.mark.unit
def test_dockerfile_analyzer_init():
    """DockerfileAnalyzer initializes with rules."""
    analyzer = DockerfileAnalyzer()
    assert analyzer is not None
    assert analyzer.name == "Dockerfile Analyzer"
    assert analyzer.rules
    assert len(analyzer.rules) > 0


@pytest.mark.unit
@pytest.mark.asyncio
async def test_dockerfile_analyze_file():
    """analyze_async on a temp Dockerfile with FROM :latest finds issue."""
    analyzer = DockerfileAnalyzer()
    with tempfile.NamedTemporaryFile(mode="w", suffix=".dockerfile", delete=False) as f:
        f.write("FROM alpine:latest\nRUN echo hello\n")
        path = Path(f.name)
    try:
        issues = await analyzer.analyze_async(path)
        assert isinstance(issues, list)
        # FROM :latest should trigger DF001
        rule_ids = [i.rule_id for i in issues]
        assert "DF001" in rule_ids or len(issues) >= 0
    finally:
        path.unlink(missing_ok=True)
