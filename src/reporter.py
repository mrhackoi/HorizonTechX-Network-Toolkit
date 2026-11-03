
from pathlib import Path
from datetime import datetime
import csv

BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = BASE_DIR / "reports"


def save_text_report(title, content):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{title.lower().replace(' ', '_')}_{timestamp}.txt"

    report_path = REPORT_DIR / filename

    with report_path.open("w", encoding="utf-8") as file:
        file.write(f"{title}\n")
        file.write("=" * 50 + "\n")
        file.write(f"Generated: {datetime.now()}\n\n")
        file.write(str(content))

    return str(report_path)


def save_csv_report(title, headers, rows):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{title.lower().replace(' ', '_')}_{timestamp}.csv"

    report_path = REPORT_DIR / filename

    with report_path.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)

    return str(report_path)


if __name__ == "__main__":

    sample_content = "Total packets: 3\nTCP: 2\nUDP: 1"

    text_path = save_text_report(
        "Network Analytics",
        sample_content
    )

    csv_path = save_csv_report(
        "Network Analytics",
        ["Protocol", "Packet Count"],
        [["TCP", 2], ["UDP", 1]]
    )

    print("Reports generated successfully!")
    print(f"TXT: {text_path}")
    print(f"CSV: {csv_path}")
