"""API request/response models"""

from pydantic import BaseModel
from typing import Optional, Dict, Any


class ScanRequest(BaseModel):
    """Scan request model"""
    image: str
    image_file: Optional[str] = None
    dockerfile_path: Optional[str] = None
    enable_vulnerability: bool = True
    enable_secrets: bool = True
    enable_sbom: bool = True
    enable_llm: bool = False
    llm_provider: Optional[str] = None
    llm_model: Optional[str] = None


class ScanResponse(BaseModel):
    """Scan response model"""
    success: bool
    results: Dict[str, Any]
    error: Optional[str] = None
