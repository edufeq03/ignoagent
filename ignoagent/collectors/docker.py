"""Docker container collector.

Isolates Docker container inspection and data collection.
"""

import subprocess
from typing import Dict, Any, List, Union


def collect() -> Union[List[str], Dict[str, Any]]:
    """Collects running Docker containers list.

    Returns:
        Union[List[str], Dict[str, Any]]: List of running container names, or error payload.
    """
    try:
        docker_output = subprocess.check_output(
            ["docker", "ps", "--format", "{{.Names}}"],
            text=True
        )
        return docker_output.splitlines()
    except Exception as e:
        return {"error": str(e)}
