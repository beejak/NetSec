"""Main container scanner engine"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union
from datetime import datetime

from netsec_container.core.vulnerability import VulnerabilityScanner
from netsec_container.core.secrets import SecretsScanner
from netsec_container.core.sbom import SBOMGenerator
from netsec_container.core.dockerfile import DockerfileAnalyzer
from netsec_container.core.scoring import RiskScorer
from netsec_container.core.results import ScanResults

logger = logging.getLogger(__name__)


class ContainerScanner:
    """Main container security scanner"""
    
    def __init__(
        self,
        enable_vulnerability: bool = True,
        enable_secrets: bool = True,
        enable_sbom: bool = True,
        enable_dockerfile: bool = True,
        enable_llm: bool = False,
        llm_provider: Optional[str] = None,
        llm_model: Optional[str] = None,
    ):
        """
        Initialize container scanner
        
        Args:
            enable_vulnerability: Enable vulnerability scanning
            enable_secrets: Enable secrets detection
            enable_sbom: Enable SBOM generation
            enable_dockerfile: Enable Dockerfile analysis
            enable_llm: Enable LLM-powered features
            llm_provider: LLM provider (openai, anthropic, local)
            llm_model: LLM model name
        """
        self.enable_vulnerability = enable_vulnerability
        self.enable_secrets = enable_secrets
        self.enable_sbom = enable_sbom
        self.enable_dockerfile = enable_dockerfile
        self.enable_llm = enable_llm
        
        # Initialize scanners
        self.vulnerability_scanner = None
        if enable_vulnerability:
            self.vulnerability_scanner = VulnerabilityScanner()
        
        self.secrets_scanner = None
        if enable_secrets:
            self.secrets_scanner = SecretsScanner()
        
        self.sbom_generator = None
        if enable_sbom:
            self.sbom_generator = SBOMGenerator()
        
        self.dockerfile_analyzer = None
        if enable_dockerfile:
            self.dockerfile_analyzer = DockerfileAnalyzer()
        
        # LLM components (lazy import)
        self.llm_analyzer = None
        if enable_llm:
            try:
                from netsec_container.llm.analyzer import LLMAnalyzer
                self.llm_analyzer = LLMAnalyzer(
                    provider=llm_provider or "openai",
                    model=llm_model or "gpt-4"
                )
            except ImportError:
                logger.warning("LLM dependencies not available. Install with: pip install openai anthropic")
        
        self.risk_scorer = RiskScorer()
    
    async def scan_image_async(
        self,
        image: str,
        image_file: Optional[Union[str, Path]] = None,
        dockerfile_path: Optional[Union[str, Path]] = None,
    ) -> ScanResults:
        """
        Scan container image asynchronously
        
        Args:
            image: Container image name/tag
            image_file: Path to saved image tar file
            dockerfile_path: Path to Dockerfile for analysis
            
        Returns:
            ScanResults object with all findings
        """
        start_time = datetime.now()
        results = ScanResults(image=image, scan_start=start_time)
        
        try:
            # Extract image layers if needed
            image_path = None
            if image_file:
                image_path = Path(image_file)
            
            # Run scans in parallel
            tasks = []
            
            if self.enable_vulnerability and self.vulnerability_scanner:
                tasks.append(
                    self.vulnerability_scanner.scan_async(image, image_path)
                )
            
            if self.enable_secrets and self.secrets_scanner:
                tasks.append(
                    self.secrets_scanner.scan_async(image, image_path)
                )
            
            if self.enable_sbom and self.sbom_generator:
                tasks.append(
                    self.sbom_generator.generate_async(image, image_path)
                )
            
            if self.enable_dockerfile and self.dockerfile_analyzer and dockerfile_path:
                tasks.append(
                    self.dockerfile_analyzer.analyze_async(dockerfile_path)
                )
            
            # Wait for all scans to complete
            scan_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            for i, result in enumerate(scan_results):
                if isinstance(result, Exception):
                    logger.error(f"Scan task {i} failed: {result}")
                    continue
                
                if i == 0 and self.enable_vulnerability:
                    results.vulnerabilities = result
                elif i == 1 and self.enable_secrets:
                    results.secrets = result
                elif i == 2 and self.enable_sbom:
                    results.sbom = result
                elif i == 3 and self.enable_dockerfile:
                    results.dockerfile_issues = result
            
            # Calculate risk score
            results.risk_score = self.risk_scorer.calculate_score(results)
            
            # LLM analysis if enabled
            if self.enable_llm and self.llm_analyzer:
                try:
                    results.llm_remediation = await self.llm_analyzer.analyze_and_remediate(results)
                except Exception as e:
                    logger.warning(f"LLM analysis failed: {e}")
            
            results.scan_end = datetime.now()
            results.scan_duration = (results.scan_end - results.scan_start).total_seconds()
            
        except Exception as e:
            logger.error(f"Scan failed: {e}", exc_info=True)
            results.error = str(e)
            results.scan_end = datetime.now()
        
        return results
    
    def scan_image(
        self,
        image: str,
        image_file: Optional[Union[str, Path]] = None,
        dockerfile_path: Optional[Union[str, Path]] = None,
    ) -> ScanResults:
        """
        Scan container image (synchronous wrapper)
        
        Args:
            image: Container image name/tag
            image_file: Path to saved image tar file
            dockerfile_path: Path to Dockerfile for analysis
            
        Returns:
            ScanResults object with all findings
        """
        return asyncio.run(self.scan_image_async(image, image_file, dockerfile_path))
    
    def generate_report(
        self,
        results: ScanResults,
        format: str = "pdf",
        output: Optional[Union[str, Path]] = None,
    ) -> Path:
        """
        Generate security report
        
        Args:
            results: ScanResults object
            format: Report format (pdf, csv, json)
            output: Output file path
            
        Returns:
            Path to generated report
        """
        if format.lower() == "pdf":
            from netsec_container.reports.pdf import PDFReportGenerator
            generator = PDFReportGenerator()
            return generator.generate(results, output)
        elif format.lower() == "csv":
            from netsec_container.reports.csv import CSVReportGenerator
            generator = CSVReportGenerator()
            return generator.generate(results, output)
        elif format.lower() == "json":
            from netsec_container.reports.json import JSONReportGenerator
            generator = JSONReportGenerator()
            return generator.generate(results, output)
        else:
            raise ValueError(f"Unsupported format: {format}")
