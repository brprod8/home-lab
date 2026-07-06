function updateClock() {
    const clock = document.getElementById("clock");
    if (clock) {
        clock.textContent = new Date().toLocaleTimeString();
    }
}

