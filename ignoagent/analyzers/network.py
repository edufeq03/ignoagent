"""Network analyzer module.

Analyzes open ports output for sensitive exposed services.
"""

from typing import Dict, Any, List, Optional


def analyze_ports(open_ports: Optional[str]) -> Dict[str, Any]:
    """Analyzes open listening network ports against known security risks.

    Args:
        open_ports (Optional[str]): String output from listening sockets command.

    Returns:
        Dict[str, Any]: Network risk assessment score, alerts, and recommendations.
    """
    risks: List[str] = []
    recommendations: List[str] = []

    if not open_ports:
        return {
            "risk_score": 0,
            "alerts": [],
            "recommendations": []
        }

    checks = {
        "2377": {
            "alert": "Docker Swarm Manager exposto publicamente",
            "recommendation": "Bloquear porta 2377 no firewall"
        },
        "7946": {
            "alert": "Porta de comunicação Docker Swarm detectada",
            "recommendation": "Avaliar necessidade de exposição externa"
        },
        "3000": {
            "alert": "Serviço web administrativo detectado na porta 3000",
            "recommendation": "Manter protegido por firewall ou proxy reverso"
        },
        "22": {
            "alert": "SSH padrão exposto",
            "recommendation": "Alterar porta SSH ou restringir por IP"
        }
    }

    for port, data in checks.items():
        if f":{port}" in open_ports:
            risks.append(data["alert"])
            recommendations.append(data["recommendation"])

    score = len(risks) * 15

    return {
        "risk_score": score,
        "alerts": risks,
        "recommendations": recommendations
    }
