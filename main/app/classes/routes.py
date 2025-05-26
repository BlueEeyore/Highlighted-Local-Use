from flask import render_template, abort, current_app, Blueprint
import os
from app.logger_config import get_logger
from app.database import clazz, user, lesson
from app.classes.forms import VideoForm
from werkzeug.utils import secure_filename

logger = get_logger(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
      

classes_bp = Blueprint('classes', __name__, url_prefix='/classes', template_folder='templates')


@classes_bp.route("/<int:uid>", methods=['GET', 'POST'])
def classes(uid):
    logger.debug("in classes")

    user_classes = user.get_classes(uid)

    return render_template("classes.html", classes=user_classes)


@classes_bp.route("/join", methods=['GET', 'POST'])
def join_class():
    logger.debug("in join_class")

    classes = clazz.all_classes()

    return render_template("join_class.html", classes=classes)


@classes_bp.route("/create", methods=['GET', 'POST'])
def create_class():
    logger.debug("in create_class")


    return render_template("create_class.html")


@classes_bp.route("/<int:cid>", methods=['GET', 'POST'])
def individual_class(cid):
    logger.debug("in individual_class")


    return render_template("class.html")


@classes_bp.route("/<int:cid>/createlesson", methods=['GET', 'POST'])
def create_lesson(cid):
    logger.debug("in create_lesson")

    form = VideoForm()
    if form.validate_on_submit():   # when form is submitted
        logger.debug("form submitted")

        # grab video file and save to static folder
        video = form.video.data
        video.save(os.path.join(os.path.abspath(current_app.config["UPLOAD_FOLDER"]),secure_filename(video.filename)))


        # [save video to database here]


    return render_template("create_lesson.html", form=form)


@classes_bp.route("/<int:cid>/<int:lid>", methods=['GET', 'POST'])
def lesson(cid, lid):
    logger.debug("in lesson")

    this_lesson = lesson.get_lesson(lid)

    creator = this_lesson.user
    name = this_lesson.name
    videofn = this_lesson.videofn
    creationtime = this_lesson.creationtime

    transcripts = this_lesson.transcripts
    comments = this_lesson.comments


    return render_template("lesson.html")
