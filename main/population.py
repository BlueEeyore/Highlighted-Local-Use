from app import create_app
from app.database import user, clazz, userclass, lesson
from app.database.models import db
from faker import Faker
import string
import random
from app.auth.hashing import consistent_hash


fake = Faker()


def unique_joincode(length):
    """generates a unique joincode"""
    while True:
        chars = string.ascii_uppercase + string.digits
        code = ''.join(random.choices(chars, k=length))
        if not clazz.get_class_by("joincode", code):
            return code


def add_users(n=100):
    """adds fake users"""
    for x in range(n-1):
        user.insert(
                email=fake.email(),
                password=consistent_hash(fake.password()),
                firstname=fake.first_name(),
                lastname=fake.last_name(),
                bio=fake.text(max_nb_chars=100),
                school=fake.company(),
                pfp=None,
                notifications=fake.text(max_nb_chars=5)
        )
    user.insert(
            email="test@gmail.com",
            password=consistent_hash("password"),
            firstname="John",
            lastname="Smith",
            bio="random bio",
            school="burnside high school",
            pfp=None,
            notifications=fake.text(max_nb_chars=5)
    )
    db.session.commit()


def add_classes(n=100):
    """adds fake classes"""
    for x in range(n):
        clazz.insert(
                name=fake.text(max_nb_chars=20),
                private=fake.boolean(),
                school=fake.text(max_nb_chars=20),
                joincode=unique_joincode(length=6),
                starttime=fake.date_time().isoformat()
        )
    db.session.commit()


def add_userclasses(min_cons=1, max_cons=50):
    """adds connections between fake users and classes"""
    users = user.all_users()
    classes = clazz.all_classes()

    for sample_class in classes:
        # select sandom number of connections
        cons = random.randint(min_cons, max_cons)

        # select random users to connect to class
        joined_users = random.sample(users, cons)

        # add association to userclass table
        for joined_user in joined_users:
            userclass.insert(
                    uid=joined_user.id,
                    cid=sample_class.id,
                    role=fake.text(max_nb_chars=10)
            )
    db.session.commit()

    ## Below code is to add classes to users
    ## (not the same as adding users to classes)
    ## (must have at least one user in each class)

    # for sample_user in users:
    #     # select random number of connections
    #     cons = random.randint(min_cons, max_cons)

    #     # select random classes to connect to user
    #     joined_classes = random.sample(classes, cons)

    #     # add association to userclass table
    #     for joined_class in joined_classes:
    #         userclass.insert(
    #                 uid=sample_user.id,
    #                 cid=joined_class.id,
    #                 role=fake.text(max_nb_chars=10)
    #         )
    # db.session.commit()


def add_lessons(min_cons=0, max_cons=3):
    """adds lessons"""
    classes = clazz.all_classes()

    for iclazz in classes:
        lessons = random.randint(min_cons, max_cons)
        creator = random.choice(clazz.get_users(iclazz.id))

        for ilesson in range(lessons):
            lesson.insert(
                    creatorid=creator.id,
                    classid=iclazz.id,
                    name=fake.text(max_nb_chars=20),
                    videofn=fake.file_path(),
                    mimetype=fake.mime_type(),
                    creationtime=fake.date_time().isoformat()
            )
    db.session.commit()
                    

def add_transcripts(min_cons=10, max_cons=200):
    """adds transcripts"""
    lessons = lesson.all_lessons()

    for ilesson in lessons:
        transcripts = random.randint(min_cons, max_cons)

        for itranscript in range(transcripts):
            transcript.insert(
                    lid=ilesson.id,
                    timestamp=fake.timestamp(),
                    text=fake.text(max_nb_chars=20)
            )
    db.session.commit()


def add_comments():
    """adds comments"""
    lessons = lesson.all_lessons()
    
    for ilesson in lessons:
        pass
        


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        with app.test_request_context():
            db.drop_all()
            db.create_all()
            add_users()
            add_classes()
            add_userclasses()
            add_lessons()
            
            print(f"all users: {user.all_users()}")
            user.get_user(1)
            print(user.get_classes(uid=1))
