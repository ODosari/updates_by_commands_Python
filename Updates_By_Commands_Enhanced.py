# Name: "updates_commands_python"
# Version: "0.5"
# By: "Obaid Aldosari"
# GitHub: "https://github.com/ODosari/UpdatesTerminalCommandsPython"

import subprocess
import json
import os
import datetime
import time
import logging
from logging.handlers import RotatingFileHandler

from System_Checks import check_platform, check_internet_connection

CONFIG_FILE_PATH = "Updates_By_Commands_Config.json"
LOG_FILE_PATH = "Updates_By_Commands_Log.log"


def check_file_status():
    """Check and notify the user about the existence of config and log files."""
    check_config_exists = os.path.exists(CONFIG_FILE_PATH)
    log_exists = os.path.exists(LOG_FILE_PATH)

    # Notify about the config and log file status
    if check_config_exists:
        print(
            f"\033[1;94mConfiguration file already exists at:\033[0m {os.path.abspath(CONFIG_FILE_PATH)}"
        )
    else:
        print(
            f"\033[1;94mConfiguration file will be created at:\033[0m {os.path.abspath(CONFIG_FILE_PATH)}"
        )

    if log_exists:
        print(
            f"\033[1;94mLog file already exists at:\033[0m {os.path.abspath(LOG_FILE_PATH)}"
        )
    else:
        print(
            f"\033[1;94mLog file will be created at:\033[0m {os.path.abspath(LOG_FILE_PATH)}"
        )

    return check_config_exists


def setup_logging():
    """Set up logging after checking the log file status."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            RotatingFileHandler(LOG_FILE_PATH, maxBytes=10**6, backupCount=5),
        ],
    )


def create_config(file_path=CONFIG_FILE_PATH):
    """Create a configuration file with default or user-specified commands."""
    default_commands = [
        "brew upgrade && brew cleanup && brew autoremove",
        "conda update --all -y",
        "rustup update",
        "npm update",
        "gcloud components update",
    ]

    print("Default commands are:")
    for cmd in default_commands:
        print("-", cmd)

    while True:
        use_default = (
            input("Do you want to use the default commands? (Y/n) ").strip().lower()
        )
        if use_default in ["y", "n", ""]:
            break
        print("Invalid input. Please enter 'Y' or 'n'.")

    if use_default == "n":
        while True:
            try:
                num_commands = int(input("How many commands would you like to add? "))
                break
            except ValueError:
                print("Invalid number. Please enter an integer.")

        user_commands = []
        for i in range(num_commands):
            while True:
                cmd = input(f"Enter command {i + 1}: ")
                if cmd.strip():
                    user_commands.append(cmd)
                    break
                print("Command cannot be empty.")

        print("Your custom commands are:")
        for i, cmd in enumerate(user_commands, start=1):
            print(f"{i}. {cmd}")

        while True:
            user_confirm = (
                input("Do you want to save and execute these commands? (Y/n) ")
                .strip()
                .lower()
            )
            if user_confirm in ["y", "n"]:
                break
            print("Invalid input. Please enter 'Y' or 'n'.")

        if user_confirm == "n":
            print("Aborting command addition.")
            return

        commands_to_save = user_commands
    else:
        commands_to_save = default_commands

    with open(file_path, "w") as config_file:
        json.dump({"commands": commands_to_save}, config_file)


def load_commands_from_config(file_path=CONFIG_FILE_PATH):
    """Load commands from a configuration file. Create one if it doesn't exist."""
    if not os.path.exists(file_path):
        create_config(file_path)

    with open(file_path, "r") as config_file:
        try:
            return json.load(config_file).get("commands", [])
        except json.JSONDecodeError:
            logging.error("Configuration file is corrupted. Re-creating it.")
            create_config(file_path)
            with open(file_path, "r") as new_config_file:
                return json.load(new_config_file).get("commands", [])


def log_execution(command, execution_time, file_path=LOG_FILE_PATH):
    """Log a command execution to a file."""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    with open(file_path, "a") as log_file:
        log_file.write(f"[{current_time}] Command: {command}\n")
        log_file.write(f"Execution time: {execution_time:.2f} seconds\n")
        log_file.write(f"{'='*50}\n")


def log_error(message, file_path=LOG_FILE_PATH):
    """Log an error message to a file."""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    with open(file_path, "a") as log_file:
        log_file.write(f"[{current_time}] ERROR: {message}\n{'='*50}\n")


def run_command(update_command, verbose=True):
    """Run a shell command and handle output."""
    try:
        start_time = time.time()
        with subprocess.Popen(
            update_command,
            shell=True,
            executable="/bin/zsh",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,  # Line buffered to handle real-time output
        ) as process:
            stdout_lines = []
            stderr_lines = []

            for line in process.stdout:
                if verbose:
                    print(line, end="")  # Print each line immediately
                stdout_lines.append(line)

            for line in process.stderr:
                if verbose:
                    print(f"\033[1;91m{line}\033[0m", end="")  # Print errors in red
                stderr_lines.append(line)

            process.wait()

        execution_time = time.time() - start_time

        if process.returncode != 0:
            error_msg = f"Command '{update_command}' failed with return code: {process.returncode}"
            log_error(error_msg)
            raise subprocess.CalledProcessError(process.returncode, update_command)
        else:
            log_execution(update_command, execution_time)
    except Exception as e:
        error_msg = f"Command '{update_command}' encountered an error: {e}"
        log_error(error_msg)
        return 1
    return 0


def main(verbose=True):
    """Main function to run the update commands."""
    commands = load_commands_from_config()
    total_commands = len(commands)

    for i, command in enumerate(commands, start=1):
        if verbose:
            print(
                f"\033[1;97mRunning update command \033[1;92m{i} \033[1;97mof \033[1;92m{total_commands}\033[1;97m:\033[0m {command}"
            )

        start_time = time.time()
        run_command(command, verbose)
        end_time = time.time()

        if verbose:
            execution_time = end_time - start_time
            print(f"\033[1;94mExecution time: {execution_time:.2f} seconds\033[0m")


if __name__ == "__main__":
    os_details = check_platform()
    print(f"\033[1;94m==> Operating System Details:\033[0m {os_details}")

    internet_status = check_internet_connection()
    if internet_status:
        print("\033[1;92m==> Internet connection is available.\033[0m")

        # Check and notify about the config and log file status
        config_exists = check_file_status()

        # Setup logging after checking the file status
        setup_logging()

        if config_exists:
            main()  # Proceed without asking if the configuration file already exists
        else:
            main_confirm = (
                input("Do you want to proceed with the updates? (Y/n) ").strip().lower()
            )
            if main_confirm in ["y", ""]:
                main()
            else:
                print("\033[1;91m==> Update process aborted by user.\033[0m")
    else:
        print("\033[1;91m==> No internet connection detected. Exiting.\033[0m")
