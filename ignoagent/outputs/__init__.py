"""Outputs module for IgnoAgent."""

from ignoagent.outputs.file import save_history, save_outbox, save_report, save_status
from ignoagent.outputs.sender import send

__all__ = ["save_history", "save_outbox", "save_report", "save_status", "send"]
