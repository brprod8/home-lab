from flask import Blueprint, render_template, request, jsonify
from don.actions import get_desktop_health
from don.logger import log_info, log_error
import subprocess
import os
import uuid
import threading
import time
from datetime import datetime

desktop_bp = Blueprint("desktop", __name__)

SCRIPTS_FOLDER = "scripts"

jobs = {}
job_history = []


def get_scripts():
    os.makedirs(SCRIPTS_FOLDER, exist_ok=True)
    return [f for f in os.listdir(SCRIPTS_FOLDER) if f.endswith(".py")]


def create_job(job_type, file_path, script_name=None):
    job_id = str(uuid.uuid4())

    jobs[job_id] = {
        "job_id": job_id,
        "type": job_type,
        "script_name": script_name or os.path.basename(file_path),
        "file_path": file_path,
        "status": "queued",
        "output": "",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "started_at": None,
        "completed_at": None,
        "runtime_seconds": None
    }

    log_info(f"Job queued: {job_id} | {job_type} | {script_name}")

    thread = threading.Thread(
        target=run_python_job,
        args=(job_id,),
        daemon=True
    )

    thread.start()

    return job_id


def run_python_job(job_id):
    job = jobs[job_id]

    job["status"] = "running"
    job["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    start_time = time.time()

    log_info(f"Job started: {job_id}")

    try:
        result = subprocess.run(
            ["python", job["file_path"]],
            capture_output=True,
            text=True,
            timeout=300
        )

        output = result.stdout + result.stderr

        if not output.strip():
            output = "Script finished with no output."

        if result.returncode == 0:
            job["status"] = "completed"
            log_info(f"Job completed: {job_id}")
        else:
            job["status"] = "failed"
            log_error(f"Job failed: {job_id}")

        job["output"] = output

    except subprocess.TimeoutExpired:
        job["status"] = "timeout"
        job["output"] = "Script timed out after 300 seconds."
        log_error(f"Job timeout: {job_id}")

    except Exception as error:
        job["status"] = "failed"
        job["output"] = str(error)
        log_error(f"Job exception: {job_id} | {error}")

    finally:
        job["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        job["runtime_seconds"] = round(time.time() - start_time, 2)

        job_history.insert(0, job.copy())

        if len(job_history) > 20:
            job_history.pop()


@desktop_bp.route("/")
def desktop_page():
    health = get_desktop_health()
    scripts = get_scripts()

    return render_template(
        "desktop.html",
        health=health,
        scripts=scripts,
        jobs=job_history
    )


@desktop_bp.route("/run_code", methods=["POST"])
def run_code():
    code = request.form.get("code", "")

    if not code.strip():
        return jsonify({"error": "No code entered."}), 400

    os.makedirs(SCRIPTS_FOLDER, exist_ok=True)

    temp_file = os.path.join(SCRIPTS_FOLDER, "phone_code.py")

    with open(temp_file, "w", encoding="utf-8") as file:
        file.write(code)

    job_id = create_job(
        job_type="live_code",
        file_path=temp_file,
        script_name="phone_code.py"
    )

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

    job_id = create_job(
        job_type="saved_script",
        file_path=script_path,
        script_name=script_name
    )

    return jsonify({
        "job_id": job_id,
        "status": "queued"
    })


@desktop_bp.route("/job/<job_id>")
def job_status(job_id):
    if job_id not in jobs:
        return jsonify({
            "status": "not_found",
            "output": "Job not found or server restarted."
        }), 404

    return jsonify(jobs[job_id])


@desktop_bp.route("/jobs")
def jobs_list():
    return jsonify({
        "active_jobs": list(jobs.values()),
        "history": job_history
    })


@desktop_bp.route("/health")
def desktop_health():
    return jsonify(get_desktop_health())

@desktop_bp.route("/save_script", methods=["POST"])
def save_script():
    script_name = request.form.get("script_name", "").strip()
    code = request.form.get("code", "")

    if not script_name:
        return jsonify({"error": "No script name provided."}), 400

    if not script_name.endswith(".py"):
        script_name += ".py"

    if ".." in script_name or "/" in script_name or "\\" in script_name:
        return jsonify({"error": "Invalid script name."}), 400

    os.makedirs(SCRIPTS_FOLDER, exist_ok=True)

    script_path = os.path.join(SCRIPTS_FOLDER, script_name)

    with open(script_path, "w", encoding="utf-8") as file:
        file.write(code)

    return jsonify({"message": "Script saved.", "script_name": script_name})


@desktop_bp.route("/scripts")
def list_scripts():
    return jsonify({"scripts": get_scripts()})