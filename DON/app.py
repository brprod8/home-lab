from flask import Flask, render_template, jsonify, redirect

from don.network_events import track_network_events
from don.config import SUBNET
from don.scanner import scan_network
from don.action_probe import build_action_devices_table
from don.roku import roku_bp
from don.desktop import desktop_bp
from don.network_utils import get_active_host_ip
from don.ping_tools import ping, get_latency




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

@app.route("/api/discover")
def api_discover():
    """
    Discover Network:
    Full subnet discovery.

    This scans the configured subnet and rebuilds DON inventory.

    Note:
    This is not necessarily a true broadcast to x.x.x.255.
    It depends on how scan_network(SUBNET) is written.
    Usually this is a ping sweep / ARP-style discovery across:
        192.168.86.1 - 192.168.86.254
    """

    global latest_devices
    global latest_actions

    latest_devices = scan_network(SUBNET)
    latest_actions = build_action_devices_table(latest_devices)

    track_network_events(latest_devices)

    return jsonify({
        "success": True,
        "mode": "discover",
        "message": f"Discovery complete on {SUBNET}. {len(latest_devices)} device(s) found.",
        "devices": latest_devices,
        "actions": latest_actions
    })


@app.route("/api/ping_don_devices")
def api_ping_don_devices():
    """
    Ping DON Devices:
    Ping only devices already inside the DON table.

    This does NOT scan the whole subnet.
    This does NOT discover new devices.
    """

    import subprocess

    global latest_devices
    global latest_actions

    updated_devices = []
    results = []



    for device in latest_devices:

        ip = device.get("ip")

        online, output = ping(ip)

        updated_device = device.copy()

        updated_device["health"] = "Healthy" if online else "Offline"

        if online:
            updated_device["latency"] = get_latency(output)
        else:
            updated_device["latency"] = "-"

        updated_devices.append(updated_device)

        results.append({
            "ip": ip,
            "hostname": device.get("hostname", "Unknown"),
            "online": online,
            "latency": updated_device["latency"],
            "message": "Ping successful" if online else "No response"
        })

    latest_devices = updated_devices
    latest_actions = build_action_devices_table(latest_devices)

    track_network_events(latest_devices)

    return jsonify({
        "success": True,
        "mode": "ping_known_devices",
        "message": f"Pinged {len(results)} DON device(s).",
        "results": results,
        "devices": latest_devices,
        "actions": latest_actions
    })


@app.route("/api/refresh")
def api_refresh():
    """
    Live Info:
    Return cached dashboard data only.
    No scan.
    No ping sweep.
    """

    return jsonify({
        "success": True,
        "mode": "refresh",
        "message": "Dashboard refreshed from cached data.",
        "devices": latest_devices,
        "actions": latest_actions
    })


@app.route("/api/live")
def api_live():
    """
    Live refresh.
    Same as refresh_network, used for dashboard live updates.
    """
    refresh_network()

    return jsonify({
        "mode": "live",
        "message": "Live info refreshed",
        "devices": latest_devices,
        "actions": latest_actions
    })

# --------------------------------------------------
# Run
# --------------------------------------------------

if __name__ == "__main__":
    host = get_active_host_ip()

    print(f"DON starting on: http://{host}:5000")

    app.run(
        host=host,
        port=5000,
        debug=True
    )
