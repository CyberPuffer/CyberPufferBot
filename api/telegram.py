from telegram import constants
from telegram.ext import Updater
from distutils.version import LooseVersion
from telegram import __version__ as ptb_version
from utils import global_vars, log
logger = log.get_logger(name='Bot')

def polling(args):

    api_config = args['config'].split(':')

    # Get API secret
    api_secret = ':'.join(api_config[1:3])

    # Check config type
    try:
        config_id = int(api_config[3])
        config_type = 'cloud'
    except ValueError:
        config_file = api_config[3]
        config_type = 'local'

    # Proxy settings
    request_kwargs = {'proxy_url': args['proxy']} if args['proxy'] is not None else None
    
    updater = Updater(token=api_secret, use_context=True, request_kwargs=request_kwargs)
    dispatcher = updater.dispatcher
    global_vars.dispatcher = dispatcher
    load_all_funcs(dispatcher, config_id)
    if LooseVersion(ptb_version) >= LooseVersion('13.5'):
        updater.start_polling(allowed_updates=constants.UPDATE_ALL_TYPES)
    else:
        logger.warn('PTB version < 13.5, not all update types are listening')
        updater.start_polling()

def get_cloud_config(dispatcher, config_id):
    from tomli import loads
    channel_info = dispatcher.bot.get_chat(config_id)
    if channel_info.pinned_message is None:
        msg = dispatcher.bot.send_message(config_id, init_index(),protect_content=True)
        dispatcher.bot.pin_chat_message(config_id,msg.message_id,disable_notification=True)
        index = msg
    else:
        index = channel_info.pinned_message
    return loads(index.text)

def init_index():
    from tomli_w import dumps
    index = {
        'version': 0
    }
    return dumps(index)

def get_handler(name):
    # from importlib import __import__
    func = __import__('modules.{name}.{name}'.format(name=name))
    try:
        return getattr(getattr(func, name), name).get_handler()
    except AttributeError:
        pass
    try:
        return load_generic_func(getattr(getattr(getattr(func, name), name),name), name)
    except:
        pass

def find_handler(dispatcher, name):
    default_handler_group = dispatcher.handlers[0]
    for handler in default_handler_group:
        if handler.callback.__name__ == name:
            return handler

def load_funcs(dispatcher, name):
    from traceback import print_exc
    try:
        handler = get_handler(name)
        if handler is not None:
            dispatcher.add_handler(handler)
            logger.info('Module {} loaded'.format(name))
        else:
            logger.warning('Module {} failed to load, handler not found'.format(name))
            return False
    except TypeError:
        handler_r, action = handler
        if handler_r is not None:
            dispatcher.add_handler(handler_r)
            logger.info('Module {} loaded'.format(name))
        if 'reload' in action.keys():
            for item in action['reload']:
                logger.warning('Module {} triggered a reload for module {}'.format(name, item))
                reload_funcs(dispatcher, item)
    except Exception:
        print_exc()
        logger.warning('Module {} failed to load'.format(name))
        return False
    return True

def load_generic_func(func, name):
    from telegram.ext import CommandHandler
    def wrapped_func(update, context):
        sender = {
            "user_id": update.effective_chat.id,
            "source": "Telegram"
            }
        reply_message, reply_user = func(update.message.text, sender)
        reply = [context.bot.send_message(chat_id=reply_user["user_id"], text=reply_message)]
        return reply
    return CommandHandler(name, wrapped_func)

def unload_funcs(dispatcher, name):
    handler = find_handler(dispatcher,name)
    if handler is not None:
        dispatcher.remove_handler(handler)
        logger.info('Module {} unloaded'.format(name))
        return True
    else:
        logger.warning('{} failed to unload'.format(name))
        return False

def reload_funcs(dispatcher, name):
    unload_funcs(dispatcher, name)
    load_funcs(dispatcher, name)

def load_all_funcs(dispatcher, config_id):
    from utils import global_vars
    conf = get_cloud_config(dispatcher, config_id)
    global_vars.telegram_config = conf
    for name in [n.strip() for n in conf['enabled_modules'].split(',')]:
        load_funcs(dispatcher, name)

def list_funcs(dispatcher):
    default_handler_group = dispatcher.handlers[0]
    func_list = []
    for handler in default_handler_group:
        func_list.append(handler.callback.__name__)
    return func_list