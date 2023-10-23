import platform
import socket


def check_platform():
    """Check the operating system and its version."""
    os_name = platform.system()
    os_version = platform.version()
    os_release = platform.release()

    if os_name == "Darwin":
        os_name = "macOS"
        os_version = platform.mac_ver()[0]  # Get macOS version
        os_release = platform.mac_ver()[2]  # Get macOS name (e.g., "Mojave")
    elif os_name == "Linux":
        # For Linux, we can use the 'dist' or 'linux_distribution' function to get more details
        # However, 'linux_distribution' is removed in Python 3.8+, so we fall back to 'dist' for older versions
        try:
            os_name, os_version, os_release = platform.linux_distribution()
        except AttributeError:
            os_name, os_version, os_release = platform.dist()
    elif os_name == "Windows":
        os_name = "Windows"
        os_version = platform.win32_ver()[1]  # Get Windows version (e.g., "10")
        os_release = platform.win32_ver()[0]  # Get Windows release name (e.g., "10")

    return f"{os_name} {os_version} ({os_release})"


def check_internet_connection(host="8.8.8.8", port=53, timeout=3):
    """Check if there's an internet connection by trying to establish a socket connection."""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(f"Internet connection check failed: {ex}")
        return False
