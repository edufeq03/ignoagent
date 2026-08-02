"""System metrics collector.

Collects CPU, memory, disk, and uptime metrics.
"""

import shutil
import time
from typing import Dict, Any
import psutil


def collect() -> Dict[str, Any]:
    """Collects system metrics.

    Returns:
        Dict[str, Any]: Collected metrics dictionary containing CPU, memory,
        disk usage, and uptime.
    """
    disk = shutil.disk_usage("/")

    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk": {
            "total_gb": round(disk.total / (1024**3), 2),
            "used_gb": round(disk.used / (1024**3), 2),
            "free_gb": round(disk.free / (1024**3), 2),
            "percent": round(
                (disk.used / disk.total) * 100,
                2
            )
        },
        "uptime_seconds": int(
            time.time() - psutil.boot_time()
        )
    }
