import re
from typing import Optional

import arrow
import typer
from typing_extensions import Annotated

__VERSION__ = "0.3.1"

app = typer.Typer()


def format_duration(duration: int, from_now: bool) -> str:
    """
    Given a time delta (in seconds), return a human-readable string.
    Consider if the seconds is a negative value, the time delta is in the future.
    format the time delta in a human-readable format using ago() or humanize() method.
    :param duration:    The time delta to format (in seconds).
    :param from_now:    If True, return a relative time delta.
    :return: str        A human-readable string representing the time delta.
    """
    # Check if the duration is +- 5 seconds
    if -10 < duration < 10:
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


def calculate_delta_seconds(start: str, end: Optional[str] = None) -> str:
    """
    Calculate the elapsed time between two timestamps.

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
        (end_time - start_time).total_seconds()
    )  # This will be positive if end_time is in the future. Negative if in the past.
    # return the formatted duration, from_now should be True if end_time is not within 10 seconds of now.

    return format_duration(duration, from_now)

def version_callback(value: bool):
    if value:
        typer.echo(f"delt version {__VERSION__}")
        raise typer.Exit()


@app.command()
def main(
    start: Annotated[
        str, typer.Argument(help="First timestamp, formatted as 'YYYY-MM-DD HH:mm:ss'")
    ],
    end: Annotated[
        str,
        typer.Argument(help="Second timestamp, formatted as 'YYYY-MM-DD HH:mm:ss'"),
    ] = None,
    version: Optional[bool] = typer.Option(
        None, "--version", "-v", callback=version_callback)

) -> None:
    """Calculate the human-readable elapsed time between two ServiceNow (YYYY-MM-DD HH:mm:ss) formatted timestamps."""

    # Check if start matches the format 'YYYY-MM-DD' and end matches the format 'HH:mm:ss'
    # Assume the user forgot to quote the timestamps and concatenate them.
    if end is not None:
        if re.match(r"^\d{4}-\d{2}-\d{2}$", start) and re.match(
            r"^\d{2}:\d{2}:\d{2}$", end
        ):
            # Assume the user forgot to quote the timestamps and concatenate them
            start, end = f"{start} {end}", None
    try:
        # Calculate the elapsed time
        elapsed_time = calculate_delta_seconds(start, end)

        typer.echo(
            f"Elapsed time from '{start}' to {end}:\n{elapsed_time}"
        )

    except arrow.parser.ParserError:
        # Handle parsing errors specifically related to arrow
        typer.echo(
            "Error: One of the timestamps is not in the correct format. Please use 'YYYY-MM-DD HH:mm:ss'."
        )
        raise typer.Exit(code=1)

    except Exception as e:
        # Handle any other exceptions that may occur
        typer.echo(f"An unexpected error occurred: {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
