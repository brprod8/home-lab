import socket

def get_active_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def derive_subnet(host_ip):
    parts = host_ip.split(".")
    return f"{parts[0]}.{parts[1]}.{parts[2]}"


