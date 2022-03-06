from utils import log

logger = log.get_logger(name='Functions')

def get_handler(name):
    # from importlib import __import__
    func = __import__('modules.{name}.{name}'.format(name=name))
    return getattr(getattr(func, name), name).get_handler()

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

def load_all_funcs(dispatcher, args):
    from utils import config, globals
    conf = config.get_config(dispatcher, args)
    globals.config = conf
    for name in [n.strip() for n in conf['enabled_modules'].split(',')]:
        load_funcs(dispatcher, name)

def list_funcs(dispatcher):
    default_handler_group = dispatcher.handlers[0]
    func_list = []
    for handler in default_handler_group:
        func_list.append(handler.callback.__name__)
    return func_list