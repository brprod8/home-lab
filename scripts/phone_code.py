import subprocess

subnet = "192.168.86"

print(f"Scanning {subnet}.0/24...\n")

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

print("\nScan complete.")
print(f"Total online devices: {len(online_devices)}")

print("\nDevices Found:")
for ip in online_devices:
    print(ip)