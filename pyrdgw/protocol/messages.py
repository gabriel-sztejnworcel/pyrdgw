
from pyrdgw.protocol.enumerations import *

from typing import List


class HandshakeRequest:

    '''
    Type ID: PKT_TYPE_HANDSHAKE_REQUEST
    Packet: PKT_TYPE_HANDSHAKE_REQUEST
    '''

    def __init__(self, ver_major: int, ver_minor: int, extended_auth: HttpExtendedAuth):
        self.ver_major = ver_major
        self.ver_minor = ver_minor
        self.extended_auth = extended_auth


class HandshakeResponse:

    '''
    Type ID: PKT_TYPE_HANDSHAKE_RESPONSE
    Packet: HTTP_HANDSHAKE_RESPONSE_PACKET
    '''

    def __init__(self, error_code: int, ver_major: int, ver_minor: int, extended_auth: HttpExtendedAuth):
        self.error_code = error_code
        self.ver_major = ver_major
        self.ver_minor = ver_minor
        self.extended_auth = extended_auth


class TunnelCreate:
    
    '''
    Type ID: PKT_TYPE_TUNNEL_CREATE
    Packet: HTTP_TUNNEL_PACKET + HTTP_TUNNEL_PACKET_OPTIONAL
    '''

    def __init__(
        self,
        caps_flags: HttpCapabilityType,
        fields_present: HttpTunnelPacketFieldsPresentFlags,
        paa_cookie: bytes):

        self.caps_flags = caps_flags
        self.fields_present = fields_present
        self.paa_cookie = paa_cookie


class TunnelResponse:

    '''
    Type ID: PKT_TYPE_TUNNEL_RESPONSE
    Packet: HTTP_TUNNEL_RESPONSE + HTTP_TUNNEL_RESPONSE_OPTIONAL
    '''

    def __init__(
        self,
        server_version: int,
        status_code: int,
        fields_present: HttpTunnelResponseFieldsPresentFlags,
        tunnel_id: int,
        caps_flags: HttpCapabilityType):

        self.server_version = server_version
        self.status_code = status_code
        self.fields_present = fields_present
        self.tunnel_id = tunnel_id
        self.caps_flags = caps_flags


class TunnelAuthorize:

    '''
    Type ID: PKT_TYPE_TUNNEL_AUTH
    Packet: HTTP_TUNNEL_AUTH_PACKET + HTTP_TUNNEL_AUTH_PACKET_OPTIONAL
    '''

    def __init__(self, fields_present: HttpTunnelAuthFieldsPresentFlags, client_name: str):
        self.fields_present = fields_present
        self.client_name = client_name


class TunnelAuthorizeResponse:

    '''
    Type ID: PKT_TYPE_TUNNEL_AUTH_RESPONSE
    Packet: HTTP_TUNNEL_AUTH_RESPONSE + HTTP_TUNNEL_AUTH_RESPONSE_OPTIONAL
    '''

    def __init__(
        self,
        error_code: int,
        fields_present: HttpTunnelAuthResponseFieldsPresentFlags,
        redir_flags: HttpTunnelRedirFlags,
        idle_timeout: int):

        self.error_code = error_code
        self.fields_present = fields_present
        self.redir_flags = redir_flags
        self.idle_timeout = idle_timeout


class ChannelCreate:

    '''
    Type ID: PKT_TYPE_CHANNEL_CREATE
    Packet: HTTP_CHANNEL_PACKET + HTTP_CHANNEL_PACKET_VARIABLE
    '''

    def __init__(
        self,
        num_resources: int,
        num_alt_resources: int,
        port: int,
        resources: List[str],
        alt_resources: List[str]):

        self.num_resources = num_resources
        self.num_alt_resources = num_alt_resources
        self.port = port
        self.resources = resources
        self.alt_resources = alt_resources


class ChannelResponse:

    '''
    Type ID: PKT_TYPE_CHANNEL_RESPONSE
    Packet: HTTP_CHANNEL_RESPONSE + HTTP_CHANNEL_RESPONSE_OPTIONAL
    '''

    def __init__(
        self,
        error_code: int,
        fields_present: HttpChannelResponseFieldsPresentFlags,
        channel_id: int):

        self.error_code = error_code
        self.fields_present = fields_present
        self.channel_id = channel_id


class ClosePacket:

    '''
    Type ID: PKT_TYPE_CLOSE_CHANNEL
    Packet: HTTP_CLOSE_PACKET
    '''

    def __init__(self, status_code: int):
        self.status_code = status_code


class CloseResponsePacket:

    '''
    Type ID: PKT_TYPE_CLOSE_CHANNEL_RESPONSE
    Packet: HTTP_CLOSE_PACKET
    '''
    
    def __init__(self, status_code: int):
        self.status_code = status_code


class DataPacket:

    '''
    Type ID: PKT_TYPE_DATA
    Packet: HTTP_DATA_PACKET
    '''

    def __init__(self, data: bytes):
        self.data = data
