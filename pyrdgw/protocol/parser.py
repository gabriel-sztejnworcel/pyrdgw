from pyrdgw.protocol.messages import *
from pyrdgw.protocol.enumerations import *
from pyrdgw.util.streams import *
from pyrdgw.log_messages import *


class ProtocolParser:

    def peek_packet_type(self, buf: bytes) -> int:
        stream = ReadableStream(buf)
        packet_type = stream.peek_uint16()
        return packet_type

    
    def read_handshake_request(self, buf: bytes) -> HandshakeRequest:
        '''
        HTTP_HANDSHAKE_REQUEST_PACKET Structure:

        HTTP_PACKET_HEADER:
        packetType              - uint16 = PKT_TYPE_HANDSHAKE_REQUEST
        reserved                - uint16
        packetLength            - uint32 = 14

        Body:
        verMajor                - uint8
        verMinor                - uint8
        clientVersion           - uint16 = 0
        ExtendedAuth            - uint16
        '''

        stream = ReadableStream(buf)
        packet_type = stream.read_uint16()

        if packet_type != HttpPacketType.PKT_TYPE_HANDSHAKE_REQUEST:
            raise Exception(LogMessages.PROTOCOL_INVALID_PACKET_TYPE)

        _ = stream.read_uint16()    # Reserved field
        packet_length = stream.read_uint32()

        if packet_length != 14:
            raise Exception(LogMessages.PROTOCOL_INVALID_PACKET_LENGTH)

        ver_major = stream.read_uint8()
        ver_minor = stream.read_uint8()
        client_version = stream.read_uint16()

        if client_version != 0:
            raise Exception(LogMessages.PROTOCOL_INVALID_CLIENT_VERSION)

        extended_auth = stream.read_uint16()

        handshake_request = HandshakeRequest(ver_major, ver_minor, extended_auth)
        return handshake_request

    
    def read_tunnel_create(self, buf: bytes) -> TunnelCreate:
        '''
        HTTP_TUNNEL_PACKET Structure:

        HTTP_PACKET_HEADER:
        packetType              - uint16 = PKT_TYPE_TUNNEL_CREATE
        reserved                - uint16
        packetLength            - uint32 = 18 + len(PAACookie.blob)

        Body:
        capsFlags               - uint32
        fieldsPresent           - uint16
        reserved                - uint16

        HTTP_TUNNEL_PACKET_OPTIONAL Structure:
        reauthTunnelContext     - uint64 - NOT SUPPORTED
        PAACookie:
        cbLen                   - uint16
        blob                    - cbLen
        '''
        stream = ReadableStream(buf)
        packet_type = stream.read_uint16()

        if packet_type != HttpPacketType.PKT_TYPE_TUNNEL_CREATE:
            raise Exception(LogMessages.PROTOCOL_INVALID_PACKET_TYPE)

        _ = stream.read_uint16()    # Reserved field
        packet_length = stream.read_uint32()

        caps_flags = stream.read_uint32()
        fields_present = stream.read_uint16()

        if fields_present != HttpTunnelPacketFieldsPresentFlags.HTTP_TUNNEL_PACKET_FIELD_PAA_COOKIE:
            raise Exception(LogMessages.PROTOCOL_MISSING_PAA_COOKIE)

        _ = stream.read_uint16()    # Reserved field
        paa_cookie_length = stream.read_uint16()

        if packet_length != 18 + paa_cookie_length:
            raise Exception(LogMessages.PROTOCOL_INVALID_PACKET_LENGTH)

        paa_cookie = stream.read_bytes(paa_cookie_length)

        tunnel_create = TunnelCreate(caps_flags, fields_present, paa_cookie)
        return tunnel_create

    
    def read_tunnel_authorize(self, buf: bytes) -> TunnelAuthorize:
        '''
        HTTP_TUNNEL_AUTH_PACKET Structure:

        HTTP_PACKET_HEADER:
        packetType              - uint16 = PKT_TYPE_TUNNEL_AUTH
        reserved                - uint16
        packetLength            - uint32 = 12 + len(clientName)

        Body:
        fieldsPresent           - uint16
        cbClientName            - uint16
        clientName              - cbClientName

        HTTP_TUNNEL_AUTH_PACKET_OPTIONAL Structure:
        clientName:
        cbLen                   - uint16
        str                     - cbLen
        statementOfHealth       - NOT SUPPORTED
        '''
        stream = ReadableStream(buf)
        packet_type = stream.read_uint16()

        if packet_type != HttpPacketType.PKT_TYPE_TUNNEL_AUTH:
            raise Exception(LogMessages.PROTOCOL_INVALID_PACKET_TYPE)

        _ = stream.read_uint16()    # Reserved field
        packet_length = stream.read_uint32()

        fields_present = stream.read_uint16()

        if fields_present != 0:
            raise Exception(LogMessages.PROTOCOL_UNEXPECTED_FIELDS_TUNNEL_AUTH_OPTIONAL)

        client_name_length = stream.read_uint16()

        if packet_length != 12 + client_name_length:
            raise Exception(LogMessages.PROTOCOL_INVALID_PACKET_LENGTH)

        client_name = stream.read_utf16str(client_name_length)

        tunnel_authorize = TunnelAuthorize(fields_present, client_name)
        return tunnel_authorize

    
    def read_channel_create(self, buf: bytes) -> ChannelCreate:
        '''
        HTTP_CHANNEL_PACKET Structure:

        HTTP_PACKET_HEADER:
        packetType              - uint16 = PKT_TYPE_CHANNEL_CREATE
        reserved                - uint16
        packetLength            - uint32 = 14 + len(pResource) + len(pAltResources)

        Body:
        numResources            - uint8
        numAltResources         - uint8
        port                    - uint16
        protocol                - uint16 = 3

        HTTP_CHANNEL_PACKET_VARIABLE Structure:
        pResource               - Array<cbLen - uint16, str - cbLen> - numResources
        pAltResources           - Array<cbLen - uint16, str - cbLen> - numAltResources
        '''
        stream = ReadableStream(buf)
        packet_type = stream.read_uint16()

        if packet_type != HttpPacketType.PKT_TYPE_CHANNEL_CREATE:
            raise Exception(LogMessages.PROTOCOL_INVALID_PACKET_TYPE)

        _ = stream.read_uint16()    # Reserved field
        packet_length = stream.read_uint32()

        num_resources = stream.read_uint8()
        num_alt_resources = stream.read_uint8()
        port = stream.read_uint16()
        protocol = stream.read_uint16()

        if  protocol != 3:
            raise Exception(LogMessages.PROTOCOL_INVALID_PROTOCOL_CHANNEL_CREATE)

        resources = list()
        total_resources_length = 0
        for i in range(num_resources):
            resource_length = stream.read_uint16()
            total_resources_length = total_resources_length + 2 + resource_length
            resource = stream.read_utf16str(resource_length)
            resources.append(resource)

        alt_resources = list()
        total_alt_resources_length = 0
        for i in range(num_alt_resources):
            alt_resource_length = stream.read_uint16()
            total_alt_resources_length = total_alt_resources_length + 2 + alt_resource_length
            alt_resource = stream.read_utf16str(alt_resource_length)
            alt_resources.append(alt_resource)

        if packet_length != 14 + total_resources_length + total_alt_resources_length:
            raise Exception(LogMessages.PROTOCOL_INVALID_PACKET_LENGTH)

        channel_create = ChannelCreate(num_resources, num_alt_resources, port, resources, alt_resources)
        return channel_create


    def read_close_packet(self, buf: bytes) -> ClosePacket:
        '''
        HTTP_CLOSE_PACKET Structure:

        HTTP_PACKET_HEADER:
        packetType              - uint16 = PKT_TYPE_CLOSE_CHANNEL
        reserved                - uint16
        packetLength            - uint32 = 12

        Body:
        statusCode              - uint32
        '''
        stream = ReadableStream(buf)
        packet_type = stream.read_uint16()

        if packet_type != HttpPacketType.PKT_TYPE_CLOSE_CHANNEL:
            raise Exception(LogMessages.PROTOCOL_INVALID_PACKET_TYPE)

        _ = stream.read_uint16()    # Reserved field
        packet_length = stream.read_uint32()

        if packet_length != 12:
            raise Exception(LogMessages.PROTOCOL_INVALID_PACKET_LENGTH)

        status_code = stream.read_uint32()

        close_packet = ClosePacket(status_code)
        return close_packet


    def read_data_packet(self, buf: bytes) -> DataPacket:
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
        stream = ReadableStream(buf)
        packet_type = stream.read_uint16()

        if packet_type != HttpPacketType.PKT_TYPE_DATA:
            raise Exception(LogMessages.PROTOCOL_INVALID_PACKET_TYPE)

        _ = stream.read_uint16()    # Reserved field
        packet_length = stream.read_uint32()

        data_length = stream.read_uint16()

        if packet_length != 10 + data_length:
            raise Exception(LogMessages.PROTOCOL_INVALID_PACKET_LENGTH)

        data = stream.read_bytes(data_length)

        data_packet = DataPacket(data)
        return data_packet