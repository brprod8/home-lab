async function refreshHealth() {
    const response = await fetch("/desktop/health");
    const data = await response.json();

    const healthGrid = document.getElementById("healthGrid");
    healthGrid.innerHTML = "";

    for (const key in data) {
        const card = document.createElement("div");
        card.className = "metric";

        card.innerHTML = `
            <div class="metric-label">${key}</div>
            <div class="metric-value">${data[key]}</div>
        `;

        healthGrid.appendChild(card);
    }
}
