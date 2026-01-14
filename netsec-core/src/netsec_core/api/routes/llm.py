"""LLM-powered analysis routes."""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from netsec_core.llm.analyzer import LLMAnalyzer, LLMAnalyzerLocal

router = APIRouter()


def get_llm_analyzer(
    provider: Optional[str] = None,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> LLMAnalyzer:
    """
    Get LLM analyzer instance with bring-your-own-key support.
    
    Args:
        provider: LLM provider (openai, anthropic, ollama, lmstudio, vllm, huggingface)
        model: Model name to use
        api_key: API key for cloud providers (optional, can use env vars)
        base_url: Base URL for local models (optional)
    
    Returns:
        LLMAnalyzer instance or LLMAnalyzerLocal as fallback
    """
    try:
        import os
        
        # Determine provider
        if provider:
            selected_provider = provider
        elif os.getenv("LLM_PROVIDER"):
            selected_provider = os.getenv("LLM_PROVIDER")
        elif os.getenv("OPENAI_API_KEY"):
            selected_provider = "openai"
        elif os.getenv("ANTHROPIC_API_KEY"):
            selected_provider = "anthropic"
        elif os.getenv("OLLAMA_BASE_URL"):
            selected_provider = "ollama"
        elif os.getenv("LMSTUDIO_BASE_URL"):
            selected_provider = "lmstudio"
        else:
            selected_provider = None
        
        # Determine model
        selected_model = model or os.getenv("LLM_MODEL", "gpt-3.5-turbo")
        
        # Determine base URL
        selected_base_url = base_url or os.getenv("LLM_BASE_URL")
        
        # Create analyzer
        if selected_provider:
            return LLMAnalyzer(
                provider=selected_provider,
                model=selected_model,
                api_key=api_key,
                base_url=selected_base_url,
            )
        else:
            return LLMAnalyzerLocal()
    except Exception:
        return LLMAnalyzerLocal()


@router.post("/analyze-traffic")
async def analyze_traffic_llm(
    traffic_summary: Dict[str, Any],
    provider: Optional[str] = None,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
):
    """
    Analyze network traffic using LLM.
    
    Supports bring-your-own-key and local models.
    """
    try:
        analyzer = get_llm_analyzer(
            provider=provider,
            model=model,
            api_key=api_key,
            base_url=base_url,
        )
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
    provider: Optional[str] = None,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
):
    """Reduce false positives in findings using LLM."""
    try:
        analyzer = get_llm_analyzer(
            provider=provider,
            model=model,
            api_key=api_key,
            base_url=base_url,
        )
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
    provider: Optional[str] = None,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
):
    """Generate remediation guidance using LLM."""
    try:
        analyzer = get_llm_analyzer(
            provider=provider,
            model=model,
            api_key=api_key,
            base_url=base_url,
        )
        remediation = analyzer.generate_remediation(finding, context)
        return remediation
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating remediation: {str(e)}",
        )


@router.post("/explain-finding")
async def explain_finding(
    finding: Dict[str, Any],
    provider: Optional[str] = None,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
):
    """Generate natural language explanation of a finding."""
    try:
        analyzer = get_llm_analyzer(
            provider=provider,
            model=model,
            api_key=api_key,
            base_url=base_url,
        )
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
