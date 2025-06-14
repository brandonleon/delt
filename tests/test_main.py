from datetime import datetime

from delt import main

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


def test_run_countdown_date(monkeypatch) -> None:
    outputs: list[str] = []

    monkeypatch.setattr(main.typer, "echo", lambda msg: outputs.append(msg))

    arrow_mod = main.arrow

    def fake_get(date_str: str) -> arrow_mod.Arrow:
        fmt = "%Y-%m-%d" if len(date_str) == 10 else "%Y-%m-%d %H:%M:%S"
        return arrow_mod.Arrow(datetime.strptime(date_str, fmt))

    times = iter(
        [
            arrow_mod.Arrow(datetime(2028, 7, 6, 0, 0, 0)),
            arrow_mod.Arrow(datetime(2028, 7, 7, 0, 0, 0)),
        ]
    )

    monkeypatch.setattr(main.arrow, "get", fake_get)
    # The 'times' iterator is intentionally limited to two values to simulate specific timestamps.
    # Adding a safeguard to prevent StopIteration errors if 'times' is exhausted.
    monkeypatch.setattr(
        main.arrow,
        "now",
        lambda: next(times, arrow_mod.Arrow(datetime(1970, 1, 1, 0, 0, 0))),
    )
    monkeypatch.setattr(main.time, "sleep", lambda _: None)

    main.run_countdown("2028-07-07")

    assert outputs[0].startswith("Remaining: in ")
