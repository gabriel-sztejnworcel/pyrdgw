
import asyncio
import pathlib
import ssl
import websockets
import logging

from http_parser.pyparser import HttpParser

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

        except:
            pass


    async def __gw_handler(self, server_reader, server_writer):
        
        parser = HttpParser()

        recv_buf = await server_reader.read(65536)
        len_parsed = parser.execute(recv_buf, len(recv_buf))


        if len_parsed != len(recv_buf):
            raise Exception(LogMessages.GW_FAILED_PROCESS_HTTP_REQUEST)

        headers = parser.get_headers()

        if parser.get_method() == 'RDG_OUT_DATA' and \
            'CONNECTION' in headers and headers['CONNECTION'] == 'Upgrade' and \
            'UPGRADE' in headers and headers['UPGRADE'] == 'websocket':

            websocket_hostname = self.config['websocket_server']['hostname']
            websocket_port = self.config['websocket_server']['port']
            websocket_ca_path = self.config['websocket_server']['ca_path']

            ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ssl_ctx.load_verify_locations(cafile=websocket_ca_path)
            ssl_ctx.check_hostname = True
            ssl_ctx.verify_mode = ssl.VerifyMode.CERT_REQUIRED
            
            async_loop = asyncio.get_event_loop()

            client_reader, client_writer = await asyncio.open_connection(
                websocket_hostname, websocket_port, ssl=ssl_ctx, loop=async_loop)

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
            self.__gw_handler, hostname, port, ssl=ssl_context, loop=loop)

        server = loop.run_until_complete(coroutine)

        msg = LogMessages.GW_SERVER_LISTENING.format(hostname, port)
        self.logger.info(msg)
