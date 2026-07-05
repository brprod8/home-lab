"""
actions.py

DON - Device Actions Module

This file contains reusable action functions.
action_probe.py uses some of these functions to check what a device is compatible with.

Current supported action types:
- Generic network actions
- Roku actions
- Local desktop health actions
"""

import socket
import subprocess





try:
    import requests
except ImportError:
    requests = None

try:
    import psutil
except ImportError:
    psutil = None



# ======================================================
# GENERIC NETWORK ACTIONS
# ======================================================

def ping_device(ip):
    """
    Ping a device and return the raw ping output.
    """
    result = subprocess.run(
        ["ping", "-n", "4", ip],
        capture_output=True,
        text=True
    )

    return result.stdout


def test_port(ip, port, timeout=1):
    """
    Test whether a TCP port is open.
    Returns True or False.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        return sock.connect_ex((ip, int(port))) == 0
    except Exception:
        return False
    finally:
        sock.close()


# ======================================================
# LOCAL DESKTOP ACTIONS
# ======================================================

def get_desktop_health():
    """
    Returns CPU, RAM, and Disk usage for the computer running DON.
    This does not check remote computers.
    """
    if psutil is None:
        return {
            "error": "psutil is not installed. Run: pip install psutil"
        }

    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return {
        "CPU %": cpu,
        "RAM %": ram.percent,
        "RAM Used GB": round(ram.used / (1024 ** 3), 2),
        "RAM Total GB": round(ram.total / (1024 ** 3), 2),
        "Disk %": disk.percent,
        "Disk Used GB": round(disk.used / (1024 ** 3), 2),
        "Disk Total GB": round(disk.total / (1024 ** 3), 2),
    }


# ======================================================
# ROKU ACTIONS
# ======================================================

def roku_press(ip, button):
    """
    Send a Roku remote button press.
    Example buttons:
    Home, Back, Select, Up, Down, Left, Right,
    VolumeUp, VolumeDown, VolumeMute, Play, Power
    """
    if requests is None:
        return {
            "success": False,
            "error": "requests is not installed. Run: pip install requests"
        }

    url = f"http://{ip}:8060/keypress/{button}"

    try:
        response = requests.post(url, timeout=3)

        return {
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "action": f"Roku {button}"
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error),
            "action": f"Roku {button}"
        }


def roku_home(ip):
    return roku_press(ip, "Home")


def roku_back(ip):
    return roku_press(ip, "Back")


def roku_select(ip):
    return roku_press(ip, "Select")


def roku_up(ip):
    return roku_press(ip, "Up")


def roku_down(ip):
    return roku_press(ip, "Down")


def roku_left(ip):
    return roku_press(ip, "Left")


def roku_right(ip):
    return roku_press(ip, "Right")


def roku_volume_up(ip):
    return roku_press(ip, "VolumeUp")


def roku_volume_down(ip):
    return roku_press(ip, "VolumeDown")


def roku_volume_mute(ip):
    return roku_press(ip, "VolumeMute")


def roku_play_pause(ip):
    return roku_press(ip, "Play")


def roku_power(ip):
    return roku_press(ip, "Power")


def roku_search(ip):
    return roku_press(ip, "Search")


def roku_info(ip):
    return roku_press(ip, "Info")


def roku_launch_app(ip, app_id):
    """
    Launch a Roku app by App ID.
    Example:
    YouTube is often 837, but use query/apps to confirm.
    """
    if requests is None:
        return {
            "success": False,
            "error": "requests is not installed. Run: pip install requests"
        }

    url = f"http://{ip}:8060/launch/{app_id}"

    try:
        response = requests.post(url, timeout=3)

        return {
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "action": f"Launch Roku App {app_id}"
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error),
            "action": f"Launch Roku App {app_id}"
        }


def roku_youtube(ip, youtube_app_id=837):
    return roku_launch_app(ip, youtube_app_id)


def roku_get_apps(ip):
    """
    Returns the Roku app list XML from /query/apps.
    """
    if requests is None:
        return {
            "success": False,
            "error": "requests is not installed. Run: pip install requests"
        }

    url = f"http://{ip}:8060/query/apps"

    try:
        response = requests.get(url, timeout=3)

        return {
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "content": response.text
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error)
        }

def roku_type_text(ip, text):
    if requests is None:
        return {"success": False, "error": "requests is not installed. Run: pip install requests"}

    import urllib.parse
    import time

    try:
        for char in text:
            encoded_char = urllib.parse.quote(char, safe="")
            url = f"http://{ip}:8060/keypress/Lit_{encoded_char}"
            response = requests.post(url, timeout=3)

            if response.status_code != 200:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "action": f"Typed text stopped at character: {char}"
                }

            time.sleep(0.05)

        return {
            "success": True,
            "status_code": 200,
            "action": f"Typed text: {text}"
        }

    except Exception as error:
        return {"success": False, "error": str(error)}

try:
    import psutil
except ImportError:
    psutil = None



# ======================================================
# FUTURE ACTION PLACEHOLDERS
# ======================================================

# Ubuntu Server Actions
# - SSH
# - CPU/RAM/Disk
# - Docker
# - Restart services

# File Server Actions
# - List files
# - Upload
# - Download
# - Storage health

# Camera Actions
# - RTSP stream check
# - Snapshot if supported
# - ONVIF later

# AI Server Actions
# - Submit prompt
# - Run model
# - Return response