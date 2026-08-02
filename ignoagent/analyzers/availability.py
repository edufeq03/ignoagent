"""Availability analyzer module.

Analyzes service state and system metrics to identify availability risks.
"""

from typing import Dict, Any, List


def analyze_availability(services: Dict[str, Any], system: Dict[str, Any]) -> Dict[str, Any]:
    """Analyzes system and service state for availability degradation.

    Args:
        services (Dict[str, Any]): Data from services collector.
        system (Dict[str, Any]): Data from system collector.

    Returns:
        Dict[str, Any]: Availability risk assessment score, alerts, and recommendations.
    """
    alerts: List[str] = []
    recommendations: List[str] = []
    score = 0

    failed_services = services.get("failed_services", [])
    if failed_services:
        score += 20 * len(failed_services)
        alerts.append(f"{len(failed_services)} serviço(s) systemd em falha")
        recommendations.append("Verificar logs do systemctl para os serviços falhos")

    disk_percent = system.get("disk", {}).get("percent", 0)
    if disk_percent > 90:
        score += 30
        alerts.append(f"Uso de disco crítico: {disk_percent}%")
        recommendations.append("Liberar espaço em disco imediatamente")

    memory_percent = system.get("memory_percent", 0)
    if memory_percent > 90:
        score += 20
        alerts.append(f"Uso de memória elevado: {memory_percent}%")
        recommendations.append("Identificar processos consumindo muita memória")

    return {
        "risk_score": score,
        "alerts": alerts,
        "recommendations": recommendations
    }
