import math
from unittest.mock import patch

import pytest

from healthcheck.checks.system import check_cpu, check_memory
from healthcheck.models import Status

ram_percent = [(15, Status.OK), (81, Status.WARNING), (99, Status.CRITICAL)]
cpu_parameters = [(15, Status.OK), (81, Status.WARNING), (99, Status.CRITICAL)]


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


@patch("healthcheck.checks.system.psutil.cpu_percent")
def test_check_cpu_critical(mock_cpu):
    mock_cpu.return_value = 91.5
    result = check_cpu(warn=80, crit=90)

    assert result.name == "cpu"
    assert result.status == Status.CRITICAL
    assert result.value == 91.5
    assert "91.50%" in result.message
    mock_cpu.assert_called_once_with(interval=1)


@pytest.mark.parametrize("value, expected", cpu_parameters)
@patch("healthcheck.checks.system.psutil.cpu_percent")
def test_check_cpu_all(mock_cpu, value, expected):
    mock_cpu.return_value = value
    result = check_cpu(warn=80, crit=90)

    assert result.status == expected
    assert result.value == value


@patch("healthcheck.checks.system.psutil.cpu_percent")
def test_check_cpu_returns_unknown_on_psutil_oserror(mock_cpu):
    mock_cpu.side_effect = OSError("Cannot read /proc/stat")
    result = check_cpu(warn=80, crit=90)

    assert result.name == "cpu"
    assert result.status == Status.UNKNOWN
    assert math.isnan(result.value)
    assert "/proc/stat" in result.message


@patch("healthcheck.checks.system.psutil.cpu_percent")
def test_check_cpu_invalid_thresholds(mock_cpu):
    mock_cpu.return_value = 67
    with pytest.raises(
        ValueError, match="Warning threshold can't be greater than or equal to critical"
    ):
        check_cpu(warn=80, crit=80)
