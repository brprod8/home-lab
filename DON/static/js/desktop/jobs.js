function getStatusClass(status) {
    if (status === "running") return "job-status running";
    if (status === "completed") return "job-status completed";
    if (status === "failed") return "job-status failed";
    if (status === "timeout") return "job-status timeout";
    return "job-status queued";
}

function resetPipeline() {
    document.getElementById("stepSave").textContent = "○ Waiting for job";
    document.getElementById("stepLaunch").textContent = "○ Launch Python";
    document.getElementById("stepRun").textContent = "○ Running";
    document.getElementById("stepDone").textContent = "○ Completed / Failed";

    document.getElementById("stepSave").className = "";
    document.getElementById("stepLaunch").className = "";
    document.getElementById("stepRun").className = "";
    document.getElementById("stepDone").className = "";
}

function setPipeline(status, source) {
    resetPipeline();

    if (status === "queued") {
        document.getElementById("stepSave").textContent =
            source === "phone_code.py" ? "● Saving to scripts/phone_code.py" : "● Preparing saved script";
        document.getElementById("stepSave").className = "active-step";
    }

    if (status === "running") {
        document.getElementById("stepSave").textContent =
            source === "phone_code.py" ? "✓ Saved to scripts/phone_code.py" : "✓ Script found";
        document.getElementById("stepLaunch").textContent = "● Launching Python process";
        document.getElementById("stepRun").textContent = "● Running script";
        document.getElementById("stepLaunch").className = "active-step";
        document.getElementById("stepRun").className = "active-step";
    }

    if (status === "completed") {
        document.getElementById("stepSave").textContent =
            source === "phone_code.py" ? "✓ Saved to scripts/phone_code.py" : "✓ Script found";
        document.getElementById("stepLaunch").textContent = "✓ Python launched";
        document.getElementById("stepRun").textContent = "✓ Output collected";
        document.getElementById("stepDone").textContent = "✓ Completed successfully";
        document.getElementById("stepDone").className = "active-step";
    }

    if (status === "failed" || status === "timeout") {
        document.getElementById("stepDone").textContent = "✗ Job ended with " + status;
        document.getElementById("stepDone").className = "active-step";
    }
}

function updateProgress(status) {
    const bar = document.getElementById("progressBar");

    if (status === "queued") bar.style.width = "20%";
    else if (status === "running") bar.style.width = "70%";
    else if (status === "completed") bar.style.width = "100%";
    else if (status === "failed" || status === "timeout") bar.style.width = "100%";
    else bar.style.width = "0%";
}

function startRuntimeTimer() {
    if (runtimeTimer) clearInterval(runtimeTimer);

    jobStartLocalTime = Date.now();

    runtimeTimer = setInterval(() => {
        const seconds = ((Date.now() - jobStartLocalTime) / 1000).toFixed(2);
        document.getElementById("jobRuntime").textContent = seconds + " seconds";
    }, 500);
}

function stopRuntimeTimer(finalRuntime) {
    if (runtimeTimer) {
        clearInterval(runtimeTimer);
        runtimeTimer = null;
    }

    if (finalRuntime !== null && finalRuntime !== undefined) {
        document.getElementById("jobRuntime").textContent = finalRuntime + " seconds";
    }
}

function renderJob(job) {
    const outputBox = document.getElementById("outputBox");
    const statusBox = document.getElementById("currentJobStatus");

    statusBox.className = getStatusClass(job.status);
    statusBox.textContent = job.status.toUpperCase();

    document.getElementById("jobScript").textContent = job.script_name || "Unknown";
    document.getElementById("jobId").textContent = job.job_id || "None";

    if (job.runtime_seconds !== null && job.runtime_seconds !== undefined) {
        document.getElementById("jobRuntime").textContent = job.runtime_seconds + " seconds";
    }

    updateProgress(job.status);
    setPipeline(job.status, job.script_name);

    outputBox.textContent =
        "Job Source: " + (job.type === "live_code" ? "Phone Python Editor" : "Saved Script") + "\\n" +
        "Executing: scripts/" + job.script_name + "\\n" +
        "Status: " + job.status + "\\n" +
        "Created: " + job.created_at + "\\n" +
        "Started: " + job.started_at + "\\n" +
        "Completed: " + job.completed_at + "\\n" +
        "Runtime: " + job.runtime_seconds + " seconds\\n\\n" +
        "Live Output:\\n" +
        job.output;
}

async function pollJob(jobId) {
    if (activePoll) {
        clearInterval(activePoll);
        activePoll = null;
    }

    startRuntimeTimer();

    activePoll = setInterval(async function () {
        try {
            const response = await fetch(`/desktop/job/${jobId}`);
            const job = await response.json();

            if (job.status === "not_found") {
                clearInterval(activePoll);
                activePoll = null;
                stopRuntimeTimer(null);

                document.getElementById("currentJobStatus").className = "job-status failed";
                document.getElementById("currentJobStatus").textContent = "NOT FOUND";
                document.getElementById("outputBox").textContent = "Job not found or server restarted.";
                updateProgress("failed");
                setPipeline("failed", "unknown");
                return;
            }

            renderJob(job);

            if (
                job.status === "completed" ||
                job.status === "failed" ||
                job.status === "timeout"
            ) {
                clearInterval(activePoll);
                activePoll = null;
                stopRuntimeTimer(job.runtime_seconds);
                renderJob(job);
                loadJobHistory();
                refreshScripts();
            }

        } catch (error) {
            clearInterval(activePoll);
            activePoll = null;
            stopRuntimeTimer(null);

            document.getElementById("currentJobStatus").className = "job-status failed";
            document.getElementById("currentJobStatus").textContent = "POLLING ERROR";
            document.getElementById("outputBox").textContent = "Polling error: " + error;
            updateProgress("failed");
            setPipeline("failed", "unknown");
        }

    }, 1000);
}
