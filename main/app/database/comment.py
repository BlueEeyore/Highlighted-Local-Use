from app.database.models import Comment
from app.database.models import db
from app.logger_config import get_logger
from app import error
import sys

logger = get_logger(__name__)


def print_cols():
    """prints the columns of comment"""
    logger.debug("printing comment columns")
    for column in Comment.__table__.columns:
        print(column.name, column.type)


def all_comments():
    """returns all comments"""
    logger.debug("getting all comments")
    try:
        return Comment.query.all()
    except Exception as e:
        error.push_log("failed to query Comment", e, sys.exc_info())
        return None


def get_comment(cid):
    """returns comment for given cid"""
    logger.debug(f"getting comment with cid {cid}")
    try:
        return Comment.query.get(cid)
    except Exception as e:
        error.push_log("failed to query comments", e, sys.exc_info())
        return None


def get_comment_by(col_name, val):
    """queries comment"""
    logger.debug(f"""getting all comments with
                  column {col_name} and value {val}""")

    # finding the column in Comment associated with the given column name
    logger.debug(f"getting attribute for column {col_name} in Comment")
    try:
        col_attr = getattr(Comment, col_name)
    except AttributeError as e:
        error.push_log(
            f"failed to get attribute for col {col_name} in Comment",
            e,
            sys.exc_info()
        )
        return None

    # returning all comments filtered by that column
    logger.debug(f"returning all comments filtered by column {col_name}")
    return Comment.query.filter(col_attr == val).all()


def get_children(cid):
    """gets all children and grandchildren for given comment id"""
    logger.debug(f"getting children for comment with cid {cid}")
    com = get_comment(cid)
    if not com:
        error.push_log("couldn't find comment")
        return None
    # this long sql query that is used several times throughout this function
    # queries for the replies of the comment and then orders them by
    # upload time
    try:
        children = com.replies.order_by(Comment.uploadtime).all()
    except Exception as e:
        error.push_log(
            "couldn't query replies and order by uploadtime",
            e,
            sys.exc_info()
        )
        return None
    curr_children = children.copy()
    done = False
    while not done:
        next_children = []
        for child in curr_children:
            if child.replies.all():
                next_children.extend(child.replies.order_by(Comment.uploadtime).all())
        if len(next_children) == 0:
            done = True
        children.extend(next_children)
        curr_children = next_children.copy()
    logger.info(f"returning children {children}")
    return children


def insert(
        uid,
        lid,
        parentid,
        content,
        uploadtime,
        anonymous,
        private,
        comtype,
        tsrange,
        ts_start_offset,
        ts_end_offset,
        length
):
    """inserts a comment"""
    logger.debug(f"""adding comment with {[
        uid,
        lid,
        parentid,
        content,
        uploadtime,
        anonymous,
        private,
        comtype,
        tsrange,
        ts_start_offset,
        ts_end_offset,
        length
    ]}""")

    # set new comment instance
    new_comment = Comment(
        uid=uid,
        lid=lid,
        parentid=parentid,
        content=content,
        uploadtime=uploadtime,
        anonymous=anonymous,
        private=private,
        comtype=comtype,
        tsrange=tsrange,
        ts_start_offset=ts_start_offset,
        ts_end_offset=ts_end_offset,
        length=length
    )

    # add new comment to db
    try:
        db.session.add(new_comment)
    except Exception as e:
        error.push_log(
            f"failed to add new comment {new_comment} to db",
            e,
            sys.exc_info
        )
        db.session.rollback()
        return None

    return new_comment
