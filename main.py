import asyncio
import logging
from threading import Thread
from app.websocket_server import start_server
from app.http_server import create_http_server
from config.settings import Config

logging.basicConfig(level=logging.INFO)

def run_http_server():
    """Run the HTTP server in a separate thread."""
    app = create_http_server()
    app.run(host=Config.HTTP_HOST, port=Config.HTTP_PORT)

async def main():
    """Run WebSocket server and start the HTTP server."""
    # Start HTTP server in a separate thread
    http_thread = Thread(target=run_http_server)
    http_thread.start()

    # Start WebSocket server
    await start_server(Config.WS_HOST, Config.WS_PORT, Config.PROTOCOLS)

if __name__ == "__main__":
    asyncio.run(main())
