from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField, SelectMultipleField, TextAreaField, FileField, SubmitField, PasswordField
from wtforms.validators import InputRequired, DataRequired, Length


# sample order form that im copying from for dev
class OrderForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=20)])
    topping = RadioField('Pizza Topping',
                         choices=[('Supreme', 'Supreme'), ('Vegetarian', 'Vegetarian'), ('Hawaiian', 'Hawaiian')],
                         validators=[DataRequired()])
    sauce = SelectField('Pizza Sauce', choices=[('Tomato', 'Tomato'), ('BBQ', 'BBQ'), ('Garlic', 'Garlic')],
                        validators=[DataRequired()])
    extras = SelectMultipleField('Optional Extras',
                                 choices=[('Extra Cheese', 'Extra Cheese'), ('Gluten Free Base', 'Gluten Free Base')])
    instructions = TextAreaField('Delivery Instructions')
    submit = SubmitField('Send my Order')


# login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(min=3, max=30)])
    password = PasswordField('Password',validators=[InputRequired('Password required')])
    submit = SubmitField('Login')


# signup form
class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired("Email required"), Length(min=3, max=40)])
    password = PasswordField('Password',validators=[DataRequired('Password required'), Length(min=3, max=30)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=3, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=3, max=50)])
    school = StringField('School', validators=[DataRequired(), Length(min=3, max=50)])
    bio = TextAreaField('Bio (max 300 characters)', validators=[Length(max=300)])
    pfp = FileField('Profile Picture (You can add this later)')
    submit = SubmitField('Sign up')