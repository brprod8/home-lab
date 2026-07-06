from flask import Blueprint, render_template, request
from don.actions import (
    roku_home, roku_back, roku_select, roku_up, roku_down,
    roku_left, roku_right, roku_volume_up, roku_volume_down,
    roku_volume_mute, roku_youtube, roku_play_pause,
    roku_search, roku_info, roku_type_text
)
from don.logger import log_info, log_error

roku_bp = Blueprint("roku", __name__)


@roku_bp.route("/<ip>")
def roku_page(ip):
    return render_template("roku.html", ip=ip)


@roku_bp.route("/<ip>/<command>", methods=["GET", "POST"])
def roku_command(ip, command):
    commands = {
        "home": roku_home,
        "back": roku_back,
        "select": roku_select,
        "up": roku_up,
        "down": roku_down,
        "left": roku_left,
        "right": roku_right,
        "volume_up": roku_volume_up,
        "volume_down": roku_volume_down,
        "mute": roku_volume_mute,
        "youtube": roku_youtube,
        "play": roku_play_pause,
        "search": roku_search,
        "info": roku_info,
    }

    if command not in commands:
        return f"Unknown command: {command}", 400

    commands[command](ip)
    return f"{command} sent"


@roku_bp.route("/<ip>/type_text", methods=["POST"])
def roku_type_text_route(ip):
    text = request.form.get("text", "")

    if not text.strip():
        return "No text entered.", 400

    result = roku_type_text(ip, text)

    if result.get("success"):
        return f"Typed: {text}"

    return f"Failed: {result.get('error', result)}", 500