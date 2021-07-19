from telegram import Bot, Update, constants
from telegram.ext import Updater, Dispatcher
from queue import Queue
from utils import config, log
from functions import *

logger = log.get_logger(name = 'Bot')

enabled_funcs = [
    (uptime,uptime.uptime_handler),
    # (stats, stats.stats_handler),
    (antispam, antispam.channel_handler),
    (keyword_reply, keyword_reply.keyword_handler)
    ]

def add_funcs(dispatcher):
    for func, handler in enabled_funcs:
        dispatcher.add_handler(handler)
        logger.info('{} loaded'.format(func.__name__))

# Entrypoint for GCE Cloud Functions
def webhook(request):
    bot = Bot(token=config.telegram_api_secret)
    dispatcher = Dispatcher(bot, Queue())
    add_funcs(dispatcher)

    if request.method == "POST":
        update_text = request.get_json(force=True)
        update = Update.de_json(update_text, bot)
        dispatcher.process_update(update)
    return "ok"

if __name__ == "__main__":
    REQUEST_KWARGS={'proxy_url': config.proxy_url}
    updater = Updater(token=config.telegram_api_secret, use_context=True, request_kwargs=REQUEST_KWARGS)
    dispatcher = updater.dispatcher
    add_funcs(dispatcher)
    updater.start_polling(allowed_updates=constants.UPDATE_ALL_TYPES)