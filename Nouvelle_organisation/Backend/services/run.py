from app import create_app

app = create_app()

if __name__ == '_main_':
    app.run(debug=True)
