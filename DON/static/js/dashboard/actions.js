async function discoverNetwork() {
    const btn = document.querySelector(".quick-discover");
    const original = btn.textContent;

    btn.disabled = true;
    btn.textContent = "⌁ Discovering...";

    try {
        const response = await fetch("/api/discover");

        if (!response.ok) {
            throw new Error("Discovery request failed");
        }

        const data = await response.json();

        updateDashboard(data);
        updateClock();

        const found = data.devices ? data.devices.length : 0;

        btn.textContent = `✓ Discovery worked • ${found} devices`;

    } catch (error) {
        console.error("Discovery failed:", error);
        btn.textContent = "✗ Discovery failed";
    }

    setTimeout(() => {
        btn.disabled = false;
        btn.textContent = original;
    }, 2500);
}


async function pingDonDevices() {
    const btn = document.querySelector(".quick-ping");
    const original = btn.textContent;

    btn.disabled = true;
    btn.textContent = "⌁ Pinging...";

    try {
        const response = await fetch("/api/ping_don_devices");

        if (!response.ok) {
            throw new Error("Ping request failed");
        }

        const data = await response.json();

        updateDashboard(data);
        updateClock();

        const devices = data.devices || [];
        const online = devices.filter(d => d.health === "Healthy").length;
        const offline = devices.length - online;

        btn.textContent = `✓ Ping worked • ${online} up / ${offline} down`;

    } catch (error) {
        console.error("Ping failed:", error);
        btn.textContent = "✗ Ping failed";
    }

    setTimeout(() => {
        btn.disabled = false;
        btn.textContent = original;
    }, 2500);
}