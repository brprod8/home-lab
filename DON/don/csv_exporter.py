import csv
import os


def save_csv(devices, path="output/don_table.csv"):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "IP Address",
            "Hostname",
            "MAC Address",
            "Status",
            "Latency",
            "Network Health",
            "Packet Loss",
            "Health Test Latencies",
            "Open Ports",
            "Services",
            "Capabilities",
            "Device Type"
        ])

        for d in devices:
            writer.writerow([
                d["ip"],
                d["hostname"],
                d["mac"],
                d["status"],
                d["latency"],
                d["health"],
                d["packet_loss"],
                d["health_latency"],
                ",".join(map(str, d["ports"])),
                d["services"],
                d["capabilities"],
                d["type"]
            ])
