from delt.main import (
    calculate_delta_seconds,
    format_exact_duration_parts,
    run_countdown,
)


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


def test_run_countdown(monkeypatch) -> None:
    outputs: list[str] = []

    monkeypatch.setattr("delt.main.typer.echo", lambda msg: outputs.append(msg))

    start_time = run_countdown.__globals__["arrow"].get("2024-01-01 00:00:00")
    times = [
        start_time,
        start_time.shift(seconds=12),
    ]

    monkeypatch.setattr("delt.main.arrow.now", lambda: times.pop(0))
    monkeypatch.setattr("delt.main.time.sleep", lambda _s: None)

    target = start_time.shift(seconds=12).format("YYYY-MM-DD HH:mm:ss")
    run_countdown(target)

    assert "Remaining: in" in outputs[0]
    assert outputs[-1] == "Time's up!"
    assert len(outputs) == 2
