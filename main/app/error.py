from app import session_globals
from .logger_config import get_logger

logger = get_logger(__name__)


class LogicalStack:
    def __init__(self):
        self.stack = []

    def push(self, message):
        """adds message on to the end of the LogicalStack"""
        self.stack.append(message)

    def pop(self):
        """removes and returns final item of the LogicalStack"""
        result = self.stack.pop()
        return result

    def dump(self):
        """returns each item of the stack on individual lines"""
        return "\n -".join(self.stack)


def push_error(e):
    """pushes error to stack in session
    if stack not yet in session then adds it to session"""
    error_stack = get_stack()
    error_stack.push(e)


def push_log(msg, e=None, exc_info=None):
    """pushes error to stack in session and logs it"""
    # push error and then msg to error stack
    push_error(msg)
    if e:
        push_error(str(e))

    # log error
    logger.error(msg, exc_info=exc_info)


def get_stack():
    """returns error stack in session if exists
    otherwise initialises in session and returns new stack"""
    logger.debug("getting error stack")
    error_stack = session_globals.get("error_stack")
    if not error_stack:
        logger.debug("error stack not in session. Creating new one")
        error_stack = LogicalStack()
        session_globals.set("error_stack", error_stack)
    return error_stack


if __name__ == "__main__":
    # test
    trace = LogicalStack()
    trace.push("Initialize system")
    trace.push("Load config")
    trace.push("Connect to DB")

    print(trace.dump())
