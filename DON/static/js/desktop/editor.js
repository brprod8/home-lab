document.getElementById("codeForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const code = document.getElementById("codeBox").value;
    const outputBox = document.getElementById("outputBox");
    const statusBox = document.getElementById("currentJobStatus");

    statusBox.className = "job-status queued";
    statusBox.textContent = "QUEUED";

    document.getElementById("jobScript").textContent = "phone_code.py";
    outputBox.textContent =
        "Phone submitted code...\\n\\n" +
        "Saving code to scripts/phone_code.py...\\n" +
        "Waiting for background worker...";
    updateProgress("queued");
    setPipeline("queued", "phone_code.py");

    const response = await fetch("/desktop/run_code", {
        method: "POST",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
        body: "code=" + encodeURIComponent(code)
    });

    const data = await response.json();

    if (data.job_id) {
        document.getElementById("jobId").textContent = data.job_id;
        outputBox.textContent =
            "Phone submitted code...\\n\\n" +
            "✓ Saved to scripts/phone_code.py\\n" +
            "✓ Job queued: " + data.job_id + "\\n" +
            "Launching Python...";
        pollJob(data.job_id);
    } else {
        statusBox.className = "job-status failed";
        statusBox.textContent = "FAILED";
        outputBox.textContent = data.error || "Unknown error.";
        updateProgress("failed");
        setPipeline("failed", "phone_code.py");
    }
});

async function saveScript() {
    const code = document.getElementById("codeBox").value;
    let scriptName = document.getElementById("scriptNameInput").value.trim();
    const outputBox = document.getElementById("outputBox");

    if (!scriptName) {
        outputBox.textContent = "Enter a script name first. Example: ping_subnet";
        return;
    }

    if (!scriptName.endsWith(".py")) {
        scriptName += ".py";
    }

    outputBox.textContent =
        "Saving script...\\n\\n" +
        "File: scripts/" + scriptName;

    const response = await fetch("/desktop/save_script", {
        method: "POST",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
        body:
            "script_name=" + encodeURIComponent(scriptName) +
            "&code=" + encodeURIComponent(code)
    });

    const data = await response.json();

    if (response.ok) {
        outputBox.textContent =
            "✓ Saved successfully.\\n\\n" +
            "File: scripts/" + data.script_name;
        refreshScripts();
    } else {
        outputBox.textContent = "Save failed: " + (data.error || "Unknown error");
    }
}
