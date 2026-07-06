function updateStats(devices) {
    let healthy = 0;
    let offline = 0;
    let totalPorts = 0;

    devices.forEach(device => {
        if (device.health === "Healthy") {
            healthy++;
        } else {
            offline++;
        }

        if (Array.isArray(device.ports)) {
            totalPorts += device.ports.length;
        }
    });

    const total = devices.length;
    const percent = total > 0 ? Math.round((healthy / total) * 100) : 0;

    document.getElementById("totalDevices").innerText = total;
    document.getElementById("healthyDevices").innerText = healthy;
    document.getElementById("alertDevices").innerText = offline;
    document.getElementById("openPorts").innerText = totalPorts;

    document.getElementById("totalDevicesSub").innerText =
        "Online: " + (total - offline) + " • Offline: " + offline;

    document.getElementById("healthyPercent").innerText = percent + "% of devices";
    document.getElementById("donutPercent").innerText = percent + "%";

    document.getElementById("healthDonut").style.background =
        `conic-gradient(#22c55e 0 ${percent}%, #ef4444 ${percent}% 100%)`;

    document.getElementById("alertsSub").innerText =
        offline === 0 ? "No issues detected" : "Requires attention";

    document.getElementById("systemStatusText").innerText =
        offline === 0 ? "Healthy" : "Attention Needed";

    document.getElementById("systemStatusText").style.color =
        offline === 0 ? "#22c55e" : "#f59e0b";

    document.getElementById("systemStatusSub").innerText =
        offline === 0 ? "All systems operational" : offline + " device(s) need attention";
}

