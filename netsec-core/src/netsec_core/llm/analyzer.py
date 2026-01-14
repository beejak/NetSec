"""LLM-powered security analysis with support for cloud and local models."""

from typing import Dict, Any, List, Optional
import os
import json


class LLMAnalyzer:
    """LLM-powered analyzer for security findings and remediation.
    
    Supports:
    - Cloud providers: OpenAI, Anthropic (bring your own API key)
    - Local providers: Ollama, LM Studio, vLLM, HuggingFace Transformers
    """

    def __init__(
        self,
        provider: str = "openai",
        model: str = "gpt-3.5-turbo",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        """
        Initialize LLM Analyzer.

        Args:
            provider: LLM provider ("openai", "anthropic", "ollama", "lmstudio", "vllm", "huggingface")
            model: Model name to use (e.g., "gpt-3.5-turbo", "llama2", "mistral")
            api_key: API key for cloud providers (optional, can use env vars)
            base_url: Base URL for local/self-hosted models (e.g., "http://localhost:11434" for Ollama)
        """
        self.provider = provider.lower()
        self.model = model
        self.base_url = base_url
        
        # API key handling - support bring your own key
        if api_key:
            self.api_key = api_key
        elif self.provider == "openai":
            self.api_key = os.getenv("OPENAI_API_KEY")
        elif self.provider == "anthropic":
            self.api_key = os.getenv("ANTHROPIC_API_KEY")
        elif self.provider in ["ollama", "lmstudio", "vllm"]:
            # Local models don't need API keys
            self.api_key = None
        else:
            self.api_key = None
        
        self._client = None

    def _get_client(self):
        """Get LLM client based on provider."""
        if self._client is not None:
            return self._client

        if self.provider == "openai":
            try:
                import openai
                if not self.api_key:
                    raise ValueError(
                        "OpenAI API key not provided. Set OPENAI_API_KEY env var or pass api_key parameter"
                    )
                # Support custom base URL for OpenAI-compatible APIs
                client_kwargs = {"api_key": self.api_key}
                if self.base_url:
                    client_kwargs["base_url"] = self.base_url
                self._client = openai.OpenAI(**client_kwargs)
                return self._client
            except ImportError:
                raise ImportError("openai package not installed. Install with: pip install openai")

        elif self.provider == "anthropic":
            try:
                import anthropic
                if not self.api_key:
                    raise ValueError(
                        "Anthropic API key not provided. Set ANTHROPIC_API_KEY env var or pass api_key parameter"
                    )
                self._client = anthropic.Anthropic(api_key=self.api_key)
                return self._client
            except ImportError:
                raise ImportError("anthropic package not installed. Install with: pip install anthropic")

        elif self.provider == "ollama":
            # Ollama uses OpenAI-compatible API
            try:
                import openai
                base_url = self.base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
                self._client = openai.OpenAI(
                    api_key="ollama",  # Ollama doesn't require real API key
                    base_url=base_url
                )
                return self._client
            except ImportError:
                raise ImportError("openai package required for Ollama. Install with: pip install openai")

        elif self.provider == "lmstudio":
            # LM Studio uses OpenAI-compatible API
            try:
                import openai
                base_url = self.base_url or os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
                self._client = openai.OpenAI(
                    api_key="lm-studio",  # LM Studio doesn't require real API key
                    base_url=base_url
                )
                return self._client
            except ImportError:
                raise ImportError("openai package required for LM Studio. Install with: pip install openai")

        elif self.provider == "vllm":
            # vLLM uses OpenAI-compatible API
            try:
                import openai
                base_url = self.base_url or os.getenv("VLLM_BASE_URL", "http://localhost:8000/v1")
                self._client = openai.OpenAI(
                    api_key="vllm",  # vLLM doesn't require real API key
                    base_url=base_url
                )
                return self._client
            except ImportError:
                raise ImportError("openai package required for vLLM. Install with: pip install openai")

        elif self.provider == "huggingface":
            # HuggingFace Transformers (local inference)
            try:
                from transformers import pipeline
                # This will be handled differently in _call_llm
                self._client = "huggingface"  # Placeholder
                return self._client
            except ImportError:
                raise ImportError(
                    "transformers package not installed. Install with: pip install transformers torch"
                )

        else:
            raise ValueError(
                f"Unsupported provider: {self.provider}. "
                f"Supported: openai, anthropic, ollama, lmstudio, vllm, huggingface"
            )

    def analyze_traffic(self, traffic_summary: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze network traffic using LLM.

        Args:
            traffic_summary: Summary of network traffic

        Returns:
            LLM analysis results
        """
        prompt = f"""
        Analyze the following network traffic summary and identify any security concerns:
        
        {traffic_summary}
        
        Provide:
        1. Security concerns identified
        2. Risk level assessment
        3. Recommended actions
        """

        try:
            analysis = self._call_llm(prompt)
            return {
                "analysis": analysis,
                "timestamp": self._get_timestamp(),
            }
        except Exception as e:
            return {
                "error": str(e),
                "fallback": "LLM analysis unavailable, using rule-based analysis",
            }

    def reduce_false_positives(
        self,
        findings: List[Dict[str, Any]],
        context: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Reduce false positives in security findings using LLM.

        Args:
            findings: List of security findings
            context: Additional context about the environment

        Returns:
            Filtered findings with false positives removed
        """
        if not findings:
            return []

        prompt = f"""
        Review the following security findings and identify false positives:
        
        Findings:
        {self._format_findings(findings)}
        
        Context: {context or "No additional context"}
        
        For each finding, determine if it's a false positive. Return only legitimate security issues.
        """

        try:
            filtered = self._call_llm(prompt)
            # Parse LLM response and filter findings
            # This is a simplified version - in production, would parse structured response
            return findings  # Placeholder - would implement actual filtering
        except Exception:
            # Fallback to rule-based filtering
            return self._rule_based_filter(findings)

    def generate_remediation(
        self,
        finding: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Generate remediation guidance using LLM.

        Args:
            finding: Security finding
            context: Additional context

        Returns:
            Remediation guidance
        """
        prompt = f"""
        Generate detailed remediation steps for the following security finding:
        
        Finding Type: {finding.get('type', 'unknown')}
        Severity: {finding.get('severity', 'unknown')}
        Description: {finding.get('description', '')}
        
        Context: {context or "No additional context"}
        
        Provide:
        1. Immediate mitigation steps
        2. Short-term remediation
        3. Long-term prevention
        4. Verification steps
        """

        try:
            remediation = self._call_llm(prompt)
            return {
                "finding_id": finding.get("finding_id", ""),
                "remediation": remediation,
                "generated_by": "llm",
                "timestamp": self._get_timestamp(),
            }
        except Exception:
            # Fallback to rule-based remediation
            return self._rule_based_remediation(finding)

    def explain_finding(self, finding: Dict[str, Any]) -> str:
        """
        Generate natural language explanation of a finding.

        Args:
            finding: Security finding

        Returns:
            Natural language explanation
        """
        prompt = f"""
        Explain the following security finding in simple, clear language:
        
        Type: {finding.get('type', 'unknown')}
        Severity: {finding.get('severity', 'unknown')}
        Description: {finding.get('description', '')}
        
        Provide a clear explanation that a non-technical person can understand.
        """

        try:
            explanation = self._call_llm(prompt)
            return explanation
        except Exception:
            return finding.get("description", "No explanation available")

    def _call_llm(self, prompt: str) -> str:
        """Call LLM with prompt."""
        if self.provider in ["openai", "ollama", "lmstudio", "vllm"]:
            # OpenAI-compatible API
            client = self._get_client()
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a cybersecurity expert."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1000,
                temperature=0.7,
            )
            return response.choices[0].message.content

        elif self.provider == "anthropic":
            client = self._get_client()
            response = client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt},
                ],
            )
            return response.content[0].text

        elif self.provider == "huggingface":
            # Local HuggingFace model
            try:
                from transformers import pipeline
                generator = pipeline(
                    "text-generation",
                    model=self.model,
                    device_map="auto",
                )
                full_prompt = f"You are a cybersecurity expert.\n\n{prompt}"
                result = generator(
                    full_prompt,
                    max_length=len(full_prompt.split()) + 200,
                    num_return_sequences=1,
                    temperature=0.7,
                )
                return result[0]["generated_text"].replace(full_prompt, "").strip()
            except Exception as e:
                raise RuntimeError(f"Error calling HuggingFace model: {e}")

        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def _format_findings(self, findings: List[Dict[str, Any]]) -> str:
        """Format findings for LLM prompt."""
        formatted = []
        for i, finding in enumerate(findings, 1):
            formatted.append(
                f"{i}. {finding.get('type', 'unknown')} - {finding.get('severity', 'unknown')}: {finding.get('description', '')}"
            )
        return "\n".join(formatted)

    def _rule_based_filter(self, findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rule-based false positive filtering (fallback)."""
        filtered = []
        for finding in findings:
            # Simple rule: keep high/critical severity findings
            severity = finding.get("severity", "").lower()
            if severity in ["high", "critical"]:
                filtered.append(finding)
            # Keep medium if it's a known important type
            elif severity == "medium" and finding.get("type") in [
                "dns_tunneling",
                "weak_cipher",
                "certificate_expired",
            ]:
                filtered.append(finding)
        return filtered

    def _rule_based_remediation(self, finding: Dict[str, Any]) -> Dict[str, Any]:
        """Rule-based remediation (fallback)."""
        finding_type = finding.get("type", "")
        remediation_templates = {
            "dns_tunneling": {
                "immediate": "Block suspicious DNS queries",
                "short_term": "Implement DNS filtering and monitoring",
                "long_term": "Deploy DNS security solution",
            },
            "weak_cipher": {
                "immediate": "Disable weak ciphers",
                "short_term": "Update SSL/TLS configuration",
                "long_term": "Implement strong cipher policies",
            },
            "certificate_expired": {
                "immediate": "Renew certificate immediately",
                "short_term": "Set up certificate monitoring",
                "long_term": "Implement automated certificate management",
            },
        }

        template = remediation_templates.get(finding_type, {
            "immediate": "Review and address the security issue",
            "short_term": "Implement appropriate security controls",
            "long_term": "Establish ongoing monitoring",
        })

        return {
            "finding_id": finding.get("finding_id", ""),
            "remediation": template,
            "generated_by": "rule_based",
            "timestamp": self._get_timestamp(),
        }

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat()


class LLMAnalyzerLocal:
    """Local LLM analyzer (no API required)."""

    def __init__(self):
        """Initialize local analyzer."""
        pass

    def analyze_traffic(self, traffic_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze traffic using rule-based methods."""
        return {
            "analysis": "Rule-based analysis (LLM not available)",
            "timestamp": self._get_timestamp(),
        }

    def reduce_false_positives(self, findings: List[Dict[str, Any]], context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Filter false positives using rules."""
        # Simple filtering logic
        return [f for f in findings if f.get("severity", "").lower() in ["high", "critical"]]

    def generate_remediation(self, finding: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate remediation using templates."""
        from netsec_core.remediation.guide import RemediationGuide
        guide = RemediationGuide()
        return guide.get_remediation(finding.get("type", ""), finding)

    def explain_finding(self, finding: Dict[str, Any]) -> str:
        """Explain finding in simple terms."""
        return finding.get("description", "No explanation available")

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat()
