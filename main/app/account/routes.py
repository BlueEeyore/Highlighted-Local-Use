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
    first_name = user_info.firstname
    last_name = user_info.lastname
    bio = user_info.bio
    school = user_info.school

    return render_template(
        "profile.html",
        first_name=first_name,
        last_name=last_name,
        bio=bio,
        school=school
    )


@account_bp.route("/settings/<int:uid>", methods=['GET', 'POST'])
def settings(uid):
    logger.debug("in settings")


    return render_template("settings.html")


@account_bp.route("/edit_profile/<int:uid>", methods=['GET', 'POST'])
def edit_profile(uid):
    logger.debug("in edit profile")


    return render_template("edit_profile.html")
