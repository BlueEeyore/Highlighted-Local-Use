from app.database.models import UserClass
from app.database.models import db
from app.logger_config import get_logger
from app import error
import sys

logger = get_logger(__name__)


def print_cols():
    """prints the columns of UserClass"""
    logger.debug("printing user columns")
    for column in UserClass.__table__.columns:
        print(column.name, column.type)

def insert(uid, cid, role):
    """inserts a userclass association"""
    logger.debug(f"adding userclass association with {[uid, cid, role]}")

    # setting new userclass instance
    new_userclass = UserClass(uid=uid, cid=cid, role=role)

    # adding new userclass association to db
    try:
        db.session.add(new_userclass)
    except Exception as e:
        error.push_log(f"failed to add new userclass {new_userclass} to db", e, sys.exc_info())
        db.session.rollback()
        return None
    return new_userclass
