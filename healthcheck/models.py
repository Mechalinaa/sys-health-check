import math
from dataclasses import dataclass
from enum import IntEnum


class Status(IntEnum):
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3


@dataclass
class CheckResult:
    name: str
    status: Status
    value: float | str
    message: str


def evaluate(value: float, warn: float, crit: float) -> Status:
    """Compare a measured value against warning and critical thresholds.

    A value equal to a threshold already counts as that threshold's status:
    value >= crit is CRITICAL, value >= warn is WARNING, anything lower is OK.

    Raises:
        ValueError: if the value is negative or warn >= crit. Both mean a bug
            in the code or the configuration, which someone has to fix.

    Returns:
        Status.UNKNOWN if the value is NaN (the measurement failed), otherwise
        the status that matches the thresholds.
    """
    if value < 0:
        raise ValueError("Value must be greater than or equal to 0")
    if warn >= crit:
        raise ValueError("Warning threshold can't be greater than or equal to critical")
    if math.isnan(value):
        return Status.UNKNOWN
    if value >= crit:
        return Status.CRITICAL
    elif value >= warn:
        return Status.WARNING
    else:
        return Status.OK


SEVERITY_ORDER = [Status.OK, Status.UNKNOWN, Status.WARNING, Status.CRITICAL]


def worst_status(statuses: list[Status]) -> Status:
    """Return the most severe status from the list.

    Severity follows SEVERITY_ORDER (CRITICAL is the worst), not the numeric
    value of Status, because that value is the process exit code and
    UNKNOWN (3) would otherwise outrank CRITICAL (2).

    Returns:
        The most severe status, or Status.UNKNOWN for an empty list,
        because no checks were run.
    """
    return max(statuses, key=SEVERITY_ORDER.index, default=Status.UNKNOWN)
