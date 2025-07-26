from flask import render_template, abort, current_app, Blueprint, redirect, url_for, request, jsonify
import os
from app import session_globals, error
from app.transcription import Transcription
from app.logger_config import get_logger
from app.database import clazz, user, lesson, transcript, comment
from app.database.models import db
from app.classes.forms import VideoForm, CommentReplyForm, ClassForm
from werkzeug.utils import secure_filename
import sys

logger = get_logger(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
      

classes_bp = Blueprint('classes', __name__, url_prefix='/classes', template_folder='templates')


# cannot have uid in route because it redirects to login if not logged in
@classes_bp.route("/", methods=['GET', 'POST'])
def classes():
    logger.debug("in classes")

    # getting uid
    uid = session_globals.get("uid")

    # checking if uid isn't in session, then redirects to login
    if not uid:
        return redirect(url_for("auth.login", next=request.url))

    # getting all classes belonging to user
    logger.debug("getting user classes")
    user_classes = user.get_classes(uid)

    class_dicts = [user_class.to_dict() for user_class in user_classes]
    # class_forms = []
    # for user_class in user_classes:
    #     class_form = ClassForm(prefix=f"{user_class.id}-")
    #     class_form.class_id.data = user_class.id
    #     class_forms.append(class_form)

    # classes_data = list(zip(class_dicts, class_forms))

    return render_template("classes.html", classes_data=class_dicts)


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
    
    # getting uid
    uid = session_globals.get("uid")

    # checking if uid isn't in session, then redirects to login
    if not uid:
        return redirect(url_for("auth.login", next=request.url))

    # getting all lessons in class
    logger.debug("getting user classes")
    lessons = clazz.get_lessons(cid)

    # get dictionary form for each lesson
    lesson_dicts = [less.to_dict() for less in lessons]
    lesson_dicts.sort(key=lambda x:x["creationtime"])   # sort by creation time

    logger.debug("rendering individual class template")
    return render_template("class.html", lessons=lesson_dicts, cid=cid)


@classes_bp.route("/<int:cid>/createlesson", methods=['GET', 'POST'])
def create_lesson(cid):
    logger.debug("in create_lesson")
    
    # getting uid
    logger.debug("getting uid")
    uid = session_globals.get("uid")

    # checking if uid isn't in session, then redirects to login
    if not uid:
        logger.debug("not logged in, redirecting to login")
        return redirect(url_for("auth.login", next=request.url))

    form = VideoForm()
    if form.validate_on_submit():   # when form is submitted
        logger.debug("video form submitted")

        # grab lesson name
        lesson_name = form.name.data

        # grab video file and save to static folder
        video = form.video.data
        fn = secure_filename(video.filename)
        file_path = os.path.join(os.path.abspath(current_app.config["UPLOAD_FOLDER"]), fn)
        video.save(file_path)

        # get mime type for video
        mime_type = video.mimetype

        # insert lesson into db
        uid = session_globals.get("uid")
        new_lesson = lesson.insert(uid, cid, lesson_name, fn, mime_type, "_")  # insert returns id for new row
        db.session.commit()
        
        # transcribe video
        logger.debug("about to transcribe video")
        transcriber = Transcription()
        transcript_dict = transcriber.trans_video(file_path)
        transcript.insert_transcript(new_lesson.id, transcript_dict)
        logger.info("successfully inserted transcript")

        # get the id for the lesson just inserted
        lid = new_lesson.id

        logger.debug("redirecting to individual_lesson route")
        return redirect(url_for("classes.individual_lesson", cid=cid, lid=lid))


    logger.debug("rendering create_lesson template")
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

    # preparing the results dict that will be passed to frontend
    results = {}

    # gets every comment in dictionary form
    this_lesson = lesson.get_lesson(lid)
    if not this_lesson:
        error.push_log("failed to find lesson that corresponds with url lid")
        abort(500)
    saved_comments = this_lesson.comments
    results["highlights"] = [h.to_dict() for h in saved_comments]
    logger.info(f"HIGHLIGHTS: {results['highlights']}")

    # sorts by start offset and then end offset and then id
    results["highlights"].sort(key = lambda x : [x["ts_start_offset"], x["ts_end_offset"], x["id"]])

    parentid = None # if the submittion isn't a replies this will remain as None
    reply_forms = {}
    for highlight in results["highlights"]:
        if highlight["comtype"] in ["comment", "reply"]:
            # set up individual reply form for each comment
            form = CommentReplyForm(prefix=f"{highlight['id']}-") # prefix to distinguish forms
            # form = CommentReplyForm()
            form.start_offset.data = highlight["ts_start_offset"]
            form.end_offset.data = highlight["ts_end_offset"]
            form.parentid.data = highlight["id"]
            form.comtype.data = highlight["comtype"]

            reply_forms[highlight['id']] = (highlight, form)

            # if comment reply form was submitted
            if form.validate_on_submit():
                logger.debug("comment reply form submitted")

                # getting data from form submission
                comment_content = form.msg.data
                parentid = int(form.parentid.data)
                start_offset = int(form.start_offset.data)
                end_offset = int(form.end_offset.data)
                comtype = "reply"
    
    # now make comment data into a nice frontend-friendly format
    children_forms = []
    for com_id in reply_forms:
        if reply_forms[com_id][0]["comtype"] == "comment":
            replies = comment.get_children(com_id)
            if replies is None:
                error.push_log("failed to get comment replies")
                abort(500)
            children_forms.append((reply_forms[com_id], tuple([reply_forms[reply.id] for reply in replies])))
            # children_forms is now of format
            # [((parent_dict, form), ((child_dict1, form), (child_dict2, form)...))...]

    # get a dict of the standalone highlights (not attached to comments or replies)
    standalone_highlights = [h for h in results["highlights"] if h["comtype"]=="highlight"]

    # post request is sent when any of the following occur:
    # - user selects "highlight option"
    # - user submits a comment
    # - a reply form was submitted
    if request.method == "POST":
        logger.debug("information posted to individual_lesson")

        # parentid is None if submission wasn't a reply
        if parentid is None:
            # when user highlights text and selects "highlight" or "jump to text",
            # a request is sent from javascript rather than html
            if request.is_json:
                logger.debug("""information posted from javascript (meaning
                            user selected highlight)""")
                try:
                    data = request.get_json()
                except Exception as e:
                    error.push_log("failed to get form from js frontend", e, sys.exc_info)
                    abort(500)

            # when user submits a comment, post request is sent from html
            else:
                logger.debug("""information posted from html (meaning user 
                            selected comment""")
                try:
                    data = request.form
                except Exception as e:
                    error.push_log("failed to get form from html frontend", e, sys.exc_info)
                    abort(500)
                
            # grabbing information from frontend
            try:
                # redirecting to same page with video timestamp info if
                # post request was sent due to user clicking "jump to timestamp"
                posttype = data.get("posttype")
                if posttype == "timestamp":
                    ts = data.get("timestamp")
                    session_globals.set("video_timestamp", ts)
                    return redirect(url_for("classes.individual_lesson", cid=cid, lid=lid))

                start_offset = int(data.get("start_offset"))
                end_offset = int(data.get("end_offset"))
                selected_text = data.get("selected_text")   # for debugging
                comtype = data.get("comtype")
                logger.info(start_offset)

                # this could be done earlier in the "if request.is_json" but
                # leaving it separate in case I add more options later
                if comtype == "comment":
                    comment_content = data.get("comment_text")
                else:
                    comment_content = None
            except Exception as e:
                error.push_log("failed to grab data from frontend form", e, sys.exc_info)
                abort(500)

        # insert new comment/highlight
        new_comment = comment.insert(
            uid=uid,
            lid=lid,
            parentid=parentid,
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
            error.push_log("failed to insert new comment")
            abort(500)
        db.session.commit()

        # if request.is_json:
        #     logger.debug("sending back success to javascript frontend")
        #     return jsonify({"status": "success", "highlight": new_comment.to_dict()})
        logger.debug("redirecting back to same page for re-rendering")
        return redirect(url_for("classes.individual_lesson", cid=cid, lid=lid))

    logger.debug("in 'get' section")

    results["creator"] = this_lesson.creatorid
    results["name"] = this_lesson.name
    results["videofn"] = this_lesson.videofn
    results["creationtime"] = this_lesson.creationtime
    results["mime_type"] = this_lesson.mimetype

    results["video_timestamp"] = session_globals.get("video_timestamp")
    if results["video_timestamp"] is not None:
        session_globals.remove("video_timestamp")

    # results["video_path"] = os.path.join(os.path.abspath(current_app.config["UPLOAD_FOLDER"]), this_lesson.videofn)

    results["transcripts"] = this_lesson.transcripts

    results["cid"] = cid
    results["lid"] = lid
    
    # javascript sends get request when user selects "comment"
    # if user didn't select "comment", these values will just be None
    start_offset = request.args.get("start_offset")
    end_offset = request.args.get("end_offset")
    selected_text = request.args.get("selected_text")
    
    
    if start_offset and end_offset:     # only occurs when user selected "comment"
        # make a dictionary with the info for the comment form
        results["comment_form_data"] = {
            "start_offset": start_offset,
            "end_offset": end_offset,
            "selected_text": selected_text
        }
    
    parent_comments = [com[0][0] for com in children_forms]

    logger.debug("rendering individual lesson page")
    logger.info(f"COMMENT DICTS: {children_forms}")
    logger.info(f"PARENT DICTS: {parent_comments}")
    return render_template(
        "lesson.html",
        results=results,
        comment_forms=children_forms,
        parent_comments_json=parent_comments,
        standalone_highlights_json=standalone_highlights
        )