import logging
from flask import session
from datetime import timedelta


logger = logging.getLogger(__name__)


def session_config(app):
    """configures session"""
    # sign the session cookie
    app.secret_key = "very-secret-key"

    # make the session last a certain amount of time rather than
    # just closing when the browser closes
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)


def set(key, value):
    """assigns key to value"""
    logger.debug(f"setting {key} to {value}")

    # checking if the global dictionary has been created yet. If not, creates it
    if "global_dict" not in session:
        logger.debug("creating global_dict")
        session["global_dict"] = {}

    session["global_dict"][key] = value


def get(key):
    """gets value associated with given key
    returns None if key doesn't exist"""
    logger.debug(f"getting {key}")

    # checks if the item is in the dictionary. If not, returns None
    if key not in session["global_dict"]:
        logger.debug(f"key {key} not found")
        return None

    return session["global_dict"][key]


def remove(key):
    """removes item associated with given key"""
    logger.debug(f"removing {key}")
    del session["global_dict"][key]
    

def print_dict():
    """prints the global dictionary (used only for debugging)"""
    logger.debug(f"printing dictionary")
    print(session["global_dict"])


def increment(key):
    """increments value associated with given key (must be int)"""
    logger.debug(f"incrementing {key}")
    session["global_dict"][key] += 1


def decrement(key):
    """decrements value associated with given key (must be int)"""
    logger.debug(f"decrementing {key}")
    session["global_dict"][key] -= 1





# class SessionGlobals:
#     def __init__(self):
#         logger.debug("initialising")
# 
#         self.vars = {}
# 
#     def set(self, key, value):
#         """assigns key to value"""
#         logger.debug(f"setting {key} to {value}")
# 
#         self.vars[key] = value
# 
#     def get(self, key):
#         """gets value associated with given key"""
#         logger.debug(f"getting {key}")
#         
#         return self.vars[key]
# 
#     def remove(self, key):
#         """removes item associated with given key"""
#         logger.debug(f"removing {key}")
# 
#         del self.vars[key]
# 
#     def increment(self, key):
#         """increments value associated with given key (must be int)"""
#         logger.debug(f"incrementing {key}")
# 
#         try:
#             self.vars[key] += 1
#         except TypeError as e:
#             logger.exception(e)
#             raise
# 
#     def decrement(self, key):
#         """decrements value associated with given key (must be int)"""
#         logger.debug(f"decrementing {key}")
# 
#         try:
#             self.vars[key] -= 1
#         except TypeError as e:
#             logger.exception(e)
#             raise
