from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import TextAreaField, FileField, SubmitField, PasswordField
from wtforms.validators import InputRequired, DataRequired, Length


# login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Length(min=3, max=30)
    ])
    password = PasswordField('Password', validators=[
        InputRequired('Password required')
    ])
    submit = SubmitField('Login')


# signup form
class SignupForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired("Email required"),
        Length(
            min=3,
            max=40,
            message="Email needs to be 3-40 characters"
        )
    ])
    password = PasswordField('Password', validators=[
        DataRequired('Password required'),
        Length(
            min=3,
            max=30,
            message="Password needs to be 3-30 characters"
        )
    ])
    first_name = StringField('First Name', validators=[
        DataRequired(),
        Length(
            min=3,
            max=50,
            message="First name needs to be 3-50 characters"
        )
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(),
        Length(
            min=3,
            max=50,
            message="Last name needs to be 3-50 characters"
        )
    ])
    school = StringField('School', validators=[
        DataRequired(),
        Length(
            min=3,
            max=50,
            message="School needs to be 3-50 characters"
        )
    ])
    bio = TextAreaField('Bio (max 300 characters)', validators=[
        Length(
            max=300,
            message="Bio can't be longer than 300 characters"
        )
    ])
    pfp = FileField('Profile Picture (You can add this later)')
    submit = SubmitField('Sign up')
