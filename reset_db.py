# reset_db.py
from app import create_app
from app.database.models import db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        confirm = input("⚠️ This will DROP ALL TABLES. Type YES to continue: ")
        if confirm != "YES":
            print("Cancelled.")
            raise SystemExit(0)

        try:
            print("Disabling foreign key checks...")
            with db.engine.begin() as conn:
                conn.exec_driver_sql("PRAGMA foreign_keys = OFF;")

            print("Dropping all tables...")
            db.drop_all()  # no bind needed

            print("Creating all tables...")
            db.create_all()  # no bind needed

            print("Re-enabling foreign key checks...")
            with db.engine.begin() as conn:
                conn.exec_driver_sql("PRAGMA foreign_keys = ON;")

            print("✅ Database reset complete.")
        finally:
            db.session.remove()