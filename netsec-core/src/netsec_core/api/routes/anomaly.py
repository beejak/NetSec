"""Anomaly detection routes."""

from fastapi import APIRouter, HTTPException
from netsec_core.core.anomaly_detector import AnomalyDetector

router = APIRouter()
detector = AnomalyDetector()


@router.post("/learn-baseline")
async def learn_baseline(duration: int = 3600):
    """Learn baseline for anomaly detection."""
    try:
        result = detector.learn_baseline(duration=duration)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error learning baseline: {str(e)}",
        )


@router.post("/detect")
async def detect_anomalies(metric: str, value: float):
    """Detect anomalies in network traffic."""
    try:
        result = detector.detect_anomalies(metric=metric, value=value)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error detecting anomalies: {str(e)}",
        )


@router.get("/status")
async def get_anomaly_status():
    """Get anomaly detection status."""
    try:
        status = detector.get_status()
        return status
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting status: {str(e)}",
        )
