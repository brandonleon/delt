import re
import time
from typing import Annotated, Callable, cast

import arrow
import typer
from arrow.parser import ParserError

app = typer.Typer()


def format_duration(
    duration: int,
    from_now: bool,
    now_diff: int = 10,
    exact: bool = False,
    reverse: bool = False,
) -> str:
    """Given a time delta (in seconds), return a human-readable string or exact breakdown."""
    if exact:
        return format_exact_duration_parts(duration)
    if -now_diff < duration < now_diff:
        return "just now."
    seconds = abs(duration)
    units = [
        ("year", 31536000),
        ("month", 2592000),
        ("week", 604800),
        ("day", 86400),
        ("hour", 3600),
        ("minute", 60),
        ("second", 1),
    ]
    for name, count in units:
        if seconds >= count:
            value = seconds // count
            break
    else:
        value, name = 0, "second"

    result = f"{value} {name}{'s' if value != 1 else ''}"
    if not from_now:
        return result + "."
    if reverse:
        duration = -duration

    if duration > 0:
        return f"in {result}."
    return f"{result} ago."


def format_exact_duration_parts(duration: int) -> str:
    """
    Convert a duration in seconds to a human-readable string with an exact breakdown.

    The output includes years, months, weeks, days, hours, minutes, and seconds,
    omitting any units with a value of zero.

    Args:
        duration (int): The duration in seconds (can be negative).

    Returns:
        str: A comma-separated string listing each non-zero time unit.
    """
    seconds = abs(duration)
    units = [
        ("year", 31536000),
        ("month", 2592000),
        ("week", 604800),
        ("day", 86400),
        ("hour", 3600),
        ("minute", 60),
        ("second", 1),
    ]
    parts = []
    for name, count in units:
        value, seconds = divmod(seconds, count)
        if value:
            parts.append(f"{value} {name}{'s' if value != 1 else ''}")
    if not parts:
        parts.append("0 seconds")
    return ", ".join(parts)


# Type for the calculate_delta_seconds function with the in_countdown attribute
class DeltaCalculator(Callable[[str, str | None, bool], str]):
    in_countdown: bool


def calculate_delta_seconds(
    start: str, end: str | None = None, exact: bool = False
) -> str:
    """Calculate the elapsed time between two timestamps."""
    from_now = False
    if end is None:
        end = arrow.now().format("YYYY-MM-DD HH:mm:ss")
        from_now = True
    start_time = arrow.get(start)
    end_time = arrow.get(end)
    duration = int((end_time - start_time).total_seconds())
    # For "from now" comparisons, we want the direction to be from now to the target time
    # Cast the function to our custom type that includes the in_countdown attribute
    calc_func = cast(DeltaCalculator, calculate_delta_seconds)
    if from_now and not getattr(calc_func, "in_countdown", False):
        duration = -duration  # Reverse the duration for "from now" comparisons
    return format_duration(duration, from_now, exact=exact)


def run_countdown(target: str, exact: bool = False) -> None:
    """Continuously display the time remaining until ``target``."""
    # Get the local timezone from the current time
    local_tz = arrow.now().tzinfo
    # Parse the target time and explicitly set it to local timezone
    target_time = arrow.get(target).replace(tzinfo=local_tz)
    # Cast the function to our custom type that includes the in_countdown attribute
    calc_func = cast(DeltaCalculator, calculate_delta_seconds)
    calc_func.in_countdown = True
    try:
        while True:
            now = arrow.now()
            remaining = int((target_time - now).total_seconds())
            if remaining < 0:
                typer.echo("Time's up!")
                break
            typer.echo(
                f"Remaining: {format_duration(-remaining, from_now=True, exact=exact)}"
            )
            time.sleep(1)
    except KeyboardInterrupt:
        typer.echo("\nCountdown cancelled.")
    finally:
        # Cast the function to our custom type that includes the in_countdown attribute
        calc_func = cast(DeltaCalculator, calculate_delta_seconds)
        calc_func.in_countdown = False


def version_callback(value: bool) -> None:
    if value:
        from importlib.metadata import PackageNotFoundError, version

        try:
            typer.echo(f"delt version {version('delt')}")
        except PackageNotFoundError:
            typer.echo("Version information not found.")
        raise typer.Exit


@app.command()
def main(
    start: Annotated[
        str,
        typer.Argument(help="First timestamp, formatted as 'YYYY-MM-DD HH:mm:ss'"),
    ],
    end: Annotated[
        str | None,
        typer.Argument(help="Second timestamp, formatted as 'YYYY-MM-DD HH:mm:ss'"),
    ] = None,
    exact: bool = typer.Option(
        False,
        "--exact",
        "-e",
        help="Show the exact elapsed time in seconds.",
    ),
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        callback=version_callback,
        is_flag=True,
        is_eager=True,
    ),
    countdown: bool = typer.Option(
        False,
        "--countdown",
        "-c",
        help="Continuously display time remaining until the start timestamp.",
    ),
) -> None:
    """Calculate the human-readable elapsed time between two timestamps."""
    if (
        end is not None
        and re.match(r"^\d{4}-\d{2}-\d{2}$", start)
        and re.match(r"^\d{2}:\d{2}:\d{2}$", end)
    ):
        start, end = f"{start} {end}", None
    try:
        if countdown:
            run_countdown(start, exact=exact)
            return
        elapsed_time = calculate_delta_seconds(start, end, exact=exact)
        if end is None and arrow.get(start) > arrow.now():
            # Don't assign None to start; just adjust the message below
            typer.echo(
                f"Elapsed time from 'now' to '{start}':\n{elapsed_time}",
            )
        else:
            typer.echo(
                f"Elapsed time from '{start}' to '{end if end is not None else 'now'}':\n{elapsed_time}",
            )
    except ParserError as e:
        typer.echo(
            "Error: One of the timestamps is not in the correct format. "
            "Please use 'YYYY-MM-DD HH:mm:ss'.",
        )
        raise typer.Exit(code=1) from e
    except Exception as e:
        typer.echo(f"An unexpected error occurred: {e}")
        raise typer.Exit(code=1) from e


if __name__ == "__main__":
    app()
