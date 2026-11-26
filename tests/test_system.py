import math
from unittest.mock import patch

import pytest

from healthcheck.checks.system import check_memory
from healthcheck.models import Status

ram_percent = [(15, Status.OK), (81, Status.WARNING), (99, Status.CRITICAL)]


@patch("healthcheck.checks.system.psutil.virtual_memory")
def test_check_memory_critical(mock_vm):
    mock_vm.return_value.percent = 95
    result = check_memory(warn=80, crit=90)

    assert result.name == "memory"
    assert result.status == Status.CRITICAL
    assert result.value == 95
    assert "95.00%" in result.message
    mock_vm.assert_called_once()


@pytest.mark.parametrize("value, expected", ram_percent)
@patch("healthcheck.checks.system.psutil.virtual_memory")
def test_check_memory_all(mock_vm, value, expected):
    mock_vm.return_value.percent = value
    result = check_memory(warn=80, crit=90)

    assert result.status == expected
    assert result.value == value


@patch("healthcheck.checks.system.psutil.virtual_memory")
def test_check_memory_returns_unknown_on_psutil_oserror(mock_vm):
    mock_vm.side_effect = OSError("Cannot read /proc/meminfo")
    result = check_memory(warn=80, crit=90)

    assert result.name == "memory"
    assert result.status == Status.UNKNOWN
    assert math.isnan(result.value)
    assert "/proc/meminfo" in result.message


@patch("healthcheck.checks.system.psutil.virtual_memory")
def test_check_memory_invalid_thresholds(mock_vm):
    mock_vm.return_value.percent = 67
    with pytest.raises(
        ValueError, match="Warning threshold can't be greater than or equal to critical"
    ):
        check_memory(warn=80, crit=80)
