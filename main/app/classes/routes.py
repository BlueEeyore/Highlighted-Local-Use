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
    logger.info(f"session globals dict is now {session_globals._get_globs()}")
    uid = session_globals.get("uid")

    # checking if uid isn't in session, then redirects to login
    if not uid:
        return redirect(url_for("auth.login", next=request.url))

    if request.method == "POST":
        print('information posted')
        if request.is_json:
            data = request.get_json()
            print(f"text highlighted: {data['text']}")
            
            start = data.get("start_offset")
            end = data.get("end_offset")
            comtype = data.get("comtype")

            if comtype == "comment":
                comment_content = data.get("comment")
            else:
                comment_content = None

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
                ts_start_offset=start,
                ts_end_offset=end,
                length=None
            )
            db.session.commit()

            print(new_comment.to_dict())
            return jsonify({"status": "success", "highlight": new_comment.to_dict()})

        else:
            start_offset = int(request.form["start_offset"])
            end_offset = int(request.form["end_offset"])
            selected_text = request.form["selected_text"]
            comment_content = request.form["comment_text"]

            new_comment = comment.insert(
                uid=uid,
                lid=lid,
                parentid=None,
                content=comment_content,
                uploadtime=None,
                anonymous=None,
                private=None,
                comtype="comment",
                tsrange=None,
                ts_start_offset=start_offset,
                ts_end_offset=end_offset,
                length=None
            )
            db.session.commit()

            return redirect(url_for("classes.individual_lesson", cid=cid, lid=lid))

    start_offset = request.args.get("start_offset")
    end_offset = request.args.get("end_offset")
    selected_text = request.args.get("selected_text")

    this_lesson = lesson.get_lesson(lid)
    saved_comments = comment.get_comment_by("lid", lid)
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

    results["highlights"] = [h.to_dict() for h in saved_comments]

    if start_offset and end_offset:
        results["comment_form_data"] = {
            "start_offset": start_offset,
            "end_offset": end_offset,
            "selected_text": selected_text
        }

    return render_template("lesson.html", results=results)
