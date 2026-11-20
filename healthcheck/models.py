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
    """Function to evaluate threshold depending on given value and set warning and critical thresholds. Warning can't be greater than or equal to critical value. Function returns Status"""
    if warn >= crit:
        raise ValueError("Warning threshold can't be greater than or equal to critical")
    if value >= crit:
        return Status.CRITICAL
    elif value >= warn:
        return Status.WARNING
    else:
        return Status.OK
