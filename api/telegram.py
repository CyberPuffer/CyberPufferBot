from telegram import constants
from telegram.ext import Updater
from distutils.version import LooseVersion
from telegram import __version__ as ptb_version
from utils.global_vars import message_handler
from utils.log import get_logger

logger = get_logger(name='Telegram')

def polling(args):

    # Parse API secret
    api_config = args['config'].split(':')
    api_secret = ':'.join(api_config[1:3])

   # Init handler in global varibles
    handler_name = 'Telegram:' + api_config[1]
    message_handler[handler_name] = {}

    # Check config type
    try:
        config_path = int(api_config[3])
        config_type = 'cloud'
    except ValueError:
        config_path = api_config[3]
        config_type = 'local'

    # Proxy settings
    request_kwargs = {'proxy_url': args['proxy']} if args['proxy'] is not None else None
    
    # Init dispatcher
    updater = Updater(token=api_secret, use_context=True, request_kwargs=request_kwargs)
    dispatcher = updater.dispatcher

    # Register dispatcher and sender
    message_handler[handler_name]['dispatcher'] = dispatcher

    def sender(message, receiver):
        return send_message(message, receiver, handler_name)
    message_handler[handler_name]['sender'] = sender

    # Load all modules
    load_all_funcs(dispatcher, handler_name, config_type, config_path)

    # Start polling
    if LooseVersion(ptb_version) >= LooseVersion('13.5'):
        updater.start_polling(allowed_updates=constants.UPDATE_ALL_TYPES)
    else:
        logger.warn('PTB version < 13.5, not all update types are listening')
        updater.start_polling()

def load_all_funcs(dispatcher, handler_name, config_type, config_id):
    from traceback import print_exc

    # Load module config
    conf = get_config(dispatcher, config_type, config_id)
    message_handler[handler_name]['config'] = conf

    # Load all modules handlers
    for name in [n.strip() for n in conf['enabled_modules'].split(',')]:
        try:
            func = __import__('modules.{name}.{name}'.format(name=name))
            handler = load_func(getattr(getattr(getattr(func, name), name),name), name, handler_name)
            dispatcher.add_handler(handler)
            logger.info('Module {} loaded'.format(name))
        except:
            print_exc()
            logger.warning('Module {} failed to load'.format(name))

def load_func(func, name, handler_name):
    from telegram.ext import CommandHandler, MessageHandler, Filters
    def wrapped_func(update, context):
        sender = {
            "user_id": update.effective_chat.id,
            "source": handler_name
            }
        reply_message, receiver = func(update.message.text, sender)
        reply = send_message(reply_message,receiver,handler_name)
        return reply
    if name == 'keyword':
        return MessageHandler(Filters.text & (~Filters.command), wrapped_func)
    else:
        return CommandHandler(name, wrapped_func)

def get_config(dispatcher, config_type, config_id):
    from tomli import loads, load
    if config_type == 'cloud':
        channel_info = dispatcher.bot.get_chat(config_id)
        if channel_info.pinned_message is None:
            msg = dispatcher.bot.send_message(config_id, init_config())
            dispatcher.bot.pin_chat_message(config_id,msg.message_id,disable_notification=True)
            index = msg
        else:
            index = channel_info.pinned_message
        return loads(index.text)
    elif config_type == 'local':
        with open(config_id, encoding="utf-8") as f:
            return load(f)
    else:
        raise NotImplementedError("Config type not supported")

def init_config():
    from tomli_w import dumps
    index = {
        'enabled_modules': "uptime, keyword, luck, weibo"
    }
    return dumps(index)

def send_message(message, receiver, handler_name):
    from utils.global_vars import message_handler
    context = message_handler[handler_name]['dispatcher']
    if 'type' in receiver.keys():
        if receiver['type'] == 'text':
            reply = context.bot.send_message(chat_id=receiver["user_id"], text=message)
        elif receiver['type'] == 'sticker':
            reply = context.bot.send_sticker(chat_id=receiver["user_id"], sticker=message)
        elif receiver['type'] == 'forward':
            sep, from_chat_id, message_id = message.partition('@')
            reply = context.bot.forward_message(chat_id=receiver["user_id"], from_chat_id=from_chat_id, message_id=message_id)
        else:
            pass
    else:
        reply = context.bot.send_message(chat_id=receiver["user_id"], text=message)
    return reply

def find_handler(dispatcher, name):
    default_handler_group = dispatcher.handlers[0]
    for handler in default_handler_group:
        if handler.callback.__name__ == name:
            return handler

def unload_funcs(dispatcher, name):
    handler = find_handler(dispatcher,name)
    if handler is not None:
        dispatcher.remove_handler(handler)
        logger.info('Module {} unloaded'.format(name))
        return True
    else:
        logger.warning('{} failed to unload'.format(name))
        return False

def list_funcs(dispatcher):
    default_handler_group = dispatcher.handlers[0]
    func_list = []
    for handler in default_handler_group:
        func_list.append(handler.callback.__name__)
    return func_list