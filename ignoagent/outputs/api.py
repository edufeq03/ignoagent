"""Central API synchronization output handler."""

import json
from pathlib import Path
from typing import Any, Dict, Optional
import urllib.error
import urllib.request

from ignoagent.utils.config import load_config
from ignoagent.utils.filesystem import get_base_path
from ignoagent.utils.identity import get_instance_id
from ignoagent.utils.logger import logger

DEFAULT_API_URL = "http://localhost:8000/v1/reports"


def send_to_api(report: Dict[str, Any], api_url: Optional[str] = None, token: Optional[str] = None) -> bool:
    """Sends a single report payload to the Central API endpoint.

    Args:
        report (Dict[str, Any]): Report payload dictionary.
        api_url (Optional[str]): API endpoint URL.
        token (Optional[str]): Bearer token for authentication.

    Returns:
        bool: True if successfully sent and acknowledged (HTTP 200/201/202), False otherwise.
    """
    config = load_config()
    target_url = api_url or config.get("api", {}).get("url", DEFAULT_API_URL)
    auth_token = token or config.get("api", {}).get("token", "ignt_tok_default")

    agent_info = report.get("agent", {})
    instance_id = agent_info.get("instance_id") or get_instance_id()
    agent_version = agent_info.get("version", "0.1.0")

    payload_bytes = json.dumps(report, ensure_ascii=False).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth_token}",
        "X-Instance-ID": instance_id,
        "X-Protocol-Version": "1.0",
        "X-Agent-Version": agent_version,
    }

    req = urllib.request.Request(
        target_url,
        data=payload_bytes,
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status in (200, 201, 202):
                logger.info("Relatório enviado com sucesso para API Central (%s). HTTP %d", target_url, response.status)
                return True
            else:
                logger.warning("API Central retornou status inesperado: HTTP %d", response.status)
                return False
    except urllib.error.HTTPError as e:
        logger.error("Erro HTTP ao enviar relatório para API Central (%s): HTTP %d %s", target_url, e.code, e.reason)
        return False
    except urllib.error.URLError as e:
        logger.warning("API Central indisponível (%s): %s. Relatório mantido no outbox.", target_url, e.reason)
        return False
    except Exception as e:
        logger.error("Erro inesperado ao sincronizar com API Central: %s", str(e))
        return False


def sync_outbox(api_url: Optional[str] = None) -> int:
    """Scans reports/outbox/ directory and attempts to send pending reports to the Central API.

    Transmitted reports are deleted from the local outbox queue upon HTTP confirmation.

    Args:
        api_url (Optional[str]): API endpoint URL override.

    Returns:
        int: Count of successfully sent reports.
    """
    outbox_dir = get_base_path() / "reports" / "outbox"
    if not outbox_dir.exists():
        return 0

    pending_files = sorted(list(outbox_dir.glob("*.json")))
    if not pending_files:
        return 0

    sent_count = 0
    for file_path in pending_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                report_data = json.load(f)

            if send_to_api(report_data, api_url=api_url):
                file_path.unlink(missing_ok=True)
                sent_count += 1
            else:
                # Interrompe o loop no primeiro erro para preservar a ordem temporal e evitar tentativas repetidas
                break
        except Exception as e:
            logger.error("Erro ao processar relatório do outbox (%s): %s", file_path.name, str(e))

    return sent_count
