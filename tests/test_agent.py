"""Integration tests for agent report generation."""

from ignoagent.agent import generate_report


def test_generate_report():
    """Tests orchestrator report generation flow."""
    report = generate_report()
    assert isinstance(report, dict)
    assert "agent" in report
    assert "heartbeat" in report
    assert "timestamp" in report
    assert "server" in report
    assert "system" in report
    assert "services" in report
    assert "hardening" in report
    assert "security" in report
    assert "analysis" in report
    assert "network_analysis" in report
