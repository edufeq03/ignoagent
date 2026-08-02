"""Unit tests for IgnoAgent collectors."""

from ignoagent.collectors import (
    collect_docker,
    collect_hardening,
    collect_security,
    collect_services,
    collect_ssh,
    collect_system,
)


def test_collect_system():
    """Tests system metrics collector structure."""
    data = collect_system()
    assert isinstance(data, dict)
    assert "cpu_percent" in data
    assert "memory_percent" in data
    assert "disk" in data
    assert "uptime_seconds" in data


def test_collect_services():
    """Tests services collector structure."""
    data = collect_services()
    assert isinstance(data, dict)
    assert "docker" in data
    assert "failed_services" in data


def test_collect_security():
    """Tests security log collector structure."""
    data = collect_security()
    assert isinstance(data, dict)
    assert "ssh_failed_attempts" in data
    assert "source_ips" in data
    assert "invalid_users" in data


def test_collect_hardening():
    """Tests hardening metrics collector structure."""
    data = collect_hardening()
    assert isinstance(data, dict)
    assert "kernel" in data
    assert "firewall" in data
    assert "fail2ban" in data
    assert "open_ports" in data
    assert "updates" in data


def test_collect_ssh():
    """Tests SSH activity collector structure."""
    data = collect_ssh()
    assert isinstance(data, dict)
    assert ("failed_logins" in data and "successful_logins" in data) or "error" in data
