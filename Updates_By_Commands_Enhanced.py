# Name = "updates_commands_python"
# Version = "0.3"
# By = "Obaid Aldosari"
# GitHub = "https://github.com/ODosari/UpdatesTerminalCommandsPython"

import subprocess
import json
import os
import datetime

from System_Checks import check_platform, check_internet_connection


def create_config(file_path="Updates_By_Commands_Config.json"):
    """Create a configuration file with default or user-specified commands."""
    default_commands = [
        "brew upgrade && brew cleanup && brew autoremove",
        "conda update --all -y",
        "rustup update",
    ]

    print("Default commands are:")
    for cmd in default_commands:
        print("-", cmd)

    user_input = (
        input("Do you want to use the default commands? (Y/n) ").strip().lower()
    )

    if user_input == "n":
        num_commands = int(input("How many commands would you like to add? "))
        user_commands = [input(f"Enter command {i+1}: ") for i in range(num_commands)]
        commands_to_save = user_commands
    else:
        commands_to_save = default_commands

    with open(file_path, "w") as file:
        json.dump({"commands": commands_to_save}, file)


def load_commands_from_config(file_path="Updates_By_Commands_Config.json"):
    """Load commands from a configuration file. Create one if it doesn't exist."""
    if not os.path.exists(file_path):
        create_config(file_path)

    with open(file_path, "r") as file:
        return json.load(file).get("commands", [])


def run_command(update_commands):
    """Run a shell command using Zsh."""
    try:
        subprocess.run(update_commands, shell=True, executable="/bin/zsh", check=True)
    except subprocess.CalledProcessError as e:
        error_msg = f"Command '{update_commands}' failed with error: {e}"
        print(f"\033[1;91m{error_msg}\033[0m")  # Error message in red
        return error_msg


def log_output(command, output, file_path="Updates_By_Commands_Log.txt"):
    """Log the output of a command to a file."""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    with open(file_path, "a") as file:
        file.write(
            f"[{current_time}] Command: {command}\nOutput:\n{output}\n{'='*50}\n"
        )


def main():
    """Main function to run the update commands."""
    commands = load_commands_from_config()
    total_commands = len(commands)

    for i, command in enumerate(commands, start=1):
        print(
            f"\033[1;97mRunning update command \033[1;92m{i} \033[1;97mof \033[1;92m{total_commands}\033[1;97m:\033[0m {command}"
        )

        output = run_command(command)
        log_output(command, output)


if __name__ == "__main__":
    os_details = check_platform()
    print(f"\033[1;94m==> Operating System Details:\033[0m {os_details}")

    internet_status = check_internet_connection()
    if internet_status:
        print("\033[1;92m==> Internet connection is available.\033[0m")
        main()
    else:
        print("\033[1;91m==> No internet connection detected. Exiting.\033[0m")
