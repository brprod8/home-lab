from flask import Blueprint, render_template, request, jsonify
from don.actions import get_desktop_health
import subprocess
import os
import uuid
import threading

desktop_bp = Blueprint("desktop", __name__)

SCRIPTS_FOLDER = "scripts"
jobs = {}


def get_scripts():
    os.makedirs(SCRIPTS_FOLDER, exist_ok=True)
    return [f for f in os.listdir(SCRIPTS_FOLDER) if f.endswith(".py")]


def run_python_job(job_id, file_path):
    jobs[job_id]["status"] = "running"

    try:
        result = subprocess.run(
            ["python", file_path],
            capture_output=True,
            text=True,
            timeout=300
        )

        output = result.stdout + result.stderr

        if not output.strip():
            output = "Script finished with no output."

        jobs[job_id]["status"] = "complete"
        jobs[job_id]["output"] = output

    except subprocess.TimeoutExpired:
        jobs[job_id]["status"] = "timeout"
        jobs[job_id]["output"] = "Script timed out after 300 seconds."

    except Exception as error:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["output"] = str(error)


@desktop_bp.route("/")
def desktop_page():
    health = get_desktop_health()
    scripts = get_scripts()
    return render_template("desktop.html", health=health, scripts=scripts)


@desktop_bp.route("/run_code", methods=["POST"])
def run_code():
    code = request.form.get("code", "")

    if not code.strip():
        return jsonify({"error": "No code entered."}), 400

    os.makedirs(SCRIPTS_FOLDER, exist_ok=True)

    temp_file = os.path.join(SCRIPTS_FOLDER, "phone_code.py")

    with open(temp_file, "w", encoding="utf-8") as file:
        file.write(code)

    job_id = str(uuid.uuid4())

    jobs[job_id] = {
        "status": "queued",
        "output": ""
    }

    thread = threading.Thread(
        target=run_python_job,
        args=(job_id, temp_file),
        daemon=True
    )

    thread.start()

    return jsonify({
        "job_id": job_id,
        "status": "queued"
    })


@desktop_bp.route("/run", methods=["POST"])
def run_script():
    script_name = request.form.get("script", "")

    if not script_name:
        return jsonify({"error": "No script selected."}), 400

    if ".." in script_name or "/" in script_name or "\\" in script_name:
        return jsonify({"error": "Invalid script name."}), 400

    script_path = os.path.join(SCRIPTS_FOLDER, script_name)

    if not os.path.exists(script_path):
        return jsonify({"error": "Script not found."}), 404

    job_id = str(uuid.uuid4())

    jobs[job_id] = {
        "status": "queued",
        "output": ""
    }

    thread = threading.Thread(
        target=run_python_job,
        args=(job_id, script_path),
        daemon=True
    )

    thread.start()

    return jsonify({
        "job_id": job_id,
        "status": "queued"
    })


@desktop_bp.route("/job/<job_id>")
def job_status(job_id):
    if job_id not in jobs:
        return jsonify({
            "status": "not_found",
            "output": "Job not found."
        }), 404

    return jsonify(jobs[job_id])


@desktop_bp.route("/health")
def desktop_health():
    return jsonify(get_desktop_health())