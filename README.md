# HorizonTechX – Advanced Network Toolkit

A Python-based network diagnostics and monitoring toolkit developed as part of the Horizon TechX Cybersecurity Internship.

## Overview

HorizonTechX Network Toolkit provides a simple interface for performing network diagnostics, DNS resolution, packet metadata monitoring, and traffic analysis.

The project includes both Command-Line Interface (CLI) and Graphical User Interface (GUI) modes.

## Features

- **Network Sniffer:** Capture and display packet metadata.
- **Ping Test:** Check host connectivity and response time.
- **DNS Lookup:** Resolve domain names into IPv4 and IPv6 addresses.
- **Network Information:** Display local system and network details.
- **Traceroute:** Inspect the network path to a destination.
- **Traffic Analytics:** Analyze packet counts, protocols, sources, and destinations.
- **Report Generation:** Export analytics reports in TXT and CSV formats.
- **Dark GUI:** User-friendly interface built with Python Tkinter.

## Technologies Used

- Python 3.12
- Scapy
- Tkinter
- Socket
- Subprocess
- Threading
- CSV

## Project Structure

```text
HorizonTechX_Network_Sniffer/
│
├── src/
│   ├── main.py
│   ├── cli.py
│   ├── gui.py
│   ├── sniffer.py
│   ├── diagnostics.py
│   ├── dns_lookup.py
│   ├── analytics.py
│   └── reporter.py
│
├── logs/
├── reports/
├── screenshots/
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
```

Navigate to the project directory:

```bash
cd HorizonTechX_Network_Sniffer
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

Activate it on Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python src/main.py
```

Select your preferred mode:

1. CLI Mode
2. GUI Mode
3. Exit

To launch the GUI directly:

```bash
python src/gui.py
```

## Platform Notes

- The diagnostic, DNS, and network information modules support Windows and Linux, subject to platform capabilities.
- Live packet capture depends on the available packet-capture backend and permissions.
- Windows may display a Scapy warning if a compatible packet-capture provider is unavailable.
- Kali Linux is the intended environment for live packet-capture testing.
- Traceroute results may vary depending on firewall rules and network restrictions.

## Testing Status

| Module              | Status                                |
| ------------------- | ------------------------------------- |
| CLI                 | Tested                                |
| GUI                 | Launch and basic functionality tested |
| Ping                | Tested                                |
| DNS Lookup          | Tested                                |
| Network Information | Tested                                |
| Traceroute          | Tested                                |
| Live Packet Capture | Kali Linux testing pending            |
| Traffic Analytics   | Live capture testing pending          |
| TXT/CSV Export      | Basic functionality tested            |

## Security & Ethical Use

This toolkit is intended for educational purposes, network diagnostics, and authorized security testing.

Only monitor networks and systems for which you have explicit permission.

The sniffer focuses on packet metadata and does not intentionally collect packet payload contents.

## Internship Project

**Organization:** Horizon TechX  
**Project:** Advanced Network Toolkit  
**Domain:** Cybersecurity / Network Monitoring  
**Developer:** Dhoni Kumar Shah

## License

This project is available for educational and learning purposes. Add an appropriate open-source license before redistribution.
