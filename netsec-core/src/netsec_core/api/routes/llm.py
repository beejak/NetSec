"""LLM-powered analysis routes."""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from netsec_core.llm.analyzer import LLMAnalyzer, LLMAnalyzerLocal

router = APIRouter()


def get_llm_analyzer() -> LLMAnalyzer:
    """Get LLM analyzer instance."""
    try:
        # Try to use LLM if API key is available
        import os
        if os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY"):
            provider = "openai" if os.getenv("OPENAI_API_KEY") else "anthropic"
            return LLMAnalyzer(provider=provider)
        else:
            return LLMAnalyzerLocal()
    except Exception:
        return LLMAnalyzerLocal()


@router.post("/analyze-traffic")
async def analyze_traffic_llm(traffic_summary: Dict[str, Any]):
    """Analyze network traffic using LLM."""
    try:
        analyzer = get_llm_analyzer()
        result = analyzer.analyze_traffic(traffic_summary)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing traffic: {str(e)}",
        )


@router.post("/reduce-false-positives")
async def reduce_false_positives(
    findings: List[Dict[str, Any]],
    context: Optional[Dict[str, Any]] = None,
):
    """Reduce false positives in findings using LLM."""
    try:
        analyzer = get_llm_analyzer()
        filtered = analyzer.reduce_false_positives(findings, context)
        return {
            "original_count": len(findings),
            "filtered_count": len(filtered),
            "findings": filtered,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error reducing false positives: {str(e)}",
        )


@router.post("/generate-remediation")
async def generate_remediation(
    finding: Dict[str, Any],
    context: Optional[Dict[str, Any]] = None,
):
    """Generate remediation guidance using LLM."""
    try:
        analyzer = get_llm_analyzer()
        remediation = analyzer.generate_remediation(finding, context)
        return remediation
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating remediation: {str(e)}",
        )


@router.post("/explain-finding")
async def explain_finding(finding: Dict[str, Any]):
    """Generate natural language explanation of a finding."""
    try:
        analyzer = get_llm_analyzer()
        explanation = analyzer.explain_finding(finding)
        return {
            "finding_id": finding.get("finding_id"),
            "explanation": explanation,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error explaining finding: {str(e)}",
        )
