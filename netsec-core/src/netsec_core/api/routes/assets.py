"""Asset discovery routes."""

from fastapi import APIRouter, HTTPException
from typing import List, Optional
from netsec_core.core.asset_discovery import AssetDiscovery

router = APIRouter()
discovery = AssetDiscovery()


@router.post("/discover")
async def discover_assets(network: str, ports: Optional[List[int]] = None):
    """Discover assets on a network."""
    try:
        result = discovery.discover_network(network=network, ports=ports)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error discovering assets: {str(e)}",
        )


@router.post("/inventory")
async def generate_inventory(assets: List[dict]):
    """Generate asset inventory report."""
    try:
        result = discovery.generate_inventory(assets=assets)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating inventory: {str(e)}",
        )
