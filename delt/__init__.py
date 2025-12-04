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

"""
