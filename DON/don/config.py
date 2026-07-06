from don.network_utils import get_active_host_ip, derive_subnet

HOST_IP = get_active_host_ip()
SUBNET = derive_subnet(HOST_IP)

PORT = 5000
COMMON_PORTS = [
    21, 22, 23, 53, 80, 443, 445,
    554, 8060, 8080, 8443, 9000, 3389
]

PING_TIMEOUT_MS = "700"
PORT_TIMEOUT_SECONDS = 0.3
MAX_WORKERS = 50
