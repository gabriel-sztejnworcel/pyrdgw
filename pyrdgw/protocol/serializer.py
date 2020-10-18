
from pyrdgw.protocol.messages import *
from pyrdgw.util.streams import *


class ProtocolSerializer:

    def write_handshake_response(self, handshake_response: HandshakeResponse) -> bytes:
        
        '''
        HTTP_HANDSHAKE_RESPONSE_PACKET Structure:

        HTTP_PACKET_HEADER:
        packetType              - uint16 = PKT_TYPE_HANDSHAKE_RESPONSE
        reserved                - uint16
        packetLength            - uint32 = 18

        Body:
        errorCode               - uint32
        verMajor                - uint8
        verMinor                - uint8
        serverVersion           - uint16 = 0
        ExtendedAuth            - uint16
        '''

        stream = WritableStream()

        stream.write_uint16(HttpPacketType.PKT_TYPE_HANDSHAKE_RESPONSE)
        stream.write_uint16(0)
        stream.write_uint32(18)

        stream.write_uint32(handshake_response.error_code)
        stream.write_uint8(handshake_response.ver_major)
        stream.write_uint8(handshake_response.ver_minor)
        stream.write_uint16(0)
        stream.write_uint16(handshake_response.extended_auth)

        return stream.buf

    
    def write_tunnel_response(self, tunnel_response: TunnelResponse) -> bytes:
        
        '''
        HTTP_TUNNEL_RESPONSE Structure:

        HTTP_PACKET_HEADER:
        packetType              - uint16 = PKT_TYPE_TUNNEL_RESPONSE
        reserved                - uint16
        packetLength            - uint32 = 26

        Body:
        serverVersion           - uint16
        statusCode              - uint32
        fieldsPresent           - uint16
        reserved                - uint16

        HTTP_TUNNEL_RESPONSE_OPTIONAL:
        tunnelId                - uint32
        capsFlags               - uint32
        '''

        stream = WritableStream()

        stream.write_uint16(HttpPacketType.PKT_TYPE_TUNNEL_RESPONSE)
        stream.write_uint16(0)
        stream.write_uint32(26)

        stream.write_uint16(tunnel_response.server_version)
        stream.write_uint32(tunnel_response.status_code)
        stream.write_uint16(tunnel_response.fields_present)
        stream.write_uint16(0)

        stream.write_uint32(tunnel_response.tunnel_id)
        stream.write_uint32(tunnel_response.caps_flags)

        return stream.buf

    
    def write_tunnel_authorize_response(
        self, tunnel_authorize_response: TunnelAuthorizeResponse) -> bytes:

        '''
        HTTP_TUNNEL_AUTH_RESPONSE Structure:

        HTTP_PACKET_HEADER:
        packetType              - uint16 = PKT_TYPE_TUNNEL_AUTH_RESPONSE
        reserved                - uint16
        packetLength            - uint32 = 24

        Body:
        errorCode               - uint32
        fieldsPresent           - uint16
        reserved                - uint16

        HTTP_TUNNEL_AUTH_RESPONSE_OPTIONAL:
        redirFlags              - uint32
        idleTimeout             - uint32
        '''

        stream = WritableStream()

        stream.write_uint16(HttpPacketType.PKT_TYPE_TUNNEL_AUTH_RESPONSE)
        stream.write_uint16(0)
        stream.write_uint32(24)

        stream.write_uint32(tunnel_authorize_response.error_code)
        stream.write_uint16(tunnel_authorize_response.fields_present)
        stream.write_uint16(0)

        stream.write_uint32(tunnel_authorize_response.redir_flags)
        stream.write_uint32(tunnel_authorize_response.idle_timeout)

        return stream.buf


    def write_channel_response(self, channel_response: ChannelResponse) -> bytes:
        
        '''
        HTTP_CHANNEL_RESPONSE Structure:

        HTTP_PACKET_HEADER:
        packetType              - uint16 = PKT_TYPE_CHANNEL_RESPONSE
        reserved                - uint16
        packetLength            - uint32 = 20

        Body:
        errorCode               - uint32
        fieldsPresent           - uint16
        reserved                - uint16

        HTTP_CHANNEL_RESPONSE_OPTIONAL:
        channelId               - uint32
        '''

        stream = WritableStream()

        stream.write_uint16(HttpPacketType.PKT_TYPE_CHANNEL_RESPONSE)
        stream.write_uint16(0)
        stream.write_uint32(20)

        stream.write_uint32(channel_response.error_code)
        stream.write_uint16(channel_response.fields_present)
        stream.write_uint16(0)

        stream.write_uint32(channel_response.channel_id)

        return stream.buf


    def write_close_response_packet(self, close_response_packet: CloseResponsePacket) -> bytes:
        
        '''
        HTTP_CLOSE_PACKET Structure:

        HTTP_PACKET_HEADER:
        packetType              - uint16 = PKT_TYPE_CLOSE_CHANNEL_RESPONSE
        reserved                - uint16
        packetLength            - uint32 = 12

        Body:
        statusCode              - uint32
        '''

        stream = WritableStream()

        stream.write_uint16(HttpPacketType.PKT_TYPE_CLOSE_CHANNEL_RESPONSE)
        stream.write_uint16(0)
        stream.write_uint32(12)

        stream.write_uint32(close_response_packet.status_code)

        return stream.buf


    def write_data_packet(self, data_packet: DataPacket) -> bytes:
        
        '''
        HTTP_DATA_PACKET Structure:

        HTTP_PACKET_HEADER:
        packetType              - uint16 = PKT_TYPE_DATA
        reserved                - uint16
        packetLength            - uint32 = 10 + len(data)

        Body:
        cbDataLen               - uint16
        data                    - cbDataLen
        '''

        stream = WritableStream()

        stream.write_uint16(HttpPacketType.PKT_TYPE_DATA)
        stream.write_uint16(0)
        stream.write_uint32(10 + len(data_packet.data))

        stream.write_uint16(len(data_packet.data))
        stream.write_bytes(data_packet.data)

        return stream.buf
