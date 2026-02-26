from app.database.models import UserClass, db
from app.logger_config import get_logger
from app import error
import sys

logger = get_logger(__name__)


def print_cols():
    """prints the columns of UserClass"""
    logger.debug("printing user columns")
    for column in UserClass.__table__.columns:
        print(column.name, column.type)


def get_role(uid, cid):
    """returns role of user with uid in class with cid"""
    logger.debug(f"getting role with uid {uid} and cid {cid}")
    try:
        user_class = UserClass.query.filter_by(cid=cid, uid=uid).first()
    except Exception as e:
        error.push_log("failed to query UserClass", e, sys.exc_info())
        return None

    if user_class:
        role = user_class.role
    else:
        error.push_log("couldn't find role associated with user and class")
        return None

    return role


def insert(uid, cid, role):
    """inserts a userclass association"""
    logger.debug(f"adding userclass association with {[uid, cid, role]}")

    # setting new userclass instance
    new_userclass = UserClass(uid=uid, cid=cid, role=role)

    # adding new userclass association to db
    try:
        db.session.add(new_userclass)
    except Exception as e:
        error.push_log(
            f"failed to add new userclass {new_userclass} to db",
            e,
            sys.exc_info()
        )
        db.session.rollback()
        return None
    return new_userclass
