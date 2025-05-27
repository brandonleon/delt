import re
from typing import Annotated

import arrow
import typer

app = typer.Typer()


def format_duration(
    duration: int, from_now: bool, now_diff: int = 10, exact: bool = False
) -> str:
    """Given a time delta (in seconds), return a human-readable string or exact breakdown."""
    if exact:
        seconds = abs(duration)
        weeks, seconds = divmod(seconds, 604800)
        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        parts = []
        if weeks:
            parts.append(f"{weeks} week{'s' if weeks != 1 else ''}")
        if days:
            parts.append(f"{days} day{'s' if days != 1 else ''}")
        if hours:
            parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
        if minutes:
            parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
        if seconds or not parts:
            parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
        return ", ".join(parts)
    if -now_diff < duration < now_diff:
        return "just now."
    present = arrow.now()
    delta = present.shift(seconds=duration)
    if not from_now:
        return f"{delta.humanize(only_distance=True)}."
    return (
        f"{'in ' if duration < 0 else ''}"
        f"{delta.humanize(only_distance=True)}"
        f"{' ago' if duration > 0 else ''}."
    )


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
    return format_duration(duration, from_now, exact=exact)


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
    version: bool | None = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
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
        elapsed_time = calculate_delta_seconds(start, end, exact=exact)
        if end is None and arrow.get(start) > arrow.now():
            start, end = end, start
        typer.echo(
            f"Elapsed time from '{'now' if start is None else start}' "
            f"to '{'now' if end is None else end}':\n{elapsed_time}",
        )
    except arrow.parser.ParserError as e:
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
