"""Risk scoring system for container security"""

from typing import List
from netsec_container.core.results import ScanResults, Vulnerability, Secret


class RiskScorer:
    """Calculate risk scores for container scans"""
    
    def __init__(self):
        # Severity weights
        self.severity_weights = {
            "critical": 10.0,
            "high": 7.0,
            "medium": 4.0,
            "low": 1.0,
            "info": 0.5,
        }
        
        # Secret type weights
        self.secret_weights = {
            "private_key": 10.0,
            "ssh_key": 10.0,
            "aws_secret_key": 9.0,
            "database_url": 8.0,
            "password": 7.0,
            "api_key": 6.0,
            "github_token": 5.0,
            "jwt_token": 4.0,
        }
    
    def calculate_score(self, results: ScanResults) -> float:
        """
        Calculate overall risk score (0-100)
        
        Args:
            results: ScanResults object
            
        Returns:
            Risk score (0-100)
        """
        score = 0.0
        
        # Vulnerability scoring
        vuln_score = self._calculate_vulnerability_score(results.vulnerabilities)
        
        # Secrets scoring
        secret_score = self._calculate_secrets_score(results.secrets)
        
        # Dockerfile issues scoring
        dockerfile_score = self._calculate_dockerfile_score(results.dockerfile_issues)
        
        # Combine scores (weighted)
        total_score = (vuln_score * 0.6) + (secret_score * 0.3) + (dockerfile_score * 0.1)
        
        # Normalize to 0-100
        score = min(100.0, total_score)
        
        # Set risk level
        results.risk_level = self._get_risk_level(score)
        
        return score
    
    def _calculate_vulnerability_score(self, vulnerabilities: List[Vulnerability]) -> float:
        """Calculate vulnerability risk score"""
        if not vulnerabilities:
            return 0.0
        
        score = 0.0
        
        for vuln in vulnerabilities:
            base_score = self.severity_weights.get(vuln.severity, 1.0)
            
            # Add CVSS score if available
            cvss_bonus = vuln.score / 10.0 if vuln.score > 0 else 0
            
            # Exploit available bonus
            exploit_bonus = 2.0 if vuln.exploit_available else 0
            
            vuln_score = base_score + cvss_bonus + exploit_bonus
            score += vuln_score
        
        # Cap at 100
        return min(100.0, score)
    
    def _calculate_secrets_score(self, secrets: List[Secret]) -> float:
        """Calculate secrets risk score"""
        if not secrets:
            return 0.0
        
        score = 0.0
        
        for secret in secrets:
            base_weight = self.secret_weights.get(secret.type, 5.0)
            confidence_multiplier = secret.confidence
            
            secret_score = base_weight * confidence_multiplier
            score += secret_score
        
        # Cap at 100
        return min(100.0, score)
    
    def _calculate_dockerfile_score(self, issues: List) -> float:
        """Calculate Dockerfile issues score"""
        if not issues:
            return 0.0
        
        score = 0.0
        
        for issue in issues:
            weight = self.severity_weights.get(issue.severity, 1.0)
            score += weight
        
        # Cap at 100
        return min(100.0, score)
    
    def _get_risk_level(self, score: float) -> str:
        """Get risk level from score"""
        if score >= 80:
            return "critical"
        elif score >= 60:
            return "high"
        elif score >= 40:
            return "medium"
        elif score >= 20:
            return "low"
        else:
            return "info"
