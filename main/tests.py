from app import create_app, transcription

app = create_app()
app.run(debug=True)


with app.app_context():
    with app.test_request_context():
        transcription.test()
