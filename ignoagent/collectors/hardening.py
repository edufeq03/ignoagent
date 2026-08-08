"""Hardening metrics collector.

Collects kernel release, firewall rules, fail2ban status, open listening ports, and upgradable packages safely without shell=True.
"""

import os
import platform
import subprocess
from typing import Dict, Any, Optional, List


def run_args(cmd: List[str], timeout: int = 5) -> Optional[str]:
    """Executes a command using argument list without shell invocation.

    Args:
        cmd (List[str]): List of command arguments.
        timeout (int): Timeout in seconds.

    Returns:
        Optional[str]: Output stripped string or None if command fails or times out.
    """
    try:
        res = subprocess.run(
            cmd,
            shell=False,
            text=True,
            capture_output=True,
            timeout=timeout
        )
        if res.returncode == 0 or res.stdout:
            return res.stdout.strip()
        return None
    except (subprocess.SubprocessError, OSError):
        return None


def get_firewall_status() -> str:
    """Collects UFW firewall status safely."""
    raw = run_args(["ufw", "status"]) or run_args(["/usr/sbin/ufw", "status"])
    if not raw:
        return "inactive / unverified"
    # Filtrar primeiras 5 linhas em Python sem depender de shell pipe | head -5
    lines = raw.splitlines()[:5]
    return "\n".join(lines)


def get_open_ports() -> str:
    """Collects open listening ports using ss safely."""
    raw = run_args(["ss", "-tulpn"]) or run_args(["/usr/bin/ss", "-tulpn"])
    if not raw:
        return ""
    # Filtrar linhas contendo LISTEN em Python sem depender de shell pipe | grep LISTEN
    listen_lines = [line for line in raw.splitlines() if "LISTEN" in line]
    return "\n".join(listen_lines[:10])


def get_pending_updates() -> str:
    """Reads available package updates from system notification file."""
    updates_path = "/var/lib/update-notifier/updates-available"
    if os.path.exists(updates_path):
        try:
            with open(updates_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if "packages" in line.lower():
                        return line.strip()
        except OSError:
            pass
    return "0"


def collect() -> Dict[str, Any]:
    """Collects system hardening and patch statistics.

    Returns:
        Dict[str, Any]: Hardening dictionary containing kernel, firewall, fail2ban,
        open ports, and pending updates count.
    """
    fail2ban = run_args(["systemctl", "is-active", "fail2ban"]) or run_args(["/usr/bin/systemctl", "is-active", "fail2ban"]) or "inactive"

    return {
        "kernel": platform.release(),
        "firewall": get_firewall_status(),
        "fail2ban": fail2ban,
        "open_ports": get_open_ports(),
        "updates": get_pending_updates()
    }
