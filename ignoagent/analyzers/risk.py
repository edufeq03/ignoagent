"""Risk analyzer module.

Evaluates security metrics, SSH logins, invalid users, and assigns risk scores and severity levels.
"""

from typing import Dict, Any, List


def analyze(security: Dict[str, Any]) -> Dict[str, Any]:
    """Analyzes security collector metrics for threat levels and vulnerabilities.

    Args:
        security (Dict[str, Any]): Data collected from security collector.

    Returns:
        Dict[str, Any]: Risk score, severity label, alerts list, and recommendations list.
    """
    score = 0
    alerts: List[str] = []
    recommendations: List[str] = []

    failed = security.get("ssh_failed_attempts", 0)
    users = security.get("invalid_users", [])

    if failed > 0:
        score += 10
        alerts.append(f"{failed} tentativas SSH falhas detectadas")
        recommendations.append("Verificar origem das tentativas de login")

    if "root" in users:
        score += 15
        alerts.append("Tentativas de login usando usuário root")
        recommendations.append("Desabilitar login root via SSH")

    if failed > 100:
        score += 25
        alerts.append("Volume elevado de tentativas SSH")

    if score >= 50:
        severity = "HIGH"
    elif score >= 25:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    return {
        "risk_score": score,
        "severity": severity,
        "alerts": alerts,
        "recommendations": recommendations
    }
