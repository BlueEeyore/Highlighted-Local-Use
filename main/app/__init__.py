import logging
logger = logging.getLogger(__name__)


# configuring app
logger.debug("configuring app")
from flask import Flask
app = Flask(__name__)

# configuring session
logger.debug("configuring session")
from .session_globals import session_config
session_config(app)

# running routes
logger.debug("running app")
from app import routes
app.run(debug=True)
