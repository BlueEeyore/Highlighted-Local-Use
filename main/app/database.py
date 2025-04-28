from app.routes import db
from faker import Faker

fake = Faker()


class UserClass(db.Model):
    __tablename__ = "UserClass"
    uid = db.Column(db.Integer, db.ForeignKey("User.id"), primary_key=True)
    cid = db.Column(db.Integer, db.ForeignKey("Class.id"), primary_key=True)
    role = db.Column(db.String(50))


class User(db.Model):
    __tablename__ = "User"
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
    userclasses = db.relationship("UserClass", backref="user")


class Class(db.Model):
    __tablename__ = "Class"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    joincode = db.Column(db.String(255), nullable=False, unique=True)
    starttime = db.Column(db.String(255), nullable=False)

    lessons = db.relationship("Lesson", backref="class")
    comments = db.relationship("Comment", backref="class")
    userclasses = db.relationship("UserClass", backref="class")



class Lesson(db.Model):
    __tablename__ = "Lesson"
    id = db.Column(db.Integer, primary_key=True)
    creatorid = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    classid = db.Column(db.Integer, db.ForeignKey("Class.id"), nullable=False)
    name = db.Column(db.String(255))
    videofn = db.Column(db.String(255))
    creationtime = db.Column(db.String(255), nullable=False)

    transcripts = db.relationship("Transcript", backref="lesson")
    comments = db.relationship("Comment", backref="lesson")


class Transcript(db.Model):
    __tablename__ = "Transcript"
    id = db.Column(db.Integer, primary_key=True)
    lid = db.Column(db.Integer, db.ForeignKey("Lesson.id"), nullable=False)
    timestamp = db.Column(db.String(255))
    text = db.Column(db.Text)


class Comment(db.model):
    __tablename__ = "Comment"
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    lid = db.Column(db.Integer, db.ForeignKey("Lesson.id"), nullable=False)
    parentid = db.Column(db.Integer, db.ForeignKey("Comment.id"))
    content = db.Column(db.Text)
    uploadtime = db.Column(db.String(255))  # might change to timestamp type later
    anonymous = db.Column(db.Boolean)
    private = db.Column(db.Boolean)
    comtype = db.Column(db.String(50))
    tsrange = db.Column(db.Text)
    ts_offset = db.Column(db.Integer)
    length = db.Column(db.Integer)

    parents = db.relationship("Comment", remote_side=[id], backref="replies")
