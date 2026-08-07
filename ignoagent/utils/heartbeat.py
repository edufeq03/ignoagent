"""Heartbeat generator utility."""

from datetime import datetime, timezone
from typing import Dict, Any


def create_heartbeat() -> Dict[str, Any]:
    """Generates agent heartbeat payload.

    Returns:
        Dict[str, Any]: Heartbeat containing timestamp and status.
    """
    return {
        "last_execution": datetime.now(timezone.utc).isoformat(),
        "status": "online"
    }
