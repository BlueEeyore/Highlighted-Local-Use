from app.routes import db
import random



class UserClass(db.Model):
    __tablename__ = "userclasses"
    uid = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    cid = db.Column(db.Integer, db.ForeignKey("classes.id"), primary_key=True)
    role = db.Column(db.String(50))

    user = db.relationship("User", back_populates="userclasses")
    clazz = db.relationship("Class", back_populates="userclasses")

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text)
    school = db.Column(db.String(255))
    pfp = db.Column(db.String(255))
    notifications = db.Column(db.String(255))

    lessons = db.relationship("Lesson", backref="user")    
    userclasses = db.relationship("UserClass", back_populates="user")


class Class(db.Model):
    __tablename__ = "classes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    joincode = db.Column(db.String(255), nullable=False, unique=True)
    starttime = db.Column(db.String(255), nullable=False)

    lessons = db.relationship("Lesson", backref="clazz")
    userclasses = db.relationship("UserClass", back_populates="clazz")



class Lesson(db.Model):
    __tablename__ = "lessons"
    id = db.Column(db.Integer, primary_key=True)
    creatorid = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    classid = db.Column(db.Integer, db.ForeignKey("classes.id"), nullable=False)
    name = db.Column(db.String(255))
    videofn = db.Column(db.String(255))
    creationtime = db.Column(db.String(255), nullable=False)

    transcripts = db.relationship("Transcript", backref="lesson")
    comments = db.relationship("Comment", backref="lesson")


class Transcript(db.Model):
    __tablename__ = "transcripts"
    id = db.Column(db.Integer, primary_key=True)
    lid = db.Column(db.Integer, db.ForeignKey("lessons.id"), nullable=False)
    timestamp = db.Column(db.String(255))
    text = db.Column(db.Text)


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    lid = db.Column(db.Integer, db.ForeignKey("lessons.id"), nullable=False)
    parentid = db.Column(db.Integer, db.ForeignKey("comments.id"))
    content = db.Column(db.Text)
    uploadtime = db.Column(db.String(255))  # might change to timestamp type later
    anonymous = db.Column(db.Boolean)
    private = db.Column(db.Boolean)
    comtype = db.Column(db.String(50))
    tsrange = db.Column(db.Text)
    ts_offset = db.Column(db.Integer)
    length = db.Column(db.Integer)

    parents = db.relationship("Comment", remote_side=[id], backref="replies")
