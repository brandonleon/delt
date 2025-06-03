# delt

**delt** is a command-line tool designed for calculating the elapsed time between two timestamps in a human-readable format.
It leverages the `Arrow` library for handling date and time manipulations and `Typer` for creating a user-friendly command-line interface.

## Features

- Calculate the time difference between two timestamps.
- Presents results in a human-readable format, indicating whether the time is in the past or future.
- Handles edge cases (e.g., when timestamps are within 10 seconds of the current time).
- Display the current version of the tool.

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


### Examples

1. Calculate the elapsed time between two timestamps:

    ``` bash
    delt "2024-11-14 15:00:00" "2024-11-14 16:00:00"
    ```

    Output:
    ``` text
    1 hour
    ```

2. Calculate the elapsed time from a given timestamp to the current time:

    ``` bash
    delt "2024-11-14 15:00:00"
    ```

    Output (varies based on the current time):
    ``` text
    10 minutes ago
    ```

### Display the Version

To see the version of `delt`, run:

``` bash
delt --version
```
Output:
``` text
delt version 0.3.7
```

## Dependencies

- **Arrow**: A powerful library for date and time manipulations.
- **Typer**: A library for building intuitive CLI applications.

## License

This project is licensed under the [Creative Commons Attribution License (CC BY)](https://creativecommons.org/licenses/by/4.0/).  
You are free to use, distribute, remix, adapt, and build upon this work—even commercially—as long as you credit the original creator.
