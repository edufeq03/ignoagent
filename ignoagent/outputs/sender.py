"""Sender queue and synchronization output module."""

from typing import Any, Dict
from ignoagent.outputs.api import sync_outbox
from ignoagent.outputs.file import save_outbox
from ignoagent.utils.logger import logger


def send(report: Dict[str, Any]) -> str:
    """Enqueues report payload to outbox and triggers outbox synchronization.

    Args:
        report (Dict[str, Any]): Report payload.

    Returns:
        str: Outbox file path string.
    """
    outbox_path = save_outbox(report)
    
    # Tenta sincronizar a fila do outbox com a API Central imediatamente
    sent_count = sync_outbox()
    if sent_count > 0:
        logger.info("Transmitido(s) %d relatório(s) da pasta Outbox para a API Central com sucesso!", sent_count)

    return str(outbox_path)
