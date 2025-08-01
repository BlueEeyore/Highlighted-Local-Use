from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


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
    pfp = db.Column(db.LargeBinary)
    notifications = db.Column(db.String(255))

    lessons = db.relationship("Lesson", backref="user")    
    userclasses = db.relationship("UserClass", back_populates="user")
    comments = db.relationship("Comment", back_populates="user")

    def full_name(self):
        """converts object into full name of user"""
        return f"{self.firstname} {self.lastname}"


class Class(db.Model):
    __tablename__ = "classes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    joincode = db.Column(db.String(255), nullable=False, unique=True)
    starttime = db.Column(db.String(255), nullable=False)

    lessons = db.relationship("Lesson", backref="clazz")
    userclasses = db.relationship("UserClass", back_populates="clazz")

    def to_dict(self):
        """helper to convert object into dict"""
        return {
            "id": self.id,
            "name": self.name,
            "joincode": self.joincode,
            "starttime": self.starttime
        }



class Lesson(db.Model):
    __tablename__ = "lessons"
    id = db.Column(db.Integer, primary_key=True)
    creatorid = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    classid = db.Column(db.Integer, db.ForeignKey("classes.id"), nullable=False)
    name = db.Column(db.String(255))
    videofn = db.Column(db.String(255))
    mimetype = db.Column(db.String(255))
    creationtime = db.Column(db.String(255), nullable=False)

    transcripts = db.relationship("Transcript", backref="lesson")
    comments = db.relationship("Comment", backref="lesson")

    def to_dict(self):
        """helper function to convert object into dictionary form"""
        return {
            "id": self.id,
            "creatorid": self.creatorid,
            "classid": self.classid,
            "name": self.name,
            "videofn": self.videofn,
            "mimetype": self.mimetype,
            "creationtime": self.creationtime,
            "creator": f"{self.user.firstname} {self.user.lastname}"
        }



class Transcript(db.Model):
    __tablename__ = "transcripts"
    id = db.Column(db.Integer, primary_key=True)
    lid = db.Column(db.Integer, db.ForeignKey("lessons.id"), nullable=False)
    timestamp = db.Column(db.String(255))
    text = db.Column(db.Text)

    def to_dict(self):
        """helper to convert object to dict form"""
        start, end = [float(x) for x in self.timestamp.split(", ")]
        return {
            "id": self.id,
            "lid": self.lid,
            "start_ts": start,
            "end_ts": end,
            "text": self.text
        }


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
    tsrange = db.Column(db.Text)    # delete later
    ts_start_offset = db.Column(db.Integer)
    ts_end_offset = db.Column(db.Integer)
    length = db.Column(db.Integer)

    user = db.relationship("User", back_populates="comments")
    replies = db.relationship(
        "Comment",
        backref=db.backref("parent", remote_side=[id]),
        lazy="dynamic",
        single_parent=True,
        cascade="all, delete-orphan"    # deletes children when parent is deleted
    )

    def to_dict(self):
        """helper to convert the object to a dictionary"""
        return {
            "id": self.id,
            "uid": self.uid,
            "lid": self.lid,
            "parentid": self.parentid,
            "content": self.content,
            "uploadtime": self.uploadtime,
            "anonymous": self.anonymous,
            "private": self.private,
            "comtype": self.comtype,
            "tsrange": self.tsrange,
            "ts_start_offset": self.ts_start_offset,
            "ts_end_offset": self.ts_end_offset,
            "length": self.length,
            "creator": f"{self.user.firstname} {self.user.lastname}"
        }