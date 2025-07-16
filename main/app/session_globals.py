from .logger_config import get_logger
from flask import session
from flask_session import Session
from datetime import timedelta
from app.transcription import Transcription
import uuid
import redis


logger = get_logger(__name__)
session_dicts = {}


def session_config(app):
    """configures session"""
    # sign the session cookie
    app.secret_key = "very-secret-key"

    # make the session last a certain amount of time rather than
    # just closing when the browser closes
    # app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=0.5)  # commented for dev


def _get_globs():
    """gets global dictionary"""
    # check whether the session already has a unique id
    if "uuid" not in session:
        # give the session a unique id
        session["uuid"] = str(uuid.uuid4())

        # assign a new empty global dictionary to the new session
        session_dicts[session["uuid"]] = {}
    return session_dicts[session["uuid"]]


def set(key, value):
    """assigns key to value"""
    logger.debug(f"setting {key} to {value} in session")

    globs = _get_globs()
    globs[key] = value


def get(key):
    """gets value associated with given key
    returns None if key doesn't exist"""
    logger.debug(f"getting {key} from session dict")

    globs = _get_globs()

    # checks if the item is in the dictionary. If not, returns None
    if key not in globs:
        logger.debug(f"key {key} not found")
        return None

    return globs[key]


def remove(key):
    """removes item associated with given key"""
    logger.debug(f"removing {key}")

    globs = _get_globs()
    del globs[key]
    

def print_dict():
    """prints the global dictionary (used only for debugging)"""
    logger.debug(f"printing dictionary")

    globs = _get_globs()
    print(globs)


def increment(key):
    """increments value associated with given key (must be int)"""
    logger.debug(f"incrementing {key}")

    globs = _get_globs()
    globs[key] -= 1


def decrement(key):
    """decrements value associated with given key (must be int)"""
    logger.debug(f"decrementing {key}")

    globs = _get_globs()
    globs[key] -= 1


def get_transcriber():
    """
    Gets Transcription object instance from session.
    If instance doesn't exist, creates a new one
    """
    logger.debug("getting Transcription object from session")

    transcriber = get("transcription")

    if transcriber is None:
        logger.debug("Transcription object does not exist in session. Creating new one")
        transcriber = Transcription()
        set("transcription", transcriber)
    
    return transcriber



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
