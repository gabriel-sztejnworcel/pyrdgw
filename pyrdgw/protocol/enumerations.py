import enum

class ProtocolState(enum.IntEnum):
    INITIAL = 0
    RECEIVING_HANDSHAKE_REQUEST = 1
    RECEIVING_TUNNEL_CREATE = 2
    RECEIVING_TUNNEL_AUTHORIZE = 3
    RECEIVING_CHANNEL_CREATE = 4
    DATA_TRANSFER = 5


class HttpPacketType(enum.IntEnum):
    PKT_TYPE_HANDSHAKE_REQUEST = 0x1
    PKT_TYPE_HANDSHAKE_RESPONSE = 0x2
    PKT_TYPE_EXTENDED_AUTH_MSG = 0x3
    PKT_TYPE_TUNNEL_CREATE = 0x4
    PKT_TYPE_TUNNEL_RESPONSE = 0x5
    PKT_TYPE_TUNNEL_AUTH = 0x6
    PKT_TYPE_TUNNEL_AUTH_RESPONSE = 0x7
    PKT_TYPE_CHANNEL_CREATE = 0x8
    PKT_TYPE_CHANNEL_RESPONSE = 0x9
    PKT_TYPE_DATA = 0xA
    PKT_TYPE_SERVICE_MESSAGE = 0xB
    PKT_TYPE_REAUTH_MESSAGE = 0xC
    PKT_TYPE_KEEPALIVE = 0xD
    PKT_TYPE_CLOSE_CHANNEL = 0x10
    PKT_TYPE_CLOSE_CHANNEL_RESPONSE = 0x11


class HttpExtendedAuth:
    HTTP_EXTENDED_AUTH_NONE = 0x00
    HTTP_EXTENDED_AUTH_SC = 0x01
    HTTP_EXTENDED_AUTH_PAA = 0x02
    HTTP_EXTENDED_AUTH_SSPI_NTLM = 0x04


class HttpCapabilityType:
    HTTP_CAPABILITY_TYPE_QUAR_SOH = 0x1
    HTTP_CAPABILITY_IDLE_TIMEOUT = 0x2
    HTTP_CAPABILITY_MESSAGING_CONSENT_SIGN = 0x4
    HTTP_CAPABILITY_MESSAGING_SERVICE_MSG = 0x8
    HTTP_CAPABILITY_REAUTH = 0x10
    HTTP_CAPABILITY_UDP_TRANSPORT = 0x20


class HttpTunnelPacketFieldsPresentFlags:
    HTTP_TUNNEL_PACKET_FIELD_PAA_COOKIE = 0x1


class HttpTunnelResponseFieldsPresentFlags:
    HTTP_TUNNEL_RESPONSE_FIELD_TUNNEL_ID = 0x1
    HTTP_TUNNEL_RESPONSE_FIELD_CAPS = 0x2
    HTTP_TUNNEL_RESPONSE_FIELD_SOH_REQ = 0x4
    HTTP_TUNNEL_RESPONSE_FIELD_CONSENT_MSG = 0x10


class HttpTunnelAuthFieldsPresentFlags:
    HTTP_TUNNEL_AUTH_FIELD_SOH = 0x1


class HttpTunnelAuthResponseFieldsPresentFlags:
    HTTP_TUNNEL_AUTH_RESPONSE_FIELD_REDIR_FLAGS = 0x1
    HTTP_TUNNEL_AUTH_RESPONSE_FIELD_IDLE_TIMEOUT = 0x2
    HTTP_TUNNEL_AUTH_RESPONSE_FIELD_SOH_RESPONSE = 0x4


class HttpTunnelRedirFlags:
    HTTP_TUNNEL_REDIR_ENABLE_ALL = 0x80000000
    HTTP_TUNNEL_REDIR_DISABLE_ALL = 0x40000000
    HTTP_TUNNEL_REDIR_DISABLE_DRIVE = 0x1
    HTTP_TUNNEL_REDIR_DISABLE_PRINTER = 0x2
    HTTP_TUNNEL_REDIR_DISABLE_PORT = 0x4
    HTTP_TUNNEL_REDIR_DISABLE_CLIPBOARD = 0x8
    HTTP_TUNNEL_REDIR_DISABLE_PNP = 0x10


class HttpChannelResponseFieldsPresentFlags:
    HTTP_CHANNEL_RESPONSE_FIELD_CHANNELID = 0x1
    HTTP_CHANNEL_RESPONSE_FIELD_AUTHNCOOKIE = 0x2
    HTTP_CHANNEL_RESPONSE_FIELD_UDPPORT = 0x4


class ReturnCode:
    ERROR_SUCCESS = 0x00000000
    ERROR_ACCESS_DENIED = 0x00000005
    E_PROXY_INTERNALERROR = 0x800759D8


class ProtocolVersion:
    VER_MAJOR = 1
    VER_MINOR = 0
    SERVER_VERSION = 1