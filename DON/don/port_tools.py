import socket
from don.config import PORT_TIMEOUT_SECONDS


def test_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(PORT_TIMEOUT_SECONDS)

    try:
        return sock.connect_ex((ip, port)) == 0
    except Exception:
        return False
    finally:
        sock.close()


def scan_ports(ip, ports):
    open_ports = []

    for port in ports:
        if test_port(ip, port):
            open_ports.append(port)

    return open_ports
