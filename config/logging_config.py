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
    try:
        logs_dir.mkdir(exist_ok=True)
        logs_writable = True
    except (PermissionError, OSError) as e:
        print(f"Warning: Cannot create logs directory: {e}")
        print("Falling back to console-only logging")
        logs_writable = False

    # Default log file with timestamp
    if log_file is None and logs_writable:
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
            }
        },
        "loggers": {},
        "root": {"level": log_level, "handlers": ["console"]},
    }

    # Add file handlers only if logs directory is writable
    if logs_writable and log_file:
        try:
            # Test if we can write to the log file
            test_file = Path(log_file)
            test_file.touch()

            config["handlers"]["file"] = {
                "class": "logging.FileHandler",
                "level": "DEBUG",
                "formatter": "detailed",
                "filename": str(log_file),
                "mode": "a",
                "encoding": "utf-8",
            }

            config["handlers"]["error_file"] = {
                "class": "logging.FileHandler",
                "level": "ERROR",
                "formatter": "detailed",
                "filename": str(logs_dir / "errors.log"),
                "mode": "a",
                "encoding": "utf-8",
            }

            # Update root and logger handlers to include file handlers
            config["root"]["handlers"] = ["console", "file"]
            file_handlers = ["console", "file", "error_file"]
            simple_file_handlers = ["console", "file"]

        except (PermissionError, OSError) as e:
            print(f"Warning: Cannot write to log files: {e}")
            print("Using console-only logging")
            file_handlers = ["console"]
            simple_file_handlers = ["console"]
    else:
        file_handlers = ["console"]
        simple_file_handlers = ["console"]

    # Configure application loggers
    config["loggers"] = {
        "whisprmate": {"level": "DEBUG", "handlers": file_handlers, "propagate": False},
        "whisprmate.audio": {
            "level": "DEBUG",
            "handlers": simple_file_handlers,
            "propagate": False,
        },
        "whisprmate.auth": {"level": "DEBUG", "handlers": simple_file_handlers, "propagate": False},
        "whisprmate.file": {"level": "DEBUG", "handlers": simple_file_handlers, "propagate": False},
        "whisprmate.transcript": {
            "level": "DEBUG",
            "handlers": simple_file_handlers,
            "propagate": False,
        },
    }

    logging.config.dictConfig(config)

    # Log startup message
    logger = logging.getLogger("whisprmate")
    logger.info("=" * 60)
    logger.info("WhisprMate Application Starting")
    logger.info(f"Log Level: {log_level}")
    logger.info(f"Log File: {log_file if log_file else 'Console only'}")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    if not logs_writable:
        logger.warning("File logging disabled due to permissions - using console only")
    logger.info("=" * 60)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a specific module.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(f"whisprmate.{name}")
