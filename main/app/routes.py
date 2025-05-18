from app import app
from flask import render_template, abort
from flask_sqlalchemy import SQLAlchemy
import os


basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Hello_21!@localhost:3306/13dtp'
db.init_app(app)
      

import app.database as database







#if __name__ == "__main__":
#    app.run(debug=True)
