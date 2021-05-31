import coloredlogs, logging

loggers = {}
def get_logger(name=None):
    global loggers
    if not name: name = __name__
    if loggers.get(name):
        return loggers.get(name)
    logger = logging.getLogger(name)
    coloredlogs.install(logger=logger)
    loggers[name] = logger
    return logger