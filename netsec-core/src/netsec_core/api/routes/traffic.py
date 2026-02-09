"""Traffic analysis routes."""

import logging
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from typing import Optional

logger = logging.getLogger(__name__)
router = APIRouter()
_analyzer: Optional[object] = None


def _get_analyzer():
    """Lazy-load TrafficAnalyzer to avoid import errors if scapy is not available."""
    global _analyzer
    if _analyzer is None:
        try:
            from netsec_core.core.traffic_analyzer import TrafficAnalyzer
            _analyzer = TrafficAnalyzer()
        except ImportError as e:
            raise ImportError(f"scapy is required for traffic analysis: {e}")
    return _analyzer


@router.post("/capture")
async def capture_traffic(
    interface: str = None,
    count: int = None,
    timeout: int = None,
    filter_str: str = None,
):
    """Capture network traffic."""
    try:
        analyzer = _get_analyzer()
        result = analyzer.capture_traffic(
            interface=interface,
            count=count,
            timeout=timeout,
            filter_str=filter_str,
        )
        return result
    except ImportError:
        logger.warning("Traffic capture requires scapy")
        raise HTTPException(status_code=503, detail="Traffic capture requires scapy.")
    except Exception:
        logger.exception("Traffic capture failed")
        raise HTTPException(status_code=500, detail="An error occurred while capturing traffic.")


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
        analyzer = _get_analyzer()
        result = analyzer.analyze_traffic(pcap_file=pcap_file)
        return result
    except ImportError:
        logger.warning("Traffic analysis requires scapy")
        raise HTTPException(status_code=503, detail="Traffic analysis requires scapy.")
    except Exception:
        logger.exception("Traffic analysis failed")
        raise HTTPException(status_code=500, detail="An error occurred while analyzing traffic.")


@router.get("/flows")
async def get_flows():
    """Get network flows."""
    try:
        analyzer = _get_analyzer()
        flows = analyzer.get_flows()
        return {
            "flows": flows,
            "count": len(flows),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except ImportError:
        logger.warning("Traffic flows require scapy")
        raise HTTPException(status_code=503, detail="Traffic flows require scapy.")
    except Exception:
        logger.exception("Get flows failed")
        raise HTTPException(status_code=500, detail="An error occurred while getting flows.")
