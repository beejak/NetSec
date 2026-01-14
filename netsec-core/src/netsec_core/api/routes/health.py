"""Health check routes."""

from datetime import datetime
from fastapi import APIRouter

from netsec_core.api.models import HealthResponse
from netsec_core import __version__

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version=__version__,
        timestamp=datetime.utcnow(),
    )
