from flask import render_template, abort, Blueprint, redirect, url_for
import os
from app.logger_config import get_logger
from app import session_globals, error

logger = get_logger(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
      

main_bp = Blueprint('main', __name__, template_folder='templates')


@main_bp.route("/", methods=['GET', 'POST'])
def home():
    logger.debug("in home")

    # getting uid
    uid = session_globals.get("uid")

    # checking if uid isn't in session, meaning user isn't logged in
    if not uid:
        is_logged = False
    else:
        is_logged = True

    return render_template("home.html", is_logged=is_logged)
