
import tkinter as tk
from tkinter import ttk
import threading
import queue

from sniffer import get_interfaces, capture_packets
from diagnostics import ping_host, get_network_info, traceroute_host
from dns_lookup import lookup_domain
from analytics import analyze_packets, format_analytics_report
from reporter import save_text_report, save_csv_report


# ==============================
# THEME
# ==============================

BG = "#0b1220"
SIDEBAR = "#101b2d"
PANEL = "#162438"
PANEL_DARK = "#0e1928"

ACCENT = "#00e5b0"
CYAN = "#00c8ff"

TEXT = "#e8f1f5"
MUTED = "#8da3b8"
BORDER = "#263b52"
ERROR_COLOR = "#ff7777"


class HorizonGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("Horizon TechX | Advanced Network Toolkit")
        self.root.geometry("1200x760")
        self.root.minsize(950, 620)
        self.root.configure(bg=BG)

        self.task_queue = queue.Queue()

        self.busy = False
        self.closing = False

        self.page_id = 0
        self.after_id = None

        self.last_analytics = None
        self.last_analytics_report = None

        self.configure_styles()
        self.build_layout()
        self.show_dashboard()

        self.root.protocol("WM_DELETE_WINDOW", self.close_application)

        self.after_id = self.root.after(100, self.process_queue)

    # ==============================
    # WINDOW LIFECYCLE
    # ==============================

    def close_application(self):

        if self.closing:
            return

        self.closing = True

        if self.after_id is not None:
            try:
                self.root.after_cancel(self.after_id)
            except tk.TclError:
                pass

        self.root.destroy()

    # ==============================
    # STYLES
    # ==============================

    def configure_styles(self):

        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=PANEL_DARK,
            foreground=TEXT,
            fieldbackground=PANEL_DARK,
            rowheight=28,
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            background=SIDEBAR,
            foreground=ACCENT,
            font=("Arial", 10, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", "#21445a")],
            foreground=[("selected", TEXT)]
        )

        style.configure(
            "TCombobox",
            fieldbackground=PANEL_DARK,
            background=PANEL,
            foreground=TEXT
        )

    # ==============================
    # MAIN LAYOUT
    # ==============================

    def build_layout(self):

        header = tk.Frame(self.root, bg=SIDEBAR, height=75)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="HORIZON TECHX",
            font=("Arial", 21, "bold"),
            fg=ACCENT,
            bg=SIDEBAR
        ).pack(side="left", padx=25)

        tk.Label(
            header,
            text="ADVANCED NETWORK TOOLKIT",
            font=("Arial", 10, "bold"),
            fg=MUTED,
            bg=SIDEBAR
        ).pack(side="left", padx=15)

        self.status = tk.StringVar(value="SYSTEM READY")

        tk.Label(
            header,
            textvariable=self.status,
            font=("Consolas", 9, "bold"),
            fg=ACCENT,
            bg=SIDEBAR
        ).pack(side="right", padx=25)

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True)

        self.sidebar = tk.Frame(
            body,
            bg=SIDEBAR,
            width=220
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="NAVIGATION",
            font=("Arial", 10, "bold"),
            fg=MUTED,
            bg=SIDEBAR
        ).pack(anchor="w", padx=20, pady=(25, 15))

        navigation = [
            ("Dashboard", self.show_dashboard),
            ("Network Sniffer", self.show_sniffer),
            ("Ping Test", self.show_ping),
            ("DNS Lookup", self.show_dns),
            ("Network Info", self.show_network_info),
            ("Traceroute", self.show_traceroute),
            ("Traffic Analytics", self.show_analytics)
        ]

        for label, command in navigation:

            tk.Button(
                self.sidebar,
                text="  " + label,
                command=command,
                anchor="w",
                bg=SIDEBAR,
                fg=TEXT,
                activebackground=PANEL,
                activeforeground=ACCENT,
                font=("Arial", 10, "bold"),
                relief="flat",
                cursor="hand2",
                padx=12,
                pady=12
            ).pack(fill="x", padx=8, pady=2)

        self.content = tk.Frame(body, bg=BG)
        self.content.pack(
            side="left",
            fill="both",
            expand=True,
            padx=25,
            pady=22
        )

        tk.Label(
            self.root,
            text="Horizon TechX | Network Diagnostics & Monitoring",
            font=("Arial", 9),
            fg=MUTED,
            bg=SIDEBAR,
            pady=10
        ).pack(fill="x", side="bottom")

    # ==============================
    # UI HELPERS
    # ==============================

    def clear_page(self):

        self.page_id += 1

        for widget in self.content.winfo_children():
            widget.destroy()

    def page_title(self, title, description):

        tk.Label(
            self.content,
            text=title,
            font=("Arial", 22, "bold"),
            fg=ACCENT,
            bg=BG
        ).pack(anchor="w")

        tk.Label(
            self.content,
            text=description,
            font=("Arial", 10),
            fg=MUTED,
            bg=BG
        ).pack(anchor="w", pady=(5, 20))

    def create_panel(self, parent=None):

        if parent is None:
            parent = self.content

        return tk.Frame(
            parent,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1
        )

    def create_label(self, parent, text):

        tk.Label(
            parent,
            text=text,
            font=("Arial", 10, "bold"),
            fg=TEXT,
            bg=PANEL
        ).pack(anchor="w", padx=15, pady=(12, 4))

    def create_entry(self, parent, default=""):

        entry = tk.Entry(
            parent,
            font=("Consolas", 11),
            bg=PANEL_DARK,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            width=38
        )

        entry.pack(anchor="w", padx=15, pady=5)

        if default:
            entry.insert(0, default)

        return entry

    def create_button(self, parent, text, command):

        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=ACCENT,
            fg=BG,
            activebackground=CYAN,
            activeforeground=BG,
            font=("Arial", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=16,
            pady=9
        )

        button.pack(anchor="w", padx=15, pady=12)

        return button

    def create_output(self, parent=None, height=15):

        if parent is None:
            parent = self.content

        output = tk.Text(
            parent,
            height=height,
            bg=PANEL_DARK,
            fg=ACCENT,
            insertbackground=TEXT,
            font=("Consolas", 10),
            relief="flat",
            wrap="word",
            padx=12,
            pady=10
        )

        output.pack(
            fill="both",
            expand=True,
            padx=2,
            pady=2
        )

        return output

    def write_output(self, output, content):

        if self.closing:
            return

        try:
            if not output.winfo_exists():
                return

            output.delete("1.0", tk.END)
            output.insert(tk.END, str(content))

        except tk.TclError:
            pass

    # ==============================
    # BACKGROUND TASK HANDLING
    # ==============================

    def run_task(self, function, callback, description):

        if self.closing:
            return

        if self.busy:
            self.status.set("PLEASE WAIT - TASK RUNNING")
            return

        self.busy = True
        current_page = self.page_id

        self.status.set(description)

        def worker():

            try:
                result = function()
                self.task_queue.put(
                    (True, result, callback, current_page)
                )

            except Exception as error:
                self.task_queue.put(
                    (False, str(error), callback, current_page)
                )

        threading.Thread(
            target=worker,
            daemon=True,
            name="HorizonBackgroundTask"
        ).start()

    def process_queue(self):

        if self.closing:
            return

        try:

            while True:

                success, result, callback, task_page = (
                    self.task_queue.get_nowait()
                )

                self.busy = False

                # Ignore callbacks from previously opened pages.
                if task_page != self.page_id:
                    continue

                try:
                    if not success:
                        result = "ERROR: " + result

                    callback(result)

                    if success:
                        self.status.set("SYSTEM READY")
                    else:
                        self.status.set("TASK FAILED")

                except tk.TclError:
                    # A widget may have been destroyed.
                    continue

                except Exception as error:
                    self.status.set("TASK FAILED")
                    print(f"GUI callback error: {error}")

        except queue.Empty:
            pass

        if not self.closing:
            try:
                self.after_id = self.root.after(
                    100,
                    self.process_queue
                )
            except tk.TclError:
                self.closing = True

    # ==============================
    # DASHBOARD
    # ==============================

    def show_dashboard(self):

        self.clear_page()

        self.page_title(
            "NETWORK OPERATIONS",
            "Horizon TechX Advanced Network Monitoring Dashboard"
        )

        cards = [
            ("01", "NETWORK SNIFFER", "Packet metadata capture"),
            ("02", "PING TEST", "Host connectivity testing"),
            ("03", "DNS LOOKUP", "IPv4 and IPv6 resolution"),
            ("04", "NETWORK INFO", "System network details"),
            ("05", "TRACEROUTE", "Network path diagnostics"),
            ("06", "ANALYTICS", "Traffic statistics and reports")
        ]

        pages = [
            self.show_sniffer,
            self.show_ping,
            self.show_dns,
            self.show_network_info,
            self.show_traceroute,
            self.show_analytics
        ]

        grid = tk.Frame(self.content, bg=BG)
        grid.pack(fill="both", expand=True)

        for column in range(3):
            grid.columnconfigure(column, weight=1)

        for row in range(2):
            grid.rowconfigure(row, weight=1)

        for index, card_data in enumerate(cards):

            number, title, description = card_data

            card = self.create_panel(grid)

            card.grid(
                row=index // 3,
                column=index % 3,
                padx=8,
                pady=8,
                sticky="nsew"
            )

            tk.Label(
                card,
                text=number,
                font=("Arial", 12, "bold"),
                fg=CYAN,
                bg=PANEL
            ).pack(anchor="w", padx=15, pady=(18, 8))

            tk.Label(
                card,
                text=title,
                font=("Arial", 12, "bold"),
                fg=TEXT,
                bg=PANEL
            ).pack(anchor="w", padx=15)

            tk.Label(
                card,
                text=description,
                font=("Arial", 9),
                fg=MUTED,
                bg=PANEL
            ).pack(anchor="w", padx=15, pady=10)

            tk.Button(
                card,
                text="OPEN MODULE",
                command=pages[index],
                bg=ACCENT,
                fg=BG,
                relief="flat",
                font=("Arial", 9, "bold"),
                cursor="hand2",
                padx=12,
                pady=7
            ).pack(anchor="w", padx=15, pady=12)

    # ==============================
    # NETWORK SNIFFER
    # ==============================

    def show_sniffer(self):

        self.clear_page()

        self.page_title(
            "NETWORK SNIFFER",
            "Capture packet metadata on an authorized network."
        )

        panel = self.create_panel()
        panel.pack(fill="x", pady=5)

        self.create_label(panel, "NETWORK INTERFACE")

        try:
            interfaces = get_interfaces()
        except Exception as error:
            interfaces = []
            tk.Label(
                panel,
                text=f"Interface detection failed: {error}",
                fg=ERROR_COLOR,
                bg=PANEL
            ).pack(anchor="w", padx=15)

        interface_box = ttk.Combobox(
            panel,
            values=interfaces,
            state="readonly",
            width=45
        )
        interface_box.pack(anchor="w", padx=15, pady=5)

        if interfaces:
            interface_box.current(0)

        self.create_label(panel, "PROTOCOL")

        protocol_box = ttk.Combobox(
            panel,
            values=["ALL", "TCP", "UDP", "ICMP"],
            state="readonly",
            width=15
        )
        protocol_box.current(0)
        protocol_box.pack(anchor="w", padx=15, pady=5)

        self.create_label(panel, "PACKET COUNT")
        count_entry = self.create_entry(panel, "20")

        self.create_label(panel, "TIMEOUT IN SECONDS")
        timeout_entry = self.create_entry(panel, "15")

        output_panel = self.create_panel()
        output_panel.pack(fill="both", expand=True, pady=12)

        output = self.create_output(output_panel, 12)

        def capture():

            try:
                count = int(count_entry.get())
                timeout = int(timeout_entry.get())
            except ValueError:
                self.write_output(output, "ERROR: Enter valid numbers.")
                return

            if not 1 <= count <= 500:
                self.write_output(output, "ERROR: Packet count must be 1-500.")
                return

            if not 1 <= timeout <= 120:
                self.write_output(output, "ERROR: Timeout must be 1-120.")
                return

            interface = interface_box.get() or None
            protocol = protocol_box.get()

            def task():
                return capture_packets(
                    interface=interface,
                    protocol=protocol,
                    count=count,
                    timeout=timeout
                )

            def display(packets):

                if isinstance(packets, str) and packets.startswith("ERROR:"):
                    self.write_output(output, packets)
                    return

                if not packets:
                    self.write_output(
                        output,
                        "No packets captured during this session."
                    )
                    return

                lines = [
                    f"Captured packets: {len(packets)}",
                    "=" * 65
                ]

                for packet in packets:
                    lines.append(
                        f"{packet['timestamp']} | "
                        f"{packet['source']} -> "
                        f"{packet['destination']} | "
                        f"{packet['protocol']} | "
                        f"{packet['size']} bytes"
                    )

                self.write_output(output, "\n".join(lines))

            self.run_task(task, display, "CAPTURING PACKETS...")

        self.create_button(panel, "START CAPTURE", capture)

    # ==============================
    # PING TEST
    # ==============================

    def show_ping(self):

        self.clear_page()

        self.page_title(
            "PING TEST",
            "Check host connectivity and response time."
        )

        panel = self.create_panel()
        panel.pack(fill="x")

        self.create_label(panel, "HOSTNAME OR IP ADDRESS")
        host_entry = self.create_entry(panel, "google.com")

        output_panel = self.create_panel()
        output_panel.pack(fill="both", expand=True, pady=15)

        output = self.create_output(output_panel, 17)

        def run_ping():

            host = host_entry.get().strip()

            if not host:
                self.write_output(output, "ERROR: Enter a hostname or IP.")
                return

            self.run_task(
                lambda: ping_host(host),
                lambda result: self.write_output(output, result),
                "RUNNING PING..."
            )

        self.create_button(panel, "RUN PING", run_ping)

    # ==============================
    # DNS LOOKUP
    # ==============================

    def show_dns(self):

        self.clear_page()

        self.page_title(
            "DNS LOOKUP",
            "Resolve domain names into IPv4 and IPv6 addresses."
        )

        panel = self.create_panel()
        panel.pack(fill="x")

        self.create_label(panel, "DOMAIN NAME")
        domain_entry = self.create_entry(panel, "google.com")

        output_panel = self.create_panel()
        output_panel.pack(fill="both", expand=True, pady=15)

        output = self.create_output(output_panel, 17)

        def lookup():

            domain = domain_entry.get().strip()

            if not domain:
                self.write_output(output, "ERROR: Enter a domain name.")
                return

            self.run_task(
                lambda: lookup_domain(domain),
                lambda result: self.write_output(output, result),
                "RESOLVING DOMAIN..."
            )

        self.create_button(panel, "LOOKUP DOMAIN", lookup)

    # ==============================
    # NETWORK INFORMATION
    # ==============================

    def show_network_info(self):

        self.clear_page()

        self.page_title(
            "NETWORK INFORMATION",
            "Local system and network information."
        )

        panel = self.create_panel()
        panel.pack(fill="both", expand=True)

        output = self.create_output(panel, 20)

        def refresh():

            def display(info):

                if isinstance(info, str):
                    self.write_output(output, info)
                    return

                lines = [
                    "HORIZON TECHX - NETWORK INFORMATION",
                    "=" * 45
                ]

                for key, value in info.items():
                    lines.append(f"{key}: {value}")

                self.write_output(output, "\n".join(lines))

            self.run_task(
                get_network_info,
                display,
                "FETCHING NETWORK INFORMATION..."
            )

        self.create_button(
            self.content,
            "REFRESH INFORMATION",
            refresh
        )

        refresh()

    # ==============================
    # TRACEROUTE
    # ==============================

    def show_traceroute(self):

        self.clear_page()

        self.page_title(
            "TRACEROUTE",
            "Inspect the network path to a destination."
        )

        panel = self.create_panel()
        panel.pack(fill="x")

        self.create_label(panel, "DESTINATION HOST OR IP")
        host_entry = self.create_entry(panel, "1.1.1.1")

        output_panel = self.create_panel()
        output_panel.pack(fill="both", expand=True, pady=15)

        output = self.create_output(output_panel, 18)

        def trace():

            host = host_entry.get().strip()

            if not host:
                self.write_output(output, "ERROR: Enter a destination.")
                return

            self.run_task(
                lambda: traceroute_host(host),
                lambda result: self.write_output(output, result),
                "TRACING NETWORK ROUTE..."
            )

        self.create_button(panel, "START TRACEROUTE", trace)

    # ==============================
    # TRAFFIC ANALYTICS
    # ==============================

    def show_analytics(self):

        self.clear_page()

        self.page_title(
            "TRAFFIC ANALYTICS",
            "Analyze captured packet metadata and export reports."
        )

        self.last_analytics = None
        self.last_analytics_report = None

        panel = self.create_panel()
        panel.pack(fill="x")

        self.create_label(panel, "PACKET COUNT")
        count_entry = self.create_entry(panel, "20")

        self.create_label(panel, "TIMEOUT IN SECONDS")
        timeout_entry = self.create_entry(panel, "15")

        output_panel = self.create_panel()
        output_panel.pack(fill="both", expand=True, pady=12)

        output = self.create_output(output_panel, 15)

        def run_analytics():

            try:
                count = int(count_entry.get())
                timeout = int(timeout_entry.get())
            except ValueError:
                self.write_output(output, "ERROR: Enter valid numbers.")
                return

            if not 1 <= count <= 500:
                self.write_output(output, "ERROR: Packet count must be 1-500.")
                return

            if not 1 <= timeout <= 120:
                self.write_output(output, "ERROR: Timeout must be 1-120.")
                return

            def analyze():

                packets = capture_packets(
                    count=count,
                    timeout=timeout
                )

                statistics = analyze_packets(packets)

                return {
                    "statistics": statistics,
                    "report": format_analytics_report(statistics)
                }

            def display(result):

                if isinstance(result, str):
                    self.write_output(output, result)
                    return

                statistics = result["statistics"]

                if not statistics.get("total_packets", 0):
                    self.last_analytics = None
                    self.last_analytics_report = None

                    self.write_output(
                        output,
                        "No packets available for analytics."
                    )
                    return

                self.last_analytics = statistics
                self.last_analytics_report = result["report"]

                self.write_output(output, result["report"])

            self.run_task(
                analyze,
                display,
                "ANALYZING TRAFFIC..."
            )

        def export_txt():

            report = self.last_analytics_report

            if not report:
                self.write_output(
                    output,
                    "Run analytics successfully before exporting."
                )
                return

            self.run_task(
                lambda: save_text_report("Traffic Analytics", report),
                lambda path: self.write_output(
                    output,
                    f"TXT report saved:\n{path}"
                ),
                "SAVING TXT REPORT..."
            )

        def export_csv():

            statistics = self.last_analytics

            if not statistics:
                self.write_output(
                    output,
                    "Run analytics successfully before exporting."
                )
                return

            rows = [
                [protocol, total]
                for protocol, total
                in statistics["protocol_counts"].items()
            ]

            self.run_task(
                lambda: save_csv_report(
                    "Traffic Analytics",
                    ["Protocol", "Packet Count"],
                    rows
                ),
                lambda path: self.write_output(
                    output,
                    f"CSV report saved:\n{path}"
                ),
                "SAVING CSV REPORT..."
            )

        self.create_button(
            panel,
            "RUN ANALYTICS",
            run_analytics
        )

        export_panel = tk.Frame(self.content, bg=BG)
        export_panel.pack(anchor="w")

        tk.Button(
            export_panel,
            text="EXPORT TXT",
            command=export_txt,
            bg=ACCENT,
            fg=BG,
            relief="flat",
            font=("Arial", 9, "bold"),
            padx=15,
            pady=9
        ).pack(side="left", padx=5)

        tk.Button(
            export_panel,
            text="EXPORT CSV",
            command=export_csv,
            bg=CYAN,
            fg=BG,
            relief="flat",
            font=("Arial", 9, "bold"),
            padx=15,
            pady=9
        ).pack(side="left", padx=5)


# ==============================
# LAUNCH APPLICATION
# ==============================

def launch_gui():

    root = tk.Tk()
    HorizonGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
