from .database import Transcript
from app.database import db
from .logger_config import get_logger
from app import error
import sys

logger = get_logger(__name__)


def print_cols():
    """prints the columns of Transcript"""
    logger.debug("printing transcript columns")
    for column in Transcript.__table__.columns:
        print(column.name, column.type)


def all_transcripts():
    """returns all transcripts"""
    logger.debug("getting all transcripts")
    try:
        return Transcript.query.all()
    except Exception as e:
        error.push_log("failed to query transcripts", e, sys.exc_info())
        return None


def get_transcript(tid):
    """returns transcript for given tid"""
    logger.debug(f"getting user with uid {uid}")
    try:
        return User.query.get(uid)
    except Exception as e:
        error.push_log("failed to query users", e, sys.exc_info())
        return None


def get_transcript_by(col_name, val):
    """queries transcript"""
    logger.debug(f"getting all transcript with column {col_name} and value {val}")

    # finding the column in Transcript associated with the given column name
    logger.debug(f"getting attribute for column {col_name} in Transcript")
    try:
        col_attr = getattr(Transcript, col_name)
    except AttributeError as e:
        error.push_log(f"failed to get attribute for col {col_name} in Transcript", e, sys.exc_info())
        return None

    # returning all transcripts filtered by that column
    return Transcript.query.filter(col_attr==val).all()


def insert(lid, timestamp, text):
    """inserts a transcript"""
    logger.debug(f"adding trancsript with {[lid, timestamp, text]}")

    # setting new transcript instance
    new_transcript = Transcrept(lid=lid, timestamp=timestamp, text=text)

    # adding new transcript to db
    try:
        db.session.add(new_transcript)
    except Exception as e:
        error.push_log(f"failed to insert transcript {new_transcript} to db", e, sys.exc_info())
