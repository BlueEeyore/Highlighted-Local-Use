from .database import UserClass
import logging

logger = logging.getLogger(__name__)


def print_cols():
    """prints the columns of UserClass"""
    logger.debug("printing user columns")
    for column in UserClass.__table__.columns:
        print(column.name, column.type)

def insert(uid, cid, role):
    """inserts a userclass association"""
    logger.debug(f"adding userclass association with {[uid, cid, role]}")
    new_userclass = UserClass(uid=uid, cid=cid, role=role)
    db.session.add(new_userclass)
