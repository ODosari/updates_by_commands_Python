#name = "updates_commands_rust"
#version = "0.1.0"
#by = "Obaid Aldosari"
#github = "https://github.com/ODosari/UpdatesTerminalCommandsRust"


# Import the subprocess module for running shell commands
import subprocess


# Function to run a shell command using Zsh
def run_command(update_commands):
    try:
        # Execute the command in a Zsh shell
        # 'shell=True' allows shell commands
        # 'executable="/bin/zsh"' specifies the Zsh shell
        # 'check=True' raises an exception if the command fails
        subprocess.run(update_commands, shell=True, executable="/bin/zsh", check=True)
    except subprocess.CalledProcessError as e:
        # Handle errors and print a message
        print(f"Command '{update_commands}' failed with error: {e}")


# Main function
if __name__ == "__main__":
    # List of commands to run
    commands = [
        "brew upgrade && brew cleanup && brew autoremove",  # Homebrew commands
        "conda update --all -y",  # Conda update
        "rustup update"  # Rust update
    ]

    # Get the total number of commands
    total_commands = len(commands)

    # Loop through each command and run it
    # 'enumerate' provides both the index 'i' and the value 'command'
    # 'start=1' starts the index from 1
    for i, command in enumerate(commands, start=1):
        # Print the command number and the command itself in bold and green color
        # ANSI escape codes are used for styling
        print(f"\033[1;97mRunning update command \033[1;92m{i} \033[1;97mof \033[1;92m{total_commands}\033[1;97m:\033[0m {command}")

        # Run the command
        run_command(command)
