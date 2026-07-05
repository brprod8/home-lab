import subprocess


def get_hostname(ip):
    try:
        output = subprocess.check_output(
            ["nslookup", ip],
            stderr=subprocess.DEVNULL
        ).decode(errors="ignore")

        for line in output.splitlines():
            if line.strip().startswith("Name:"):
                return line.split("Name:")[1].strip()

    except Exception:
        pass

    return "Unknown"
