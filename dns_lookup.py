
import socket


def lookup_domain(domain):
    domain = domain.strip().rstrip(".")

    if not domain:
        return "Please enter a domain name."

    try:
        results = socket.getaddrinfo(
            domain,
            None,
            family=socket.AF_UNSPEC,
            type=socket.SOCK_STREAM
        )

        ipv4 = sorted({
            result[4][0]
            for result in results
            if result[0] == socket.AF_INET
        })

        ipv6 = sorted({
            result[4][0]
            for result in results
            if result[0] == socket.AF_INET6
        })

        output = [
            f"Domain: {domain}",
            "",
            "IPv4 Addresses:"
        ]

        output.extend(ipv4 or ["No IPv4 address found."])

        output.extend(["", "IPv6 Addresses:"])
        output.extend(ipv6 or ["No IPv6 address found."])

        return "\n".join(output)

    except socket.gaierror as error:
        return f"DNS lookup failed: {error}"

    except Exception as error:
        return f"Unexpected error: {error}"


if __name__ == "__main__":

    domain = input("Enter domain name: ")
    print("\nDNS LOOKUP RESULTS")
    print("=" * 35)
    print(lookup_domain(domain))
