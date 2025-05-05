from app import app
from app import database
from app.routes import db

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        database.print_user_cols()
