from .database import User
from app.database import db
from .logger_config import get_logger
from app import error
import sys

logger = get_logger(__name__)


def print_cols():
    """prints the columns of User"""
    logger.debug("printing user columns")
    for column in User.__table__.columns:
        print(column.name, column.type)


def all_users():
    """returns all users"""
    logger.debug("getting all users")
    try:
        return User.query.all()
    except Exception as e:
        error.push_log("failed to query users", e, sys.exc_info())
        return None


def get_user(uid):
    """returns user for given uid"""
    logger.debug(f"getting user with uid {uid}")
    try:
        return User.query.get(uid)
    except Exception as e:
        error.push_log("failed to query users", e, sys.exc_info())
        return None


def get_user_by(col_name, val):
    """queries user"""
    logger.debug(f"getting all users with column {col_name} and value {val}")

    # finding the column in User associated with the given column name
    logger.debug(f"getting attribute for column {col_name} in User")
    try:
        col_attr = getattr(User, col_name)
    except AttributeError as e:
        error.push_log(f"failed to get attribute for col {col_name} in User", e, sys.exc(info))
        return None

    # returning all users filtered by that column
    return User.query.filter(col_attr==val).all()


def get_classes(uid):
    """returns classes that the user is a part of"""
    logger.debug(f"getting user classes for {uid}")

    # query user with uid
    try:
        user = User.query.get(uid)
    except Exception as e:
        error.push_log("failed to query user", e, sys.exc_info())
        return None

    # get classes associated with queried user
    try:
        classes = [uc.clazz for uc in user.userclasses]
    except Exception as e:
        error.push_log("failed to query user for uc and then query uc for classes", e, sys.exc_info())
        return None

    return classes

def insert(email, password, firstname, lastname, bio, school, pfp, notifications):
    """inserts a user"""
    logger.debug(f"adding user with {[email, password, firstname, lastname, bio, school, pfp, notifications]}")

    # set new user instance
    new_user = User(email=email, password=password, firstname=firstname, lastname=lastname, bio=bio, school=school, pfp=pfp, notifications=notifications)

    # add new user to db
    try:
        db.session.add(new_user)
    except Exception as e:
        error.push_log(f"failed to add new user {new_user} to db", e, sys.exc_info)
        return None
