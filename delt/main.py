import re
from datetime import timedelta

import arrow
import typer
from typing_extensions import Annotated

app = typer.Typer()


def format_duration(duration: timedelta, append_ago: bool = False) -> str:
    """Format the duration into a human-readable string."""
    seconds = duration.total_seconds()
    intervals = (
        (31536000, "year", "years"),
        (2592000, "month", "months"),
        (604800, "week", "weeks"),
        (86400, "day", "days"),
        (3600, "hour", "hours"),
        (60, "minute", "minutes"),
        (1, "second", "seconds"),
    )
    parts = []
    for limit, singular, plural in intervals:
        if seconds >= limit:
            value = int(seconds // limit)
            parts.append(f"{value} {singular if value == 1 else plural}")
            seconds %= limit
    result = ", ".join(parts)
    return f"{result} ago" if append_ago else result


def calculate_elapsed_time(start: str, end: str) -> str:
    """Calculate the elapsed time between two timestamps."""
    start_time = arrow.get(start)
    end_time = arrow.get(end)
    duration = end_time - start_time
    return format_duration(duration, append_ago=False)


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
        elapsed_time = calculate_elapsed_time(
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
