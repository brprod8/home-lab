import subprocess
from don.config import PING_TIMEOUT_MS


def ping(ip):
    result = subprocess.run(
        ["ping", "-n", "1", "-w", PING_TIMEOUT_MS, ip],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )

    return result.returncode == 0, result.stdout


def get_latency(ping_output):
    for line in ping_output.splitlines():
        if "time=" in line:
            try:
                part = line.split("time=")[1]
                return part.split("ms")[0].strip() + "ms"
            except Exception:
                return "Unknown"

        if "time<" in line:
            return "<1ms"

    return "Unknown"
