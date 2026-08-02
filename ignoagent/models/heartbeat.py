"""Heartbeat dataclass model."""

from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class HeartbeatModel:
    """Represents agent heartbeat status."""
    last_execution: str
    status: str = "online"

    def to_dict(self) -> Dict[str, Any]:
        """Converts heartbeat model instance to dictionary."""
        return asdict(self)
