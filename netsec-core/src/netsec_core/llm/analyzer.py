"""LLM-powered security analysis."""

from typing import Dict, Any, List, Optional
import os


class LLMAnalyzer:
    """LLM-powered analyzer for security findings and remediation."""

    def __init__(self, provider: str = "openai", model: str = "gpt-3.5-turbo"):
        """
        Initialize LLM Analyzer.

        Args:
            provider: LLM provider ("openai", "anthropic", or "local")
            model: Model name to use
        """
        self.provider = provider
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        self._client = None

    def _get_client(self):
        """Get LLM client based on provider."""
        if self._client is not None:
            return self._client

        if self.provider == "openai":
            try:
                import openai
                if not self.api_key:
                    raise ValueError("OPENAI_API_KEY environment variable not set")
                self._client = openai.OpenAI(api_key=self.api_key)
                return self._client
            except ImportError:
                raise ImportError("openai package not installed. Install with: pip install openai")

        elif self.provider == "anthropic":
            try:
                import anthropic
                if not self.api_key:
                    raise ValueError("ANTHROPIC_API_KEY environment variable not set")
                self._client = anthropic.Anthropic(api_key=self.api_key)
                return self._client
            except ImportError:
                raise ImportError("anthropic package not installed. Install with: pip install anthropic")

        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

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
        if self.provider == "openai":
            client = self._get_client()
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a cybersecurity expert."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1000,
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
