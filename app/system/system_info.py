import platform
import socket
import time
from datetime import timedelta

import psutil


BOOT_TIME = psutil.boot_time()


def get_system_info():
    """Collect current system information and resource usage."""

    memory = psutil.virtual_memory()
    disk_path = "C:\\" if platform.system() == "Windows" else "/"
    disk = psutil.disk_usage(disk_path)

    uptime_seconds = max(0, int(time.time() - BOOT_TIME))

    return {
        "computer_name": socket.gethostname(),
        "operating_system": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor() or "Unavailable",
        "logical_cores": psutil.cpu_count(logical=True) or "Unavailable",
        "python_version": platform.python_version(),
        "cpu_usage": psutil.cpu_percent(interval=None),
        "ram_used_gb": round(memory.used / (1024 ** 3), 2),
        "ram_total_gb": round(memory.total / (1024 ** 3), 2),
        "ram_usage": memory.percent,
        "disk_used_gb": round(disk.used / (1024 ** 3), 2),
        "disk_total_gb": round(disk.total / (1024 ** 3), 2),
        "disk_usage": disk.percent,
        "uptime": str(timedelta(seconds=uptime_seconds)),
    }