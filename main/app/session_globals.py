from .logger_config import get_logger
from flask import session
from flask_session import Session
from datetime import timedelta
from app.transcription import Transcription
from app.database.models import db
# from flask_session.session_interface.serializer import PickleSerializer
import pickle


logger = get_logger(__name__)


# class PickleSerializer:
#     """Minimal serializer for Flask-Session to pickle arbitrary objects."""
#     def encode(self, session_dict):
#         # Flask-Session will call this to turn session into bytes.
#         return pickle.dumps(session_dict)

#     def decode(self, pickle_bytes):
#         # Flask-Session will call this to rehydrate session.
#         return pickle.loads(pickle_bytes)
# class PickleSerializer:
#     def dumps(self, obj):
#         return pickle.dumps(obj)
#     def loads(self, data):
        # return pickle.loads(data)
# --- Pickle Serializer Wrapper ---
# Flask-Session expects a serializer with encode/decode methods.
class PickleSerializer:
    def encode(self, session_object):
        """
        Serialize the session object.

        The session object is a complex ServerSideSession object.
        We convert it to a simple dictionary before pickling to
        remove the non-serializable parts, like the 'on_update' callback.
        """
        # Convert the session object to a plain dictionary
        plain_dict = dict(session_object)
        return pickle.dumps(plain_dict, pickle.HIGHEST_PROTOCOL) 

    def decode(self, data):
        """Deserialize the data using pickle."""
        return pickle.loads(data)

def session_config(app):
    """configures session"""
    # sign the session cookie
    app.secret_key = "very-secret-key"

    app.config["SESSION_TYPE"] = "sqlalchemy"
    app.config["SESSION_SQLALCHEMY"] = db
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_USE_SIGNER"] = True # Secures the session ID cookie

    # # switch serialiser to pickle instead of JSON
    # app.config["SESSION_SERIALIZER"] = pickle
    
    # if i want to change the table name:
    # app.config['SESSION_SQLALCHEMY_TABLE'] = 'flask_session'

    session_handle = Session(app)
    session_handle.app.session_interface.serializer = PickleSerializer()

    # make the session last a certain amount of time rather than
    # just closing when the browser closes
    # app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=0.5)  # commented for dev


def _get_globs():
    """gets global dictionary"""
    return session


def set(key, value):
    """assigns key to value"""
    logger.debug(f"setting {key} to {value} in session")

    globs = _get_globs()
    globs[key] = value
    session.modified = True


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


# def get_transcriber():
#     """
#     Gets Transcription object instance from session.
#     If instance doesn't exist, creates a new one
#     """
#     logger.debug("getting Transcription object from session")

#     transcriber = get("transcription")

#     if transcriber is None:
#         logger.debug("Transcription object does not exist in session. Creating new one")
#         transcriber = Transcription()
#         set("transcription", transcriber)
    
#     return transcriber



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
