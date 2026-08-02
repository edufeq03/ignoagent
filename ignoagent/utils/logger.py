"""Logging utility for IgnoAgent.

Provides a configured logger instance to maintain clean, structured log output.
"""

import logging
import sys
from typing import Optional


def get_logger(name: str = "ignoagent", level: Optional[int] = None) -> logging.Logger:
    """Gets or creates a structured logger for IgnoAgent.

    Args:
        name (str): Logger module name.
        level (int, optional): Logging level. Defaults to INFO if unspecified.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level or logging.INFO)

    return logger


logger = get_logger("ignoagent")
