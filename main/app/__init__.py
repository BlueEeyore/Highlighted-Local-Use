from flask import Flask
from .database import db
from .logger_config import get_logger


def create_app():
    # configuring app
    app = Flask(__name__)


    # to get it to log to console:
    #console_handler = logging.StreamHandler()
    #console_handler.setFormatter(formatter)
    #app.logger.addHandler(console_handler)


    # intialise logger (for this file)
    logger = get_logger(__name__)


    # config and initialise db
    logger.debug("initialising db")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Hello_21!@localhost:3306/13dtp'
    db.init_app(app)


    # register blueprints from different modules
    from app.classes.routes import classes_bp
    app.register_blueprint(classes_bp)


    # configuring session
    logger.debug("configuring session")
    from .session_globals import session_config
    session_config(app)


    # config upload folder
    app.config["UPLOAD_FOLDER"] = "app/static/files"


    # config secret key
    app.config["SECRET_KEY"] = "super-secret-key"


    # running routes
    # logger.debug("running app")
    # from app import routes
    # app.run(debug=True)


    return app
