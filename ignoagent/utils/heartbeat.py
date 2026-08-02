"""Heartbeat generator utility."""

from datetime import datetime
from typing import Dict, Any


def create_heartbeat() -> Dict[str, Any]:
    """Generates agent heartbeat payload.

    Returns:
        Dict[str, Any]: Heartbeat containing timestamp and status.
    """
    return {
        "last_execution": datetime.now().isoformat(),
        "status": "online"
    }
