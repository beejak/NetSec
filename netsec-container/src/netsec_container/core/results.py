"""Scan results data structures"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional, Any


@dataclass
class Vulnerability:
    """Container vulnerability finding"""
    cve_id: str
    package: str
    version: str
    severity: str  # critical, high, medium, low
    score: float  # CVSS score
    description: str
    fixed_version: Optional[str] = None
    exploit_available: bool = False
    layer: Optional[str] = None


@dataclass
class Secret:
    """Secret finding"""
    type: str  # aws_key, api_key, password, etc.
    value: str  # Redacted/masked value
    file_path: str
    line_number: int
    confidence: float  # 0.0 to 1.0
    context: Optional[str] = None


@dataclass
class DockerfileIssue:
    """Dockerfile security issue"""
    rule_id: str
    severity: str
    description: str
    line_number: int
    recommendation: str


@dataclass
class SBOM:
    """Software Bill of Materials"""
    packages: List[Dict[str, Any]]
    format: str  # spdx, cyclonedx
    version: str


@dataclass
class LLMRemediation:
    """LLM-generated remediation guidance"""
    summary: str
    steps: List[str]
    code_examples: List[Dict[str, str]]
    priority: str
    estimated_time: Optional[str] = None


@dataclass
class ScanResults:
    """Complete scan results"""
    image: str
    scan_start: datetime
    scan_end: Optional[datetime] = None
    scan_duration: Optional[float] = None  # seconds
    
    # Findings
    vulnerabilities: List[Vulnerability] = field(default_factory=list)
    secrets: List[Secret] = field(default_factory=list)
    sbom: Optional[SBOM] = None
    dockerfile_issues: List[DockerfileIssue] = field(default_factory=list)
    
    # Scoring
    risk_score: float = 0.0  # 0-100
    risk_level: str = "unknown"  # critical, high, medium, low, info
    
    # LLM
    llm_remediation: Optional[LLMRemediation] = None
    
    # Metadata
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def get_vulnerabilities(self, severity: Optional[str] = None) -> List[Vulnerability]:
        """Get vulnerabilities, optionally filtered by severity"""
        if severity:
            return [v for v in self.vulnerabilities if v.severity == severity]
        return self.vulnerabilities
    
    def get_secrets(self) -> List[Secret]:
        """Get all secrets found"""
        return self.secrets
    
    def get_risk_score(self) -> float:
        """Get overall risk score"""
        return self.risk_score
    
    def get_risk_level(self) -> str:
        """Get risk level"""
        return self.risk_level
    
    def has_critical_issues(self) -> bool:
        """Check if scan found critical issues"""
        critical_vulns = [v for v in self.vulnerabilities if v.severity == "critical"]
        return len(critical_vulns) > 0 or self.risk_level == "critical"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert results to dictionary"""
        return {
            "image": self.image,
            "scan_start": self.scan_start.isoformat(),
            "scan_end": self.scan_end.isoformat() if self.scan_end else None,
            "scan_duration": self.scan_duration,
            "vulnerabilities": [
                {
                    "cve_id": v.cve_id,
                    "package": v.package,
                    "version": v.version,
                    "severity": v.severity,
                    "score": v.score,
                    "description": v.description,
                    "fixed_version": v.fixed_version,
                    "exploit_available": v.exploit_available,
                }
                for v in self.vulnerabilities
            ],
            "secrets": [
                {
                    "type": s.type,
                    "file_path": s.file_path,
                    "line_number": s.line_number,
                    "confidence": s.confidence,
                }
                for s in self.secrets
            ],
            "risk_score": self.risk_score,
            "risk_level": self.risk_level,
            "error": self.error,
        }
