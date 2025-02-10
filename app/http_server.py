from flask import Flask, jsonify, request
from ocpp.v16 import call
from app.websocket_server import chargers
from app.charge_point import ChargePoint
import asyncio


app = Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
    """HTTP endpoint to check server status."""
    return jsonify({"status": "ok", "message": "Server is running"}), 200

@app.route('/send-command', methods=['POST'])
def send_command():
    """Send a command to connected WebSocket clients."""
    data = request.json
    command = data.get("command", "")
    # Here you can integrate with WebSocket logic to broadcast the command
    # Example: Use a shared queue or directly send the command to clients
    return jsonify({"status": "command_sent", "command": command}), 200

@app.route('/clear-charging-profile', methods=['POST'])
async def clear_charging_profile():
    """Clearing charging profile for a connector"""
    data = request.json
    print(data, len(chargers))
    # global chargers
    cp = chargers[0]
    #cp = ChargePoint('cid', chargers[0])
    print(cp)
    await cp.clear_charging_profile(data["connector_id"])
    return jsonify({"status": "ok", "message": "Request sent successfully"}), 200

def create_http_server():
    """Return the configured Flask app."""
    return app
