function updatePingMonitor(devices) {
    let html = "";

    devices.forEach(device => {
        const isOffline = device.health === "Offline";

        html += `
            <div class="ping-row">
                <div>
                    <a class="action-link" href="/device/${device.ip}">${device.ip}</a>
                </div>
                <div class="${isOffline ? "offline" : "ping-ms"}">
                    ${isOffline ? "Offline" : safeText(device.latency)}
                </div>
                <div class="spark"></div>
            </div>
        `;
    });

    document.getElementById("pingMonitor").innerHTML = html;
}

