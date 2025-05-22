from flask import Flask
import logging


# configuring app
app = Flask(__name__)


# initialising logger
file_handler = logging.FileHandler("logs.log")
app.logger.addHandler(file_handler)

# to get it to log to console:
#console_handler = logging.StreamHandler()
#console_handler.setFormatter(formatter)
#app.logger.addHandler(console_handler)


logger = logging.getLogger(__name__)


# configuring session
logger.debug("configuring session")
from .session_globals import session_config
session_config(app)


# running routes
logger.debug("running app")
from app import routes
app.run(debug=True)
