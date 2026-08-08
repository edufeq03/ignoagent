"""End-to-end acceptance tests for outbox offline resilience and synchronization.

Verifies the acceptance criteria:
1. API Offline: Executing agent multiple times queues reports in outbox/.
2. API Online: Executing agent flushes all pending outbox reports sequentially to API.
3. Outbox becomes completely empty upon successful delivery.
4. Idempotency: All reports carry unique report_id and no reports are duplicated or lost.
"""

from unittest.mock import MagicMock, patch
import urllib.error
from pathlib import Path
import json
import pytest

from ignoagent.agent import generate_report
from ignoagent.utils.filesystem import get_base_path


def cleanup_outbox():
    outbox_dir = get_base_path() / "reports" / "outbox"
    if outbox_dir.exists():
        for f in outbox_dir.glob("*.json"):
            f.unlink()


import os

def test_outbox_offline_and_reconnection_e2e():
    """Validates the full offline outbox queueing and online synchronization workflow."""
    os.environ["IGNOAGENT_API_TOKEN"] = "ignt_tok_test_e2e"
    cleanup_outbox()
    outbox_dir = get_base_path() / "reports" / "outbox"

    # Step 1: API Offline (urllib raises URLError)
    offline_error = urllib.error.URLError("Connection refused (API Offline)")

    with patch("urllib.request.urlopen", side_effect=offline_error):
        # Step 2: Execute agent 3 times while offline
        rep1 = generate_report()
        rep2 = generate_report()
        rep3 = generate_report()

    # Step 3: Verify exactly 3 reports are queued in outbox/
    outbox_files = sorted(list(outbox_dir.glob("*.json")))
    assert len(outbox_files) == 3, f"Expected 3 outbox files, found {len(outbox_files)}"

    outbox_report_ids = []
    for f in outbox_files:
        with open(f, "r", encoding="utf-8") as file:
            data = json.load(file)
            assert "report_id" in data
            outbox_report_ids.append(data["report_id"])

    assert len(set(outbox_report_ids)) == 3, "Each report must have a unique report_id"
    assert rep1["report_id"] in outbox_report_ids
    assert rep2["report_id"] in outbox_report_ids
    assert rep3["report_id"] in outbox_report_ids

    # Step 4 & 5: API Online again. Execute agent 1 more time.
    received_by_api = []

    def mock_successful_urlopen(req, timeout=10):
        # Extract payload sent to API
        body = req.data.decode("utf-8")
        payload = json.loads(body)
        received_by_api.append(payload)

        mock_resp = MagicMock()
        mock_resp.status = 201
        mock_resp.__enter__.return_value = mock_resp
        return mock_resp

    with patch("urllib.request.urlopen", side_effect=mock_successful_urlopen):
        rep4 = generate_report()

    # Step 6: Verify all 4 reports (3 pending from outbox + 1 new) were received by API
    assert len(received_by_api) == 4, f"Expected 4 requests to API, received {len(received_by_api)}"

    received_report_ids = [r["report_id"] for r in received_by_api]
    expected_order = [rep1["report_id"], rep2["report_id"], rep3["report_id"], rep4["report_id"]]

    assert received_report_ids == expected_order, f"Reports received out of order or duplicated: {received_report_ids}"

    # Step 7: Verify outbox/ is now completely empty
    remaining_outbox = list(outbox_dir.glob("*.json"))
    assert len(remaining_outbox) == 0, f"Expected outbox to be empty, but found: {remaining_outbox}"

    # Step 8: Clean up
    cleanup_outbox()
