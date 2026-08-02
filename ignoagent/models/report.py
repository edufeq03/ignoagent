"""Report dataclass model."""

from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class ReportModel:
    """Represents compiled status report."""
    agent: Dict[str, Any]
    heartbeat: Dict[str, Any]
    timestamp: str
    server: Dict[str, Any]
    system: Dict[str, Any]
    services: Dict[str, Any]
    hardening: Dict[str, Any]
    security: Dict[str, Any]
    analysis: Dict[str, Any]
    network_analysis: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Converts report model instance to dictionary."""
        return asdict(self)
