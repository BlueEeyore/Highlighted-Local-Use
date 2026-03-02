from app.database.models import Class, db
from app.logger_config import get_logger
from app import error
import sys
import random
import string

logger = get_logger(__name__)


def print_cols():
    """prints the columns of Class"""
    logger.debug("printing class columns")
    for column in Class.__table__.columns:
        print(column.name, column.type)


def all_classes():
    """returns all classes"""
    logger.debug("getting all classes")
    try:
        return Class.query.all()
    except Exception as e:
        error.push_log("failed to query classes", e, sys.exc_info())
        return None


def get_class(cid):
    """returns class for given cid"""
    logger.debug(f"getting class with cid {cid}")
    try:
        return Class.query.get(cid)
    except Exception as e:
        error.push_log("failed to query classes", e, sys.exc_info())
        return None


def get_class_by(col_name, val):
    """queries class by one requirement"""
    logger.debug(f"getting all classes with column {col_name} and value {val}")

    # finding the column in Class associated with the given column name
    logger.debug(f"getting attribute for column {col_name} in Class")
    try:
        col_attr = getattr(Class, col_name)
    except AttributeError as e:
        error.push_log(
            f"failed to get attribute for col {col_name} in Class",
            e,
            sys.exc_info()
        )
        return None

    # returning all classes filtered by that column
    logger.debug(f"returning all classes filtered by column {col_name}")
    return Class.query.filter(col_attr == val).all()


def get_filtered(*filters):
    """queries class with given filters"""
    logger.debug(f"getting all classes with filters {filters}")

    try:
        return db.session.query(Class).filter(*filters).all()
    except Exception as e:
        error.push_log(
            f"failed to query Class with filters {filters}",
            e,
            sys.exc_info()
        )
        return None


def get_users(cid):
    """returns users that are in a class"""
    logger.debug(f"getting users in class with {cid}")

    # query class with cid
    try:
        clazz = Class.query.get(cid)
    except Exception as e:
        error.push_log("failed to query class", e, sys.exc_info())
        return None

    # get users associated with queried class
    try:
        users = [uc.user for uc in clazz.userclasses]
    except Exception as e:
        error.push_log(
            "failed to query class for uc and then query uc for users",
            e,
            sys.exc_info()
        )
        return None

    return users


def get_lessons(cid):
    """returns lessons that are in a class"""
    logger.debug(f"getting lessons in class with {cid}")

    # query class with cid
    try:
        clazz = Class.query.get(cid)
    except Exception as e:
        error.push_log("failed to query class", e, sys.exc_info())
        return None

    # get lessons associated with queried class
    try:
        lessons = clazz.lessons
    except Exception as e:
        error.push_log("failed to query class for lessons", e, sys.exc_info())
        return None

    return lessons


def generate_unique_joincode(length=8):
    """generates a unique joincode for the class"""
    characters = string.ascii_uppercase + string.digits
    i = 0
    while True:
        i += 1
        if i >= 1000:
            return None

        code = ''.join(random.choices(characters, k=length))
        exists = db.session.query(Class).filter_by(joincode=code).first()
        if not exists:
            return code


def insert(name, private, school, joincode, starttime):
    """inserts a class"""
    logger.debug(f"""adding class with {[
        name, private, school, joincode, starttime
    ]}""")

    # set new class instance
    new_class = Class(
        name=name,
        private=private,
        school=school,
        joincode=joincode,
        starttime=starttime
    )

    # add new class to db
    try:
        db.session.add(new_class)
    except Exception as e:
        error.push_log(
            f"failed to add new class {new_class} to db",
            e,
            sys.exc_info()
        )
        db.session.rollback()
        return None

    # commit to db
    try:
        db.session.commit()
    except Exception as e:
        error.push_log("failed to commit to db", e, sys.exc_info())
        db.session.rollback()
        return None

    return new_class
