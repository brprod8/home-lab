function updateTopPorts(devices) {
    const counts = {};

    devices.forEach(device => {
        if (Array.isArray(device.ports)) {
            device.ports.forEach(port => {
                counts[port] = (counts[port] || 0) + 1;
            });
        }
    });

    const sorted = Object.entries(counts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 4);

    let html = "";

    if (sorted.length === 0) {
        html = "<div>No open ports detected.</div>";
    } else {
        sorted.forEach(([port, count]) => {
            html += `<div>🔵 ${port} seen on ${count} device(s)</div>`;
        });
    }

    document.getElementById("topPorts").innerHTML = html;
}

