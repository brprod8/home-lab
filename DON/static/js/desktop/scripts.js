document.getElementById("scriptForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    const script = document.getElementById("scriptSelect").value;
    runSavedScript(script);
});

async function runSavedScript(script) {
    const outputBox = document.getElementById("outputBox");
    const statusBox = document.getElementById("currentJobStatus");

    statusBox.className = "job-status queued";
    statusBox.textContent = "QUEUED";
    document.getElementById("jobScript").textContent = script;

    outputBox.textContent =
        "Saved script selected...\\n\\n" +
        "File: scripts/" + script + "\\n" +
        "Preparing background worker...";

    updateProgress("queued");
    setPipeline("queued", script);

    const response = await fetch("/desktop/run", {
        method: "POST",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
        body: "script=" + encodeURIComponent(script)
    });

    const data = await response.json();

    if (data.job_id) {
        document.getElementById("jobId").textContent = data.job_id;
        outputBox.textContent =
            "✓ Script found: scripts/" + script + "\\n" +
            "✓ Job queued: " + data.job_id + "\\n" +
            "Launching Python...";
        pollJob(data.job_id);
    } else {
        statusBox.className = "job-status failed";
        statusBox.textContent = "FAILED";
        outputBox.textContent = data.error || "Unknown error.";
        updateProgress("failed");
        setPipeline("failed", script);
    }
}

async function refreshScripts() {
    const response = await fetch("/desktop/scripts");
    const data = await response.json();

    const select = document.getElementById("scriptSelect");
    const list = document.getElementById("scriptsList");

    select.innerHTML = "";
    list.innerHTML = "";

    if (!data.scripts || data.scripts.length === 0) {
        list.textContent = "No saved scripts yet.";
        return;
    }

    data.scripts.forEach(script => {
        const option = document.createElement("option");
        option.value = script;
        option.textContent = script;
        select.appendChild(option);

        const item = document.createElement("div");
        item.className = "script-item";
        item.innerHTML = `
            <div>
                <div class="script-name">📄 ${script}</div>
                <div class="script-meta">Saved Python script</div>
            </div>
            <button onclick="runSavedScript('${script}')">▶</button>
        `;
        list.appendChild(item);
    });
}

async function deleteScript(scriptName) {

    if (!confirm(`Delete ${scriptName}?`))
        return;

    const form = new FormData();
    form.append("script_name", scriptName);

    const response = await fetch("/desktop/delete_script", {
        method: "POST",
        body: form
    });

    const data = await response.json();

    alert(data.message || data.error);

    refreshScripts();

}