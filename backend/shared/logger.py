import logging

class Logger():

    current_logger = logging.getLogger()

    @classmethod
    def set_current_logger_by_name(cls, name: str):
        cls.current_logger = get_logger(name)

    @classmethod
    def get_current_logger(cls):
        return cls.current_logger
    
def get_logger(name: str):
    if name in logging.root.manager.loggerDict:
        return logging.getLogger(name)
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        # "{asctime} - {levelname} - {module} - {pathname} - {filename} - {funcName} - {message}",
        "{asctime} - {levelname} - {filename} - {funcName} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
