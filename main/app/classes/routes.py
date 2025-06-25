from flask import render_template, abort, current_app, Blueprint, redirect, url_for, request, jsonify
import os
from app import session_globals, error
from app.transcription import Transcription
from app.logger_config import get_logger
from app.database import clazz, user, lesson, transcript, comment
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
        return redirect(url_for("auth.login", next=request.url))

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

    lessons = clazz.get_lessons(cid)

    return render_template("class.html", lessons=lessons, cid=cid)


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
    
    # getting uid
    logger.debug("getting uid")
    uid = session_globals.get("uid")

    # checking if uid isn't in session, then redirects to login
    if not uid:
        logger.debug("not logged in, redirecting to login")
        return redirect(url_for("auth.login", next=request.url))

    # post request is sent either when user selects "highlight option"
    # or submits a comment
    if request.method == "POST":
        logger.debug("information posted to individual_lesson")
        
        # when user highlights text and either selects "highlight",
        # a request is sent from javascript rather than html
        try:
            if request.is_json:
                logger.debug("""information posted from javascript (meaning
                            user selected highlight)""")
                data = request.get_json()

            # when user submits a comment, post request is sent from html
            else:
                logger.debug("""information posted from html (meaning user 
                             selected comment""")
                data = request.form
        except Exception as e:
            # handle error
            pass
            
        # grabbing information from frontend
        try:
            start_offset = int(data.get("start_offset"))
            end_offset = int(data.get("end_offset"))
            selected_text = data.get("selected_text")   # for debugging
            comtype = data.get("comtype")

            # this could be done earlier in the "if request.is_json" but
            # leaving it separate in case I add more options later
            if comtype == "comment":
                comment_content = data.get("comment_text")
            else:
                comment_content = None
        except Exception as e:
            # handle error
            pass

        logger.debug("inserting new comment")
        new_comment = comment.insert(
            uid=uid,
            lid=lid,
            parentid=None,
            content=comment_content,
            uploadtime=None,
            anonymous=None,
            private=None,
            comtype=comtype,
            tsrange=None,
            ts_start_offset=start_offset,
            ts_end_offset=end_offset,
            length=None
        )
        if not new_comment:
            # handle error
            pass
        db.session.commit()

        # if request.is_json:
        #     logger.debug("sending back succes to javascript frontend")
        #     return jsonify({"status": "success", "highlight": new_comment.to_dict()})
        logger.debug("redirecting back to same page for re-rendering")
        return redirect(url_for("classes.individual_lesson", cid=cid, lid=lid))

    logger.debug("in 'get' section")
    this_lesson = lesson.get_lesson(lid)
    if not this_lesson:
        # handle error
        pass
    saved_comments = this_lesson.comments
    results = {}

    results["creator"] = this_lesson.creatorid
    results["name"] = this_lesson.name
    results["videofn"] = this_lesson.videofn
    results["creationtime"] = this_lesson.creationtime
    results["mime_type"] = this_lesson.mimetype

    # results["video_path"] = os.path.join(os.path.abspath(current_app.config["UPLOAD_FOLDER"]), this_lesson.videofn)

    results["transcripts"] = this_lesson.transcripts
    # results["comments"] = this_lesson.comments

    results["cid"] = cid
    results["lid"] = lid

    # gets dictionary form for every comment
    results["highlights"] = [h.to_dict() for h in saved_comments]
    
    # javascript sends get request when user selects "comment"
    # if user didn't select "comment", these values will just be None
    start_offset = request.args.get("start_offset")
    end_offset = request.args.get("end_offset")
    selected_text = request.args.get("selected_text")
    
    # only occurs when user selected "comment"
    if start_offset and end_offset:
        # make a dictionary with the info for the comment form
        results["comment_form_data"] = {
            "start_offset": start_offset,
            "end_offset": end_offset,
            "selected_text": selected_text
        }

    logger.debug("rendering individual lesson page")
    return render_template("lesson.html", results=results)