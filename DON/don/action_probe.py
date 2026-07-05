import csv
import re
from don.port_tools import test_port
from don.actions import get_desktop_health


def is_mac_address(value):
    if not value:
        return False

    mac_pattern = r"^([0-9a-fA-F]{2}[-:]){5}[0-9a-fA-F]{2}$"
    return re.match(mac_pattern, value.strip()) is not None


def is_ip_address(value):
    if not value:
        return False

    ip_pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
    return re.match(ip_pattern, value.strip()) is not None


def supports_roku(device):
    return 8060 in device["ports"] or test_port(device["ip"], 8060)


def supports_local_desktop(device):
    mac_value = str(device["mac"]).strip()

    if is_ip_address(mac_value):
        health = get_desktop_health()
        return "error" not in health

    if mac_value == "Unknown":
        health = get_desktop_health()
        return "error" not in health

    if is_mac_address(mac_value):
        return False

    return False


def find_compatible_actions(device):
    actions = []
    notes = []

    if supports_roku(device):
        actions.append("Roku Control")
        notes.append("Roku ECP detected on port 8060")

    if supports_local_desktop(device):
        actions.append("Local Desktop Health")
        notes.append("Local PC detected because MAC field is Unknown or contains an IP address")

    if not actions:
        actions.append("No Supported Actions")
        notes.append("Device reachable, but no current DON action module supports it")

    return actions, notes


def build_action_devices_table(devices):
    action_devices = []

    for device in devices:
        actions, notes = find_compatible_actions(device)

        action_devices.append({
            "ip": device["ip"],
            "hostname": device["hostname"],
            "mac": device["mac"],
            "ports": ",".join(map(str, device["ports"])),
            "device_type": device["type"],
            "actions_checked": "; ".join(actions),
            "notes": "; ".join(notes)
        })

    return action_devices


def save_action_devices_csv(action_devices, path="output/action_devices.csv"):
    with open(path, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "IP Address",
            "Hostname",
            "MAC Address",
            "Open Ports",
            "Device Type",
            "Actions Checked",
            "Notes"
        ])

        for d in action_devices:
            writer.writerow([
                d["ip"],
                d["hostname"],
                d["mac"],
                d["ports"],
                d["device_type"],
                d["actions_checked"],
                d["notes"]
            ])