from flask import render_template, abort, current_app, Blueprint, redirect, url_for, request
import os
from app import session_globals
from app.database.models import db
from app.logger_config import get_logger
from app.auth.forms import LoginForm, SignupForm
from werkzeug.utils import secure_filename
from app.database import user
from app.auth.hashing import consistent_hash

logger = get_logger(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
      

auth_bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')


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
            return render_template("login.html", form=form, invalid=True)

        # if user password doesn't match
        if user.get_user(uid).password != password_hash:
            logger.debug("password doesn't match")
            return render_template("login.html", form=form, invalid=True)

        # add uid to session
        session_globals.set("uid", uid)
        next_page = request.args.get("next")
        if next_page:
            logger.debug(f"login successful - redirecting to previous url {next_page} for user with uid {uid}")
            return redirect(next_page)
        logger.debug(f"login successful - redirecting to classes page for user with uid {uid}")
        return redirect(url_for("classes.classes", uid=uid))

    logger.debug("rendering login page")
    return render_template("login.html", form=form, invalid=False)


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
            return render_template("signup.html", form=form, error_msg="Email already taken")

        # checking that everything is valid before inserting into db
        if len(email) > 40:
            logger.debug("email is too long (they hacked the frontend")
            return render_template("signup.html", form=form, error_msg="email too long")
        if len(password) > 30:
            logger.debug("password is too long (they hacked the frontend")
            return render_template("signup.html", form=form, error_msg="password too long")
        if len(first_name) > 50:
            logger.debug("first name is too long (they hacked the frontend")
            return render_template("signup.html", form=form, error_msg="first name too long")
        if len(last_name) > 50:
            logger.debug("last name is too long (they hacked the frontend")
            return render_template("signup.html", form=form, error_msg="last name too long")
        if len(school) > 50:
            logger.debug("school is too long (they hacked the frontend")
            return render_template("signup.html", form=form, error_msg="school too long")
        if len(bio) > 300:
            logger.debug("bio is too long (they hacked the frontend")
            return render_template("signup.html", form=form, error_msg="bio too long")

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


@auth_bp.route("/logout", methods=['GET', 'POST'])
def logout():
    logger.debug("logging out")

    # having the uid in session means that the user is logged in
    # Clearing the session gets rid of the uid
    session.remove("uid")
    return redirect(url_for("home.home"))
