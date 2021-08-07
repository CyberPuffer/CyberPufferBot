from utils import log

logger = log.get_logger(name = 'Functions')

def load_funcs(dispatcher):
    # from importlib import __import__
    from utils import config
    for function in config.enabled_functions:
        func = getattr(__import__('functions.'+function), function)
        if func.handler is not None:
            dispatcher.add_handler(func.handler)
            logger.info('{} loaded'.format(func.__name__))