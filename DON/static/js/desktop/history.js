async function loadJobHistory() {
    const response = await fetch("/desktop/jobs");
    const data = await response.json();

    const historyBox = document.getElementById("jobHistory");
    historyBox.innerHTML = "";

    if (!data.history || data.history.length === 0) {
        historyBox.textContent = "No job history yet.";
        return;
    }

    data.history.forEach(job => {
        const item = document.createElement("div");
        item.className = "history-item";

        let icon = "🟢";
        if (job.status === "failed") icon = "🔴";
        if (job.status === "timeout") icon = "🟡";
        if (job.status === "running") icon = "🟢";

        item.innerHTML = `
            <div>
                <div class="history-name">${icon} ${job.script_name}</div>
                <div class="history-meta">
                    Status: ${job.status}<br>
                    Runtime: ${job.runtime_seconds} seconds<br>
                    Completed: ${job.completed_at}
                </div>
            </div>
            <button onclick="viewJob('${job.job_id}')">View Output</button>
        `;

        historyBox.appendChild(item);
    });
}

async function viewJob(jobId) {
    const response = await fetch(`/desktop/job/${jobId}`);
    const job = await response.json();

    if (job.status === "not_found") {
        document.getElementById("outputBox").textContent = "Job not found or server restarted.";
        return;
    }

    renderJob(job);
}
