from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SelectField
from wtforms import TextAreaField, SubmitField, HiddenField, BooleanField
from wtforms.validators import DataRequired, Optional, Length, ValidationError
import os


def file_size_limit(max_size_mb):
    def _file_size_limit(form, field):
        if field.data:
            field.data.stream.seek(0, os.SEEK_END)
            size = field.data.stream.tell()
            field.data.stream.seek(0)
            if size > max_size_mb * 1024 * 1024:
                raise ValidationError(
                    f'File must be smaller than {max_size_mb}MB.'
                )
    return _file_size_limit


# upload video form
class VideoForm(FlaskForm):
    """form for uploading video"""
    video = FileField("Video", validators=[
        FileRequired(),
        FileAllowed(['mp4'], 'mp4 only!'),
        file_size_limit(1000)   # max 1gb
        ])
    name = StringField("Lesson Name", validators=[
        DataRequired(),
        Length(
            min=1,
            max=100,
            message="Lesson name must be between 1 and 100 characters long."
        )
    ])
    model_size = SelectField("Transcription Model Size", choices=[
        ("small", "Small (Fastest)"),
        ("medium", "Medium (Balanced)"),
        ("large", "Large (Most Accurate)")
    ], default="medium")
    submit = SubmitField("Upload File")


# comment reply form
class CommentReplyForm(FlaskForm):
    """form for replying to comments"""
    parentid = HiddenField()
    start_offset = HiddenField()
    end_offset = HiddenField()
    comtype = HiddenField()
    msg = TextAreaField("Reply", validators=[
        DataRequired(),
        Length(
            min=1,
            max=100,
            message="Reply must be between 1 and 100 characters"
        )
    ])
    submit = SubmitField("Submit Reply")


class CommentForm(FlaskForm):
    """form for creating a comment"""
    start_offset = HiddenField()
    end_offset = HiddenField()
    selected_text = HiddenField()   # not really necessary but keeping for now
    comtype = HiddenField()
    comment_text = TextAreaField(validators=[
        DataRequired(),
        Length(
            min=1,
            max=100,
            message="Comment must be between 1 and 100 characters"
        )
    ])
    visibility = SelectField("Visibility", choices=[
        ("standard", "Standard"),
        ("anonymous", "Anonymous"),
        ("private", "Private")
    ])
    is_correction = BooleanField("Correction?")
    submit = SubmitField("Save Comment")


class ClassForm(FlaskForm):
    """form for creating class"""
    name = StringField("Class name", validators=[
        DataRequired(),
        Length(min=3, max=40)
    ])
    school = StringField("School/University (Optional)", validators=[
        Length(max=40)
    ])
    submit = SubmitField("Create")