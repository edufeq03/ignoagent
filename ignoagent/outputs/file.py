"""File output handlers for IgnoAgent.

Centralizes local filesystem persistence for reports, status, history, and outbox queues.
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Union

from ignoagent.utils.filesystem import get_base_path, save_json


def save_report(report: Dict[str, Any], path: Union[str, Path]) -> Path:
    """Saves compiled report JSON payload to a specified file path.

    Args:
        report (Dict[str, Any]): Report data dictionary.
        path (Union[str, Path]): Target file path.

    Returns:
        Path: Path object of written file.
    """
    return save_json(report, path)


def save_status(report: Dict[str, Any]) -> Path:
    """Saves report status to reports/status.json.

    Args:
        report (Dict[str, Any]): Report data dictionary.

    Returns:
        Path: Saved status file path.
    """
    status_file = get_base_path() / "reports" / "status.json"
    return save_json(report, status_file)


def save_history(report: Dict[str, Any]) -> Path:
    """Saves timestamped report to reports/history directory.

    Args:
        report (Dict[str, Any]): Report data dictionary.

    Returns:
        Path: Saved history file path.
    """
    filename = datetime.now().strftime("%Y-%m-%d_%H%M%S") + ".json"
    history_file = get_base_path() / "reports" / "history" / filename
    return save_json(report, history_file)


def save_outbox(report: Dict[str, Any]) -> Path:
    """Enqueues report to reports/outbox directory for API synchronization.

    Args:
        report (Dict[str, Any]): Report data dictionary.

    Returns:
        Path: Saved outbox file path.
    """
    filename = datetime.now().strftime("%Y-%m-%d_%H%M%S") + ".json"
    outbox_file = get_base_path() / "reports" / "outbox" / filename
    return save_json(report, outbox_file)
