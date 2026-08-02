"""Security collector.

Parses authentication logs for failed login attempts, source IPs, and invalid users.
"""

import re
from pathlib import Path
from typing import Dict, Any, List, Set

AUTH_LOG = Path("/var/log/auth.log")


def collect() -> Dict[str, Any]:
    """Collects security authentication metric logs.

    Returns:
        Dict[str, Any]: Security metrics including failed SSH attempts, source IPs,
        and invalid user names.
    """
    result: Dict[str, Any] = {
        "ssh_failed_attempts": 0,
        "source_ips": [],
        "invalid_users": []
    }

    if not AUTH_LOG.exists():
        return result

    try:
        lines = AUTH_LOG.read_text(errors="ignore").splitlines()
    except Exception:
        return result

    ips: Set[str] = set()
    users: Set[str] = set()

    for line in lines[-500:]:
        if "Failed password" in line or "Invalid user" in line:
            result["ssh_failed_attempts"] += 1

            ip_match = re.search(
                r'from ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)',
                line
            )
            if ip_match:
                ips.add(ip_match.group(1))

            user_match = re.search(
                r'(?:invalid user|for invalid user|for)\s+([a-zA-Z0-9_-]+)',
                line
            )
            if user_match:
                users.add(user_match.group(1))

    result["source_ips"] = list(ips)
    result["invalid_users"] = list(users)

    return result
