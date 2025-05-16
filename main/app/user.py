from .database import User
import logging

logger = logging.getLogger(__name__)


def print_cols():
    """prints the columns of User"""
    logger.debug("printing user columns")
    for column in User.__table__.columns:
        print(column.name, column.type)

def get_user(uid):
    """returns user for given uid"""
    logger.debug(f"getting user with uid {uid}")
    user = User.query.get(uid)
    return user

def get_classes(uid):
    """returns classes that the user is a part of"""
    logger.debug(f"getting user classes for {uid}")
    print(f"UID TYPE: {type(uid)}")
    user = User.query.get(uid)
    classes = [uc.clazz for uc in User.userclasses]
    return classes

def insert(email, password, firstname, lastname, bio, school, pfp, notifications):
    """inserts a user"""
    logger.debug(f"adding user with {[email, password, firstname, lastname, bio, school, pfp, notifications]}")
    new_user = User(email=email, password=password, firstname=firstname, lastname=lastname, bio=bio, school=school, pfp=pfp, notifications=notifications)
    db.session.add(new_user)
