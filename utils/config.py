from os import path, environ
from configparser import ConfigParser
from utils import log
from json import load, loads

logger = log.get_logger(name = 'Config')

proxy_url = None
database_path = None
telegram_api_secret = None
enabled_functions = []
if (path.exists('conf/config.ini')):
    config = ConfigParser()
    config.read('conf/config.ini')
    proxy_url = config.get('Bot', 'proxy_url')
    database_path = config.get('Bot', 'database_path')
    telegram_api_secret = config.get('Telegram', 'telegram_api_secret')
    enabled_functions = config.get('Bot', 'enabled_functions')
    auto_delete_timer = config.get('Bot', 'auto_delete_timer')
proxy_url = environ.get('HTTPS_PROXY') or proxy_url
database_path = environ.get('DATABASE_PATH') or database_path
telegram_api_secret = environ.get('TELEGRAM_API_SECRET') or telegram_api_secret
enabled_functions = environ.get('ENABLED_FUNCTIONS') or enabled_functions
enabled_functions = enabled_functions.split(' ')
auto_delete_timer = environ.get('AUTO_DELETE_TIMER') or auto_delete_timer
auto_delete_timer = int(auto_delete_timer)

word_list = None
if (path.exists('conf/keyword_list.json')):
    with open("conf/keyword_list.json", "r") as fp:
        word_list = load(fp)
word_list = loads(environ.get('WORD_LIST_JSON')) if environ.get('WORD_LIST_JSON') else word_list

assert telegram_api_secret, "Telegram API secret not found."