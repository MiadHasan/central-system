import logging
import websockets
from app.charge_point import ChargePoint

logging.basicConfig(level=logging.INFO)
chargers = []

async def on_connect(websocket, path):
    """Handle new WebSocket connections."""
    try:
        requested_protocols = websocket.request_headers["Sec-WebSocket-Protocol"]
    except KeyError:
        logging.error("Client hasn't requested any Subprotocol. Closing connection.")
        return await websocket.close()

    if websocket.subprotocol:
        logging.info("Protocols Matched: %s", websocket.subprotocol)
    else:
        logging.warning(
            "Protocols Mismatched | Expected Subprotocols: %s,"
            " but client supports %s | Closing connection",
            websocket.available_subprotocols,
            requested_protocols,
        )
        return await websocket.close()

    charge_point_id = path.strip("/")
    charge_point = ChargePoint(charge_point_id, websocket)
    global chargers
    chargers.append(charge_point)

    logging.info("New ChargePoint connected: %s", charge_point_id)

    #await charge_point.clear_charging_profile(2)
    await charge_point.start()

async def start_server(host: str, port: int, protocols: list):
    """Start the WebSocket server."""
    server = await websockets.serve(
        on_connect, host, port, subprotocols=protocols
    )
    logging.info("WebSocket server started on ws://%s:%d", host, port)
    await server.wait_closed()
