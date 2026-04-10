import time
import threading
from waitress import serve
from flask import Flask, jsonify
from flask_cors import CORS
CORS(app)

from pysnmp.hlapi import *

# ---------------- CONFIG ----------------
CHECK_INTERVAL = 10
SNMP_COMMUNITY = "public"

DEVICES = [
    {"name": "R1", "ip": "192.168.20.1", "type": "Router"},
    {"name": "SW1", "ip": "192.168.10.12", "type": "Switch"},
    {"name": "FW1", "ip": "192.168.10.10", "type": "Firewall"},
    {"name": "SRV1", "ip": "192.168.20.166", "type": "Server"},
]

# ---------------- STORAGE ----------------
device_data = []
alerts = []

# ---------------- FLASK APP ----------------
app = Flask(__name__)
CORS(app)

# ---------------- SNMP FUNCTION ----------------
def snmp_get(ip, oid):
    try:
        iterator = getCmd(
            SnmpEngine(),
            CommunityData(SNMP_COMMUNITY, mpModel=0),
            UdpTransportTarget((ip, 161), timeout=2, retries=1),
            ContextData(),
            ObjectType(ObjectIdentity(oid))
        )

        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

        if errorIndication or errorStatus:
            return None

        for varBind in varBinds:
            return str(varBind[1])

    except Exception:
        return None


# ---------------- DEVICE CHECK ----------------
def check_device(device):
    ip = device["ip"]

    # SNMP OIDs
    SYS_NAME_OID = "1.3.6.1.2.1.1.5.0"
    UPTIME_OID = "1.3.6.1.2.1.1.3.0"

    sys_name = snmp_get(ip, SYS_NAME_OID)
    uptime = snmp_get(ip, UPTIME_OID)

    if sys_name:
        status = "UP"
        severity = 0
        message = "SNMP OK"
    else:
        status = "DOWN"
        severity = 3
        message = "SNMP timeout / unreachable"

    return {
        "name": device["name"],
        "ip": ip,
        "type": device["type"],
        "status": status,
        "severity": severity,
        "message": message,
        "sys_name": sys_name,
        "uptime": uptime,
        "time": time.ctime()
    }


# ---------------- MONITOR LOOP ----------------
def monitor():
    global device_data

    while True:
        device_data = [check_device(d) for d in DEVICES]
        time.sleep(CHECK_INTERVAL)


# ---------------- API ROUTES ----------------
@app.route("/")
def home():
    return {"status": "SNMP Monitoring System Running"}

@app.route("/devices")
def get_devices():
    return jsonify(device_data)

@app.route("/alerts")
def get_alerts():
    return jsonify(alerts)

@app.route("/health")
def health():
    return {"status": "healthy"}


# ---------------- START SYSTEM ----------------
if __name__ == "__main__":
    print("Starting SNMP Monitoring System...")

    thread = threading.Thread(target=monitor, daemon=True)
    thread.start()

    serve(app, host="0.0.0.0", port=5000)