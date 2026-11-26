import psutil

from healthcheck.models import CheckResult, Status, evaluate


def check_memory(warn: float, crit: float) -> CheckResult:
    """Check RAM usage in percent against warning and critical thresholds"""
    try:
        ram = psutil.virtual_memory()
    except OSError as e:
        return CheckResult("memory", Status.UNKNOWN, float("nan"), f"RAM usage {e}")
    ram_percent = ram.percent
    ram_status = evaluate(ram_percent, warn, crit)
    return CheckResult(
        "memory", ram_status, ram_percent, f"RAM usage {ram_percent:.2f}%"
    )


def check_cpu(warn: float, crit: float) -> CheckResult:
    """Check CPU usage in percent against warning and critical thresholds"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
    except OSError as e:
        return CheckResult("cpu", Status.UNKNOWN, float("nan"), f"CPU usage {e}")
    cpu_status = evaluate(cpu_percent, warn, crit)
    return CheckResult("cpu", cpu_status, cpu_percent, f"CPU usage {cpu_percent:.2f}%")
