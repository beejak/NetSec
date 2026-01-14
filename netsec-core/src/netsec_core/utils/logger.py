"""Logging utilities for NetSec-Core."""

import logging
import sys
from pathlib import Path
from typing import Optional
from netsec_core.config import config


def setup_logger(
    name: str = "netsec_core",
    level: Optional[str] = None,
    log_file: Optional[str] = None,
    verbose: bool = False,
) -> logging.Logger:
    """
    Set up logger for NetSec-Core.

    Args:
        name: Logger name
        level: Log level (default: from config)
        log_file: Log file path (default: from config)
        verbose: Enable verbose logging (default: False)

    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    
    # Set log level
    if verbose:
        log_level = logging.DEBUG
    else:
        log_level = level or config.log_level
        log_level = getattr(logging, log_level.upper(), logging.INFO)
    
    logger.setLevel(log_level)

    # Remove existing handlers
    logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler
    if log_file or config.log_file:
        log_path = Path(log_file or config.log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Use rotating file handler for better log management
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            config.log_format,
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


# Default logger
logger = setup_logger()
