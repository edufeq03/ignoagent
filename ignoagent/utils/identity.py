"""Identity and unique instance identifier utility."""

import uuid
from pathlib import Path
from ignoagent.utils.filesystem import get_base_path


def get_instance_id() -> str:
    """Retrieves or generates unique instance ID for this agent.

    Returns:
        str: UUID string representing the instance ID.
    """
    instance_file = get_base_path() / "config" / "instance_id"

    if instance_file.exists():
        return instance_file.read_text().strip()

    instance_id = str(uuid.uuid4())
    instance_file.parent.mkdir(parents=True, exist_ok=True)
    instance_file.write_text(instance_id, encoding="utf-8")

    return instance_id
