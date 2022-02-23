from os import path, environ
from configparser import ConfigParser
from utils import log

logger = log.get_logger(name = 'Config')

proxy_url = None
database_path = None
telegram_api_secret = None
enabled_modules = []
if (path.exists('config.ini')):
    config = ConfigParser()
    config.read('config.ini')
    proxy_url = config.get('Bot', 'proxy_url')
    database_path = config.get('Bot', 'database_path')
    telegram_api_secret = config.get('Telegram', 'telegram_api_secret')
    enabled_modules = config.get('Bot', 'enabled_modules')
    auto_delete_timer = config.get('Bot', 'auto_delete_timer')
    debug_signature = config.get('Admin', 'debug_signature')
    debug_key = config.get('Admin', 'debug_key')
    admin_user_id = config.get('Admin', 'admin_user_id')
    cailianshe_channel_id = config.get('CaiLianShe', 'cailianshe_channel_id')

proxy_url = environ.get('HTTPS_PROXY') or proxy_url
database_path = environ.get('DATABASE_PATH') or database_path
telegram_api_secret = environ.get('TELEGRAM_API_SECRET') or telegram_api_secret
enabled_modules = environ.get('ENABLED_modules') or enabled_modules
enabled_modules = enabled_modules.split(' ')
auto_delete_timer = environ.get('AUTO_DELETE_TIMER') or auto_delete_timer
auto_delete_timer = int(auto_delete_timer)

assert telegram_api_secret, "Telegram API secret not found."