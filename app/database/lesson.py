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


def insert(classid, name, videofn, mimetype, creationtime):
    """inserts a lesson"""
    logger.debug(f"""adding lesson with {[
        classid,
        name,
        videofn,
        mimetype,
        creationtime
    ]}""")

    # setting new lesson instance
    try:
        new_lesson = Lesson(
            classid=classid,
            name=name,
            videofn=videofn,
            mimetype=mimetype,
            creationtime=creationtime
        )
    except Exception as e:
        error.push_log(
            "filed to create Lesson row instance",
            e,
            sys.exc_info()
        )
        return False

    # adding new lesson to db
    try:
        db.session.add(new_lesson)
    except Exception as e:
        error.push_log(
            f"failed to add new lesson {new_lesson} to db",
            e,
            sys.exc_info()
        )
        db.session.rollback()
        return None

    return new_lesson


def delete(lid):
    """deletes a lesson for given lid"""
    logger.debug(f"deleting lesson with lid {lid}")
    less = get_lesson(lid)
    if not less:
        error.push_log(f"lesson {lid} not found for deletion")
        return False
    try:
        db.session.delete(less)
        db.session.commit()
        logger.debug(f"lesson {lid} deleted successfully")
        return True
    except Exception as e:
        error.push_log(f"failed to delete lesson {lid}", e, sys.exc_info())
        db.session.rollback()
        return False


def rename(lid, new_name):
    """renames a lesson for given lid"""
    logger.debug(f"renaming lesson {lid} to {new_name}")
    less = get_lesson(lid)
    if not less:
        error.push_log(f"lesson {lid} not found for renaming")
        return False
    try:
        less.name = new_name
        db.session.commit()
        logger.debug(f"lesson {lid} renamed successfully")
        return True
    except Exception as e:
        error.push_log(f"failed to rename lesson {lid}", e, sys.exc_info())
        db.session.rollback()
        return False
