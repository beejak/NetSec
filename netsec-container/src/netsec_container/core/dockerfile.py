"""Dockerfile security analyzer"""

import asyncio
import logging
from pathlib import Path
from typing import List, Optional, Union

from netsec_container.core.results import DockerfileIssue

logger = logging.getLogger(__name__)


class DockerfileAnalyzer:
    """Analyze Dockerfiles for security issues"""
    
    def __init__(self):
        self.name = "Dockerfile Analyzer"
        self.rules = self._load_rules()
    
    def _load_rules(self) -> List[Dict]:
        """Load Dockerfile security rules"""
        return [
            {
                "id": "DF001",
                "severity": "high",
                "pattern": r"FROM\s+.*:latest",
                "description": "Using 'latest' tag is not recommended",
                "recommendation": "Use specific version tags for reproducibility",
            },
            {
                "id": "DF002",
                "severity": "critical",
                "pattern": r"USER\s+root",
                "description": "Running as root user",
                "recommendation": "Create and use non-root user",
            },
            {
                "id": "DF003",
                "severity": "high",
                "pattern": r"ADD\s+.*",
                "description": "Using ADD instead of COPY",
                "recommendation": "Use COPY instead of ADD unless you need URL fetching or tar extraction",
            },
            {
                "id": "DF004",
                "severity": "medium",
                "pattern": r"RUN\s+.*curl\s+.*\|\s*sh",
                "description": "Piping curl to shell is dangerous",
                "recommendation": "Download, verify, then execute scripts",
            },
            {
                "id": "DF005",
                "severity": "high",
                "pattern": r"EXPOSE\s+.*",
                "description": "Exposing ports without documentation",
                "recommendation": "Document why ports are exposed",
            },
            {
                "id": "DF006",
                "severity": "critical",
                "pattern": r"(?i)(password|secret|key|token)\s*=\s*['\"][^'\"]+['\"]",
                "description": "Hardcoded secrets in Dockerfile",
                "recommendation": "Use secrets management or environment variables",
            },
        ]
    
    async def analyze_async(self, dockerfile_path: Union[str, Path]) -> List[DockerfileIssue]:
        """
        Analyze Dockerfile for security issues
        
        Args:
            dockerfile_path: Path to Dockerfile
            
        Returns:
            List of DockerfileIssue objects
        """
        issues = []
        dockerfile_path = Path(dockerfile_path)
        
        if not dockerfile_path.exists():
            logger.warning(f"Dockerfile not found: {dockerfile_path}")
            return issues
        
        try:
            with open(dockerfile_path, "r", encoding="utf-8") as f:
                content = f.read()
                lines = content.splitlines()
                
                for line_num, line in enumerate(lines, 1):
                    for rule in self.rules:
                        import re
                        if re.search(rule["pattern"], line, re.IGNORECASE):
                            issue = DockerfileIssue(
                                rule_id=rule["id"],
                                severity=rule["severity"],
                                description=rule["description"],
                                line_number=line_num,
                                recommendation=rule["recommendation"],
                            )
                            issues.append(issue)
        
        except Exception as e:
            logger.error(f"Dockerfile analysis error: {e}", exc_info=True)
        
        return issues
