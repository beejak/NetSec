"""LLM-powered security analysis and remediation"""

import asyncio
import logging
from typing import Optional, Dict, Any

from netsec_container.core.results import ScanResults, LLMRemediation

logger = logging.getLogger(__name__)


class LLMAnalyzer:
    """LLM-powered security analysis and remediation"""
    
    def __init__(self, provider: str = "openai", model: str = "gpt-4"):
        """
        Initialize LLM analyzer
        
        Args:
            provider: LLM provider (openai, anthropic, local)
            model: Model name
        """
        self.provider = provider
        self.model = model
        self.client = self._initialize_client()
    
    def _initialize_client(self):
        """Initialize LLM client"""
        if self.provider == "openai":
            try:
                from openai import AsyncOpenAI
                return AsyncOpenAI()
            except ImportError:
                logger.error("OpenAI library not installed. Install with: pip install openai")
                return None
        elif self.provider == "anthropic":
            try:
                from anthropic import AsyncAnthropic
                return AsyncAnthropic()
            except ImportError:
                logger.error("Anthropic library not installed. Install with: pip install anthropic")
                return None
        else:
            logger.warning(f"Unknown LLM provider: {self.provider}")
            return None
    
    async def analyze_and_remediate(self, results: ScanResults) -> Optional[LLMRemediation]:
        """
        Analyze scan results and generate remediation guidance
        
        Args:
            results: ScanResults object
            
        Returns:
            LLMRemediation object or None
        """
        if not self.client:
            return None
        
        try:
            prompt = self._build_remediation_prompt(results)
            
            if self.provider == "openai":
                response = await self._call_openai(prompt)
            elif self.provider == "anthropic":
                response = await self._call_anthropic(prompt)
            else:
                return None
            
            return self._parse_remediation_response(response)
        
        except Exception as e:
            logger.error(f"LLM analysis error: {e}", exc_info=True)
            return None
    
    def _build_remediation_prompt(self, results: ScanResults) -> str:
        """Build prompt for LLM remediation"""
        prompt = f"""You are a container security expert. Analyze these scan results and provide remediation guidance.

Container Image: {results.image}
Risk Score: {results.risk_score}/100
Risk Level: {results.risk_level}

Vulnerabilities Found: {len(results.vulnerabilities)}
"""
        
        if results.vulnerabilities:
            prompt += "\nTop Vulnerabilities:\n"
            for vuln in results.vulnerabilities[:10]:  # Top 10
                prompt += f"- {vuln.cve_id} ({vuln.severity}): {vuln.description}\n"
                if vuln.fixed_version:
                    prompt += f"  Fixed in: {vuln.fixed_version}\n"
        
        if results.secrets:
            prompt += f"\nSecrets Found: {len(results.secrets)}\n"
            for secret in results.secrets[:5]:  # Top 5
                prompt += f"- {secret.type} in {secret.file_path}:{secret.line_number}\n"
        
        prompt += """
Provide:
1. A brief summary of the security issues
2. Step-by-step remediation steps (prioritized)
3. Code examples or configuration fixes where applicable
4. Estimated time to fix
5. Priority level (critical, high, medium, low)

Format your response as JSON with keys: summary, steps (array), code_examples (array of {language, code}), priority, estimated_time.
"""
        return prompt
    
    async def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a container security expert providing remediation guidance."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content
    
    async def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic API"""
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
        return response.content[0].text
    
    def _parse_remediation_response(self, response: str) -> LLMRemediation:
        """Parse LLM response into LLMRemediation object"""
        import json
        import re
        
        # Try to extract JSON from response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group(0))
                return LLMRemediation(
                    summary=data.get("summary", ""),
                    steps=data.get("steps", []),
                    code_examples=data.get("code_examples", []),
                    priority=data.get("priority", "medium"),
                    estimated_time=data.get("estimated_time"),
                )
            except json.JSONDecodeError:
                pass
        
        # Fallback: parse as text
        lines = response.split("\n")
        summary = lines[0] if lines else ""
        steps = [line.strip() for line in lines[1:] if line.strip() and line.strip().startswith(("-", "1.", "2.", "3."))]
        
        return LLMRemediation(
            summary=summary,
            steps=steps[:10],  # Limit to 10 steps
            code_examples=[],
            priority="medium",
        )
