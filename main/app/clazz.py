from .database import Class
import logging

logger = logging.getLogger(__name__)


def print_cols():
    """prints the columns of Class"""
    logger.debug("printing class columns")
    for column in Class.__table__.columns:
        print(column.name, column.type)

def get_user(cid):
    """returns class for given cid"""
    logger.debug(f"getting class with cid {cid}")
    clazz = Class.query.get(cid)
    return clazz

def get_classes(uid):
    """returns users that are in a class"""
    logger.debug(f"getting users in class with {cid}")
    clazz = Class.query.get(cid)
    users = [uc.user for uc in Class.userclasses]
    return users

def insert(name, joincode, starttime):
    """inserts a class"""
    logger.debug(f"adding class with {[name, joincode, starttime]}")
    new_class = Class(name=name, joincode=joincode, starttime=starttime)
    db.session.add(new_class)
