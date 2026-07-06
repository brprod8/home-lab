import subprocess
import socket
import platform
from datetime import datetime

subnet = "192.168.86"  # change if needed

print("DON Network Ping Report")
print("=" * 40)
print("Computer:", socket.gethostname())
print("OS:", platform.system(), platform.release())
print("Started:", datetime.now())
print("=" * 40)
print()

online_devices = []

for host in range(1, 255):
    ip = f"{subnet}.{host}"

    result = subprocess.run(
        ["ping", "-n", "1", "-w", "300", ip],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    if result.returncode == 0:
        online_devices.append(ip)
        print(f"[ONLINE] {ip}")

print()
print("=" * 40)
print("Scan complete")
print("Total online devices:", len(online_devices))
print("Finished:", datetime.now())
print("=" * 40)