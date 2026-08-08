"""Unit tests for API synchronization module."""

from unittest.mock import MagicMock, patch
import json

from ignoagent.outputs.api import send_to_api, sync_outbox
from ignoagent.outputs.file import save_outbox


SAMPLE_REPORT = {
    "agent": {
        "agent_id": "test-agent",
        "environment": "laboratory",
        "owner": "ignotec",
        "version": "0.1.0",
        "instance_id": "882d86be-fe53-49d1-a995-6d772e7d5e19"
    },
    "heartbeat": {
        "last_execution": "2026-08-02T15:45:42.866551",
        "status": "online"
    },
    "timestamp": "2026-08-02T15:45:42.866570",
    "server": {
        "hostname": "vps-test",
        "os": "Linux",
        "python": "3.11.9"
    },
    "system": {
        "cpu_percent": 1.0,
        "memory_percent": 50.0,
        "disk": {"total_gb": 100.0, "used_gb": 50.0, "free_gb": 50.0, "percent": 50.0},
        "uptime_seconds": 3600
    },
    "services": {"docker": [], "failed_services": []},
    "hardening": {"kernel": "6.8.0", "updates": "0"},
    "security": {"ssh_failed_attempts": 0, "source_ips": [], "invalid_users": []},
    "analysis": {"risk_score": 0, "severity": "LOW", "alerts": [], "recommendations": []},
    "network_analysis": {"risk_score": 0, "alerts": [], "recommendations": []}
}


@patch("urllib.request.urlopen")
def test_send_to_api_success(mock_urlopen):
    mock_response = MagicMock()
    mock_response.status = 201
    mock_response.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_response

    result = send_to_api(SAMPLE_REPORT, api_url="http://localhost:8000/v1/reports", token="ignt_tok_test")
    assert result is True
    assert mock_urlopen.called


@patch("urllib.request.urlopen")
def test_sync_outbox_success(mock_urlopen, tmp_path):
    mock_response = MagicMock()
    mock_response.status = 201
    mock_response.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_response

    outbox_file = save_outbox(SAMPLE_REPORT)
    assert outbox_file.exists()

    sent = sync_outbox(api_url="http://localhost:8000/v1/reports", token="ignt_tok_test")
    assert sent >= 1
    # Confirma que o arquivo transmitido foi removido do outbox local
    assert not outbox_file.exists()
