
import asyncio
import pathlib
import ssl
import websockets
import logging

from email.parser import BytesParser

from pyrdgw.log_messages import *


class GWServer:

    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger('pyrdgw')


    async def __gw_forward_data(self, reader, writer):

        try:
            while True:
                buf = await reader.read(65536)
                writer.write(buf)
                await writer.drain()

        except Exception as ex:
            logging.error(f"Exception while forwarding data: {ex}")


    async def __gw_handler(self, server_reader, server_writer):

        recv_buf = await server_reader.read(10240)
        request_line, headers_alone = recv_buf.split(b'\r\n', 1)
        method = request_line.split(b" ")[0]
        headers = BytesParser().parsebytes(headers_alone)

        if (method == b'RDG_OUT_DATA' and
                headers.get('CONNECTION') == 'Upgrade' and
                headers.get('UPGRADE') == 'websocket'):

            websocket_hostname = self.config['websocket_server']['hostname']
            websocket_port = self.config['websocket_server']['port']
            websocket_ca_path = self.config['websocket_server']['ca_path']

            ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ssl_ctx.load_verify_locations(cafile=websocket_ca_path)
            ssl_ctx.check_hostname = True
            ssl_ctx.verify_mode = ssl.VerifyMode.CERT_REQUIRED

            client_reader, client_writer = await asyncio.open_connection(
                websocket_hostname, websocket_port, ssl=ssl_ctx)

            start_index = len(b'RDG_OUT_DATA')
            send_buf = b'GET' + recv_buf[start_index:]
            client_writer.write(send_buf)
            await client_writer.drain()

            client_to_server_task = asyncio.ensure_future(self.__gw_forward_data(client_reader, server_writer))
            server_to_client_task = asyncio.ensure_future(self.__gw_forward_data(server_reader, client_writer))

            done, pending = await asyncio.wait(
                [client_to_server_task, server_to_client_task],
                return_when=asyncio.FIRST_COMPLETED)

            for task in pending:
                task.cancel()

        else:
            self.logger.error(LogMessages.GW_ATTEMPT_NON_WEBSOCKET)


    def run(self):

        hostname = self.config['gw_server']['hostname']
        port = self.config['gw_server']['port']
        cert_path = self.config['gw_server']['cert_path']
        key_path = self.config['gw_server']['key_path']
        
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(cert_path, keyfile=key_path)

        loop = asyncio.get_event_loop()

        coroutine = asyncio.start_server(
            self.__gw_handler, hostname, port, ssl=ssl_context)

        server = loop.run_until_complete(coroutine)

        msg = LogMessages.GW_SERVER_LISTENING.format(hostname, port)
        self.logger.info(msg)
