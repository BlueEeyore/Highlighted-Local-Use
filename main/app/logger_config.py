import logging


file_handler = logging.FileHandler("logs/logs.log")

formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)
file_handler.setFormatter(formatter)


def get_logger(name):
    """returns module logger"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # avoiding having multiple handlers
    if not logger.hasHandlers():
        logger.addHandler(file_handler)

    logger.info("logger configured")
    return logger
