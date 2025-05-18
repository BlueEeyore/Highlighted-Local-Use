from .database import User
from app.routes import db
import logging

logger = logging.getLogger(__name__)


def print_cols():
    """prints the columns of User"""
    logger.debug("printing user columns")
    for column in User.__table__.columns:
        print(column.name, column.type)


def all_users():
    """returns all users"""
    logger.debug("getting all users")
    return User.query.all()


def get_user(uid):
    """returns user for given uid"""
    logger.debug(f"getting user with uid {uid}")
    user = User.query.get(uid)
    return user


def get_user_by(col_name, val):
    """queries user"""
    logger.debug(f"getting all users with column {col_name} and value {val}")

    # finding the column in User associated with the given column name
    col_attr = getattr(User, col_name)

    # returning all users filtered by that column
    return User.query.filter(col_attr==val).all()


def get_classes(uid):
    """returns classes that the user is a part of"""
    logger.debug(f"getting user classes for {uid}")

    user = User.query.get(uid)
    classes = [uc.clazz for uc in user.userclasses]
    return classes

def insert(email, password, firstname, lastname, bio, school, pfp, notifications, unique_col="email"):
    """inserts a user"""
    logger.debug(f"adding user with {[email, password, firstname, lastname, bio, school, pfp, notifications]}")
    new_user = User(email=email, password=password, firstname=firstname, lastname=lastname, bio=bio, school=school, pfp=pfp, notifications=notifications)
    db.session.add(new_user)
