function updateDashboard(data) {
    const devices = data.devices || [];
    const actions = data.actions || [];

    updateStats(devices);
    updateDeviceTable(devices, actions);
    updatePingMonitor(devices);
    updateAlerts(devices);
    updateTopPorts(devices);
    updateGraph(devices);
}

async function requestLiveInfo() {
    const buttons = document.querySelectorAll(".live-btn, .quick-live, .quick-ping, .quick-discover");

    buttons.forEach(btn => {
        btn.dataset.originalText = btn.dataset.originalText || btn.textContent;
        btn.textContent = "⟳ Scanning...";
        btn.disabled = true;
    });

    try {
        const response = await fetch("/api/refresh");

        if (!response.ok) {
            throw new Error("Refresh API returned " + response.status);
        }

        const data = await response.json();

        updateDashboard(data);
        updateClock();

        buttons.forEach(btn => {
            btn.textContent = "✓ Updated";
            btn.disabled = false;
        });

        setTimeout(() => {
            buttons.forEach(btn => {
                btn.textContent = btn.dataset.originalText;
            });
        }, 1500);

    } catch (error) {
        console.error("Refresh failed:", error);

        buttons.forEach(btn => {
            btn.textContent = "✗ Failed";
            btn.disabled = false;
        });

        setTimeout(() => {
            buttons.forEach(btn => {
                btn.textContent = btn.dataset.originalText;
            });
        }, 2000);
    }
}

