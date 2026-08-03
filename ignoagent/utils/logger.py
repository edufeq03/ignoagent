"""Logging utility for IgnoAgent.

Provides a configured logger instance with colored output and clean formatting.
"""

import logging
import sys
from typing import Optional

# ANSI Color Codes
CYAN = "\033[0;36m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
BOLD_RED = "\033[1;31m"
GRAY = "\033[0;90m"
RESET = "\033[0m"


class ColoredFormatter(logging.Formatter):
    """Custom formatter adding ANSI colors to logger output."""

    def format(self, record: logging.LogRecord) -> str:
        timestamp = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
        msg = record.getMessage()

        # Colorize level / tags
        if record.levelno >= logging.ERROR:
            level_str = f"{BOLD_RED}[ERROR]{RESET}"
        elif record.levelno >= logging.WARNING:
            level_str = f"{YELLOW}[WARNING]{RESET}"
        else:
            level_str = f"{GREEN}[INFO]{RESET}"

        # Colorize arrows / paths if present
        if "->" in msg:
            parts = msg.split("->")
            formatted_parts = [parts[0]]
            for part in parts[1:]:
                formatted_parts.append(f"->{GRAY}{part}{RESET}")
            msg = "".join(formatted_parts)

        # Colorize lines like ======
        if msg.startswith("==="):
            return f"{CYAN}{msg}{RESET}"

        return f"[{timestamp}] {level_str} {msg}"


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
        formatter = ColoredFormatter()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level or logging.INFO)

    return logger


logger = get_logger("ignoagent")
