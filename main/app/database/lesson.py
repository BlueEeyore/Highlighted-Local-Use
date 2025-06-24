from app.database.models import Lesson
from app.database.models import db
from app.logger_config import get_logger
from app import error
import sys


logger = get_logger(__name__)


def print_cols():
    """prints the columns of Lesson"""
    logger.debug("printing lesson columns")
    for column in Lesson.__table__.columns:
        print(column.name, column.type)


def all_lessons():
    """returns all lessons in table"""
    logger.debug("getting all lesson columns")
    try:
        return Lesson.query.all()
    except Exception as e:
        error.push_log("failed to query lessons", e, sys.exc_info())
        return None


def get_lesson(lid):
    """returns lesson for given lid"""
    logger.debug(f"getting lesson with lid {lid}")
    try:
        return Lesson.query.get(lid)
    except Exception as e:
        error.push_log("failed to query lessons", e, sys.exc_info())
        return None


def insert(creatorid, classid, name, videofn, mimetype, creationtime):
    """inserts a lesson"""
    logger.debug(f"adding lesson with {[creatorid, classid, name, videofn, mimetype, creationtime]}")

    # setting new lesson instance
    try:
        new_lesson = Lesson(creatorid=creatorid, classid=classid, name=name, videofn=videofn, mimetype=mimetype, creationtime=creationtime)
    except Exception as e:
        error.push_log(f"filed to create Lesson row instance", e, sys.exc_info()) 
        return False

    # adding new lesson to db
    try:
        db.session.add(new_lesson)
    except Exception as e:
        error.push_log(f"failed to add new lesson {new_lesson} to db", e, sys.exc_info())
        db.session.rollback()
        return None

    return new_lesson