import re
import time
from typing import Annotated

import arrow
import typer
from arrow.parser import ParserError

app = typer.Typer()

# Time units in seconds for duration calculations
TIME_UNITS = [
    ("year", 31536000),
    ("month", 2592000),
    ("week", 604800),
    ("day", 86400),
    ("hour", 3600),
    ("minute", 60),
    ("second", 1),
]


def format_duration(
    duration: int,
    from_now: bool,
    now_diff: int = 10,
    exact: bool = False,
    reverse: bool = False,
    in_countdown: bool = False,
) -> str:
    """Given a time delta (in seconds), return a human-readable string or exact breakdown."""
    if exact:
        return format_exact_duration_parts(duration)
    if -now_diff < duration < now_diff:
        actual_seconds = abs(duration)
        return (
            f"just now ({actual_seconds} second{'s' if actual_seconds != 1 else ''})."
        )
    seconds = abs(duration)
    for name, count in TIME_UNITS:
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

    # For countdown mode, return just the time without "in" prefix
    if in_countdown:
        return result

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
    parts = []
    for name, count in TIME_UNITS:
        value, seconds = divmod(seconds, count)
        if value:
            parts.append(f"{value} {name}{'s' if value != 1 else ''}")
    if not parts:
        parts.append("0 seconds")
    return ", ".join(parts)


def calculate_delta_seconds(
    start: str, end: str | None = None, exact: bool = False, in_countdown: bool = False
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
    if from_now and not in_countdown:
        duration = -duration  # Reverse the duration for "from now" comparisons
    return format_duration(duration, from_now, exact=exact, in_countdown=in_countdown)


def run_countdown(target: str, exact: bool = False) -> None:
    """Continuously display the time remaining until ``target``."""
    # Parse the target time and try to set it to local timezone
    target_time = arrow.get(target)
    try:
        # Get the local timezone from a reference time and apply it to target
        local_tz = arrow.now().tzinfo
        target_time = target_time.replace(tzinfo=local_tz)
    except AttributeError:
        # Fallback for testing or when tzinfo is not available
        pass
    try:
        while True:
            now = arrow.now()
            remaining = int((target_time - now).total_seconds())
            if remaining <= 0:
                # Clear the line and show completion message
                typer.echo("\rTime's up!           ")
                break
            duration_str = format_duration(
                -remaining, from_now=True, exact=exact, in_countdown=True
            )
            # Use carriage return to overwrite the same line
            typer.echo(f"\rRemaining: {duration_str}    ", nl=False)
            time.sleep(1)
    except KeyboardInterrupt:
        # Clear the line before showing cancellation message
        typer.echo("\r" + " " * 50 + "\r", nl=False)
        typer.echo("Countdown cancelled.")


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
        typer.Argument(
            help="First timestamp, formatted as 'YYYY-MM-DD HH:mm:ss' (or split as 'YYYY-MM-DD' 'HH:mm:ss')"
        ),
    ],
    end: Annotated[
        str | None,
        typer.Argument(
            help="Second timestamp, formatted as 'YYYY-MM-DD HH:mm:ss' (omit to compare with 'now')"
        ),
    ] = None,
    exact: bool = typer.Option(
        False,
        "--exact",
        "-e",
        help="Show exact time breakdown (years, months, weeks, days, hours, minutes, seconds).",
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

        # Validate timestamps and provide helpful message if reversed
        start_time = arrow.get(start)
        end_time = arrow.get(end) if end is not None else arrow.now()

        if end is not None and start_time > end_time:
            typer.echo(
                "Note: Start time is after end time. Showing absolute time difference.\n",
                err=False,
            )

        elapsed_time = calculate_delta_seconds(start, end, exact=exact)
        if end is None and start_time > arrow.now():
            typer.echo(
                f"Time until '{start}':\n{elapsed_time}",
            )
        elif end is None and start_time < arrow.now():
            typer.echo(
                f"Time since '{start}':\n{elapsed_time}",
            )
        else:
            typer.echo(
                f"Time difference from '{start}' to '{end if end is not None else 'now'}':\n{elapsed_time}",
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
