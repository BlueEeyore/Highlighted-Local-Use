from flask import render_template, abort, current_app, Blueprint, redirect, url_for, request, flash
import os, sys
from app import session_globals, error
from app.database.models import db
from app.logger_config import get_logger
from app.auth.forms import LoginForm, SignupForm
from werkzeug.utils import secure_filename
from app.database import user
from app.auth.hashing import consistent_hash

logger = get_logger(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
      

auth_bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')


@auth_bp.route("/logout")
def logout():
    logger.debug("logging out")
    
    # user is registered as "logged in" when their uid is in session
    # clearing the session removes this uid, so they're logged out
    try:
        session_globals.clear()
    except Exception as e:
        error.push_log("failed to clear session", e, sys.exc_info())
        abort(500)
    return redirect(url_for("main.home"))


@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    logger.debug("in login")

    # login route is the default for the profile page
    # If uid is already in session then the user is already logged in
    if session_globals.get("uid"):
        return redirect(url_for("account.profile", uid=session_globals.get("uid")))

    form = LoginForm()
    if form.validate_on_submit():   # when form is submitted
        logger.debug("form submitted")

        email = form.email.data
        password_hash = consistent_hash(form.password.data)

        logger.debug("getting uid for user with provided email")
        uid = user.get_user_by("email", email)[0].id    # get_user_by returns list

        # if user doesn't exist
        if not uid:
            logger.debug("user not found in db")
            flash("Invalid username or password", "danger")
            return render_template("login.html", form=form)

        # if user password doesn't match
        if user.get_user(uid).password != password_hash:
            logger.debug("password doesn't match")
            flash("Invalid username or password", "danger")
            return render_template("login.html", form=form)

        # add uid to session
        session_globals.set("uid", uid)
        next_page = request.args.get("next")
        if next_page:
            logger.debug(f"login successful - redirecting to previous url {next_page} for user with uid {uid}")
            return redirect(next_page)
        logger.debug(f"login successful - redirecting to classes page for user with uid {uid}")
        return redirect(url_for("classes.classes", uid=uid))

    logger.debug("rendering login page")
    return render_template("login.html", form=form)


@auth_bp.route("/signup", methods=['GET', 'POST'])
def signup():
    logger.debug("in signup")

    form = SignupForm()
    if form.validate_on_submit():   # when form is submitted
        logger.debug("form submitted")

        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        school = form.school.data
        bio = form.bio.data
        pfp = form.pfp.data

        logger.debug(f"checking if user with provided email {email} already exists")
        user_exists = True if user.get_user_by("email", email) else False

        if user_exists:
            logger.debug("user with given email already exists")
            flash("Email already taken", "danger")
            return render_template("signup.html", form=form)

        # checking that everything is valid before inserting into db
        if len(email) > 40:
            logger.debug("email is too long (they hacked the frontend")
            flash("Email too long", "danger")
            return render_template("signup.html", form=form)
        if len(password) > 30:
            logger.debug("password is too long (they hacked the frontend")
            flash("Password too long", "danger")
            return render_template("signup.html", form=form)
        if len(first_name) > 50:
            logger.debug("first name is too long (they hacked the frontend")
            flash("First name too long", "danger")
            return render_template("signup.html", form=form)
        if len(last_name) > 50:
            logger.debug("last name is too long (they hacked the frontend")
            flash("Last name too long", "danger")
            return render_template("signup.html", form=form)
        if len(school) > 50:
            logger.debug("school is too long (they hacked the frontend")
            flash("School too long", "danger")
            return render_template("signup.html", form=form)
        if len(bio) > 300:
            logger.debug("bio is too long (they hacked the frontend")
            flash("Bio too long", "danger")
            return render_template("signup.html", form=form)

        logger.debug("inserting into user table")
        user.insert(
                email=email,
                password=consistent_hash(password),
                firstname=first_name,
                lastname=last_name,
                school=school,
                bio=bio,
                pfp=pfp,
                notifications=None
                )
        db.session.commit()

        uid = user.get_user_by("email", email)[0].id    # get_user_by returns list
        session_globals.set("uid", uid)

        logger.debug("redirecting to classes page for user")
        return redirect(url_for("classes.classes"))


    logger.debug("rendering signup template")
    return render_template("signup.html", form=form, error_msg=False)