"""Anomaly Detector implementation."""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict, deque
import statistics
import math


class AnomalyDetector:
    """Anomaly Detector for network traffic analysis."""

    def __init__(self):
        """Initialize Anomaly Detector."""
        self.baseline_data = defaultdict(lambda: {"values": deque(maxlen=1000), "mean": 0.0, "std": 0.0})
        self.learning = False
        self.learning_duration = 3600  # 1 hour default
        self.learning_start = None
        self.anomaly_threshold = 3.0  # 3 standard deviations

    def learn_baseline(self, duration: int = 3600) -> Dict[str, Any]:
        """
        Learn baseline statistics for anomaly detection.

        Args:
            duration: Learning duration in seconds

        Returns:
            Dictionary containing learning status
        """
        self.learning = True
        self.learning_duration = duration
        self.learning_start = datetime.utcnow()
        self.baseline_data = defaultdict(lambda: {"values": deque(maxlen=1000), "mean": 0.0, "std": 0.0})

        return {
            "status": "learning",
            "duration": duration,
            "start_time": self.learning_start.isoformat(),
            "message": "Baseline learning started. Feed traffic data to build baseline.",
        }

    def add_traffic_data(
        self,
        metric: str,
        value: float,
        timestamp: Optional[datetime] = None,
    ):
        """
        Add traffic data point for baseline learning.

        Args:
            metric: Metric name (e.g., "packets_per_second", "bytes_per_second")
            value: Metric value
            timestamp: Timestamp (default: now)
        """
        if not self.learning:
            return

        if timestamp is None:
            timestamp = datetime.utcnow()

        # Check if learning period is over
        if self.learning_start:
            elapsed = (timestamp - self.learning_start).total_seconds()
            if elapsed >= self.learning_duration:
                self._finalize_baseline()
                return

        # Add to baseline data
        self.baseline_data[metric]["values"].append(value)

    def _finalize_baseline(self):
        """Finalize baseline by calculating statistics."""
        for metric, data in self.baseline_data.items():
            if len(data["values"]) > 0:
                values = list(data["values"])
                data["mean"] = statistics.mean(values)
                if len(values) > 1:
                    data["std"] = statistics.stdev(values)
                else:
                    data["std"] = 0.0

        self.learning = False

    def detect_anomalies(
        self,
        metric: str,
        value: float,
        timestamp: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """
        Detect anomalies in traffic data.

        Args:
            metric: Metric name
            value: Current value
            timestamp: Timestamp (default: now)

        Returns:
            Dictionary containing anomaly detection results
        """
        if timestamp is None:
            timestamp = datetime.utcnow()

        baseline = self.baseline_data.get(metric)

        if not baseline or baseline["std"] == 0.0:
            return {
                "metric": metric,
                "value": value,
                "anomaly_detected": False,
                "reason": "Insufficient baseline data",
                "timestamp": timestamp.isoformat(),
            }

        mean = baseline["mean"]
        std = baseline["std"]

        # Calculate z-score
        if std > 0:
            z_score = abs((value - mean) / std)
        else:
            z_score = 0.0

        is_anomaly = z_score > self.anomaly_threshold

        result = {
            "metric": metric,
            "value": value,
            "baseline_mean": mean,
            "baseline_std": std,
            "z_score": z_score,
            "anomaly_detected": is_anomaly,
            "severity": self._calculate_severity(z_score),
            "timestamp": timestamp.isoformat(),
        }

        if is_anomaly:
            result["description"] = f"Anomaly detected: {metric} = {value} (baseline: {mean:.2f} ± {std:.2f}, z-score: {z_score:.2f})"

        return result

    def _calculate_severity(self, z_score: float) -> str:
        """Calculate anomaly severity based on z-score."""
        if z_score >= 5.0:
            return "critical"
        elif z_score >= 4.0:
            return "high"
        elif z_score >= 3.0:
            return "medium"
        else:
            return "low"

    def get_status(self) -> Dict[str, Any]:
        """Get anomaly detection status."""
        return {
            "learning": self.learning,
            "learning_start": self.learning_start.isoformat() if self.learning_start else None,
            "learning_duration": self.learning_duration,
            "baseline_metrics": list(self.baseline_data.keys()),
            "threshold": self.anomaly_threshold,
            "timestamp": datetime.utcnow().isoformat(),
        }

    def detect_pattern_anomalies(
        self,
        traffic_data: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Detect pattern-based anomalies in traffic data.

        Args:
            traffic_data: List of traffic data points

        Returns:
            List of detected anomalies
        """
        anomalies = []

        if len(traffic_data) < 10:
            return anomalies

        # Extract values
        values = [d.get("value", 0) for d in traffic_data]

        # Detect sudden spikes
        if len(values) >= 2:
            for i in range(1, len(values)):
                change = abs(values[i] - values[i-1])
                if change > statistics.mean(values) * 2:
                    anomalies.append({
                        "type": "sudden_spike",
                        "index": i,
                        "value": values[i],
                        "previous_value": values[i-1],
                        "change": change,
                        "severity": "high",
                    })

        # Detect unusual patterns
        if len(values) >= 5:
            recent_mean = statistics.mean(values[-5:])
            overall_mean = statistics.mean(values)
            if abs(recent_mean - overall_mean) > overall_mean * 0.5:
                anomalies.append({
                    "type": "pattern_deviation",
                    "recent_mean": recent_mean,
                    "overall_mean": overall_mean,
                    "deviation": abs(recent_mean - overall_mean),
                    "severity": "medium",
                })

        return anomalies
