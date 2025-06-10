from delt.main import calculate_delta_seconds, format_exact_duration_parts


def test_format_exact_duration_parts_positive() -> None:
    assert format_exact_duration_parts(90) == "1 minute, 30 seconds"


def test_format_exact_duration_parts_negative() -> None:
    assert format_exact_duration_parts(-3600) == "1 hour"


def test_calculate_delta_seconds_exact() -> None:
    start = "2024-01-01 00:00:00"
    end = "2024-01-01 00:01:30"
    assert calculate_delta_seconds(start, end, exact=True) == "1 minute, 30 seconds"


def test_calculate_delta_seconds_humanized_single_unit() -> None:
    start = "2024-01-01 00:00:00"
    end = "2024-01-01 01:00:00"
    assert calculate_delta_seconds(start, end) == "1 hour."
