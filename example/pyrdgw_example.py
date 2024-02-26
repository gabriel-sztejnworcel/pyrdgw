import logging
import asyncio

from pyrdgw.server.rdgw_websocket_server import RDGWWebSocketServer

def authn_handler(rdg_connection_id, rdg_correlation_id, rdg_user_id, paa_cookie):
    print('rdg_connection_id:', rdg_connection_id)
    print('rdg_correlation_id:', rdg_correlation_id)
    print('rdg_user_id:', rdg_user_id)
    print('paa_cookie:', paa_cookie.decode('utf-16'))
    return True

def authz_handler(rdg_connection_id, rdg_correlation_id, rdg_user_id, resources, port):
    print('rdg_connection_id:', rdg_connection_id)
    print('rdg_correlation_id:', rdg_correlation_id)
    print('rdg_user_id:', rdg_user_id)
    print('resources:', resources)
    print('port:', port)
    return True

try:
    websocket_server = RDGWWebSocketServer(host='localhost',
                                           port=443,
                                           cert_path='d:/certs/gabriel.com.crt',
                                           key_path='d:/certs/gabriel.com.key',
                                           authn_handler=authn_handler,
                                           authz_handler=authz_handler)
    websocket_server.run()
    loop = asyncio.get_event_loop()
    loop.run_forever()

except Exception as ex:
    logger = logging.getLogger('pyrdgw')
    logger.error(ex)