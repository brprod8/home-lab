function updateDeviceTable(devices, actions) {
    let html = `
        <tr>
            <th>Hostname</th>
            <th>IP Address</th>
            <th>MAC Address</th>
            <th>Status</th>
            <th>Response Time</th>
            <th>Open Ports</th>
            <th>Type</th>
            <th>Actions</th>
        </tr>
    `;

    devices.forEach(device => {
        const healthHTML =
            device.health === "Healthy"
                ? `<span class="healthy-pill">● Healthy</span>`
                : `<span class="offline-pill">● ${safeText(device.health)}</span>`;

        html += `
            <tr>
                <td>${safeText(device.hostname)}</td>
                <td><a class="action-link" href="/device/${device.ip}">${device.ip}</a></td>
                <td>${safeText(device.mac)}</td>
                <td>${healthHTML}</td>
                <td>${safeText(device.latency)}</td>
                <td>${portsToText(device.ports)}</td>
                <td>${safeText(device.type)}</td>
                <td>${getActionHTML(device, actions)}</td>
            </tr>
        `;
    });

    document.getElementById("deviceTable").innerHTML = html;
}

