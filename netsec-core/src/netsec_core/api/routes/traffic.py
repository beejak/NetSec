"""Traffic analysis routes."""

from fastapi import APIRouter, HTTPException
from netsec_core.core.traffic_analyzer import TrafficAnalyzer

router = APIRouter()
analyzer = TrafficAnalyzer()


@router.post("/capture")
async def capture_traffic(
    interface: str = None,
    count: int = None,
    timeout: int = None,
    filter_str: str = None,
):
    """Capture network traffic."""
    try:
        result = analyzer.capture_traffic(
            interface=interface,
            count=count,
            timeout=timeout,
            filter_str=filter_str,
        )
        return result
    except ImportError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Traffic capture requires scapy: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error capturing traffic: {str(e)}",
        )


@router.get("/stream")
async def stream_traffic():
    """Stream network traffic (WebSocket)."""
    # WebSocket implementation would go here
    raise HTTPException(
        status_code=501,
        detail="WebSocket streaming requires additional implementation",
    )


@router.post("/analyze")
async def analyze_traffic(pcap_file: str = None):
    """Analyze captured traffic."""
    try:
        result = analyzer.analyze_traffic(pcap_file=pcap_file)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing traffic: {str(e)}",
        )


@router.get("/flows")
async def get_flows():
    """Get network flows."""
    try:
        flows = analyzer.get_flows()
        return {
            "flows": flows,
            "count": len(flows),
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting flows: {str(e)}",
        )


from datetime import datetime  # noqa: E402
