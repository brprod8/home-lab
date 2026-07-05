from flask import Blueprint, render_template
from don.config import SUBNET
from don.scanner import scan_network

topology_bp = Blueprint("topology", __name__)


@topology_bp.route("/")
def topology():

    devices = scan_network(SUBNET)

    return render_template(
        "topology.html",
        devices=devices
    )