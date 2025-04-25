import logging
logger = logging.getLogger(__name__)


class SessionGlobals:
    def __init__(self):
        logger.debug("initialising")

        self.vars = {}

    def set(self, key, value):
        """assigns key to value"""
        logger.debug(f"setting {key} to {value}")

        self.vars[key] = value

    def get(self, key):
        """gets value associated with given key"""
        logger.debug(f"getting {key}")
        
        return self.vars[key]

    def remove(self, key):
        """removes item associated with given key"""
        logger.debug(f"removing {key}")

        del self.vars[key]

    def increment(self, key):
        """increments value associated with given key (must be int)"""
        logger.debug(f"incrementing {key}")

        try:
            self.vars[key] += 1
        except TypeError as e:
            logger.exception(e)
            raise

    def decrement(self, key):
        """decrements value associated with given key (must be int)"""
        logger.debug(f"decrementing {key}")

        try:
            self.vars[key] -= 1
        except TypeError as e:
            logger.exception(e)
            raise
