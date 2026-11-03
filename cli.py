
from sniffer import get_interfaces, capture_packets
from diagnostics import ping_host, get_network_info, traceroute_host
from dns_lookup import lookup_domain
from analytics import analyze_packets, format_analytics_report
from reporter import save_text_report, save_csv_report


def handle_capture_error(error):
    print(f"\nCapture unavailable: {error}")
    print(
        "Live packet capture will be tested on Kali Linux "
        "in the authorized lab environment."
    )


def network_sniffer():
    print("\n--- NETWORK SNIFFER ---")

    try:
        interfaces = get_interfaces()

        if not interfaces:
            print("No network interfaces found.")
            return

        print("\nAvailable interfaces:")

        for index, interface in enumerate(interfaces, start=1):
            print(f"{index}. {interface}")

        choice = input(
            "\nSelect interface number (Enter for default): "
        ).strip()

        interface = None

        if choice:
            try:
                interface = interfaces[int(choice) - 1]
            except (ValueError, IndexError):
                print("Invalid interface selection.")
                return

        protocol = (
            input("Protocol (ALL/TCP/UDP/ICMP) [ALL]: ")
            .strip()
            .upper() or "ALL"
        )

        count = int(input("Packet count [20]: ").strip() or "20")
        timeout = int(
            input("Timeout in seconds [15]: ").strip() or "15"
        )

        packets = capture_packets(
            interface=interface,
            protocol=protocol,
            count=count,
            timeout=timeout
        )

        print(f"\nCaptured {len(packets)} packets.")

        for packet in packets:
            print(packet)

    except ValueError as error:
        print(f"Input error: {error}")

    except RuntimeError as error:
        handle_capture_error(error)


def ping_test():
    host = input("\nEnter hostname or IP: ").strip()
    print(ping_host(host))


def dns_test():
    domain = input("\nEnter domain name: ").strip()
    print(lookup_domain(domain))


def network_information():
    print("\n--- NETWORK INFORMATION ---")

    information = get_network_info()

    for key, value in information.items():
        print(f"{key}: {value}")


def traceroute_test():
    host = input("\nEnter hostname or IP: ").strip()
    print(traceroute_host(host))


def traffic_analytics():
    print("\n--- TRAFFIC ANALYTICS ---")

    try:
        count = int(input("Packet count [20]: ").strip() or "20")
        timeout = int(
            input("Timeout in seconds [15]: ").strip() or "15"
        )

        packets = capture_packets(
            count=count,
            timeout=timeout
        )

        statistics = analyze_packets(packets)
        report = format_analytics_report(statistics)

        print("\n" + report)

        if not packets:
            print("\nNo packets captured. No report generated.")
            return

        save = input(
            "\nSave reports as TXT and CSV? (y/n): "
        ).strip().lower()

        if save == "y":
            text_path = save_text_report(
                "Traffic Analytics",
                report
            )

            rows = [
                [protocol, total]
                for protocol, total
                in statistics["protocol_counts"].items()
            ]

            csv_path = save_csv_report(
                "Traffic Analytics",
                ["Protocol", "Packet Count"],
                rows
            )

            print("\nReports saved successfully!")
            print(f"TXT: {text_path}")
            print(f"CSV: {csv_path}")

    except ValueError as error:
        print(f"Input error: {error}")

    except RuntimeError as error:
        handle_capture_error(error)


def show_cli():

    actions = {
        "1": network_sniffer,
        "2": ping_test,
        "3": dns_test,
        "4": network_information,
        "5": traceroute_test,
        "6": traffic_analytics
    }

    while True:
        print("\n" + "=" * 45)
        print(" HORIZON TECHX - NETWORK TOOLKIT")
        print("=" * 45)
        print("1. Network Sniffer")
        print("2. Ping Test")
        print("3. DNS Lookup")
        print("4. Network Information")
        print("5. Traceroute")
        print("6. Traffic Analytics")
        print("7. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "7":
            print("Exiting Horizon TechX Network Toolkit.")
            break

        action = actions.get(choice)

        if action:
            try:
                action()

            except KeyboardInterrupt:
                print("\nOperation interrupted.")

            except Exception as error:
                print(f"Unexpected error: {error}")

        else:
            print("Invalid option. Please select 1-7.")


if __name__ == "__main__":
    show_cli()
