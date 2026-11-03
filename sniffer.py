
from datetime import datetime
from scapy.all import sniff, IP, IPv6, TCP, UDP, ICMP, get_if_list


def get_interfaces():
    """Return available network interfaces."""
    try:
        return get_if_list()
    except Exception as error:
        raise RuntimeError(f"Interface detection failed: {error}")


def get_packet_metadata(packet):
    """Extract metadata without reading packet payload."""

    if IP in packet:
        source = packet[IP].src
        destination = packet[IP].dst

    elif IPv6 in packet:
        source = packet[IPv6].src
        destination = packet[IPv6].dst

    else:
        return None

    if TCP in packet:
        protocol = "TCP"
    elif UDP in packet:
        protocol = "UDP"
    elif ICMP in packet:
        protocol = "ICMP"
    else:
        protocol = "OTHER"

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": source,
        "destination": destination,
        "protocol": protocol,
        "size": len(packet)
    }


def capture_packets(
    interface=None,
    protocol="ALL",
    count=20,
    timeout=30,
    callback=None
):
    """
    Capture metadata from an authorized network interface.

    Returns a list of packet metadata dictionaries.
    """

    protocol = protocol.upper()

    allowed_protocols = ["ALL", "TCP", "UDP", "ICMP"]

    if protocol not in allowed_protocols:
        raise ValueError("Protocol must be ALL, TCP, UDP or ICMP.")

    if count < 1:
        raise ValueError("Count must be at least 1.")

    if timeout < 1:
        raise ValueError("Timeout must be at least 1 second.")

    packet_filter = {
        "ALL": "ip or ip6",
        "TCP": "tcp",
        "UDP": "udp",
        "ICMP": "icmp"
    }[protocol]

    captured = []

    def process_packet(packet):
        metadata = get_packet_metadata(packet)

        if metadata is not None:
            captured.append(metadata)

            if callback:
                callback(metadata)

    try:
        sniff(
            iface=interface,
            filter=packet_filter,
            prn=process_packet,
            store=False,
            count=count,
            timeout=timeout
        )

    except PermissionError:
        raise RuntimeError(
            "Permission denied. Run on your authorized lab system "
            "with the required packet-capture permissions."
        )

    except Exception as error:
        raise RuntimeError(f"Packet capture failed: {error}")

    return captured


if __name__ == "__main__":

    print("HORIZON TECHX - NETWORK SNIFFER")
    print("=" * 40)

    print("\nAvailable interfaces:")

    try:
        for interface in get_interfaces():
            print(f"- {interface}")

    except RuntimeError as error:
        print(error)
