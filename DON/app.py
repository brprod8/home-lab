from flask import Flask, render_template, jsonify, redirect

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


def refresh_network():
    """
    Scan the network once and cache the results.
    """
    global latest_devices
    global latest_actions

    latest_devices = scan_network(SUBNET)
    latest_actions = build_action_devices_table(latest_devices)


# Scan once when Flask starts
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


# --------------------------------------------------
# Run
# --------------------------------------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )