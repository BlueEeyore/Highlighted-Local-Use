from app import app
from app import database
from app.routes import db

if __name__ == "__main__":
    db.drop_all()
    db.create_all()
