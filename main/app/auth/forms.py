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
        Length(min=3, max=40)
    ])
    password = PasswordField('Password', validators=[
        DataRequired('Password required'),
        Length(min=3, max=30)
    ])
    first_name = StringField('First Name', validators=[
        DataRequired(),
        Length(min=3, max=50)
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(),
        Length(min=3, max=50)
    ])
    school = StringField('School', validators=[
        DataRequired(),
        Length(min=3, max=50)
    ])
    bio = TextAreaField('Bio (max 300 characters)', validators=[
        Length(max=300)
    ])
    pfp = FileField('Profile Picture (You can add this later)')
    submit = SubmitField('Sign up')
