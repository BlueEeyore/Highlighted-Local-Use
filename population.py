from app import create_app
from app.database import clazz, lesson, transcript
from app.database.models import db
from faker import Faker
import string
import random
from datetime import datetime

fake = Faker()


def unique_joincode(length):
    """generates a unique joincode"""
    while True:
        chars = string.ascii_uppercase + string.digits
        code = ''.join(random.choices(chars, k=length))
        if not clazz.get_class_by("joincode", code):
            return code


def add_classes(n=10):
    """adds fake classes"""
    for x in range(n):
        clazz.insert(
                name=fake.catch_phrase(),
                school=fake.company(),
                joincode=unique_joincode(length=6),
                starttime=datetime.utcnow()
        )
    db.session.commit()


def add_lessons(min_cons=1, max_cons=5):
    """adds lessons"""
    classes = clazz.all_classes()

    for iclazz in classes:
        num_lessons = random.randint(min_cons, max_cons)

        for ilesson in range(num_lessons):
            lesson.insert(
                    classid=iclazz.id,
                    name=fake.bs().title(),
                    videofn="SCIE101_26S1_LecC_Science__Society_And_Me_2026-02-26_22_39_16_stream1.mp4",
                    mimetype="video/mp4",
                    creationtime=datetime.utcnow().isoformat()
            )
    db.session.commit()


def add_transcripts(min_cons=5, max_cons=15):
    """adds transcripts"""
    lessons = lesson.all_lessons()

    for ilesson in lessons:
        num_transcripts = random.randint(min_cons, max_cons)
        
        current_time = 0.0
        for itranscript in range(num_transcripts):
            duration = random.uniform(2.0, 10.0)
            end_time = current_time + duration
            timestamp = f"{current_time}, {end_time}"
            
            transcript.insert_transcript(
                    ilesson.id,
                    [{
                        "timestamp": timestamp,
                        "text": fake.sentence()
                    }]
            )
            current_time = end_time
    db.session.commit()


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Populating classes...")
        add_classes()
        print("Populating lessons...")
        add_lessons()
        print("Populating transcripts...")
        add_transcripts()
        print("Done!")
