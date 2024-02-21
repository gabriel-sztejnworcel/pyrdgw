
from pyrdgw.server.websocket_server import *
from pyrdgw.server.gw_server import *

import logging
import json


def init_logger():

    logger = logging.getLogger('pyrdgw')
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger


def update_log_level(logger: logging.Logger, config):

    log_level = config['logging']['log_level']
    logger.setLevel(logging._nameToLevel[log_level])


def load_configuration():
    
    with open('config.json') as config_file:
        config = json.load(config_file)


    # Validate WebSocket server configuration
    
    if 'websocket_server' not in config:
        raise Exception(LogMessages.CONFIG_MISSING_KEY.format('websocket_server'))

    websocket_server_config = config['websocket_server']

    if 'hostname' not in websocket_server_config:
        raise Exception(LogMessages.CONFIG_MISSING_KEY.format('websocket_server.hostname'))

    if 'port' not in websocket_server_config:
        raise Exception(LogMessages.CONFIG_MISSING_KEY.format('websocket_server.port'))

    if 'cert_path' not in websocket_server_config:
        raise Exception(LogMessages.CONFIG_MISSING_KEY.format('websocket_server.cert_path'))

    if 'key_path' not in websocket_server_config:
        raise Exception(LogMessages.CONFIG_MISSING_KEY.format('websocket_server.key_path'))

    if 'ca_path' not in websocket_server_config:
        raise Exception(LogMessages.CONFIG_MISSING_KEY.format('websocket_server.ca_path'))

    
    # Validate gw server configuration
    
    if 'gw_server' not in config:
        raise Exception(LogMessages.CONFIG_MISSING_KEY.format('gw_server'))

    gw_server_config = config['gw_server']

    if 'hostname' not in gw_server_config:
        raise Exception(LogMessages.CONFIG_MISSING_KEY.format('gw_server.hostname'))

    if 'port' not in gw_server_config:
        raise Exception(LogMessages.CONFIG_MISSING_KEY.format('gw_server.port'))

    if 'cert_path' not in gw_server_config:
        raise Exception(LogMessages.CONFIG_MISSING_KEY.format('gw_server.cert_path'))

    if 'key_path' not in gw_server_config:
        raise Exception(LogMessages.CONFIG_MISSING_KEY.format('gw_server.key_path'))


    # Validate logging configuration

    if 'logging' not in config:
        raise Exception(LogMessages.CONFIG_MISSING_KEY.format('logging'))

    logging_config = config['logging']

    if 'log_level' not in logging_config:
        raise Exception(LogMessages.CONFIG_MISSING_KEY.format('logging_config.log_level'))


    return config


if __name__ == '__main__':

    logger: logging.Logger = None
    
    try:

        logger = init_logger()
        config = load_configuration()
        update_log_level(logger, config)

        websocket_server = WebSocketServer(config)
        websocket_server.run()

        gw_server = GWServer(config)
        gw_server.run()

        loop = asyncio.get_event_loop()
        loop.run_forever()

    except Exception as ex:
        
        if logger is not None:
            logger.error(ex)