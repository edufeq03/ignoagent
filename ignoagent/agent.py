"""Agent core orchestrator module.

Coordinates metrics collection, vulnerability analysis, report compilation, and output persistence.
"""

import platform
import socket
import uuid
from datetime import datetime, timezone
from typing import Dict, Any

from pathlib import Path
from ignoagent.analyzers.network import analyze_ports
from ignoagent.analyzers.risk import analyze as analyze_risk
from ignoagent.collectors.hardening import collect as collect_hardening
from ignoagent.collectors.security import collect as collect_security
from ignoagent.collectors.services import collect as collect_services
from ignoagent.collectors.system import collect as collect_system
from ignoagent.outputs.file import save_history, save_status
from ignoagent.outputs.sender import send
from ignoagent.utils.config import load_config, load_identity
from ignoagent.utils.heartbeat import create_heartbeat
from ignoagent.utils.identity import get_instance_id
from ignoagent.utils.logger import logger


def generate_report() -> Dict[str, Any]:
    """Orchestrates collectors and analyzers to compile and persist status report.

    Returns:
        Dict[str, Any]: Compiled report dictionary.
    """
    identity = load_identity()
    config = load_config()

    system_data = collect_system()
    services_data = collect_services()
    hardening_data = collect_hardening()
    security_data = collect_security()

    risk_analysis = analyze_risk(security_data)
    network_analysis = analyze_ports(hardening_data.get("open_ports"))

    agent_cfg = config.get("agent", {})
    agent_metadata = {**identity, **agent_cfg, "instance_id": get_instance_id()}
    report_id = f"rep_{uuid.uuid4().hex}"

    report = {
        "report_id": report_id,
        "agent": agent_metadata,
        "heartbeat": create_heartbeat(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "server": {
            "hostname": socket.gethostname(),
            "os": platform.platform(),
            "python": platform.python_version(),
        },
        "system": system_data,
        "services": services_data,
        "hardening": hardening_data,
        "security": security_data,
        "analysis": risk_analysis,
        "network_analysis": network_analysis,
    }

    status_file = save_status(report)
    history_file = save_history(report)
    outbox_file = send(report)
    outbox_dir = Path(outbox_file).parent

    logger.info("====================================================================")
    logger.info("IgnoAgent — Execução de Auditoria Concluída com Sucesso")
    logger.info("====================================================================")
    logger.info("Status atualizado:\n          -> %s", status_file)
    logger.info("Histórico registrado:\n          -> %s", history_file)
    logger.info("Pasta Outbox:\n          -> %s", outbox_dir)
    logger.info("Arquivo na Outbox:\n          -> %s", outbox_file)
    logger.info("====================================================================")

    return report


if __name__ == "__main__":
    generate_report()
