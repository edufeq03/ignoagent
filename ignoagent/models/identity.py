"""Identity dataclass model."""

from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional


@dataclass
class IdentityModel:
    """Represents agent instance identity."""
    instance_id: str
    name: Optional[str] = None
    environment: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Converts identity model instance to dictionary."""
        return asdict(self)
