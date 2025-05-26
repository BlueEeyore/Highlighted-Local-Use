from flask import render_template, abort, current_app, Blueprint
import os
from .logger_config import get_logger
from app.classes.forms import VideoForm
from werkzeug.utils import secure_filename

logger = get_logger(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
      

auth_bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')


@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    logger.debug("in login")


    return render_template("login.html")


@auth_bp.route("/signup", methods=['GET', 'POST'])
def signup():
    logger.debug("in signup")


    return render_template("signup.html")
