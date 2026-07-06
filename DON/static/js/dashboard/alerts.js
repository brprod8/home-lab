function updateAlerts(devices) {
    const offlineDevices = devices.filter(device => device.health === "Offline");
    let html = "";

    if (offlineDevices.length === 0) {
        html = `<div class="clear-box">No active alerts.</div>`;
    } else {
        offlineDevices.forEach(device => {
            html += `
                <div class="alert-box">
                    ⚠ ${device.ip} is offline<br>
                    <small>${safeText(device.hostname)} did not respond during the latest scan.</small>
                </div>
            `;
        });
    }

    document.getElementById("recentAlerts").innerHTML = html;
}

