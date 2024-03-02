# PyRDGW
Remote Desktop Gateway protocol [[MS-TSGU]](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-tsgu) server-side implementation in Python 3.

### What is Remote Desktop Gateway?
Remote Desktop Gateway provides an RDP (Remote Desktop Protocol) connection over a secure HTTPS tunnel. The main use case is to allow users to connect from the internet to servers inside a private network without the need for a VPN.

### Current Limitations
- Only WebSocket transport is supported so only clients that support it should work (MSTSC on Windows 10 and Windows Server 2016 and above should work).
- The only supported authentication method is PAA, clients need to provide an access token which will be passed to the authentication handler callback to perform the authentication.

### Building and Installing
```
python setup.py bdist_wheel
python -m pip install path/to/whl/file
```

### Running
Example code for running the server:
```
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
                        cert_path='cert.pem',
                        key_path='key.pem',
                        authentication_handler=authentication_handler,
                        authorization_handler=authorization_handler)
    server.run()
    loop = asyncio.get_event_loop()
    loop.run_forever()

except Exception as ex:
    logger = logging.getLogger('pyrdgw')
    logger.error(ex)
```
- A certificate and the matching private key must be provided.
- The user can pass callbacks for authentication and authorization. The access token (PAA cookie) from the client is passed to the authentication handler together with a session id which can be used to store any required state for the authorization handler, which is called later to decide if the client is allowed to connect to the requested resource.

### On the Client Machine
- The CA certificate must be trusted by the client, and the RDGW hostname should resolvable by the client and match the certificate.
- The client must provide an access token, this can be done by using an RDP file with 'gatewayaccesstoken', like the example below.
```
full address:s:192.168.0.101
gatewaycredentialssource:i:5
gatewayaccesstoken:s:ACCESSTOKEN123
gatewayhostname:s:pyrdgw.com
gatewayprofileusagemethod:i:1
gatewayusagemethod:i:1
server port:i:3389
```