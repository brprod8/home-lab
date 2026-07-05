import subprocess


def get_mac(ip):
    try:
        output = subprocess.check_output("arp -a", shell=True).decode(errors="ignore")

        for line in output.splitlines():
            if ip in line:
                parts = line.split()

                if len(parts) >= 2:
                    return parts[1]

    except Exception:
        pass

    return "Unknown"
