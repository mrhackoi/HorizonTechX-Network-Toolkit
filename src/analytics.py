
from collections import Counter


def analyze_packets(packets):
    """Analyze a list of packet metadata dictionaries."""

    protocol_counts = Counter()
    source_counts = Counter()
    destination_counts = Counter()

    total_bytes = 0

    for packet in packets:
        protocol_counts[packet.get("protocol", "OTHER")] += 1

        source = packet.get("source", "Unknown")
        destination = packet.get("destination", "Unknown")

        source_counts[source] += 1
        destination_counts[destination] += 1

        try:
            total_bytes += int(packet.get("size", 0))
        except (TypeError, ValueError):
            pass

    return {
        "total_packets": len(packets),
        "total_bytes": total_bytes,
        "protocol_counts": dict(protocol_counts),
        "top_sources": source_counts.most_common(5),
        "top_destinations": destination_counts.most_common(5)
    }


def format_analytics_report(statistics):
    """Convert analytics results into readable text."""

    lines = [
        "HORIZON TECHX - TRAFFIC ANALYTICS",
        "=" * 40,
        f"Total packets: {statistics['total_packets']}",
        f"Total data size: {statistics['total_bytes']} bytes",
        "",
        "PROTOCOL STATISTICS",
        "-" * 30
    ]

    for protocol, count in statistics["protocol_counts"].items():
        lines.append(f"{protocol}: {count}")

    lines.extend([
        "",
        "TOP SOURCE IPs",
        "-" * 30
    ])

    for address, count in statistics["top_sources"]:
        lines.append(f"{address}: {count}")

    lines.extend([
        "",
        "TOP DESTINATION IPs",
        "-" * 30
    ])

    for address, count in statistics["top_destinations"]:
        lines.append(f"{address}: {count}")

    return "\n".join(lines)


if __name__ == "__main__":

    sample_packets = [
        {
            "protocol": "TCP",
            "source": "192.168.1.10",
            "destination": "192.168.1.20",
            "size": 120
        },
        {
            "protocol": "UDP",
            "source": "192.168.1.10",
            "destination": "8.8.8.8",
            "size": 80
        },
        {
            "protocol": "TCP",
            "source": "192.168.1.20",
            "destination": "192.168.1.10",
            "size": 150
        }
    ]

    results = analyze_packets(sample_packets)
    print(format_analytics_report(results))
