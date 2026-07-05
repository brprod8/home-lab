from don.config import SUBNET
from don.scanner import scan_network
from don.csv_exporter import save_csv
from don.action_probe import build_action_devices_table, save_action_devices_csv
from don.dashboard import build_dashboard_html
from don.topology import build_topology_html


def print_devices(devices):
    print("\nDON - Devices On Network")
    print("-" * 130)

    print(
        f"{'IP Address':15} "
        f"{'Hostname':30} "
        f"{'MAC Address':20} "
        f"{'Health':12} "
        f"{'Open Ports':20} "
        f"{'Device Type'}"
    )

    print("-" * 130)

    for d in devices:
        print(
            f"{d['ip']:15} "
            f"{d['hostname']:30} "
            f"{d['mac']:20} "
            f"{d['health']:12} "
            f"{str(d['ports']):20} "
            f"{d['type']}"
        )


def main():
    print(f"\nScanning {SUBNET}.0/24...\n")

    devices = scan_network(SUBNET)

    print_devices(devices)

    save_csv(devices)
    print("\nSaved DON table to output/don_table.csv")

    action_devices = build_action_devices_table(devices)

    save_action_devices_csv(action_devices)
    print("Saved action devices table to output/action_devices.csv")

    build_dashboard_html(devices, action_devices)
    build_topology_html(devices)

    print("Saved dashboard to output/dashboard.html")
    print("Saved topology to output/topology.html")


if __name__ == "__main__":
    main()