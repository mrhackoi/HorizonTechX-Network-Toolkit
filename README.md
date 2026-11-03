# Horizon TechX – Network Toolkit

A Python-based Network Diagnostics, Packet Sniffing, and Traffic Analysis Toolkit built with **Scapy** and **Tkinter**. It provides command-line and graphical interfaces for network troubleshooting, DNS resolution, packet inspection, and basic traffic analytics.

Developed as part of the **Horizon TechX Cybersecurity Internship**.

---

## 🚀 Features

- **Network Sniffer** – Capture and inspect network packets.
- **Ping Test** – Check host reachability and response time.
- **DNS Lookup** – Resolve domain names and retrieve IP addresses.
- **Network Information** – Display hostname, IP address, platform, and system architecture.
- **Traceroute** – Trace the network path to a destination.
- **Traffic Analytics** – Analyze captured packets, protocols, packet sizes, and source/destination IPs.
- **Report Generation** – Export traffic analytics reports in TXT and CSV formats.
- **Dual Interface** – Use the toolkit through CLI or a Tkinter-based GUI.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Scapy | Packet capture and analysis |
| Tkinter | Graphical user interface |
| Socket | Network and DNS operations |
| Platform | System information |
| CSV | Report export |

## 📁 Project Structure

```text
HorizonTechX-Network-Toolkit/
│
├── src/
│   ├── analytics.py
│   ├── cli.py
│   ├── diagnostics.py
│   ├── dns_lookup.py
│   ├── gui.py
│   ├── main.py
│   ├── reporter.py
│   └── sniffer.py
│
├── logs/
│   └── .gitkeep
│
├── reports/
│   └── .gitkeep
│
├── screenshots/
│   ├── 1.png
│   ├── 2.png
│   ├── 3.png
│   ├── 4.png
│   ├── 5.png
│   ├── 6.png
│   ├── 7.png
│   ├── 8.png
│   ├── 9.png
│   ├── 10.png
│   ├── 11.png
│   ├── 12.png
│   ├── 13.png
│   └── 14.png
│
├── .gitignore
├── README.md
└── requirements.txt
```

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/mrhackoi/HorizonTechX-Network-Toolkit.git

cd HorizonTechX-Network-Toolkit
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip

pip install -r requirements.txt
```

### 4. Verify Installation

```bash
python -m compileall -q src
```

## ▶️ Usage

### CLI Mode

Launch the main application:

```bash
python src/main.py
```

Select **CLI Mode** from the application menu.

Available options:

1. Network Sniffer
2. Ping Test
3. DNS Lookup
4. Network Information
5. Traceroute
6. Traffic Analytics
7. Exit

### GUI Mode

Launch the graphical interface:

```bash
python src/gui.py
```

The GUI provides a visual interface for accessing the toolkit's network utilities.

## 🔐 Root / Sudo Permissions

**Important:** Packet capture requires appropriate network interface permissions on Linux.

For Kali Linux, run the application with elevated privileges when using packet-capture functionality.

### Launch GUI with Root Permissions

```bash
sudo ./venv/bin/python src/gui.py
```

### Launch CLI with Root Permissions

```bash
sudo ./venv/bin/python src/main.py
```

### Permission Requirements

| Feature | Root Permission |
|---|---|
| Network Sniffer | Required for packet capture |
| Traffic Analytics | Required for packet capture |
| Ping Test | Generally not required |
| DNS Lookup | Not required |
| Network Information | Not required |
| Traceroute | Depends on the system and method used |

**Note:** Running the GUI with `sudo` is useful when you need its packet-capture features. Other diagnostic functions generally work without elevated privileges. Use packet capture only on systems and networks you own or are authorized to inspect.

## 📊 Testing & Verification

The toolkit was tested in a Kali Linux environment.

**Test Environment**

- Operating System: Kali Linux Rolling 2026.3
- Python: 3.14.7
- Scapy: 2.8.0
- Architecture: x86_64

**Testing Results**

| Test | Result |
|---|---|
| Python compilation | Passed |
| Application launcher | Passed |
| CLI launch | Passed |
| Ping – 127.0.0.1 | 4 packets received, 0% loss |
| DNS – google.com | Successfully resolved |
| Network Information | Passed |
| Traceroute – google.com | Destination reached at hop 9 |
| Traffic Analytics | Packet capture successful |
| TXT Report Export | Generated successfully |
| CSV Report Export | Generated successfully |
| Network Sniffer | Successfully captured 20 packets on eth0 |
| GUI Launch | Successfully launched |

**Packet Capture Note:** An initial capture returned zero packets because no matching traffic was observed during that capture window. A subsequent capture successfully collected 20 packets.

## 📄 Generated Reports

Traffic Analytics supports report export in:

- **TXT:** Human-readable traffic summary.
- **CSV:** Structured data for further analysis.

Generated reports are saved in the `reports/` directory.

Example:

```text
reports/
├── traffic_analytics_TIMESTAMP.txt
└── traffic_analytics_TIMESTAMP.csv
```

## 📸 Screenshots

The `screenshots/` directory contains the project setup, installation, CLI testing, network diagnostics, packet capture, analytics, and GUI evidence.

Screenshots are numbered from `1.png` to `14.png`.

## ⚠️ Limitations

- Packet capture depends on interface permissions and available network traffic.
- Some network interfaces may not receive traffic in certain virtual machine configurations.
- Traceroute results may vary depending on routing and firewall configurations.
- GUI availability depends on a working graphical desktop environment and Tkinter support.
- Packet capture should only be performed in authorized environments.

## 🔮 Future Improvements

- Real-time traffic visualization.
- Advanced protocol filtering.
- Improved packet statistics and analytics.
- Additional report formats.
- Enhanced GUI dashboard.
- More detailed network monitoring capabilities.

## 👨‍💻 Author

**Dhoni Kumar Shah**

Cybersecurity | Network Security | VAPT | Security Research

GitHub: [@mrhackoi](https://github.com/mrhackoi)

## 📜 Disclaimer

This project is intended for educational purposes, authorized network diagnostics, and defensive security testing only. The developer is not responsible for misuse or unauthorized monitoring of networks.

---

**Horizon TechX – Network Toolkit**  
*Learn • Analyze • Secure*
