from .database import Lesson
from app.routes import db
import logging
from app import error
import sys


logger = logging.getLogger(__name__)


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


def insert(creatorid, classid, name, videofn, creationtime):
    """inserts a lesson"""
    logger.debug(f"adding lesson with {[creatorid, classid, name, videofn, creationtime]}")

    # setting new lesson instance
    new_lesson = Lesson(creatorid=creatorid, classid=classid, name=name, videofn=videofn, creationtime=creationtime)

    # adding new lesson to db
    try:
        db.session.add(new_lesson)
    except Exception as e:
        error.push_log(f"failed to add new lesson {new_lesson} to db", e, sys.exc_info())
