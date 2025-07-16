from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField, SelectMultipleField, TextAreaField, SubmitField, FileField, HiddenField
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


# upload video form
class VideoForm(FlaskForm):
    """form for uploading video"""
    video = FileField("Video", validators=[InputRequired()])
    submit = SubmitField("Upload File")
    

# comment reply form
class CommentReplyForm(FlaskForm):
    """form for replying to comments"""
    msg = TextAreaField("Reply")
    parentid = HiddenField()
    start_offset = HiddenField()
    end_offset = HiddenField()
    comtype = HiddenField()
    submit = SubmitField("Submit Reply")