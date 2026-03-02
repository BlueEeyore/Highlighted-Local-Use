from flask import Flask
from app.database.models import db
from .logger_config import get_logger
from app.error_handlers import register_error_handlers
from app import session_globals


def create_app():
    # configuring app
    app = Flask(__name__)

    # to get it to log to console:
    # console_handler = logging.StreamHandler()
    # console_handler.setFormatter(formatter)
    # app.logger.addHandler(console_handler)

    # intialise logger (for this file)
    logger = get_logger(__name__)

    # config and initialise db
    logger.debug("initialising db")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    db.init_app(app)

    # configuring session
    logger.debug("configuring session")
    session_globals.session_config(app)

    # register blueprints from different modules
    from app.classes.routes import classes_bp
    app.register_blueprint(classes_bp)

    # config upload folder
    app.config["UPLOAD_FOLDER"] = "app/static/files"

    # register error handlers
    register_error_handlers(app)

    # running routes
    # logger.debug("running app")
    # from app import routes
    # app.run(debug=True)

    return app
