from datetime import timedelta

import arrow
import typer
from typing_extensions import Annotated


def format_duration(duration: timedelta, append_ago: bool = False) -> str:
    """Format the duration into a human-readable string."""
    seconds = duration.total_seconds()

    # Define time intervals in seconds
    intervals = (
        (31536000, "year", "years"),  # 365 days
        (2592000, "month", "months"),  # 30 days
        (604800, "week", "weeks"),  # 7 days
        (86400, "day", "days"),  # 1 day
        (3600, "hour", "hours"),  # 1 hour
        (60, "minute", "minutes"),  # 1 minute
        (1, "second", "seconds"),  # 1 second
    )

    parts = []
    for limit, singular, plural in intervals:
        if seconds >= limit:
            value = int(seconds // limit)  # Use floor division for whole units
            parts.append(f"{value} {singular if value == 1 else plural}")
            seconds %= limit  # Get the remainder for the next lower interval

    result = ", ".join(parts)
    return f"{result} ago" if append_ago else result


def calculate_elapsed_time(start: str, end: str) -> str:
    """Calculate the elapsed time between two timestamps."""
    start_time = arrow.get(start)
    end_time = arrow.get(end)
    duration = end_time - start_time
    return format_duration(duration, append_ago=False)


def main(
    start: Annotated[
        str, typer.Argument(help="First timestamp, formatted as 'YYYY-MM-DD HH:mm:ss'")
    ],
    end: Annotated[
        str,
        typer.Argument(help="Second timestamp, formatted as 'YYYY-MM-DD HH:mm:ss'"),
    ] = None,
) -> None:
    """
    Calculate the human-readable elapsed time between two ServiceNow (YYYY-MM-DD HH:mm:ss) formatted timestamps.
    """
    start_time = arrow.get(start)
    end_time = arrow.now() if end is None else arrow.get(end)
    if end:
        elapsed_time = calculate_elapsed_time(start, end)
    else:
        elapsed_time = format_duration(end_time - start_time, True)
    end_time_str = end_time.format("YYYY-MM-DD HH:mm:ss")
    typer.echo(f"Elapsed time from '{start}' to {end_time_str}:\n{elapsed_time}")


if __name__ == "__main__":
    typer.run(main)