from flask import Blueprint, render_template, request, jsonify
from don.actions import get_desktop_health
import subprocess
import os

desktop_bp = Blueprint("desktop", __name__)

SCRIPTS_FOLDER = "scripts"


def get_scripts():
    os.makedirs(SCRIPTS_FOLDER, exist_ok=True)
    return [f for f in os.listdir(SCRIPTS_FOLDER) if f.endswith(".py")]


@desktop_bp.route("/")
def desktop_page():
    health = get_desktop_health()
    scripts = get_scripts()
    return render_template("desktop.html", health=health, scripts=scripts)


@desktop_bp.route("/run_code", methods=["POST"])
def run_code():
    code = request.form.get("code", "")

    if not code.strip():
        return "No code entered."

    os.makedirs(SCRIPTS_FOLDER, exist_ok=True)

    temp_file = os.path.join(SCRIPTS_FOLDER, "phone_code.py")

    with open(temp_file, "w", encoding="utf-8") as file:
        file.write(code)

    try:
        result = subprocess.run(
            ["python", temp_file],
            capture_output=True,
            text=True,
            timeout=20
        )

        output = result.stdout + result.stderr

        if not output.strip():
            output = "Script ran successfully, but produced no output."

        return output

    except subprocess.TimeoutExpired:
        return "Script timed out after 20 seconds."


@desktop_bp.route("/run", methods=["POST"])
def run_script():
    script_name = request.form.get("script", "")

    if not script_name:
        return "No script selected."

    if ".." in script_name or "/" in script_name or "\\" in script_name:
        return "Invalid script name."

    safe_path = os.path.join(SCRIPTS_FOLDER, script_name)

    if not os.path.exists(safe_path):
        return "Script not found."

    try:
        result = subprocess.run(
            ["python", safe_path],
            capture_output=True,
            text=True,
            timeout=20
        )

        output = result.stdout + result.stderr

        if not output.strip():
            output = "Script ran successfully, but produced no output."

        return output

    except subprocess.TimeoutExpired:
        return "Script timed out after 20 seconds."


@desktop_bp.route("/health")
def desktop_health():
    return jsonify(get_desktop_health())