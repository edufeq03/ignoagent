"""Hardening metrics collector.

Collects kernel release, firewall rules, fail2ban status, open listening ports, and upgradable packages.
"""

import subprocess
import platform
from typing import Dict, Any, Optional, List


def run_command(command: str) -> Optional[str]:
    """Executes a shell command safely.

    Args:
        command (str): Command string to execute.

    Returns:
        Optional[str]: Output stripped string or None if command fails.
    """
    try:
        result = subprocess.check_output(
            command,
            shell=True,
            text=True,
            stderr=subprocess.DEVNULL
        )
        return result.strip()
    except Exception:
        return None


def collect() -> Dict[str, Any]:
    """Collects system hardening and patch statistics.

    Returns:
        Dict[str, Any]: Hardening dictionary containing kernel, firewall, fail2ban,
        open ports, and pending updates count.
    """
    return {
        "kernel": platform.release(),
        "firewall": run_command("sudo /usr/sbin/ufw status | head -5"),
        "fail2ban": run_command("/usr/bin/systemctl is-active fail2ban"),
        "open_ports": run_command("/usr/bin/ss -tulpn | grep LISTEN"),
        "updates": run_command("/usr/bin/apt list --upgradable 2>/dev/null | tail -n +2 | wc -l")
    }
