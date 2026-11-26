import psutil

from healthcheck.models import CheckResult, Status, evaluate


def check_memory(warn: float, crit: float) -> CheckResult:
    """Check RAM usage in percent against warning and critical thresholds"""
    try:
        ram = psutil.virtual_memory()
    except OSError as e:
        return CheckResult("memory", Status.UNKNOWN, float("nan"), f"RAM usage {e}")
    usage_percent = ram.percent
    ram_status = evaluate(usage_percent, warn, crit)
    return CheckResult(
        "memory", ram_status, usage_percent, f"RAM usage {usage_percent:.2f}%"
    )
