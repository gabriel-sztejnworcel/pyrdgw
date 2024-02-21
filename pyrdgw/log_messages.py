
class LogMessages:

    GW_SERVER_LISTENING = 'RD Gateway server listening on {}:{}'
    GW_FAILED_PROCESS_HTTP_REQUEST = 'Failed to process HTTP request'
    GW_ATTEMPT_NON_WEBSOCKET = 'Unsupported attempt to connect without WebSocket'
    
    WEBSOCKET_RECEIVED_CONNECTION_REQUEST = 'Received WebSocket connection request'
    WEBSOCKET_SERVER_LISTENING = 'WebSocket server listening on {}:{}'

    PROTOCOL_INVALID_MAJOR_VERSION = 'Invalid major protocol version'
    PROTOCOL_INVALID_MINOR_VERSION = 'Invalid minor protocol version'
    PROTOCOL_INVALID_AUTHENTICATION_METHOD = 'Invalid authentication method'
    PROTOCOL_NO_RESOURCES_FOR_CHANNEL = 'No resources were supplied for the channel'
    PROTOCOL_INVALID_PACKET_TYPE = 'Invalid packet type'
    PROTOCOL_INVALID_PACKET_LENGTH = 'Invalid packet length'
    PROTOCOL_INVALID_CLIENT_VERSION = 'Invalid client version'
    PROTOCOL_MISSING_PAA_COOKIE = 'PAA cookie is missing'
    PROTOCOL_UNEXPECTED_FIELDS_TUNNEL_AUTH_OPTIONAL = 'Unexpected optional fields in tunnel authorize request'
    PROTOCOL_INVALID_PROTOCOL_CHANNEL_CREATE = 'Invalid protocol in channel create request'
    PROTOCOL_TRANSITION_STATE = 'Transition from state {} to {}'
    PROTOCOL_RECEIVED_CLIENT_NAME = 'Received client name: {}'
    PROTOCOL_SENDING_MESSAGE = 'Sending protocol message {}'
    PROTOCOL_RECEIVED_MESSAGE = 'Received protocol message {}'

    COMM_FAILED_CONNECT_ANY_RESOURCE = 'Failed to connect to any of the specified resources'
    COMM_CONNECTED_RESOURCE = 'Connected to target: {}:{}'
    COMM_FAILED_CONNECT_RESOURCE = 'Failed to connect to {}:{}. Reason: {}'
    
    CONFIG_MISSING_KEY = 'Missing key "{}" in configuration file'