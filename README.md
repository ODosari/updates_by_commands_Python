# Updates Multiple Terminal Commands Using Python

## Overview

This repository contains a Python script for running a series of update commands in a Zsh shell. The script is designed to execute commands for updating Homebrew, Conda, and Rust.

- **Name**: updates_commands_python
- **Version**: 0.1.0
- **By**: Obaid Aldosari
- **GitHub**: [https://github.com/ODosari/UpdatesTerminalCommandsPython](https://github.com/ODosari/UpdatesTerminalCommandsPython)

## Features

- Executes a list of shell commands in a Zsh shell.
- Uses ANSI escape codes for styling the terminal output.
- Handles errors and prints appropriate messages.

## Requirements

- Python 3.x
- Zsh shell

## How to Run

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/ODosari/UpdatesTerminalCommandsPython.git
    ```

2. **Navigate to the Project Directory**:

    ```bash
    cd UpdatesTerminalCommandsPython
    ```

3. **Run the Python Script**:

    ```bash
    python3 Updates_By_Commands_Basic.py
    ```
   For Basic execution, or the following for enhanced script:

    ```bash
    python3 Updates_By_Commands_Enhanced.py
    ```

## Adding More Commands

If you wish to add more commands to the script, you can simply extend the `commands` list in the `main` function. For example:

```python
commands = [
    "brew upgrade && brew cleanup && brew autoremove",
    "conda update --all -y",
    "rustup update",
    "your_new_command_here"  # Add your new command here
]
```

## Code Explanation

### Importing Required Module

The script uses Python's `subprocess` module to run shell commands.

```python
import subprocess
```

### Function to Run Commands

The `run_command` function takes a shell command as an argument and executes it using the Zsh shell.

```python
def run_command(update_commands):
    ...
```

### Main Function

The `main` function contains a list of commands to run. It then loops through each command, prints it with styling, and executes it.

```python
if __name__ == "__main__":
    ...
```

## Contributing

Feel free to fork the project, open a PR, or submit an issue.

---
