
import asyncio
import ssl
import websockets
import logging

from pyrdgw.protocol.state_machine import *
from pyrdgw.server.rdgw_websocket_server_protocol import *


class RDGWServer:

    def __init__(self, host, port, cert_path, key_path, authentication_handler=None, authorization_handler=None):
        self.host = host
        self.port = port
        self.cert_path = cert_path
        self.key_path = key_path
        self.authentication_handler = authentication_handler
        self.authorization_handler = authorization_handler
        self.logger = logging.getLogger('pyrdgw')

    
    async def websocket_handler(self, websocket, path):
        state_machine = ProtocolStateMachine(websocket, self.authentication_handler, self.authorization_handler)
        await state_machine.run()

    
    def run(self):
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(self.cert_path, self.key_path)

        start_server = websockets.serve(
            self.websocket_handler, self.host, self.port, ssl=ssl_context, create_protocol=RDGWWebSocketServerProtocol)

        asyncio.get_event_loop().run_until_complete(start_server)

        msg = LogMessages.WEBSOCKET_SERVER_LISTENING.format(self.host, self.port)
        self.logger.info(msg)