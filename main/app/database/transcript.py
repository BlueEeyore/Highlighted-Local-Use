from app.database.models import Transcript
from app.database.models import db
from app.logger_config import get_logger
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
    logger.debug(f"getting transcript with tid {tid}")
    try:
        return Transcript.query.get(tid)
    except Exception as e:
        error.push_log("failed to query transcripts", e, sys.exc_info())
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
    logger.debug(f"returning all transcripts filtered by column {col_name}")
    return Transcript.query.filter(col_attr==val).all()


def insert(lid, timestamp, text):
    """inserts a transcript"""
    logger.debug(f"adding trancsript with {[lid, timestamp, text]}")

    # setting new transcript instance
    new_transcript = Transcript(lid=lid, timestamp=timestamp, text=text)

    # adding new transcript to db
    try:
        db.session.add(new_transcript)
    except Exception as e:
        error.push_log(f"failed to insert transcript {new_transcript} to db", e, sys.exc_info())
        db.session.rollback()
        return None
    return new_transcript


def insert_transcript(lid, transcript_dict):
    """takes a transcription results dict and inserts everything into db"""
    logger.debug(f"adding transcription")

    # transcript_dict has all the info about the transcription
    # this gets just the segments
    segments = transcript_dict["segments"]
    # inserting each segment into the transcript table
    for segment in segments:
        print(segment)
        ts = f"{segment['start']}, {segment['end']}"
        insert(lid, ts, segment["text"])
    
    try:
        db.session.commit()
    except Exception as e:
        error.push_log(f"failed to commit db changes", e, sys.exc_info())
        db.session.rollback()
        return None
    return True