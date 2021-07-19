from os import path, environ
from configparser import ConfigParser
from utils import log
from json import load, loads

logger = log.get_logger(name = 'Config')

if (path.exists('conf/config.ini')):
    config = ConfigParser()
    config.read('conf/config.ini')
    proxy_url = config.get('Bot', 'proxy_url', fallback='')
    database_path = config.get('Bot', 'database_path')
    telegram_api_secret = config.get('Telegram', 'telegram_api_secret')

proxy_url = environ.get('HTTPS_PROXY') or proxy_url
database_path = environ.get('DATABASE_PATH') or database_path
telegram_api_secret = environ.get('TELEGRAM_API_SECRET') or telegram_api_secret

if (path.exists('conf/config.ini')):
    with open("conf/config.ini", "r") as fp:
        word_list = load(fp)

word_list = loads(environ.get('TELEGRAM_API_SECRET')) if environ.get('TELEGRAM_API_SECRET') else word_list

assert telegram_api_secret, "Telegram API secret not found."