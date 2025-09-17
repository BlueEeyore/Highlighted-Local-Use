from flask import render_template
from app import session_globals

def register_error_handlers(app):
    """
    registers all of the app's error handlers
    (to be used in __init__.py)
    """

    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        error_stack = session_globals.get("error_stack")
        stack_trace = error_stack.dump()
        error_stack.clear()
        return render_template("errors/500.html", stack_trace=stack_trace), 500

    # add more error handlers here
