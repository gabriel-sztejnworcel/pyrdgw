import logging
import asyncio

from pyrdgw.server.rdgw_server import RDGWServer

def authentication_handler(server_session_id, paa_cookie):
    print('server_session_id:', str(server_session_id))
    print('paa_cookie:', paa_cookie.decode('utf-16'))
    return True

def authorization_handler(server_session_id, resources, port):
    print('server_session_id:', str(server_session_id))
    print('resources:', resources)
    print('port:', port)
    return True

try:
    server = RDGWServer(host='localhost',
                        port=443,
                        cert_path='d:/certs/gabriel.com.crt',
                        key_path='d:/certs/gabriel.com.key',
                        authentication_handler=authentication_handler,
                        authorization_handler=authorization_handler)
    server.run()
    loop = asyncio.get_event_loop()
    loop.run_forever()

except Exception as ex:
    logger = logging.getLogger('pyrdgw')
    logger.error(ex)