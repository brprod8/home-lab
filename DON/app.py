from flask import Flask, render_template, jsonify, redirect

from don.network_events import track_network_events
from don.config import SUBNET
from don.scanner import scan_network
from don.action_probe import build_action_devices_table
from don.roku import roku_bp
from don.desktop import desktop_bp


app = Flask(__name__)

app.register_blueprint(roku_bp, url_prefix="/roku")
app.register_blueprint(desktop_bp, url_prefix="/desktop")


# --------------------------------------------------
# Cached Network Data
# --------------------------------------------------

latest_devices = []
latest_actions = []
previous_device_states = {}

def refresh_network():
    global latest_devices
    global latest_actions

    latest_devices = scan_network(SUBNET)
    latest_actions = build_action_devices_table(latest_devices)

    track_network_events(latest_devices)


# # Scan once when Flask starts
refresh_network()


# --------------------------------------------------
# Dashboard
# --------------------------------------------------

@app.route("/")
def main_dashboard():

    return render_template(
        "main.html",
        devices=latest_devices,
        actions=latest_actions
    )


# --------------------------------------------------
# Refresh Network
# --------------------------------------------------

@app.route("/api/refresh")
def api_refresh():
    global latest_devices, latest_actions
    refresh_network()


    latest_devices = scan_network(SUBNET)
    latest_actions = build_action_devices_table(latest_devices)

    return jsonify({
        "devices": latest_devices,
        "actions": latest_actions
    })

# --------------------------------------------------
# Topology
# --------------------------------------------------

@app.route("/topology")
@app.route("/topology/")
def topology_page():

    return render_template(
        "topology.html",
        devices=latest_devices
    )


# --------------------------------------------------
# Devices
# --------------------------------------------------

@app.route("/devices")
def devices_page():

    return render_template(
        "main.html",
        devices=latest_devices,
        actions=latest_actions
    )


# --------------------------------------------------
# Alerts
# --------------------------------------------------

@app.route("/alerts")
def alerts_page():

    return render_template(
        "main.html",
        devices=latest_devices,
        actions=latest_actions
    )


# --------------------------------------------------
# Actions
# --------------------------------------------------

@app.route("/actions")
def actions_page():

    return render_template(
        "main.html",
        devices=latest_devices,
        actions=latest_actions
    )


# --------------------------------------------------
# Intelligence
# --------------------------------------------------

@app.route("/intelligence")
def intelligence_page():

    return render_template(
        "main.html",
        devices=latest_devices,
        actions=latest_actions
    )


# --------------------------------------------------
# Settings
# --------------------------------------------------

@app.route("/settings")
def settings_page():

    return render_template(
        "main.html",
        devices=latest_devices,
        actions=latest_actions
    )


# --------------------------------------------------
# API
# --------------------------------------------------

@app.route("/api/health")
def api_health():

    return jsonify(latest_devices)


@app.route("/api/actions")
def api_actions():

    return jsonify(latest_actions)

@app.route("/device/<ip>")
def device_detail(ip):
    device = None

    for d in latest_devices:
        if d["ip"] == ip:
            device = d
            break

    if device is None:
        return "Device not found", 404

    actions = []

    for a in latest_actions:
        if a["ip"] == ip:
            actions = a["actions_checked"]

    return render_template(
        "device_detail.html",
        device=device,
        actions=actions
    )


@app.route("/api/ping_device/<ip>")
def ping_device_api(ip):
    import subprocess

    result = subprocess.run(
        ["ping", "-n", "1", "-w", "500", ip],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    online = result.returncode == 0
   

    return jsonify({
        "ip": ip,
        "online": online,
        "message": "Device responded" if online else "No response"
    })


@app.route("/api/discover")
def api_discover():
    global latest_devices, latest_actions

    latest_devices = scan_network(SUBNET)
    latest_actions = build_action_devices_table(latest_devices)

    return jsonify({
        "devices": latest_devices,
        "actions": latest_actions,
        "message": "Network discovery complete"
    })


@app.route("/api/ping_don_devices")
def api_ping_don_devices():
    import subprocess

    results = []

    for device in latest_devices:
        ip = device["ip"]

        result = subprocess.run(
            ["ping", "-n", "1", "-w", "500", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        online = result.returncode == 0

        results.append({
            "ip": ip,
            "hostname": device.get("hostname", "Unknown"),
            "online": online,
            "message": "Online" if online else "No response"
        })

    return jsonify({
        "results": results,
        "message": "Pinged all DON table devices"
    })
#------------------------------------------------------#
@app.route("/logs")
def logs_page():
    try:
        with open("logs/don.log", "r") as file:
            logs = file.read()
    except FileNotFoundError:
        logs = "No logs yet."

    return f"<pre style='background:#111;color:#0f0;padding:20px;'>{logs}</pre>"




@app.route("/events")
def events_page():
    try:
        with open("logs/events.log", "r", encoding="utf-8") as file:
            events = file.read()
    except FileNotFoundError:
        events = "No events yet."

    return f"<pre style='background:#111;color:#0f0;padding:20px;'>{events}</pre>"

# --------------------------------------------------
# Run
# --------------------------------------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )