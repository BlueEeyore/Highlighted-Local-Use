from flask import render_template, abort, current_app, Blueprint
import os
from app.logger_config import get_logger

logger = get_logger(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
      

admin_bp = Blueprint('admin', __name__, template_folder='templates')


@admin_bp.route("/notifications/<int:uid>", methods=['GET', 'POST'])
def notifications(uid):
    logger.debug("in notifications")


    return render_template("notifications.html")


@admin_bp.route("/settings/<int:uid>", methods=['GET', 'POST'])
def settings(uid):
    logger.debug("in settings")


    return render_template("settings.html")
