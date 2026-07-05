import time
from don.ping_tools import ping, get_latency


def add_network_health(ip):
    success_count = 0
    latencies = []

    for _ in range(3):
        online, output = ping(ip)

        if online:
            success_count += 1
            latencies.append(get_latency(output))

        time.sleep(0.2)

    if success_count == 3:
        return "Healthy", "0% loss", ", ".join(latencies)
    elif success_count > 0:
        packet_loss = int(((3 - success_count) / 3) * 100)
        return "Unstable", f"{packet_loss}% loss", ", ".join(latencies)
    else:
        return "Offline", "100% loss", "N/A"
