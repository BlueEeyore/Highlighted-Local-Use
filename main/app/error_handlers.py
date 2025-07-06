from flask import render_template

def register_error_handlers(app):
    """
    registers all of the app's error handlers
    (to be used in __init__.py)
    """

    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def not_found(e):
        return render_template("errors/500.html"), 500

    # add more error handlers here
