import logging
import asyncio

from pyrdgw.server.rdgw_websocket_server import RDGWWebSocketServer

def auth_handler(paa_cookie):
    print('Token:', paa_cookie.decode('utf-16'))
    return True

try:
    websocket_server = RDGWWebSocketServer(host='localhost',
                                           port=443,
                                           cert_path='d:/certs/gabriel.com.crt',
                                           key_path='d:/certs/gabriel.com.key',
                                           auth_handler=auth_handler)
    
    websocket_server.run()
    loop = asyncio.get_event_loop()
    loop.run_forever()

except Exception as ex:
    logger = logging.getLogger('pyrdgw')
    logger.error(ex)