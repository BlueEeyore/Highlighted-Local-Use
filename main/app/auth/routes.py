from flask import render_template, abort, current_app, Blueprint
import os
from .logger_config import get_logger
from app.auth.forms import LoginForm, SignupForm
from werkzeug.utils import secure_filename

logger = get_logger(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
      

auth_bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')


@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    logger.debug("in login")

    form = LoginForm()
    if form.validate_on_submit():   #when form is submitted
        logger.debug("form submitted")

        email = form.email.data
        password = form.password.data




    return render_template("login.html")


@auth_bp.route("/signup", methods=['GET', 'POST'])
def signup():
    logger.debug("in signup")


    return render_template("signup.html")
