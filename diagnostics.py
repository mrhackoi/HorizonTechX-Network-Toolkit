
import platform
import socket
import subprocess


def ping_host(host, count=4):
    host = host.strip()

    if not host:
        return "Please enter a hostname or IP address."

    if count < 1:
        return "Count must be at least 1."

    if platform.system().lower() == "windows":
        command = ["ping", "-n", str(count), host]
    else:
        command = ["ping", "-c", str(count), host]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=20
        )

        return result.stdout or result.stderr or "No output received."

    except subprocess.TimeoutExpired:
        return "Ping request timed out."

    except FileNotFoundError:
        return "Ping command is unavailable."

    except Exception as error:
        return f"Ping error: {error}"


def get_network_info():
    hostname = socket.gethostname()

    try:
        ip_address = socket.gethostbyname(hostname)
    except socket.gaierror:
        ip_address = "Unavailable"

    return {
        "hostname": hostname,
        "ip_address": ip_address,
        "platform": platform.system(),
        "platform_version": platform.version(),
        "architecture": platform.machine()
    }


def traceroute_host(host, max_hops=15):
    host = host.strip()

    if not host:
        return "Please enter a hostname."

    if max_hops < 1:
        return "Maximum hops must be at least 1."

    if platform.system().lower() == "windows":
        command = ["tracert", "-d", "-h", str(max_hops), host]
    else:
        command = [
            "traceroute", "-n", "-m", str(max_hops), host
        ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=60
        )

        return result.stdout or result.stderr or "No output received."

    except subprocess.TimeoutExpired:
        return "Traceroute timed out."

    except FileNotFoundError:
        return "Traceroute command is unavailable."

    except Exception as error:
        return f"Traceroute error: {error}"


if __name__ == "__main__":
    print("HORIZON TECHX - NETWORK DIAGNOSTICS")
    print("=" * 40)

    print("\nNetwork Information:")
    for key, value in get_network_info().items():
        print(f"{key}: {value}")
