"""Services collector.

Collects running Docker containers and failed systemd services.
"""

import subprocess
from typing import Dict, Any
from ignoagent.collectors.docker import collect as collect_docker


def collect() -> Dict[str, Any]:
    """Collects system service metrics and container states.

    Returns:
        Dict[str, Any]: Dictionary containing docker container names and systemd failed services.
    """
    result: Dict[str, Any] = {
        "docker": [],
        "failed_services": []
    }

    docker_res = collect_docker()
    if isinstance(docker_res, list):
        result["docker"] = docker_res
    elif isinstance(docker_res, dict) and "error" in docker_res:
        result["docker_error"] = docker_res["error"]

    try:
        failed = subprocess.check_output(
            [
                "systemctl",
                "--failed",
                "--no-legend"
            ],
            text=True,
            timeout=2
        )

        if failed.strip():
            result["failed_services"] = failed.splitlines()

    except Exception as e:
        result["systemd_error"] = str(e)

    return result
