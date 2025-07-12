"""Logging configuration for the WhisprMate application."""

import logging
import logging.config
import os
from datetime import datetime
from pathlib import Path


def setup_logging(log_level: str = "INFO", log_file: str = None) -> None:
    """Set up logging configuration for the application.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path. If None, uses default location.
    """
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Default log file with timestamp
    if log_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = logs_dir / f"whisprmate_{timestamp}.log"

    # Logging configuration
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "detailed": {
                "format": (
                    "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "simple": {"format": "%(levelname)s - %(name)s - %(message)s"},
            "console": {
                "format": "🎙️ %(asctime)s [%(levelname)s] %(name)s: %(message)s",
                "datefmt": "%H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "console",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.FileHandler",
                "level": "DEBUG",
                "formatter": "detailed",
                "filename": str(log_file),
                "mode": "a",
                "encoding": "utf-8",
            },
            "error_file": {
                "class": "logging.FileHandler",
                "level": "ERROR",
                "formatter": "detailed",
                "filename": str(logs_dir / "errors.log"),
                "mode": "a",
                "encoding": "utf-8",
            },
        },
        "loggers": {
            "whisprmate": {
                "level": "DEBUG",
                "handlers": ["console", "file", "error_file"],
                "propagate": False,
            },
            "whisprmate.audio": {
                "level": "DEBUG",
                "handlers": ["console", "file"],
                "propagate": False,
            },
            "whisprmate.auth": {
                "level": "DEBUG",
                "handlers": ["console", "file"],
                "propagate": False,
            },
            "whisprmate.file": {
                "level": "DEBUG",
                "handlers": ["console", "file"],
                "propagate": False,
            },
            "whisprmate.transcript": {
                "level": "DEBUG",
                "handlers": ["console", "file"],
                "propagate": False,
            },
        },
        "root": {"level": log_level, "handlers": ["console", "file"]},
    }

    logging.config.dictConfig(config)

    # Log startup message
    logger = logging.getLogger("whisprmate")
    logger.info("=" * 60)
    logger.info("WhisprMate Application Starting")
    logger.info(f"Log Level: {log_level}")
    logger.info(f"Log File: {log_file}")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    logger.info("=" * 60)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a specific module.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(f"whisprmate.{name}")
