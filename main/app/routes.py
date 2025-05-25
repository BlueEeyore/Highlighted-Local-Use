from flask import render_template, abort, current_app, Blueprint
import os
from forms import VideoForm
from werkzeug.utils import secure_filename


basedir = os.path.abspath(os.path.dirname(__file__))
      

import app.database as database



@app.route('/', methods=['GET', 'POST'])
def prac_form():
    print("in prac_form")
    form = VideoForm()
    if form.validate_on_submit():
        video = form.video.data.filename
        video.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),current_app.config["UPLOAD_FOLDER"],secure_filename(video.filename)))

        # [save video to database here]


    print("in prac_form")
    return render_template('form.html', form=form)




#if __name__ == "__main__":
#    app.run(debug=True)
