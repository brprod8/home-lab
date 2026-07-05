PORT_INTELLIGENCE = {
    21: ("FTP", "File transfer"),
    22: ("SSH", "Remote Linux/server access; SCP; SFTP"),
    23: ("Telnet", "Insecure remote access"),
    53: ("DNS", "Name resolution"),
    80: ("HTTP", "Web interface"),
    443: ("HTTPS", "Secure web interface"),
    445: ("SMB", "Windows file sharing"),
    554: ("RTSP", "Camera/video stream"),
    8060: ("Roku ECP", "Roku remote control API"),
    8080: ("HTTP Alternate", "Alternate web interface"),
    8443: ("HTTPS Alternate", "Secure alternate web interface"),
    9000: ("App Service", "Possible custom app/service"),
    3389: ("RDP", "Windows Remote Desktop")
}


def classify_device(open_ports):
    if 8060 in open_ports:
        return "Roku"
    if 554 in open_ports:
        return "Camera/RTSP"
    if 22 in open_ports:
        return "Linux/SSH Server"
    if 3389 in open_ports:
        return "Windows/RDP"
    if 445 in open_ports:
        return "Windows/File Server"
    if 80 in open_ports or 443 in open_ports:
        return "Web Device"

    return "Unknown"


def add_device_intelligence(open_ports):
    services = []
    capabilities = []

    for port in open_ports:
        if port in PORT_INTELLIGENCE:
            service, capability = PORT_INTELLIGENCE[port]
            services.append(f"{port}:{service}")
            capabilities.append(capability)

    if not services:
        return "No open known services", "Ping only / no local service found"

    return "; ".join(services), "; ".join(capabilities)
