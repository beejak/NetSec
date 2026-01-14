"""SBOM (Software Bill of Materials) generator"""

import asyncio
import logging
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional, Union, Any

from netsec_container.core.results import SBOM

logger = logging.getLogger(__name__)


class SBOMGenerator:
    """Generate Software Bill of Materials for container images"""
    
    def __init__(self):
        self.name = "SBOM Generator"
        self.use_syft = self._check_syft_available()
        if not self.use_syft:
            logger.warning("Syft not found. Install for SBOM generation: https://github.com/anchore/syft")
    
    def _check_syft_available(self) -> bool:
        """Check if Syft is available"""
        try:
            result = subprocess.run(
                ["syft", "version"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    async def generate_async(
        self,
        image: str,
        image_path: Optional[Union[str, Path]] = None,
        format: str = "spdx-json",
    ) -> Optional[SBOM]:
        """
        Generate SBOM asynchronously
        
        Args:
            image: Container image name/tag
            image_path: Path to saved image tar file
            format: SBOM format (spdx-json, cyclonedx-json)
            
        Returns:
            SBOM object or None
        """
        if self.use_syft:
            return await self._generate_with_syft(image, image_path, format)
        else:
            logger.warning("SBOM generation requires Syft")
            return None
    
    async def _generate_with_syft(
        self,
        image: str,
        image_path: Optional[Union[str, Path]] = None,
        format: str = "spdx-json",
    ) -> Optional[SBOM]:
        """Generate SBOM using Syft"""
        try:
            # Build Syft command
            cmd = [
                "syft",
                "packages",
                "-o", format,
            ]
            
            if image_path:
                cmd.extend(["--file", str(image_path)])
            else:
                cmd.append(image)
            
            # Run Syft
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                logger.error(f"Syft SBOM generation failed: {stderr.decode()}")
                return None
            
            # Parse SBOM
            try:
                sbom_data = json.loads(stdout.decode())
                
                # Extract packages
                packages = []
                if format.startswith("spdx"):
                    packages = sbom_data.get("packages", [])
                elif format.startswith("cyclonedx"):
                    packages = sbom_data.get("components", [])
                
                return SBOM(
                    packages=packages,
                    format=format.split("-")[0],
                    version=sbom_data.get("spdxVersion") or sbom_data.get("bomFormat", "unknown"),
                )
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse Syft output: {e}")
                return None
        
        except Exception as e:
            logger.error(f"SBOM generation error: {e}", exc_info=True)
            return None
