from hpe_api import get_hpe_devices

# LOCAL DEVICES
DEVICES = [
    {"name": "R1", "ip": "192.168.20.1", "type": "Router"},
    {"name": "SW1", "ip": "192.168.10.12", "type": "Switch"},
]

def check_device(device):
    return {
        "name": device["name"],
        "ip": device["ip"],
        "type": device["type"],
        "status": "UP"   # replace with ping logic if needed
    }

def get_local_devices():
    return [check_device(d) for d in DEVICES]

# COMBINED DATA
def get_all_devices():
    return {
        "local": get_local_devices(),
        "hpe": get_hpe_devices()
    }