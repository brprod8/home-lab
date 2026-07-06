import json
import os
from don.event_logger import log_event

STATE_FILE = "logs/device_states.json"


def load_previous_states():
    if not os.path.exists(STATE_FILE):
        return {}

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return {}


def save_current_states(states):
    os.makedirs("logs", exist_ok=True)

    with open(STATE_FILE, "w", encoding="utf-8") as file:
        json.dump(states, file, indent=4)


previous_device_states = load_previous_states()


def extract_latency_ms(latency):
    if latency is None:
        return None

    digits = ""

    for char in str(latency):
        if char.isdigit():
            digits += char

    if digits == "":
        return None

    return int(digits)


def track_network_events(new_devices):
    global previous_device_states

    current_states = {}

    for device in new_devices:
        ip = device["ip"]
        hostname = device.get("hostname", "Unknown")
        health = device.get("health", "Unknown")
        latency = device.get("latency", "Unknown")

        current_states[ip] = {
            "hostname": hostname,
            "health": health,
            "latency": latency
        }

        old = previous_device_states.get(ip)

        if old is None:
            log_event("DISCOVERED", f"{ip} ({hostname}) discovered ({health})")
            continue

        if old["health"] != health:
            if health == "Offline":
                log_event("ALERT", f"{ip} ({hostname}) went offline")
            elif old["health"] == "Offline" and health != "Offline":
                log_event("RECOVERY", f"{ip} ({hostname}) came back online")
            else:
                log_event("STATUS", f"{ip} changed from {old['health']} to {health}")

        old_latency = extract_latency_ms(old.get("latency"))
        new_latency = extract_latency_ms(latency)

        if old_latency is not None and new_latency is not None and old_latency > 0:
            if new_latency >= old_latency * 3 and new_latency >= 100:
                log_event(
                    "WARNING",
                    f"{ip} ({hostname}) latency increased from {old_latency}ms to {new_latency}ms"
                )

    for old_ip, old_device in previous_device_states.items():
        if old_ip not in current_states:
            log_event(
                "MISSING",
                f"{old_ip} ({old_device.get('hostname', 'Unknown')}) disappeared from scan"
            )

    previous_device_states = current_states
    save_current_states(current_states)