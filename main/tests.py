from app import create_app
from app.database import user

app = create_app()
app.run(debug=True)


with app.app_context():
    with app.test_request_context():
        pass