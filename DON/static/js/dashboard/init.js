function startAutoRefresh() {
    if (refreshTimer) {
        clearInterval(refreshTimer);
    }

    refreshTimer = setInterval(requestLiveInfo, 30000);
}

updateClock();
setInterval(updateClock, 1000);
startAutoRefresh();

