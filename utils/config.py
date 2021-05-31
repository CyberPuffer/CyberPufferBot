from os import path
from configparser import ConfigParser
from utils import log

logger = log.get_logger(name = 'Config')

if (path.exists('conf/config.ini')):
    config = ConfigParser()
    config.read('conf/config.ini')
    proxy_url = config.get('Bot', 'proxy_url', fallback='')
    database_path = config.get('Bot', 'database_path')
    telegram_api_secret = config.get('Telegram', 'telegram_api_secret')
else:
    logger.error('Config file not found.')
    exit(1)