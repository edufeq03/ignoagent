"""Sender queue output module."""

from typing import Any, Dict
from ignoagent.outputs.file import save_outbox


def send(report: Dict[str, Any]) -> str:
    """Enqueues report payload to outbox.

    Args:
        report (Dict[str, Any]): Report payload.

    Returns:
        str: Outbox file path string.
    """
    outbox_path = save_outbox(report)
    return str(outbox_path)
