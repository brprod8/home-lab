function updateGraph(devices) {
    const healthy = devices.filter(d => d.health === "Healthy").length;
    const total = devices.length || 1;
    const offline = total - healthy;
    const healthPercent = healthy / total;

    const baseY = 220 - (healthPercent * 120);
    const latencyPoints = [
        `0,${baseY + 20}`,
        `100,${baseY + 5}`,
        `200,${baseY + 18}`,
        `300,${baseY - 10}`,
        `400,${baseY + 12}`,
        `500,${baseY}`,
        `600,${baseY + 16}`,
        `700,${baseY - 4}`,
        `800,${baseY + 8}`
    ].join(" ");

    const lossY = 240 - (offline * 12);
    const lossPoints = [
        `0,240`,
        `100,${lossY}`,
        `200,240`,
        `300,${lossY}`,
        `400,238`,
        `500,${lossY}`,
        `600,240`,
        `700,${lossY}`,
        `800,238`
    ].join(" ");

    document.getElementById("latencyLine").setAttribute("points", latencyPoints);
    document.getElementById("lossLine").setAttribute("points", lossPoints);
}

