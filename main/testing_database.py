from app import app
from app import user
from app.routes import db

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        user.print_cols()
        user.get_user(1)
        print(user.get_classes(uid=1))
