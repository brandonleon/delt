# delt

**delt** is a command-line tool designed for calculating the elapsed time between two timestamps in a human-readable format.
It leverages the `Arrow` library for handling date and time manipulations and `Typer` for creating a user-friendly command-line interface.

## Features

- Calculate the time difference between two timestamps.
- Presents results in a human-readable format, indicating whether the time is in the past or future.
- Handles edge cases (e.g., when timestamps are within 10 seconds of the current time).
- Display the current version of the tool.
- Continuously display remaining time until a future timestamp with `--countdown`.

## Installation

To install the tool using `uv`, run:

``` bash
uv tool install https://github.com/brandonleon/delt.git
```

## Usage

Once installed, you can access the tool using the `delt` command:

``` bash
delt <start_timestamp> [<end_timestamp>] [OPTIONS]
```

### Options

- `-e`, `--exact`  
  Show the exact elapsed time as weeks, days, hours, minutes, and seconds.

- `-v`, `--version`
  Display the current version of the tool.
- `-c`, `--countdown`
  Show a live countdown until the start timestamp.


### Examples

1. **Calculate time difference between two timestamps:**

    ``` bash
    delt "2024-11-14 15:00:00" "2024-11-14 16:00:00"
    ```

    Output:
    ``` text
    Time difference from '2024-11-14 15:00:00' to '2024-11-14 16:00:00':
    1 hour.
    ```

2. **Calculate time since a past timestamp (from 'now'):**

    ``` bash
    delt "2024-11-14 15:00:00"
    ```

    Output (varies based on current time):
    ``` text
    Time since '2024-11-14 15:00:00':
    10 minutes ago.
    ```

3. **Calculate time until a future timestamp:**

    ``` bash
    delt "2025-12-31 23:59:59"
    ```

    Output (varies based on current time):
    ``` text
    Time until '2025-12-31 23:59:59':
    in 1 year.
    ```

4. **Show exact breakdown with all time units:**

    ``` bash
    delt "2024-01-01 00:00:00" "2024-01-02 03:45:30" --exact
    ```

    Output:
    ``` text
    Time difference from '2024-01-01 00:00:00' to '2024-01-02 03:45:30':
    1 day, 3 hours, 45 minutes, 30 seconds
    ```

5. **Display live countdown until a future timestamp:**

    ``` bash
    delt "2024-12-25 09:00:00" --countdown
    ```

    Output (updates every second):
    ``` text
    Remaining: 5 days
    ```

6. **Use split date and time format (alternative syntax):**

    ``` bash
    delt 2024-11-14 15:00:00
    ```

    This automatically combines the date and time parts.

7. **Compare timestamps within 10 seconds:**

    ``` bash
    delt "2024-11-14 15:00:00" "2024-11-14 15:00:03"
    ```

    Output:
    ``` text
    Time difference from '2024-11-14 15:00:00' to '2024-11-14 15:00:03':
    just now (3 seconds).
    ```

8. **Handle reversed timestamps:**

    ``` bash
    delt "2024-12-01 12:00:00" "2024-01-01 12:00:00"
    ```

    Output:
    ``` text
    Note: Start time is after end time. Showing absolute time difference.

    Time difference from '2024-12-01 12:00:00' to '2024-01-01 12:00:00':
    11 months.
    ```

### Additional Features & Tips

#### Timezone Handling
- Timestamps are parsed in local timezone by default
- Countdown mode explicitly uses local timezone to prevent mismatches
- The tool relies on the Arrow library's timezone handling

#### Edge Cases
- **"Just now" threshold**: Timestamps within 10 seconds show as "just now" with the exact second count
- **Future vs Past**: The tool automatically detects if a timestamp is in the future or past
- **Reversed order**: If start time is after end time, a helpful note is displayed

#### Flexible Input Format
While the primary format is `'YYYY-MM-DD HH:mm:ss'`, you can:
- Split date and time as separate arguments: `delt 2024-11-14 15:00:00`
- Arrow library may support additional formats (experiment with your use case)

#### Keyboard Shortcuts
- **Ctrl+C** in countdown mode: Gracefully cancels the countdown

### Display the Version

To see the version of `delt`, run:

``` bash
delt --version
```

Example output:
``` text
delt version 0.6.2
```

## Dependencies

- **Arrow**: A powerful library for date and time manipulations.
- **Typer**: A library for building intuitive CLI applications.

## Running Tests

The test suite can be run without installing the project as an editable package.
Use `uv` to execute `pytest` via the Python module so the project directory is
added to the import path:

```bash
uv run python -m pytest
```

This ensures the `delt` package is discoverable during collection and execution.

## License

This project is licensed under the [Creative Commons Attribution License (CC BY)](https://creativecommons.org/licenses/by/4.0/).  
You are free to use, distribute, remix, adapt, and build upon this work—even commercially—as long as you credit the original creator.
