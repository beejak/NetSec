"""Secrets scanner for container images"""

import asyncio
import logging
import re
from pathlib import Path
from typing import List, Optional, Union, Dict

from netsec_container.core.results import Secret
from netsec_container.core.image_extractor import ImageExtractor

logger = logging.getLogger(__name__)


class SecretsScanner:
    """Scan container images for hardcoded secrets"""
    
    def __init__(self):
        self.name = "Secrets Scanner"
        self.patterns = self._load_secret_patterns()
        self.image_extractor = ImageExtractor()
    
    def _load_secret_patterns(self) -> List[Dict[str, any]]:
        """Load secret detection patterns"""
        return [
            {
                "type": "aws_access_key",
                "pattern": r"AKIA[0-9A-Z]{16}",
                "confidence": 0.9,
            },
            {
                "type": "aws_secret_key",
                "pattern": r"aws_secret_access_key\s*=\s*['\"]?([A-Za-z0-9/+=]{40})['\"]?",
                "confidence": 0.85,
            },
            {
                "type": "api_key",
                "pattern": r"(?i)(api[_-]?key|apikey)\s*[=:]\s*['\"]?([A-Za-z0-9_\-]{20,})['\"]?",
                "confidence": 0.7,
            },
            {
                "type": "password",
                "pattern": r"(?i)(password|passwd|pwd)\s*[=:]\s*['\"]?([^\s'\"<>]{8,})['\"]?",
                "confidence": 0.75,
            },
            {
                "type": "private_key",
                "pattern": r"-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----",
                "confidence": 0.95,
            },
            {
                "type": "ssh_key",
                "pattern": r"-----BEGIN\s+(DSA|RSA|EC|OPENSSH)\s+PRIVATE\s+KEY-----",
                "confidence": 0.95,
            },
            {
                "type": "github_token",
                "pattern": r"ghp_[A-Za-z0-9]{36}",
                "confidence": 0.9,
            },
            {
                "type": "slack_token",
                "pattern": r"xox[baprs]-[0-9a-zA-Z\-]{10,}",
                "confidence": 0.85,
            },
            {
                "type": "jwt_token",
                "pattern": r"eyJ[A-Za-z0-9-_=]+\.eyJ[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*",
                "confidence": 0.8,
            },
            {
                "type": "database_url",
                "pattern": r"(?i)(mysql|postgres|mongodb)://[^\s'\"<>]+",
                "confidence": 0.85,
            },
        ]
    
    async def scan_async(
        self,
        image: str,
        image_path: Optional[Union[str, Path]] = None,
    ) -> List[Secret]:
        """
        Scan image for secrets asynchronously
        
        Args:
            image: Container image name/tag
            image_path: Path to saved image tar file
            
        Returns:
            List of Secret objects
        """
        secrets = []
        
        try:
            # Extract image layers
            if image_path:
                extracted_path = await self._extract_image(image_path)
            else:
                extracted_path = await self._extract_image_from_docker(image)
            
            if not extracted_path:
                logger.warning("Could not extract image for secrets scanning")
                return secrets
            
            # Scan extracted files
            secrets = await self._scan_directory(extracted_path)
            
            # Cleanup
            if extracted_path.exists():
                import shutil
                shutil.rmtree(extracted_path)
        
        except Exception as e:
            logger.error(f"Secrets scan error: {e}", exc_info=True)
        
        return secrets
    
    async def _extract_image(self, image_path: Union[str, Path]) -> Optional[Path]:
        """Extract container image tar file"""
        try:
            return self.image_extractor.extract_tar_file(image_path)
        except Exception as e:
            logger.error(f"Failed to extract image tar: {e}")
            return None
    
    async def _extract_image_from_docker(self, image: str) -> Optional[Path]:
        """Extract image from Docker/Podman"""
        try:
            return await self.image_extractor.extract_image(image)
        except Exception as e:
            logger.error(f"Failed to extract image: {e}")
            return None
    
    async def _scan_directory(self, directory: Path) -> List[Secret]:
        """Scan directory for secrets"""
        secrets = []
        
        # Common files to skip
        skip_patterns = [
            r"\.git/",
            r"node_modules/",
            r"\.pyc$",
            r"\.pyo$",
            r"\.so$",
            r"\.dylib$",
            r"\.dll$",
        ]
        
        # Scan files
        for file_path in directory.rglob("*"):
            if not file_path.is_file():
                continue
            
            # Skip binary files and patterns
            should_skip = False
            for pattern in skip_patterns:
                if re.search(pattern, str(file_path)):
                    should_skip = True
                    break
            
            if should_skip:
                continue
            
            # Read file content
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    line_number = 0
                    
                    for line in content.splitlines():
                        line_number += 1
                        
                        # Check each pattern
                        for pattern_config in self.patterns:
                            matches = re.finditer(
                                pattern_config["pattern"],
                                line,
                                re.IGNORECASE | re.MULTILINE
                            )
                            
                            for match in matches:
                                secret = Secret(
                                    type=pattern_config["type"],
                                    value=self._mask_secret(match.group(0)),
                                    file_path=str(file_path.relative_to(directory)),
                                    line_number=line_number,
                                    confidence=pattern_config["confidence"],
                                    context=line.strip()[:100],  # First 100 chars
                                )
                                secrets.append(secret)
            
            except Exception as e:
                logger.debug(f"Error reading {file_path}: {e}")
                continue
        
        return secrets
    
    def _mask_secret(self, secret: str) -> str:
        """Mask secret value for display"""
        if len(secret) <= 8:
            return "***"
        return secret[:4] + "***" + secret[-4:]
