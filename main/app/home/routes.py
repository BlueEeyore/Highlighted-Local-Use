from flask import render_template, abort, current_app, Blueprint
import os
from app.logger_config import get_logger

logger = get_logger(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
      

home_bp = Blueprint('home', __name__, template_folder='templates')


@home_bp.route("/", methods=['GET', 'POST'])
def home():
    logger.debug("in home")


    return render_template("home.html")
