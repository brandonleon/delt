"""delt - A command-line tool for calculating elapsed time between timestamps.

This package provides a command-line interface for calculating the human-readable
elapsed time between two timestamps formatted as 'YYYY-MM-DD HH:mm:ss'. It uses
the Arrow library for date and time manipulation, allowing for easy handling of
time zones and formatting.

Features:
-  Calculate the time difference between two timestamps.
-  Output the elapsed time in a human-readable format, indicating whether the
  time is in the past or the future.
-  Handle edge cases such as timestamps within 10 seconds of the current time.
-  Support for version display.

Usage:
    To use this tool, run the following command in your terminal:

    python -m delt <start_timestamp> [<end_timestamp>]

Example:
    python -m delt "2024-11-14 15:00:00" "2024-11-14 16:00:00"

    This will output the elapsed time between the two provided timestamps.

Dependencies:
-  Arrow: A library for handling dates and times.
-  Typer: A library for building command-line interfaces.

Version:
    Current version: 0.3.1

"""

import re
from typing import Annotated

import arrow
import typer

app = typer.Typer()


def format_duration(duration: int, from_now: bool, now_diff: int = 10) -> str:
    """Given a time delta (in seconds), return a human-readable string.

    Consider if the seconds is a negative value, the time delta is in the future.
    format the time delta in a human-readable format using ago() or humanize() method.

    :param duration:    The time delta to format (in seconds).
    :param from_now:    If True, return a relative time delta.
    :param now_diff:    The threshold in seconds to consider as 'just now'.
    :return: str        A human-readable string representing the time delta.
    """
    # Check if the duration is +- now_diff seconds
    if -now_diff < duration < now_diff:
        return "just now."

    # Create an arrow object as a duration from now
    present = arrow.now()
    delta = present.shift(seconds=duration)

    if not from_now:
        return f"{delta.humanize(only_distance=True)}."

    return (
        f"{'in ' if duration < 0 else ''}"
        f"{delta.humanize(only_distance=True)}"
        f"{' ago' if duration > 0 else ''}."
    )


def calculate_delta_seconds(start: str, end: str | None = None) -> str:
    """Calculate the elapsed time between two timestamps.

    If the timestamp is in the past it will be a negative value.

    Args:
        start: The start timestamp.
        end: The end timestamp (optional).

    Returns:
        A string representing the elapsed time between the two timestamps.

    """
    from_now = False
    if end is None:
        # If end is None, assume the end time is now
        end = arrow.now().format("YYYY-MM-DD HH:mm:ss")
        from_now = True

    start_time = arrow.get(start)
    end_time = arrow.get(end)

    # Calculate the duration in seconds
    duration = int(
        (end_time - start_time).total_seconds(),
    )  # This will be positive if end_time is in the future. Negative if in the past.

    return format_duration(duration, from_now)


def version_callback(value: bool) -> None:
    """Print the version of the application if requested.

    This callback function is triggered when the --version or -v option is
    specified. It prints the current version of the application and exits.
    """
    if value:
        from importlib.metadata import PackageNotFoundError, version

        try:
            typer.echo(f"delt version {version('delt')}")
        except PackageNotFoundError:
            typer.echo("Version information not found.")
        raise typer.Exit


# noinspection PyUnusedLocal
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
    version: bool | None = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
    ),
) -> None:
    """Calculate the human-readable elapsed time between two timestamps."""
    # Check if start matches the format 'YYYY-MM-DD'
    # and end matches the format 'HH:mm:ss'
    # Assume the user forgot to quote the timestamps and concatenate them.
    if (
        end is not None
        and re.match(r"^\d{4}-\d{2}-\d{2}$", start)
        and re.match(r"^\d{2}:\d{2}:\d{2}$", end)
    ):
        # Assume the user forgot to quote the timestamps and concatenate them
        start, end = f"{start} {end}", None
    try:
        # Calculate the elapsed time
        elapsed_time = calculate_delta_seconds(start, end)

        if (
            end is None and arrow.get(start) > arrow.now()
        ):  # If the start time is in the future
            start, end = end, start

        typer.echo(
            f"Elapsed time from '{'now' if start is None else start}' "
            f"to '{'now' if end is None else end}':\n{elapsed_time}",
        )

    except arrow.parser.ParserError as e:
        # Handle parsing errors specifically related to arrow
        typer.echo(
            "Error: One of the timestamps is not in the correct format. "
            "Please use 'YYYY-MM-DD HH:mm:ss'.",
        )
        raise typer.Exit(code=1) from e

    except Exception as e:
        # Handle any other exceptions that may occur
        typer.echo(f"An unexpected error occurred: {e}")
        raise typer.Exit(code=1) from e


if __name__ == "__main__":
    app()
