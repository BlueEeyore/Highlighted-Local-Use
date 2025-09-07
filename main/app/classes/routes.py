from flask import render_template, abort, current_app, Blueprint, redirect, url_for, request, jsonify, flash
import os
from app import session_globals, error
from app.transcription import Transcription
from app.logger_config import get_logger
from app.database import clazz, user, lesson, transcript, comment, userclass
from app.database.models import db, Comment, Class, UserClass
from app.classes.forms import VideoForm, CommentReplyForm, CommentForm, ClassForm, JoinClassForm
from werkzeug.utils import secure_filename
from datetime import datetime
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

    # getting uid
    uid = session_globals.get("uid")

    # checking if uid isn't in session, then redirects to login
    if not uid:
        return redirect(url_for("auth.login", next=request.url))

    join_form = JoinClassForm()
    classid = None 

    # when "join class" button clicked
    if request.method == "POST":
        logger.info(join_form.is_submitted())
        logger.info(join_form.validate())
        if join_form.validate_on_submit():
            joincode = join_form.joincode.data
            class_joined = clazz.get_class_by("joincode", joincode)
            if len(class_joined) == 0:
                flash("Class does not exist", "danger")
            else:
                classid = class_joined[0].id
        else:
            classid = request.form["classid"]
        
        # adding user to new class
        if classid:
            conn = userclass.insert(uid=uid, cid=classid, role="student")
            if not conn:
                error.push_log("failed to add new userclass connection")
                abort(500)
            try:
                db.session.commit()
            except Exception as e:
                error.push_log("failed to commit to db", e, sys.exc_info())
                abort(500)

    # getting all public classes user is not a part of and converting objects to dictionary form
    classes = clazz.get_filtered(
        Class.private == False,
        ~Class.userclasses.any(UserClass.uid == uid)    # user is not a part of
    )
    class_dicts = [cla.to_dict() for cla in classes]

    logger.debug("rendering join_class template")
    return render_template("join_class.html", classes=class_dicts, join_form=join_form)


@classes_bp.route("/create", methods=['GET', 'POST'])
def create_class():
    logger.debug("in create_class")

    # getting uid
    uid = session_globals.get("uid")

    # checking if uid isn't in session, then redirects to login
    if not uid:
        return redirect(url_for("auth.login", next=request.url))

    # initialising the class creation form
    form = ClassForm()

    # if the class creation form is submitted
    if form.validate_on_submit():
        logger.debug("form submitted. Grabbing form data")
        name = form.name.data
        school = form.school.data
        private = True if form.privacy.data == "private" else False
        joincode = clazz.generate_unique_joincode()
        
        logger.debug("inserting new class into db")
        new_class = clazz.insert(creatorid=uid,
                                 name=name,
                                 private=private,
                                 school=school,
                                 joincode=joincode,
                                 starttime=datetime.utcnow())
        if not new_class:
            error.push_log("failed to create new class")
            abort(500)
        try:
            db.session.commit()
        except Exception as e:
            error.push_log("failed to commit to db", e, sys.exc_info())
            abort(500)
        logger.debug("new class inserted successfully")

        logger.debug("redirecting to new class page")
        logger.info(new_class)
        return redirect(url_for("classes.individual_class", cid=new_class.id))

    logger.debug("rendering class creation template")
    return render_template("create_class.html", form=form)


@classes_bp.route("/<int:cid>", methods=['GET', 'POST'])
def individual_class(cid):
    logger.debug("in individual_class")
    
    # getting uid
    uid = session_globals.get("uid")

    # checking if uid isn't in session, then redirects to login
    if not uid:
        return redirect(url_for("auth.login", next=request.url))

    # get class
    this_class = clazz.get_class(cid)
    if not this_class:
        error.push_log("class does not exist")
        abort(404)

    # get class name
    class_name = this_class.name

    # get join code
    joincode = this_class.joincode

    # getting all lessons in class
    logger.debug("getting user classes")
    lessons = clazz.get_lessons(cid)

    # get dictionary form for each lesson
    lesson_dicts = [less.to_dict() for less in lessons]
    lesson_dicts.sort(key=lambda x:x["creationtime"])   # sort by creation time

    role = userclass.get_role(uid=uid, cid=cid)
    if role is None:
        error.push_log("failed to get user role")
        abort(500)

    logger.debug("rendering individual class template")
    return render_template(
        "class.html",
        lessons=lesson_dicts,
        cid=cid,
        class_name=class_name,
        role=role,
        joincode=joincode
    )


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
        new_lesson = lesson.insert(  # insert returns id for new row
            uid,
            cid,
            lesson_name,
            fn,
            mime_type,
            datetime.utcnow())
        if not new_lesson:
            error.push_log("failed to create new lesson")
            abort(500)
        try:
            db.session.commit()
        except Exception as e:
            error.push_log("failed to commit to db", e, sys.exc_info())
            abort(500)
        
        # transcribe video
        logger.debug("about to transcribe video")
        transcriber = Transcription()
        transcript_dict = transcriber.trans_video(file_path)
        transcript.insert_transcript(new_lesson.id, transcript_dict)
        logger.debug("successfully inserted transcript")

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

    # flag for if forms have already had data grabbed
    post_handled = False

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

    # presetting new comment aspects.
    parentid = None
    anonymous = None
    private = None


    reply_forms = {}
    for highlight in results["highlights"]:
        visible = not (highlight["private"] and (highlight["uid"] != uid))
        if highlight["comtype"] in ["comment", "correction", "reply"] and visible:
            # set up individual reply form for each comment
            form = CommentReplyForm(prefix=f"{highlight['id']}-") # prefix to distinguish forms
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
                post_handled = True
    
    # make comment data into a frontend-friendly format
    children_forms = []
    for com_id in reply_forms:
        if reply_forms[com_id][0]["comtype"] in ["comment", "correction"]:
            replies = comment.get_children(com_id)
            if replies is None:
                error.push_log("failed to get comment replies")
                abort(500)
            children_forms.append((reply_forms[com_id], tuple([reply_forms[reply.id] for reply in replies])))
            # children_forms is now of format
            # [((parent_dict, form), ((child_dict1, form), (child_dict2, form)...))...]

    # get a dict of the standalone highlights (not attached to comments or replies)
    standalone_highlights = [h for h in results["highlights"] if h["comtype"]=="highlight" and h["uid"]==uid]


    # javascript sends get request when user selects "comment"
    # if user didn't select "comment", these values will just be None
    temp_start_offset = request.args.get("start_offset")
    temp_end_offset = request.args.get("end_offset")
    temp_selected_text = request.args.get("selected_text")
    new_comment_form = CommentForm()
    if temp_start_offset and temp_end_offset:     # only occurs when user selected "comment"
        # form with the info for the comment
        logger.debug("User selected 'comment'. Preparing comment form")
        new_comment_form.start_offset.data = temp_start_offset
        new_comment_form.end_offset.data = temp_end_offset
        new_comment_form.selected_text.data = temp_selected_text
        results["new_comment_form"] = new_comment_form

        # temporary highlight for pending comment
        temp_highlight = {
            "id": None,
            "uid":uid,
            "lid":lid,
            "parentid":None,
            "content":None,
            "uploadtime":None,
            "anonymous":None,
            "private":None,
            "comtype":"setting",
            "tsrange":None,
            "ts_start_offset":temp_start_offset,
            "ts_end_offset":temp_end_offset,
            "length":None
        }
        standalone_highlights.append(temp_highlight)   
    if new_comment_form.validate_on_submit():
        comment_content = new_comment_form.comment_text.data
        start_offset = int(new_comment_form.start_offset.data)
        end_offset = int(new_comment_form.end_offset.data)

        comtype = "comment"
        is_correction = new_comment_form.is_correction.data
        if is_correction:
            comtype = "correction"

        visibility = new_comment_form.visibility.data
        if visibility == "anonymous":
            anonymous = True
        elif visibility == "private":
            private = True

        # flagging that the post request has been handled and comment can just immediately be inserted
        post_handled = True


    # post request is sent when any of the following occur:
    # - user selects "highlight option"
    # - user submits a comment
    # - a reply form was submitted
    if request.method == "POST":
        logger.debug("information posted to individual_lesson")

        # parentid is None if submission wasn't a reply
        if not post_handled:
            # when user highlights text and selects "highlight" or "jump to text",
            # a request is sent from javascript rather than html
            if request.is_json:
                logger.debug("""information posted from javascript (meaning
                            user selected highlight)""")
                try:
                    data = request.get_json()
                except Exception as e:
                    error.push_log("failed to get form from js frontend", e, sys.exc_info())
                    abort(500)

            # when user submits a comment, post request is sent from html
            else:
                logger.debug("""information posted from html (meaning user 
                            selected comment""")
                try:
                    data = request.form
                except Exception as e:
                    error.push_log("failed to get form from html frontend", e, sys.exc_info())
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

                # this could be done earlier in the "if request.is_json" but
                # leaving it separate in case I add more options later
                if comtype in ["comment", "correction"]:
                    comment_content = data.get("comment_text")
                else:
                    comment_content = None
            except Exception as e:
                error.push_log("failed to grab data from frontend form", e, sys.exc_info())
                abort(500)

        # insert new comment/highlight
        new_comment = comment.insert(
            uid=uid,
            lid=lid,
            parentid=parentid,
            content=comment_content,
            uploadtime=None,
            anonymous=anonymous,
            private=private,
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

    # convert transcript segments to dict form with start and end timestamps
    results["transcripts"] = [ts.to_dict() for ts in this_lesson.transcripts]

    results["uid"] = uid
    results["cid"] = cid
    results["lid"] = lid
    
    results["user"] = user.get_user(uid).full_name()
    
    parent_comments = [com[0][0] for com in children_forms]

    logger.debug("rendering individual lesson page")
    return render_template(
        "lesson.html",
        results=results,
        comment_forms=children_forms,
        parent_comments_json=parent_comments,
        standalone_highlights_json=standalone_highlights
        )