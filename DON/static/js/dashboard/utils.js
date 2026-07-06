function safeText(value) {
    if (value === null || value === undefined || value === "") {
        return "Unknown";
    }
    return value;
}

function portsToText(ports) {
    if (!ports || ports.length === 0) {
        return "";
    }
    return Array.isArray(ports) ? ports.join(", ") : ports;
}

function getActionHTML(device, actions) {
    let html = "-";

    actions.forEach(actionDevice => {
        if (actionDevice.ip === device.ip) {
            const checked = actionDevice.actions_checked || "";

            if (checked.includes("Roku")) {
                html = `<a class="action-link" href="/roku/${device.ip}">Roku</a>`;
            } else if (checked.includes("Desktop")) {
                html = `<a class="action-link" href="/desktop/">Desktop</a>`;
            }
        }
    });

    return html;
}

