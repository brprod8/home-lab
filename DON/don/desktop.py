from flask import Blueprint, render_template, request, jsonify, send_from_directory
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
OUTPUT_FOLDER = "output"

jobs = {}
job_history = []


def safe_name(name):
    if not name:
        return None

    name = name.strip()

    if ".." in name or "/" in name or "\\" in name:
        return None

    return name


def get_scripts():
    os.makedirs(SCRIPTS_FOLDER, exist_ok=True)
    return sorted([f for f in os.listdir(SCRIPTS_FOLDER) if f.endswith(".py")])


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

    thread = threading.Thread(target=run_python_job, args=(job_id,), daemon=True)
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

        job["status"] = "completed" if result.returncode == 0 else "failed"
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
    return render_template(
        "desktop.html",
        health=get_desktop_health(),
        scripts=get_scripts(),
        jobs=job_history
    )


@desktop_bp.route("/editor")
def python_editor_page():
    return render_template(
        "python_editor.html",
        scripts=get_scripts()
    )


@desktop_bp.route("/run_code", methods=["POST"])
def run_code():
    code = request.form.get("code", "")

    if not code.strip():
        return jsonify({"error": "No code entered."}), 400

    os.makedirs(SCRIPTS_FOLDER, exist_ok=True)

    script_name = "phone_code.py"
    script_path = os.path.join(SCRIPTS_FOLDER, script_name)

    with open(script_path, "w", encoding="utf-8") as file:
        file.write(code)

    job_id = create_job(
        job_type="live_code",
        file_path=script_path,
        script_name=script_name
    )

    return jsonify({
        "job_id": job_id,
        "status": "queued",
        "message": "Code saved to scripts/phone_code.py"
    })


@desktop_bp.route("/run", methods=["POST"])
def run_script():
    script_name = safe_name(request.form.get("script", ""))

    if not script_name:
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

    script_name = safe_name(script_name)

    if not script_name:
        return jsonify({"error": "Invalid script name."}), 400

    os.makedirs(SCRIPTS_FOLDER, exist_ok=True)

    script_path = os.path.join(SCRIPTS_FOLDER, script_name)

    with open(script_path, "w", encoding="utf-8") as file:
        file.write(code)

    return jsonify({
        "message": "Script saved.",
        "script_name": script_name
    })


@desktop_bp.route("/delete_script", methods=["POST"])
def delete_script():
    script_name = safe_name(request.form.get("script_name", ""))

    if not script_name:
        return jsonify({"error": "Invalid script name."}), 400

    if script_name == "phone_code.py":
        return jsonify({"error": "phone_code.py cannot be deleted."}), 400

    script_path = os.path.join(SCRIPTS_FOLDER, script_name)

    if not os.path.exists(script_path):
        return jsonify({"error": "Script not found."}), 404

    os.remove(script_path)

    return jsonify({
        "message": "Script deleted.",
        "script_name": script_name
    })


@desktop_bp.route("/scripts")
def list_scripts():
    return jsonify({"scripts": get_scripts()})


@desktop_bp.route("/files")
def list_output_files():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    files = []

    for root, dirs, filenames in os.walk(OUTPUT_FOLDER):
        for filename in filenames:
            full_path = os.path.join(root, filename)
            relative_path = os.path.relpath(full_path, OUTPUT_FOLDER)

            relative_url = relative_path.replace("\\", "/")

            files.append({
                "name": filename,
                "path": relative_url,
                "size": os.path.getsize(full_path),
                "url": f"/desktop/files/{relative_url}"
            })

    return jsonify({"files": files})


@desktop_bp.route("/files/<path:filename>")
def view_output_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)


@desktop_bp.route("/delete_file", methods=["POST"])
def delete_output_file():
    filename = request.form.get("filename", "").strip()

    if not filename or ".." in filename:
        return jsonify({"error": "Invalid filename."}), 400

    file_path = os.path.join(OUTPUT_FOLDER, filename)

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found."}), 404

    os.remove(file_path)

    return jsonify({
        "message": "File deleted.",
        "filename": filename
    })