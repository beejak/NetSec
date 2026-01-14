"""Configuration management for NetSec-Core."""

import os
from typing import Optional, Dict, Any
from pathlib import Path


class Config:
    """Configuration manager for NetSec-Core."""

    def __init__(self):
        """Initialize configuration."""
        self.base_dir = Path(__file__).parent.parent.parent
        self.load_config()

    def load_config(self):
        """Load configuration from environment variables."""
        # API Configuration
        self.api_host = os.getenv("API_HOST", "0.0.0.0")
        self.api_port = int(os.getenv("API_PORT", "8000"))
        self.api_reload = os.getenv("API_RELOAD", "false").lower() == "true"
        self.api_workers = int(os.getenv("API_WORKERS", "1"))

        # Logging Configuration
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_file = os.getenv("LOG_FILE", str(self.base_dir / "logs" / "netsec-core.log"))
        self.log_format = os.getenv(
            "LOG_FORMAT",
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Scanner Configuration
        self.scan_timeout = float(os.getenv("SCAN_TIMEOUT", "5.0"))
        self.scan_max_workers = int(os.getenv("SCAN_MAX_WORKERS", "50"))
        self.dns_timeout = float(os.getenv("DNS_TIMEOUT", "5.0"))
        self.dns_lifetime = float(os.getenv("DNS_LIFETIME", "10.0"))

        # SSL/TLS Configuration
        self.ssl_timeout = float(os.getenv("SSL_TIMEOUT", "10.0"))
        self.ssl_check_expiration_days = int(os.getenv("SSL_CHECK_EXPIRATION_DAYS", "30"))

        # LLM Configuration
        self.llm_provider = os.getenv("LLM_PROVIDER", "openai")
        self.llm_model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.llm_enabled = bool(self.openai_api_key or self.anthropic_api_key)

        # Anomaly Detection Configuration
        self.anomaly_threshold = float(os.getenv("ANOMALY_THRESHOLD", "3.0"))
        self.anomaly_learning_duration = int(os.getenv("ANOMALY_LEARNING_DURATION", "3600"))

        # Traffic Analysis Configuration
        self.traffic_capture_timeout = int(os.getenv("TRAFFIC_CAPTURE_TIMEOUT", "60"))
        self.traffic_max_packets = int(os.getenv("TRAFFIC_MAX_PACKETS", "10000"))

        # Data Storage
        self.data_dir = Path(os.getenv("DATA_DIR", str(self.base_dir / "data")))
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Logs Directory
        self.logs_dir = Path(os.getenv("LOGS_DIR", str(self.base_dir / "logs")))
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        # CORS Configuration
        self.cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
        self.cors_credentials = os.getenv("CORS_CREDENTIALS", "true").lower() == "true"

    def get_dict(self) -> Dict[str, Any]:
        """Get configuration as dictionary."""
        return {
            "api": {
                "host": self.api_host,
                "port": self.api_port,
                "reload": self.api_reload,
                "workers": self.api_workers,
            },
            "logging": {
                "level": self.log_level,
                "file": self.log_file,
                "format": self.log_format,
            },
            "scanner": {
                "timeout": self.scan_timeout,
                "max_workers": self.scan_max_workers,
                "dns_timeout": self.dns_timeout,
                "dns_lifetime": self.dns_lifetime,
            },
            "ssl": {
                "timeout": self.ssl_timeout,
                "check_expiration_days": self.ssl_check_expiration_days,
            },
            "llm": {
                "provider": self.llm_provider,
                "model": self.llm_model,
                "enabled": self.llm_enabled,
            },
            "anomaly": {
                "threshold": self.anomaly_threshold,
                "learning_duration": self.anomaly_learning_duration,
            },
            "traffic": {
                "capture_timeout": self.traffic_capture_timeout,
                "max_packets": self.traffic_max_packets,
            },
            "cors": {
                "origins": self.cors_origins,
                "credentials": self.cors_credentials,
            },
        }

    def update_from_file(self, config_file: Path):
        """Update configuration from file (future enhancement)."""
        # Would implement YAML/JSON config file loading
        pass


# Global configuration instance
config = Config()
