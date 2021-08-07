loggers = {}
def get_logger(name=None):
    from coloredlogs import install 
    from logging import getLogger
    global loggers
    if not name: name = __name__
    if loggers.get(name):
        return loggers.get(name)
    logger = getLogger(name)
    install(logger=logger)
    loggers[name] = logger
    return logger