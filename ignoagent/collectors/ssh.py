"""SSH activity collector.

Counts failed and accepted SSH logins from authentication log files.
"""

import subprocess
from typing import Dict, Any


def collect() -> Dict[str, Any]:
    """Collects SSH login attempt statistics.

    Returns:
        Dict[str, Any]: Dictionary with failed and successful login counts.
    """
    result: Dict[str, Any] = {
        "failed_logins": 0,
        "successful_logins": 0
    }

    try:
        failed = subprocess.run(
            ["bash", "-c", "grep 'Failed password' /var/log/auth.log | wc -l"],
            capture_output=True,
            text=True
        )

        success = subprocess.run(
            ["bash", "-c", "grep 'Accepted password' /var/log/auth.log | wc -l"],
            capture_output=True,
            text=True
        )

        result["failed_logins"] = int(failed.stdout.strip() or 0)
        result["successful_logins"] = int(success.stdout.strip() or 0)

    except Exception as e:
        result["error"] = str(e)

    return result
