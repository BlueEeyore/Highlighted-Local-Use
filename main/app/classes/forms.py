from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField, SelectMultipleField, TextAreaField, SubmitField, FileField, HiddenField, BooleanField
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
    name = TextAreaField("Lesson Name", validators=[DataRequired(), Length(min=1, max=100)])
    submit = SubmitField("Upload File")
    

# comment reply form
class CommentReplyForm(FlaskForm):
    """form for replying to comments"""
    parentid = HiddenField()
    start_offset = HiddenField()
    end_offset = HiddenField()
    comtype = HiddenField()
    msg = TextAreaField("Reply", validators=[DataRequired()])
    submit = SubmitField("Submit Reply")


class CommentForm(FlaskForm):
    """form for creating a comment"""
    start_offset = HiddenField()
    end_offset = HiddenField()
    selected_text = HiddenField()   # not really necessary but keeping for now
    comtype = HiddenField()
    comment_text = TextAreaField(validators=[DataRequired()])
    visibility = SelectField("Visibility", choices=[("standard", "Standard"), ("anonymous", "Anonymous"), ("private", "Private")])
    is_correction = BooleanField("Transcript Correction")
    submit = SubmitField("Save Comment")


# class button form (currently unused)
class ClassForm(FlaskForm):
    """gives the id of class clicked on classes page"""
    class_id = HiddenField()
    submit = SubmitField()