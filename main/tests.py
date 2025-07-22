from app import create_app
from app.database import user
from app.database.models import db

app = create_app()
app.run(debug=True)


with app.app_context():
    with app.test_request_context():
        db.session.execute(db.text("DELETE FROM sessions"))
        db.session.commit()