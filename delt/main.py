import re

import arrow
import typer
from typing_extensions import Annotated

app = typer.Typer()


def format_duration(duration: int) -> str:
    """
    Given a time delta (in seconds), return a human-readable string.
    Consider if the seconds is a negative value, the time delta is in the future.
    format the time delta in a human-readable format using ago() or humanize() method.
    :param duration:    The time delta to format (in seconds).
    :return: str        A human-readable string representing the time delta.
    """
    # Check if the duration is +- 5 seconds
    if -10 < duration < 10:
        return "just now."

    # Create an arrow object as a duration from now
    present = arrow.utcnow()
    delta = present.shift(seconds=duration)

    return (f"{'in ' if duration < 0 else ''}"
            f"{delta.humanize(only_distance=True)}"
            f"{' ago' if duration > 0 else ''}.")


def calculate_delta_seconds(start: str, end: str) -> str:
    """
    Calculate the elapsed time between two timestamps.

    If the timestamp is in the past it will be a negative value.

    Args:
        start: The start timestamp.
        end: The end timestamp (optional).

    Returns:
        A string representing the elapsed time between the two timestamps.
    """

    start_time = arrow.get(start)
    end_time = arrow.get(end)

    # Calculate the duration in seconds
    duration = int(
        (end_time - start_time).total_seconds()
    )  # This will be positive if end_time is in the future. Negative if in the past.

    return format_duration(duration)


@app.command()
def main(
    start: Annotated[
        str, typer.Argument(help="First timestamp, formatted as 'YYYY-MM-DD HH:mm:ss'")
    ],
    end: Annotated[
        str,
        typer.Argument(help="Second timestamp, formatted as 'YYYY-MM-DD HH:mm:ss'"),
    ] = None,
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
        # Parse the end timestamp or use the current time if not provided
        end_time = arrow.now() if end is None else arrow.get(end)

        # Calculate the elapsed time
        elapsed_time = calculate_delta_seconds(
            start, end_time.format("YYYY-MM-DD HH:mm:ss")
        )

        end_time_str = end_time.format("YYYY-MM-DD HH:mm:ss")
        typer.echo(f"Elapsed time from '{start}' to {end_time_str}:\n{elapsed_time}")

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
