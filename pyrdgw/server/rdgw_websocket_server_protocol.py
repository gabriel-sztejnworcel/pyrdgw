import websockets
import asyncio
import logging

from websockets import InvalidMessage
from websockets.legacy.http import d, read_headers, read_line
from pyrdgw.log_messages import *

class RDGWWebSocketServerProtocol(websockets.WebSocketServerProtocol):

    def __init__(self, *args, **kwargs):
        self.rdg_connection_id = ''
        self.rdg_correlation_id = ''
        self.rdg_user_id = ''
        self.logger = logging.getLogger('pyrdgw')
        super().__init__(*args, **kwargs)

    '''
    This function overrides websockets' read_http_request to allow the websocket request to succeed, since
    RDGW uses RDG_OUT_DATA HTTP method in the websocket upgrade request, instead of the standard GET method.
    '''
    async def read_http_request(self):
        stream = self.reader
        try:
            try:
                request_line = await read_line(stream)

            except EOFError as exc:
                raise EOFError("connection closed while reading HTTP request line") from exc

            try:
                method, raw_path, version = request_line.split(b" ", 2)

            except ValueError:  # not enough values to unpack (expected 3, got 1-2)
                raise ValueError(f"invalid HTTP request line: {d(request_line)}") from None

            if method != b"RDG_OUT_DATA":
                raise ValueError(f"unsupported HTTP method: {d(method)}")

            if version != b"HTTP/1.1":
                raise ValueError(f"unsupported HTTP version: {d(version)}")

            path = raw_path.decode("ascii", "surrogateescape")

            headers = await read_headers(stream)

        except asyncio.CancelledError:  # pragma: no cover
            raise

        except Exception as exc:
            raise InvalidMessage("did not receive a valid HTTP request") from exc

        if self.debug:
            self.logger.debug("< RDG_OUT_DATA %s HTTP/1.1", path)
            for key, value in headers.raw_items():
                self.logger.debug("< %s: %s", key, value)

        self.path = path
        self.request_headers = headers

        return path, headers


    def process_request(self, path, request_headers):
        if 'RDG-Connection-Id' in request_headers:
            self.rdg_connection_id = request_headers['RDG-Connection-Id']

        if 'RDG-Correlation-Id' in request_headers:
            self.rdg_correlation_id = request_headers['RDG-Correlation-Id']

        if 'RDG-User-Id' in request_headers:
            self.rdg_user_id = request_headers['RDG-User-Id']

        msg = self.rdg_correlation_id + ' - ' + LogMessages.WEBSOCKET_RECEIVED_CONNECTION_REQUEST
        self.logger.info(msg)

        return None