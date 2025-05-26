from flask import render_template, abort, current_app, Blueprint
import os
from app.classes.forms import VideoForm
from werkzeug.utils import secure_filename


# basedir = os.path.abspath(os.path.dirname(__file__))
      

classes_bp = Blueprint('classes', __name__, url_prefix='/classes', template_folder='templates')


@classes_bp.route('/<int:cid>/createlesson', methods=['GET', 'POST'])
def create_lesson(cid):
    print("in prac_form")
    form = VideoForm()
    if form.validate_on_submit():
        video = form.video.data
        # video.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),current_app.config["UPLOAD_FOLDER"],secure_filename(video.filename)))
        video.save(os.path.join(os.path.abspath(current_app.config["UPLOAD_FOLDER"]),secure_filename(video.filename)))

        # [save video to database here]


    print("in prac_form")
    return render_template('form.html', form=form)




#if __name__ == "__main__":
#    app.run(debug=True)
