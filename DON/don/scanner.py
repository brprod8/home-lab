from concurrent.futures import ThreadPoolExecutor

from don.config import COMMON_PORTS, MAX_WORKERS
from don.ping_tools import ping, get_latency
from don.arp_tools import get_mac
from don.dns_tools import get_hostname
from don.port_tools import scan_ports
from don.intelligence import classify_device, add_device_intelligence
from don.health import add_network_health


def scan_device(ip):
    online, output = ping(ip)

    if not online:
        return None

    latency = get_latency(output)
    mac = get_mac(ip)
    hostname = get_hostname(ip)
    open_ports = scan_ports(ip, COMMON_PORTS)

    device_type = classify_device(open_ports)
    services, capabilities = add_device_intelligence(open_ports)
    health, packet_loss, health_latency = add_network_health(ip)

    return {
        "ip": ip,
        "hostname": hostname,
        "mac": mac,
        "status": "Online",
        "latency": latency,
        "health": health,
        "packet_loss": packet_loss,
        "health_latency": health_latency,
        "ports": open_ports,
        "services": services,
        "capabilities": capabilities,
        "type": device_type
    }


def scan_network(subnet):
    ips = [f"{subnet}.{i}" for i in range(1, 255)]
    devices = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        results = executor.map(scan_device, ips)

    for result in results:
        if result:
            devices.append(result)

    return devices
