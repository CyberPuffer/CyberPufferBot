from utils import globals, config, functions
from queue import Queue
from telegram import Bot, Update
from telegram.ext import Dispatcher
from telegram.utils.request import Request

# Use global varible cache to optimize speed
dispatcher = None

# Entrypoint for GCE Cloud Functions
def webhook(request):
    globals.webhook = True
    bot = Bot(token=config.telegram_api_secret)
    bot._request=Request(proxy_url=config.proxy_url)

    global dispatcher
    if not dispatcher:
        dispatcher = Dispatcher(bot, Queue())
        functions.load_all_funcs(dispatcher)

    if request.method == "POST":
        update_text = request.get_json(force=True)
        update = Update.de_json(update_text, bot)
        dispatcher.process_update(update)
    return "ok"