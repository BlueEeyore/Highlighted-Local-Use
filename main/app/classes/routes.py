from flask import render_template, abort, current_app, Blueprint, redirect, url_for
import os
from app import session_globals
from app.transcription import Transcription
from app.logger_config import get_logger
from app.database import clazz, user, lesson, transcript
from app.database.models import db
from app.classes.forms import VideoForm
from werkzeug.utils import secure_filename

logger = get_logger(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
      

classes_bp = Blueprint('classes', __name__, url_prefix='/classes', template_folder='templates')


# cannot have uid in route because it redirects to login if not logged in
@classes_bp.route("/", methods=['GET', 'POST'])
def classes():
    logger.debug("in classes")

    # getting uid
    logger.info(f"session globals dict is now {session_globals._get_globs()}")
    uid = session_globals.get("uid")

    # checking if uid isn't in session, then redirects to login
    if not uid:
        return redirect("/auth/login")

    # getting all classes belonging to user
    logger.debug("getting user classes")
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
        fn = secure_filename(video.filename)
        file_path = os.path.join(os.path.abspath(current_app.config["UPLOAD_FOLDER"]), fn)
        video.save(file_path)

        # get mime type for video
        mime_type = video.mimetype

        # insert lesson into db
        uid = session_globals.get("uid")
        new_lesson = lesson.insert(uid, cid, "name", fn, mime_type, "_")  # insert returns id for new row
        db.session.commit()
        
        # transcribe video
        transcriber = Transcription()
        transcript_dict = transcriber.trans_video(file_path)
        transcript.insert_transcript(new_lesson.id, transcript_dict)

        # get the id for the lesson just inserted
        lid = new_lesson.id


        return redirect(url_for("classes.individual_lesson", cid=cid, lid=lid))


    return render_template("create_lesson.html", form=form)


@classes_bp.route("/<int:cid>/<int:lid>", methods=['GET', 'POST'])
def individual_lesson(cid, lid):
    logger.debug("in individual lesson route")

    this_lesson = lesson.get_lesson(lid)
    results = {}

    results["creator"] = this_lesson.creatorid
    results["name"] = this_lesson.name
    results["videofn"] = this_lesson.videofn
    results["creationtime"] = this_lesson.creationtime
    results["mime_type"] = this_lesson.mimetype

    # results["video_path"] = os.path.join(os.path.abspath(current_app.config["UPLOAD_FOLDER"]), this_lesson.videofn)

    results["transcripts"] = this_lesson.transcripts
    results["comments"] = this_lesson.comments


    return render_template("lesson.html", results=results)
