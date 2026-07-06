function clearOutput() {
    document.getElementById("outputBox").textContent = "Output cleared.";
    resetPipeline();
    updateProgress("idle");
}

function stopVisualJob() {
    if (activePoll) {
        clearInterval(activePoll);
        activePoll = null;
        stopRuntimeTimer(null);
        document.getElementById("currentJobStatus").className = "job-status timeout";
        document.getElementById("currentJobStatus").textContent = "POLLING STOPPED";
    }
}
