from app import app, user, clazz, userclass
from app.routes import db
from faker import Faker


fake = Faker()


def add_users(n=100):
    """adds fake users"""
    for x in range(n):
        user.insert(
                email=fake.email(),
                password=fake.password(),
                firstname=fake.first_name(),
                lastname=fake.last_name(),
                bio=fake.text(max_nb_chars=200),
                school=fake.company(),
                pfp=fake.image(),
                notifications=fake.text(max_nb_chars=5)
        )
    db.session.commit()


def add_classes(n=100):
    """adds fake classes"""
    for x in range(n):
        clazz.insert(
                name=fake.name(),
                joincode=fake.code(),
                starttime=fake.date_time().isoformat()
        )
    db.session.commit()


def add_userclasses(min_cons=0, max_cons = 3):
    """adds connections between fake users and classes"""
    users = User.query.all()
    classes = Class.query.all()

    for user in users:
        # select random number of connections
        cons = random.randint(min_cons, max_cons)

        # select random classes to connect to user
        joined_classes = random.sample(classes, cons)

        # add association to userclass table
        for joined_class in joined_classes:
            userclass.insert(
                    uid=user.id,
                    cid=joined_class.id,
                    role=fake.text(max_nb_chars=10)
            )
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        add_users()
        add_classes()
        add_userclasses()
