"""Unit tests for IgnoAgent analyzers."""

from ignoagent.analyzers import analyze_availability, analyze_ports, analyze_risk


def test_analyze_risk_low():
    """Tests risk analyzer with clean security payload."""
    security = {"ssh_failed_attempts": 0, "invalid_users": []}
    result = analyze_risk(security)
    assert result["risk_score"] == 0
    assert result["severity"] == "LOW"
    assert len(result["alerts"]) == 0


def test_analyze_risk_high():
    """Tests risk analyzer with root invalid attempts and high failures."""
    security = {"ssh_failed_attempts": 150, "invalid_users": ["root", "admin"]}
    result = analyze_risk(security)
    assert result["risk_score"] == 50  # 10 (failed>0) + 15 (root) + 25 (failed>100)
    assert result["severity"] == "HIGH"
    assert len(result["alerts"]) == 3


def test_analyze_ports():
    """Tests network ports risk analyzer."""
    open_ports = "tcp 0 0 0.0.0.0:22 0.0.0.0:* LISTEN\ntcp 0 0 0.0.0.0:3000 0.0.0.0:* LISTEN"
    result = analyze_ports(open_ports)
    assert result["risk_score"] == 30  # 2 ports matched * 15
    assert len(result["alerts"]) == 2


def test_analyze_availability():
    """Tests availability risk analyzer."""
    services = {"failed_services": ["nginx.service"]}
    system = {"disk": {"percent": 95}, "memory_percent": 92}
    result = analyze_availability(services, system)
    assert result["risk_score"] == 70  # 20 (failed service) + 30 (disk>90) + 20 (mem>90)
    assert len(result["alerts"]) == 3
