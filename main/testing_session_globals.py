from app import session_globals
from app import app


with app.test_request_context("/"):
    print("start test")
    session_globals.set("hi", 1)
    print(session_globals.get("hi"))
    session_globals.increment("hi")
    session_globals.print_dict()
    session_globals.decrement("hi")
    session_globals.print_dict()
