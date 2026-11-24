import psutil

from healthcheck.models import CheckResult, evaluate


def check_memory(warn: float, crit: float) -> CheckResult:
    """Check RAM usage in percent against warning and critical thresholds"""
    ram = psutil.virtual_memory()
    usage_percent = ram.percent
    ram_status = evaluate(usage_percent, warn, crit)
    return CheckResult(
        "memory", ram_status, usage_percent, f"RAM usage {usage_percent:.2f}%"
    )
