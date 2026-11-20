from dataclasses import asdict

import pytest

from healthcheck.models import (
    SEVERITY_ORDER,
    CheckResult,
    Status,
    evaluate,
    worst_status,
)

correct_data = [
    (0, 80, 90, Status.OK),
    (79.9, 80, 90, Status.OK),
    (80, 80, 90, Status.WARNING),
    (89.9, 80, 90, Status.WARNING),
    (89.9, 89.9, 90, Status.WARNING),
    (90, 80, 90, Status.CRITICAL),
    (100, 80, 90, Status.CRITICAL),
]

status_codes = [
    (0, Status.OK),
    (1, Status.WARNING),
    (2, Status.CRITICAL),
    (3, Status.UNKNOWN),
]

worst_status_cases = [
    ([Status.OK, Status.OK], Status.OK),
    ([Status.OK, Status.WARNING], Status.WARNING),
    ([Status.CRITICAL, Status.UNKNOWN], Status.CRITICAL),
    ([Status.UNKNOWN, Status.CRITICAL], Status.CRITICAL),
    ([Status.WARNING, Status.UNKNOWN], Status.WARNING),
    ([Status.OK], Status.OK),
    ([Status.UNKNOWN, Status.CRITICAL, Status.OK, Status.WARNING], Status.CRITICAL),
]


@pytest.mark.parametrize("value, warn, crit, expected", correct_data)
def test_evaluate_status_correct_values(value, warn, crit, expected):
    assert evaluate(value, warn, crit) == expected


def test_evaluate_warn_equals_crit():
    with pytest.raises(
        ValueError, match="Warning threshold can't be greater than or equal to critical"
    ):
        evaluate(50, 80, 80)


def test_evaluate_warn_greater_than_crit():
    with pytest.raises(
        ValueError, match="Warning threshold can't be greater than or equal to critical"
    ):
        evaluate(67, 90, 80)


def test_evaluate_negative_value():
    with pytest.raises(ValueError, match="Value must be greater than or equal to 0"):
        evaluate(-1, 80, 90)


def test_evaluate_value_isnan():
    result = evaluate(float("nan"), 80, 90)
    assert result == Status.UNKNOWN


@pytest.mark.parametrize("code, status", status_codes)
def test_check_status_codes(code, status):
    assert code == status


@pytest.mark.parametrize("status_list, most_severe", worst_status_cases)
def test_most_severe_status(status_list, most_severe):
    assert worst_status(status_list) == most_severe


def test_most_severe_status_empty_list():
    empty = []
    assert worst_status(empty) == Status.UNKNOWN


def test_size_severity_order_matches_intenum():
    assert set(SEVERITY_ORDER) == set(Status)


def test_evaluate_value_isnan_and_wrong_threshold():
    with pytest.raises(
        ValueError, match="Warning threshold can't be greater than or equal to critical"
    ):
        evaluate(float("nan"), 90, 80)


def test_check_result_converts_to_dict():
    result = CheckResult(
        name="cpu", status=Status.WARNING, value=85.0, message="CPU usage 85.0%"
    )

    assert asdict(result) == {
        "name": "cpu",
        "status": Status.WARNING,
        "value": 85.0,
        "message": "CPU usage 85.0%",
    }
