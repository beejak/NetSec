"""Image extraction utilities for container scanning"""

import asyncio
import logging
import subprocess
import tarfile
import tempfile
from pathlib import Path
from typing import Optional, Union

logger = logging.getLogger(__name__)


class ImageExtractor:
    """Extract container images for scanning"""
    
    def __init__(self):
        self.name = "Image Extractor"
        self.use_docker = self._check_docker_available()
        self.use_podman = self._check_podman_available()
    
    def _check_docker_available(self) -> bool:
        """Check if Docker is available"""
        try:
            result = subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def _check_podman_available(self) -> bool:
        """Check if Podman is available"""
        try:
            result = subprocess.run(
                ["podman", "--version"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    async def extract_image(
        self,
        image: str,
        output_dir: Optional[Union[str, Path]] = None,
    ) -> Optional[Path]:
        """
        Extract container image to directory
        
        Args:
            image: Container image name/tag
            output_dir: Output directory (creates temp if None)
            
        Returns:
            Path to extracted image directory or None
        """
        if output_dir is None:
            output_dir = tempfile.mkdtemp(prefix="netsec_container_")
        else:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = Path(output_dir)
        
        try:
            # Try Docker first, then Podman
            if self.use_docker:
                return await self._extract_with_docker(image, output_path)
            elif self.use_podman:
                return await self._extract_with_podman(image, output_path)
            else:
                logger.warning("Neither Docker nor Podman available for image extraction")
                return None
        except Exception as e:
            logger.error(f"Image extraction failed: {e}", exc_info=True)
            return None
    
    async def _extract_with_docker(
        self,
        image: str,
        output_dir: Path,
    ) -> Optional[Path]:
        """Extract image using Docker"""
        try:
            # Save image to tar
            tar_path = output_dir / "image.tar"
            
            # Pull image if needed (non-blocking check)
            await self._ensure_image_available(image, "docker")
            
            # Save image
            cmd = ["docker", "save", "-o", str(tar_path), image]
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                logger.error(f"Docker save failed: {stderr.decode()}")
                return None
            
            # Extract tar
            extract_path = output_dir / "extracted"
            extract_path.mkdir(exist_ok=True)
            
            with tarfile.open(tar_path, "r") as tar:
                tar.extractall(extract_path)
            
            # Cleanup tar file
            tar_path.unlink()
            
            return extract_path
        
        except Exception as e:
            logger.error(f"Docker extraction error: {e}", exc_info=True)
            return None
    
    async def _extract_with_podman(
        self,
        image: str,
        output_dir: Path,
    ) -> Optional[Path]:
        """Extract image using Podman"""
        try:
            # Save image to tar
            tar_path = output_dir / "image.tar"
            
            # Pull image if needed
            await self._ensure_image_available(image, "podman")
            
            # Save image
            cmd = ["podman", "save", "-o", str(tar_path), image]
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                logger.error(f"Podman save failed: {stderr.decode()}")
                return None
            
            # Extract tar
            extract_path = output_dir / "extracted"
            extract_path.mkdir(exist_ok=True)
            
            with tarfile.open(tar_path, "r") as tar:
                tar.extractall(extract_path)
            
            # Cleanup tar file
            tar_path.unlink()
            
            return extract_path
        
        except Exception as e:
            logger.error(f"Podman extraction error: {e}", exc_info=True)
            return None
    
    async def _ensure_image_available(self, image: str, tool: str) -> bool:
        """Ensure image is available locally, pull if needed"""
        try:
            # Check if image exists
            if tool == "docker":
                cmd = ["docker", "images", "-q", image]
            else:
                cmd = ["podman", "images", "-q", image]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            
            stdout, _ = await process.communicate()
            
            # If image not found, try to pull
            if not stdout.strip():
                logger.info(f"Image {image} not found locally, attempting to pull...")
                if tool == "docker":
                    pull_cmd = ["docker", "pull", image]
                else:
                    pull_cmd = ["podman", "pull", image]
                
                pull_process = await asyncio.create_subprocess_exec(
                    *pull_cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                
                await pull_process.communicate()
                
                if pull_process.returncode != 0:
                    logger.warning(f"Failed to pull image {image}")
                    return False
            
            return True
        
        except Exception as e:
            logger.warning(f"Error checking image availability: {e}")
            return False
    
    def extract_tar_file(
        self,
        tar_path: Union[str, Path],
        output_dir: Optional[Union[str, Path]] = None,
    ) -> Optional[Path]:
        """
        Extract container image tar file
        
        Args:
            tar_path: Path to image tar file
            output_dir: Output directory (creates temp if None)
            
        Returns:
            Path to extracted image directory or None
        """
        tar_path = Path(tar_path)
        
        if not tar_path.exists():
            logger.error(f"Tar file not found: {tar_path}")
            return None
        
        if output_dir is None:
            output_dir = tempfile.mkdtemp(prefix="netsec_container_")
        else:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
        
        extract_path = Path(output_dir) / "extracted"
        extract_path.mkdir(exist_ok=True)
        
        try:
            with tarfile.open(tar_path, "r") as tar:
                tar.extractall(extract_path)
            
            return extract_path
        
        except Exception as e:
            logger.error(f"Tar extraction error: {e}", exc_info=True)
            return None
