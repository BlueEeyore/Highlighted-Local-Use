from .database import Class
from app.routes import db
import logging

logger = logging.getLogger(__name__)


def print_cols():
    """prints the columns of Class"""
    logger.debug("printing class columns")
    for column in Class.__table__.columns:
        print(column.name, column.type)


def all_classes():
    """returns all classes"""
    logger.debug("getting all classes")
    return Class.query.all()


def get_class(cid):
    """returns class for given cid"""
    logger.debug(f"getting class with cid {cid}")
    clazz = Class.query.get(cid)
    return clazz

def get_class_by(col_name, val):
    """queries class"""
    logger.debug(f"getting all classes with column {col_name} and value {val}")

    # finding the column in Class associated with the given column name
    col_attr = getattr(Class, col_name)

    # returning all classes filtered by that column
    return Class.query.filter(col_attr==val).all()


def get_users(cid):
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
