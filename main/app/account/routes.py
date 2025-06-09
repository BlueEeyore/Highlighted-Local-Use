from flask import render_template, abort, current_app, Blueprint
import os
from app.database import user
from app.logger_config import get_logger

logger = get_logger(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
      

account_bp = Blueprint('account', __name__, template_folder='templates')


@account_bp.route("/profile/<int:uid>", methods=['GET', 'POST'])
def profile(uid):
    logger.debug("in profile")

    logger.debug("getting user")
    user_info = user.get_user(uid)

    return render_template("profile.html", user_info=user_info)


@account_bp.route("/settings/<int:uid>", methods=['GET', 'POST'])
def settings(uid):
    logger.debug("in settings")


    return render_template("settings.html")


@account_bp.route("/edit_profile/<int:uid>", methods=['GET', 'POST'])
def edit_profile(uid):
    logger.debug("in edit profile")


    return render_template("edit_profile.html")
